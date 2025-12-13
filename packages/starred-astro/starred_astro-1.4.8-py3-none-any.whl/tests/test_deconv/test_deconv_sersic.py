import glob
import numpy as np
import pytest
import unittest
import os
from copy import deepcopy
import matplotlib.pyplot as plt

from tests import TEST_PATH, OUT_PATH
from starred.deconvolution.deconvolution import setup_model
from starred.deconvolution.loss import Loss
from starred.deconvolution.parameters import ParametersDeconv
from starred.plots.plot_function import view_deconv_model
from starred.optim.optimization import Optimizer

from astropy.io import fits
import pickle as pkl


class TestSersicDeconv(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(TEST_PATH, 'data', 'lensed_quasar')
        self.outpath = OUT_PATH

        file_paths = sorted(glob.glob(os.path.join(self.data_path, 'lens*.fits')))
        self.data = np.array([fits.open(f)[0].data for f in file_paths])

        self.im_size = np.shape(self.data)[1]
        self.epochs = np.shape(self.data)[0]

        # Noise map
        file_paths = sorted(glob.glob(os.path.join(self.data_path, 'sigma*.fits')))
        self.sigma_2 = np.array([fits.open(f)[0].data for f in file_paths]) ** 2

        # PSF
        file_paths = sorted(glob.glob(os.path.join(self.data_path, 'narrow_PSF*.fits')))
        self.s = np.array([fits.open(f)[0].data for f in file_paths])

    def test_deconv_sersic(self):
        subsampling_factor = 2  # the upsampling we used to represent the PSF
        convolution_method = 'scipy'

        with open(os.path.join(self.data_path, 'info_exp0.pkl'), 'rb') as f:
            source_amp, amps, mag, mag_lensed, lcs, SNR, shift_vecx, shift_vecy, ps_ra, ps_dec = pkl.load(f)

        pixel_size = 0.21
        initial_c_x = ps_ra / pixel_size - 0.5
        initial_c_y = ps_dec / pixel_size
        M = len(initial_c_x)
        initial_a = 1000 * np.array([self.data[i, :, :].max() for i in range(self.epochs) for j in range(M)])
        # provide a normalization for the image, makes things numerically more tractable:
        scale = self.data.max()
        initial_a /= scale
        model, kwargs_init, kwargs_up, kwargs_down, kwargs_fixed = setup_model(self.data, self.sigma_2, self.s,
                                                                               initial_c_x,
                                                                               initial_c_y, subsampling_factor,
                                                                               initial_a=initial_a, astrometric_bound=5,
                                                                               dithering_bound=10,
                                                                               convolution_method='fft', N_sersic=1.)

        kwargs_init['kwargs_sersic']['amp'] = [4.]
        kwargs_init['kwargs_sersic']['n_sersic'] = [1.3]
        kwargs_init['kwargs_sersic']['R_sersic'] = [11.]
        kwargs_init['kwargs_sersic']['center_x'] = [0.7]
        kwargs_init['kwargs_sersic']['center_y'] = [0.7]
        kwargs_init['kwargs_sersic']['e1'] = [0.1]
        kwargs_init['kwargs_sersic']['e2'] = [-0.1]

        kwargs_fixed['kwargs_background']['h'] = kwargs_init['kwargs_background']['h']

        parameters = ParametersDeconv(kwargs_init,
                                      kwargs_fixed,
                                      kwargs_up=kwargs_up,
                                      kwargs_down=kwargs_down)

        loss = Loss(self.data, model, parameters, self.sigma_2,
                    regularization_terms='l1_starlet',
                    regularization_strength_scales=0,
                    regularization_strength_hf=0,
                    regularization_strength_positivity=0,  # here we add a penalty if negative background,
                    regularization_strength_pts_source=0)

        optim = Optimizer(loss, parameters, method='l-bfgs-b')
        best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(maxiter=100)

        kwargs_partial = deepcopy(parameters.best_fit_values(as_kwargs=True))

        chi2 = loss.reduced_chi2(kwargs_partial)
        assert chi2 < 1.01


if __name__ == '__main__':
    pytest.main()
