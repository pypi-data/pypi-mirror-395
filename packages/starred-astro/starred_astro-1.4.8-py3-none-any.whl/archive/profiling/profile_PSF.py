import glob
import matplotlib.pyplot as plt
import numpy as np
import jax.numpy as jnp
import os

from copy import deepcopy
from matplotlib import colors

from starred.psf.psf import PSF
from starred.psf.loss import Loss
from starred.optim.optimization import Optimizer
from starred.utils.inference_base import InferenceBase
from starred.psf.parameters import ParametersPSF
from starred.plots import f2n
from starred.utils.generic_utils import save_fits
import time


# Parameters
def main():
    subsampling_factors = [2]
    n_iter_initial = 20
    n_iter = 60
    gain = 2  # WFI camera
    t_exp = 1  # because images are in ADU
    lambda_scales = 1
    lambda_hf = 1
    # method = 'trust-constr'
    method = 'Newton-CG'
    convolution_method = 'scipy'
    data_path = '../notebooks/data/1_observations'
    plot = False
    rerun = True

    # Data
    # sizes = [0.5, 1 ,2]
    image_up_vec = []
    inference_loss_runtime = []
    inference_gradloss_runtime = []
    inference_hvp_runtime = []

    if rerun:
        for subsampling_factor in subsampling_factors:
            file_paths = sorted(glob.glob(os.path.join(data_path, '*.npy')))
            print('Using %i images ' % len(file_paths))
            new_vignets_data = np.array([np.load(f) for f in file_paths]) * t_exp / gain
            N = len(file_paths)  # number of stars
            image_size = np.shape(new_vignets_data)[1]  # data dimensions
            # resize = int(int(image_size) / (2*s))
            # new_vignets_data = new_vignets_data[:, int(image_size/2)-resize:int(image_size/2)+resize, int(image_size/2)-resize:int(image_size/2)+resize ]
            # image_size = np.shape(new_vignets_data)[1]  # data dimensions
            image_size_up = image_size * subsampling_factor
            image_up_vec.append(image_size_up)
            print('Image size sumbsampling :', image_size_up)

            # Noise map estimation
            sigma_2 = np.zeros((N, image_size, image_size))
            sigma_sky_2 = np.array(
                [np.std(new_vignets_data[i, int(0.9 * image_size):, int(0.9 * image_size):]) for i in range(N)]) ** 2
            for i in range(N):
                sigma_2[i, :, :] = sigma_sky_2[i] + new_vignets_data[i, :, :].clip(min=0)

            # Positions
            x0_est = np.array([0., 0., 0.])
            y0_est = np.array([0., 0., 0.])

            if plot:
                fig, axs = plt.subplots(2, 3, figsize=(15, 10))
                fraction = 0.046
                pad = 0.04

                plt.rc('font', size=12)
                axs[0, 0].set_title('Data: WFI star 1', fontsize=12)
                axs[0, 0].tick_params(axis='both', which='major', labelsize=10)
                axs[1, 0].set_title('Estimated noise map', fontsize=12)
                axs[1, 0].tick_params(axis='both', which='major', labelsize=10)
                axs[0, 1].set_title('Data: WFI star 2', fontsize=12)
                axs[0, 1].tick_params(axis='both', which='major', labelsize=10)
                axs[1, 1].set_title('Estimated noise map', fontsize=12)
                axs[1, 1].tick_params(axis='both', which='major', labelsize=10)
                axs[0, 2].set_title('Data: WFI star 2', fontsize=12)
                axs[0, 2].tick_params(axis='both', which='major', labelsize=10)
                axs[1, 2].set_title('Estimated noise map', fontsize=12)
                axs[1, 2].tick_params(axis='both', which='major', labelsize=10)

                fig.colorbar(axs[0, 0].imshow(new_vignets_data[0, :, :], norm=colors.SymLogNorm(linthresh=100)),
                             ax=axs[0, 0], fraction=fraction, pad=pad)
                fig.colorbar(axs[1, 0].imshow(np.sqrt(sigma_2[0, :, :]), norm=colors.LogNorm()), ax=axs[1, 0],
                             fraction=fraction, pad=pad)

                fig.colorbar(axs[0, 1].imshow(new_vignets_data[1, :, :], norm=colors.SymLogNorm(linthresh=100)),
                             ax=axs[0, 1], fraction=fraction, pad=pad)
                fig.colorbar(axs[1, 1].imshow(np.sqrt(sigma_2[1, :, :]), norm=colors.LogNorm()), ax=axs[1, 1],
                             fraction=fraction, pad=pad)

                fig.colorbar(axs[0, 2].imshow(new_vignets_data[2, :, :], norm=colors.SymLogNorm(linthresh=100)),
                             ax=axs[0, 2], fraction=fraction, pad=pad)
                fig.colorbar(axs[1, 2].imshow(np.sqrt(sigma_2[2, :, :]), norm=colors.LogNorm()), ax=axs[1, 2],
                             fraction=fraction, pad=pad)
                plt.show()

            # Parameter initialization
            initial_fwhm = 0.3
            initial_beta = 0.9
            initial_a = np.array([np.median(new_vignets_data, axis=0).max() for i in range(N)])
            a_norm = 5e2 * initial_a[0]
            initial_a = initial_a / a_norm
            initial_background = jnp.zeros((image_size_up ** 2))

            # Calling the PSF model
            model = PSF(image_size=image_size,
                        number_of_sources=N,
                        upsampling_factor=subsampling_factor,
                        a_norm=a_norm, gaussian_fwhm=2,
                        convolution_method=convolution_method)

            kwargs_init = {
                'kwargs_moffat': {'fwhm': initial_fwhm, 'beta': initial_beta},
                'kwargs_gaussian': {'a': initial_a, 'x0': x0_est, 'y0': y0_est},
                'kwargs_background': {'background': initial_background},
            }
            kwargs_fixed = {
                'kwargs_moffat': {},
                'kwargs_gaussian': {},
                # 'kwargs_background': [{'background':initial_background}],
                'kwargs_background': {},
            }

            kwargs_up = {
                'kwargs_moffat': {'fwhm': 10., 'beta': 5.},
                'kwargs_gaussian': {'a': list([np.inf for i in range(N)]),
                                     'x0': list([image_size * subsampling_factor for i in range(N)]),
                                     'y0': list([image_size * subsampling_factor for i in range(N)])
                                     },
                'kwargs_background': {'background': list([np.inf for i in range(image_size_up ** 2)])},
                # 'kwargs_background': {},
            }

            kwargs_down = {
                'kwargs_moffat': {'fwhm': 0., 'beta': 0.},
                'kwargs_gaussian': {'a': list([0 for i in range(N)]),
                                     'x0': list([-image_size * subsampling_factor for i in range(N)]),
                                     'y0': list([-image_size * subsampling_factor for i in range(N)]),
                                     },
                'kwargs_background': {'background': list([0 for i in range(image_size_up ** 2)])}
                # 'kwargs_background': {},
            }

            parameters = ParametersPSF(kwargs_init, kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down)
            # print(args)
            args_init = parameters.kwargs2args(kwargs_init)

            # Moffat fitting and amplitude tunning
            loss = Loss(new_vignets_data, model, parameters, sigma_2, N, regularization_terms='l1_starlet',
                        regularization_strength_scales=0, regularization_strength_hf=0)
            start_time = time.perf_counter()
            psf = loss._psf.model(0, **kwargs_init)
            time2 = time.perf_counter()
            print('1st PSF model call : ', time2 - start_time)
            psf = loss._psf.model(0, **kwargs_init)
            time3 = time.perf_counter()
            print('2nd PSF model call : ', time3 - time2)
            psf = loss._psf.model(0, **kwargs_init)
            time4 = time.perf_counter()
            print('3rd PSF model call : ', time4 - time3)

            start_time = time.perf_counter()
            logL = loss._log_likelihood_chi2(kwargs_init)
            time2 = time.perf_counter()
            print('1st Likelihood  call : ', time2 - start_time)
            logL = loss._log_likelihood_chi2(kwargs_init)
            time3 = time.perf_counter()
            print('2nd Likelihood call : ', time3 - time2)
            logL = loss._log_likelihood_chi2(kwargs_init)
            time4 = time.perf_counter()
            print('3rd Likelihood call : ', time4 - time3)

            start_time = time.perf_counter()
            logL = loss._log_regul_l1_starlet(kwargs_init)
            time2 = time.perf_counter()
            print('1st regul  call : ', time2 - start_time)
            logL = loss._log_regul_l1_starlet(kwargs_init)
            time3 = time.perf_counter()
            print('2nd regul call : ', time3 - time2)

            start_time = time.perf_counter()
            logL = loss.loss(args_init)
            time2 = time.perf_counter()
            print('1st loss call : ', time2 - start_time)
            logL = loss.loss(args_init)
            time3 = time.perf_counter()
            print('2nd loss call : ', time3 - time2)

            inf = InferenceBase(loss, parameters)
            start_time = time.perf_counter()
            logL = inf.loss(args_init)
            time2 = time.perf_counter()
            print('1st inference base loss call : ', time2 - start_time)
            logL = inf.loss(args_init)
            time3 = time.perf_counter()
            print('2nd inference base loss call  : ', time3 - time2)
            inference_loss_runtime.append(time3 - time2)

            start_time = time.perf_counter()
            grad = inf.gradient(args_init)
            time2 = time.perf_counter()
            print('1st inference base grad loss call : ', time2 - start_time)
            grad = inf.gradient(args_init)
            time3 = time.perf_counter()
            print('2nd inference base grad loss call  : ', time3 - time2)
            inference_gradloss_runtime.append(time3 - time2)

            # Hessian computation is very slow
            # start_time = time.perf_counter()
            # logL = inf.hessian(args_init)
            # time2 = time.perf_counter()
            # print('1st inference base hessian loss call : ', time2 - start_time)
            # logL = inf.hessian(args_init)
            # time3 = time.perf_counter()
            # print('2nd inference base hessian loss call  : ', time3 - time2)

            start_time = time.perf_counter()
            hvp = inf.hessian_vec_prod(args_init, grad)
            time2 = time.perf_counter()
            print('1st inference base hvp loss call : ', time2 - start_time)
            hvp = inf.hessian_vec_prod(args_init, grad)
            time3 = time.perf_counter()
            print('2nd inference base hvp loss call  : ', time3 - time2)
            inference_hvp_runtime.append(time3 - time2)

            exit()


        plt.title('Loss Scaling runtime')
        plt.plot(image_up_vec, inference_loss_runtime, 'bx', linestyle='-')
        plt.xlabel('Image size (pix)')
        plt.ylabel('runtime (s)')
        plt.savefig('./plots/PSF_loss_scaling.png')
        plt.show()

        plt.title('Grad Loss Scaling runtime')
        plt.plot(image_up_vec, inference_gradloss_runtime, 'bx', linestyle='-')
        plt.xlabel('Image size (pix)')
        plt.ylabel('runtime (s)')
        plt.savefig('./plots/PSF_grad_scaling.png')
        plt.show()

        plt.title('HVP Scaling runtime')
        plt.plot(image_up_vec, inference_hvp_runtime, 'bx', linestyle='-')
        plt.xlabel('Image size (pix)')
        plt.ylabel('runtime (s)')
        plt.savefig('./plots/PSF_hvp_scaling.png')
        plt.show()

        np.save('./plots/scaling_%s.npy'%convolution_method, [image_up_vec, inference_loss_runtime, inference_gradloss_runtime, inference_hvp_runtime])

    else :
        image_up_vec, inference_loss_runtime, inference_gradloss_runtime, inference_hvp_runtime = np.load('./plots/scaling_fft.npy')
        image_up_vec_lax, inference_loss_runtime_lax, inference_gradloss_runtime_lax, inference_hvp_runtime_lax = np.load('./plots/scaling_lax.npy')

        fig, axes = plt.subplots(1,3, figsize=(10,5))
        plt.subplots_adjust(wspace=0.3)
        axes[0].plot(image_up_vec, inference_loss_runtime, 'bx', linestyle='-', label='fft')
        axes[0].plot(image_up_vec_lax, inference_loss_runtime_lax, 'rx', linestyle='-', label='lax')
        axes[0].set_xlabel('Image size (pix)')
        axes[0].set_ylabel('Loss runtime (s)')
        axes[0].legend()

        axes[1].plot(image_up_vec, inference_gradloss_runtime, 'bx', linestyle='-', label='fft')
        axes[1].plot(image_up_vec_lax, inference_gradloss_runtime_lax, 'rx', linestyle='-', label='lax')
        axes[1].set_xlabel('Image size (pix)')
        axes[1].set_ylabel('Grad Loss runtime (s)')

        axes[2].plot(image_up_vec, inference_hvp_runtime, 'bx', linestyle='-', label='fft')
        axes[2].plot(image_up_vec_lax, inference_hvp_runtime_lax, 'rx', linestyle='-', label='lax')
        axes[2].set_xlabel('Image size (pix)')
        axes[2].set_ylabel('HVP Loss runtime (s)')

        plt.show()
        fig.savefig('./plots/scaling_methods.png')



    '''
    kernel = 12 pix 
    Current profiling : 
    
    Using 3 images 
    Image size sumbsampling : 128
    1st PSF model call :  0.15876294300000016
    2nd PSF model call :  0.004814289000000027
    1st Likelihood  call :  0.4102544400000001
    2nd Likelihood call :  0.014116215999999682
    1st regul  call :  0.5056900779999998
    2nd regul call :  0.014557926000000165
    1st loss call :  0.9375636389999995
    2nd loss call :  0.02869103300000031
    1st inference base loss call :  1.0143735980000006
    2nd inference base loss call  :  0.027471987000000198
    1st inference base grad loss call :  4.127179117
    2nd inference base grad loss call  :  0.10951346899999947
    1st inference base hessian loss call :  5.194785623
    2nd inference base hessian loss call  :  0.13429040100000122
    
    
    kernel = 24 pix 
    Using 3 images 
    Image size sumbsampling : 128
    1st PSF model call :  0.1955061649999994
    2nd PSF model call :  0.020723656000000368
    1st Likelihood  call :  0.4702828539999997
    2nd Likelihood call :  0.05906637100000012
    1st regul  call :  0.5113523950000003
    2nd regul call :  0.01429727699999983
    1st loss call :  1.0465054450000002
    2nd loss call :  0.07078783700000013
    1st inference base loss call :  1.0169250600000002
    2nd inference base loss call  :  0.07039779299999971
    1st inference base grad loss call :  3.2968127800000007
    2nd inference base grad loss call  :  0.23658238800000042
    1st inference base hessian loss call :  4.253641561
    2nd inference base hessian loss call  :  0.5166751300000012
    '''


if __name__ == "__main__":
    main()
