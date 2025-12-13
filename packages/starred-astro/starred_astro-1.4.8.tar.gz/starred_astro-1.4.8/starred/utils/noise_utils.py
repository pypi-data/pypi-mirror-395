import time
import numpy as np
from starred.deconvolution.deconvolution import Deconv
from starred.psf.psf import PSF
from starred.utils.jax_utils import decompose
from starred.utils.generic_utils import Upsample
from copy import deepcopy
from scipy.ndimage import shift
import warnings


def propagate_noise(model, noise_maps, kwargs, masks=None, wavelet_type_list=['starlet'],
                    method='MC', num_samples=100, seed=None,
                    likelihood_type='chi2', verbose=False,
                    upsampling_factor=1, scaling_noise_ref=None):
    """Performs noise propagation using MC or SLIT methods.
    
    :param model: array containing the model
    :param noise_maps: array containing the noise maps
    :param kwargs:  dictionary containing the parameters of the model
    :param masks: array containing the masks
    :param wavelet_type_list: list with the appropriate wavelet families
    :param method: method for noise propagation. Choose 'MC' for an empirical propagation of the noise or 'SLIT' for analytical propagation.
    :param num_samples: number of realizations for the MC method. Not used if `method`='SLIT'.
    :type num_samples: int
    :param upsampling_factor: the upsampling factor
    :type upsampling_factor: int
    :param scaling_noise_ref: index position of the reference noise map (lambda is given in the unit of standard deviation for this noise map).
    Leave it to `None` to take the mean of all provided noise maps (recommended). This only works for the PSF reconstruction. For the deconvolution,
    the reference image's noise map is always used, so lambda is given in unit of noise level, according to this noise map.
    :type scaling_noise_ref: integer

    """
    if likelihood_type not in ['l2_norm', 'chi2']:
        raise ValueError("Only 'l2_norm' and 'chi2' are supported options for likelihood_type.")

    n_image, n_pix, n_pix = np.shape(noise_maps)
    if isinstance(model, PSF):
        if scaling_noise_ref is None:
            masked_noise = deepcopy(noise_maps)
            if masks is not None:
                ind = np.where(masks == 0)
                masked_noise = deepcopy(noise_maps)
                masked_noise[ind] = np.nan

            centered_masked_noise_maps = np.zeros_like(masked_noise)
            # center the noise maps according to the estimated shift, we just use linear interpolation here
            for i in range(n_image):
                centered_masked_noise_maps[i] = shift(input=deepcopy(masked_noise[i]),
                                                      shift=(-kwargs['kwargs_gaussian']['y0'][i],
                                                             -kwargs['kwargs_gaussian']['x0'][i]),
                                                      mode='constant', cval=np.nan, order=1)
            noise_map = np.nanmean(centered_masked_noise_maps, axis=0)

        else:
            if masks is not None:
                if not np.all(masks[scaling_noise_ref, :, :] == 1.):
                    raise RuntimeError(
                        "Your reference star contain masked pixels, I cannot propagate the noise correctly. "
                        "Use `scaling_noise_ref = None` or remove the mask."
                    )
            noise_map = shift(deepcopy(noise_maps[scaling_noise_ref, :, :]), (
                - kwargs['kwargs_gaussian']['y0'][scaling_noise_ref],
                - kwargs['kwargs_gaussian']['x0'][scaling_noise_ref]), mode='constant', cval=np.nan, order=1)

        # check that there is no region which is not covered by any stars. If we are unlucky and this is the case,
        # we will fill with the median noise level.
        noise_map = np.nan_to_num(noise_map, nan=np.nanmedian(noise_map)) / np.sqrt(n_image)
        # (this is an effective noise map, scales as 1/sqrt(number of stars) )

        # get the centered convolution kernel
        kwargs_centered = deepcopy(kwargs['kwargs_gaussian'])
        kwargs_centered['x0'] = np.zeros(n_image)
        kwargs_centered['y0'] = np.zeros(n_image)
        deconv_kernel = model.get_gaussian(0, kwargs_centered, deepcopy(kwargs['kwargs_moffat']))
        # (get the gaussian kernel, will be normalised to 1 later)
        a = 1  # leave the possibility to adjust but this should be set to one

    elif isinstance(model, Deconv):
        # for the deconvolution, things are simpler, the reference image always is used to scale the lambda parameter.
        if scaling_noise_ref is not None:
            if scaling_noise_ref != 0:
                warnings.warn(
                    'For the deconvolution, we will use the reference image for the noise propagation in any cases. '
                    '"scaling_noise_ref" is not used.')
        noise_map = deepcopy(noise_maps[0, :, :]) / np.sqrt(
            n_image)  # effective noise maps, assuming all images have the same exposure time
        deconv_kernel = model.psf[0, :, :]
        a = 1  # leave the possibility to adjust but this should be set to one
    else:
        raise TypeError('Unknown instance.')

    deconv_kernel /= np.sum(deconv_kernel)  # normalise kernel

    var_map = np.array(noise_map ** 2)  # cast to numpy array otherwise computations are slowed down
    std_map = np.array(noise_map)

    # wavelet transform Phi^T operators
    PhiT_operator_list = []
    num_scales_list = []
    for wavelet_type in wavelet_type_list:
        if wavelet_type in ['battle-lemarie-1', 'battle-lemarie-3']:
            num_scales = 1  # we only care about the first scale for this one
        else:
            num_scales = int(np.log2(min(n_pix * upsampling_factor, n_pix * upsampling_factor)))
        # wavelet = jax_utils.WaveletTransform(num_scales,
        #                                      wavelet_type=wavelet_type,
        #                                      )
        PhiT_operator_list.append(decompose)
        num_scales_list.append(num_scales)

    nx_psi, ny_psi = n_pix * upsampling_factor, n_pix * upsampling_factor

    psi_wt_std_list = []
    # map noise values to source plane

    if method == 'MC':
        psi_wt_std_list = []
        for wavelet_type, PhiT_operator, num_scales in zip(wavelet_type_list, PhiT_operator_list, num_scales_list):
            start = time.time()
            psi_wt_reals = []
            np.random.seed(seed)
            std_map_up = Upsample(std_map, factor=upsampling_factor)
            var_map_up = Upsample(var_map, factor=upsampling_factor)
            for i in range(num_samples):
                noise_i = std_map_up * np.random.randn(*std_map_up.shape)  # draw a noise realization
                noise_i2 = std_map_up * np.random.randn(*std_map_up.shape)  # draw a noise realization

                # if chi2 loss, rescale by the data variance
                if likelihood_type == 'chi2':
                    noise_i /= var_map_up  # operator Ck -1 (so that w has unit of 1/flux)

                # before, noise_i was upscaled here and the result stored in psi_i.
                # Now the upscaling is done earlier, but we keep the link psi_i = noise_i
                psi_i = noise_i
                psi_i_blurred = model._convolve(psi_i, deconv_kernel)  # Bt operator
                psi_i_blurred *= a  # transpose of scalar multiplication is the multiplication by a scalar
                psi_wt_i = PhiT_operator(psi_i_blurred, num_scales)
                psi_wt_reals.append(psi_wt_i)

            psi_wt_reals = np.array(psi_wt_reals)  # --> shape = (num_samples, num_scales, nx_psi, ny_psi)
            if verbose: print(f"loop over MC samples for wavelet '{wavelet_type}':", time.time() - start)

            # compute the variance per wavelet scale per potential pixel over all the samples
            psi_wt_var = np.var(psi_wt_reals, axis=0)
            # check
            if np.any(psi_wt_var < 0.):  # pragma: no cover
                raise ValueError("Negative variance terms!")

            # convert to standard deviation
            psi_wt_std = np.sqrt(psi_wt_var)
            psi_wt_std_list.append(psi_wt_std)

    elif method == 'SLIT':

        for PhiT_operator, num_scales in zip(PhiT_operator_list, num_scales_list):

            noise_diag = std_map * np.sqrt(np.sum(deconv_kernel.T ** 2))
            if likelihood_type == 'chi2':
                noise_diag /= var_map
            noise_diag_up = Upsample(noise_diag, factor=upsampling_factor)

            blurred_noise = a * model._convolve(noise_diag_up, deconv_kernel)

            dirac = np.zeros((nx_psi, ny_psi))
            dirac[nx_psi // 2, ny_psi // 2] = 1
            dirac_wt = PhiT_operator(dirac, num_scales)

            psi_wt_std = []
            for k in range(num_scales + 1):
                psi_wt_std2_k = model._convolve(blurred_noise ** 2, dirac_wt[k] ** 2)
                psi_wt_std_k = np.sqrt(psi_wt_std2_k)
                psi_wt_std_k = np.nan_to_num(psi_wt_std_k, nan=np.nanmin(
                    psi_wt_std_k)) * upsampling_factor ** 2  # scaling is important here to match 'MC' scaling convention
                psi_wt_std.append(psi_wt_std_k)
            psi_wt_std = np.array(psi_wt_std)  # --> shape = (num_scales, nx_psi, ny_psi)
            psi_wt_std_list.append(psi_wt_std)  # one per type of (wavelet, num_scales)
    else:
        raise ValueError(f"Method '{method}' for noise propagation is not supported.")

    return psi_wt_std_list


def dirac_impulse(num_pix):
    """
    Returns a 2D array with a Dirac impulse at its center.

    :param num_pix: number of pixels per axis
    :type num_pix: int
    :return: 2D array

    """
    dirac = np.zeros((num_pix, num_pix), dtype=float)
    dirac[int(num_pix / 2), int(num_pix / 2)] = 1.
    return dirac
