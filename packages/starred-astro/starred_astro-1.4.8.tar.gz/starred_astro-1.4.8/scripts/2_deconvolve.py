import argparse
import glob
import numpy as np
import json
import os
import warnings
import matplotlib.pyplot as plt

from copy import deepcopy
from astropy.io import fits

from starred.deconvolution.deconvolution import setup_model
from starred.procedures.deconvolution_routines import multi_steps_deconvolution
from starred.plots import plot_function as pltf
from starred.deconvolution.parameters import ParametersDeconv
from starred.utils.generic_utils import convert_numpy_array_to_list
from starred.deconvolution.loss import Prior


args = None
parser = argparse.ArgumentParser(description='Deconvolution Options')
parser.add_argument('--subsampling-factor', dest='subsampling_factor', type=int, default=2,
                    help='The subsampling factor.')
parser.add_argument('--niter', dest='n_iter', type=int,
                    default=500, help='Number of iterations')
parser.add_argument('--init-learning-rate', dest='lr_init', type=float,
                    default=5e-2, help='Initial learning rate for second optimization round (AdaBelief optimizer).')
parser.add_argument('--lambda-scales', dest='lambda_scales', type=float,
                    default=1, help='Low and medium frequencies regularization parameter.')
parser.add_argument('--lambda-hf', dest='lambda_hf', type=float,
                    default=1, help='High frequency regularization parameter.')
parser.add_argument('--noise-map', dest='noise_map_provided', action='store_true',
                    default=False, help='True if noise map is being provided.')
parser.add_argument('--point-sources', dest='point_sources', type=int,
                    help='Number of point sources present in the data.')
parser.add_argument('--cx', nargs='+', default=[], help='Horizontal positions of the point sources')
parser.add_argument('--cy', nargs='+', default=[], help='Vertical positions of the point sources')
parser.add_argument('--a', dest='a', nargs='+', default=None,
                    help='Initial amplitude of the point sources. Default: 0.')
parser.add_argument('--adjust_sky', dest='adjust_sky', action='store_true', default=False,
                    help='Fit a constant at each epoch to model the sky level.')
parser.add_argument('--plot-interactive', dest='plot_interactive', action='store_true', default=False,
                    help='Display plot if True')
parser.add_argument('--astrometric-prior', dest='astrometric_prior', type=float, default=None,
                    help='1 sigma with of teh Gaussian prior on point source position (in pixel).')
parser.add_argument('--two-steps', dest='two_steps', action='store_true', default=False,
                    help='Run a two steps deconvolution: first fixing the astrometry of the point source, and then releasing everything.')
parser.add_argument('--data-path', dest='data_path', type=str, default='./', help='Folder path to the data.')
parser.add_argument('--noise-map-path', dest='noise_map_path', type=str, default='./',
                    help='Folder path to the noise maps.')
parser.add_argument('--psf-path', dest='psf_path', type=str, default='./', help='Folder path to the narrow psfs.')
parser.add_argument('--output-path', dest='output_path', type=str, default='./',
                    help='Folder path to save the outputs.')
parser.add_argument('--output-format', dest='output_format', type=str, default='fits',
                    help='Prefered format to save the outputs (fits or npy). Default: fits')
parser.add_argument('--save-output-level', dest='save_output_level', type=int, default=4,
                    help='Level of output to save. 1:just the output parameters and the figures, 2-add the input data, '
                         '3- add the output products (background, narrow PSF, full PSF) 4- add the output products for every image. Default:4.')


arguments = parser.parse_args()

def main(args):

    # Parameters
    subsampling_factor = args.subsampling_factor
    M = args.point_sources
    lambda_scales = args.lambda_scales
    lambda_hf = args.lambda_hf
    convolution_method = 'scipy'

    # Create outputpath if it does not exist:
    os.makedirs(args.output_path, exist_ok=True)

    if M != 0:
        assert len(
            args.cx) == M, "Please provide --cx arguments (initial x position of point sources) that have the same size as the number of point sources!"
        assert len(
            args.cy) == M, "Please provide --cy arguments (initial y position of point sources) that have the same size as the number of point sources!"

    # Retrieving data
    file_paths_npy = sorted(glob.glob(os.path.join(args.data_path, '*.npy')))
    file_paths_fits = sorted(glob.glob(os.path.join(args.data_path, '*.fits')))
    data = np.array([np.load(f) for f in file_paths_npy])
    if len(data) == 0:
        data = np.array([fits.open(f)[0].data for f in file_paths_fits])
    else:
        if len(file_paths_fits) > 0:
            data += np.array([fits.open(f)[0].data for f in file_paths_fits])

    im_size = np.shape(data)[1]
    epochs = np.shape(data)[0]
    im_size_up = im_size * subsampling_factor
    
    # Noise map
    if args.noise_map_provided:
        sigma_paths_npy = sorted(glob.glob(os.path.join(args.noise_map_path, '*.npy')))
        sigma_paths_fits = sorted(glob.glob(os.path.join(args.noise_map_path, '*.fits')))
        sigma_2 = np.array([np.load(f) for f in sigma_paths_npy]) ** 2
        if len(sigma_2) == 0:
            sigma_2 = np.array([fits.open(f)[0].data for f in sigma_paths_fits])
        else:
            if len(file_paths_fits) > 0:
                sigma_2 += np.array([fits.open(f)[0].data for f in sigma_paths_fits])
    else:
        print('Computing noise maps from the data...')
        warnings.warn("Make sure that your data are in electrons!")
        sigma_2 = np.zeros((epochs, im_size, im_size))
        sigma_sky_2 = np.array([np.std(data[i,int(0.9*im_size):,int(0.9*im_size):]) for i in range(epochs)]) ** 2
        for i in range(epochs):
            sigma_2[i, :, :] = sigma_sky_2[i] + data[i, :, :].clip(min=0)

    # Retrieving the PSF
    file_psf_paths_npy = sorted(glob.glob(os.path.join(args.psf_path, '*.npy')))
    file_psf_paths_fits = sorted(glob.glob(os.path.join(args.psf_path, '*.fits')))
    s = np.array([np.load(f) for f in file_psf_paths_npy])
    if len(s) == 0:
        s = np.array([fits.open(f)[0].data for f in file_psf_paths_fits])
    else:
        if len(file_psf_paths_fits) > 0:
            s += np.array([fits.open(f)[0].data for f in file_psf_paths_fits])

    assert np.shape(sigma_2) == np.shape(
        data), f"Error: Data vector has shape {np.shape(data)}, whereas noise maps vector has shape {np.shape(sigma_2)}."
    assert epochs == np.shape(s)[
        0], f"Error: Data vector has {epochs} epochs, whereas I found {np.shape(s)[0]} PSF files. You should provide one PSF per epoch."

    # Renormalise your data and the noise maps by the max of the first image. Works better when using adabelief
    norm = data[0].max() / 100.
    data /= norm
    sigma_2 /= norm ** 2

    # Parameter initialization
    initial_c_x = np.array(args.cx, dtype=float)
    initial_c_y = np.array(args.cy, dtype=float)
    if args.a is None:
        initial_a = np.zeros(epochs * M)
    else:
        initial_a = np.array(args.a * epochs, dtype=float)
    model, kwargs_init, kwargs_up, kwargs_down, kwargs_fixed = setup_model(data,
                                                                           sigma_2,
                                                                           s,
                                                                           initial_c_x,
                                                                           initial_c_y,
                                                                           subsampling_factor,
                                                                           initial_a=initial_a)
    parameters = ParametersDeconv(kwargs_init,
                                  kwargs_fixed,
                                  kwargs_up=kwargs_up,
                                  kwargs_down=kwargs_down)

    # Display initial condition:
    fig = pltf.plot_deconvolution(model, data, sigma_2, s, kwargs_init, epoch=1, units=None, figsize=(15, 10))
    fig.suptitle('Initial conditions', fontsize=16)
    if args.plot_interactive:
        plt.show()
    fig.savefig(os.path.join(args.output_path, 'initial_conditions.pdf'))

    # defining fitting sequence
    kwargs_optax = {
        'max_iterations': args.n_iter, 'min_iterations': None,
        'init_learning_rate': args.lr_init, 'schedule_learning_rate': True,
        'restart_from_init': False, 'stop_at_loss_increase': False,
        'progress_bar': True, 'return_param_history': True
    }
    if args.astrometric_prior is None:
        prior_astrom = None
    else:
        prior_astrom = Prior(
            prior_analytic=[['c_x', initial_c_x, args.astrometric_prior], ['c_y', initial_c_y, args.astrometric_prior]],
            prior_background=None)

    if args.two_steps:
        fitting_sequence = [
            ['pts-source-astrometry'],
            [],
        ]
        optim_list = ['adabelief', 'adabelief']
        kwargs_optim_list = [kwargs_optax, kwargs_optax]
        prior_list = [prior_astrom, prior_astrom]
    else:
        fitting_sequence = [
            [],
        ]
        optim_list = ['adabelief']
        kwargs_optim_list = [kwargs_optax]
        prior_list = [prior_astrom]

    # Running the deconvolution
    model, parameters, loss, kwargs_partial_list, fig_list, LogL_list, loss_history_list = multi_steps_deconvolution(
        data, model, parameters, sigma_2, s, subsampling_factor,
        fitting_sequence=fitting_sequence,
        optim_list=optim_list, kwargs_optim_list=kwargs_optim_list,
        lambda_scales=lambda_scales, lambda_hf=lambda_hf, lambda_positivity_bkg=0.,
        lambda_pts_source=0., lambda_positivity_ps=100., regularization_terms='l1_starlet',
        prior_list=prior_list, regularize_full_model=False,
        adjust_sky=args.adjust_sky,
        noise_propagation='MC', verbose=True)


    kwargs_final = deepcopy(parameters.best_fit_values(as_kwargs=True))
    best_fit = parameters.kwargs2args(kwargs_final)
    chi2 = -2 * loss._log_likelihood_chi2(kwargs_final) / (im_size ** 2)
    Logl_regul = loss._log_regul(kwargs_final)
    Logl = loss._log_likelihood(kwargs_final)

    print()
    print("=== Final Results ===")
    print('Final parameters :', kwargs_final)
    print('Chi2 :', chi2)
    print('Loss : ', loss.loss(best_fit))
    print('Log Likelihood :', Logl)
    print('Log Regul:', Logl_regul)
    print('Log Regul positivity :', loss._log_regul_positivity(kwargs_final))

    with open(os.path.join(args.output_path, 'results.txt'), 'w') as f:
        f.write("=== Final Results === \n")
        f.write(f'Norm : {norm} \n')
        f.write(f'Chi2 : {chi2} \n')
        f.write(f'Loss : {loss.loss(best_fit)} \n')
        f.write(f'Log Likelihood : {Logl} \n')
        f.write(f'Log Regul: {Logl_regul} \n')
        f.write(f'Log Regul positivity {loss._log_regul_positivity(kwargs_final)} \n')

    # Saving
    for i in range(len(loss_history_list)):
        fig = pltf.plot_loss(loss_history=loss_history_list[i], title='Step %i' % (i + 1))
        fig.savefig(os.path.join(args.output_path, 'loss_step%i.pdf' % (i + 1)))
        fig_list[i].savefig(os.path.join(args.output_path, 'deconvolution_step%i.pdf' % (i + 1)))

        if args.plot_interactive:
            plt.show()

    if args.save_output_level > 3:
        model.export(args.output_path, kwargs_final, data, sigma_2, format=args.output_format, norm=norm, epoch=None)

    model.dump(os.path.join(args.output_path, 'model.hdf5'), kwargs_final, data=data, sigma_2=sigma_2,
               save_output_level=args.save_output_level, format='hdf5')
    with open(os.path.join(args.output_path, 'kwargs_final.json'), 'w') as f:
        json.dump(convert_numpy_array_to_list(kwargs_final), f)

if __name__ == '__main__':
    main(arguments)