from copy import deepcopy

import jax.numpy as jnp
import numpy as np

__all__ = ['Parameters']


class Parameters(object):
    """
    Parameters class.

    """

    def __init__(self, kwargs_init, kwargs_fixed, kwargs_up=None, kwargs_down=None):
        """
        :param kwargs_init: dictionary with information on the initial values of the parameters
        :param kwargs_fixed: dictionary containing the fixed parameters 
        :param kwargs_up: dictionary with information on the upper bounds of the parameters 
        :param kwargs_down: dictionary with information on the lower bounds of the parameters 

        """
        self._kwargs_init = self.convert_in_jnp_array(kwargs_init)
        self._kwargs_fixed = self.convert_in_jnp_array(kwargs_fixed)
        if kwargs_up is not None:
            self._kwargs_up = self.convert_in_jnp_array(kwargs_up)
        else:
            self._kwargs_up = None
        if kwargs_down is not None:
            self._kwargs_down = self.convert_in_jnp_array(kwargs_down)
        else:
            self._kwargs_down = None
        self._kwargs_free_indices = self.get_nan_indices()
        
        # update the bounds in case we only have sub parts of our parameter-arrays
        # that are free:
        uku, ukd = self._update_bounds(self._kwargs_init, self._kwargs_fixed, self._kwargs_up, self._kwargs_down)
        self._kwargs_up = uku
        self._kwargs_down = ukd
            

    @property
    def optimized(self):
        """Checks whether a function is optimized."""
        return hasattr(self, '_map_values')

    def convert_in_jnp_array(self, kwargs):
        new_kwargs = {}
        for key in kwargs.keys():
            new_kwargs[key] = {}
            for key2 in kwargs[key].keys():
                new_kwargs[key][key2] = jnp.asarray(deepcopy(kwargs[key][key2]))

        return new_kwargs

    def initial_values(self, as_kwargs=False, copy=False):
        """Returns the initial values of the parameters."""
        if as_kwargs:
            return deepcopy(self._kwargs_init) if copy else self._kwargs_init
        else:
            return deepcopy(self._init_values) if copy else self._init_values

    def current_values(self, as_kwargs=False, restart=False, copy=False):
        """Returns the current values of the parameters."""
        if restart is True or not self.optimized:
            return self.initial_values(as_kwargs=as_kwargs, copy=copy)
        return self.best_fit_values(as_kwargs=as_kwargs, copy=copy)

    def best_fit_values(self, as_kwargs=False, copy=False):
        """Maximum-a-postriori estimate."""
        if as_kwargs:
            return deepcopy(self._kwargs_map) if copy else self._kwargs_map
        else:
            return deepcopy(self._map_values) if copy else self._map_values

    def set_best_fit(self, args):
        """Sets the maximum-a-postriori estimate as the parameter values."""
        self._map_values = args
        self._kwargs_map = self.args2kwargs(self._map_values)

    def _update_arrays(self):
        self._init_values = self.kwargs2args(self._kwargs_init)
        self._kwargs_init = self.args2kwargs(self._init_values)  # for updating missing fields
        self._num_params = len(self._init_values)
        if self.optimized:
            self._map_values = self.kwargs2args(self._kwargs_map)

    def _set_params(self, kwargs, kwargs_key):
        """Setting the parameters."""
        args = []
        kwargs_profile = kwargs[kwargs_key]
        kwargs_fixed_k = self._kwargs_fixed[kwargs_key]
        param_names = self.get_param_names_for_model(kwargs_key)
        for name in param_names:
            if name not in kwargs_fixed_k:
                if isinstance(kwargs_profile[name], list):
                    args += kwargs_profile[name]
                elif isinstance(kwargs_profile[name], (np.ndarray, np.generic, jnp.ndarray, jnp.generic)):
                    el = kwargs_profile[name].tolist()
                    if hasattr(el, '__len__'):
                        args += el
                    else:
                        args += [el]
                else:
                    args += [kwargs_profile[name]]
            else:
                # add the indices in the self._kwargs_free_indices
                free_ind = self._kwargs_free_indices[kwargs_key][name]
                if len(free_ind) >= 1:
                    args += kwargs_profile[name][free_ind].tolist()
        return args
    
    @staticmethod
    def _update_bounds(kwargs_init, kwargs_fixed, kwargs_up, kwargs_down):
        """
        Called during initialization of this class.
        Updates the bounds (kwargs_up and kwargs_down) based on the fixed parameters (kwargs_fixed).
        NaN values in kwargs_fixed represent parameters that are still free to be optimized.
        The function adjusts the bounds to include only the indices where there are NaN values in kwargs_fixed.
    
        :param kwargs_init: Initial parameters
        :param kwargs_fixed: Fixed parameters, with NaN for values that are still optimized
        :param kwargs_up: Upper bounds for parameters
        :param kwargs_down: Lower bounds for parameters
        :return: Updated kwargs_up and kwargs_down
        """
        for main_key in kwargs_fixed:
            for sub_key in kwargs_fixed[main_key]:
                fixed_values = np.array(kwargs_fixed[main_key][sub_key])  # Ensuring it's a numpy array
                if isinstance(fixed_values, np.ndarray):
                    nan_indices = np.isnan(fixed_values)
                    if np.any(nan_indices):
                        if kwargs_up is not None:
                            if not np.sum(nan_indices) == len(
                                    kwargs_up[main_key][sub_key]):  # check if the kwargs have already been updated
                                kwargs_up[main_key][sub_key] = np.array(kwargs_up[main_key][sub_key])[nan_indices]
                        if kwargs_down is not None:
                            if not np.sum(nan_indices) == len(
                                    kwargs_down[main_key][sub_key]):  # check if the kwargs have already been updated
                                kwargs_down[main_key][sub_key] = np.array(kwargs_down[main_key][sub_key])[nan_indices]
        return kwargs_up, kwargs_down

    def get_bounds(self):
        """Returns the upper and lower bounds of the parameters."""
        if self._kwargs_up is None or self._kwargs_down is None:
            return None
        else:
            list_down_limit = []
            list_up_limit = []
            for kwargs_key in self._kwargs_down.keys():
                param_names = self.get_param_names_for_model(kwargs_key)
                for name in param_names:
                    if not name in self._kwargs_fixed[kwargs_key].keys():
                        assert name in self._kwargs_up[kwargs_key].keys(), \
                            "Missing '%s' key in the kwargs_up['%s']" % (name, kwargs_key)
                        assert name in self._kwargs_down[
                            kwargs_key].keys(), "Missing '%s' key in the kwargs_down['%s']" % (name, kwargs_key)
                        up = self._kwargs_up[kwargs_key][name]
                        down = self._kwargs_down[kwargs_key][name]

                    else:
                        # even if key in fixed, maybe we have nans - meaning
                        # a subset is not fixed.
                        free = self._kwargs_free_indices[kwargs_key][name]
                        if len(free) == 0:
                            continue
                        up = self._kwargs_up[kwargs_key][name]
                        down = self._kwargs_down[kwargs_key][name]
                        
                    if isinstance(down, list):
                        list_down_limit += down
                    elif isinstance(down, (np.ndarray, jnp.ndarray)):
                        el = down.tolist()
                        if hasattr(el, '__len__'):
                            list_down_limit += el
                        else:
                            list_down_limit += [el]
                    else:
                        list_down_limit += [self._kwargs_down[kwargs_key][name]]
                    if isinstance(up, list):
                        list_up_limit += up
                    elif isinstance(up, (np.ndarray, jnp.ndarray)):
                        el = up.tolist()
                        if hasattr(el, '__len__'):
                            list_up_limit += el
                        else:
                            list_up_limit += [el]
                    else:
                        list_up_limit += [self._kwargs_up[kwargs_key][name]]
                        

            return (jnp.array(list_down_limit).flatten(),
                    jnp.array(list_up_limit).flatten())

    def update_kwargs(self, kwargs_init=None, kwargs_fixed=None, kwargs_up=None,
                      kwargs_down=None):

        """Updates the kwargs with provided values."""
        if kwargs_init is not None:
            self._kwargs_init = kwargs_init
        if kwargs_fixed is not None:
            self._kwargs_fixed = kwargs_fixed
            self._kwargs_free_indices = self.get_nan_indices()
        if kwargs_init is not None:
            self._kwargs_up = kwargs_up
        if kwargs_init is not None:
            self._kwargs_down = kwargs_down

    def _param_names(self, kwargs, kwargs_key):
        """Setting the parameters."""
        names = []
        kwargs_profile = kwargs[kwargs_key]
        kwargs_fixed_k = self._kwargs_fixed[kwargs_key]
        param_names = self.get_param_names_for_model(kwargs_key)

        for name in param_names:
            if name not in kwargs_fixed_k:
                value = kwargs_profile[name]
                if isinstance(value, (float, int)):
                    names.append(name)
                elif len(value) == 1 and isinstance(value, (list, np.ndarray, np.generic, jnp.ndarray, jnp.generic)):
                    names.append(name)
                elif isinstance(value, (list, np.ndarray, np.generic, jnp.ndarray, jnp.generic)):
                    names += [f'{name}_{i}' for i in range(len(value))]
                else:
                    names.append(name)
            else:
                num_free_param = len(self._kwargs_free_indices[kwargs_key][name])
                if num_free_param == 1:
                    names.append(f'{name}_{self._kwargs_free_indices[kwargs_key][name]}')
                else:
                    names += [f'{name}_{i}' for i in self._kwargs_free_indices[kwargs_key][name]]

        return names

    def get_nan_indices(self):
        kwargs_indice_free = {}
        for kwargs_key in self._kwargs_fixed.keys():
            kwargs_indice_free[kwargs_key] = {}
            for key in self._kwargs_fixed[kwargs_key]:
                indices = jnp.where(jnp.isnan(self._kwargs_fixed[kwargs_key][key]))[0]
                kwargs_indice_free[kwargs_key][key] = indices

        return kwargs_indice_free


