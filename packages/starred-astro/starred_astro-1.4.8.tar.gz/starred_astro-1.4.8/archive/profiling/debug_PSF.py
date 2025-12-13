import glob
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import os

from copy import deepcopy
from matplotlib import colors

from starred.psf.psf import PSF
from starred.psf.loss import Loss
from starred.optim.optimization import Optimizer
from starred.optim.inference_base import InferenceBase
from starred.psf.parameters import ParametersPSF
from starred.plots import plot_function as ptf
from starred.utils.noise_utils import propagate_noise
from starred.utils.generic_utils import save_fits
import jax.scipy.optimize
import scipy.optimize
from scipy.optimize import Bounds

import time

# Parameters
def main():
    subsampling_factor = 2
    n_iter_initial = 20
    n_iter = 60
    gain = 2 # WFI camera
    t_exp = 1 # because images are in ADU
    lambda_scales = 600
    lambda_hf = 1000
    # method = 'trust-constr'
    # method = 'L-BFGS-B'
    data_path = '../notebooks/data/1_observations'
    output_folder = './outputs/PSF'
    plot =True

    # Data
    time_run_vec = []
    sizes = [1]
    for s in sizes:
        file_paths = sorted(glob.glob(os.path.join(data_path, '*_001.npy')))
        print('Using %i images '%len(file_paths))
        new_vignets_data = np.array([np.load(f) for f in file_paths]) * t_exp / gain
        N = len(file_paths) # number of stars
        image_size = np.shape(new_vignets_data)[1] # data dimensions
        resize = int(int(image_size) / (2*s))
        new_vignets_data = new_vignets_data[:, int(image_size/2)-resize:int(image_size/2)+resize, int(image_size/2)-resize:int(image_size/2)+resize ]
        image_size = np.shape(new_vignets_data)[1]  # data dimensions
        image_size_up = image_size * subsampling_factor

        print('Image size :', image_size)

        # Noise map estimation
        sigma_2 = np.zeros((N, image_size, image_size))
        sigma_sky_2 = np.array(
            [np.std(new_vignets_data[i, int(0.9 * image_size):, int(0.9 * image_size):]) for i in range(N)]) ** 2
        for i in range(N):
            sigma_2[i, :, :] = sigma_sky_2[i] + new_vignets_data[i, :, :].clip(min=0)

        # Positions
        x0_est = np.array([0. for i in range(N)])
        y0_est = np.array([0. for i in range(N)])

        if plot :
            fig = ptf.display_data(new_vignets_data, sigma_2=sigma_2, units='e-')
            plt.show()

        # Parameter initialization
        initial_fwhm = 0.3
        initial_beta = 0.9
        # initial_a = np.array(np.sum(new_vignets_data, axis=(1,2)))
        # a_norm = initial_a[0]
        # initial_a = initial_a / a_norm
        initial_a = np.array([np.median(new_vignets_data, axis=0).max() for i in range(N)])
        a_norm = 5e2 * initial_a[0]
        initial_a = initial_a / a_norm

        initial_background = np.zeros((image_size_up ** 2))

        # Calling the PSF model
        model = PSF(image_size= image_size, number_of_sources=N, upsampling_factor=subsampling_factor, a_norm=a_norm,
                    convolution_method='fft')
        kwargs_init = {
            'kwargs_moffat': {'fwhm': initial_fwhm, 'beta': initial_beta},
            'kwargs_gaussian': {'a': initial_a, 'x0': x0_est, 'y0':y0_est},
            'kwargs_background': {'background': initial_background},
        }
        kwargs_fixed = {
            'kwargs_moffat': {},
            'kwargs_gaussian': {},
            # 'kwargs_background': {},
            'kwargs_background': {'background':initial_background},
        }

        kwargs_up = {
            'kwargs_moffat': {'fwhm': np.inf, 'beta': np.inf},
            'kwargs_gaussian': {'a':list([np.inf for i in range(N)]),
                                 'x0':list([image_size*subsampling_factor for i in range(N)]),
                                 'y0':list([image_size*subsampling_factor for i in range(N)])
                                 },
            # 'kwargs_background': [{'background': list([np.inf for i in range(image_size_up**2)])}],
            'kwargs_background': {},
        }

        kwargs_down = {
            'kwargs_moffat': {'fwhm': 0., 'beta': 0.},
            'kwargs_gaussian': {'a': list([0 for i in range(N)]),
                                 'x0': list([-image_size*subsampling_factor for i in range(N)]),
                                 'y0': list([-image_size*subsampling_factor for i in range(N)]),
                                 },
            'kwargs_background': {},
            # 'kwargs_background': {'background': list([np.inf for i in range(image_size_up ** 2)])},
        }

        method = 'trust-constr'
        #newton-CG with gradient (scipy) --> 5 iteration, 7 loss evaluation, 34 gradient evaluation, 0 hvp evaluation, run in 7.01s
        #newton-CG with hvp (scipy) --> 5 iteration, 7 loss evaluation, 7 gradient evaluation, 15 hvp evaluation, run in 11.01s

        parameters = ParametersPSF(kwargs_init, kwargs_fixed, kwargs_up, kwargs_down)
        args_init = parameters.kwargs2args(kwargs_init)

        bounds = parameters.get_bounds()

        loss = Loss(new_vignets_data, model, parameters, sigma_2, N, regularization_terms='l1_starlet',
                    regularization_strength_scales=0, regularization_strength_hf=0)
        inf = InferenceBase(loss, parameters)

        start_time = time.perf_counter()
        optim = Optimizer(loss, parameters, method=method)
        # res = jax.scipy.optimize.minimize(inf.loss, args_init, method= method, tol=None, options={'maxiter':50})
        # res = scipy.optimize.minimize(inf.loss, args_init, jac=inf.gradient, method= method, tol=None, options={'maxiter':50})
        # res = scipy.optimize.minimize(inf.loss, args_init, jac=inf.gradient, hessp=inf.hessian_vec_prod, method= method, tol=None, **extra_kwargs) #trust-constr
        # res = scipy.optimize.minimize(inf.loss, args_init, jac=inf.gradient, method= method, tol=None, **extra_kwargs) #trust-constr
        # res = scipy.optimize.minimize(inf.loss, args_init, jac=inf.gradient, hessp=inf.hessian_vec_prod, method= method, tol=None, options={'maxiter':50})
        best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(maxiter=n_iter_initial, restart_from_init=True,
                                                                            use_grad=True, use_hessian=False, use_hvp=True)

        print('Run time : ', time.perf_counter() - start_time)
        # print(res)
        # print(parameters.args2kwargs(res.x))
        print('Best fit :',best_fit)
        print('LogL best :', logL_best_fit)
        print('Res :', extra_fields)
        print('Runtime :' , runtime)

        # Retrieving different elements of the PSF
        # kwargs_final = parameters.args2kwargs(res.x)
        kwargs_final = parameters.args2kwargs(best_fit)
        print(kwargs_final)
        fig = ptf.single_PSF_plot(model, new_vignets_data, sigma_2, kwargs_final, n_psf=0, units='e-')
        plt.show()

        #dfefix backgorun
        kwargs_fixed = {
            'kwargs_moffat': {},
            'kwargs_gaussian': {},
            'kwargs_background': {},
        }
        kwargs_up = {
            'kwargs_moffat': {'fwhm': np.inf, 'beta': np.inf},
            'kwargs_gaussian': {'a': list([np.inf for i in range(N)]),
                                 'x0': list([image_size * subsampling_factor for i in range(N)]),
                                 'y0': list([image_size * subsampling_factor for i in range(N)]),
                                 },
            'kwargs_background': {'background': list([np.inf for i in range(image_size_up ** 2)])},
        }

        kwargs_down = {
            'kwargs_moffat': {'fwhm': 0., 'beta': 0.},
            'kwargs_gaussian': {'a': list([0 for i in range(N)]),
                                'x0': list([-image_size * subsampling_factor for i in range(N)]),
                                'y0': list([-image_size * subsampling_factor for i in range(N)])
                                },

            'kwargs_background': {'background': list([-np.inf for i in range(image_size_up ** 2)])},
        }
        parameters = ParametersPSF(kwargs_final, kwargs_fixed, kwargs_up, kwargs_down)

        #compute noise weight maps :
        # bkg_noise_map2 = sigma_sky_2 + np.zeros_like(new_vignets_data)
        # W = propagate_noise(model, np.sqrt(bkg_noise_map2), kwargs_final, wavelet_type_list=['starlet'], method='SLIT', num_samples=1000,
        #             seed=1, likelihood_type='chi2', verbose=False, upsampling_factor=subsampling_factor, debug=False)[0]
        #
        # gix, axs = plt.subplots(1, len(W), figsize=(12, 4))
        # for i, l in enumerate(W):
            # axs[i].imshow(l)
        # plt.show()
        #
        loss = Loss(new_vignets_data, model, parameters, sigma_2, N, regularization_terms='l1_starlet',
                    regularization_strength_scales=lambda_scales, regularization_strength_hf=lambda_hf, W=None)
        optim = Optimizer(loss, parameters, method=method)
        best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(maxiter=n_iter, restart_from_init=False,
                                                                        use_grad=True, use_hessian=False, use_hvp=True)

        kwargs_final = parameters.args2kwargs(best_fit)
        print(kwargs_final)

        fig1 = ptf.single_PSF_plot(model,new_vignets_data, sigma_2, kwargs_final, units='e-')
        fig2 = ptf.multiple_PSF_plot(model,new_vignets_data, sigma_2, kwargs_final, units='e-')

        plt.show()

        narrow = model.model(0, **kwargs_final)[2]
        hdu = fits.PrimaryHDU(data=narrow)
        hdu.writeto(os.path.join(output_folder, 'narrow_PSF.fits'), overwrite=True)

        for i in range(N):
            estimated_full_psf = (model.model(i, **kwargs_final)[0]).reshape(image_size, image_size)
            dif = new_vignets_data[i, :, :] - estimated_full_psf
            rr = np.abs(dif) / np.sqrt(sigma_2[i, :, :])

            hdu = fits.PrimaryHDU(data=estimated_full_psf)
            hdu.writeto(os.path.join(output_folder, 'full_psf_%i.fits'%i), overwrite=True)

            hdu = fits.PrimaryHDU(data=dif)
            hdu.writeto(os.path.join(output_folder, 'residuals_%i.fits'%i), overwrite=True)

            hdu = fits.PrimaryHDU(data=rr)
            hdu.writeto(os.path.join(output_folder, 'scaled_residuals_%i.fits'%i), overwrite=True)

if __name__ == "__main__":
    main()