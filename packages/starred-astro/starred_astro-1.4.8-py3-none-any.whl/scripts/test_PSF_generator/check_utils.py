import copy
import glob
import os
from astropy.io import fits
from starred.utils.generic_utils import Downsample
from starred.psf.psf import PSF
import matplotlib.pyplot as plt

import pickle as pkl
import numpy as np

def get_aperture_photometry(folder):
    stars = sorted(glob.glob(os.path.join(folder, 'stars', 'star_*.fits')))
    aperture_photometry = [np.sum(fits.open(st)[0].data) for st in stars]

    return aperture_photometry

def get_astrometric_error(model, kwargs_final, kwargs_true, verbose=True):
    """
    Return the precision, accuracy and total MAE astrometric error
    """

    _, mag_true, shift_true, _ = kwargs_true
    x0_true = [dxdy[1] for dxdy in shift_true]
    y0_true = [dxdy[0] for dxdy in shift_true]

    if isinstance(model, PSF):
        coord = model.get_astrometry(**kwargs_final)
    elif isinstance(model, list) or isinstance(model, np.ndarray):
        coord = model
    else :
        raise RuntimeError('Unknown mode of type %s'%type(model))
    x0_fit = coord[:,0]
    y0_fit = coord[:, 1]

    astrometry_error_x = x0_true - x0_fit
    astrometry_error_y = y0_true - y0_fit
    tot_error = np.mean(np.sqrt(astrometry_error_x**2 + astrometry_error_y**2))
    bias_x = np.mean(astrometry_error_x)
    bias_y = np.mean(astrometry_error_y)

    if verbose:
        print('Astrometric residuals x :', astrometry_error_x)
        print('Astrometric residuals y :', astrometry_error_y)

    astrometry_error_x -= np.median(astrometry_error_x)
    astrometry_error_y -= np.median(astrometry_error_y)
    astrometry_error = np.sqrt((astrometry_error_x) ** 2 + (astrometry_error_y) ** 2)

    precision = np.mean(np.abs(astrometry_error))
    accuracy = np.sqrt(bias_x**2 + bias_y**2)

    if verbose:
        print('Astrometric residuals :', astrometry_error)
        print('Astrometric precision :', precision)
        print('Astrometric accuracy :', accuracy)
        print('Total MAE astrometric error :',tot_error)

    return precision, accuracy, tot_error

def get_photometric_error(model, norm, kwargs_final, kwargs_true, verbose=True, high_res=False):
    """
    Return the precision, accuracy and total MAE photometric error
    """
    flux_true, mag_true, _, _ = kwargs_true
    flux_true = np.asarray(flux_true)

    if isinstance(model, PSF):
        flux_model = model.get_photometry(**kwargs_final, high_res=high_res) * norm
    elif isinstance(model, list) or isinstance(model, np.ndarray):
        flux_model = model
    else :
        raise RuntimeError('Unknown mode of type %s'%type(model))
    
    flux_residuals = (flux_model - flux_true) / flux_true
    rel_acc = np.mean(flux_residuals)
    rel_precision = np.mean(np.abs(flux_residuals -  rel_acc))
    tot_error = np.mean(np.abs(flux_residuals))


    if verbose:
        print('Photometric errors :', flux_residuals)
        print('Relative photometric precision :', rel_precision)
        print('Relative photometric acuracy :',rel_acc)
        print('Total MAE photometric error :',tot_error)

    return rel_precision, rel_acc, tot_error

def get_aperture_photometric_error(kwargs_true, aperture_photometry = None, verbose=True):
    flux_true, mag_true, _, _ = kwargs_true
    flux_true = np.asarray(flux_true)

    if aperture_photometry is not None :
        aperture_error = (aperture_photometry - flux_true) / flux_true
    else :
        aperture_error = np.nan(len(flux_true))
    
    rel_acc = np.mean(aperture_error)
    rel_precision = np.mean(np.abs(aperture_error -  rel_acc))
    tot_error = np.mean(np.abs(aperture_error))

    if verbose:
        print('Photometric aperture errors :', aperture_error)
        print('Relative aperture photometric precision :', rel_precision)
        print('Relative aperture photometric acuracy :',rel_acc)
        print('Total MAE aperture photometric error :',tot_error)

    return rel_precision, rel_acc, tot_error

def check_psf_fidelity(psf, true_PSF_down, true_PSF_up, N_intern = 10, verbose = True):
    """
    Provide either a starred.psf.psf.PSF classs or a list containing the upssampled and downsampled PSF.

    Metrics are : i) MAE of the PSF (up and downsampled), ii) Max error of the PSF (up and downsampled),
     iii) MAE of the inner PSF (up and downsampled, central N_intern pixels)

     :param N_intern: Internal region to compute the inner PSF error (in unit of big downsampled pixels)
    """

    if isinstance(psf, list):
        psf_up, psf_down = psf
    else: 
        psf_up = psf
    
    psf_up /= np.sum(psf_up)    

    true_psf_size_up, _ = np.shape(true_PSF_up)
    true_psf_size_down, _ = np.shape(true_PSF_down)
    upsampling_factor = int(true_psf_size_up/true_psf_size_down)
    N_intern_up = N_intern * upsampling_factor

    psf_down = Downsample(psf_up, upsampling_factor)
    psf_down /= np.sum(psf_down) # normalise the PSF

    true_PSF_up /= np.sum(true_PSF_up)
    true_PSF_down /= np.sum(true_PSF_down)

    psf_up = np.asarray(psf_up)
    psf_down = np.asarray(psf_down)
    residuals_psf_up = psf_up - true_PSF_up
    residuals_psf_down = psf_down - true_PSF_down

    # print(np.sum(psf_up), np.sum(true_PSF_up))
    # print(np.min(psf_up), np.max(psf_up))
    # print(np.min(true_PSF_up), np.max(true_PSF_up))
    # print(np.min(residuals_psf_up), np.max(residuals_psf_up))

    MAE_error_up = np.mean(np.abs(psf_up - true_PSF_up))
    MAE_error_down = np.mean(np.abs(psf_down - true_PSF_down))

    max_error_rel_up = np.max(np.abs(psf_up - true_PSF_up) / np.max(true_PSF_up))
    max_error_rel_down = np.max(np.abs(psf_down - true_PSF_down) / np.max(true_PSF_down))

    # in unit of true psf subsampling factor
    MAE_error_inner_up = np.mean(np.abs(psf_up[int(true_psf_size_up / 2) - N_intern_up:int(true_psf_size_up / 2) + N_intern_up,
                                              int(true_psf_size_up / 2) - N_intern_up:int(true_psf_size_up / 2) + N_intern_up] - true_PSF_up[
                                                int(true_psf_size_up / 2) - N_intern_up:int(true_psf_size_up / 2) + N_intern_up,
                                                int(true_psf_size_up / 2) - N_intern_up:int(true_psf_size_up / 2) + N_intern_up]))

    MAE_error_inner_down = np.mean(np.abs(psf_down[int(true_psf_size_up / 2) - N_intern:int(true_psf_size_up / 2) + N_intern,
                                              int(true_psf_size_up / 2) - N_intern:int(true_psf_size_up / 2) + N_intern] - true_PSF_down[
                                                int(true_psf_size_up / 2) - N_intern:int(true_psf_size_up / 2) + N_intern,
                                                int(true_psf_size_up / 2) - N_intern:int(true_psf_size_up / 2) + N_intern]))

    if verbose :
        print('PSF MAE error (upsampled, downsampled):', MAE_error_up, MAE_error_down)
        print('PSF max error (upsampled, downsampled) :', max_error_rel_up, max_error_rel_down)
        print('PSF MAE error on inner %i, %i pixels region (upsampled, downsampled):'%(N_intern_up, N_intern), MAE_error_inner_up, MAE_error_inner_down)


    return [MAE_error_up, MAE_error_down], [max_error_rel_up, max_error_rel_down], \
           [MAE_error_inner_up, MAE_error_inner_down], [np.asarray(psf_up), np.asarray(psf_down)], [residuals_psf_up, residuals_psf_down]

def plot_residuals(residuals_starred, psf_starred, residuals_test = None, test_up = None , test_down = None, data_set = 'Photutils', show= False):
    if residuals_test is not None :
        fig, ax = plt.subplots(2, 2, figsize=(10, 10))
        im0 = ax[0, 0].imshow(residuals_starred[0])
        fig.colorbar(im0, orientation='vertical', ax=ax[0, 0])
        ax[0, 0].set_title('STARRED - Truth')
        im1 = ax[0, 1].imshow(residuals_test[0])
        fig.colorbar(im1, orientation='vertical', ax=ax[0, 1])
        ax[0, 1].set_title('%s - Truth'%data_set)
        im2 = ax[1, 0].imshow(test_up - psf_starred[0])
        fig.colorbar(im2, orientation='vertical', ax=ax[1, 0])
        ax[1, 0].set_title('%s - STARRED'%data_set)
        im3 = ax[1, 1].imshow(test_down - psf_starred[1])
        fig.colorbar(im3, orientation='vertical', ax=ax[1, 1])
        ax[1, 1].set_title('%s - STARRED downsampled'%data_set)
    else :
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        im0 = ax.imshow(residuals_starred[0])
        fig.colorbar(im0, orientation='vertical', ax=ax)
        ax.set_title('STARRED - Truth')

    if show:
        plt.show()

    return fig

