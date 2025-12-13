import warnings
from copy import deepcopy
from functools import partial
from scipy.interpolate import griddata

import jax.numpy as jnp
import numpy as np
from jax import vmap, jit
from jax.lax import scan, dynamic_slice, dynamic_update_slice
import dill as pkl
import os
import h5py
import json

from starred.utils.generic_utils import pad_and_convolve_fft, \
    pad_and_convolve, scipy_convolve, \
    fwhm2sigma, gaussian_function, \
    make_grid, Downsample, save_fits, save_npy, convert_numpy_array_to_list, convert_list_to_numpy_array
from starred.utils.jax_utils import translate_array, rotate_array
from starred.utils.light_profile_analytical import sersic_ellipse


class Deconv(object):
    """
    Image deconvolution class. The order of the params below matters for unpacking re-packing dictionaries.

    """

    def __init__(self, image_size, number_of_sources, scale,
                 upsampling_factor=2, epochs=1, psf=None,
                 gaussian_fwhm=2, N_sersic=0, convolution_method='fft'):
        """
        :param image_size: input image size in pixels
        :type image_size: int
        :param number_of_sources: amount of point sources
        :type number_of_sources: int
        :param scale: point source scaling factor
        :type scale: float
        :param upsampling_factor: the proportion by which the sampling rate increases with respect to the input image
        :type upsampling_factor: int
        :param epochs: for a joint deconvolution, the number of epochs considered. For single deconvolution, ``epochs`` is 1
        :type epochs: int
        :param psf: Point Spread Function array from ``starred.psf.psf``, acting as deconvolution kernel here
        :param gaussian_fwhm: the Gaussian's FWHM in pixels
        :type gaussian_fwhm: int
        :param convolution_method: method to use to calculate the convolution : 'fft', 'scipy' (recommended), or 'lax'
        :type convolution_method: str

        """
        self.image_size = image_size

        # setter since vectorized functions used here depend on upsampling factor:
        self.setUpsamplingFactor(upsampling_factor)

        self.image_size_up = image_size * upsampling_factor
        self.epochs = epochs
        self.M = number_of_sources
        self.N_sersic = N_sersic
        self.gaussian_fwhm = gaussian_fwhm
        # let's carry the coordinates of our working grid (the upscaled one):
        self.x, self.y = make_grid(numPix=self.image_size_up, deltapix=1.)

        if psf is None:
            raise TypeError('Please provide the narrow PSF.')
        else:
            if not len(psf.shape) == 3:
                raise RuntimeError(
                    'We expect your psf to have a shape of form (epochs, nx, ny). '
                    f'Your psf has shape: {psf.shape}'
                )
            n_epochs, nx, ny = psf.shape
            assert n_epochs == self.epochs, "Please provide one PSF for each epoch"

            if nx != self.image_size_up or ny != self.image_size_up:
                warnings.warn(
                    'The narrow PSF does not have the same size as the upsampled image. '
                    'This might be desired to speed up the computation but make sure it is at '
                    'the resolution of the upsampled image.')

            # for convolution_method = 'fft', image and kernel must have the same size
            if (nx != self.image_size_up or ny != self.image_size_up) and convolution_method == 'fft':
                print('Padding the PSFs to match the upsampled image size...')
                if (self.image_size_up - nx) % 2 or (self.image_size_up - ny) % 2:
                    raise RuntimeError(
                        'Upsampled image size and PSF size do not match. Please pad the PSF manually to match '
                        'the size of the upsampled image. Make sure it is properly centered. '
                        'PSF kernels should have an even number of pixels if your are using convolution method "fft".')
                else:
                    padx, pady = int((self.image_size_up - nx) / 2), int((self.image_size_up - ny) / 2)
                    psf = jnp.pad(psf, ((0, 0), (padx, padx), (pady, pady)), constant_values=0.)

            self.psf = psf.astype(jnp.float32)

        if convolution_method == 'fft':
            self._convolve = pad_and_convolve_fft
            if nx % 2 == 0:
                self.shift_gaussian = -0.5
            else:
                self.shift_gaussian = 0.
            self.shift_direction = 1
        elif convolution_method == 'lax':
            self._convolve = pad_and_convolve
            if nx % 2 == 0:
                self.shift_gaussian = -0.5
            else:
                self.shift_gaussian = 0.
            self.shift_direction = 1
        elif convolution_method == 'scipy':
            self._convolve = scipy_convolve
            if nx % 2 == 0:
                self.shift_gaussian = 0.5
            else:
                self.shift_gaussian = 0.
            self.shift_direction = 1
        else:
            raise NotImplementedError('Unknown convolution method: choose fft, scipy (recommended) or lax')

        self.convolution_method = convolution_method
        self.sigma = fwhm2sigma(self.gaussian_fwhm)

        self._model = self.modelstack if self.epochs > 5 else self.modelstack_forloop
        self.scale = scale

    def shifted_gaussians(self, c_x, c_y, a, source_ID=None):
        """
        Generates a 2D array with the point sources of the deconvolved image.

        :param c_x: 1D array containing the x positions of the point sources in unit of "big" pixel
        :param c_y: 1D array containing the y positions of the point sources in unit of "big" pixel
        :param a: 1D array containing the amplitude coefficients of each Gaussian representing a point source
        :return: 2D array

        """
        if source_ID is None:
            source_ID = range(self.M)
        return jnp.sum(jnp.array([gaussian_function(
            x=self.x, y=self.y,
            amp=a[i], sigma_x=self.sigma,
            sigma_y=self.sigma,
            center_x=(self._upsampling_factor * c_x[i] - self.shift_gaussian) * self.shift_direction,
            center_y=(self._upsampling_factor * c_y[i] - self.shift_gaussian) * self.shift_direction
        ).reshape(self.image_size_up, self.image_size_up) for i in range(self.M) if i in source_ID]), axis=0)

    def sersic_background(self, R_sersic=[1.], n_sersic=[1.], e1=[0.], e2=[0.], center_x=[0.], center_y=[0.], amp=[0.]):
        """
        Return a 1D vector containing all the pixels of the Sersic background.

        :param amp: surface brightness/amplitude value at the half light radius
        :param R_sersic: semi-major axis half light radius, in big pixel
        :param n_sersic: Sersic index
        :param e1: eccentricity parameter
        :param e2: eccentricity parameter
        :param center_x: center in x-coordinate
        :param center_y: center in y-coordinate
        """

        back = jnp.zeros(self.image_size_up ** 2)
        if self.N_sersic > 0:
            for i in range(self.N_sersic):
                back += sersic_ellipse(x=self.x, y=self.y, R_sersic=self._upsampling_factor * R_sersic[i],
                                       n_sersic=n_sersic[i], e1=e1[i], e2=e2[i],
                                       center_x=(
                                                        self._upsampling_factor * center_x[
                                                    i] - self.shift_gaussian) * self.shift_direction,
                                       center_y=(
                                                        self._upsampling_factor * center_y[
                                                    i] - self.shift_gaussian) * self.shift_direction,
                                       amp=amp[i])
        return back

    def _get_background(self, kwargs):
        """
        Return the pixelated background (it does not add the mean per epoch, just the model).

        """
        kwargs_background = kwargs['kwargs_background']
        kwargs_sersic = kwargs['kwargs_sersic']

        h = kwargs_background['h']
        sersic = self.sersic_background(**kwargs_sersic)

        return h + sersic

    @partial(jit, static_argnums=(0,))
    def one_epoch(self, psf, params, h):
        """
        Produces a 2D array corresponding to one epoch of the deconvolution.

        :param psf: 2D array representing the PSF at this epoch, usually upsampled
        :param params: 1D array with the parameters in the following order:

            - the x positions of the point sources (M params)
            - the y positions of the point sources (M params)
            - the amplitudes of the point sources (M params)
            - the x translation of the whole epoch (1 param)
            - the y translation of the whole epoch (1 param)
        :param h:
            a 1D array containing the unique background of the deconvolution, ``self.image_size_up**2`` params.

        :return: 2D array that represents the model for one epoch. This is, a collection of point sources plus
        background, convolved with the PSF and potentially translated in the x and y directions

        """

        # unpack:
        # (a bit messy, see the re-packing in self.model and the comment there)
        # TODO
        c_x = params[0:self.M]
        c_y = params[self.M:2 * self.M]
        a = params[2 * self.M:3 * self.M]
        dx = params[3 * self.M]
        dy = params[3 * self.M + 1]
        alpha = params[3 * self.M + 2]
        mean = params[3 * self.M + 3]

        # initially, just the background:
        f = h.reshape((self.image_size_up, self.image_size_up))

        # add the point sources at the deconvolved resolution:
        f += self.scale * self.shifted_gaussians(c_x, c_y, a)

        # rotate
        f = rotate_array(f, alpha)

        # shift to compensate small translations between epochs:
        f = translate_array(f, self._upsampling_factor * dx, self._upsampling_factor * dy)

        # convolve with the psf to match the resolution of the observation:
        f = self._convolve(f, psf).reshape(self.image_size_up,
                                           self.image_size_up)

        # now we can also add the constant background:
        f += mean
        # adding after translation avoids border effects
        # (translation pads image with 0s, very noticeable when mean != 0)

        return f

    def getDeconvolved(self, kwargs, epoch=None):
        """
        This is a utility function to retrieve the deconvolved model at one
        specific epoch. It will typically be called only once after the optimization process.

        :param kwargs: dictionary containing the parameters of the model
        :param epoch: number of epochs, if none, it will return the mean image
        :type epoch: int
        :return: tuple of two 2D arrays: (deconvolved image, background)

        """
        kwargs_analytic = kwargs['kwargs_analytic']
        kwargs_background = kwargs['kwargs_background']

        c_x = kwargs_analytic['c_x']
        c_y = kwargs_analytic['c_y']
        if epoch is None:
            a = self.mean_pts_amps(kwargs_analytic['a'])
            dx = 0.
            dy = 0.
            alpha = 0.
            mean = jnp.mean(kwargs_background['mean'])
        else:
            a = kwargs_analytic['a'][self.M * epoch:self.M * (epoch + 1)]
            dx = kwargs_analytic['dx'][epoch]
            dy = kwargs_analytic['dy'][epoch]
            alpha = kwargs_analytic['alpha'][epoch]
            mean = kwargs_background['mean'][epoch]

        h = self._get_background(kwargs).reshape(self.image_size_up, self.image_size_up)
        h = h.copy()
        f = h.copy()
        if self.M != 0:
            f += self.scale * self.shifted_gaussians(c_x, c_y, a)

        deconvolved = rotate_array(f, alpha)
        deconvolved = translate_array(deconvolved, self._upsampling_factor * dx,
                                      self._upsampling_factor * dy)  # TODO : + mean here ?

        background = rotate_array(h, alpha)
        background = translate_array(background, self._upsampling_factor * dx, self._upsampling_factor * dy) + mean

        return deconvolved, background

    def getPts_source(self, kwargs, epoch=None, source_ID=None):
        """
        This is a utility function to retrieve an image with only the point source components at one
        specific epoch.

        :param kwargs: dictionary containing the parameters of the model
        :param epoch: number of epochs. If none, it will return the mean image
        :type epoch: int
        :return: 2D array.
        """
        kwargs_analytic = kwargs['kwargs_analytic']
        kwargs_background = kwargs['kwargs_background']

        c_x = kwargs_analytic['c_x']
        c_y = kwargs_analytic['c_y']
        if epoch is None:
            a = self.mean_pts_amps(kwargs_analytic['a'])
            dx = 0.
            dy = 0.
            alpha = 0.
        else:
            a = kwargs_analytic['a'][self.M * epoch:self.M * (epoch + 1)]
            dx = kwargs_analytic['dx'][epoch]
            dy = kwargs_analytic['dy'][epoch]
            alpha = kwargs_analytic['alpha'][epoch]

        f = jnp.zeros_like(kwargs_background['h'].reshape((self.image_size_up, self.image_size_up)))

        if self.M != 0:
            f += self.scale * self.shifted_gaussians(c_x, c_y, a, source_ID=source_ID)
            f = rotate_array(f, alpha)
            f = translate_array(f, self._upsampling_factor * dx, self._upsampling_factor * dy)

        return f

    def setUpsamplingFactor(self, upsampling_factor):
        """
        Sets the upsampling factor.

        :param upsampling_factor: the proportion by which the sampling rate increases with respect to the input image
        :type upsampling_factor: int

        """
        self._upsampling_factor = upsampling_factor

        # down sample operator from utils: will need a vectorized version.
        self.DownsampleAllEpochs = vmap(lambda array: Downsample(array, upsampling_factor),
                                        in_axes=(0,))

    @partial(jit, static_argnums=(0,))
    def modelstack_scan(self, pars):
        # unused. keeping for a while just in case.
        # lax.scan function works as: carry, output = f(carry, input)
        # make f below: (we'll use a decoy for carry as we are not using it.)
        one_epoch = lambda pair: self.one_epoch(pair[0], pair[1])
        # pair is (psf, params)
        f = lambda carry, x: (None, one_epoch(x))
        # scan(f, init_carry, params)
        return scan(f, None, (self.psf, pars))[1]

    @partial(jit, static_argnums=(0,))
    def modelstack_forloop(self, pars, h):
        """
        Creates a model for all the epochs with shape (epoch, image_size_up, image_size_up) by looping over the epochs.
        This is slightly faster for a low number of epochs (~1 to 5) than using a vectorized version of ``self.one_epoch``.

        :param pars: stack of arrays of parameters for one epoch. Shape (epoch, N), where N is the number of parameters
                     per epoch (see the docstring of ``self.one_epoch``)
        :param h: 1D array containing the pixelated background. Separated from `pars` because does not vary between epochs.

        :return: 2D array of shape (epoch, image_size_up, image_size_up)

        """
        return jnp.array([self.one_epoch(self.psf[i], pars[i], h) for i in range(self.epochs)])

    @partial(jit, static_argnums=(0,))
    def modelstack(self, pars, h):
        """
        Creates a model for all the epochs with shape (epoch, image_size_up, image_size_up) by vectorizing ``self.one_epoch``.
        Much faster for a large number of epochs (> 10), regime where the ``self.modelstack_forloop`` version cannot be jit'ed anymore.

        :param pars: stack of arrays of parameters for one epoch. Shape (epoch, N), where N is the number of parameters per epoch (see the docstring of ``self.one_epoch``)
        :param h: 1D array containing the pixelated background. Separated from `pars` because does not vary between epochs.

        :return: 2D array of shape (epoch, image_size_up, image_size_up)

        """

        # vmap magic to vectorize our one_epoch method:
        h_fixed = partial(self.one_epoch, h=h)  # with the background fixed in the function, since always the same.
        broadcast = vmap(h_fixed, in_axes=(0, 0))
        # here we specify `in_axes`: vectorize over the first axis of the
        # array of PSFs, and over the first axis of the array of parameters.
        # by the way:
        # - array of PSFs: stack of 2D slices
        # - array of parameters: stack of 1D slices, each containing the parameters
        #                        for one epoch.

        return broadcast(self.psf, pars)

    @partial(jit, static_argnums=(0,))
    def model(self, kwargs):
        """
        Creates the 2D deconvolution model image.

        :param kwargs: dictionary containing the parameters of the model.
        :return: 3D array - A stack of 2D images (one layer per epoch)

        """

        # part 1: unpack the keywords and put them in a giant 2D array:
        an = deepcopy(kwargs['kwargs_analytic'])
        back = self._get_background(kwargs)
        mean = kwargs['kwargs_background']['mean']

        # a bit messy here, we manually unpack each keyword.
        # the ParameterDeconv class should be taking care of this,
        # but we don't have access to it in this class in the way
        # things are set up right now.
        # TODO

        # vectorized unpacking for insane performance bro
        row1 = jnp.tile(jnp.hstack([an[key] for key in ['c_x', 'c_y']]), (self.epochs, 1))
        i_values = jnp.arange(self.epochs)[:, None]
        multiplier = i_values * self.M
        indices = jnp.arange(self.M) + multiplier  # generates a 2D array of indices
        row2 = an['a'][indices.flatten()].reshape(self.epochs, self.M)  # Flatten indices and reshape results

        row3 = an['dx'].reshape(self.epochs, 1)
        row4 = an['dy'].reshape(self.epochs, 1)
        row5 = an['alpha'].reshape(self.epochs, 1)
        epochmean = mean[i_values]
        # nice 2D array, containing Nepochs 1D arrays of all params.
        args = jnp.hstack([row1, row2, row3, row4, row5, epochmean])

        # part 2, pass the giant 2D array to the model function:
        modelupscale = self._model(args, back)
        # this generates a model on the upscaled grid.

        # Now we down sample. Each new pixel is the average of all the
        # small pixels that composed it before.
        model = self.DownsampleAllEpochs(modelupscale)

        # to conserve the surface brightness:
        model = model * ((self.image_size_up ** 2) / (self.image_size ** 2))

        return model

    def dump(self, path, kwargs, data=None, sigma_2=None, save_output_level=4, format='hdf5'):
        """
        Stores the model in a given file in pickle or hdf5 format (recommended).

        :param path: Filename of the output.
        :param kwargs: Dictionary containing the fitted value of the model
        :param data: (Nepoch x image_size x image_size) array containing the data
        :param sigma_2: (Nepoch x image_size x image_size) array containing the noise maps
        :param save_output_level: Int. Level of output product to save: 1-just the parameters of the model, 2- add the input data, 3- add the output products (background, and pts source channel) 4- add the output products for every image.
        """

        if format == 'pkl':
            with open(path, 'wb') as f:
                pkl.dump([self, kwargs, data, sigma_2], f, protocol=pkl.HIGHEST_PROTOCOL)
        elif format == 'hdf5':
            kwargs_model = {
                'image_size': int(self.image_size),
                'number_of_sources': int(self.M),
                'scale': float(self.scale),
                'upsampling_factor': int(self._upsampling_factor),
                'epochs': int(self.epochs),
                'psf': np.asarray(self.psf).tolist(),
                'gaussian_fwhm': int(self.gaussian_fwhm),
                'N_sersic': int(self.N_sersic),
                'convolution_method': str(self.convolution_method),
            }
            with h5py.File(path, 'w') as f:
                dset = f.create_dataset("kwargs_options", data=json.dumps(kwargs_model))
                dset = f.create_dataset("kwargs_Deconv", data=json.dumps(convert_numpy_array_to_list(kwargs)))

                if save_output_level >= 2:
                    if data is not None:
                        dset = f.create_dataset("Data", data=data)
                    if sigma_2 is not None:
                        dset = f.create_dataset("Sigma2", data=sigma_2)

                if save_output_level >= 3:
                    h = self._get_background(kwargs).reshape(self.image_size_up, self.image_size_up)
                    pts_source_mean = self.getPts_source(kwargs, epoch=None)
                    dset = f.create_dataset("Background", data=h)
                    dset = f.create_dataset("Point source mean", data=pts_source_mean)

                if save_output_level >= 4:
                    models = np.zeros((self.epochs, self.image_size, self.image_size))
                    residuals = np.zeros((self.epochs, self.image_size, self.image_size))
                    deconvolutions = np.zeros((self.epochs, self.image_size_up, self.image_size_up))
                    for i in range(self.epochs):
                        output = self.model(kwargs)[i]
                        deconv, h = self.getDeconvolved(kwargs, i)
                        d = data[i, :, :]
                        dif = d - output

                        models[i, :, :] = output  # low resolution model
                        residuals[i, :, :] = dif
                        deconvolutions[i, :, :] = deconv  # high resolution model

                    dset = f.create_dataset("Models cube", data=models)
                    dset = f.create_dataset("Residuals cube", data=residuals)
                    dset = f.create_dataset("deconvolution cube", data=deconvolutions)

        else:
            raise NotImplementedError(f'Unrecognized format {format}. Choose between pkl and hdf5.')

    def export(self, output_folder, kwargs_final, data, sigma_2, epoch=None, norm=1, format='fits', header=None):
        """
        Saves all the output files.

        :param output_folder: path to the output folder
        :type output_folder: str
        :param kwargs_final: dictionary containing all keyword arguments
        :param data: array containing the images
        :param sigma_2: array containing the noise maps
        :param epoch: integer or array or list containing the indices of the epoch to export. None, for exporting all epochs.
        :param norm: normalisation, to have the outputs in the correct unit
        :param format: output format. Choose between ``npy`` or ``fits``
        :type format: str
        :param header: HDU header, as return by astropy.io.fits (optional). This is used to propagate the WCS coordinate to the outputfiles
        """

        if format == 'fits':
            save_fct = save_fits
        elif format == 'npy':
            save_fct = save_npy
        else:
            raise NotImplementedError(f'Format {format} unknown.')

        if epoch is None:
            print('Exporting all epochs')
            epoch_arr = np.arange(self.epochs)
        elif not hasattr(epoch, "__len__"):
            epoch_arr = np.array([epoch])
        else:
            epoch_arr = np.array(epoch)

        high_res_header = deepcopy(header)
        if header is not None:
            # change the WCS coordinate for the high resolution output images
            for k in ['CDELT1', 'CDELT2']:
                if k in high_res_header.keys():
                    high_res_header[k] = header[k] / self._upsampling_factor
            for k in ['CRPIX1', 'CRPIX2']:
                if k in high_res_header.keys():
                    high_res_header[k] = header[k] * self._upsampling_factor

        for i, e in enumerate(epoch_arr):
            output = self.model(kwargs_final)[e] * norm
            deconv, _ = self.getDeconvolved(kwargs_final, e)
            deconv *= norm
            data_show = data[e, :, :] * norm
            dif = data_show - output
            rr = dif / np.sqrt(sigma_2[e, :, :] * norm ** 2)

            save_fct(data_show, os.path.join(output_folder, 'data_{0:05d}'.format(i)), header=header)
            save_fct(output, os.path.join(output_folder, 'model_{0:05d}'.format(i)), header=header)
            save_fct(dif, os.path.join(output_folder, 'residuals_{0:05d}'.format(i)), header=header)
            save_fct(rr, os.path.join(output_folder, 'scaled_residuals_{0:05d}'.format(i)), header=header)
            save_fct(deconv, os.path.join(output_folder, 'deconvolution_{0:05d}'.format(i)), header=high_res_header)

        h = self._get_background(kwargs_final).reshape(self.image_size_up, self.image_size_up) * norm
        save_fct(h, os.path.join(output_folder, 'background_model'), header=high_res_header)

    def flux_at_epoch(self, kwargs, epoch=0):
        """
        Return an array containing the flux of the point sources at epoch `epoch`.

        :param kwargs: dictionary containing all keyword arguments
        :param epoch: index of the epoch
        """
        a = kwargs['kwargs_analytic']['a'][self.M * epoch:self.M * (epoch + 1)] * self.scale

        return a

    def get_mask_pts_source(self, kwargs, mask_size=3, nan_mask=False):
        """
        Return an array containing a mask of size 'mask_size' around the point sources. Output array is at the
        sub-sampled resolution.

        :param kwargs: dictionary containing all keyword arguments
        :param mask_size: size of the mask around the point sources. In "small" pixel.
        :param nan_mask: If true, return a mask where 0. have been replaced by nan

        """

        x0 = jnp.floor(kwargs['kwargs_analytic'][
                           'c_x'] * self._upsampling_factor + self.image_size_up / 2. - mask_size / 2.).astype(
            int)
        y0 = jnp.floor(kwargs['kwargs_analytic'][
                           'c_y'] * self._upsampling_factor + self.image_size_up / 2. - mask_size / 2.).astype(
            int)

        masks_pts_source = jnp.ones((self.image_size_up, self.image_size_up))

        for i in range(self.M):
            if nan_mask:
                replacement = jnp.nan * jnp.ones((mask_size, mask_size))
                masks_pts_source = dynamic_update_slice(masks_pts_source, replacement,
                                                        (y0[i], x0[i]))  # inverted indices
            else:
                replacement = jnp.zeros((mask_size, mask_size))
                masks_pts_source = dynamic_update_slice(masks_pts_source, replacement,
                                                        (y0[i], x0[i]))  # inverted indices

        return masks_pts_source

    def mean_pts_amps(self, a):
        """
        Return the mean amplitude per points source, over all epoch. Return a 1D vector of size self.M.

        :param a: amplitude vector, correspond to kwargs['kwargs_analytic']['a']
        """
        mean_amp = a.reshape(self.epochs, self.M)
        return jnp.mean(mean_amp, axis=0)

    def background_interpolate(self, kwargs, interpolation_order=0, inner_mask_size=3, outer_mask_size=7):
        """
        Return an interpolated version of the background, interpolated below the point sources.

        :param kwargs: dictionary containing all keyword arguments
        :param interpolation_order: order of the interpolation. For now, only 0 is available. It will take the mean of the pixel in the outer mask.
        :param inner_mask_size: size of the region to interpolate
        :param outer_mask_size: size of the outer mask used for the interpolation

        """
        assert outer_mask_size > inner_mask_size, "Outer mask should be bigger than the inner mask!"

        interp_back = deepcopy(kwargs['kwargs_background']['h']).reshape(self.image_size_up,
                                                                         self.image_size_up)

        x0_inner = jnp.floor(kwargs['kwargs_analytic'][
                                 'c_x'] * self._upsampling_factor + self.image_size_up / 2. - inner_mask_size / 2.).astype(
            int)
        y0_inner = jnp.floor(kwargs['kwargs_analytic'][
                                 'c_y'] * self._upsampling_factor + self.image_size_up / 2. - inner_mask_size / 2.).astype(
            int)
        x0_outer = jnp.floor(kwargs['kwargs_analytic'][
                                 'c_x'] * self._upsampling_factor + self.image_size_up / 2. - outer_mask_size / 2.).astype(
            int)
        y0_outer = jnp.floor(kwargs['kwargs_analytic'][
                                 'c_y'] * self._upsampling_factor + self.image_size_up / 2. - outer_mask_size / 2.).astype(
            int)

        if interpolation_order == 0:
            for i in range(self.M):
                # get the outer mask
                outerslice = dynamic_slice(interp_back, (y0_outer[i], x0_outer[i]), (outer_mask_size, outer_mask_size))
                replacement = jnp.nan * jnp.ones((outer_mask_size - 2, outer_mask_size - 2))
                masked_outerslice = dynamic_update_slice(outerslice, replacement,
                                                         (1, 1))

                # compute the mean in the outer ring around pts sources
                mean_outer_ring = jnp.nanmean(masked_outerslice)

                # replace the inner mask by the interpolated value
                replacement = jnp.ones((inner_mask_size, inner_mask_size)) * mean_outer_ring
                interp_back = dynamic_update_slice(interp_back, replacement,
                                                   (y0_inner[i], x0_inner[i]))  # inverted indices
        else:
            raise NotImplementedError('Higher order interpolation not implemented yet in JAX.')

        return interp_back, masked_outerslice, replacement


def setup_model(data, sigma_2, s, xs, ys, subsampling_factor, initial_a=None, astrometric_bound=None,
                dithering_bound=None, convolution_method='scipy', N_sersic=0, rotate=False):
    """
    Utility setting up a deconvolution model. The returned dictionaries of
    parameters can later be adjusted by the user.

    :param data: 3D array containing the images, one per epoch. shape (epochs, im_size, im_size)
    :param sigma_2: 3D array containing the noisemaps, one per epoch. shape (epochs, im_size, im_size)
    :param s: 3D array containing the narrow PSFs, one per epoch. shape (epochs, im_size_up, im_size_up) where im_size_up needs be a multiple of im_size.
    :param xs: 1D array or list containing the x positions of the point sources. For M point sources, len(xs) is M. In units of big pixel.
    :param ys: 1D array or list containing the y positions of the point sources. For M point sources, len(ys) is M. In units of big pixel.
    :param initial_a: list containing the amplitudes of the point sources. For M point sources and N epochs, len(initial_a) is M*N. If none, amplitudes are applied scaled by the maax of each epoch.
    :param subsampling_factor: integer, ratio of the size of the data pixels to that of the PSF pixels.
    :param astrometric_bound: integer, maximum shift of the point sources, relative to the initial position. None: no upper nor lower limit
    :param dithering_bound: integer, maximum shift from image to image. None: no upper nor lower limit
    :param convolution_method: 'scipy', 'fft', or 'lax'. To be passed to the Deconv class. Recommended : 'scipy'.
    :param N_sersic: Number of sersic profile to add to the background in addition to the pixelated grid (Default: 0)
    :param rotate: bool, if true, takes rotation between epochs into account. If false, alpha gets fixed.

    :return: a tuple: (a starred.deconvolution.Deconv instance,
                       a dictionary with the initial values of the model parameters,
                       a dictionary with the upper boundaries of the model parameters,
                       a dictionary with the lower boundaries of the model parameters,
                       a dictionary with the fixed parameters of the model)
    """
    # xs and ys, let's make them numpy arrays cuz it's easier
    xs = np.array(xs)
    ys = np.array(ys)
    M = xs.size  # number of point sources
    epochs = data.shape[0]
    N_sersic = int(N_sersic)

    if initial_a is None:
        initial_a = 6 * np.array([np.nanmax(data[i, :, :]) for i in range(epochs) for j in range(M)])

    if not xs.size == ys.size:
        message = "Your xs or ys (refering to amplitudes and positions of your point sources)"
        message += " arguments need be the of the same length!\n"
        message += f"But we have size(xs)={xs.size}, size(ys)={ys.size}"
        raise RuntimeError(message)

    if not int(len(initial_a) / epochs) == xs.size:
        message = "Your initial amplitudes does not match the number of point sources and epochs."
        message += f" initial amplitudes must have length N_point_source * N_epochs = {M * epochs}.\n"
        message += f"But we have size(initial_a)={len(initial_a)}"
        raise RuntimeError(message)

    if not sigma_2.shape == data.shape:
        message = "The shape of your data and noisemaps is not what we expect."
        message += " They need be of shape ~ (epochs, some nx, some ny).\n"
        message += f"But we have shape(data)={data.shape}, shape(sigma_2)={sigma_2.shape}."
        raise RuntimeError(message)

    if not epochs == sigma_2.shape[0] == s.shape[0]:
        message = "The number of epochs in your data, noisemaps or PSFs do not match\n"
        message += f"We have shape(data)={data.shape}, shape(sigma_2)={sigma_2.shape}, shape(s)={s.shape}\n"
        message += "We expected the first dimension of each (# of epochs) to be the same."
        raise RuntimeError(message)

    im_size = data[0].shape[0]
    im_size_up = im_size * subsampling_factor
    if astrometric_bound is None:
        astrometric_bound = im_size / 2.
    if dithering_bound is None:
        dithering_bound = im_size / 2.

    # Parameter initialization
    initial_c_x = xs
    initial_c_y = ys
    # intensity per point:
    scale = np.nanmax(data)
    initial_a /= scale
    # initial background:
    initial_h = np.zeros((im_size_up ** 2))
    # dictionary containing the parameters of deconvolution.
    # (The translations dx, dy are set to zero for the first epoch.
    # Thus we only initialize (epochs-1) of them.)
    kwargs_init = {
        'kwargs_analytic': {
            'c_x': initial_c_x,  # point sources positions
            'c_y': initial_c_y,
            'dx': np.ravel([0. for _ in range(epochs)]),  # translation per epoch
            'dy': np.ravel([0. for _ in range(epochs)]),
            'alpha': np.ravel([0. for _ in range(epochs)]),  # rotation per epoch
            'a': initial_a},  # amplitudes of point sources
        'kwargs_background': {'h': initial_h,  # background
                              'mean': np.ravel([0. for _ in range(epochs)])},
        # additive constant for background per epoch
        'kwargs_sersic': {'amp': [0. for _ in range(N_sersic)],
                          'R_sersic': [1. for _ in range(N_sersic)],
                          'n_sersic': [1. for _ in range(N_sersic)],
                          'center_x': [0. for _ in range(N_sersic)],
                          'center_y': [0. for _ in range(N_sersic)],
                          'e1': [0. for _ in range(N_sersic)],
                          'e2': [0. for _ in range(N_sersic)],
                          }
    }
    # same as above, providing fixed parameters:
    kwargs_fixed = {
        'kwargs_analytic': {},
        'kwargs_background': {},
        'kwargs_sersic': {},
    }

    # fix alpha, if rotate=False
    if not rotate:
        kwargs_fixed['kwargs_analytic']['alpha'] = kwargs_init['kwargs_analytic']['alpha']

    if epochs == 1:
        # we fix image translation
        kwargs_fixed['kwargs_analytic']['dx'] = [0.]
        kwargs_fixed['kwargs_analytic']['dy'] = [0.]

    # boundaries.
    kwargs_up = {
        'kwargs_analytic': {'c_x': list(initial_c_x + astrometric_bound),
                            'c_y': list(initial_c_y + astrometric_bound),
                            'dx': [dithering_bound for _ in range(epochs)],
                            'dy': [dithering_bound for _ in range(epochs)],
                            'alpha': [np.pi for _ in range(epochs)],
                            'a': list([np.inf for i in range(M * epochs)])
                            },
        'kwargs_background': {'h': list([np.inf for i in range(0, im_size_up ** 2)]),
                              'mean': [np.inf for _ in range(epochs)]
                              },
        'kwargs_sersic': {'amp': [np.inf for _ in range(N_sersic)],
                          'R_sersic': [100. for _ in range(N_sersic)],
                          'n_sersic': [8. for _ in range(N_sersic)],
                          'center_x': [im_size_up for _ in range(N_sersic)],
                          'center_y': [im_size_up for _ in range(N_sersic)],
                          'e1': [0.5 for _ in range(N_sersic)],
                          'e2': [0.5 for _ in range(N_sersic)],
                          },
    }
    kwargs_down = {
        'kwargs_analytic': {'c_x': list(initial_c_x - astrometric_bound),
                            'c_y': list(initial_c_y - astrometric_bound),
                            'dx': [-dithering_bound for _ in range(epochs)],
                            'dy': [-dithering_bound for _ in range(epochs)],
                            'alpha': [-np.pi for _ in range(epochs)],
                            'a': list([0 for i in range(M * epochs)])},
        'kwargs_background': {'h': list([-np.inf for i in range(0, im_size_up ** 2)]),
                              'mean': [-np.inf for _ in range(epochs)]
                              },
        'kwargs_sersic': {'amp': [0. for _ in range(N_sersic)],
                          'R_sersic': [0. for _ in range(N_sersic)],
                          'n_sersic': [0.5 for _ in range(N_sersic)],
                          'center_x': [-im_size_up for _ in range(N_sersic)],
                          'center_y': [-im_size_up for _ in range(N_sersic)],
                          'e1': [-0.5 for _ in range(N_sersic)],
                          'e2': [-0.5 for _ in range(N_sersic)],
                          },
    }
    # Initializing the model
    model = Deconv(image_size=im_size,
                   number_of_sources=M,
                   scale=scale,
                   upsampling_factor=subsampling_factor,
                   epochs=epochs,
                   psf=s,
                   convolution_method=convolution_method,
                   N_sersic=N_sersic)

    # returning model and kwargs.
    return model, kwargs_init, kwargs_up, kwargs_down, kwargs_fixed


def load_Deconv_model(input_file, format='hdf5'):
    """ Load Deconv model class from hdf5 or pickle file"""

    if format == 'pkl':
        with open(input_file, 'rb') as f:
            model, kwargs, data, sigma_2 = pkl.load(f)

    elif format == 'hdf5':
        with h5py.File(input_file, 'r') as f:
            kwargs_model = json.loads(f['kwargs_options'][()])
            kwargs_model['psf'] = np.asarray(kwargs_model['psf'])  # convert back the list to np.array
            model = Deconv(**kwargs_model)
            kwargs = json.loads(f['kwargs_Deconv'][()])
            kwargs = convert_list_to_numpy_array(kwargs)

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

    else:
        raise NotImplementedError(f'Unrecognized format {format}. Choose between pkl and hdf5.')

    return model, kwargs, data, sigma_2
