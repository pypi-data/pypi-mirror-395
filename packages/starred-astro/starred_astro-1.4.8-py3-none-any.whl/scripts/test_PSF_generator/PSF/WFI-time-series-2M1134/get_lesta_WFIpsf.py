import numpy as np 
import os
import glob

dir = '/projects/astro/cosmograil/REDUC/run/2M1134_WFI/psf_abhino'
outdir = '/home/astro/millon/Desktop/PSF_WFI_temp'

folders = sorted(glob.glob(os.path.join(dir, '1_*')))
print(len(folders))

for fol in folders:
    basename = fol.split('/')[-1]

    psf = os.path.join(fol, 'results', 'psf_1.fits' )
    dest = os.path.join(outdir, basename + '_psf.fits')

    os.system('cp %s %s'%(psf, dest))
    print('cp %s %s'%(psf, dest))
