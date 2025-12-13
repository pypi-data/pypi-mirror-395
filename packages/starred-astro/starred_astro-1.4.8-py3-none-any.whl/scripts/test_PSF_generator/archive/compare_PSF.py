import numpy as np
from astropy.io import fits
import os
import time
import matplotlib.pyplot as plt
import numpy as np

SNR = [1000]
instrument = ['WFI']
PSF_path = './PSF'
mock_path = './mock_stars'
for inst in instrument:
    for SN in SNR:
        true_PSF_path = os.path.join(PSF_path, 'psf_%s.fits'%inst)
        true_PSF = fits.open(true_PSF_path)[0].data

        rec_PSF_path = os.path.join(mock_path, inst, 'SNR_%2.f'%SN, 'output', 'psf.fits')
        rec_PSF = fits.open(rec_PSF_path)[0].data

        fig, axs = plt.subplots(1, 3, figsize=(8,4))
        axs[0].imshow(true_PSF, origin='lower')
        axs[1].imshow(rec_PSF, origin='lower')
        axs[2].imshow((true_PSF - rec_PSF), origin='lower')
        plt.show()

        rms_res = np.std(true_PSF - rec_PSF)
        print('RMS residuals :', rms_res)

        nx, ny = np.shape(true_PSF)
        cx, cy = int(nx/2), int(ny/2)
        rms_res_100 = np.std(true_PSF[cx-10:cx+10, cy-10:cy+10 ] - rec_PSF[cx-10:cx+10, cy-10:cy+10 ])
        med_error = np.median(np.abs(true_PSF[cx-10:cx+10, cy-10:cy+10 ] - rec_PSF[cx-10:cx+10, cy-10:cy+10 ])
                               / true_PSF[cx-10:cx+10, cy-10:cy+10])
        print('RMS residuals 100 inner pixels :', rms_res_100)
        print('Median error on 100 inner pixels :', med_error)