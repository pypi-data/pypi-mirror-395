import time
import warnings

import jax
import numpy as np
import optax
from starred.optim.inference_base import FisherCovariance
from tqdm import tqdm
import jaxopt

from starred.optim.inference_base import InferenceBase


__all__ = ['Optimizer']

SUPPORTED_METHOD_OPTAX = ['adam', 'adabelief', 'radam']
SUPPORTED_METHOD_JAXOPT = ['BFGS', 'GradientDescent', 'LBFGS', 'l-bfgs-b', 'LevenbergMarquardt']
SUPPORTED_METHOD_SCIPYMINIMIZE = ['Nelder-Mead', 'Powell', 'CG', 'Newton-CG', 'TNC', 'COBYLA', 'SLSQP', 'trust-constr',
                                  'dogleg', 'trust-ncg', 'trust-exact', 'trust-krylov']
SUPPORTED_BOUNDED_METHOD = ['l-bfgs-b']

# GRADIENT_METHOD = ['Nelder-Mead', 'Powell', 'CG' 'Newton-CG', 'trust-krylov', 'trust-exact', 'trust-constr']
# HVP_METHOD = ['Nelder-Mead', 'Powell', 'CG','Newton-CG', 'trust-constr', 'trust-krylov', 'trust-constr']


class Optimizer(InferenceBase):
    """
        Class that handles optimization tasks, `i.e.`, finding best-fit point estimates of parameters
        It currently handles a subset of scipy.optimize.minimize routines,
        using first and second order derivatives when required.
    """

    def __init__(self, loss_class, param_class, method='BFGS'):
        super().__init__(loss_class, param_class)
        if method not in SUPPORTED_METHOD_OPTAX + SUPPORTED_METHOD_JAXOPT + SUPPORTED_METHOD_SCIPYMINIMIZE :
            raise NotImplementedError(f'Minimisation method {method} is not supported yet.')
        else:
            self.method = method

        self._metrics = MinimizeMetrics(self.loss, self.method)
    @property
    def loss_history(self):
        """Returns the loss history."""
        if len(self._metrics.loss_history) == 0:
            raise ValueError("You must run the optimizer at least once to access the history")
        return self._metrics.loss_history

    @property
    def param_history(self):
        """Returns the parameter history."""
        if len(self._metrics.param_history) == 0:
            raise ValueError("You must run the optimizer at least once to access the history")
        return self._metrics.param_history

    def minimize(self, restart_from_init=True, **kwargs_optimiser):
        """Minimizes the loss function and returns the best fit."""
        init_params = self._param.current_values(as_kwargs=False, restart=restart_from_init, copy=True)
        start = time.time()

        if self.method in SUPPORTED_METHOD_OPTAX:
            best_fit, extra_fields = self._run_optax(init_params, **kwargs_optimiser)
        elif self.method in SUPPORTED_METHOD_JAXOPT + SUPPORTED_METHOD_SCIPYMINIMIZE:
            best_fit, extra_fields = self._run_jaxopt(init_params, **kwargs_optimiser)
        else:
            raise NotImplementedError(f'Minimization method {self.method} is not supported yet.')

        runtime = time.time() - start
        self._param.set_best_fit(best_fit)
        logL_best_fit = self.loss(best_fit)

        return best_fit, logL_best_fit, extra_fields, runtime

    def _run_jaxopt(self, params, **kwargs_optimiser):
        extra_kwargs = {}
        if self.method in SUPPORTED_BOUNDED_METHOD:
            extra_kwargs['bounds'] = self.parameters.get_bounds()
        else:
            warnings.warn('You are using an unconstrained optimiser. Bounds are ignored.')

        if self.method == 'BFGS':
            solver = jaxopt.BFGS(fun=self.loss, **kwargs_optimiser)
        elif self.method == 'GradientDescent':
            solver = jaxopt.GradientDescent(fun=self.loss, **kwargs_optimiser)
        elif self.method == 'LBFGS':
            solver = jaxopt.LBFGS(fun=self.loss, **kwargs_optimiser)
        elif self.method in SUPPORTED_METHOD_SCIPYMINIMIZE :
            solver = jaxopt.ScipyMinimize(fun=self.loss, method=self.method, callback=self._metrics,
                                          **kwargs_optimiser)
        elif self.method == 'l-bfgs-b':
            solver = jaxopt.ScipyBoundedMinimize(fun=self.loss, method="l-bfgs-b", callback=self._metrics,
                                                 **kwargs_optimiser)
        elif self.method == 'LevenbergMarquardt':
            solver = jaxopt.LevenbergMarquardt(residual_fun=lambda x: jax.numpy.array([self.loss(x)]), 
                                               **kwargs_optimiser)

        res = solver.run(params, **extra_kwargs)
        extra_fields = {'result_class': res, 'stat':res.state, 'loss_history':self._metrics.loss_history}

        return res.params, extra_fields

    def _run_optax(self, params, max_iterations=100, min_iterations=None,
                   init_learning_rate=1e-2, schedule_learning_rate=True,
                   restart_from_init=False, stop_at_loss_increase=False,
                   progress_bar=True, return_param_history=False, decay_rate=0.99):

        if min_iterations is None:
            min_iterations = max_iterations
        if schedule_learning_rate is True:
            # Exponential decay of the learning rate
            scheduler = optax.exponential_decay(
                init_value=init_learning_rate,
                decay_rate=decay_rate,
                transition_steps=max_iterations)

            if self.method == 'adabelief':
                scale_algo = optax.scale_by_belief()
            elif self.method == 'radam':
                scale_algo = optax.scale_by_radam()
            elif self.method == 'adam':
                scale_algo = optax.scale_by_adam()
            else:
                raise NotImplementedError(f"Optax algorithm '{self.method}' is not supported")

            # Combining gradient transforms using `optax.chain`
            optim = optax.chain(
                # optax.clip_by_global_norm(1.0),  # clip by the gradient by the global norm
                scale_algo,  # use the updates from the chosen optimizer
                optax.scale_by_schedule(scheduler),  # Use the learning rate from the scheduler
                optax.scale(-1.)  # because gradient *descent*
            )
        else:
            if self.method == 'adabelief':
                optim = optax.adabelief(init_learning_rate)
            elif self.method== 'radam':
                optim = optax.radam(init_learning_rate)
            elif self.method == 'adam':
                optim = optax.adam(init_learning_rate)
            else:
                raise NotImplementedError(f"Optax algorithm '{self.method}' is not supported")

        # Initialise optimizer state
        opt_state = optim.init(params)
        prev_params, prev_loss_val = params, 1e10

        @jax.jit
        def gradient_step(params, opt_state):
            # loss_val, grads = jax.value_and_grad(self._loss)(params)
            loss_val, grads = self.value_and_gradient(params)
            updates, opt_state = optim.update(grads, opt_state, params)
            params = optax.apply_updates(params, updates)
            return params, opt_state, loss_val

        # Gradient descent loop
        for i in self._for_loop(range(int(max_iterations)), progress_bar,
                                total=int(max_iterations),
                                desc=f"optax.{self.method}"):
            params, opt_state, loss_val = gradient_step(params, opt_state)
            if stop_at_loss_increase and i > min_iterations and loss_val > prev_loss_val: #pragma: no cover
                params, loss_val = prev_params, prev_loss_val
                break
            else:
                self._metrics.loss_history.append(loss_val)
                prev_params, prev_loss_val = params, loss_val
            if return_param_history is True:
                self._metrics.param_history.append(params)

        best_fit = params
        extra_fields = {'loss_history': np.array(
            self._metrics.loss_history)}

        if return_param_history is True:
            extra_fields['param_history'] = self._metrics.param_history

        return best_fit, extra_fields

    @staticmethod
    def _for_loop(iterable, progress_bar_bool, **tqdm_kwargs):
        if progress_bar_bool is True:
            return tqdm(iterable, **tqdm_kwargs)
        else:
            return iterable

    def compute_fisher_matrix(self):
        if len(self._param.best_fit_values(as_kwargs=False)) > 500:
            warnings.warn('Computing the Fisher matrix for more than 500 dimensions will blow up your memory. '
                          'You should reduce the dimensionnality of your model')

        fish = FisherCovariance(self._param, self)
        fish.compute_fisher_information()

        return fish


class MinimizeMetrics(object):
    """Simple callable class used as callback in ``scipy.optimize.minimize`` method."""

    def __init__(self, func, method):
        self.loss_history = []
        self.param_history = []
        self._func = func
        if method == 'trust-constr':
            self._call = None #bug fix for now, jaxopt does not support 2 argument callback for now : https://github.com/google/jaxopt/issues/428
            # self._call = self._call_2args
        else:
            self._call = self._call_1arg

    def __call__(self, *args, **kwargs):
        return self._call(*args, **kwargs)

    def _call_1arg(self, x):
        self.loss_history.append(self._func(x))
        self.param_history.append(x)

    def _call_2args(self, x, state):
        # Input state parameter is necessary for 'trust-constr' method
        # You can use it to stop execution early by returning True
        self.loss_history.append(self._func(x))
        self.param_history.append(x)
