import numpy as np
from copy import deepcopy
from starred.psf.parameters import ParametersPSF
from starred.deconvolution.parameters import Parameters
from starred.psf.psf import PSF
from numpy.testing import assert_array_equal
import jax.numpy as jnp
from starred.plots import plot_function as pltf
import glob
import unittest
import os

from tests import TEST_PATH

import jax

jax.config.update("jax_enable_x64", True)  # we require double digit precision


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.path = TEST_PATH
        self.datapath = os.path.join(self.path, "data")
        self.data = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.datapath, 'star_*.npy')))])
        self.plot = False

        self.N = len(self.data)  # number of stars
        self.image_size = np.shape(self.data)[1]  # data dimensions

        # Noise map estimation
        self.sigma_2 = np.zeros((self.N, self.image_size, self.image_size))
        sigma_sky_2 = np.array(
            [np.std(self.data[i, int(0.9 * self.image_size):, int(0.9 * self.image_size):]) for i in range(self.N)]) ** 2
        for i in range(self.N):
            self.sigma_2[i, :, :] = sigma_sky_2[i] + self.data[i, :, :].clip(min=0)

        # Renormalise your data and the noise maps by the max of the first image. Works better when using adabelief
        self.norm = self.data[0].max() / 100.
        self.data /= self.norm
        self.sigma_2 /= self.norm ** 2

    def test_param_PSF(self):
        model = PSF(image_size=self.image_size, number_of_sources=self.N,
                    upsampling_factor=2,
                    convolution_method='scipy',
                    include_moffat=True, elliptical_moffat=True)

        kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = model.smart_guess(self.data, fixed_background=True)

        index = [0, 1, -1]  # leave free the parameters in this list
        custom_background = np.zeros((self.image_size*2)**2)
        custom_background[index] = np.nan

        kwargs_fixed_test = {
            'kwargs_moffat': {},
            'kwargs_gaussian': {},
            'kwargs_background': {'background': jnp.array(custom_background)},
            'kwargs_distortion': {'dilation_x': np.zeros(5), 'dilation_y': np.zeros(5), 'shear': np.zeros(5)}
        }
        parameters_test = ParametersPSF(kwargs_init, kwargs_fixed_test, kwargs_up, kwargs_down)
        args = parameters_test.kwargs2args(kwargs_init)
        assert len(args) == 20

        kwargs = parameters_test.args2kwargs(args)
        assert_array_equal(kwargs['kwargs_background']['background'], jnp.zeros((self.image_size*2)**2))
        assert_array_equal(kwargs['kwargs_background']['mean'], jnp.zeros(self.N))

        param_names = parameters_test.get_all_free_param_names(kwargs)

        kwargs_fixed_test2 = {
            'kwargs_moffat': {},
            'kwargs_gaussian': {'a': jnp.array([1., np.nan, 1.])},
            'kwargs_background': {'background': jnp.array(custom_background), 'mean': jnp.zeros(self.N)},
            'kwargs_distortion': {'dilation_x': np.zeros(5), 'dilation_y': np.zeros(5), 'shear': np.zeros(5)}
        }

        parameters_test2 = ParametersPSF(kwargs_init, kwargs_fixed_test2, None, None)
        args = parameters_test2.kwargs2args(kwargs_init)
        assert len(args) == 15




