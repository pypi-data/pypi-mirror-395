import os
import sys

import numpy as np
from astropy.wcs import WCS

"""
A set of functions to interact with ds9 region

"""


def export_astrometry_as_ds9region(model_deconv, outputfolder, kwargs, header=None, regsize=0.02):
    """"
    Export your final results as a DS9 readable region.

    :param model_deconv: starred.deconvolution.Deconv object.
    :param outputfolder: Path to the output folder.
    :param kwargs: dictionary containing the parameters of the model
    :param header: header of the fits file of the first epoch of the data, must contains WCS coordinate. If None, it will be exported in pixel image coordinate.
    :param regsize: Region size, in arcsecond or in pixel if the header is not provided.

    """
    final_cx = kwargs['kwargs_analytic']['c_x']
    final_cy = kwargs['kwargs_analytic']['c_y']

    if header is not None:
        wcs = WCS(header=header)
        radec_out = wcs.pixel_to_world(
            final_cx + model_deconv.image_size / 2.,
            final_cy + model_deconv.image_size / 2.)

        with open(os.path.join(outputfolder, 'point_sources_astrometry.reg'), 'w') as f:
            f.write(
                f'# Region file format: DS9 version 4.1 global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source={model_deconv.M} \nfk5 \n')
            for i in range(model_deconv.M):
                stri = radec_out.to_string('hmsdms', sep=':')[i].replace(' ', ',')
                f.write(f'circle({stri},{regsize}") \n')

    else:
        with open(os.path.join(outputfolder, 'point_sources_astrometry.reg'), 'w') as f:
            f.write(
                f'# Region file format: DS9 version 4.1 global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source={model_deconv.M} \nimage \n')
            for i in range(model_deconv.M):
                x = final_cx[i] + model_deconv.image_size / 2. + 0.5
                y = final_cy[i] + model_deconv.image_size / 2. + 0.5  # To match half pixel indexing of ds9
                f.write(f'circle({x}, {y}, {regsize}) \n')
