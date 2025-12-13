import glob
import numpy as np
import matplotlib.pyplot as plt
import starred.plots.plot_function as pltf
import os
import pytest
import unittest

from tests import TEST_PATH
from starred.psf.psf import PSF
from starred.plots import f2n

plt.switch_backend('Agg')
class TestPlots(unittest.TestCase):
    def setUp(self):
        self.path = TEST_PATH
        self.datapath = os.path.join(self.path, "data")
        self.noisepath = os.path.join(self.path, "noise_map")
        self.data = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.datapath, '*200w_psfg.npy')))])
        self.masks = np.ones_like(self.data)
        self.masks[0, -10:, -10] = 0.

        self.norm = self.data[0].max() / 100.
        self.data /= self.norm
        self.sigma = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.noisepath, '*200w_psfg.npy')))])
        self.sigma /= self.norm ** 2

        self.N = len(self.data)

    def tearDown(self):
        plt.close('all')

    def test_f2n_plots(self):

        fig = plt.figure(figsize=(12, 12))
        f2n.spplot(i=1, array=self.data[0,:,:], fig=fig, title="Star 1")
        f2n.spplot(i=2, array=self.data[1,:,:], fig=fig, title="Star 2")
        f2n.spplot(i=3, array=self.data[2,:,:], fig=fig, title="Star 3")
        f2n.spplot(i=4, array=self.sigma[0,:,:], fig=fig, title="Noise map 1")
        f2n.spplot(i=5, array=self.sigma[1,:,:], fig=fig, title="Noise map 2")
        f2n.spplot(i=6, array=self.sigma[2,:,:], fig=fig, title="Noise map 3")
        plt.show()

    def test_plt_function(self):
        model = PSF(image_size=32, number_of_sources=3)
        initial_a = np.ones(self.N)
        initial_C = float(np.median(self.data[0], axis=0).max()) * 500
        initial_background = np.zeros((64**2))
        initial_background_mean = np.zeros(self.N)

        x0_est = np.array([0. for i in range(3)])
        y0_est = np.array([0. for i in range(3)])
        for i in range(3):
            indices = np.where(self.data[i,:,:]==self.data[i,:,:].max())
            x0_est[i] = (indices[1][0] - int(32 / 2))
            y0_est[i] = (indices[0][0] - int(32 / 2))

        kwargs = {
            'kwargs_moffat': {'fwhm': 2.0, 'beta': 5.0, 'C':initial_C},
            'kwargs_gaussian': {'a': initial_a, 'x0': x0_est, 'y0': y0_est},
            'kwargs_background': {'background': initial_background, 'mean': initial_background_mean},
            'kwargs_distortion': {'dilation_x': np.zeros(5), 'dilation_y': np.zeros(5), 'shear': np.zeros(5)}
        }

        pltf.single_PSF_plot(model, self.data, self.sigma, kwargs, n_psf=0, units='e-')
        pltf.single_PSF_plot(model, self.data, self.sigma, kwargs, n_psf=0, upsampling=2, masks=self.masks)
        pltf.multiple_PSF_plot(model, self.data, self.sigma, kwargs, units='e-')
        plt.show()

    def tests_display_data(self):
        model = PSF(image_size=32, number_of_sources=3)
        kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = model.smart_guess(self.data, fixed_background=True,
                                                                              guess_method='barycenter')
        pltf.display_data(self.data, self.sigma,
                          center=(kwargs_init['kwargs_gaussian']['x0'], kwargs_init['kwargs_gaussian']['y0']),
                          masks=self.masks)
        pltf.display_data(self.data, sigma_2=None, units='e-',
                          center=(kwargs_init['kwargs_gaussian']['x0'], kwargs_init['kwargs_gaussian']['y0']),
                          )

if __name__ == '__main__':
    pytest.main()
