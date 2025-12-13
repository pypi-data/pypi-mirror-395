import glob
import numpy as np
import matplotlib.pyplot as plt
import os
from astropy.io import fits

from copy import deepcopy
from matplotlib import colors

from starred.deconvolution.deconvolution import Deconv
from starred.deconvolution.loss import Loss
from starred.optim.optimization import Optimizer
from starred.deconvolution.parameters import ParametersDeconv

# Parameters
plots=True
epochs = 1
subsampling_factor = 2
n_iter_first = 20
n_iter = 70
M = 2
t_exp = 1 # as the image is in ADU
gain = 2 # WFI camera gain
method = 'trust-constr'
lambda_scales = 8e-2
lambda_hf = 1e-3
data_path = '../notebooks/data/2_observation'
psf_path = '../notebooks/data/2_psf'
output_folder = './outputs'

# Retrieving data
file_paths = sorted(glob.glob(os.path.join(data_path, '*.npy')))
data = np.array([np.load(f) for f in file_paths]) * t_exp / gain

im_size = np.shape(data)[1]
im_size_up = im_size * subsampling_factor

# Retrieving the PSF
file_paths = sorted(glob.glob(os.path.join(psf_path, '*.npy')))
s = np.array([np.load(f) for f in file_paths])

if plots:
    fig, axs = plt.subplots(1, 2, figsize=(10, 10))
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

# Noise map
sigma_2 = np.zeros((epochs, im_size, im_size))
sigma_sky_2 = np.array([np.std(data[i,int(0.9*im_size):,int(0.9*im_size):]) for i in range(epochs)]) ** 2
for i in range(epochs):
    sigma_2[i,:,:] = sigma_sky_2[i] + data[i,:,:].clip(min=0)

# Parameter initialization
initial_c_x = np.array([-2.2, 2.5]) * subsampling_factor
initial_c_y = np.array([-4.5, 1.25]) * subsampling_factor
initial_a = np.array([data[i,:,:].max() for j in range(M) for i in range(epochs)]) / 10e3
initial_h = np.zeros((im_size_up**2))

kwargs_init = {
    'kwargs_analytic': {'c_x': initial_c_x, 'c_y': initial_c_y, 'a': initial_a, 'dx':np.ravel([0. for _ in range(epochs)]),
                        'dy':np.ravel([0. for _ in range(epochs)])},
    'kwargs_background':{'h': initial_h,
                         'mean': np.ravel([0. for _ in range(epochs)])},
}
kwargs_fixed = {
    'kwargs_analytic': {},
    'kwargs_background': {'h': initial_h},
}

kwargs_up = {
    'kwargs_analytic': {'c_x': list([im_size_up/2. for i in range(M*epochs)]),
                        'c_y': list([im_size_up/2. for i in range(M*epochs)]),
                         'a': list([np.inf for i in range(M*epochs)]),
                        'dx': [0.5 for _ in range(epochs)],
                        'dy': [0.5 for _ in range(epochs)] },
    'kwargs_background': {'h': list([np.inf for i in range(0, im_size_up**2)]),
                           'mean': [np.inf for _ in range(epochs)]},
}

kwargs_down = {
    'kwargs_analytic': {'c_x': list([-im_size_up/2. for i in range(M*epochs)]),
                        'c_y': list([-im_size_up/2. for i in range(M*epochs)]),
                        'dx': [0.5 for _ in range(epochs)],
                        'dy': [0.5 for _ in range(epochs)],
                         'a': list([0 for i in range(M*epochs)]) },
    'kwargs_background': {'h': list([-np.inf for i in range(0, im_size_up**2)]),
                            'mean': [-np.inf for _ in range(epochs)]
                           },
        }

# Getting the model
model = Deconv(image_size=im_size, number_of_sources=M, upsampling_factor=subsampling_factor, scale=data.max(),
               epochs=epochs, psf=s, convolution_method='fft')
parameters = ParametersDeconv(kwargs_init, kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down)

# Tunning amplitudes and point source positions
loss = Loss(data, model, parameters, sigma_2, regularization_terms='l1_starlet', regularization_strength_scales=0, regularization_strength_hf=0)
optim = Optimizer(loss, parameters, method=method)
optim.minimize(maxiter=n_iter_first, restart_from_init=True,
                                                    use_grad=True, use_hessian=False, use_hvp=False)

# Printing partial results
kwargs_partial = deepcopy(parameters.best_fit_values(as_kwargs=True))
print(kwargs_partial)

# Background tunning
kwargs_fixed = {
    'kwargs_analytic': {},
    'kwargs_background': {},
}

parameters = ParametersDeconv(kwargs_partial, kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down)
loss = Loss(data, model, parameters, sigma_2, regularization_terms='l1_starlet', regularization_strength_scales=lambda_scales, regularization_strength_hf=lambda_hf)
optim = Optimizer(loss, parameters, method=method)
optim.minimize(maxiter=n_iter, restart_from_init=False,
                                    use_grad=True, use_hessian=False, use_hvp=True)

# Printing final results
kwargs_final = deepcopy(parameters.best_fit_values(as_kwargs=True))
print(kwargs_final)

if plots:
    plt.plot(range(n_iter), optim.loss_history)
    plt.xlabel('Steps')
    plt.ylabel('Loss')
    plt.show()

    # Retrieving different elements of the deconvolved image
    epoch = 0
    h, deconv = model.getDeconvolved(kwargs_final, epoch)
    h, deconv = h * gain / t_exp, deconv * gain / t_exp
    cback = model.model(kwargs_final)[epoch].reshape(im_size, im_size)
    print(np.shape(data))
    data_show = data[epoch, :, :]

    dif = data_show - cback
    rr = np.abs(dif) / np.sqrt(sigma_2[epoch, :, :])
    data_show *= gain / t_exp
    cback *= gain / t_exp

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

    fig.colorbar(axs[0, 0].imshow(data_show, norm=colors.SymLogNorm(linthresh=5e2)), ax=axs[0, 0], fraction=fraction,
                 pad=pad)
    fig.colorbar(axs[0, 1].imshow(cback, norm=colors.SymLogNorm(linthresh=5e2)), ax=axs[0, 1], fraction=fraction,
                 pad=pad)
    fig.colorbar(axs[0, 2].imshow(rr, norm=colors.LogNorm(vmin=0.1)), ax=axs[0, 2], fraction=fraction, pad=pad)
    fig.colorbar(axs[1, 0].imshow(h, norm=colors.SymLogNorm(linthresh=5e1, vmin=5e1)), ax=axs[1, 0], fraction=fraction,
                 pad=pad)
    fig.colorbar(axs[1, 1].imshow(deconv, norm=colors.SymLogNorm(linthresh=5e1, vmin=5e1)), ax=axs[1, 1],
                 fraction=fraction, pad=pad)
    fig.colorbar(axs[1, 2].imshow(s[epoch, :, :], norm=colors.SymLogNorm(linthresh=1e-3)), ax=axs[1, 2],
                 fraction=fraction, pad=pad)
    plt.show()


hdu = fits.PrimaryHDU(data=data_show)
hdu.writeto(os.path.join(output_folder, 'data.fits'), overwrite=True)

hdu = fits.PrimaryHDU(data=cback)
hdu.writeto(os.path.join(output_folder, 'model_low_res.fits'), overwrite=True)

hdu = fits.PrimaryHDU(data=rr)
hdu.writeto(os.path.join(output_folder, 'residuals.fits'), overwrite=True)

hdu = fits.PrimaryHDU(data=h)
hdu.writeto(os.path.join(output_folder, 'background.fits'), overwrite=True)

hdu = fits.PrimaryHDU(data=deconv)
hdu.writeto(os.path.join(output_folder, 'model_high_res.fits'), overwrite=True)

# Checking flux conservation (this does need to )
flux_diff = np.sum(data_show) - np.sum(deconv)
flux_diff_rel = flux_diff / np.sum(data_show)
print('Flux difference [ADU]:', flux_diff)
print('Relative flux difference [percent]:', flux_diff_rel*100)
print('Magnitude difference:', -2.5*np.log10(1 + flux_diff_rel))