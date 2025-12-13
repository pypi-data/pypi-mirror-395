from copy import deepcopy
import glob
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import os
import pytest
import unittest
import matplotlib.pyplot as plt
import skimage


from tests import TEST_PATH
from starred.psf.psf import PSF
from starred.procedures.psf_routines import narrow_psf_from_model
from starred.utils.generic_utils import make_grid, gaussian_function, fwhm2sigma

class TestConvolution(unittest.TestCase):

    def setUp(self):
        self.path = TEST_PATH


    def test_centering(self):
        """
        Expected behaviour is the following :
        - for even number of small pixels : Moffat centered in the middle of the central 4 pixels, Gaussian,
        centered in the middle of the center lower left pixel, convolution centered in the middle of the central 4 pixels
        - for odd number of small pixels : Moffat, Gaussian and convolution are centered in the center of the central pixel
        """
        image_sizes = [64, 65]
        subsampling_factors = [1,2,3]
        convolution_methods = ['fft']

        for image_size in image_sizes:
            for subsampling_factor in subsampling_factors:
                for convolution_method in convolution_methods:
                    image_size_up = image_size * subsampling_factor
                    model = PSF(image_size=image_size, number_of_sources=1, upsampling_factor=subsampling_factor,
                                convolution_method=convolution_method)

                    x0, y0 = -0., -0.
                    fwhm, beta = 1., 1.
                    gaussian = model.shifted_gaussians(0, [x0], [y0])
                    moffat = model.analytic(fwhm, beta)
                    convolution = model._convolve(moffat, gaussian, False).reshape(image_size_up, image_size_up)

                    arrays_list = [gaussian, moffat, convolution]
                    array_name = ['gaussian', 'moffat', 'convolution']
                    print('Image size, Subsampling factor :', image_size, subsampling_factor)
                    for array, name in zip(arrays_list, array_name):
                        print('### %s ###' % name)
                        print(convolution_method)
                        nx, ny = np.shape(array)
                        indices = np.where(array == array.max())

                        #expected behaviour is coded here. It should match the description in the documentation of this function
                        if (subsampling_factor*image_size)%2 == 1 :
                            indices_real = [(int(nx / 2 + x0), int(nx / 2 + y0))]
                        else :
                            if name == 'gaussian':
                                indices_real = [(int(nx / 2 + x0 - 1), int(nx / 2 + y0 - 1))]
                            elif name == 'moffat':
                                indices_real = [(int(nx / 2 - 1), int(nx / 2 - 1)), (int(nx / 2 - 1), int(nx / 2)),
                                                (int(nx / 2), int(nx / 2 - 1)), (int(nx / 2), int(nx / 2)), ]
                            else:
                                indices_real = [(int(nx / 2 - x0 - 1), int(nx / 2 - y0 - 1)), (int(nx / 2 - x0 - 1), int(nx / 2 - y0)),
                                                (int(nx / 2 - x0), int(nx / 2 - y0 - 1)), (int(nx / 2 - x0), int(nx / 2 - y0)), ]

                        n = len(indices[0])
                        n1 = len(indices_real)
                        print('Indices Max:', [(indices[0][i], indices[1][i]) for i in range(n)])
                        center = np.asarray([array[(indices[0][i], indices[1][i])] for i in range(n)])
                        print('Center values Max:', center)
                        print('Indices Real:', indices_real)
                        center_real = np.asarray([array[indices_real[i]] for i in range(n1)])
                        print('Center values Real:', center_real)

                        if name=='gaussian' or name=='moffat':
                            assert n == n1
                            assert_allclose(center, center_real, rtol=1e-5)
                        else : #convolution can introduce numerical error so indices might not be listed in np.where(array == array.max())
                            assert_allclose(center_real, np.asarray([center[0] for i in range(n1)]), rtol=1e-3)

    def test_convolution(self):
        image_sizes = [64,63]
        subsampling_factors = [1,2,3]
        plot = False

        for image_size in image_sizes:
            for subsampling_factor in subsampling_factors:
                gain = 2  # WFI camera
                t_exp = 1  # because images are in ADU
                data_path = os.path.join(TEST_PATH, 'data')
                file_paths = sorted(glob.glob(os.path.join(data_path, 'star_*.npy')))

                new_vignets_data = np.array([np.load(f) for f in file_paths]) * t_exp / gain
                N = len(file_paths)  # number of stars
                image_size_data = np.shape(new_vignets_data)[1]  # data dimensions
                crop = int(image_size_data - image_size)
                new_vignets_data = new_vignets_data[:, crop:, crop:]
                image_size_up = image_size * subsampling_factor
                initial_background = np.zeros((image_size_up ** 2))

                # noise maps
                sigma_2 = np.zeros((N, image_size, image_size))
                sigma_sky_2 = np.array(
                    [np.std(new_vignets_data[i, int(0.9 * image_size):, int(0.9 * image_size):]) for i in
                     range(N)]) ** 2
                for i in range(N):
                    sigma_2[i, :, :] = sigma_sky_2[i] + new_vignets_data[i, :, :].clip(min=0)

                model_fft = PSF(image_size=image_size, number_of_sources=1, upsampling_factor=subsampling_factor,
                                convolution_method='fft')
                model_lax = PSF(image_size=image_size, number_of_sources=1, upsampling_factor=subsampling_factor,
                                convolution_method='lax', gaussian_kernel_size=None)
                model_lax = PSF(image_size=image_size, number_of_sources=1, upsampling_factor=subsampling_factor,
                                convolution_method='lax', gaussian_kernel_size=12)
                model_scipy = PSF(image_size=image_size, number_of_sources=1, upsampling_factor=subsampling_factor,
                                convolution_method='scipy', gaussian_kernel_size=None)
                model_scipy = PSF(image_size=image_size, number_of_sources=1, upsampling_factor=subsampling_factor,
                                convolution_method='scipy', gaussian_kernel_size=32)

                kwargs_moffat = {'fwhm': 3.67601011, 'beta': 2.03707302, 'C':1.}
                kwargs_gaussian = {'a': np.array([1., 1., 1.]), 'x0': np.array([-0.0,  0.25,  0.5]),
                                   'y0': np.array([-0.0, 0.25,  0.5])}
                kwargs_background = {'background': initial_background, 'mean': np.zeros(N)}
                kwargs_distortion = {'dilation_x': np.zeros(5), 'dilation_y': np.zeros(5), 'shear': np.zeros(5)}

                fft = []
                lax = []
                diff = []
                diff2 = []
                sc = []
                residuals = []
                residuals2 = []

                fft = model_fft.model(kwargs_moffat=kwargs_moffat,
                                      kwargs_gaussian=kwargs_gaussian,
                                      kwargs_background=kwargs_background,
                                      kwargs_distortion=kwargs_distortion)
                lax = model_lax.model(kwargs_moffat=kwargs_moffat,
                                      kwargs_gaussian=kwargs_gaussian,
                                      kwargs_background=kwargs_background,
                                      kwargs_distortion=kwargs_distortion)
                sc = model_scipy.model(kwargs_moffat=kwargs_moffat,
                                       kwargs_gaussian=kwargs_gaussian,
                                       kwargs_background=kwargs_background,
                                       kwargs_distortion=kwargs_distortion)
                for i in range(N):
                    convolution_fft1 = fft[i]
                    convolution_lax1 = lax[i]
                    convolution_scipy1 = sc[i]
                    diff.append((convolution_fft1 - convolution_lax1) / np.sqrt(sigma_2[i, :,:]))
                    diff2.append((convolution_fft1 - convolution_scipy1) / np.sqrt(sigma_2[i, :,:]))
                    residuals.append((convolution_fft1 - convolution_lax1))
                    residuals2.append((convolution_fft1 - convolution_scipy1))

                    assert_allclose(np.zeros(convolution_lax1.shape), (convolution_fft1 - convolution_lax1), atol=1e-7, rtol=1)
                    assert_allclose(np.zeros(convolution_scipy1.shape), (convolution_fft1 - convolution_scipy1), atol=1e-7, rtol=1)

                if plot:
                    fig, ax = plt.subplots(5, N, figsize=(12, 10))
                    im = []
                    for i in range(N):
                        im1 = ax[0, i].imshow(fft[i])
                        im2 = ax[1, i].imshow(lax[i])
                        im2 = ax[2, i].imshow(sc[i])
                        im3 = ax[3, i].imshow(diff[i][2:-2,2:-2])
                        im4 = ax[4, i].imshow(diff2[i][2:-2,2:-2])
                        im.append(im3)
                        ax[0, i].set_title('FFT convolution %i' % i)
                        ax[1, i].set_title('LAX convolution %i' % i)
                        ax[2, i].set_title('Scipy convolution %i' % i)
                        ax[3, i].set_title('FFT - LAX  (sigma) %i' % i)
                        ax[4, i].set_title('FFT - Scipy (sigma) %i' % i)

                        fig.colorbar(im3, ax=ax[3, i])
                        fig.colorbar(im4, ax=ax[4, i])

                    plt.tight_layout()
                    plt.show()

    def test_deconvolution_fourier_same_resolution(self):
        subsampling_ins = [1, 2, 3, 4, 5]
        npix_originals = [64, 65]

        for subsampling_in in subsampling_ins:
            for npix_original in npix_originals:
                print('#############################################')
                print('Subsampling in:', subsampling_in)
                print('Original PSF size:', npix_original)

                subsampling_out = subsampling_in
                npsf_in = npix_original * subsampling_in
                npsf_out = npix_original * subsampling_out

                sigma_narrowpsf = fwhm2sigma(2)
                sigma_gaussian = fwhm2sigma(2)
                sigma_fullpsf = fwhm2sigma(np.sqrt(2 ** 2 + 2 ** 2))

                x_in, y_in = make_grid(numPix=npsf_in, deltapix=1.)
                x_out, y_out = make_grid(numPix=npsf_out, deltapix=1.)

                PSF_model = gaussian_function(
                    x=x_in, y=y_in,
                    amp=1, sigma_x=sigma_fullpsf,
                    sigma_y=sigma_fullpsf,
                    center_x=0,
                    center_y=0,
                ).reshape(npsf_in, npsf_in)

                narrow_psf_truth = gaussian_function(
                    x=x_out, y=y_out,
                    amp=1, sigma_x=sigma_narrowpsf,
                    sigma_y=sigma_narrowpsf,
                    center_x=0,
                    center_y=0,
                ).reshape(npsf_out, npsf_out)

                narrow_psf_reconstructed = narrow_psf_from_model(PSF_model, subsampling_in, subsampling_out,
                                                                 mode='fourier_division')

                assert np.allclose(narrow_psf_reconstructed, narrow_psf_truth, atol=1e-2)
                assert np.max(np.abs(narrow_psf_reconstructed - narrow_psf_truth)) / np.max(narrow_psf_truth) < 0.03

                print('Max error / max PSF:',
                      np.max(np.abs(narrow_psf_reconstructed - narrow_psf_truth)) / np.max(narrow_psf_truth))
                print('MAE :', np.mean(np.abs(narrow_psf_reconstructed - narrow_psf_truth)))

                # build the PFS class and check that the convolution works
                model = PSF(image_size=npsf_in, upsampling_factor=1, number_of_sources=1, include_moffat=False)
                kwargs, _, _, _ = model.smart_guess(PSF_model[np.newaxis, :, :])
                kwargs['kwargs_moffat']['C'] = 0.
                kwargs['kwargs_gaussian']['a'] = np.array([1.])
                kwargs['kwargs_gaussian']['x0'] = np.array([0.])
                kwargs['kwargs_gaussian']['y0'] = np.array([0.])
                kwargs['kwargs_background']['background'] = narrow_psf_reconstructed.ravel()

                full_PFS_reconstructed = model.get_full_psf(**kwargs)
                print('Max error / max PSF, full PSF:', np.max(np.abs(full_PFS_reconstructed - PSF_model)))
                print('MAE :', np.mean(np.abs(full_PFS_reconstructed - PSF_model)))

                assert np.allclose(full_PFS_reconstructed, PSF_model, atol=1e-3)
                assert np.max(np.abs(full_PFS_reconstructed - PSF_model)) / np.max(PSF_model) < 0.01

    def test_deconvolution_fourier_upsample(self):
        subsampling_ins = [1]
        increase_factors = [2, 3]
        npix_originals = [64, 65]

        for subsampling_in in subsampling_ins:
            for increase_factor in increase_factors:
                for npix_original in npix_originals:
                    print('#############################################')
                    print('Subsampling in:', subsampling_in, 'Increase factor:', increase_factor)
                    print('Original PSF size:', npix_original)

                    subsampling_out = increase_factor * subsampling_in
                    print('Subsampling out:', subsampling_out)
                    npsf_in = npix_original * subsampling_in
                    npsf_out = npix_original * subsampling_out

                    sigma_narrowpsf = fwhm2sigma(2)
                    sigma_gaussian = fwhm2sigma(2)
                    sigma_fullpsf = fwhm2sigma(np.sqrt(2 ** 2 + 2 ** 2))

                    x_in, y_in = make_grid(numPix=npsf_in, deltapix=1.)
                    x_out, y_out = make_grid(numPix=npsf_out, deltapix=1.)

                    PSF_model = gaussian_function(
                        x=x_in, y=y_in,
                        amp=1, sigma_x=sigma_fullpsf,
                        sigma_y=sigma_fullpsf,
                        center_x=0,
                        center_y=0,
                    ).reshape(npsf_in, npsf_in)

                    narrow_psf_truth = gaussian_function(
                        x=x_out, y=y_out,
                        amp=1, sigma_x=sigma_narrowpsf,
                        sigma_y=sigma_narrowpsf,
                        center_x=0,
                        center_y=0,
                    ).reshape(npsf_out, npsf_out)

                    narrow_psf_reconstructed = narrow_psf_from_model(PSF_model, subsampling_in, subsampling_out,
                                                                     mode='fourier_division')
                    print('Max error / max PSF:',
                          np.max(np.abs(narrow_psf_reconstructed - narrow_psf_truth)) / np.max(narrow_psf_truth))
                    print('MAE :', np.mean(np.abs(narrow_psf_reconstructed - narrow_psf_truth)))

                    # build the PFS class and check that the convolution works
                    model = PSF(image_size=npsf_in, upsampling_factor=increase_factor, number_of_sources=1,
                                include_moffat=False)
                    kwargs, _, _, _ = model.smart_guess(PSF_model[np.newaxis, :, :])
                    kwargs['kwargs_moffat']['C'] = 0.
                    kwargs['kwargs_gaussian']['a'] = np.array([1.])
                    kwargs['kwargs_gaussian']['x0'] = np.array([0.])
                    kwargs['kwargs_gaussian']['y0'] = np.array([0.])
                    kwargs['kwargs_background']['background'] = narrow_psf_reconstructed.ravel()

                    full_PFS_reconstructed = model.get_full_psf(**kwargs, high_res=False)

                    print('Max error / max PSF, full PSF:', np.max(np.abs(full_PFS_reconstructed - PSF_model)))
                    print('MAE :', np.mean(np.abs(full_PFS_reconstructed - PSF_model)))
                    assert np.allclose(full_PFS_reconstructed, PSF_model, atol=1e-1)
                    assert np.max(np.abs(full_PFS_reconstructed - PSF_model)) / np.max(PSF_model) < 0.15

    def test_deconvolution_fourier_downsample(self):
        subsampling_ins = [2, 3, 4]
        increase_factors = [0.5, 1 / 3., 0.25]
        # subsampling_ins = [1]
        npix_originals = [64, 65]
        # npix_originals = [64]

        for subsampling_in, increase_factor in zip(subsampling_ins, increase_factors):
            for npix_original in npix_originals:
                print('#############################################')
                print('Subsampling in:', subsampling_in, 'Increase factor:', increase_factor)
                print('Original PSF size:', npix_original)

                subsampling_out = int(increase_factor * subsampling_in)
                print('Subsampling out:', subsampling_out)
                npsf_in = int(npix_original * subsampling_in)
                npsf_out = int(npix_original * subsampling_out)

                sigma_narrowpsf = fwhm2sigma(2)
                sigma_gaussian = fwhm2sigma(2)
                sigma_fullpsf = fwhm2sigma(np.sqrt(2 ** 2 + 2 ** 2))

                x_in, y_in = make_grid(numPix=npsf_in, deltapix=1.)
                x_out, y_out = make_grid(numPix=npsf_out, deltapix=1.)

                PSF_model = gaussian_function(
                    x=x_in, y=y_in,
                    amp=1, sigma_x=sigma_fullpsf,
                    sigma_y=sigma_fullpsf,
                    center_x=0,
                    center_y=0,
                ).reshape(npsf_in, npsf_in)

                narrow_psf_truth = gaussian_function(x=x_out, y=y_out,
                                                     amp=1, sigma_x=sigma_narrowpsf,
                                                     sigma_y=sigma_narrowpsf,
                                                     center_x=0,
                                                     center_y=0,
                                                     ).reshape(npsf_out, npsf_out)

                narrow_psf_reconstructed = narrow_psf_from_model(PSF_model, subsampling_in, subsampling_out,
                                                                 mode='fourier_division')

                print('Max error / max PSF:',
                      np.max(np.abs(narrow_psf_reconstructed - narrow_psf_truth)) / np.max(narrow_psf_truth))
                print('MAE :', np.mean(np.abs(narrow_psf_reconstructed - narrow_psf_truth)))

                # build the PFS class and check that the convolution works
                model = PSF(image_size=npsf_out, upsampling_factor=1, number_of_sources=1, include_moffat=False)
                PSF_in = skimage.transform.rescale(PSF_model, scale=increase_factor, order=1)
                kwargs, _, _, _ = model.smart_guess(PSF_in[np.newaxis, :, :])
                kwargs['kwargs_moffat']['C'] = 0.
                kwargs['kwargs_gaussian']['a'] = np.array([1.])
                kwargs['kwargs_gaussian']['x0'] = np.array([0.])
                kwargs['kwargs_gaussian']['y0'] = np.array([0.])
                kwargs['kwargs_background']['background'] = narrow_psf_reconstructed.ravel()

                full_PFS_reconstructed = model.get_full_psf(**kwargs)

                print('Max error / max PSF, full PSF:', np.max(np.abs(full_PFS_reconstructed - PSF_in)))
                print('MAE :', np.mean(np.abs(full_PFS_reconstructed - PSF_in)))

                assert np.max(np.abs(full_PFS_reconstructed - PSF_in)) < 0.20

    def test_raise(self):
        with self.assertRaises(NotImplementedError):
            PSF(convolution_method='unknown')

    def test_raise_fourier_div(self):
        with self.assertRaises(NotImplementedError):
            narrow_psf_from_model(np.zeros((10, 10)), 2, 2, mode='unknown')

        with self.assertRaises(ValueError):
            narrow_psf_from_model(np.zeros((10, 10)), 3, 2, mode='fourier_division')

        with self.assertRaises(ValueError):
            narrow_psf_from_model(np.zeros((10, 10)), 2, 3, mode='fourier_division')
