import numpy as np
from starred.utils.generic_utils import gaussian_function, make_grid
from scipy import fftpack
import matplotlib.pyplot as plt
import copy
import scipy

def revert_psf(psf):
    sizex,sizey = np.shape(psf)
    # psf_t = np.fft.fft(psf)
    psf = shifted_gaussians(sigma_x=3, sigma_y=3, gaussian_size=sizex, subgrid_res=1)
    g = shifted_gaussians(sigma_x=2, sigma_y=2, gaussian_size=sizex, subgrid_res=1)
    psf_fft = fftpack.fftshift(fftpack.fftn(psf))
    psf_back = np.real(fftpack.ifftn(fftpack.ifftshift(psf_fft)))

    g_fft = fftpack.fftshift(fftpack.fftn(g))
    g_back = np.real(fftpack.ifftn(fftpack.ifftshift(g_fft)))

    s = fftpack.fftshift(fftpack.ifftn(fftpack.ifftshift(psf_fft/g_fft)))

    plt.imshow(np.real(s))
    plt.show()
    exit()
    # g_t = np.fft.fft(g)
    # s = np.fft.ifft(psf_t / g_t)
    return np.real(s), g


def shifted_gaussians(sigma_x=2, sigma_y=2, gaussian_size=30,subgrid_res=1):
    x, y = make_grid(numPix=gaussian_size, deltapix=1 , subgrid_res=subgrid_res)
    gaussian =np.array(gaussian_function(
        x=x, y=y,
        amp=1, sigma_x=sigma_x,
        sigma_y=sigma_y,
        center_x=0.,
        center_y=0.,
    ))

    return gaussian.reshape(gaussian_size,gaussian_size)

def cut_translate_psf(kernel, show = False):

    PSF_shifted = scipy.ndimage.shift(copy.deepcopy(kernel), (0.5,0.5), output=None, order=1, mode='nearest')[1:,1:]

    if show:
        plt.imshow(PSF_shifted)
        plt.show()

    return PSF_shifted