import glob
import numpy as np
import matplotlib.pyplot as plt
import os
import time

from copy import deepcopy
from matplotlib import colors

from starred.deconvolution.deconvolution import Deconv
from starred.deconvolution.loss import Loss
from starred.optim.optimization import Optimizer
from starred.deconvolution.parameters import ParametersDeconv

from starred.utils.inference_base import InferenceBase


def main():
    epochs = 1
    subsampling_factors = [2,4,6,8]
    n_iter_first = 10
    n_iter = 10
    M = 2
    t_exp = 1  # as the image is in ADU
    gain = 2  # WFI camera gain
    method = 'trust-constr'
    lambda_scales = 8e-2
    lambda_hf = 1e-4
    data_path = '../notebooks/data/2_observation'
    psf_path = '../notebooks/data/2_psf'
    plot = False

    # Retrieving data
    file_paths = sorted(glob.glob(os.path.join(data_path, '*.npy')))
    data = np.array([np.load(f) for f in file_paths]) * t_exp / gain

    # Retrieving the PSF
    file_paths = sorted(glob.glob(os.path.join(psf_path, '*.npy')))
    s = np.array([np.load(f) for f in file_paths])

    if plot:
        fig, axs = plt.subplots(1, 2, figsize=(15, 15))
        fraction = 0.046
        pad = 0.04

        plt.rc('font', size=12)
        axs[0].set_title('Data: DESJ0602-4335 lensed quasar [e-]', fontsize=12)
        axs[0].tick_params(axis='both', which='major', labelsize=10)
        axs[1].set_title('Narrow PSF', fontsize=12)
        axs[1].tick_params(axis='both', which='major', labelsize=10)

        fig.colorbar(axs[0].imshow(data[0, :, :], norm=colors.SymLogNorm(linthresh=10)), ax=axs[0], fraction=fraction,
                     pad=pad)
        fig.colorbar(axs[1].imshow(s[0, :, :], norm=colors.SymLogNorm(linthresh=1e-3)), ax=axs[1], fraction=fraction,
                     pad=pad)
        plt.show()


    inference_loss_runtime = []
    inference_gradloss_runtime = []
    inference_hvp_runtime = []
    image_up_vec = []
    for subsampling_factor in subsampling_factors:
        im_size = np.shape(data)[1]
        im_size_up = im_size * subsampling_factor
        print('Using %i images ' % len(file_paths))
        print('Image size sumbsampling :', im_size_up)
        image_up_vec.append(im_size_up)

        # Noise map
        sigma_2 = np.zeros((epochs, im_size, im_size))
        sigma_sky_2 = np.array([np.std(data[i, int(0.9 * im_size):, int(0.9 * im_size):]) for i in range(epochs)]) ** 2
        for i in range(epochs):
            sigma_2[i, :, :] = sigma_sky_2[i] + data[i, :, :].clip(min=0)

        initial_c_x = np.array([-2.2, 2.5]) * subsampling_factor
        initial_c_y = np.array([-4.5, 1.25]) * subsampling_factor
        initial_a = np.array([data[i, :, :].max() for j in range(M) for i in range(epochs)]) / 10e3
        initial_h = np.zeros((im_size_up ** 2))

        kwargs_init = {
            'kwargs_analytic': {'c_x': initial_c_x, 'c_y': initial_c_y, 'a': initial_a,
                                'dx' : np.ravel([0. for _ in range(epochs)]),
                                'dy' : np.ravel([0. for _ in range(epochs)])},
            'kwargs_background': {'h': initial_h, 'mean':np.ravel([0. for _ in range(epochs)])},
        }
        kwargs_fixed = {
            'kwargs_analytic': {},
            'kwargs_background': {'h': initial_h},
        }

        kwargs_up = {
            'kwargs_analytic': {'c_x': list([im_size_up/2. for i in range(M*epochs)]),
                                'c_y': list([im_size_up/2. for i in range(M*epochs)]),
                                'dx': [5 for _ in range(epochs)],
                                'dy': [5 for _ in range(epochs)],
                                 'a': list([np.inf for i in range(M*epochs)]) },
            'kwargs_background': {'h': list([np.inf for i in range(0, im_size_up**2)]),
                                  'mean': [np.inf for _ in range(epochs)]
                                   },
        }

        kwargs_down = {
            'kwargs_analytic': {'c_x': list([-im_size_up/2. for i in range(M*epochs)]),
                                'c_y': list([-im_size_up/2. for i in range(M*epochs)]),
                                'dx': [-5 for _ in range(epochs)],
                                'dy': [-5 for _ in range(epochs)],
                                 'a': list([0 for i in range(M*epochs)]) },
            'kwargs_background': {'h': list([-np.inf for i in range(0, im_size_up**2)]),
                                  'mean': [-np.inf for _ in range(epochs)]
                                   },
        }
        '''                    
        lb = list([0 for i in range(M*epochs)]) 
        lb_ = list(-image_size_up//2*np.ones(2*M))
        ub = list([np.inf for i in range(M*epochs)])
        ub_ = list(image_size_up//2*np.ones(2*M))
        lb__ = list([-np.inf for i in range(0, image_size_up**2)]) 
        ub__ = list([np.inf for i in range(0, image_size_up**2)]) 
        extra_kwargs['bounds'] = Bounds(lb+lb_+lb__, ub+ub_+ub__)
        '''

        # Getting the model
        model = Deconv(image_size=im_size,
                       number_of_sources=2,
                       upsampling_factor=subsampling_factor,
                       epochs=epochs,
                       psf=s,
                       gaussian_fwhm=2,
                       scale= data.max(),
                       )
        parameters = ParametersDeconv(kwargs_init, kwargs_fixed, kwargs_down=kwargs_down, kwargs_up=kwargs_up)
        args_init = parameters.kwargs2args(kwargs_init)
        loss = Loss(data, model, parameters, sigma_2, regularization_terms='l1_starlet',
                    regularization_strength_scales=0, regularization_strength_hf=0)

        start_time = time.perf_counter()
        psf = loss._deconv.model(kwargs_init)
        time2 = time.perf_counter()
        print('1st Deconv model call : ', time2 - start_time)
        psf = loss._deconv.model(kwargs_init)
        time3 = time.perf_counter()
        print('2nd Deconv model call : ', time3 - time2)

        start_time = time.perf_counter()
        logL = loss._log_likelihood_chi2(kwargs_init)
        time2 = time.perf_counter()
        print('1st Likelihood  call : ', time2 - start_time)
        logL = loss._log_likelihood_chi2(kwargs_init)
        time3 = time.perf_counter()
        print('2nd Likelihood call : ', time3 - time2)

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

        start_time = time.perf_counter()
        hvp = inf.hessian_vec_prod(args_init, grad)
        time2 = time.perf_counter()
        print('1st inference base hvp loss call : ', time2 - start_time)
        hvp = inf.hessian_vec_prod(args_init, grad)
        time3 = time.perf_counter()
        print('2nd inference base hvp loss call  : ', time3 - time2)
        inference_hvp_runtime.append(time3 - time2)

    plt.title('Loss Scaling runtime')
    plt.plot(image_up_vec, inference_loss_runtime, 'bx', linestyle='-')
    plt.xlabel('Image size (pix)')
    plt.ylabel('runtime (s)')
    plt.savefig('./plots/Deconv_loss_scaling.png')
    plt.show()

    plt.title('Grad Loss Scaling runtime')
    plt.plot(image_up_vec, inference_gradloss_runtime, 'bx', linestyle='-')
    plt.xlabel('Image size (pix)')
    plt.ylabel('runtime (s)')
    plt.savefig('./plots/Deconv_grad_scaling.png')
    plt.show()

    plt.title('HVP Scaling runtime')
    plt.plot(image_up_vec, inference_hvp_runtime, 'bx', linestyle='-')
    plt.xlabel('Image size (pix)')
    plt.ylabel('runtime (s)')
    plt.savefig('./plots/Deconv_hvp_scaling.png')
    plt.show()

if __name__ == "__main__":
    main()
