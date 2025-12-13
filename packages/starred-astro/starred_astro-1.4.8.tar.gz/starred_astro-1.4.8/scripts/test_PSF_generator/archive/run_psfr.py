import os.path

import matplotlib.pyplot as plt
from psfr.psfr import stack_psf, _linear_amplitude
import numpy as np
import glob
import astropy.io.fits as fits
import os

from photutils.psf import EPSFStar
from photutils.psf import EPSFStars
from photutils.psf import EPSFBuilder
from astropy.modeling.fitting import LevMarLSQFitter
from astropy.stats import gaussian_sigma_to_fwhm
from photutils.background import MADStdBackgroundRMS, MMMBackground
from photutils.detection import IRAFStarFinder
from photutils.psf import (DAOGroup, IntegratedGaussianPRF,
                           IterativelySubtractedPSFPhotometry)
from lenstronomy.Util import util, kernel_util, image_util

kwargs_psf_stacking = {'stacking_option': 'median'}
# stacking_option : option of stacking, 'mean',  'median' or 'median_weight'
use_psfr, use_photutils = True, False
use_error = True
SNR = [100, 1000, 10000, 100000]
# SNR = [10000]
upsamplings = [1,2,3]
seeds = np.arange(10)

instrument = ['WFI_odd']

path = './mock_stars_shift05_oddkernel_multiple'

for inst in instrument:
    for seed in seeds:
        for SN in SNR:
            file_paths = sorted(glob.glob(os.path.join(path, inst, 'seed_%i'%seed, 'SNR_%i'%SN, 'stars','*.fits')))
            file_paths_error = sorted(glob.glob(os.path.join(path, inst, 'seed_%i'%seed, 'SNR_%i'%SN, 'noise_maps', '*.fits')))
            star_list = np.array([fits.open(f)[0].data for f in file_paths])
            npixx, npixy = np.shape(star_list[0])
            sigma2_list = np.array([fits.open(f)[0].data **2 for f in file_paths_error])
            if use_error :
                error_map_list = sigma2_list
            else :
                error_map_list = None

            for upsampling in upsamplings:
                print('### ', inst, 'SNR : ', SN, 'upsampling :', upsampling, '###')
                if use_psfr :
                    psf_psfr, center_list_psfr, mask_list, amplitude_list = stack_psf(star_list, oversampling=upsampling,
                                                                      saturation_limit=None, num_iteration=50,
                                                                      n_recenter=20, kwargs_psf_stacking=kwargs_psf_stacking,
                                                                      error_map_list = error_map_list
                                                                      )
                    print(np.shape(psf_psfr))

                    if use_error:
                        outdir =os.path.join(path, inst,'seed_%i'%seed, 'SNR_%i'%SN, 'psfr_output_with_noise_maps')
                    else :
                        outdir =os.path.join(path, inst,'seed_%i'%seed, 'SNR_%i'%SN, 'psfr_output')

                    if not os.path.exists(outdir):
                        os.mkdir(outdir)

                    hdu = fits.PrimaryHDU(psf_psfr)
                    hdul = fits.HDUList([hdu])
                    hdul.writeto(os.path.join(outdir, 'psfr_upsampling%i.fits'%upsampling), overwrite=True)

                    np.savetxt(os.path.join(outdir, 'center_list_upsampling%i.txt'%upsampling), center_list_psfr)
                    np.savetxt(os.path.join(outdir, 'fluxes_upsampling%i.txt'%upsampling), amplitude_list)


                #photutils
                outdir_phot = os.path.join(path, inst,'seed_%i'%seed, 'SNR_%i' % SN, 'photutils_output')
                if not os.path.exists(outdir_phot):
                    os.mkdir(outdir_phot)

                if use_photutils:
                    star_list_epsf = []
                    for star_ in star_list:
                        x_grid, y_grid = util.make_grid(numPix=len(star_), deltapix=1, left_lower=True)
                        x_grid, y_grid = util.array2image(x_grid), util.array2image(y_grid)
                        x_c, y_c = np.sum(star_ * x_grid) / np.sum(star_), np.sum(star_ * y_grid) / np.sum(star_)
                        c_ = (len(star_) - 1) / 2
                        x_s, y_s = x_c, y_c
                        x_s, y_s = 2 * c_ - y_c, 2 * c_ - x_c
                        star_list_epsf.append(EPSFStar(star_, cutout_center=[x_s, y_s]))

                    stars_epsf = EPSFStars(star_list_epsf)
                    epsf_builder_super = EPSFBuilder(oversampling=upsampling, maxiters=1, progress_bar=True)
                    epsf_super, fitted_stars = epsf_builder_super(stars_epsf)

                    #This gives only aperture photometry :
                    # fluxes_photutils = [star.estimate_flux() for star in fitted_stars.all_stars]

                    fluxes_photutils = []
                    #perform PSF photometry
                    for j, im in enumerate(star_list):
                        bkgrms = MADStdBackgroundRMS()
                        std = bkgrms(im)
                        iraffind = IRAFStarFinder(threshold=3.5 * std,
                                                  fwhm= 2 * gaussian_sigma_to_fwhm,
                                                  minsep_fwhm=0.01, roundhi=5.0, roundlo=-5.0,
                                                  sharplo=0.0, sharphi=2.0)
                        daogroup = DAOGroup(2.0 * 2 * gaussian_sigma_to_fwhm)
                        mmm_bkg = MMMBackground()
                        fitter = LevMarLSQFitter()
                        psf_model = epsf_super
                        photometry = IterativelySubtractedPSFPhotometry(finder=iraffind,
                                                                        group_maker=daogroup,
                                                                        bkg_estimator=mmm_bkg,
                                                                        psf_model=psf_model,
                                                                        fitter=LevMarLSQFitter(),
                                                                        niters=1, fitshape=(11, 11))
                        result_tab = photometry(image=im)
                        try :
                            fluxes_photutils.append(result_tab['flux_fit'].value[0])
                        except IndexError:
                            fluxes_photutils.append(np.nan)

                        residual_image = photometry.get_residual_image()
                        hdu = fits.PrimaryHDU(residual_image)
                        hdul = fits.HDUList([hdu])
                        hdul.writeto(os.path.join(outdir_phot, 'residuals_star%i_upsampling%i.fits' %(j, upsampling)), overwrite=True)

                    center_list_photutils = fitted_stars.center_flat - int(npixx/2.)

                    hdu = fits.PrimaryHDU(epsf_super.data)
                    hdul = fits.HDUList([hdu])
                    hdul.writeto(os.path.join(outdir_phot, 'photutils_upsampling%i.fits'%upsampling), overwrite=True)
                    np.savetxt(os.path.join(outdir_phot, 'center_list_upsampling%i.txt'%upsampling), center_list_photutils)
                    np.savetxt(os.path.join(outdir_phot, 'fluxes_upsampling%i.txt' % upsampling), fluxes_photutils)

