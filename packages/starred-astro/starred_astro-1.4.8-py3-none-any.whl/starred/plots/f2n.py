#  
# Copyright (C) 2012-2020 Euclid Science Ground Segment      
#    
# This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General    
# Public License as published by the Free Software Foundation; either version 3.0 of the License, or (at your option)    
# any later version.    
#    
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied    
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more    
# details.    
#    
# You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to    
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA    
#

""" 
File: sky_image_plot.py
Created on: Sep 3, 2017
Author: Malte Tewes
This file is a standalone Euclid-agnostic module to visualize and plot sky images with matplotlib.
To visualize Euclid objects, use the wrappers in she_image_checkplot.py
"""

import matplotlib
import numpy as np
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable


class SkyImage(object):
    """Holds a pixel array
    
    Todo : use properties for z1 z2 !
    """

    def __init__(self, data, z1=None, z2=None):
        """
        
        """

        self.data = data
        self.extent = get_extent(self.data)
        self.z1 = z1
        self.z2 = z2
        self.set_z(z1, z2)

    @property
    def shape(self):  # Just a shortcut
        """The shape (width, height) of the image"""
        return self.data.shape

    def __str__(self):
        return "SkyImage{}[{}:{}]".format(self.shape, self.z1, self.z2)

    def set_z(self, z1=None, z2=None):

        if z1 is None:
            self.z1 = np.min(self.data)
        else:
            self.z1 = z1
        if z2 is None:
            self.z2 = np.max(self.data)
        else:
            self.z2 = z2

        autolist = ["Auto", "auto"]
        if (self.z1 in autolist) or (self.z2 in autolist):
            self.set_auto_z_scale()

    def set_auto_z_scale(self, full_sample_limit=10000, nsig=5.0):
        """Automatic z-scale determination"""

        stata = self.data[:]

        std = stdmad(stata)
        med = np.median(stata)

        nearskypixvals = stata[np.logical_and(stata > med - 2 * std, stata < med + 2 * std)]
        if len(nearskypixvals) > 0:
            skylevel = np.median(nearskypixvals)
        else:
            skylevel = med

        self.z1 = skylevel - nsig * std
        self.z2 = np.max(stata)


def draw_sky_image(ax, si, **kwargs):
    """Use imshow to draw a SkyImage to some axes
    
    """
    # "origin":"lower" as well as the tranpose() within the imshow arguments both combined give the right orientation
    imshow_kwargs = {"aspect": "equal", "origin": "lower", "interpolation": "nearest",
                     "cmap": matplotlib.pyplot.get_cmap('Greys_r')}
    imshow_kwargs.update(kwargs)
    ax.grid(False)
    ax.set_axis_off()
    im = ax.imshow(si.data.transpose(), extent=si.extent,
                   norm=colors.SymLogNorm(np.abs(si.z1 + 5 * stdmad(si.data[:])), vmin=si.z1 + 5 * stdmad(si.data[:]),
                                          vmax=si.z2), **imshow_kwargs)

    return im


def annotate(ax, cat, x="x", y="y", text="Hello", **kwargs):
    """Annotates the positions (x, y) from a catalog
    
    """

    annotate_kwargs = {"horizontalalignment": "left", "verticalalignment": "top", "color": "red",
                       "xytext": (0, 0), "textcoords": 'offset points'}
    annotate_kwargs.update(**kwargs)

    for row in cat:

        # We skip silently any masked positions
        if getattr(row[x], "mask", False) or getattr(row[y], "mask", False):
            continue

        rowtext = text.format(row=row)
        ax.annotate(rowtext,
                    xy=(row[x], row[y]),
                    **annotate_kwargs
                    )


def get_extent(a):
    """Defines the extent with which to plot an array a (we use the numpy convention)
    
    """
    return (0, a.shape[0], 0, a.shape[1])


def stdmad(a):
    """MAD rescaled to std of normally distributed data"""
    med = np.median(a)
    return 1.4826 * np.median(np.abs(a - med))


def spplot(i, array, fig, title):
    ax = fig.add_subplot(2, 3, i)
    si = SkyImage(np.transpose(array), z1="Auto", z2="Auto")
    im = draw_sky_image(ax, si)
    cat = [{"x": 1.0, "y": array.shape[0] - 1.0, "text": "top left"}]
    annotate(ax, cat, text=title, color="white", fontfamily='sans-serif')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im, cax=cax, orientation='vertical')
