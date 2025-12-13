import jax.numpy as jnp
import numpy as np

from starred.utils.parameters import Parameters

__all__ = ['ParametersDeconv']


class ParametersDeconv(Parameters):
    """
    Deconvolution parameters class.

    """
    param_names_analytic = ['a', 'c_x', 'c_y', 'dx', 'dy', 'alpha']
    param_names_background = ['mean', 'h']
    param_names_sersic = ['amp', 'R_sersic', 'n_sersic', 'center_x', 'center_y', 'e1', 'e2']

    def __init__(self, kwargs_init, kwargs_fixed, kwargs_up=None, kwargs_down=None):
        """
        :param kwargs_init: dictionary with information on the initial values of the parameters
        :param kwargs_fixed: dictionary containing the fixed parameters 
        :param kwargs_up: dictionary with information on the upper bounds of the parameters 
        :param kwargs_down: dictionary with information on the lower bounds of the parameters 

        """
        super(ParametersDeconv, self).__init__(kwargs_init, kwargs_fixed, kwargs_up=kwargs_up,
                                               kwargs_down=kwargs_down)

        # we'll guess the number of epochs, etc. based on the provided kwargs
        self.epochs = len(kwargs_init['kwargs_analytic']['dx'])
        self.M = len(kwargs_init['kwargs_analytic']['c_x'])
        self.N_sersic = len(kwargs_init['kwargs_sersic']['amp'])
        self.background_param_number = len(kwargs_init['kwargs_background']['h'])

        self._update_arrays()

    def args2kwargs(self, args):
        """Obtain a dictionary of keyword arguments from positional arguments."""
        i = 0
        kwargs_analytic, i = self._get_params(args, i, 'kwargs_analytic')
        kwargs_background, i = self._get_params(args, i, 'kwargs_background')
        kwargs_sersic, i = self._get_params(args, i, 'kwargs_sersic')
        # wrap-up
        kwargs = {'kwargs_analytic': kwargs_analytic, 'kwargs_background': kwargs_background,
                  'kwargs_sersic': kwargs_sersic}
        return kwargs

    def kwargs2args(self, kwargs):
        """Obtain an array of positional arguments from a dictionary of keyword arguments."""
        args = self._set_params(kwargs, 'kwargs_analytic')
        args += self._set_params(kwargs, 'kwargs_background')
        args += self._set_params(kwargs, 'kwargs_sersic')
        return jnp.array(args)

    def get_param_names_for_model(self, kwargs_key):
        """Returns the names of the parameters according to the key provided."""
        if kwargs_key == 'kwargs_analytic':
            return self.param_names_analytic
        elif kwargs_key == 'kwargs_sersic':
            return self.param_names_sersic
        return self.param_names_background

    def _get_params(self, args, i, kwargs_key):
        """Getting the parameters."""
        kwargs = {}
        kwargs_fixed_k = self._kwargs_fixed[kwargs_key]
        param_names = self.get_param_names_for_model(kwargs_key)
        for name in param_names:
            if not name in kwargs_fixed_k:
                if name == 'a':
                    num_param = self.M * self.epochs
                elif name == 'h':
                    num_param = self.background_param_number
                elif name == 'mean':
                    num_param = self.epochs
                elif name == 'dx' or name == 'dy' or name == 'alpha':
                    num_param = self.epochs
                elif name == 'c_x' or name == 'c_y':
                    num_param = self.M
                elif name in self.param_names_sersic:
                    num_param = self.N_sersic
                else:
                    raise NameError(f"The ParametersDeconv class does not know about this parameter: {name}.")
                kwargs[name] = args[i:i + num_param]
                i += num_param

            else:
                kwargs[name] = kwargs_fixed_k[name]
                free_ind = self._kwargs_free_indices[kwargs_key][name]
                if len(free_ind) > 0:
                    num_param = len(free_ind)
                    kwargs[name] = jnp.array(kwargs[name]).at[free_ind].set(args[i:i + num_param])
                    i += num_param

        return kwargs, i

    def get_all_free_param_names(self, kwargs):
        args = self._param_names(kwargs, 'kwargs_analytic')
        args += self._param_names(kwargs, 'kwargs_background')
        args += self._param_names(kwargs, 'kwargs_sersic')
        return args

