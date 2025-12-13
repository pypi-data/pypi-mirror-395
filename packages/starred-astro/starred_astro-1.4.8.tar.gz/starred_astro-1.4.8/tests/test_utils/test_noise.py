import numpy as np
import glob
from numpy.testing import assert_allclose
import os
import pytest
import unittest
import matplotlib.pyplot as plt

from starred.utils.noise_utils import propagate_noise, dirac_impulse
from starred.psf.psf import PSF

from tests import TEST_PATH

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.path = TEST_PATH
        self.datapath = os.path.join(self.path, "data")
        self.noisepath = os.path.join(self.path, "noise_map")
        self.data = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.datapath, 'star**.npy')))])
        self.masks = np.ones_like(self.data)
        self.N, self.image_size, _ = np.shape(self.data)

        self.norm = self.data[0].max() / 100.
        self.sigma_2 = np.zeros((self.N, self.image_size, self.image_size))
        sigma_sky_2 = np.array([np.std(self.data[i,int(0.9*self.image_size):,int(0.9*self.image_size):]) for i in range(self.N)]) ** 2
        for i in range(self.N):
            self.sigma_2[i,:,:] = sigma_sky_2[i] + self.data[i,:,:].clip(min=0)

        self.sigma_2 /= self.norm ** 2
        self.data /= self.norm
        self.subsampling_factor = 2

        self.kwargs_partial = {
            'kwargs_moffat': {'fwhm': np.array([3.54344314]), 'beta': np.array([2.10782421]), 'C': np.array([115.30484381])},
            'kwargs_gaussian': {'a': np.array([-0.48029483, -0.55883527, -0.33968393]), 'x0': np.array([-0.26200011,  0.52001915,  0.31850829]), 'y0': np.array([-0.03379763, -0.12634879,  0.06106638])},
            'kwargs_background': {'background': np.array([0. for i in range((self.image_size*self.subsampling_factor)**2)])}
        }

        self.model =PSF(image_size=self.image_size, number_of_sources=self.N,
                    upsampling_factor=self.subsampling_factor,
                    convolution_method='fft',
                    include_moffat=True)

        self.plot = False

    def test_noise_mc(self):
        W = propagate_noise(self.model, np.sqrt(self.sigma_2), self.kwargs_partial, wavelet_type_list=['starlet'], method='MC',
                            num_samples=500, seed=1, likelihood_type='chi2', verbose=False, upsampling_factor=self.subsampling_factor,
                            scaling_noise_ref=0)[0]

        mean = np.mean(W, axis=(1,2))
        mean_desired = [1.910464, 1.493248, 0.85761, 0.440049, 0.214746, 0.1011, 0.044608, 0.019781]

        if self.plot :
            gix, axs = plt.subplots(1, len(W), figsize=(12, 4))
            for i, l in enumerate(W):
                axs[i].imshow(l)
                print(np.mean(l))
            plt.show()

        assert_allclose(mean_desired, mean, atol=5e-2)

        #Reproduce the test, with now the mean of all noise maps as a reference
        W2 = propagate_noise(self.model, np.sqrt(self.sigma_2), self.kwargs_partial, wavelet_type_list=['starlet'], method='MC',
                            num_samples=500, seed=1, likelihood_type='chi2', verbose=False, upsampling_factor=self.subsampling_factor,
                            scaling_noise_ref=None)[0]
        mean2 = np.mean(W2, axis=(1, 2))

        mean_desired2 = [1.7293704, 1.3517164, 0.7763171, 0.39824945, 0.19427973, 0.09151274, 0.04038997, 0.01793539]
        assert_allclose(mean_desired2, mean2, atol=5e-2)

        dirac = dirac_impulse(self.image_size)
        assert np.sum(dirac) == 1

    def test_noise_slit(self):
        W = propagate_noise(self.model, np.sqrt(self.sigma_2), self.kwargs_partial, masks=self.masks, wavelet_type_list=['starlet'], method='SLIT',
                            num_samples=500, seed=1, likelihood_type='chi2', verbose=False, upsampling_factor=self.subsampling_factor,
                            scaling_noise_ref=0)[0]
        mean = np.mean(W, axis=(1, 2))
        mean_desired = [3.286233, 0.74144, 0.314976, 0.150678, 0.0737, 0.036023, 0.017899, 0.009112]
        assert_allclose(mean_desired, mean, atol=5e-2)

    def test_raise(self):
        with self.assertRaises(ValueError):
            W = propagate_noise(self.model, np.sqrt(self.sigma_2), self.kwargs_partial, likelihood_type='unknown')[0]

        with self.assertRaises(ValueError):
            W = propagate_noise(self.model, np.sqrt(self.sigma_2), self.kwargs_partial, method='unknown')[0]

        with self.assertRaises(TypeError):
            W = propagate_noise(np.array([1.]), np.sqrt(self.sigma_2), self.kwargs_partial)[0]

        with self.assertRaises(RuntimeError):
            masks_test = np.zeros_like(self.data)
            W = propagate_noise(self.model, np.sqrt(self.sigma_2), self.kwargs_partial, masks=masks_test, scaling_noise_ref=0)[0]
