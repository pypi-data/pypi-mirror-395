import unittest
import numpy as np
import json
import os
from astropy.wcs import WCS
from starred.procedures import build_psf


class TestPSFWithDistortion(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '../data/psf_distortion_data')

        self.stars = np.load(os.path.join(self.data_path, 'stamps.npy'))
        self.noisemaps = np.load(os.path.join(self.data_path, 'noisemaps.npy'))
        self.coords = np.load(os.path.join(self.data_path, 'stars_positions.npy'))

    def test_psf_with_distortion(self):

        # check that we refuse to proceed if field_distortion is True and without providing coordinates
        with self.assertRaises(Exception):
             build_psf(image=self.stars, noisemap=self.noisemaps, subsampling_factor=2, field_distortion=True)

        result = build_psf(image=self.stars, noisemap=self.noisemaps, subsampling_factor=2, field_distortion=True,
                            stamp_coordinates=self.coords/500)
        self.assertIn('kwargs_psf', result)
        kwargs = result['kwargs_psf']
        self.assertIn('kwargs_distortion', kwargs)
        # check that the fit was carried out correctly (not the case without distortion)
        self.assertLess(result['chi2'], 1.1)


if __name__ == '__main__':
    unittest.main()
