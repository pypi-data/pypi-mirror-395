from time import time

import jax.numpy as jnp
import jax.scipy.signal
import numpy as np
from astropy.io import fits
from jax import lax, jit
from jax.numpy.fft import fft2, ifft2
from functools import partial
from copy import deepcopy
import scipy.ndimage


def timer_func(func):
    """
    This function shows the execution time of the provided function object.

    """

    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func

@partial(jit, static_argnums=(2,))
def pad_and_convolve(x, y, padding=True):
    """
    Lax convolution is performed after an optional padding.

    :param x: first array 
    :param y: second array 
    :param padding: padding
    :type padding: bool

    :return: output array

    """
    x = x.reshape(1, x.shape[0], x.shape[1], 1)
    y = y.reshape(y.shape[0], y.shape[1], 1, 1)

    if padding:
        x = jnp.pad(x, ((0, 0), (4, 4), (4, 4), (0, 0)), mode='wrap')

    dimension_numbers = ('NHWC', 'HWIO', 'NHWC')
    dn = lax.conv_dimension_numbers(x.shape, y.shape, dimension_numbers)

    output = lax.conv_general_dilated(x, y, (1, 1), 'SAME', (1, 1), (1, 1), dn)
    if padding:
        return output[0, 4:-4, 4:-4, 0]
    else:
        return output[0, :, :, 0]


@partial(jit, static_argnums=(2,))
def pad_and_convolve_fft(x, y, padding=True):
    """
    FFT (Fast Fourier Transform) convolution is performed after an optional padding.

    :param x: first array 
    :param y: second array 
    :param padding: padding
    :type padding: bool

    :return: Output array

    """
    if padding:
        x = jnp.pad(x, ((4, 4), (4, 4)), constant_values=0.)
        y = jnp.pad(y, ((4, 4), (4, 4)), constant_values=0.)

    output = fft_convolve2d(x, y)
    if padding:
        return output[4:-4, 4:-4]
    else:
        return output

@jit
def fft_convolve2d(x, y):
    """ 
    2D convolution using the Fast Fourier Transform (FFT).

    :param x: first 2D array
    :param y: second 2D array

    :return: 2D array 

    """
    fr = fft2(x)
    fr2 = fft2(jnp.flipud(jnp.fliplr(y)))
    m, n = fr.shape
    cc = jnp.real(ifft2(fr * fr2))
    cc = jnp.roll(cc, int(-m / 2), axis=0)
    cc = jnp.roll(cc, int(-n / 2), axis=1)
    return cc


def fourier_division(a, b):
    """
    Divides two arrays in Fourier space. Work much better with even kernel.
    To obtain the narrow PSF, a should be the full PSF and b a gaussian with 2pix FWHM.
    This function makes use of scipy if the kernel are even, and is not yet jaxified

    :param a: first array
    :param b: second array
    """
    assert a.shape == b.shape, "Arrays must have the same shape."
    assert a.shape[0] == a.shape[1], "Array must be square."

    padding = False  # array must have odd number of pixel
    if a.shape[0] % 2 == 0:
        a = jnp.pad(a, ((0, 1), (0, 1)), mode='constant')
        b = jnp.pad(b, ((0, 1), (0, 1)), mode='constant')
        padding = True

    A = fft2(a)
    B = fft2(b)
    C = A / B
    cc = jnp.real(ifft2(C))
    m, n = C.shape
    cc = jnp.roll(cc, int(-m / 2) - 1, axis=0)
    cc = jnp.roll(cc, int(-n / 2) - 1, axis=1)

    if padding:
        # todo: jaxified that if jax.scipy.ndimage.shift is available one day
        cc = scipy.ndimage.shift(cc, (-0.5, -0.5))[:-1, :-1]

    return cc


@jit
def scipy_convolve(data, kernel):
    """
    FFT-based Scipy convolution.

    :param data: first array 
    :param kernel: second array

    :return: output array

    """
    return jax.scipy.signal.convolve(data, kernel, mode='same', method='fft')

@jit
def gaussian_function(x, y, amp, sigma_x, sigma_y, center_x, center_y):
    """
    :param x: 1D array of x positions
    :param y: 1D array of y positions
    :param amp: the amplitude coefficient
    :type amp: float
    :param sigma_x: x-spread of the Gaussian blob
    :type sigma_x: float
    :param sigma_y: y-spread of the Gaussian blob
    :type sigma_y: float
    :param center_x: x position of the center
    :type center_x: float
    :param center_y: y position of the center
    :type center_y: float

    :return: 2D Gaussian

    """
    c = 1 / jnp.sqrt((2 * np.pi * sigma_x * sigma_y))
    delta_x = jnp.subtract(x, center_x)
    delta_y = jnp.subtract(y, center_y)
    exponent = -((delta_x / sigma_x) ** 2 + (delta_y / sigma_y) ** 2) / 2.
    g = c * jnp.exp(exponent)
    g /= g.sum()
    return amp * g


# we'll use this one to vectorize the PSF models
def gaussian_function_batched(x, y, amp, sigma_x, sigma_y, center_x, center_y):
    """
    adjusted gaussian_function to accept and process batches for center_x and center_y.
    amp, sigma_x, sigma_y can also be vectors.
    but won't be needed in starred, as we scale the PSF at the moffat step.

    x and y: 2d arrays of coordinates made by make_grid and reshaped.

    """
    c = 1 / jnp.sqrt((2 * jnp.pi * sigma_x * sigma_y))
    # adding slice dimension to x and y, adding data dimension to center_x and center_y
    delta_x = x[None, :] - center_x[:, None]
    delta_y = y[None, :] - center_y[:, None]
    exponent = -((delta_x / sigma_x) ** 2 + (delta_y / sigma_y) ** 2) / 2.
    g = c * jnp.exp(exponent)
    g /= g.sum(axis=(1,))[:, None]  # normalize over x and y dimensions
    return amp[:, None] * g

def make_grid(numPix, deltapix, subgrid_res=1):
    """
    Creates pixel grid as 1D arrays of x and y positions.
    The default coordinate frame is such that (0,0) is at the center of the coordinate grid.

    :param numPix: number of pixels per axis. Provide an integer for a square grid
    :param deltapix: pixel size
    :param subgrid_res: sub-pixel resolution 
    :return: x and y position information given as two 1D arrays

    """

    numPix = [numPix, numPix]

    # Super-resolution sampling
    # numPix_eff = int(numPix * subgrid_res)
    numPix_eff = [int(n * subgrid_res) for n in numPix]
    deltapix_eff = deltapix / float(subgrid_res)

    # Compute unshifted grids.
    # X values change quickly, Y values are repeated many times
    # NOTE jax.numpy.tile checks if `reps` is of type int, but numpy.int64
    #      is not in fact this type. Simply casting as int(numPix_eff[1])
    #      causes problems elsewhere with jax tracing, so we use another approach
    # x_grid = np.tile(np.arange(numPix_eff[0]), numPix_eff[1]) * deltapix_eff
    # y_grid = np.repeat(np.arange(numPix_eff[1]), numPix_eff[0]) * deltapix_eff
    x_space = jnp.arange(numPix_eff[0]) * deltapix_eff
    y_space = jnp.arange(numPix_eff[1]) * deltapix_eff
    x_grid, y_grid = jnp.meshgrid(x_space, y_space)
    x_grid, y_grid = x_grid.flatten(), y_grid.flatten()

    # Shift so (0, 0) is centered
    shift = jnp.array([deltapix_eff * (n - 1) / 2 for n in numPix_eff])

    return x_grid - shift[0], y_grid - shift[1]

@jit
def fwhm2sigma(fwhm):
    """
    Converts the FWHM (Full Width at Half Maximum) to the Gaussian sigma.

    :param fwhm: the full width at half maximum value
    :type fwhm: float
    :return: Gaussian standard deviation, `i.e.`, sqrt(var)

    """
    sigma = fwhm / (2 * jnp.sqrt(2 * jnp.log(2)))
    return sigma

@jit
def moffat_function(x, y, amp, fwhm, beta, center_x, center_y):
    """
    :param x: 1D array of x positions
    :param y: 1D array of y positions
    :param amp: the amplitude coefficient
    :type amp: float
    :param fwhm: the full width at half maximum value
    :type fwhm: float
    :param beta: the Moffat beta parameter
    :type beta: float
    :param center_x: x position of the center
    :type center_x: float
    :param center_y: y position of the center
    :type center_y: float

    :return: 2D Moffat
    
    """
    r0 = fwhm / (2. * jnp.sqrt(2. ** (1. / beta) - 1.))
    delta_x = jnp.subtract(x, center_x)
    delta_y = jnp.subtract(y, center_y)
    rr_gg = (delta_x / r0) ** 2 + (delta_y / r0) ** 2
    return amp * (1 + rr_gg) ** (-beta)


@jit
def moffat_elliptical_function(x, y, amp, fwhm_x, fwhm_y, phi, beta, center_x, center_y):
    """
    :param x: 1D array of x positions
    :param y: 1D array of y positions
    :param amp: the amplitude coefficient
    :type amp: float
    :param fwhm_x: the full width at half maximum value in the x direction
    :type fwhm_x: float
    :param fwhm_y: the full width at half maximum value in the y direction
    :type fwhm_y: float
    :param phi: orientation angle
    :type phi: float
    :param beta: the Moffat beta parameter
    :type beta: float
    :param center_x: x position of the center
    :type center_x: float
    :param center_y: y position of the center
    :type center_y: float

    :return: 2D Elliptical Moffat

    """
    r0_x = fwhm_x / (2. * jnp.sqrt(2. ** (1. / beta) - 1.))
    r0_y = fwhm_y / (2. * jnp.sqrt(2. ** (1. / beta) - 1.))
    delta_x = jnp.subtract(x, center_x)
    delta_y = jnp.subtract(y, center_y)
    A = (jnp.cos(phi) / r0_x)**2  + (jnp.sin(phi) / r0_y)**2
    B = (jnp.sin(phi) / r0_x)**2  + (jnp.cos(phi) / r0_y)**2
    C = 2*jnp.sin(phi)*jnp.cos(phi)*(1./ r0_x**2 - 1/r0_y**2)
    rr_gg = A*(delta_x ** 2) + B * (delta_y ** 2) + C * delta_x * delta_y
    return amp * (1 + rr_gg) ** (-beta)

def twoD_Gaussian(x,y, amplitude, xo, yo, sigma_x, sigma_y, theta):
    """
    Analytical 2D Gaussian function

    :param x: array containing x-axis variable
    :param y: array containing y-axis variable
    :param amplitude: amplitude of the Gaussian
    :param xo: center x coordinate
    :param yo: center y coordinate
    :param sigma_x: standard deviation of x variable
    :param sigma_y: standard deviation of y variable
    :param theta: ellongation angle
    """
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo)
                            + c*((y-yo)**2)))
    return g


def save_fits(array, path, header=None):
    """ 
    Saves ``.fits`` file of an array to a specified ``path``.
    
    """
    hdu = fits.PrimaryHDU(array, header=header)
    hdu.writeto(path + '.fits', overwrite=True)


def save_npy(array, path, header=None):
    """
    Saves ``.npy`` file of an array to a specified ``path``. Header is not used in this format.

    """
    np.save(path + '.npy', array)

def Downsample(image, factor=1, conserve_flux = False):
    """
    Resizes an image from dimensions (nx, ny) to (nx/factor, ny/factor).

    :param image: 2D array with shape (nx, ny)
    :param factor: downsampling factor, which must be greater than or equal to 1
    :type factor: int

    :return: 2D array

    """
    if factor == 1:
        return image
    if factor < 1:
        raise ValueError('scaling factor in re-sizing %s < 1' % factor)
    f = int(factor)
    nx, ny = np.shape(image)
    if int(nx / f) == nx / f and int(ny / f) == ny / f:
        small = image.reshape([int(nx / f), f, int(ny / f), f]).mean(3).mean(1)
        if conserve_flux:
            return small * f**2
        else:
            return small
    else:
        raise ValueError("scaling with factor %s is not possible with grid size %s, %s" % (f, nx, ny))


def Upsample(image, factor=1):
    """
    Resizes an image without interpolation.

    :param image: 2D array with shape (nx, ny)
    :param factor: upsampling factor, which must be greater than or equal to 1
    :type factor: int

    :return: 2D array

    """
    if factor == 1:
        return image
    if factor < 1:
        raise ValueError('scaling factor in re-sizing %s < 1' % factor)
    f = int(factor)
    n1, n2 = image.shape
    upimage = np.zeros((n1 * f, n2 * f))
    x, y = np.where(upimage == 0)
    x_, y_ = (x / f).astype(int), (y / f).astype(int)
    upimage[x, y] = image[x_, y_] / f ** 2
    return upimage


def convert_numpy_array_to_list(kwargs):
    new_dic = {}
    for k in kwargs.keys():
        dic_temp = {}
        for j in kwargs[k].keys():
            dic_temp[j] = deepcopy(np.asarray(kwargs[k][j]).tolist())
        new_dic[k] = deepcopy(dic_temp)

    return new_dic


def convert_list_to_numpy_array(kwargs):
    new_dic = {}
    for k in kwargs.keys():
        dic_temp = {}
        for j in kwargs[k].keys():
            if isinstance(kwargs[k][j], list):
                dic_temp[j] = deepcopy(np.asarray(kwargs[k][j]))
            else:
                dic_temp[j] = deepcopy(kwargs[k][j])
        new_dic[k] = deepcopy(dic_temp)

    return new_dic
