import os, glob
import numpy as np
import time
from astropy.io import fits
from matplotlib import colors
import matplotlib.pyplot as plt
from copy import deepcopy
from BOF import mkdir_recursive
from utils_psf import revert_psf

from starred.deconvolution.deconvolution import Deconv
from starred.deconvolution.loss import Loss
from starred.optim.optimization import Optimizer
from starred.deconvolution.parameters import Parameters

thetaEs = [2.0]
instrument = ['WFI']
file_to_run = '../1_generate_psf.py'

lambda_scales = 8e-2
lambda_hf = 1e-4
t_exp = 1
gain = 4.5
subsampling_factor = 2
M = 4 #number of source
epochs = 1
show_plot = True

method = 'trust-constr'
n_iter_first = 10
n_iter = 10

for inst in instrument:
    for thetaE in thetaEs:
        datapath =  os.path.join('mock_lens/%s/theta_E_%2.2f'%(inst, thetaE))
        outputpath = os.path.join(datapath, 'output')
        mkdir_recursive(outputpath)

        file_paths = sorted(glob.glob(os.path.join(datapath, 'lens0.fits')))
        data = np.array([fits.open(f)[0].data for f in file_paths], dtype=np.single) * t_exp / gain #lenstronomy have it in ADU/s --> convert to e-
        print(np.shape(data[0]))

        im_size = np.shape(data)[1]
        im_size_up = im_size * subsampling_factor

        PSFfile_paths = sorted(glob.glob(os.path.join(datapath, 'psf*.fits')))
        # PSFfile_paths = sorted(glob.glob('../test_PSF_generator/PSF/psf_WFI.fits'))
        psf = np.array([fits.open(f)[0].data for f in PSFfile_paths], dtype=np.single)
        s, g  = revert_psf(psf[0])

        sigma_path = sorted(glob.glob(os.path.join(datapath, 'sigma0.fits')))
        sigma2 = np.array([fits.open(f)[0].data for f in sigma_path], dtype=np.single)
        print(np.shape(sigma2[0]))

        if show_plot:
            fig, axs = plt.subplots(1, 3, figsize=(10, 7))
            fraction = 0.046
            pad = 0.04

            plt.rc('font', size=12)
            axs[0].set_title('Data [e-]', fontsize=12)
            axs[0].tick_params(axis='both', which='major', labelsize=10)
            axs[1].set_title('PSF', fontsize=12)
            axs[1].tick_params(axis='both', which='major', labelsize=10)
            axs[2].set_title('Narrow PSF', fontsize=12)
            axs[2].tick_params(axis='both', which='major', labelsize=10)
            fig.colorbar(axs[0].imshow(data[0, :, :], norm=colors.SymLogNorm(linthresh=10), origin='lower'), ax=axs[0], fraction=fraction,
                         pad=pad)
            fig.colorbar(axs[1].imshow(psf[0, :, :], norm=colors.SymLogNorm(linthresh=1e-3), origin='lower'), ax=axs[1], fraction=fraction,
                         pad=pad)
            fig.colorbar(axs[2].imshow(s[:, :], norm=colors.SymLogNorm(linthresh=1e-3), origin='lower'), ax=axs[2], fraction=fraction,
                         pad=pad)
            plt.show()
            exit()

        # Parameter initialization
        center_x, center_y = im_size/2, im_size/2
        initial_c_x = (np.array([35, 30.8, 40, 24]) - center_x) * subsampling_factor
        initial_c_y = (np.array([41.2, 21.6, 30, 32]) - center_y) * subsampling_factor
        initial_a = np.array([data[i, :, :].max() for j in range(M) for i in range(epochs)]) / 10e3
        initial_h = np.zeros((im_size_up ** 2))

        #TODO : add check if the number of source is correct
        #TODO : check definition of the coordinates from the center.
        kwargs_init = {
            'kwargs_analytic': [{'c_x': initial_c_x, 'c_y': initial_c_y, 'a': initial_a}],
            'kwargs_background': [{'h': initial_h}],
        }
        kwargs_fixed = {
            'kwargs_analytic': [{}],
            'kwargs_background': [{}],
        }

        # Getting the model
        model = Deconv(im_size, M, subsampling_factor, initial_c_x, initial_c_y, initial_a, epochs, s)
        parameters = Parameters(model, kwargs_init, kwargs_fixed)

        # Tunning amplitudes and point source positions
        loss = Loss(data, model, parameters, sigma2, True, regularization_terms='l1_starlet',
                    regularization_strength_scales=0, regularization_strength_hf=0)
        Optimizer(loss, parameters).minimize(method=method, maxiter=n_iter_first, restart_from_init=True,
                                             use_exact_hessian_if_allowed=False)

        # Printing partial results
        kwargs_partial = deepcopy(parameters.best_fit_values(as_kwargs=True))
        print("intermediate :", kwargs_partial)

        # Background tunning
        loss = Loss(data, model, parameters, sigma2, False, regularization_terms='l1_starlet',
                    regularization_strength_scales=lambda_scales, regularization_strength_hf=lambda_hf)
        Optimizer(loss, parameters).minimize(method=method, maxiter=n_iter, restart_from_init=False,
                                             use_exact_hessian_if_allowed=False)

        # Printing final results
        kwargs_final = deepcopy(parameters.best_fit_values(as_kwargs=True))
        print("final : ",kwargs_final)

        # Retrieving different elements of the deconvolved image
        epoch = 0
        output = model.model(epoch, False, **kwargs_final)[2] * gain / t_exp
        h = model.model(epoch, False, **kwargs_final)[1] * gain / t_exp
        cback = model.model(epoch, False, **kwargs_final)[0].reshape(im_size, im_size)
        data = data[epoch, :, :]

        dif = data - cback
        rr = np.abs(dif) / np.sqrt(sigma2[epoch, :, :])
        data *= gain / t_exp
        cback *= gain / t_exp

        if show_plot:
            fig, axs = plt.subplots(2, 3, figsize=(15, 8))
            fraction = 0.046
            pad = 0.04
            font_size = 10
            ticks_size = 6

            plt.rc('font', size=font_size)
            axs[0, 0].set_title('Data [ADU]', fontsize=8)
            axs[0, 0].tick_params(axis='both', which='major', labelsize=ticks_size)
            axs[0, 1].set_title('Convolving back [ADU]', fontsize=8)
            axs[0, 1].tick_params(axis='both', which='major', labelsize=ticks_size)
            axs[0, 2].set_title('Map of relative residuals', fontsize=8)
            axs[0, 2].tick_params(axis='both', which='major', labelsize=ticks_size)
            axs[1, 0].set_title('Background [ADU]', fontsize=8)
            axs[1, 0].tick_params(axis='both', which='major', labelsize=ticks_size)
            axs[1, 1].set_title('Deconvolved image [ADU]', fontsize=8)
            axs[1, 1].tick_params(axis='both', which='major', labelsize=ticks_size)
            axs[1, 2].set_title('Narrow PSF', fontsize=8)
            axs[1, 2].tick_params(axis='both', which='major', labelsize=ticks_size)

            fig.colorbar(axs[0, 0].imshow(data, norm=colors.SymLogNorm(linthresh=5e2)), ax=axs[0, 0], fraction=fraction,
                         pad=pad)
            fig.colorbar(axs[0, 1].imshow(cback, norm=colors.SymLogNorm(linthresh=5e2)), ax=axs[0, 1],
                         fraction=fraction, pad=pad)
            fig.colorbar(axs[0, 2].imshow(rr, norm=colors.LogNorm(vmin=0.1)), ax=axs[0, 2], fraction=fraction, pad=pad)
            fig.colorbar(axs[1, 0].imshow(h, norm=colors.SymLogNorm(linthresh=5e1, vmin=5e1)), ax=axs[1, 0],
                         fraction=fraction, pad=pad)
            fig.colorbar(axs[1, 1].imshow(output, norm=colors.SymLogNorm(linthresh=5e1, vmin=5e1)), ax=axs[1, 1],
                         fraction=fraction, pad=pad)
            fig.colorbar(axs[1, 2].imshow(s[epoch, :, :], norm=colors.SymLogNorm(linthresh=1e-3)), ax=axs[1, 2],
                         fraction=fraction, pad=pad)
            plt.show()

            fig.savefig(os.path.join(outputpath,"deconvolution_plot.png"))