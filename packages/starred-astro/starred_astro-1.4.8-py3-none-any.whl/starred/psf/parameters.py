import jax.numpy as jnp
import numpy as np

from starred.utils.parameters import Parameters

__all__ = ['ParametersPSF']


class ParametersPSF(Parameters):
    """
    Point Spread Function parameters class.

    """
    param_names_moffat = ['fwhm_x', 'fwhm_y', 'phi', 'beta', 'C']
    param_names_background = ['background', 'mean']
    param_names_gaussian = ['a', 'x0', 'y0']
    param_names_distortion = ['dilation_x', 'dilation_y', 'shear']

    def __init__(self, kwargs_init, kwargs_fixed, kwargs_up=None, kwargs_down=None, include_moffat=True):
        """
        :param kwargs_init: dictionary with information on the initial values of the parameters
        :param kwargs_fixed: dictionary containing the fixed parameters 
        :param kwargs_up: dictionary with information on the upper bounds of the parameters 
        :param kwargs_down: dictionary with information on the lower bounds of the parameters 

        """
        super(ParametersPSF, self).__init__(kwargs_init, kwargs_fixed, kwargs_up=kwargs_up,
                                            kwargs_down=kwargs_down)

        # we'll guess the number of sources, etc. based on the provided kwargs
        self.M = len(kwargs_init['kwargs_gaussian']['x0'])  # number of sources, one per provided image
        self.background_param_number = len(kwargs_init['kwargs_background']['background'])
        # ah, and ...since we're making a strong distinction between elliptical or standard moffat, we'll
        # remove the extra params if we're not dealing with an elliptical moffat. However, in the future
        # we should change the parametrization to remove the need for this distinction:
        # can always fix the params of the elliptical to have a circular one.
        # TODO
        if not ('phi' in kwargs_init['kwargs_moffat']):
            self.param_names_moffat = ['fwhm', 'beta', 'C']

        if not include_moffat:
            self.param_names_moffat = []
            self._kwargs_init['kwargs_moffat'] = {}
            self._kwargs_fixed['kwargs_moffat'] = {}
            self._kwargs_up['kwargs_moffat'] = {}
            self._kwargs_down['kwargs_moffat'] = {}

        self._update_arrays()

    def args2kwargs(self, args):
        """Obtain a dictionary of keyword arguments from positional arguments."""
        i = 0
        kwargs_moffat, i = self._get_params(args, i, 'kwargs_moffat')
        kwargs_gaussian, i = self._get_params(args, i, 'kwargs_gaussian')
        kwargs_background, i = self._get_params(args, i, 'kwargs_background')
        kwargs_distortion, i = self._get_params(args, i, 'kwargs_distortion')
        # wrap-up
        kwargs = {'kwargs_moffat': kwargs_moffat, 'kwargs_gaussian': kwargs_gaussian,
                  'kwargs_background': kwargs_background, 'kwargs_distortion': kwargs_distortion}

        return kwargs

    def kwargs2args(self, kwargs):
        """Obtain an array of positional arguments from a dictionary of keyword arguments."""
        args = self._set_params(kwargs, 'kwargs_moffat')
        args += self._set_params(kwargs, 'kwargs_gaussian')
        args += self._set_params(kwargs, 'kwargs_background')
        args += self._set_params(kwargs, 'kwargs_distortion')
        return jnp.array(args)

    def get_param_names_for_model(self, kwargs_key):
        """Returns the names of the parameters according to the key provided."""
        if kwargs_key == 'kwargs_moffat':
            return self.param_names_moffat
        elif kwargs_key == 'kwargs_gaussian':
            return self.param_names_gaussian
        elif kwargs_key == 'kwargs_background':
            return self.param_names_background
        elif kwargs_key == 'kwargs_distortion':
            return self.param_names_distortion
        else:
            raise KeyError(f'`{kwargs_key}` is not in the kwargs')

    def _get_params(self, args, i, kwargs_key):
        """Getting the parameters."""
        kwargs = {}
        kwargs_fixed_k = self._kwargs_fixed[kwargs_key]
        param_names = self.get_param_names_for_model(kwargs_key)
        for name in param_names:
            if name not in kwargs_fixed_k.keys():
                if name == 'background':
                    num_param = self.background_param_number
                elif name == 'mean':
                    num_param = self.M
                elif name == 'a':
                    num_param = self.M
                elif name == 'x0' or name == 'y0':
                    num_param = self.M
                elif name in ['dilation_x', 'dilation_y', 'shear']:
                    num_param = 2  # 2d order 2 polynomial without constant term
                else:
                    num_param = 1
                kwargs[name] = args[i:i + num_param]
                i += num_param
            else:
                kwargs[name] = kwargs_fixed_k[name]
                free_ind = self._kwargs_free_indices[kwargs_key][name]
                if len(free_ind) > 0:
                    num_param = len(free_ind)
                    kwargs[name] = kwargs[name].at[free_ind].set(args[i:i+num_param])
                    i += num_param

        return kwargs, i

    def get_all_free_param_names(self, kwargs):
        args = self._param_names(kwargs, 'kwargs_moffat')
        args += self._param_names(kwargs, 'kwargs_gaussian')
        args += self._param_names(kwargs, 'kwargs_background')
        args += self._param_names(kwargs, 'kwargs_distortion')
        return args
