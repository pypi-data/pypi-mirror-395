import numpy as np
import jax.numpy as jnp
from copy import deepcopy
import warnings

from starred.psf.psf import PSF
from starred.psf.loss import Loss, Prior
from starred.optim.optimization import Optimizer
from starred.psf.parameters import ParametersPSF
from starred.utils.noise_utils import propagate_noise
from starred.utils.generic_utils import fourier_division, gaussian_function, fwhm2sigma, make_grid, Downsample
from starred.plots import plot_function as pltf
import matplotlib.pyplot as plt


def sanitize_inputs(image, noisemap, masks):
    """
    Sanitizes input arrays by masking NaN values and updating masks, image, and noisemap accordingly.

    Parameters
    -------------
    image: array (numpy.ndarray or jax.numpy.ndarray)
        The input image array of shape (N, nx, ny) where N is the number of stamps.

    noisemap: array (numpy.ndarray or jax.numpy.ndarray)
        The noise map array of shape (N, nx, ny) where N is the number of stamps.

    masks: array (numpy.ndarray or jax.numpy.ndarray)
        The mask array of shape (N, nx, ny) where N is the number of stamps.

    Returns
    -------------
    image: array (numpy.ndarray or jax.numpy.ndarray)
        The sanitized image array with NaN values replaced by 0.

    noisemap: array (numpy.ndarray or jax.numpy.ndarray)
        The sanitized noisemap array with NaN values replaced by 1.

    masks: array (numpy.ndarray or jax.numpy.ndarray)
        The updated mask array where positions with NaN in image or noisemap are set to False.
    """
    # first, if no mask provided by user (masks is None), then make masks:
    if masks is None:
        # also, stick to the input type
        if isinstance(image, jnp.ndarray):
            masks = jnp.ones_like(image, dtype=bool)
        else:
            masks = np.ones_like(image, dtype=bool)

    # check that we are not mixing numpy and jax arrays
    if not ((type(image) is type(noisemap)) and (type(image) is type(masks))):
        raise TypeError("Preventive error: try not mixing jax and numpy arrays for inputs")
    # check the type to use the correct module
    xp = np if isinstance(image, np.ndarray) else jnp

    bad_pixels = xp.isnan(image * noisemap)
    masks = xp.where(bad_pixels, False, masks)
    image = xp.where(bad_pixels, 0., image)  # dummy values for image and noisemap, masked anyway
    noisemap = xp.where(bad_pixels, 1., noisemap)

    return image, noisemap, masks


def build_psf(image, noisemap, subsampling_factor,
              masks=None,
              n_iter_analytic=40, n_iter_adabelief=2000,
              guess_method_star_position='barycenter', guess_fwhm_pixels=3.,
              field_distortion=False, stamp_coordinates=None, adjust_sky=False):
    """

    Routine taking in cutouts of stars (shape (N, nx, ny), with N the number of star cutouts, and nx,ny the shape of each cutout)
    and their noisemaps (same shape), producing a narrow PSF with pixel grid of the given subsampling_factor

    Parameters
    ----------
    image : array, shape (imageno, nx, ny)
        array containing the data
    noisemap : array, shape (imageno, nx, ny)
        array containing the noisemaps.
    subsampling_factor : int
        by how much we supersample the PSF pixel grid compare to data.
    masks: optional, array of same shape as image and noisemap containing 1 for pixels to be used, 0 for pixels to be ignored.
    n_iter_analytic: int, optional, number of iterations for fitting the moffat in the first step
    n_iter_adabelief: int, optional, number of iterations for fitting the background in the second step
    guess_method_star_position: str, optional, one of 'barycenter', 'max' or 'center'
    guess_fwhm_pixels: float, the estimated FWHM of the PSF, is used to initialize the moffat. Default 3.
    field_distortion: whether we allow the psf to vary across the field. If yes, 'stamp_coordinates' must be supplied.
    stamp_coordinates: array of shape (imageno, 2), the pixel coordinates of the different stars in data.
    adjust_sky: bool, optional, if True, the sky level is adjusted for each PSF star. Default False.

    Returns
    -------
    result : dictionary.
        dictionary containing the narrow PSF (key narrow_psf) and other useful things.

    """
    # checks
    if field_distortion and (stamp_coordinates is None):
        raise RuntimeError(
            "starred.psf_routines.build_psf: asked to include field distortions,"
            "but no star positions on the ccd (argument stamp_coordinates) provided."
        )

    # sanitize inputs: mask NaN values
    image, noisemap, masks = sanitize_inputs(image, noisemap, masks)

    # normalize by max of data(numerical precision best with scale ~ 1)
    norm = np.nanpercentile(image, 99.)
    image /= norm
    noisemap /= norm

    model = PSF(image_size=image[0].shape[0], number_of_sources=len(image),
                upsampling_factor=subsampling_factor,
                convolution_method='fft',
                include_moffat=True,
                elliptical_moffat=True,
                field_distortion=field_distortion)

    smartguess = lambda im: model.smart_guess(im, fixed_background=True, guess_method=guess_method_star_position,
                                              masks=masks, guess_fwhm_pixels=guess_fwhm_pixels, adjust_sky=adjust_sky)

    # Parameter initialization.
    kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = smartguess(image)

    # smartguess doesn't know about cosmics, other stars ...
    # so we'll be a bit careful.
    medx0 = np.median(kwargs_init['kwargs_gaussian']['x0'])
    medy0 = np.median(kwargs_init['kwargs_gaussian']['y0'])
    kwargs_init['kwargs_gaussian']['x0'] = medx0 * np.ones_like(kwargs_init['kwargs_gaussian']['x0'])
    kwargs_init['kwargs_gaussian']['y0'] = medy0 * np.ones_like(kwargs_init['kwargs_gaussian']['y0'])

    parameters = ParametersPSF(kwargs_init,
                               kwargs_fixed,
                               kwargs_up=kwargs_up,
                               kwargs_down=kwargs_down)

    loss = Loss(image, model, parameters, noisemap**2, len(image),
                regularization_terms='l1_starlet',
                regularization_strength_scales=0,
                regularization_strength_hf=0,
                masks=masks,
                star_positions=stamp_coordinates)

    optim = Optimizer(loss,
                      parameters,
                      method='l-bfgs-b')

    # fit the moffat:
    best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(maxiter=n_iter_analytic,
                                                                    restart_from_init=True)

    kwargs_partial = parameters.args2kwargs(best_fit)

    # now moving on to the background.
    # Release background and distortion, fix the moffat
    kwargs_fixed = {
        'kwargs_moffat': {'fwhm_x': kwargs_partial['kwargs_moffat']['fwhm_x'],
                          'fwhm_y': kwargs_partial['kwargs_moffat']['fwhm_y'],
                          'phi': kwargs_partial['kwargs_moffat']['phi'],
                          'beta': kwargs_partial['kwargs_moffat']['beta'],
                          'C': kwargs_partial['kwargs_moffat']['C']},
        'kwargs_gaussian': {},
        'kwargs_background': {},
        'kwargs_distortion': deepcopy(kwargs_init['kwargs_distortion'])
    }

    if not adjust_sky:
        kwargs_fixed['kwargs_background']['mean'] = deepcopy(kwargs_init['kwargs_background']['mean'])

    parametersfull = ParametersPSF(kwargs_partial,
                                   kwargs_fixed,
                                   kwargs_up,
                                   kwargs_down)

    # median of noisemaps, but still fully mask any pixel that might be crazy in any of the frames.
    average_noisemap = np.nanmedian(noisemap, axis=0)
    average_noisemap = np.expand_dims(average_noisemap, (0,))
    mask = np.min(masks, axis=0)
    mask = np.expand_dims(mask, (0,))
    W = propagate_noise(model=model, noise_maps=average_noisemap, kwargs=kwargs_init,
                        masks=mask,
                        wavelet_type_list=['starlet'],
                        method='MC', num_samples=100,
                        seed=1, likelihood_type='chi2',
                        verbose=False,
                        upsampling_factor=subsampling_factor)[0]

    lossfull = Loss(image, model, parametersfull,
                    noisemap**2, len(image),
                    regularization_terms='l1_starlet',
                    regularization_strength_scales=1.,
                    regularization_strength_hf=1.,
                    regularization_strength_positivity=0,
                    W=W,
                    regularize_full_psf=False,
                    masks=masks,
                    star_positions=stamp_coordinates)

    optimfull = Optimizer(lossfull, parametersfull, method='adabelief')

    optimiser_optax_option = {
                                'max_iterations': n_iter_adabelief, 'min_iterations': None,
                                'init_learning_rate': 1e-4, 'schedule_learning_rate': True,
                                # important: restart_from_init True
                                'restart_from_init': True, 'stop_at_loss_increase': False,
                                'progress_bar': True, 'return_param_history': True
                              }

    best_fit, logL_best_fit, extra_fields2, runtime = optimfull.minimize(**optimiser_optax_option)

    kwargs_partial2 = parametersfull.args2kwargs(best_fit)

    # this last step is just permitting distortion in the field.
    if field_distortion:
        kwargs_fixed = {
            'kwargs_moffat': {'fwhm_x': kwargs_partial2['kwargs_moffat']['fwhm_x'],
                              'fwhm_y': kwargs_partial2['kwargs_moffat']['fwhm_y'],
                              'phi': kwargs_partial2['kwargs_moffat']['phi'],
                              'beta': kwargs_partial2['kwargs_moffat']['beta'],
                              'C': kwargs_partial2['kwargs_moffat']['C']},
            'kwargs_gaussian': {},
            'kwargs_background': {},
            'kwargs_distortion': {}
        }

        if not adjust_sky:
            kwargs_fixed['kwargs_background']['mean'] = deepcopy(kwargs_init['kwargs_background']['mean'])

        parametersfull = ParametersPSF(kwargs_partial2,
                                       kwargs_fixed,
                                       kwargs_up,
                                       kwargs_down)

        lossfull = Loss(image, model, parametersfull,
                        noisemap ** 2, len(image),
                        regularization_terms='l1_starlet',
                        regularization_strength_scales=1.,
                        regularization_strength_hf=1.,
                        regularization_strength_positivity=0,
                        W=W,
                        regularize_full_psf=False,
                        masks=masks,
                        star_positions=stamp_coordinates)

        optimfull = Optimizer(lossfull, parametersfull, method='adabelief')

        optimiser_optax_option = {
            'max_iterations': 1000, 'min_iterations': None,
            'init_learning_rate': 3e-5, 'schedule_learning_rate': True,
            'restart_from_init': True, 'stop_at_loss_increase': False,
            'progress_bar': True, 'return_param_history': True
        }

        best_fit, logL_best_fit, extra_fields3, runtime = optimfull.minimize(**optimiser_optax_option)
        extra_fields2['loss_history'] = np.append(extra_fields2['loss_history'], extra_fields3['loss_history'])
        kwargs_final = parametersfull.args2kwargs(best_fit)
    else:
        kwargs_final = kwargs_partial2

    ###########################################################################
    # book keeping
    narrowpsf = model.get_narrow_psf(**kwargs_final, norm=True)
    fullpsf = model.get_full_psf(**kwargs_final, norm=True)
    numpsf = model.get_background(kwargs_final['kwargs_background'])
    moffat = model.get_moffat(kwargs_final['kwargs_moffat'], norm=True)
    fullmodel = model.model(**kwargs_final, positions=stamp_coordinates)
    residuals = image - fullmodel
    # approximate chi2: hard to count params with regularization - indicative.
    chi2 = masks * residuals**2 / noisemap**2
    valid_pixels_count = np.sum(masks)
    red_chi2 = np.sum(chi2) / valid_pixels_count
    valid_pixels_count_per_slice = np.sum(masks, axis=(1,2)) + 1e-3 
    # above, + 1e-3 to avoid potential divisions by 0.  the user should not
    # input fully masked stamps anyways, but never know.
    # if fully masked, will yield a very large reduced chi2, which would make
    # it easy to flag.
    red_chi2_per_stamp = np.sum(chi2, axis=(1, 2)) / valid_pixels_count_per_slice[:, None]

    result = {
        'model_instance': model,
        'kwargs_psf': kwargs_final,
        'narrow_psf': narrowpsf,
        'full_psf': fullpsf,
        'numerical_psf': numpsf,
        'moffat': moffat,
        'models': fullmodel,
        'residuals': residuals,
        'analytical_optimizer_extra_fields': extra_fields,
        'adabelief_extra_fields': extra_fields2,
        'chi2': red_chi2,
        'chi2_per_stamp': red_chi2_per_stamp
    }
    ###########################################################################
    return result


def run_multi_steps_PSF_reconstruction(data, model, parameters, sigma_2, masks=None, star_positions=None,
                                       lambda_scales=1., lambda_hf=1., lambda_positivity=0.,
                                       fitting_sequence=[['background'], ['moffat']],
                                       optim_list=['l-bfgs-b', 'adabelief'],
                                       kwargs_optim_list=None,
                                       method_noise='MC', regularize_full_psf=False,
                                       adjust_sky=False,
                                       verbose=True):
    """
    A high level function for a custom fitting sequence. Similar to build_psf() but with more options.

    :param data: array containing the observations
    :param model: Point Spread Function (PSF) class from ``starred.psf.psf``
    :param parameters: parameters class from ``starred.psf.parameters``
    :param sigma_2: array containing the square of the noise maps
    :param star_positions: default None, array of shape (N, 2) containing pixel coordinates of the stars (center of the image: (0,0)).
    :param lambda_scales: Lagrange parameter that weights intermediate scales in the transformed domain.
    :param lambda_hf: Lagrange parameter weighting the highest frequency scale
    :param lambda_positivity: Lagrange parameter weighting the positivity of the full PSF. 0 means no positivity constraint (recommended).
    :param fitting_sequence: list, List of lists, containing the element of the model to keep fixed. Example : [['pts-source-astrometry','pts-source-photometry','background'],['pts-source-astrometry','pts-source-photometry'], ...]
    :param optim_list: List of optimiser. Recommended if background is kept constant : 'l-bfgs-b', 'adabelief' otherwise.
    :param kwargs_optim_list: List of dictionary, containing the setting for the different optimiser.
    :param method_noise: method for noise propagation. Choose 'MC' for an empirical propagation of the noise or 'SLIT' for analytical propagation.
    :param regularize_full_psf: True if you want to regularize the Moffat and the background. False regularizes only the background (recommended)
    :param masks: array containing the masks for the PSF (if given)
    :param adjust_sky: bool, if True, the sky level is adjusted for each PSF star. Default False

    :return model, parameters, loss, kwargs_partial_list, LogL_list, loss_history_list
    """

    # Sanitize inputs
    data, sigma_2, masks = sanitize_inputs(data, sigma_2, masks)

    # Check the sequence
    assert len(fitting_sequence) == len(optim_list), "Fitting sequence and optimiser list have different lengths!"
    if kwargs_optim_list is not None:
        assert len(fitting_sequence) == len(
            kwargs_optim_list), "Fitting sequence and kwargs optimiser list have different lenght !"
    else:
        warnings.warn('No optimiser kwargs provided. Default configuration is used.')
        kwargs_optim_list = [{} for _ in range(len(fitting_sequence))]
    kwargs_init, kwargs_fixed_default, kwargs_up, kwargs_down = deepcopy(parameters._kwargs_init), deepcopy(
        parameters._kwargs_fixed), \
        deepcopy(parameters._kwargs_up), deepcopy(parameters._kwargs_down)
    if star_positions is not None:
        assert model.field_distortion, "Star positions are provided but the model does not include field distortion. Please set 'field_distortion=True' in the PSF model."

    kwargs_partial_list = [kwargs_init]
    loss_history_list = []
    LogL_list = []
    W = None

    for i, steps in enumerate(fitting_sequence):
        kwargs_fixed = deepcopy(kwargs_fixed_default)
        background_free = True
        print(f'### Step {i + 1}, fixing : {steps} ###')
        for fixed_feature in steps:
            if fixed_feature == 'pts-source-astrometry':
                kwargs_fixed['kwargs_gaussian']['x0'] = kwargs_partial_list[i]['kwargs_gaussian']['x0']
                kwargs_fixed['kwargs_gaussian']['y0'] = kwargs_partial_list[i]['kwargs_gaussian']['y0']
            elif fixed_feature == 'pts-source-photometry':
                kwargs_fixed['kwargs_gaussian']['a'] = kwargs_partial_list[i]['kwargs_gaussian']['a']
                kwargs_fixed['kwargs_moffat']['C'] = kwargs_partial_list[i]['kwargs_moffat']['C']
            elif fixed_feature == 'background':
                # TODO: check if there is a speed up when skipping regularization in the case of a fixed background
                kwargs_fixed['kwargs_background']['background'] = kwargs_partial_list[i]['kwargs_background'][
                    'background']
                background_free = False
            elif fixed_feature == 'moffat':
                if model.elliptical_moffat:
                    kwargs_fixed['kwargs_moffat']['fwhm_x'] = kwargs_partial_list[i]['kwargs_moffat']['fwhm_x']
                    kwargs_fixed['kwargs_moffat']['fwhm_y'] = kwargs_partial_list[i]['kwargs_moffat']['fwhm_y']
                    kwargs_fixed['kwargs_moffat']['phi'] = kwargs_partial_list[i]['kwargs_moffat']['phi']
                else:
                    kwargs_fixed['kwargs_moffat']['fwhm'] = kwargs_partial_list[i]['kwargs_moffat']['fwhm']
                kwargs_fixed['kwargs_moffat']['beta'] = kwargs_partial_list[i]['kwargs_moffat']['beta']
                kwargs_fixed['kwargs_moffat']['C'] = kwargs_partial_list[i]['kwargs_moffat']['C']
            elif fixed_feature == 'distortion':
                kwargs_fixed['kwargs_distortion']['dilation_x'] = kwargs_partial_list[i]['kwargs_distortion']['dilation_x']
                kwargs_fixed['kwargs_distortion']['dilation_y'] = kwargs_partial_list[i]['kwargs_distortion']['dilation_y']
                kwargs_fixed['kwargs_distortion']['shear'] = kwargs_partial_list[i]['kwargs_distortion']['shear']
            else:
                raise ValueError(
                    f'Steps {steps} is not defined. Choose between "pts-source-astrometry", "pts-source-photometry", "background", "moffat" or "distortion"')

        # Lift degeneracy between background and Moffat by fixing Moffat amplitude
        if background_free:
            kwargs_fixed['kwargs_moffat']['C'] = kwargs_partial_list[i]['kwargs_moffat']['C']
            lambda_scales_eff = deepcopy(lambda_scales)
            lambda_hf_eff = deepcopy(lambda_hf)
        else:
            # remove regularization for speed up
            lambda_scales_eff = 0.
            lambda_hf_eff = 0.

        if not adjust_sky:
            kwargs_fixed['kwargs_background']['mean'] = deepcopy(kwargs_init['kwargs_background']['mean'])

        # recompile the parameter class as we have changed the number of free parameters
        parameters = ParametersPSF(kwargs_partial_list[i], kwargs_fixed, kwargs_up, kwargs_down)
        loss = Loss(data, model, parameters, sigma_2, model.M, masks=masks, star_positions=star_positions,
                    regularization_terms='l1_starlet',
                    regularization_strength_scales=lambda_scales_eff, regularization_strength_hf=lambda_hf_eff,
                    regularization_strength_positivity=lambda_positivity, W=W,
                    regularize_full_psf=regularize_full_psf)

        optim = Optimizer(loss, parameters, method=optim_list[i])
        best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(**kwargs_optim_list[i])
        if verbose:
            try:
                # this will work only for the Jaxopt optimiser, which have a success argument
                if extra_fields['stat'].success:
                    print(
                        f'Success of the step {i + 1} fit in {extra_fields["stat"].iter_num} iterations ({runtime} s)')
                else:
                    print(f'Warning: step {i + 1} fit did not converge !')
            except:
                pass

        # Saving partial results
        kwargs_partial_steps = deepcopy(parameters.best_fit_values(as_kwargs=True))
        loss_history_list.append(extra_fields['loss_history'])
        LogL_list.append(logL_best_fit)

        # compute noise propagation
        W = propagate_noise(model, np.sqrt(sigma_2), kwargs_partial_steps, wavelet_type_list=['starlet'],
                            method=method_noise, masks=masks,
                            num_samples=400, seed=1, likelihood_type='chi2', verbose=False,
                            upsampling_factor=model.upsampling_factor)[0]

        # update kwargs_partial_list
        kwargs_partial_list.append(deepcopy(kwargs_partial_steps))
        if verbose:
            print('Step %i/%i took %2.f seconds' % (i + 1, len(fitting_sequence), runtime))
            print('Kwargs partial at step %i/%i' % (i + 1, len(fitting_sequence)), kwargs_partial_steps)
            print('LogL : ', logL_best_fit)
            print('Overall Reduced Chi2 : ', loss.reduced_chi2(kwargs_partial_steps))

    return model, parameters, loss, kwargs_partial_list, LogL_list, loss_history_list


def update_PSF(kernel_old, data, sigma_2, masks=None,
               lambda_scales=2., lambda_hf=2., lambda_positivity=0.,
               subsampling_factor=2.,
               optim_list=None,
               kwargs_optim_list=None,
               method_noise='MC',
               verbose=True, normalise_data=True, show_plots=False):
    """
    Update the PSF model from a provided kernel. It will not use the Moffat and the PSF will entirely be described
    by the grid of pixel.

    :param kernel_old: array containing the first guess of the kernel (should be the narrow PSF ideally...)
    :param data: arrays containing the observations. Dimension (Nstar x Npix x Npix)
    :param sigma_2: arrays containing the noise maps. Dimension (Nstar x Npix x Npix)
    :param masks: array containing the masks for the PSF (if given)
    :param lambda_scales: Lagrange parameter that weights intermediate scales in the transformed domain.
    :param lambda_hf: Lagrange parameter weighting the highest frequency scale
    :param lambda_positivity: Lagrange parameter weighting the positivity of the full PSF. 0 means no positivity constraint (recommended).
    :param subsampling_factor: int, by how much we supersample the PSF pixel grid compare to data.
    :param optim_list: List of 3 optimisers, one for each step of the fit. Default: ['l-bfgd-b', 'adabelief', 'adabelief']
    :param kwargs_optim_list: List of 3 dictionaries, containing the setting for the different optimiser. Default: None
    :param method_noise: method for noise propagation. Choose 'MC' for an empirical propagation of the noise or 'SLIT' for analytical propagation. Default: 'MC'
    :param verbose: bool, if True, print the progress of the fit. Default: True
    :param normalise_data: bool, if True, renormalise the data before running the fit. Default: True
    :param show_plots: bool, if True, show the plots of the fit. Default: False

    :return kernel_new: array containing the new full PSF
    :return narrow_psf: array containing the narrow PSF
    :return psf_kernel_list: list of arrays containing the PSF kernels fitted to the data
    :return starred_output: list containing the model, parameters, loss, kwargs_partial_list, LogL_list, loss_history_list, norm

    """
    if normalise_data:
        norm = data[0].max()
        data /= norm
        sigma_2 /= norm ** 2
    else:
        norm = 1.

    kwargs_partial_list = []
    LogL_list = []
    loss_history_list = []
    if optim_list is None:
        optim_list = ['l-bfgs-b', 'adabelief', 'adabelief']

    assert len(optim_list) == 3, "The fitting sequence should have 3 steps"

    if kwargs_optim_list is not None:
        assert len(optim_list) == len(
            kwargs_optim_list), "Fitting sequence and kwargs optimiser list have different lenght !"
    else:
        warnings.warn('No optimiser kwargs provided to STARRED. Default configuration is used.')
        kwargs_optim_list = [
            {'maxiter': 2000},  # l-bfgs-b options
            {'max_iterations': 500, 'init_learning_rate': 1e-2},  # adabelief options
            {'max_iterations': 500, 'init_learning_rate': 1e-3},  # adabelief options
        ]

    # Build the PSF model class with no Moffat
    N, image_size, _ = np.shape(data)
    model = PSF(image_size=image_size, number_of_sources=N,
                upsampling_factor=subsampling_factor,
                convolution_method='scipy',
                include_moffat=False)

    # Parameter initialization.
    kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = model.smart_guess(data, fixed_background=True,
                                                                          guess_method='center')
    # Fix the background to the previous kernel
    kwargs_init['kwargs_background']['background'] = np.ravel(kernel_old) / np.sum(kernel_old)
    kwargs_fixed['kwargs_background']['background'] = np.ravel(kernel_old) / np.sum(kernel_old)
    parameters = ParametersPSF(kwargs_init, kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down,
                               include_moffat=False)

    # Align images (keep background fixed)
    loss = Loss(data, model, parameters, sigma_2, N, regularization_terms='l1_starlet',
                regularization_strength_scales=0, regularization_strength_hf=0, masks=masks)
    optim = Optimizer(loss, parameters, method=optim_list[0])

    best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(**kwargs_optim_list[0])
    kwargs_partial = parameters.args2kwargs(best_fit)
    kwargs_partial_list.append(kwargs_partial)
    loss_history_list.append(extra_fields['loss_history'])
    LogL_list.append(logL_best_fit)

    if verbose:
        print('Step 1/3 took %2.f seconds' % (runtime))
        print('Kwargs partial at step 1/3:', kwargs_partial)
        print('LogL : ', logL_best_fit)
        print('Overall Reduced Chi2 : ', loss.reduced_chi2(kwargs_partial))

    # compute noise propagation
    W = propagate_noise(model, np.sqrt(sigma_2), kwargs_partial, masks=masks, wavelet_type_list=['starlet'],
                        method=method_noise, num_samples=500,
                        seed=1, likelihood_type='chi2', verbose=False, upsampling_factor=subsampling_factor)[0]

    # release background, fix positions and amplitudes
    kwargs_fixed['kwargs_background'] = {}
    kwargs_fixed['kwargs_gaussian']['x0'] = kwargs_partial['kwargs_gaussian']['x0']
    kwargs_fixed['kwargs_gaussian']['y0'] = kwargs_partial['kwargs_gaussian']['y0']
    kwargs_fixed['kwargs_gaussian']['a'] = kwargs_partial['kwargs_gaussian']['a']

    parameters = ParametersPSF(kwargs_partial, kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down,
                               include_moffat=False)

    loss = Loss(data, model, parameters, sigma_2, N, regularization_terms='l1_starlet',
                regularization_strength_scales=lambda_scales, regularization_strength_hf=lambda_hf,
                regularization_strength_positivity=lambda_positivity, W=W, regularize_full_psf=False,
                masks=masks)
    optim = Optimizer(loss, parameters, method=optim_list[1])
    best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(**kwargs_optim_list[1])

    kwargs_partial = parameters.args2kwargs(best_fit)
    kwargs_partial_list.append(kwargs_partial)
    loss_history_list.append(extra_fields['loss_history'])
    LogL_list.append(logL_best_fit)
    if verbose:
        print('Step 2/3 took %2.f seconds' % (runtime))
        print('Kwargs partial at step 2/3:', kwargs_partial)
        print('LogL : ', logL_best_fit)
        print('Overall Reduced Chi2 : ', loss.reduced_chi2(kwargs_partial))

    # Release everything
    kwargs_fixed['kwargs_gaussian'] = {}
    # Add prior on position and photometry to avoid full degeneracy between background and position
    prior_astrom_photom = Prior(prior_gaussian=[['x0', kwargs_partial['kwargs_gaussian']['x0'], 1.],
                                                ['y0', kwargs_partial['kwargs_gaussian']['x0'], 1.],
                                                ['a', kwargs_partial['kwargs_gaussian']['a'],
                                                 0.1 * kwargs_partial['kwargs_gaussian']['a']],
                                                ],
                         prior_background=None, prior_moffat=None)

    print('Applying priors on position to avoid degeneracy between background and position')
    parameters = ParametersPSF(kwargs_partial, kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down,
                               include_moffat=False)

    loss = Loss(data, model, parameters, sigma_2, N, regularization_terms='l1_starlet',
                regularization_strength_scales=lambda_scales, regularization_strength_hf=lambda_hf,
                regularization_strength_positivity=lambda_positivity, W=W, regularize_full_psf=False,
                masks=masks, prior=prior_astrom_photom)
    optim = Optimizer(loss, parameters, method=optim_list[2])
    best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(**kwargs_optim_list[2])

    kwargs_final = parameters.args2kwargs(best_fit)
    kwargs_partial_list.append(kwargs_final)
    loss_history_list.append(extra_fields['loss_history'])
    LogL_list.append(logL_best_fit)
    if verbose:
        print('Step 3/3 took %2.f seconds' % (runtime))
        print('Kwargs partial at step 3/3:', kwargs_final)
        print('LogL : ', logL_best_fit)
        print('Overall Reduced Chi2 : ', loss.reduced_chi2(kwargs_final))

    starred_output = [model, parameters, loss, kwargs_partial_list, LogL_list, loss_history_list, norm]
    kernel_new = model.get_full_psf(**kwargs_final, norm=True, high_res=True)
    narrow_psf = model.get_narrow_psf(**kwargs_final, norm=True)
    psf_kernel_list = model.model(**kwargs_final, high_res=False)

    if show_plots:
        print('Initial data:')
        fig0 = pltf.display_data(data, sigma_2=sigma_2, masks=masks, units='e-')
        for i, kwargs_partial in enumerate(kwargs_partial_list):
            print('Step %i' % i)
            print(kwargs_partial)
            fig1 = pltf.multiple_PSF_plot(model, data, sigma_2, kwargs_partial, masks=masks, units='e-')
            fig_loss1 = pltf.plot_loss(loss_history_list[i])
            plt.show()

    return kernel_new, narrow_psf, psf_kernel_list, starred_output


def narrow_psf_from_model(full_psf_model, subsampling_factor_in, subsampling_factor_out, mode='fourier_division'):
    """
    Compute the narrow PSF from a full PSF model.

    :param full_psf_model: array containing the full PSF model
    :param subsampling_factor_in: int, subsampling factor of the provided full PSF model
    :param subsampling_factor_out: int, subsampling factor of the desired narrow PSF

    :return narrow_psf: array containing the narrow PSF
    """

    if subsampling_factor_out > subsampling_factor_in:
        warnings.warn(
            "The desired subsampling factor is higher than the input subsampling factor of the PSF model. This is a very ill-posed problem because I will need to interpolate your PSF model.")

        if subsampling_factor_out / subsampling_factor_in % 1 != 0:
            raise ValueError("The ratio of the subsampling factors is not an integer. This is not supported.")

        # interpolate the input PSF here
        npsf, _ = np.shape(full_psf_model)
        x, y = make_grid(numPix=npsf * subsampling_factor_out / subsampling_factor_in, deltapix=1.)
        try:
            import skimage
            full_psf_model = skimage.transform.rescale(full_psf_model,
                                                       scale=subsampling_factor_out / subsampling_factor_in, order=1)
            full_psf_model /= np.sum(full_psf_model)
        except ImportError:
            raise ImportError("You need to have scikit-image installed to use the interpolation feature.")

    npsf, _ = np.shape(full_psf_model)
    x, y = make_grid(numPix=npsf, deltapix=1.)
    sigma = fwhm2sigma(2)
    shift_gaussian = 0.

    gaus_kernel = gaussian_function(
        x=x, y=y,
        amp=1, sigma_x=sigma,
        sigma_y=sigma,
        center_x=shift_gaussian,
        center_y=shift_gaussian,
    ).reshape(npsf, npsf)

    if mode == 'fourier_division':
        narrow_psf = fourier_division(full_psf_model, gaus_kernel)
    else:
        raise NotImplementedError(f"Mode {mode} not implemented. Choose 'fourier_division'.")

    if subsampling_factor_in > subsampling_factor_out:
        warnings.warn('Are you sure you want to degrade your narrow PSF model?')
        if subsampling_factor_in / subsampling_factor_out % 1 != 0:
            raise ValueError("The ratio of the subsampling factors is not an integer. This is not supported.")
        try:
            import skimage
            narrow_psf = skimage.transform.rescale(narrow_psf, scale=subsampling_factor_out / subsampling_factor_in,
                                                   order=2)
            narrow_psf /= np.sum(narrow_psf)
        except ImportError:
            raise ImportError("You need to have scikit-image installed to use the interpolation feature.")

    return narrow_psf
