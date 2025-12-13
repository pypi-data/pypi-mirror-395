import glob

import matplotlib.pyplot as plt
import numpy as np
import os
import pytest
import unittest
import pyregion

from tests import TEST_PATH, OUT_PATH
from starred.optim.optimization import Optimizer
from starred.optim.sampling import Sampler
from starred.psf.psf import PSF, load_PSF_model
from starred.psf.loss import Loss
from starred.psf.parameters import ParametersPSF
from starred.procedures.psf_routines import run_multi_steps_PSF_reconstruction, update_PSF
from starred.utils.noise_utils import propagate_noise
from starred.utils.generic_utils import Upsample
from starred.optim.inference_base import FisherCovariance
from numpy.testing import assert_allclose, assert_array_equal, assert_array_almost_equal
from starred.plots.plot_function import plot_loss, plot_convergence_by_walker


class TestOptim(unittest.TestCase):
    def setUp(self):
        self.path = TEST_PATH
        self.outpath = OUT_PATH
        self.datapath = os.path.join(self.path, "data")
        self.noisepath = os.path.join(self.path, "noise_map")
        self.data = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.datapath, 'star*.npy')))])

        self.N, self.image_size, _ = np.shape(self.data)
        self.norm = self.data[0].max() / 100.
        self.data /= self.norm
        self.sigma_2 = np.zeros((self.N, self.image_size, self.image_size))
        sigma_sky_2 = np.array([np.std(self.data[i, int(0.9 * self.image_size):, int(0.9 * self.image_size):]) for i in
                                range(self.N)]) ** 2
        for i in range(self.N):
            self.sigma_2[i, :, :] = sigma_sky_2[i] + self.data[i, :, :].clip(min=0)
        self.subsampling_factor = 2

    def testoptim_psf(self):
        masks = np.ones((self.N, self.image_size, self.image_size))
        for i in range(self.N):
            possiblemaskfilepath = os.path.join(self.noisepath, 'mask_%s.reg' % str(i))
            if os.path.exists(possiblemaskfilepath):
                r = pyregion.open(possiblemaskfilepath)
                masks[i, :, :] = 1 - r.get_mask(shape=(self.image_size, self.image_size)).astype(float)

        model = PSF(image_size=self.image_size, number_of_sources=self.N, upsampling_factor=self.subsampling_factor)
        kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = model.smart_guess(self.data, fixed_background=False,
                                                                              guess_method='barycenter')
        kwargs_init2, _, _, _ = model.smart_guess(self.data, fixed_background=True, guess_method='max')

        parameters = ParametersPSF(kwargs_init, kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down)
        initial_values_kwargs = parameters.initial_values(as_kwargs=True)
        kwargs_lbfgs = {'maxiter': 10}
        kwargs_optax = {'max_iterations': 100}
        model, parameters, loss, kwargs_partial_list, LogL_list, loss_history_list = run_multi_steps_PSF_reconstruction(
            self.data, model, parameters, self.sigma_2, lambda_scales=2.,
            lambda_hf=2., lambda_positivity=0,
            kwargs_optim_list=[kwargs_lbfgs, kwargs_optax], method_noise='SLIT',
            optim_list=['Newton-CG', 'adabelief'], regularize_full_psf=False)

        assert_array_almost_equal(loss.data, self.data, decimal=5)
        assert_array_almost_equal(loss.sigma_2, self.sigma_2, decimal=5)

        kwargs_partial = kwargs_partial_list[-2]
        kwargs_final = kwargs_partial_list[-1]
        fig_loss = plot_loss(loss_history_list[-1], title='Loss history')

        # test updates of the parameters
        for key1 in initial_values_kwargs.keys():
            for key2 in initial_values_kwargs[key1].keys():
                assert_array_almost_equal(np.asarray(initial_values_kwargs[key1][key2]),
                                          np.asarray(kwargs_init[key1][key2]), decimal=5)

        parameters._update_arrays()
        parameters.update_kwargs(kwargs_final, kwargs_fixed, kwargs_up, kwargs_down)

        estimated_full_psf = model.model(**kwargs_final)[0].reshape(64, 64)
        full_psf = model.get_full_psf(**kwargs_final, high_res=False)

        # testing export function
        model.export(self.outpath, kwargs_final, self.data, self.sigma_2, format='fits')
        model.export(self.outpath, kwargs_final, self.data, self.sigma_2, format='npy')
        with self.assertRaises(NotImplementedError):
            model.export(self.outpath, kwargs_final, self.data, self.sigma_2, format='unknown format')

        masks = np.ones((self.N, self.image_size, self.image_size))
        model.dump(os.path.join(self.outpath, 'model.pkl'), kwargs_final, self.norm, format='pkl')
        model.dump(os.path.join(self.outpath, 'model.hdf5'), kwargs_final, self.norm,
                   self.data, self.sigma_2, masks, save_output_level=4, format='hdf5')
        with self.assertRaises(NotImplementedError):
            model.dump(os.path.join(self.outpath, 'model.xxx'), kwargs_final, self.norm,
                       self.data, self.sigma_2, masks, save_output_level=4, format='unknown format')

        # test reloading of the model
        model_rec, kwargs_final2_rec, norm_rec, data_rec, sigma_2_rec, masks_rec = load_PSF_model(
            os.path.join(self.outpath, 'model.hdf5'), format='hdf5')
        model_rec_pkl, kwargs_final2_rec_pkl, norm_rec_pkl, _, _, _ = load_PSF_model(
            os.path.join(self.outpath, 'model.pkl'), format='pkl')

        # testing the photometry and astrometry
        amp = np.asarray(model.get_amplitudes(**kwargs_final), dtype=np.float32)

        photom_high_res = np.asarray(
            model.get_photometry(**kwargs_final, high_res=True) * self.norm / self.subsampling_factor ** 2,
            dtype=np.float32)
        photom = np.asarray(model.get_photometry(**kwargs_final) * self.norm, dtype=np.float32)
        astrometry = np.asarray(model.get_astrometry(**kwargs_final), dtype=np.float32)
        astrometry_exp = np.asarray([[-0.22521159, -0.06270967],
                                     [0.5312724, -0.13701367],
                                     [0.33560187, 0.03471055]]
                                    , dtype=np.float32)

        # check that this vector is constant :
        assert_allclose(amp / photom, np.asarray([(amp / photom)[0] for i in range(self.N)]), rtol=5e-2)
        assert_allclose(photom, photom_high_res, rtol=5e-2)
        assert_allclose(astrometry, astrometry_exp, atol=0.1)

        # test class updates
        W = propagate_noise(model, np.sqrt(self.sigma_2), kwargs_partial, wavelet_type_list=['starlet'], method='SLIT',
                            num_samples=50,
                            seed=1, likelihood_type='chi2', verbose=False, upsampling_factor=2)[0]
        loss.update_dataset(self.data, self.sigma_2, W, parameters)

        # test other configuration for the PSF model:
        model.include_moffat = False
        background = model.get_narrow_psf(**kwargs_final, norm=False)
        assert_allclose(background, kwargs_final['kwargs_background']['background'].reshape(
            self.image_size * self.subsampling_factor, self.image_size * self.subsampling_factor), atol=1e-8)

    def test_optax(self):
        model = PSF(image_size=self.image_size, number_of_sources=self.N, upsampling_factor=self.subsampling_factor,
                    elliptical_moffat=True)
        kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = model.smart_guess(self.data, fixed_background=True)
        parameters = ParametersPSF(kwargs_init, kwargs_fixed, kwargs_up, kwargs_down)
        loss = Loss(self.data, model, parameters, self.sigma_2, N=self.N, masks=None, regularization_terms='l1_starlet',
                    regularization_strength_scales=1, regularization_strength_hf=1,
                    regularization_strength_positivity=0, W=None, regularize_full_psf=False)

        optim1 = Optimizer(loss, parameters, method='adam')
        optim2 = Optimizer(loss, parameters, method='adabelief')
        optim3 = Optimizer(loss, parameters, method='radam')

        optim1.minimize(parameters, max_iterations=10, min_iterations=1, schedule_learning_rate=False,
                        stop_at_loss_increase=True, progress_bar=False,
                        return_param_history=True)
        optim1.minimize(parameters, max_iterations=10, min_iterations=1, schedule_learning_rate=True,
                        stop_at_loss_increase=True, progress_bar=False,
                        return_param_history=True)
        optim2.minimize(parameters, max_iterations=10, min_iterations=1, schedule_learning_rate=False)
        optim3.minimize(parameters, max_iterations=10, min_iterations=1, schedule_learning_rate=False)
        optim3.minimize(parameters, max_iterations=10, min_iterations=1, schedule_learning_rate=True)

    def test_sky_background(self):
        model = PSF(image_size=self.image_size, number_of_sources=self.N, upsampling_factor=self.subsampling_factor,
                    elliptical_moffat=True)
        kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = model.smart_guess(self.data, fixed_background=True,
                                                                              adjust_sky=True)
        parameters = ParametersPSF(kwargs_init, kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down)
        loss = Loss(self.data, model, parameters, self.sigma_2, N=self.N, masks=None,
                    regularization_terms='l1_starlet',
                    regularization_strength_scales=0,
                    regularization_strength_hf=0,
                    regularization_strength_positivity=1)

        optim1 = Optimizer(loss, parameters, method='adabelief')
        best_fit, logL_best_fit, extra_fields, runtime = optim1.minimize(max_iterations=20, min_iterations=1)
        print(best_fit)
        kwargs_final = parameters.args2kwargs(best_fit)
        assert_allclose(kwargs_final['kwargs_background']['mean'], np.zeros(self.N), atol=2e-1)

    def test_scipyminimize(self):
        model = PSF(image_size=self.image_size, number_of_sources=self.N, upsampling_factor=self.subsampling_factor)
        kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = model.smart_guess(self.data, fixed_background=True)
        parameters = ParametersPSF(kwargs_init, kwargs_fixed, kwargs_up, kwargs_down)
        loss = Loss(self.data, model, parameters, self.sigma_2, N=self.N, masks=None, regularization_terms='l1_starlet',
                    regularization_strength_scales=1, regularization_strength_hf=1,
                    regularization_strength_positivity=0, W=None, regularize_full_psf=False)

        optim1 = Optimizer(loss, parameters, method='BFGS')
        optim1.minimize(maxiter=2, restart_from_init=True)

        optim2 = Optimizer(loss, parameters, method='l-bfgs-b')
        optim2.minimize(maxiter=2, restart_from_init=True)

        optim3 = Optimizer(loss, parameters, method='GradientDescent')
        optim3.minimize(maxiter=2, restart_from_init=True)

        optim4 = Optimizer(loss, parameters, method='LBFGS')
        optim4.minimize(maxiter=2, restart_from_init=True)

        # test Fisher matrix
        fish = FisherCovariance(parameters, optim2)
        fish.compute_fisher_information()
        a = fish.covariance_matrix
        samples = fish.draw_samples(num_samples=100, seed=1)
        sigmas = fish.get_kwargs_sigma()
        interior, exterior = fish.split_matrix(a, 2, 4)

        # test sampling with emcee
        sampler = Sampler(loss, parameters, sampler='emcee')
        kwargs_sampler = {
            'walker_ratio': 3,
            'nsteps': 3,
            'sigma_init': 1e-2
        }
        args_init = parameters.kwargs2args(kwargs_init)
        samples_emcee, logL_emcee, runtime_emcee = sampler.sample(args_init, **kwargs_sampler)
        free_param = parameters.get_all_free_param_names(kwargs_init)
        ndim  = len(args_init)
        n_walkers = kwargs_sampler['walker_ratio'] * ndim
        fig_walkers = plot_convergence_by_walker(samples_emcee, free_param, n_walkers, verbose=True)

        #test sampling with HMC
        sampler_hmc = Sampler(loss, parameters, sampler='mchmc')
        kwargs_sampler_hmc = {'num_steps': 50, 'num_chains': 5, 'sigma_init': 1e-1}
        samples_hmc, logl_hmc, runtime_hmc = sampler_hmc.sample(args_init, **kwargs_sampler_hmc)

    def test_update_PSF(self):
        init_back = Upsample(np.median(self.data, axis=0), factor=self.subsampling_factor)
        kernel_new, narrow_PSF, psf_list, starred_output = update_PSF(init_back, self.data, self.sigma_2, masks=None,
                                                            lambda_scales=2,
                                                            lambda_hf=2, lambda_positivity=0,
                                                            subsampling_factor=self.subsampling_factor,
                                                            optim_list=None,
                                                            kwargs_optim_list=None,
                                                            normalise_data=False)

        model, parameters, loss, kwargs_partial_list, LogL_list, loss_history_list, _ = starred_output
        chi2 = loss.reduced_chi2(kwargs_partial_list[-1])
        assert chi2 < 1.

    def test_raise(self):
        model = PSF(image_size=self.image_size, number_of_sources=self.N, upsampling_factor=self.subsampling_factor)
        kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = model.smart_guess(self.data, fixed_background=True)
        with self.assertRaises(ValueError):
            _ = model.smart_guess(self.data, fixed_background=True, guess_method='unknown')
        parameters = ParametersPSF(kwargs_init, kwargs_fixed, kwargs_up, kwargs_down)
        masks = np.ones((self.N, self.image_size, self.image_size))

        loss = Loss(self.data, model, parameters, self.sigma_2, N=self.N,
                    masks=masks,
                    regularization_terms='l1_starlet',
                    regularization_strength_scales=0,
                    regularization_strength_hf=0)

        assert_array_equal(loss.masks, masks)

        with self.assertRaises(NotImplementedError):
            Optimizer(loss, parameters, method='unknown')

        with self.assertRaises(NotImplementedError):
            optim = Optimizer(loss, parameters)
            optim.method = 'unknown'
            optim.minimize()

        with self.assertRaises(NotImplementedError):
            optim = Optimizer(loss, parameters)
            optim.method = 'unknown'
            optim._run_optax(parameters, schedule_learning_rate=True)

        with self.assertRaises(NotImplementedError):
            optim = Optimizer(loss, parameters)
            optim.method = 'unknown'
            optim._run_optax(parameters, schedule_learning_rate=False)

        with self.assertRaises(ValueError):
            optim = Optimizer(loss, parameters)
            optim.loss_history

        with self.assertRaises(ValueError):
            optim = Optimizer(loss, parameters)
            optim.param_history

        with self.assertRaises(KeyError):
            parameters.get_param_names_for_model('unknown')


if __name__ == '__main__':
    pytest.main()
