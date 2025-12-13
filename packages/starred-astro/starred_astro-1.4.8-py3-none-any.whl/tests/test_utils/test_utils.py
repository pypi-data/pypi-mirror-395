import numpy as np
import jax.numpy as jnp
import scipy
import glob
from numpy.testing import assert_allclose
import os
import copy
import pytest
import unittest
import matplotlib.pyplot as plt

from starred.utils.generic_utils import Downsample, Upsample, timer_func, make_grid, twoD_Gaussian, \
    pad_and_convolve_fft, gaussian_function, pad_and_convolve,scipy_convolve

from tests import TEST_PATH

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.path = TEST_PATH
        self.datapath = os.path.join(self.path, "data")
        self.data = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.datapath, '*200w_psfg.npy')))])
        self.plot = False

    @timer_func
    def test_upsample_downsample(self):
        data_up = Upsample(copy.deepcopy(self.data[0]), factor=2)
        data_down = Downsample(data_up, factor=2, conserve_flux=True)

        assert_allclose(self.data[0], data_down, rtol=1e-3)

        data_equal = Upsample(copy.deepcopy(self.data[0]), factor=1)

        assert_allclose(self.data[0], data_equal, rtol=1e-3)

    def test_convolution_kernel(self):
        image_sizes = [32,33]
        for nx in image_sizes:
            if nx % 2 == 1:
                dx = 0
            else :
                dx = 1
            x, y = make_grid(numPix=nx, deltapix=1.)
            sigmax_k, sigmay_k = 2., 4.
            sigmax, sigmay = 4., 2.
            shift_x, shift_y = 0., 0. #Warning scipy and lax have different convention for uncentered kernels !
            shift_datax, shift_datay = 2., 0.

            kernel = np.array(twoD_Gaussian(x, y, 1, 0, 0, sigmax_k, sigmay_k, 0.4)).reshape(nx, nx)
            kernel = kernel / np.sum(kernel)
            kernel[kernel < 0] = 1e-6
            kernel = kernel / np.sum(kernel)

            kernel = jnp.array(kernel)
            kernel = scipy.ndimage.shift(kernel, (shift_x, shift_y), output=None, order=3, mode='nearest')
            # match scipy convention for the centering of the kernel (bottom left central pixels, instead of top right for lax)
            # This only matters for even kernel size.
            kernel_scipy = scipy.ndimage.shift(kernel, (shift_x-dx, shift_y-dx), output=None, order=1, mode='nearest')

            x, y = make_grid(numPix=nx, deltapix=1.)
            data = jnp.array(gaussian_function(x=x, y=y,
                                                          amp=1, sigma_x=sigmax, sigma_y=sigmay,
                                                          center_x=0. - shift_datay,
                                                          center_y=0. - shift_datax)).reshape(nx, nx)

            data_scipy = jnp.array(gaussian_function(x=x, y=y,
                                                          amp=1, sigma_x=sigmax, sigma_y=sigmay,
                                                          center_x=0. + shift_datay,
                                                          center_y=0. + shift_datax)).reshape(nx, nx) #Scipy has opposite shifting convention

            data = jnp.array(data) / data.sum()

            convolve_fft = pad_and_convolve_fft(kernel, data, padding=True)
            convolve_fft_nopadding = pad_and_convolve_fft(kernel, data, padding=False)
            convolve_lax = pad_and_convolve(kernel, data, padding=True).reshape(nx, nx)
            convolve_lax_nopadding = pad_and_convolve(kernel, data, padding=False).reshape(nx, nx)
            convolve_scipy = scipy_convolve(kernel_scipy, data_scipy)

            assert_allclose(convolve_fft, convolve_lax, atol=1e-5)
            assert_allclose(convolve_fft, convolve_scipy, atol=1e-5)
            assert_allclose(convolve_scipy, convolve_fft_nopadding, atol=3e-5)
            assert_allclose(convolve_scipy, convolve_lax_nopadding, atol=3e-5)

            if self.plot:
                plt.figure()
                plt.title('Kernel')
                plt.imshow(kernel, origin='lower')
                plt.colorbar()
                plt.figure()
                plt.title('Data')
                plt.imshow(data, origin='lower')
                plt.colorbar()
                plt.figure()
                plt.title('FFT')
                plt.imshow(convolve_fft, origin='lower')
                plt.colorbar()
                plt.figure()
                plt.title('LAX')
                plt.imshow(convolve_lax, origin='lower')
                plt.colorbar()
                plt.figure()
                plt.title('Scipy')
                plt.imshow(convolve_scipy, origin='lower')
                plt.colorbar()

                plt.figure()
                plt.title('FFT - LAX')
                plt.imshow(convolve_fft - convolve_lax, origin='lower')
                plt.colorbar()
                plt.figure()
                plt.title('FFT - scipy')
                plt.imshow(convolve_fft - convolve_scipy, origin='lower')
                plt.colorbar()
                plt.figure()
                plt.title('LAX- scipy')
                plt.imshow(convolve_lax - convolve_scipy, origin='lower')
                plt.colorbar()
                plt.show()

    def test_raise(self):
        with self.assertRaises(ValueError):
            Downsample(copy.deepcopy(self.data[0]), factor=0.5)

        with self.assertRaises(ValueError):
            Downsample(copy.deepcopy(self.data[0]), factor=3)

        with self.assertRaises(ValueError):
            Upsample(copy.deepcopy(self.data[0]), factor=0.5)

