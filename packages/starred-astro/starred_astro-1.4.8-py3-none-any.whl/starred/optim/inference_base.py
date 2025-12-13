from functools import partial

from jax import jit, grad, jacfwd, jacrev, jvp, value_and_grad
import jax.numpy as jnp
import numpy as np

__all__ = ['InferenceBase', 'FisherCovariance']


class InferenceBase(object):
    """Class that defines wraps the loss function, and computes first and second order derivatives.
    
    :param loss_class: Loss instance
    :param param_class: Parameters instance
    """

    def __init__(self, loss_class, param_class):
        self._loss = loss_class
        self._param = param_class

    @property
    def parameters(self):
        """Returns the parameters."""
        return self._param

    # @partial(jit, static_argnums=(0,))
    def loss(self, args):
        """
        Loss function to be minimized.
        :param args: list or array of paramers
        """
        return self._loss(args)

    def log_likelihood(self, args):
        """
        Log Likelihood function to be maximised.
        :param args: list or array of paramers
        """
        return -self._loss(args)

    # @partial(jit, static_argnums=(0,))
    def gradient(self, args):
        """Returns the gradient (first derivative) of the loss function."""
        return grad(self.loss)(args)

    # @partial(jit, static_argnums=(0,))
    def value_and_gradient(self, args):
        """Returns both the value and the gradient (first derivative) of the loss function."""
        return value_and_grad(self.loss)(args)

    # @partial(jit, static_argnums=(0,))
    def hessian(self, args):
        """Returns the Hessian (second derivative) of the loss function."""
        return jacfwd(jacrev(self.loss))(args)

    # @partial(jit, static_argnums=(0,))
    def hessian_vec_prod(self, args, vec):
        """Hessian-vector product."""
        # forward-over-reverse (https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html#hessian-vector-products-using-both-forward-and-reverse-mode)
        return jvp(grad(self.loss), (args,), (vec,))[1]


# Estimation of the parameter covariance matrix via the Fisher information
# Class copied and modified from Herculens
# Copyright (c) 2022, herculens developers and contributors, Aymeric Galan for this class

class FisherCovariance(object):

    def __init__(self, parameter_class, differentiable_class, diagonal_only=False):
        """
            :param diagonal_only: bool, if you are confident your parameters are not correlated: you can
                                  save space by calculating the diagonal of the hessian only.
        """

        self._param = parameter_class
        self._diff = differentiable_class
        self.diagonal_only = diagonal_only

    @property
    def fisher_matrix(self):
        if not hasattr(self, '_fim'):
            raise ValueError("Call first compute_fisher_information().")
        return self._fim

    @property
    def covariance_matrix(self):
        if not hasattr(self, '_cov'):
            self._cov = self.fisher2covar(self.fisher_matrix, inversion='full')
        return self._cov

    def get_kwargs_sigma(self):
        """
        Return the standard deviation of the marginalized distribution for each parameter. This corresponds to the
        square roots of the diagonal coefficient of the covariance matrix.
        """
        if self.diagonal_only:
            sigma_values = jnp.sqrt(jnp.abs(self.covariance_matrix))
        else:
            sigma_values = jnp.sqrt(jnp.abs(jnp.diag(self.covariance_matrix)))
        kwargs_sigma = self._param.args2kwargs(sigma_values)
        #Set sigma to 0 for the fixed parameters
        for key in kwargs_sigma.keys():
            kwargs_fixed_k = self._param._kwargs_fixed[key]
            for key2 in kwargs_sigma[key].keys():
                if key2 in kwargs_fixed_k:
                    if isinstance(kwargs_sigma[key][key2], (list, np.ndarray, np.generic)):
                        for i in range(len(kwargs_sigma[key][key2])):
                            if i not in self._param._kwargs_free_indices[key][key2]:
                                kwargs_sigma[key][key2][i] = 0.
                    elif isinstance(kwargs_sigma[key][key2], (jnp.ndarray, jnp.generic)):
                        for i in range(len(kwargs_sigma[key][key2])):
                            if i not in self._param._kwargs_free_indices[key][key2]:
                                kwargs_sigma[key][key2] = kwargs_sigma[key][key2].at[i].set(0.)
                    else :
                        kwargs_sigma[key][key2] = 0.

        return kwargs_sigma

    def compute_fisher_information(self, recompute=False):
        """
            :param recompute: bool, redo? default False


        """
        if hasattr(self, '_fim') and not recompute:
            return  # nothing to do
        best_fit_values = self._param.best_fit_values()
        if not self.diagonal_only:
            self._fim = self._diff.hessian(best_fit_values).block_until_ready()
        else:
            hvp = jvp(grad(self._diff.loss), (best_fit_values,), (jnp.ones_like(best_fit_values),))[1]
            self._fim = hvp  # hessian vector product with a vector of ones: diag of hessian.
        self._fim = jnp.array(self._fim)
        if hasattr(self, '_cov'):
            delattr(self, '_cov')

    def draw_samples(self, num_samples=10000, seed=None):
        """
        Draw samples from the multivariate Gaussian distribution defined by the best fit values and the covariance

        :param num_samples: int, number of samples to draw
        :param seed: int, seed for the random number generator

        :return: array of shape (num_samples, num_parameters)
        """
        if seed is not None:
            np.random.seed(seed)
        if self.diagonal_only:
            samples = np.random.normal(loc=self._param.best_fit_values(),
                                       scale=jnp.sqrt(jnp.abs(self.covariance_matrix)),
                                       size=(num_samples, len(self._param.best_fit_values())))
        else:
            samples = np.random.multivariate_normal(self._param.best_fit_values(), self.covariance_matrix,
                                                    size=num_samples)
        return samples

    def fisher2covar(self, fisher_matrix, inversion='full'):
        if self.diagonal_only:
            return 1. / fisher_matrix
        if inversion == 'full':
            return jnp.linalg.inv(fisher_matrix)
        elif inversion == 'diag':
            return 1. / jnp.diag(fisher_matrix)
        else:
            raise ValueError("Only 'full' and 'diag' options are supported for inverting the FIM.")

    @staticmethod
    def split_matrix(matrix, num_before, num_after):
        interior = matrix[num_before:-num_after, num_before:-num_after]

        block_UL = matrix[:num_before, :num_before]
        block_UR = matrix[:num_before, -num_after:]
        block_LR = matrix[-num_after:, -num_after:]
        block_LL = matrix[-num_after:, :num_before]
        exterior = jnp.block([[block_UL, block_UR],
                              [block_LL, block_LR]])

        return interior, exterior
