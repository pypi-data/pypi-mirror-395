from copy import deepcopy
import glob

import matplotlib.pyplot as plt
import numpy as np
from numpy.testing import assert_allclose
import os
import pytest
import unittest

from tests import TEST_PATH, OUT_PATH
from starred.deconvolution.deconvolution import Deconv, setup_model, load_Deconv_model
from starred.deconvolution.loss import Prior
from starred.deconvolution.parameters import ParametersDeconv
from starred.utils.noise_utils import propagate_noise
from starred.utils.ds9reg import export_astrometry_as_ds9region
from starred.procedures.deconvolution_routines import multi_steps_deconvolution
from starred.plots.plot_function import plot_deconvolution, view_deconv_model, make_movie

plt.switch_backend('Agg')


class TestOptim(unittest.TestCase):
    def setUp(self):
        self.path = TEST_PATH
        self.outpath = OUT_PATH
        self.datapath = os.path.join(self.path, "data")
        self.noisepath = os.path.join(self.path, "noise_map")
        self.psfpath = os.path.join(self.path, "psf")

    def test_multi_epochs(self):
        gain = 2
        data = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.datapath, 'des_quasar*.npy')))]) * gain
        psf = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.psfpath, 's_*_01_2021.npy')))])
        epochs = len(psf)
        subsampling_factor = 2
        M = 2
        _, im_size, _ = np.shape(data)
        # Noise map
        sigma_2 = np.zeros((epochs, im_size, im_size))
        sigma_sky_2 = np.array([np.std(data[i, int(0.9 * im_size):, int(0.9 * im_size):]) for i in range(epochs)]) ** 2
        for i in range(epochs):
            sigma_2[i, :, :] = sigma_sky_2[i] + data[i, :, :].clip(min=0)

        # Parameter initialization
        initial_c_x = np.array([-2.2, 2.75])
        initial_c_y = np.array([-4.5, 1.5])
        initial_a = 6 * np.array([data[i, :, :].max() for i in range(epochs) for j in range(M)])

        model, kwargs_init, kwargs_up, kwargs_down, kwargs_fixed = \
            setup_model(data, sigma_2, psf, initial_c_x, initial_c_y, subsampling_factor, initial_a=initial_a)

        parameters = ParametersDeconv(kwargs_init,
                                      kwargs_fixed,
                                      kwargs_up=kwargs_up,
                                      kwargs_down=kwargs_down)

        prior = Prior(prior_analytic=[['c_x', initial_c_x, 5.], ['c_y', initial_c_y, 5.]], prior_background=None)
        prior_list = [prior, None, prior]
        kwargs_lbfgs = {'maxiter': 10}
        kwargs_optax = {'max_iterations': 100}
        fitting_sequence = [['background'], ['pts-source-astrometry', 'pts-source-photometry'], []]
        optim_list = ['l-bfgs-b', 'adabelief', 'adabelief']
        kwargs_optim_list = [kwargs_lbfgs, kwargs_optax, kwargs_optax]
        model, parameters, loss, kwargs_partial_list, fig_list, LogL_list, loss_history_list = multi_steps_deconvolution(
            data,
            model,
            parameters,
            sigma_2,
            psf,
            subsampling_factor,
            fitting_sequence=fitting_sequence,
            optim_list=optim_list,
            kwargs_optim_list=kwargs_optim_list,
            lambda_scales=1,
            lambda_hf=1000,
            lambda_positivity_bkg=100,
            lambda_positivity_ps=0,
            lambda_pts_source=0.,
            prior_list=prior_list,
            adjust_sky=False, verbose=True)

        kwargs_final = kwargs_partial_list[-1]
        deconv, h = model.getDeconvolved(kwargs_final, 0)
        flux0 = model.flux_at_epoch(kwargs_final, epoch=0)

        # test parallel function:
        model_loop = model.model(kwargs_final)
        copy_model = deepcopy(model)
        copy_model._model = copy_model.modelstack
        model_para = copy_model.model(kwargs_final)
        assert_allclose(model_para, model_loop, rtol=1.5e-1)

        # test the export
        model.export(self.outpath, kwargs_final, data, sigma_2, format='fits', epoch=0)
        model.export(self.outpath, kwargs_final, data, sigma_2, format='fits', epoch=[0, 1])
        model.export(self.outpath, kwargs_final, data, sigma_2, format='npy')
        with self.assertRaises(NotImplementedError):
            model.export(self.outpath, kwargs_final, data, sigma_2, format='unknown format')

        model.dump(os.path.join(self.outpath, 'model_deconvolution.pkl'), kwargs_final, format='pkl')
        model.dump(os.path.join(self.outpath, 'model_deconvolution.hdf5'), kwargs_final, data, sigma_2,
                   save_output_level=5, format='hdf5')
        with self.assertRaises(NotImplementedError):
            model.dump(os.path.join(self.outpath, 'model_deconvolution.xxx'), kwargs_final, format='unknown format')

        model_rec, kwargs_rec, data_rec, sigma_2_rec = load_Deconv_model(
            os.path.join(self.outpath, 'model_deconvolution.pkl'), format='pkl')
        model_rec, kwargs_rec, data_rec, sigma_2_rec = load_Deconv_model(
            os.path.join(self.outpath, 'model_deconvolution.hdf5'), format='hdf5')
        with self.assertRaises(NotImplementedError):
            _, _, _, _ = load_Deconv_model(os.path.join(self.outpath, 'model_deconvolution.xxx'),
                                           format='unknown format')

        # test the plots
        plot_deconvolution(model, data, sigma_2, psf, kwargs_final, epoch=0, units='e-')
        view_deconv_model(model, kwargs_final, data, sigma_2)
        make_movie(model, kwargs_final, data, sigma_2, self.outpath, format='gif')

        # This requires installation that are too heavy for the Docker. Skip this part
        # make_movie(model, kwargs_final, data, sigma_2, self.outpath, format='mp4v')

        # Export point source astrometry in the format of ds9region
        export_astrometry_as_ds9region(model, self.outpath, kwargs_final, header=None, regsize=1.)

        # test class updates.
        W = propagate_noise(model, np.sqrt(sigma_2), kwargs_init, wavelet_type_list=['starlet'], method='MC',
                            num_samples=50,
                            seed=1, likelihood_type='chi2', verbose=False, upsampling_factor=2)[0]
        loss.update_weights(W)

        # assert raise:
        with self.assertRaises(ValueError):
            multi_steps_deconvolution(data, model, parameters, sigma_2, psf, subsampling_factor,
                                      fitting_sequence=[['unknown']], optim_list=[['adabelief']], prior_list=None)

        with self.assertRaises(AssertionError):
            multi_steps_deconvolution(data, model, parameters, sigma_2, psf, subsampling_factor,
                                      fitting_sequence=fitting_sequence, optim_list=[['adabelief']])

    def test_padding(self):
        data = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.datapath, 'des_quasar*.npy')))])
        psf = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.psfpath, 's_*_01_2021.npy')))])
        nepoch, im_size, _ = np.shape(data)

        psf_cut = np.array([psf[i, 1:-1, 1:-1] for i in range(nepoch)])
        psf_cut2 = np.array([psf[i, 1:, 1:] for i in range(nepoch)])
        print(np.shape(psf_cut))

        model = Deconv(image_size=im_size,
                       scale=1,
                       number_of_sources=2,
                       upsampling_factor=2,
                       epochs=len(psf),
                       psf=psf_cut)

        with self.assertRaises(RuntimeError):
            model2 = Deconv(image_size=im_size,
                            scale=1,
                            number_of_sources=2,
                            upsampling_factor=2,
                            epochs=len(psf),
                            psf=psf_cut2)

        assert_allclose(model.psf, psf, atol=2e-3)

    def test_raise(self):
        s = np.zeros((1, 64, 64))
        with self.assertRaises(NotImplementedError):
            Deconv(image_size=80, number_of_sources=0, scale=1, convolution_method='unknown', psf=s)

        with self.assertRaises(TypeError):
            Deconv(image_size=80, number_of_sources=0, scale=1, convolution_method='lax', psf=None)

        with self.assertRaises(RuntimeError):
            data = np.zeros((1, 64, 64))
            sigma_2 = np.zeros((1, 63, 63))
            s = np.zeros((1, 64, 64))
            _ = setup_model(data, sigma_2, s, [], [], 1, [])

        with self.assertRaises(RuntimeError):
            data, sigma_2, s = np.zeros((1, 64, 64)), np.zeros((1, 64, 64)), np.zeros((1, 64, 64))
            _ = setup_model(data, sigma_2, s, [1, 1], [1, 1, 1], 1)

        with self.assertRaises(RuntimeError):
            data, sigma_2, s = np.zeros((1, 64, 64)), np.zeros((1, 64, 64)), np.zeros((2, 64, 64))
            _ = setup_model(data, sigma_2, s, [1, 1], [1, 1, 1], 1)

        with self.assertRaises(RuntimeError):
            data, sigma_2, s = np.zeros((1, 64, 64)), np.zeros((1, 64, 64)), np.zeros((1, 64, 64))
            _ = setup_model(data, sigma_2, s, [1, 1, 1], [1, 1, 1], 1, initial_a=[1, 1, 1, 1])


if __name__ == '__main__':
    pytest.main()
