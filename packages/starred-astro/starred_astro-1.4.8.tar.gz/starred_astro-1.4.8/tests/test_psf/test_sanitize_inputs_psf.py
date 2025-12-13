import unittest
import numpy as np
import jax.numpy as jnp
from starred.procedures.psf_routines import sanitize_inputs


class TestSanitizeInputs(unittest.TestCase):
    def test_mixed_numpy_and_jax_arrays(self):
        image_np = np.array([[1, 2, np.nan], [4, 5, 6]])
        noisemap_jax = jnp.array([[0.1, 0.2, 0.3], [0.4, 0.5, jnp.nan]])
        masks_np = np.array([[True, True, True], [True, True, True]])

        with self.assertRaises(TypeError):
            sanitize_inputs(image_np, noisemap_jax, masks_np)

    def test_non_boolean_mask(self):
        image = np.array([[1, 2, np.nan], [4, 5, 6]])
        noisemap = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, np.nan]])
        masks = np.array([[1, 1, 1], [1, 1, 1]])  # non-boolean mask

        sanitized_image, sanitized_noisemap, sanitized_masks = sanitize_inputs(image, noisemap, masks)

        expected_masks = np.array([[True, True, False], [True, True, False]])
        self.assertTrue(np.array_equal(sanitized_masks, expected_masks))
        self.assertTrue(np.array_equal(sanitized_image, np.array([[1., 2., 0.], [4., 5., 0.]])))
        self.assertTrue(np.array_equal(sanitized_noisemap, np.array([[0.1, 0.2, 1.], [0.4, 0.5, 1.]])))

    def test_all_nan_inputs(self):
        image = np.array([[np.nan, np.nan], [np.nan, np.nan]])
        noisemap = np.array([[np.nan, np.nan], [np.nan, np.nan]])
        masks = np.array([[True, True], [True, True]])

        sanitized_image, sanitized_noisemap, sanitized_masks = sanitize_inputs(image, noisemap, masks)

        expected_image = np.array([[0., 0.], [0., 0.]])
        expected_noisemap = np.array([[1., 1.], [1., 1.]])
        expected_masks = np.array([[False, False], [False, False]])

        self.assertTrue(np.array_equal(sanitized_image, expected_image))
        self.assertTrue(np.array_equal(sanitized_noisemap, expected_noisemap))
        self.assertTrue(np.array_equal(sanitized_masks, expected_masks))

    def test_no_nan_inputs(self):
        image = np.array([[1, 2], [3, 4]])
        noisemap = np.array([[0.1, 0.2], [0.3, 0.4]])
        masks = np.array([[True, True], [True, True]])

        sanitized_image, sanitized_noisemap, sanitized_masks = sanitize_inputs(image, noisemap, masks)

        self.assertTrue(np.array_equal(sanitized_image, image))
        self.assertTrue(np.array_equal(sanitized_noisemap, noisemap))
        self.assertTrue(np.array_equal(sanitized_masks, masks))

    def test_mixed_dtype_arrays(self):
        image = np.array([[1, 2, np.nan], [4, 5, 6]], dtype=float)
        noisemap = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, np.nan]], dtype=float)
        masks = np.array([[1, 1, 1], [1, 1, 1]], dtype=int)  # integer mask

        sanitized_image, sanitized_noisemap, sanitized_masks = sanitize_inputs(image, noisemap, masks)

        expected_masks = np.array([[True, True, False], [True, True, False]])
        self.assertTrue(np.array_equal(sanitized_masks, expected_masks))
        self.assertTrue(np.array_equal(sanitized_image, np.array([[1., 2., 0.], [4., 5., 0.]])))
        self.assertTrue(np.array_equal(sanitized_noisemap, np.array([[0.1, 0.2, 1.], [0.4, 0.5, 1.]])))


if __name__ == '__main__':
    unittest.main()
