from functools import partial

import jax.numpy as jnp
from jax import jit, vmap
from jax.lax import conv_general_dilated, conv_dimension_numbers


class WaveletTransform(object):
    """
    Class that handles wavelet transform using JAX, using the 'a trous' algorithm.

    :param nscales: number of scales in the decomposition
    :type nscales: int
    :param wavelet_type: family of wavelets (Starlets are the only ones compatible for now)
    :type wavelet_type: str

    """

    def __init__(self, nscales, wavelet_type='starlet'):
        self._n_scales = nscales
        if wavelet_type == 'starlet':
            self._h = jnp.array([1, 4, 6, 4, 1]) / 16.
            self._fac = 2
        elif wavelet_type == 'starlet-gen2':
            raise NotImplementedError("Second generation starlet transform not yet implemented")
        else:
            raise ValueError(f"'{wavelet_type}' starlet transform is not supported")

    @property
    def scale_norms(self):
        if not hasattr(self, '_norms'):
            npix_dirac = 2 ** (self._n_scales + 2)
            dirac = jnp.diag((jnp.arange(npix_dirac) == int(npix_dirac / 2)).astype(float))
            wt_dirac = self.decompose(dirac)
            self._norms = jnp.sqrt(jnp.sum(wt_dirac ** 2, axis=(1, 2,)))
        return self._norms

    @partial(jit, static_argnums=(0,))
    def convolveSeparableSimple(self, kernel1D, image2D):  # pragma: no cover
        """
        Convolves a 2D array a 1D kernel. It assumes ``imaged2D`` was padded (using valid mode in convolution).

        :param kernel1D: 1D array of length L such that ``kernel2D`` is the result of the convolution between ``kernel1D`` and itself
        :param image2D: padded 2D array of shape (S1, S2)

        :return: 2D filtered array of shape (S1-L+1, S2-L+1)

        """
        sizex, sizey = image2D.shape

        # assumes a padded image2D!!
        myconv = lambda x, y: jnp.convolve(x, y, mode='valid')

        # batch filter of the rows
        convbroadcastx = vmap(myconv, in_axes=(0, 0))
        # and of the columns
        convbroadcasty = vmap(myconv, in_axes=(1, 0))

        # in both cases, we need a stack of the filter for the vectorization:
        hbroadx = jnp.repeat(kernel1D[jnp.newaxis, :], sizex, axis=0)
        # after the x convolution, the y dimension is reduced:
        newsizey = sizey - kernel1D.size + 1
        hbroady = jnp.repeat(kernel1D[jnp.newaxis, :], newsizey, axis=0)

        # now we can filter the image:
        filtered = convbroadcastx(image2D, hbroadx)
        filtered = convbroadcasty(filtered, hbroady)

        return filtered

    @partial(jit, static_argnums=(0, 3))
    def convolveSeparableDilated(self, image2D, kernel1D, dilation=1):
        """
        Convolves an image contained in ``image2D`` with the 1D kernel ``kernel1D``. The operation is 
        blured2D = image2D * (kernel1D ∧ kernel1D), where ∧ is a wedge product, here a tensor product. 

        :param kernel1D: 1D array to convolve the image with
        :param image2D: 2D array 
        :param dilation:  makes the spacial extent of the kernel bigger. The default is 1.

        :return: 2D array

        """

        # Preparations
        image = jnp.expand_dims(image2D, (2,))
        # shape (Nx, Ny, 1) -- (N, W, C)
        # we treat the Nx as the batch number!! (because it is a 1D convolution 
        # over the rows)
        kernel = jnp.expand_dims(kernel1D, (0, 2,))
        # here we have kernel shape ~(I,W,O)

        # so: 
        # (Nbatch, Width, Channel) * (Inputdim, Widthkernel, Outputdim) 
        #                                            -> (Nbatch, Width, Channel)
        # where Nbatch is our number of rows.
        dimension_numbers = ('NWC', 'IWO', 'NWC')
        dn = conv_dimension_numbers(image.shape,
                                    kernel.shape,
                                    dimension_numbers)
        # with these conv_general_dilated knows how to handle the different
        # axes:
        rowblur = conv_general_dilated(image, kernel,
                                       window_strides=(1,),
                                       padding='SAME',
                                       rhs_dilation=(dilation,),
                                       dimension_numbers=dn)

        # now we do the same for the columns, hence this time we have
        # (Height, Nbatch, Channel) * (Inputdim, Widthkernel, Outputdim) 
        #                                            -> (Height, Nbatch, Channel)
        # where Nbatch is our number of columns.
        dimension_numbers = ('HNC', 'IHO', 'HNC')
        dn = conv_dimension_numbers(image.shape,
                                    kernel.shape,
                                    dimension_numbers)

        rowcolblur = conv_general_dilated(rowblur, kernel,
                                          window_strides=(1,),
                                          padding='SAME',
                                          rhs_dilation=(dilation,),
                                          dimension_numbers=dn)

        return rowcolblur[:, :, 0]

    @partial(jit, static_argnums=(0,))
    def decompose(self, image):
        """Decomposes an image into a chosen wavelet basis."""
        # Validate input
        assert self._n_scales >= 0, "nscales must be a non-negative integer"
        if self._n_scales == 0:
            return image

        # Preparations
        image = jnp.copy(image)
        kernel = self._h.copy()

        # Compute the first scale:
        c1 = self.convolveSeparableDilated(image, kernel)
        # Wavelet coefficients:
        w0 = (image - c1)
        result = jnp.expand_dims(w0, 0)
        cj = c1

        # Compute the remaining scales
        # at each scale, the kernel becomes larger ( a trou ) using the
        # dilation argument in the jax wrapper for convolution.
        for step in range(1, self._n_scales):
            cj1 = self.convolveSeparableDilated(cj, kernel, dilation=2 ** step)
            # wavelet coefficients
            wj = (cj - cj1)
            result = jnp.concatenate((result, jnp.expand_dims(wj, 0)), axis=0)
            cj = cj1

        # Append final coarse scale
        result = jnp.concatenate((result, jnp.expand_dims(cj, axis=0)), axis=0)
        return result

    @partial(jit, static_argnums=(0,))
    def decompose_legacy(self, image):  # pragma: no cover
        """Decomposes an image into the chosen wavelet basis.
        This is a legacy implementation which does not use the separability of the
        starlet transform.
        To be re-used if we one day introduce
        non-separable wavelets.
        """
        # Validate input
        assert self._n_scales >= 0, "nscales must be a non-negative integer"
        if self._n_scales == 0:
            return image

        # Preparations
        image = jnp.expand_dims(image, (0, 3))
        kernel = jnp.expand_dims(jnp.outer(self._h, self._h), (2, 3))
        dimension_numbers = ('NHWC', 'HWIO', 'NHWC')
        dn = conv_dimension_numbers(image.shape, kernel.shape, dimension_numbers)

        # Compute the first scale
        c0 = image
        padded = jnp.pad(c0, ((0, 0), (self._fac, self._fac), (self._fac, self._fac), (0, 0)), mode='edge')
        c1 = conv_general_dilated(padded, kernel,
                                  window_strides=(1, 1),
                                  padding='VALID',
                                  rhs_dilation=(1, 1),
                                  dimension_numbers=dn)
        w0 = (c0 - c1)[0, :, :, 0]  # Wavelet coefficients
        result = jnp.expand_dims(w0, 0)
        cj = c1

        # Compute the remaining scales
        for ii in range(1, self._n_scales):
            b = self._fac ** (ii + 1)  # padding pixels
            padded = jnp.pad(cj, ((0, 0), (b, b), (b, b), (0, 0)), mode='edge')
            cj1 = conv_general_dilated(padded, kernel,
                                       window_strides=(1, 1),
                                       padding='VALID',
                                       rhs_dilation=(self._fac ** ii, self._fac ** ii),
                                       dimension_numbers=dn)
            # wavelet coefficients
            wj = (cj - cj1)[0, :, :, 0]
            result = jnp.concatenate((result, jnp.expand_dims(wj, 0)), axis=0)
            cj = cj1

        # Append final coarse scale
        result = jnp.concatenate((result, cj[:, :, :, 0]), axis=0)
        return result

    @partial(jit, static_argnums=(0,))
    def reconstruct(self, coeffs):
        """Reconstructs an image from wavelet decomposition coefficients."""
        return jnp.sum(coeffs, axis=0)
