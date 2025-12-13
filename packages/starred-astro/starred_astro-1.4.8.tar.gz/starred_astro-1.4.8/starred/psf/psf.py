import os
import dill as pkl
import warnings
from packaging import version
import h5py
import json
from copy import deepcopy

import jax.numpy as jnp
import numpy as np
import jax
from jax import lax, vmap
from jax.scipy.ndimage import map_coordinates

from starred.utils.generic_utils import (pad_and_convolve, pad_and_convolve_fft, fwhm2sigma, gaussian_function,
                                         make_grid, gaussian_function_batched,
                                         moffat_elliptical_function, moffat_function, Downsample, scipy_convolve,
                                         save_npy, save_fits,
                                         convert_numpy_array_to_list, convert_list_to_numpy_array)


class PSF(object):
    """
    Narrow Point Spread Function class. Coordinates and FWHM are given in the original pixel grid.

    """

    def __init__(
            self,
            image_size=64,
            number_of_sources=2,
            upsampling_factor=2,
            gaussian_fwhm=2,
            convolution_method='scipy',
            gaussian_kernel_size=None,
            include_moffat=True,
            elliptical_moffat=False,
            field_distortion=False
    ):
        """
        :param image_size: input images size in pixels
        :type image_size: int
        :param number_of_sources: number of input images (each containing a point source)
        :type number_of_sources: int
        :param upsampling_factor: the rate at which the sampling frequency increases in the PSF with respect to the input images
        :type upsampling_factor: int
        :param gaussian_fwhm: the Gaussian's FWHM in pixels. Default is 2.
        :type gaussian_fwhm: int
        :param convolution_method: method to use to calculate the convolution, choose between 'fft', 'scipy', and 'lax. Recommended if jax>=0.4.9 : 'scipy'
        :type convolution_method: str
        :param gaussian_kernel_size: dimensions of the Gaussian kernel, not used if method = 'fft'. None will select the recommended size for each method.
        :type gaussian_kernel_size: int
        :param include_moffat: True for the PSF to be expressed as the sum of a Moffat and a grid of pixels. False to not include the Moffat. Default: True
        :type include_moffat: bool
        :param elliptical_moffat: Allow elliptical Moffat.
        :type elliptical_moffat: bool
        :param field_distortion: Add distortion (dilation and shear) parametrized by a 2nd order polynomial in star position
        :type field_distortion: bool

        """
        self.elliptical_moffat = elliptical_moffat
        if self.elliptical_moffat:
            self.analytic = self._analytic_ellitpical
        else:
            self.analytic = self._analytic_circular

        self.image_size = image_size
        self.upsampling_factor = upsampling_factor
        self.image_size_up = self.image_size * self.upsampling_factor
        self.M = number_of_sources
        self.include_moffat = include_moffat

        self.field_distortion = field_distortion
        # very basic safety check regarding distortion and its meaningfulness
        if field_distortion and number_of_sources < 6:
            warnings.warn(
                    "WARNING: using very few stars while requesting to fit a distortion of the PSF "
                    "depending on the star positions in the field. Might yield nonsensical results. "
                    "Consider using many more stars."
                )

        if convolution_method == 'fft':
            self._convolve = pad_and_convolve_fft
            self.gaussian_size = self.image_size_up
            if (self.image_size * self.upsampling_factor) % 2 == 1:
                self.shift_gaussian = 0.
            else :
                self.shift_gaussian = 0.5  # convention for even kernel size and fft convolution
            self.shift_direction = 1.
        elif convolution_method == 'lax':
            self._convolve = pad_and_convolve
            if gaussian_kernel_size is None:
                self.gaussian_size = 12
            else:
                self.gaussian_size = gaussian_kernel_size
            self.shift_gaussian = 0.5
            self.shift_direction = 1.
        elif convolution_method == 'scipy':
            self._convolve = scipy_convolve
            if gaussian_kernel_size is None:
                self.gaussian_size = 16
            else:
                self.gaussian_size = gaussian_kernel_size
            if version.parse(jax.__version__) < version.parse('0.4.9'):
                warnings.warn(
                    "WARNING : jax.scipy has no FFT implementation for the moment. "
                    "It might be faster to use 'fft' on CPU."
                )

            self.shift_gaussian = 0.5
            self.shift_direction = -1  # scipy has inverted shift convention
        else:
            raise NotImplementedError('Unknown convolution method : choose fft, scipy or lax')

        self.convolution_method = convolution_method
        self.fwhm = gaussian_fwhm
        self.sigma = fwhm2sigma(self.fwhm)

    def shifted_gaussians(self, i, x0, y0):
        """
        Generates a 2D array with point sources. Normalized to 1.

        :param i: current point source index
        :type i: int
        :param x0: 1D array containing the x positions of the point sources, shift are given in unit of 'big' pixels
        :param y0: 1D array containing the y positions of the point sources, shift are given in unit of 'big' pixels
        :return: 2D array

        """
        x, y = make_grid(numPix=self.gaussian_size, deltapix=1.)
        return jnp.array(gaussian_function(
            x=x, y=y,
            amp=1, sigma_x=self.sigma,
            sigma_y=self.sigma,
            # Convention : gaussian is placed at a center of a pixel
            center_x=-(self.upsampling_factor * x0[i])*self.shift_direction - self.shift_gaussian,
            center_y=-(self.upsampling_factor * y0[i])*self.shift_direction - self.shift_gaussian,
        ).reshape(self.gaussian_size, self.gaussian_size))

    def shifted_gaussians_vectorized(self, x0, y0):
        """
        shifted_gaussian method above vectorized over 'i' using broadcasting.
        """
        x, y = make_grid(numPix=self.gaussian_size, deltapix=1.)
        center_x = -(self.upsampling_factor * x0) * self.shift_direction - self.shift_gaussian
        center_y = -(self.upsampling_factor * y0) * self.shift_direction - self.shift_gaussian
        gaussian_batches = gaussian_function_batched(
            x, y,
            amp=jnp.ones_like(x0),
            sigma_x=self.sigma,
            sigma_y=self.sigma,
            center_x=center_x,
            center_y=center_y,
        ).reshape(len(x0), self.gaussian_size, self.gaussian_size)
        return gaussian_batches  # 3D array, len(x0) slices.

    def _analytic_ellitpical(self, fwhmx, fwhmy, phi, beta):
        """
        Generates the narrow PSF's analytic term.

        :param fwhm_x: the full width at half maximum value in the x direction
        :type fwhm_x: float
        :param fwhm_y: the full width at half maximum value in the y direction
        :type fwhm_y: float
        :param phi: orientation angle
        :type phi: float
        :param beta: the Moffat beta parameter
        :type beta: float

        :return: 2D Moffat

        """
        x, y = make_grid(numPix=self.image_size_up, deltapix=1.)
        return jnp.array(moffat_elliptical_function(
            x=x, y=y,
            amp=1, fwhm_x=fwhmx * self.upsampling_factor,
            fwhm_y=fwhmy * self.upsampling_factor, phi=phi, beta=beta,
            center_x=0,
            center_y=-0,
        ).reshape(self.image_size_up, self.image_size_up))

    def _analytic_circular(self, fwhm, beta):
        """
        Generates the narrow PSF's analytic term.

        :param fwhm: the full width at half maximum value in the x direction
        :type fwhm: float
        :param beta: the Moffat beta parameter
        :type beta: float

        :return: 2D Moffat

        """
        x, y = make_grid(numPix=self.image_size_up, deltapix=1.)
        return jnp.array(moffat_function(
            x=x, y=y,
            amp=1, fwhm=fwhm * self.upsampling_factor,
            beta=beta,
            center_x=0,
            center_y=-0,
        ).reshape(self.image_size_up, self.image_size_up))

    def model(self, kwargs_moffat, kwargs_gaussian, kwargs_background,
              kwargs_distortion, positions=None, high_res=False):
        """
        Creates the 2D narrow Point Spread Function (PSF) image.
        star_coordinates is not used if PSF.field_distortion is False. The loss function will handle passing an
        array of zeros in this case.

        :param kwargs_moffat: dictionary containing keyword arguments corresponding to the analytic term of the PSF
        :param kwargs_gaussian: dictionary containing keyword arguments corresponding to the Gaussian deconvolution kernel
        :param kwargs_background: dictionary containing keyword arguments corresponding to the grid of pixels
        :param kwargs_distortion: dictionary with keyword arguments corresponding to PSF variation in the field.
        :param positions: jax array of shape (N, 2): N pairs of coordinate (x,y), one per star.
                                 Default None works when PSF instance initialized with field_distortion=False.
        :param high_res: returns the up-sampled version of the PSF
        :type high_res: bool
        :return: array containing the model

        """
        # get the narrow PSF, this is the base model.
        if self.include_moffat:
            s = self.get_narrow_psf(kwargs_moffat=kwargs_moffat, kwargs_background=kwargs_background, norm=False)
        else:
            s = self.get_narrow_psf(kwargs_moffat=kwargs_moffat, kwargs_background=kwargs_background, norm=True)

        # s is a 2d array.
        # other thing we need, the gaussians that denote position (within each data stamp) and amplitude:
        r = self.get_gaussians_vectorized(kwargs_gaussian=kwargs_gaussian, kwargs_moffat=kwargs_moffat)
        # r is a 3d array.

        # now, extra step if we included distortion
        if self.field_distortion:
            distort_batch = vmap(lambda coords: apply_distortion(s, kwargs_distortion, coords),
                                 in_axes=(0,))
            s = distort_batch(positions)
            # s is now 3d! one distorted narrow psf per star position (in global image)
            # we will need to batch convolve over the axis 0 of both s and r, so, define the batched convolve:
            convolve_batched = vmap(self._convolve, in_axes=(0, 0))
        else:
            # else, just define a batch convolve on 2d s and 3d r
            convolve_batched = vmap(self._convolve, in_axes=(None, 0))

        # ready to batch convolve
        model = convolve_batched(s, r) + kwargs_background['mean'][:, None, None]
        if not high_res:
            # we also need to batch downsample ...downsample each stamp model.
            downsample_batched = vmap(lambda x: Downsample(x, factor=self.upsampling_factor),
                                      in_axes=(0,))
            model = downsample_batched(model)
        return model

    def get_moffat(self, kwargs_moffat, norm=True):
        """
        Returns the analytical part of the PSF.

        :param kwargs_moffat: dictionary containing keyword arguments corresponding to the analytic term of the PSF
        :param norm: normalizes the Moffat
        :type norm: bool

        :return: array containing the Moffat (2D array)
        """
        if self.include_moffat:
            if self.elliptical_moffat:
                moff = kwargs_moffat['C'] * self.analytic(fwhmx=kwargs_moffat['fwhm_x'], fwhmy=kwargs_moffat['fwhm_y'],
                                                          phi=kwargs_moffat['phi'], beta=kwargs_moffat['beta'])
            else:
                moff = kwargs_moffat['C'] * self.analytic(fwhm=kwargs_moffat['fwhm'], beta=kwargs_moffat['beta'])
            if norm:
                moff = moff / moff.sum()
        else:
            moff = jnp.zeros((self.image_size_up, self.image_size_up))

        return moff

    def get_narrow_psf(self, kwargs_moffat=None, kwargs_background=None, kwargs_gaussian=None,
                       kwargs_distortion=None, norm=True, position=None):
        """
        Returns the `narrow` PSF s, the main model without field distortion. Used by PSF.model

        :param kwargs_moffat: dictionary containing keyword arguments corresponding to the analytic term of the PSF
        :param kwargs_background: dictionary containing keyword arguments corresponding to the grid of pixels
        :param kwargs_gaussian: dictionary with gaussian arguments, listed s.t. we can call get_narrow_psf(**kwargs)
        :param kwargs_distortion: dictionary of named params related to distortion.
        :param norm: default (and should always be) True, whether we divide the model by the sum of its pixels
        :param position: array of shape (2, ) containing x and y coordinates. (Or tuple (x, y))
        :return: array containing the `narrow` PSF
        """

        background = self.get_background(kwargs_background=kwargs_background)
        if self.include_moffat:
            moff = self.get_moffat(kwargs_moffat=kwargs_moffat, norm=False)
            s = moff + background
        else:
            s = background
            s += lax.cond(s.sum() == 0, lambda _: 1e-6, lambda _: 0., operand=None)  # to avoid dividing by 0

        if norm:
            s = s / s.sum()

        if position is not None:
            s = apply_distortion(narrow_psf=s, kwargs_distortion=kwargs_distortion,
                                 star_xy_coordinates=position)

        return s

    def get_full_psf(self, kwargs_moffat=None, kwargs_background=None, kwargs_gaussian=None,
                     kwargs_distortion=None, norm=True, high_res=True, position=None):
        """
        Returns the PSF of the original image, `i.e.`, the convolution between s, the `narrow` PSF, and r,
        the Gaussian kernel.

        :param kwargs_moffat: dictionary containing keyword arguments corresponding to the analytic term of the PSF
        :param kwargs_background: dictionary containing keyword arguments corresponding to the grid of pixels
        :param kwargs_gaussian: dictionary containing keyword arguments related to the gaussian
        :param kwargs_distortion: dictionary with distortion keywords.
        :param norm: whether the sum of the pixels in the PSF model should be 1 (default True)
        :param high_res: whether to return the PSF model in "small pixels" (default True, False is resolution of data)
        :param position: array of shape (2, ) or tuple (x,y) in case one uses distortion.
        :return: array containing the full PSF

        """
        if position is None:
            s = self.get_narrow_psf(kwargs_moffat=kwargs_moffat, kwargs_background=kwargs_background)
        else:
            s = self.get_narrow_psf(kwargs_moffat=kwargs_moffat, kwargs_background=kwargs_background,
                                    kwargs_gaussian=kwargs_gaussian, kwargs_distortion=kwargs_distortion,
                                    position=position)
        r = self.shifted_gaussians(0, [0.], [0.])
        if high_res:
            psf = self._convolve(s, r)
        else:
            psf = Downsample(self._convolve(s, r), factor=self.upsampling_factor)
        if norm:
            psf /= psf.sum()

        return psf

    def get_background(self, kwargs_background):
        """
        Returns the numerical part of the PSF. This does not include an eventual constant sky background correction
        stored in kwargs_background['mean'].

        :param kwargs_background: dictionary containing keyword arguments corresponding to the grid of pixels
        :return: array containing the background correction
        """

        return kwargs_background['background'].reshape(self.image_size_up, self.image_size_up)

    def get_gaussian(self, init, kwargs_gaussian, kwargs_moffat):
        """
        Returns a Gaussian function, adjusted to the star of index ``init``.

        :param init: stamp index
        :type init: int
        :param kwargs_gaussian: dictionary containing keyword arguments corresponding to the Gaussian deconvolution kernel
        :param kwargs_moffat: dictionary of arguments in relation to the moffat component.
        :return: array containing the Gaussian kernel
        """
        x0, y0 = kwargs_gaussian['x0'], kwargs_gaussian['y0']
        r = self.shifted_gaussians(init, x0, y0)

        if self.include_moffat:
            # normalization by the mean to remove degeneracy with the C parameter of the moffat
            ga = kwargs_gaussian['a'][init] / kwargs_moffat['C']
        else:
            ga = kwargs_gaussian['a'][init]

        return ga * r

    def get_gaussians_vectorized(self, kwargs_gaussian, kwargs_moffat):
        """
        Same as get_gaussian, but doing all the slices at once.

        :param kwargs_gaussian: dictionary containing keyword arguments corresponding to the Gaussian deconvolution kernel
        :param kwargs_moffat: dictionary of the arguments of the Moffat. necessary for normalization purposes.

        :return: 2D array containing slices, each with Gaussian kernel at the positions given in kwargs_gaussian.
                 (so, slices of a flattened 2D array, hence 2D)
        """
        x0, y0 = kwargs_gaussian['x0'], kwargs_gaussian['y0']
        r = self.shifted_gaussians_vectorized(x0, y0)
        # this is a 3D array, stack of slices (one per position (x,y) of the arrays (x0, y0)).

        # normalization by the mean to remove degeneracy with the C parameter of the moffat
        if self.include_moffat:
            ga = kwargs_gaussian['a'] / kwargs_moffat['C']
        else:
            ga = kwargs_gaussian['a']
        r = ga[:, None, None] * r

        # so, we now have slices each containing a single gaussian, properly normalized, at the right position
        # in each slice.
        return r

    def get_amplitudes(self, kwargs_moffat=None, kwargs_gaussian=None, kwargs_background=None, kwargs_distortion=None):
        """
        Returns the photometry of the stars.

        :param kwargs_moffat: dictionary containing keyword arguments corresponding to the analytic term of the PSF
        :param kwargs_gaussian: dictionary containing keyword arguments corresponding to the Gaussian deconvolution kernel
        :param kwargs_background: dictionary containing keyword arguments corresponding to the grid of pixels
        :param kwargs_distortion: dictionary, default None, not used but listed, so we can do get_amplitudes(**kwargs)

        :return: list containing the relative photometry
       """

        kernel = self.get_narrow_psf(kwargs_moffat=kwargs_moffat, kwargs_gaussian=kwargs_gaussian,
                                     kwargs_background=kwargs_background, norm=False)
        kernel_norm = kernel.sum()
        if self.include_moffat:
            amp = (kwargs_gaussian['a'] / kwargs_moffat['C']) * kernel_norm
        else:
            amp = kwargs_gaussian['a'] * kernel_norm

        return amp

    def get_photometry(self, kwargs_moffat=None, kwargs_gaussian=None, kwargs_background=None, kwargs_distortion=None,
                       positions=None, high_res=False):
        """
        Returns the PSF photometry of all the stars.

        :param kwargs_moffat: dictionary containing keyword arguments corresponding to the analytic term of the PSF
        :param kwargs_gaussian: dictionary containing keyword arguments corresponding to the Gaussian deconvolution kernel
        :param kwargs_background: dictionary containing keyword arguments corresponding to the grid of pixels.
        :param kwargs_distortion: dictionary, default None, not used but listed, so we can do get_amplitudes(**kwargs)
        :param positions: array of shape (N, 2), default None: positions of the stars in the original
                          astronomical image, relative to the center of the image, in pixels.
        :param high_res: bool, whether to use the up-sampled model or not. (should make little difference)
        :return: array containing the photometry
        """
        if positions is None:
            positions = np.zeros((len(kwargs_gaussian['a']), 2))
        model = self.model(kwargs_moffat=kwargs_moffat, kwargs_gaussian=kwargs_gaussian,
                           kwargs_background=kwargs_background, kwargs_distortion=kwargs_distortion,
                           positions=positions, high_res=high_res)

        # remove eventual sky correction
        if high_res:
            model = model - kwargs_background['mean'][:, None, None]
        else:
            model = model - (kwargs_background['mean'][:, None, None] / self.upsampling_factor ** 2)

        return jnp.sum(model, axis=(1, 2))

    def get_astrometry(self, kwargs_moffat=None, kwargs_gaussian=None, kwargs_background=None, kwargs_distortion=None):
        """
        Returns the astrometry. In units of 'big' pixel.

        :param kwargs_moffat: dictionary containing keyword arguments corresponding to the analytic term of the PSF
        :param kwargs_gaussian: dictionary containing keyword arguments corresponding to the Gaussian deconvolution kernel
        :param kwargs_background: dictionary containing keyword arguments corresponding to the grid of pixels
        :param kwargs_distortion: dictionary, default None, not used but listed, so we can do get_amplitudes(**kwargs)

        :return: list of tuples with format [(x1,y1), (x2,y2), ...]
        """
        coord = []
        for x, y in zip(kwargs_gaussian['x0'], kwargs_gaussian['y0']):
            coord.append([x, y])

        return np.asarray(coord)

    def export(self, output_folder, kwargs_final, data, sigma_2, format='fits',
               full_psf_position=np.array([0., 0.]), star_positions=None):
        """
        Saves all the output files in fits or npy format.

        :param output_folder: path to the output folder
        :type output_folder: str
        :param kwargs_final: dictionary containing all keyword arguments
        :param data: array containing the images
        :param sigma_2: array containing the noise maps
        :param format: output format. Choose between ``npy`` or ``fits``
        :type format: str
        :param full_psf_position: array containing the position of the full PSF within the original field of view. 
        This is only relevant when the correction for field distortions is activated (`field_distortion` was set to ``True`).
        By default, it is set to (0, 0), i.e. the center of the field of view.
        :type full_psf_position: array of shape (2,)
        :param star_positions: array containing the position of the stars that were used for correcting field distortions. It is ignored if `field_distortion` was set to `False`. 
        :type star_positions: array of shape (N, 2)
        """
        if format == 'fits':
            save_fct = save_fits
        elif format == 'npy':
            save_fct = save_npy
        else:
            raise NotImplementedError(f'Format {format} unknown.')

        narrow = self.get_narrow_psf(**kwargs_final, norm=True)
        save_fct(narrow, os.path.join(output_folder, 'narrow_PSF'))

        if self.field_distortion:
            full_no_dist = self.get_full_psf(**kwargs_final, norm=True, high_res=True, 
                                             position=None)
            save_fct(full_no_dist, os.path.join(output_folder, f'full_PSF_no_distortion'))
            full = self.get_full_psf(**kwargs_final, norm=True, high_res=True,
                                     position=full_psf_position)
        else:
            full = self.get_full_psf(**kwargs_final, norm=True, high_res=True)
        save_fct(full, os.path.join(output_folder, 'full_PSF'))

        background = self.get_background(kwargs_background=kwargs_final['kwargs_background'])
        save_fct(background, os.path.join(output_folder, 'background_PSF'))

        analytic = self.get_moffat(kwargs_moffat=kwargs_final['kwargs_moffat'], norm=True)
        save_fct(analytic, os.path.join(output_folder, 'analytic_PSF'))

        if self.field_distortion:
            estimated_full_psf = self.model(**kwargs_final, positions=star_positions)
        else:
            estimated_full_psf = self.model(**kwargs_final)
        dif = data - estimated_full_psf
        rr = jnp.abs(dif) / jnp.sqrt(sigma_2)

        for i in range(self.M):
            save_fct(estimated_full_psf[i], os.path.join(output_folder, f'full_psf_{i}'))
            save_fct(dif[i], os.path.join(output_folder, f'residuals_{i}'))
            save_fct(rr[i], os.path.join(output_folder, f'scaled_residuals_{i}'))

    def dump(self, path, kwargs, norm, data=None, sigma_2=None, masks=None, save_output_level=4, format='hdf5'):
        """
        Stores information in a given file in pickle or hdf5 format (recommended).

        :param path: Filename of the output.
        :param kwargs: Dictionary containing the fitted value of the model
        :param norm: Normalisation factor of your data. This is an important to save if you want to get the correct photometry.
        :param data: (Nstar x image_size x image_size) array containing the data
        :param sigma_2: (Nstar x image_size x image_size) array containing the noise maps
        :param masks: (Nstar x image_size x image_size) array containing the noise maps
        :param save_output_level: Int. Level of output product to save: 1-just the parameters of the model, 2- add the input data, 3- add the output products (background, narrow PSF, full PSF) 4- add the output products for every image.

        """
        if format == 'pkl':
            with open(path, 'wb') as f:
                pkl.dump([self, kwargs, norm], f, protocol=pkl.HIGHEST_PROTOCOL)
        elif format == 'hdf5':
            kwargs_model = {
                'image_size': int(self.image_size),
                'number_of_sources': int(self.M),
                'upsampling_factor': int(self.upsampling_factor),
                'gaussian_fwhm': int(self.gaussian_size),
                'convolution_method': str(self.convolution_method),
                'gaussian_kernel_size': int(self.gaussian_size),
                'include_moffat': bool(self.include_moffat),
                'elliptical_moffat': bool(self.elliptical_moffat),
            }

            with h5py.File(path, 'w') as f:
                dset = f.create_dataset("kwargs_options", data=json.dumps(kwargs_model))
                dset = f.create_dataset("kwargs_PSF", data=json.dumps(convert_numpy_array_to_list(kwargs)))
                dset = f.create_dataset("Norm", data=norm)

                if save_output_level > 1:
                    if data is not None:
                        dset = f.create_dataset("Data", data=data)
                    if sigma_2 is not None:
                        dset = f.create_dataset("Sigma2", data=sigma_2)
                    if masks is not None:
                        dset = f.create_dataset("Masks", data=masks)

                if save_output_level > 2:
                    narrow = self.get_narrow_psf(kwargs_moffat=kwargs['kwargs_moffat'],
                                                 kwargs_background=kwargs['kwargs_background'], norm=True)
                    full = self.get_full_psf(kwargs_moffat=kwargs['kwargs_moffat'],
                                             kwargs_background=kwargs['kwargs_background'], norm=True,
                                             high_res=True)
                    background = self.get_background(kwargs_background=kwargs['kwargs_background'])
                    analytic = self.get_moffat(kwargs_moffat=kwargs['kwargs_moffat'], norm=True)

                    dset = f.create_dataset("Narrow PSF", data=narrow)
                    dset = f.create_dataset("Full PSF", data=full)
                    dset = f.create_dataset("Background", data=background)
                    dset = f.create_dataset("Analytic", data=analytic)

                if save_output_level > 3:
                    full_psfs = self.model(**kwargs)
                    residuals = data - full_psfs
                    scaled_residuals = jnp.abs(residuals) / jnp.sqrt(sigma_2)
                    dset = f.create_dataset("Full PSF cube", data=full_psfs)
                    dset = f.create_dataset("Residuals cube", data=residuals)
                    dset = f.create_dataset("Scaled residuals cube", data=scaled_residuals)

        else:
            raise NotImplementedError(f'Unrecognized format {format}. Choose between pkl and hdf5.')

    def smart_guess(self, data, fixed_background=True, guess_method='barycenter',
                    masks=None, offset_limit=None, guess_fwhm_pixels=3., adjust_sky=False):
        """
        Returns an initial guess of the kwargs, given the input data.

        :param data: array of shape (nimage, npix, npix) containing the input data
        :param fixed_background: fixes the background to 0
        :type fixed_background: bool
        :param guess_method: Method to guess the position of the point sources. Choose between 'barycenter' and 'max'
        :type guess_method: str
        :param masks: array of shape (nimage, npix, npix), booleans. 1 for pixel to use, 0 for pixel to ignore.
        :param offset_limit: Upper and lower bounds for the center of the star in "big" pixel. Will be used in the kwargs_down/up['kwargs_gaussian']['x0'], kwargs_down/up['kwargs_gaussian']['y0'].
        :type offset_limit: float
        :param guess_fwhm_pixels: the estimated FWHM of the PSF, is used to initialize the moffat. Default 3.
        :type guess_fwhm_pixels: float
        :param adjust_sky: if True, the constant background is adjusted for each star. Use if you expect that the sky was not uniformely subtracted. Default False. It is still recommended to subtract the sky before using this function.
        :type adjust_sky: bool

        :return: kwargs containing an initial guess of the parameters
        """

        initial_fwhm = guess_fwhm_pixels
        initial_beta = 2.
        initial_background = jnp.zeros((self.image_size_up ** 2))
        initial_background_mean = jnp.zeros(len(data))

        # Positions (initialisation at the center of gravity)
        x0_est = np.zeros(len(data))
        y0_est = np.zeros(len(data))

        # need a grid of pixels for the center of gravity:
        X, Y = jnp.indices(data[0].shape)
        # we'll recenter the positions in the loop:
        # ( -1 because coordinates start at 0)
        centerpos = (self.image_size - 1) / 2.

        # Apply masks
        masked_data = np.copy(data)
        if masks is not None:
            masked_data *= masks

        if guess_method == 'barycenter':
            # calculate center of gravity for each epoch:
            for i in range(len(data)):
                currentimage = np.copy(masked_data[i])

                # total weight of the image:
                partition = np.nansum(currentimage)
                # first moment: weight coordinates by image values
                x0 = np.nansum(X * currentimage) / partition
                y0 = np.nansum(Y * currentimage) / partition
                # x0 and y0 have their origin at top-left of image.
                x0_est[i] = y0 - centerpos
                y0_est[i] = x0 - centerpos  # x and y need to be inverted

        elif guess_method == 'max':
            # Positions (initialisation to the brightest pixel)
            x0_est = np.zeros(len(data))
            y0_est = np.zeros(len(data))
            for i in range(len(data)):
                indices = np.where(masked_data[i, :, :] == masked_data[i, :, :].max())
                x0_est[i] = (indices[1] - self.image_size / 2.)
                y0_est[i] = (indices[0] - self.image_size / 2.)  # x and y need be inverted

        elif guess_method == 'center':
            # Positions (initialisation to the brightest pixel)
            x0_est = np.zeros(len(data))
            y0_est = np.zeros(len(data))
        else :
            raise ValueError('Guess methods unknown. PLease choose between "max", "center" and "barycenter".')

        if self.include_moffat:
            # Amplitude (use the total flux to scale the amplitude parameters)
            mean_flux = masked_data.sum() / len(data)
            ratio = jnp.array([masked_data[i].sum() / mean_flux for i in range(len(data))])
            initial_a = jnp.ones(len(data)) * ratio

            if self.elliptical_moffat:
                kwargs_moffat_guess = {'fwhm_x': initial_fwhm, 'fwhm_y': initial_fwhm, 'phi': 0., 'beta': initial_beta,
                                       'C': 1.}
                kwargs_moffat_up = {'fwhm_x': self.image_size, 'fwhm_y': self.image_size, 'phi': np.pi / 2.,
                                    'beta': 50.,
                                    'C': jnp.inf}
                kwargs_moffat_down = {'fwhm_x': 2., 'fwhm_y': 2., 'phi': 0., 'beta': 0., 'C': 0.}
            else:
                kwargs_moffat_guess = {'fwhm': initial_fwhm, 'beta': initial_beta, 'C': 1.}
                kwargs_moffat_up = {'fwhm': self.image_size, 'beta': 50., 'C': jnp.inf}
                kwargs_moffat_down = {'fwhm': 2., 'beta': 0., 'C': 0.}

            flux_moffat = Downsample(self.get_moffat(kwargs_moffat_guess, norm=False),
                                     factor=self.upsampling_factor).sum()
            initial_C = float(mean_flux / flux_moffat)

            kwargs_moffat_guess['C'] = initial_C
        else:
            initial_a = jnp.array([masked_data[i].sum() for i in range(len(data))]) * self.upsampling_factor ** 2
            kwargs_moffat_guess = {}
            kwargs_moffat_up = {}
            kwargs_moffat_down = {}
            initial_C = 1.


        param_number_distortion = 2
        kwargs_moffat_guess['C'] = initial_C
        kwargs_init = {
            'kwargs_moffat': kwargs_moffat_guess,
            'kwargs_gaussian': {'a': initial_a * initial_C, 'x0': x0_est, 'y0': y0_est},
            'kwargs_background': {'background': initial_background, 'mean': initial_background_mean},
            'kwargs_distortion': {
                'dilation_x': np.zeros(param_number_distortion),  # 5 numbers: coefficients of a 2d order 2 polynomial minus constant term
                'dilation_y': np.zeros(param_number_distortion),
                'shear': np.zeros(param_number_distortion)
            }
        }
        kwargs_fixed = {
            'kwargs_moffat': {},
            'kwargs_gaussian': {},
            'kwargs_background': {},
            'kwargs_distortion': {},
        }
        if not self.field_distortion:
            kwargs_fixed['kwargs_distortion'] = deepcopy(kwargs_init['kwargs_distortion'])

        if fixed_background:
            kwargs_fixed['kwargs_background']['background'] = initial_background

        if not adjust_sky:
            kwargs_fixed['kwargs_background']['mean'] = initial_background_mean

        if offset_limit is None:
            offset_limit = self.image_size / 2.

        # Default value for boundaries
        kwargs_up = {
            'kwargs_moffat': kwargs_moffat_up,
            'kwargs_gaussian': {'a': list([jnp.inf for i in range(len(data))]),
                                'x0': list([offset_limit for i in range(len(data))]),
                                'y0': list([offset_limit for i in range(len(data))])
                                },
            'kwargs_background': {'background': list([jnp.inf for i in range(self.image_size_up ** 2)]),
                                  'mean': list([jnp.inf for i in range(len(data))])},
            'kwargs_distortion': {
                'dilation_x': 100*np.ones(param_number_distortion),  # 5 numbers: coefficients of a 2d order 2 polynomial minus constant term
                'dilation_y': 100*np.ones(param_number_distortion),
                'shear': 100*np.ones(param_number_distortion)
            }
        }

        kwargs_down = {
            'kwargs_moffat': kwargs_moffat_down,
            'kwargs_gaussian': {'a': list([0 for i in range(len(data))]),
                                'x0': list([-offset_limit for i in range(len(data))]),
                                'y0': list([-offset_limit for i in range(len(data))]),
                                },
            'kwargs_background': {'background': list([-jnp.inf for i in range(self.image_size_up ** 2)]),
                                  'mean': list([-jnp.inf for i in range(len(data))])},
            'kwargs_distortion': {
                'dilation_x': -100 * np.ones(param_number_distortion),
                'dilation_y': -100 * np.ones(param_number_distortion),
                'shear': -100 * np.ones(param_number_distortion)
            }
        }

        return kwargs_init, kwargs_fixed, kwargs_up, kwargs_down


def shear_stretch_transformation_from_polynomial(kwargs_distortion, star_xy_coordinates):
    """
    Function used in PSF class above for distortions.
    Given the polynomial coefficients in kwargs_field_distortion and the coordinates of the star at hand,
    yields what the amount of shear and stretch is.

    :param kwargs_distortion: dictionary with polynomial coefficients, function of image coordinates.
    :param star_xy_coordinates: tuple or array, (x,y).
    :return: array of length 3, [dilation_x, dilation_y, shear].
    """
    x, y = star_xy_coordinates.T
    dilation_x_coeffs = kwargs_distortion['dilation_x']
    dilation_y_coeffs = kwargs_distortion['dilation_y']
    shear_coeffs = kwargs_distortion['shear']

    # f(x, y) = a10*x + a01*y + a20*x^2 + a11*x*y + a02*y^2
    # a00 (constant term) is set below.
    def eval_poly(coeffs):
        return coeffs[0] * x + coeffs[1] * y

    dilation_x = 1. + eval_poly(dilation_x_coeffs)  # 0 coefficients means no dilation
    dilation_y = 1. + eval_poly(dilation_y_coeffs)
    shear = eval_poly(shear_coeffs)  # 0 coefficients means no shear

    affine_transform = jnp.array([
        [dilation_x, shear],
        [shear, dilation_y]
    ])
    return affine_transform


def apply_distortion(narrow_psf, kwargs_distortion, star_xy_coordinates):
    """
    Function used in PSF class above for distortions.
    Given some coefficients in kwargs_field_distortion, applies to narrow_psf the shear and stretch effective at the
    star_xy_coordinates position.

    :param narrow_psf: the 2d image containing the narrow PSF.
    :type narrow_psf: 2d jax array
    :param kwargs_distortion: dictionary with polynomial coefficients, function of image coordinates.
    :param star_xy_coordinates: array of shape (2, ), i.e. (x, y).
    :return: the transformed narrow_psf.
    """
    # keep track of the norm we had at the beginning
    initial_norm = narrow_psf.sum()
    # grid
    height, width = narrow_psf.shape
    y_coords, x_coords = jnp.meshgrid(jnp.arange(height), jnp.arange(width), indexing='ij')

    # the params
    affine_transform = shear_stretch_transformation_from_polynomial(kwargs_distortion=kwargs_distortion,
                                                                    star_xy_coordinates=star_xy_coordinates)
    # inverse transform on coordinates
    new_coordinates = jnp.tensordot(jnp.linalg.inv(affine_transform),
                                    jnp.array([y_coords, x_coords]), axes=([1], [0]))
    # subtract any offset to keep things centered
    induced_offset = (new_coordinates.mean(axis=(1, 2))) - jnp.array([(height - 1) / 2, (width - 1) / 2])
    # new coordinates to map the original image to
    new_coordinates -= induced_offset[:, jnp.newaxis, jnp.newaxis]
    # jax ndimage magic. first order interpolation fine since we work in subsampled pixels.
    transformed_image = map_coordinates(narrow_psf, new_coordinates, order=1)
    # normalize back to original norm ... this step is only included because a lot of methods within
    # this class propose to not normalize the narrow psf.
    transformed_image /= (transformed_image.sum() / initial_norm)
    return transformed_image


def load_PSF_model(input_file, format='hdf5'):
    """ Load PSF model class from hdf5 or pickle file"""

    if format == 'pkl':
        with open(input_file, 'rb') as f:
            model, kwargs, norm = pkl.load(f)
            data, sigma_2, masks = None, None, None

    elif format == 'hdf5':
        with h5py.File(input_file, 'r') as f:
            kwargs_model = json.loads(f['kwargs_options'][()])
            model = PSF(**kwargs_model)
            kwargs = json.loads(f['kwargs_PSF'][()])
            kwargs = convert_list_to_numpy_array(kwargs)
            norm = f['Norm'][()]

            if 'Data' in f.keys():
                data = f['Data'][()]
            else:
                print(f'No Data found in {input_file}')
                data = None
            if 'Sigma2' in f.keys():
                sigma_2 = f['Sigma2'][()]
            else:
                print(f'No Noise maps found in {input_file}')
                sigma_2 = None
            if 'Masks' in f.keys():
                masks = f['Masks'][()]
            else:
                print(f'No masks found in {input_file}')
                masks = None
    else:
        raise NotImplementedError(f'Unrecognized format {format}. Choose between pkl and hdf5.')
    return model, kwargs, norm, data, sigma_2, masks
