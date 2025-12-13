import os.path

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import os
import scipy.ndimage
from BOF import mkdir_recursive
import pickle as pkl
from starred.utils.generic_utils import make_grid, gaussian_function, save_fits, Downsample, Upsample

instrument = 'tinytim10'
SNRs = [100, 1000, 10000, 100000]
test_set = './mock_stars_shift05_oddkernel_multiple'

if instrument == 'WFI' or instrument == 'WFI_odd':
    upsampling_factor = 2
    final_res_factor = 1
elif instrument == 'Gaussian':
    upsampling_factor = 8
    final_res_factor = 1
elif instrument == 'tinytim10':
    upsampling_factor = 10
    final_res_factor = 2 # to the drizzled resolution (0.04")
else :
    upsampling_factor = 1
    final_res_factor = 1 #HST : drizzled PSF at 0.04"

image_size = 63 # used only for the gaussian (otherwise final images have the same size as the PSF kernel)
shift_sigma = 0.5 # in the unit of pixel, of the final image (low resolution)
interpolation_order = 1
seeds = np.arange(10)

for seed in seeds:
    np.random.seed(seed)
    for SNR in SNRs:
        outdir = os.path.join(test_set, instrument, 'seed_%i'%seed, 'SNR_%2.f' %SNR)
        mkdir_recursive(outdir)
        outdir_star = os.path.join(outdir, 'stars')
        outdir_noisemaps = os.path.join(outdir, 'noise_maps')
        mkdir_recursive(outdir_star)
        mkdir_recursive(outdir_noisemaps)

        # simulated image are in e-
        n_star = 6
        noise = 10 #level of background noise
        amp = np.ones(n_star) * noise * SNR
        skylevel = 0 # we assume that the sky is properly subtracted
        plot = False

        if instrument=='Gaussian':
            sigmax, sigmay = 2.*upsampling_factor, 2.*upsampling_factor
            x, y = make_grid(numPix=image_size*upsampling_factor, deltapix=1.)
            PSF = np.array(gaussian_function(x=x, y=y,
                amp=1, sigma_x=sigmax, sigma_y=sigmay,
                center_x=0.,
                center_y=0.,)).reshape(image_size*upsampling_factor,image_size*upsampling_factor)
            PSF = PSF / np.sum(PSF)
            pathPSF = './PSF/psf_%s_size%i_upsampling%i'%(instrument, image_size, upsampling_factor)
            save_fits(PSF, pathPSF)

        else:
            pathPSF = './PSF/psf_%s.fits'%instrument
            PSF = fits.open(pathPSF)[0].data
            PSF[PSF < 0] = 0.
            PSF /= np.sum(PSF)

        nx,ny = np.shape(PSF)
        print('Size :', nx, ny )

        if plot:
            plt.figure(1)
            plt.title('PSF')
            plt.imshow(np.log10(PSF), origin = 'lower')
            plt.show()

        flux_list = []
        mag_list = []
        shift_tuple = []
        total_flux = []
        for i in range(n_star):
            # shift_x = 0.
            shift_x = np.random.normal(loc=0, scale=(shift_sigma*upsampling_factor) /final_res_factor)
            # shift_y = 0.
            shift_y = np.random.normal(loc=0, scale=(shift_sigma*upsampling_factor) /final_res_factor)
            PSF_shifted = PSF
            size_PSF, _ = np.shape(PSF_shifted)

            PSF_shifted = scipy.ndimage.shift(PSF, (shift_x,shift_y), output=None, order=interpolation_order, mode='nearest')

            if size_PSF %2 == 1:
                PSF_shifted = PSF_shifted[1::, 1::]
                delta = 0.5
            else :
                delta = 0.

            if upsampling_factor/final_res_factor > 1 :
                print(np.shape(PSF_shifted))
                PSF_shifted = Downsample(PSF_shifted, factor=upsampling_factor/final_res_factor) #downsample

            if instrument == 'tinytim10': # tinytim PSF is centered in the middle of the 151th pixel
                delta += - 0.5 * final_res_factor/upsampling_factor
                PSF_shifted = PSF_shifted[1::,1::]

            nx_im, ny_im = np.shape(PSF_shifted)
            print('New shape :', np.shape(PSF_shifted))
            print('Shift : ', ((shift_x/upsampling_factor) * final_res_factor - delta, (shift_y/upsampling_factor)* final_res_factor - delta))
            print('Shifted PSF norm :', np.sum(PSF_shifted))
            PSF_shifted /= np.sum(PSF_shifted) #renormalised to be sure
            print('Shifted PSF norm :', np.sum(PSF_shifted))

            star = amp[i] * PSF_shifted
            flux = np.sum(star)
            print('SNR emp :', flux/noise)

            flux_list.append(flux)
            mag = -2.5*np.log10(flux)
            mag_list.append(mag)
            shift_tuple.append(((shift_x/upsampling_factor) * final_res_factor - delta, (shift_y/upsampling_factor)* final_res_factor - delta))

            poisson_noise = np.sqrt(np.abs(star)) * np.random.randn(nx_im, ny_im)
            background = np.random.normal(loc=skylevel, scale=noise, size=(nx_im, ny_im))
            noise_maps = np.sqrt(np.abs(star)) + noise
            star = star + background + poisson_noise
            total_flux.append(np.sum(star))

            hdu = fits.PrimaryHDU(star)
            hdul = fits.HDUList([hdu])
            hdul.writeto(os.path.join(outdir_star, 'star_%i.fits'%(i)), overwrite=True)

            hdu = fits.PrimaryHDU(noise_maps)
            hdul = fits.HDUList([hdu])
            hdul.writeto(os.path.join(outdir_noisemaps, 'noise_maps_%i.fits'%(i)), overwrite=True)

        output_txt = os.path.join(outdir, 'flux_mag.txt')
        output_pkl = os.path.join(outdir, 'flux_mag.pkl')

        with open(output_txt, 'w') as f :
            f.write('fluxes : ' + str(flux_list) + '\n')
            f.write('fluxes noise : ' + str(total_flux) + '\n')
            f.write('Mag [ZP=0] : '+ str(mag_list) + '\n')
            f.write('Shift : ' + str(shift_tuple) + '\n')
            f.write('Image size: ' + str(np.shape(star)) + '\n')

        with open(output_pkl, 'wb') as handle:
            pkl.dump([flux_list, mag_list, shift_tuple, total_flux], handle)
