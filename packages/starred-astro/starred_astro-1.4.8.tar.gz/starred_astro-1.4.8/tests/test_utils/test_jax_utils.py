import numpy as np
import glob
from numpy.testing import assert_allclose
import os
import unittest
import matplotlib.pyplot as plt

import starred.utils.jax_utils as starlet

from tests import TEST_PATH

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.path = TEST_PATH
        self.datapath = os.path.join(self.path, "data")
        self.data = np.array([np.load(f) for f in sorted(glob.glob(os.path.join(self.datapath, '*200w_psfg.npy')))])
        self.plot = False

    def test_wavelets(self):
        n_scales = 7
        image = np.array(self.data[0], dtype=np.float64)
        coeffs = starlet.decompose(image, n_scales)
        rec_image = starlet.reconstruct(coeffs)

        assert_allclose(image, rec_image, atol = 1e-5)

        if self.plot:
            fig, ax = plt.subplots(1, 3, figsize=(10, 5))
            im1 = ax[0].imshow(np.log10(rec_image))
            im2 = ax[1].imshow(np.log10(image))
            im3 = ax[2].imshow(rec_image - image)
            ax[0].set_title('Image')
            ax[1].set_title('Image reconstructed')
            ax[2].set_title('Residuals')
            plt.show()

        #if n_scale = 0, the decomposition is the image
        coeffs = starlet.decompose(image, 0.)
        assert_allclose(image, coeffs, atol=1e-8)