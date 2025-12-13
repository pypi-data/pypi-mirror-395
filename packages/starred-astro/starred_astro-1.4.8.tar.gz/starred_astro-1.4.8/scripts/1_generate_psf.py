import argparse
import warnings
import glob
import numpy as np
import os
import matplotlib.pyplot as plt
from astropy.io import fits
import pyregion
from copy import deepcopy

from starred.psf.psf import PSF
from starred.psf.parameters import ParametersPSF
from starred.procedures.psf_routines import run_multi_steps_PSF_reconstruction
from starred.plots import plot_function as ptf
import jax

args = None
parser = argparse.ArgumentParser(description='NarrowPSFGen Options')
parser.add_argument('--subsampling-factor', dest='subsampling_factor', type=int,
                    default=2, help='The subsampling factor.')
parser.add_argument('--optim-analytical', dest='optim_analytical', type=str,
                    default="l-bfgs-b",
                    help='Optimiser for the Moffat fit. Default: "l-bfgs-b". Try "Newton-CG" if the Moffat fit fails.')
parser.add_argument('--niter', dest='n_iter', type=int,
                    default=300, help='Number of iterations for adabelief')
parser.add_argument('--init-learning-rate', dest='lr_init', type=float,
                    default=1e-2, help='Initial learning rate for second optimization round (AdaBelief optimizer).')
parser.add_argument('--lambda-scales', dest='lambda_scales', type=float,
                    default=3, help='Low and medium frequencies regularization parameter.')
parser.add_argument('--lambda-hf', dest='lambda_hf', type=float,
                    default=3, help='High frequency regularization parameter.')
parser.add_argument('--lambda-pos', dest='lambda_pos', type=float,
                    default=0.0, help='Positivity constraint. 0 do not impose positivity.')
parser.add_argument('--auto-noise', dest='auto_noise', action='store_true',
                    default=False,
                    help='Use this option to compute the noise directly from the data. Your data must be in e- and not ADU or e-/s.'
                         'Other option is to provide the noise map directly.')
parser.add_argument('--data-path', dest='data_path', type=str, default='./', help='Path to the data (str).')
parser.add_argument('--noise-map-path', dest='noise_map_path', type=str, default='./',
                    help='Path to the noise maps (str).')
parser.add_argument('--use-masks', dest='use_mask', action='store_true', default=False,
                    help='Add mask to the cutouts. Mask should be in the NOISE_MAP_PATH/mask_i.reg')
parser.add_argument('--output-path', dest='output_path', type=str, default='./output_starred_PSF',
                    help='Path to save the output files and plots (str).')
parser.add_argument('--plot-interactive', dest='plot_interactive', action='store_true', default=False,
                    help='Display plot if True')
parser.add_argument('--regularize-full-psf', dest='regularize_full_psf', action='store_true', default=False,
                    help='Regularize the full psf (Moffat+background) if True')
parser.add_argument('--unfix-moffat-final-step', dest='unfix_moffat_final_step', action='store_true', default=False,
                    help='Whether or not to fix Moffat parameters when fitting for the background component.')
parser.add_argument('--method-noise', dest='method_noise', type=str, default='MC',
                    help='Method to propagate noise. "SLIT" or "MC".')
parser.add_argument('--guess-method', dest='guess_method', type=str, default='barycenter',
                    help='Method to estimate the star position. "barycenter", "max" or "center". Default:"barycenter".')
parser.add_argument('--save-output-level', dest='save_output_level', type=int, default=4,
                    help='Level of output to save. 1:just the output parameters and the figures, 2-add the input data, '
                         '3- add the output products (background, narrow PSF, full PSF) 4- add the output products for every image. Default:4.')
parser.add_argument('--float64', dest='fl64', action='store_true', default=False,
                    help='Activate float64 computation on GPU. Recommended on CPU.')

arguments = parser.parse_args()
if arguments.fl64:
    print('Enabling float64 computations.')
    jax.config.update("jax_enable_x64", True)

def main(args):
    # Parameters
    subsampling_factor = args.subsampling_factor
    n_iter = args.n_iter
    lr_init_final = args.lr_init
    lambda_scales = args.lambda_scales
    lambda_hf = args.lambda_hf
    lambda_positivity = args.lambda_pos
    optim_analytical = args.optim_analytical
    method_noise = args.method_noise

    # Create outputpath if it does not exist:
    os.makedirs(args.output_path, exist_ok=True)

    # Optimiser settings:
    kwargs_analytical = {'maxiter': 1000}
    kwargs_optax = {'max_iterations': n_iter, 'min_iterations': None,
                    'init_learning_rate': lr_init_final, 'schedule_learning_rate': True,
                    'restart_from_init': False, 'stop_at_loss_increase': False,
                    'progress_bar': True, 'return_param_history': True}

    if args.unfix_moffat_final_step:
        fitting_sequence = [['background'], []]
    else:
        fitting_sequence = [['background'], ['moffat']]
    kwargs_optim_list = [kwargs_analytical, kwargs_optax]
    optim_list = [optim_analytical, 'adabelief']


    # Data
    file_paths_npy = sorted(glob.glob(os.path.join(args.data_path, '*.npy')))
    file_paths_fits = sorted(glob.glob(os.path.join(args.data_path, '*.fits')))
    new_vignets_data = np.array([np.load(f) for f in file_paths_npy])
    if len(new_vignets_data) == 0:
        new_vignets_data = np.array([fits.open(f)[0].data for f in file_paths_fits])
    else:
        if len(file_paths_fits) > 0:
            new_vignets_data += np.array([fits.open(f)[0].data for f in file_paths_fits])

    N = len(file_paths_npy) + len(file_paths_fits)  # number of stars
    if N > 0:
        print('Running joined fit on %i images...' % N)
    else:
        raise RuntimeError('No .fits or .npy files found. Search directory: %s.' % args.data_path)

    image_size = np.shape(new_vignets_data)[1]  # data dimensions

    # Masking
    if args.use_mask:
        masks = np.ones((N, image_size, image_size))
        for i in range(N):
            possiblemaskfilepath = os.path.join(args.noise_map_path, 'mask_%s.reg' % str(i))
            if os.path.exists(possiblemaskfilepath):
                r = pyregion.open(possiblemaskfilepath)
                masks[i, :, :] = 1 - r.get_mask(shape=(image_size, image_size)).astype(float)
    else:
        masks = None

    # Noise map
    if not args.auto_noise:
        sigma_paths_npy = sorted(glob.glob(os.path.join(args.noise_map_path, '*.npy')))
        sigma_paths_fits = sorted(glob.glob(os.path.join(args.noise_map_path, '*.fits')))
        sigma_2 = np.array([np.load(f) for f in sigma_paths_npy]) ** 2
        if len(sigma_2) == 0:
            sigma_2 = np.array([fits.open(f)[0].data for f in sigma_paths_fits]) ** 2
        else:
            if len(sigma_paths_fits) > 0:
                sigma_2 += np.array([fits.open(f)[0].data for f in sigma_paths_fits]) ** 2

        if len(sigma_2) == N:
            print('Found %i noise maps...' % len(sigma_2))
        else:
            raise RuntimeError(
                'Noise maps not found. Provide noise map or use "--auto-noise" if you are sure that your '
                'data are in electrons.')
    else:
        print('Computing noise maps from the data...')
        warnings.warn("Make sure that your data are in electrons!")
        sigma_2 = np.zeros((N, image_size, image_size))
        sigma_sky_2 = np.array(
            [np.std(new_vignets_data[i, int(0.9 * image_size):, int(0.9 * image_size):]) for i in range(N)]) ** 2
        for i in range(N):
            sigma_2[i, :, :] = sigma_sky_2[i] + new_vignets_data[i, :, :].clip(min=0)

    # Renormalise your data and the noise maps by the max of the first image. Works better when using adabelief
    norm = new_vignets_data[0].max() / 100.
    new_vignets_data /= norm
    sigma_2 /= norm ** 2

    # Calling the PSF model
    model = PSF(image_size=image_size, number_of_sources=N,
                upsampling_factor=subsampling_factor,
                convolution_method='scipy')

    # Parameter initialization
    kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = model.smart_guess(new_vignets_data, fixed_background=False,
                                                                          guess_method=args.guess_method)
    print('Initial guess :', kwargs_init)
    if args.plot_interactive:
        fig = ptf.display_data(new_vignets_data, sigma_2=sigma_2, figsize=(15, 10),
                               center=(kwargs_init['kwargs_gaussian']['x0'], kwargs_init['kwargs_gaussian']['y0']))
        fig.suptitle('Data and initial centering position for each star', fontsize=14)
        plt.show()

    parameters = ParametersPSF(kwargs_init, kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down)

    model, parameters, loss, kwargs_partial_list, LogL_list, loss_history_list = run_multi_steps_PSF_reconstruction(
        new_vignets_data, model,
        parameters, sigma_2, masks=masks,
        lambda_scales=lambda_scales, lambda_hf=lambda_hf,
        lambda_positivity=lambda_positivity,
        fitting_sequence=fitting_sequence,
        optim_list=optim_list,
        kwargs_optim_list=kwargs_optim_list,
        method_noise=method_noise, regularize_full_psf=False,
        verbose=True)


    #plotting figures
    for i, kwargs_partial in enumerate(kwargs_partial_list):
        if i == 0:
            suf = '(initial condition)'
        else:
            suf = ''
        fig1 = ptf.single_PSF_plot(model, new_vignets_data, sigma_2, kwargs_partial, n_psf=0, figsize=(15, 10))
        fig2 = ptf.multiple_PSF_plot(model, new_vignets_data, sigma_2, kwargs_partial)

        fig1.savefig(os.path.join(args.output_path, f'single_PSF_plot_partial_step{i}{suf}.png'))
        fig1.suptitle(f'Step {i} {suf}', fontsize=14)
        fig2.savefig(os.path.join(args.output_path, f'multit_PSF_plot_partial_step{i}{suf}.png'))
        fig2.suptitle(f'Step {i} {suf}', fontsize=14)

        if i > 0:
            fig3 = ptf.plot_loss(loss_history_list[i - 1])
            fig3.suptitle(f'Step {i}: fixing {fitting_sequence[i - 1]}, optimiser: {optim_list[i - 1]}', fontsize=14)
            fig3.savefig(os.path.join(args.output_path, f'Loss_history_step{i}.png'))

        if args.plot_interactive:
            plt.show()

    kwargs_final = deepcopy(kwargs_partial_list[-1])
    best_fit = parameters.kwargs2args(kwargs_final)
    chi2 = loss.reduced_chi2(kwargs_final)
    Logl = loss._log_likelihood(kwargs_final)
    Logl_regul = loss._log_regul(kwargs_final)

    print()
    print("=== Final Results ===")
    print('Parameters :', kwargs_final)
    print('Overall Reduced Chi2 : ', chi2)
    print('Loss : ', loss.loss(best_fit))
    print('Log Likelihood : ', Logl)
    print('Log Regul : ', Logl_regul)
    print()

    with open(os.path.join(args.output_path, 'results.txt'), 'w') as f:
        f.write("=== Final Results === \n")
        f.write(f'Norm : {norm} \n')
        f.write(f'Overall Reduced Chi2 : {chi2} \n')
        f.write(f'Loss : {loss.loss(best_fit)} \n')
        f.write(f'Log Likelihood : {Logl} \n')
        f.write(f'Log Regul: {Logl_regul} \n')

    # Saving
    if args.save_output_level > 3:
        model.export(args.output_path, kwargs_final, new_vignets_data, sigma_2, format='fits')

    model.dump(os.path.join(args.output_path, 'model.hdf5'), kwargs_final, norm, data=new_vignets_data, sigma_2=sigma_2,
               masks=masks, save_output_level=args.save_output_level, format='hdf5')

if __name__ == '__main__':
    # test command: python3 1_generate_psf.py --subsampling-factor 3 --niter 500 --output-path ./test --data-path ../notebooks/data/1_observations/ --plot-interactive
    main(arguments)
