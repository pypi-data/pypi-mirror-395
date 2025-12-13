import warnings

from starred.deconvolution.loss import Loss as deconvLoss
from starred.psf.loss import Loss as psfLoss
from starred.deconvolution.parameters import ParametersDeconv
from starred.utils.noise_utils import propagate_noise
from starred.optim.optimization import Optimizer
from starred.plots import plot_function as pltf
from starred.psf.parameters import ParametersPSF

from copy import deepcopy
import numpy as np


def multi_steps_deconvolution(data, model, parameters, sigma_2, s, subsampling_factor,
                              fitting_sequence=[['background'], ['pts-source-astrometry'], []],
                              optim_list=['l-bfgs-b', 'adabelief', 'adabelief'], kwargs_optim_list=None,
                              lambda_scales=1., lambda_hf=1000., lambda_positivity_bkg=100, lambda_positivity_ps=100,
                              lambda_pts_source=0., prior_list=None, regularize_full_model=False,
                              update_lambda_pts_source=False,
                              adjust_sky=False, noise_propagation='MC', regularization_terms='l1_starlet',
                              verbose=True):
    """
    A high-level function to run several time the optimization algorithms and ensure to find the optimal solution.

    :param data: 3D array containing the images, one per epoch. shape (epochs, im_size, im_size)
    :param model: Deconv class, deconvolution model
    :param parameters: ParametersDeconv class
    :param sigma_2: 3D array containing the noisemaps, one per epoch. shape (epochs, im_size, im_size)
    :param s: 3D array containing the narrow PSFs, one per epoch. shape (epochs, im_size_up, im_size_up) where im_size_up needs be a multiple of im_size.
    :param subsampling_factor: integer, ratio of the size of the data pixels to that of the PSF pixels.
    :param fitting_sequence: list, List of lists, containing the element of the model to keep fixed. Example : [['pts-source-astrometry','pts-source-photometry','background'],['pts-source-astrometry','pts-source-photometry'], ...]
    :param optim_list: List of optimiser. Recommended if background is kept constant : 'l-bfgs-b', 'adabelief' otherwise.
    :param kwargs_optim_list: List of dictionary, containing the setting for the different optimiser.
    :param lambda_scales: Lagrange parameter that weights intermediate scales in the transformed domain
    :param lambda_hf: Lagrange parameter weighting the highest frequency scale
    :param lambda_pts_source: Lagrange parameter regularising the pts source channel
    :param lambda_positivity_bkg: Lagrange parameter weighting the positivity of the background. 0 means no positivity constraint.
    :param lambda_positivity_ps: Lagrange parameter weighting the positivity of the point sources. 0 means no positivity constraint.
    :param regularize_full_model: option to regularise just the background (False, recommended) or background + point source channel (True)
    :param update_lambda_pts_source : bool, option to refine the points channel regularization strength at every iteration
    :param prior_list: list of Prior object, Gaussian prior on parameters to be applied at each step
    :param adjust_sky: bool, True if you want to fit some sky subtraction
    :param noise_propagation: 'MC' or 'SLIT', method to compute the noise propagation in wavelet space. Default: 'MC'.
    :param verbose: bool. Verbosity.

    Return model, parameters, loss, kwargs_partial_list, fig_list, LogL_list, loss_history_list
    """
    # Check the sequence
    assert len(fitting_sequence) == len(optim_list), "Fitting sequence and optimiser list have different lenght !"
    if kwargs_optim_list is not None:
        assert len(fitting_sequence) == len(
            kwargs_optim_list), "Fitting sequence and kwargs optimiser list have different lenght !"
    else:
        warnings.warn('No optimiser kwargs provided. Default configuration is used.')
        kwargs_optim_list = [{} for _ in range(len(fitting_sequence))]

    if prior_list is None:
        prior_list = [None for _ in range(len(fitting_sequence))]
    else:
        assert len(fitting_sequence) == len(prior_list), "Fitting sequence and prior list have different lenght !"

    # setup the model
    kwargs_init, kwargs_fixed_default, kwargs_up, kwargs_down = deepcopy(parameters._kwargs_init), deepcopy(
        parameters._kwargs_fixed), \
        deepcopy(parameters._kwargs_up), deepcopy(parameters._kwargs_down)
    if not adjust_sky:
        kwargs_fixed_default['kwargs_background']['mean'] = np.zeros(model.epochs)

    kwargs_partial_list = [kwargs_init]
    fig_list = []
    loss_history_list = []
    loss_list = []

    W = propagate_noise(model, np.sqrt(sigma_2), kwargs_init, wavelet_type_list=['starlet'],
                        method=noise_propagation,
                        num_samples=500, seed=1, likelihood_type='chi2', verbose=False,
                        upsampling_factor=subsampling_factor)[0]

    for i, steps in enumerate(fitting_sequence):
        kwargs_fixed = deepcopy(kwargs_fixed_default)
        background_free = True
        for fixed_feature in steps:
            if fixed_feature == 'pts-source-astrometry':
                kwargs_fixed['kwargs_analytic']['c_x'] = kwargs_partial_list[i]['kwargs_analytic']['c_x']
                kwargs_fixed['kwargs_analytic']['c_y'] = kwargs_partial_list[i]['kwargs_analytic']['c_y']
            elif fixed_feature == 'pts-source-photometry':
                kwargs_fixed['kwargs_analytic']['a'] = kwargs_partial_list[i]['kwargs_analytic']['a']
            elif fixed_feature == 'background':
                background_free = False
                kwargs_fixed['kwargs_background']['h'] = kwargs_partial_list[i]['kwargs_background']['h']
            elif fixed_feature == 'sersic':
                for k in kwargs_partial_list[i]['kwargs_sersic'].keys():
                    kwargs_fixed['kwargs_sersic'][k] = kwargs_partial_list[i]['kwargs_sersic'][k]
            elif fixed_feature == 'dithering':
                kwargs_fixed['kwargs_analytic']['dx'] = kwargs_partial_list[i]['kwargs_analytic']['dx']
                kwargs_fixed['kwargs_analytic']['dy'] = kwargs_partial_list[i]['kwargs_analytic']['dy']
            else:
                raise ValueError(
                    'Steps is not defined. Choose between "pts-source-astrometry", "pts-source-photometry", "background", "dithering" or "sersic".')

        # need to recompile the parameter class, since we have changed the number of free parameters
        parameters = ParametersDeconv(kwargs_partial_list[i], kwargs_fixed, kwargs_up=kwargs_up,
                                      kwargs_down=kwargs_down)

        # for speed-up we turn of the regularization to avoid the starlet decomposition, if the background is fixed
        if background_free:
            lambda_scales_eff, lambda_hf_eff, lambda_positivity_bkg_eff = deepcopy(lambda_scales), deepcopy(
                lambda_hf), deepcopy(lambda_positivity_bkg)
        else:
            lambda_scales_eff, lambda_hf_eff, lambda_positivity_bkg_eff = 0., 0., 0.

        # refine the regularization of the point source channel correction from previous iteration
        if i > 0 and update_lambda_pts_source and lambda_pts_source != 0:
            lambda_pts_prev = lambda_pts_source_eff
            lambda_pts_source_eff = loss.update_lambda_pts_source(kwargs_partial_list[i])
            if verbose:
                print(f'Updating lambda_pts_source from {lambda_pts_prev} to {lambda_pts_source_eff}')
        else:
            lambda_pts_source_eff = lambda_pts_source

            # run the optimization
        print('Step %i, fixing :' % (i + 1), steps)
        loss = deconvLoss(data, model, parameters, sigma_2, regularization_terms=regularization_terms,
                          regularization_strength_scales=lambda_scales_eff,
                          regularization_strength_hf=lambda_hf_eff,
                          regularization_strength_positivity=lambda_positivity_bkg_eff,
                          regularization_strength_positivity_ps=lambda_positivity_ps,
                          regularization_strength_pts_source=lambda_pts_source_eff,
                          regularize_full_model=regularize_full_model,
                          prior=prior_list[i], W=W, )

        optim = Optimizer(loss, parameters, method=optim_list[i])
        best_fit, loss_best_fit, extra_fields, runtime = optim.minimize(**kwargs_optim_list[i])

        # Saving partial results
        kwargs_partial_steps = deepcopy(parameters.best_fit_values(as_kwargs=True))
        fig_list.append(
            pltf.plot_deconvolution(model, data, sigma_2, s, kwargs_partial_steps, epoch=0, units='e-', cut_dict=None))
        loss_history_list.append(extra_fields['loss_history'])
        loss_list.append(loss_best_fit)

        kwargs_partial_list.append(deepcopy(kwargs_partial_steps))
        if verbose:
            print('Step %i/%i took %2.f seconds' % (i + 1, len(fitting_sequence), runtime))
            print('Kwargs partial at step %i/%i' % (i + 1, len(fitting_sequence)), kwargs_partial_steps)
            print('Loss : ', loss_best_fit)
            print('Overall Reduced Chi2 : ', loss.reduced_chi2(kwargs_partial_steps))

    return model, parameters, loss, kwargs_partial_list, fig_list, loss_list, loss_history_list
