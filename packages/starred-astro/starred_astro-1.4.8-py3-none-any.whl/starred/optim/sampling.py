import time
import jax
import jax.numpy as jnp
import numpy as np

import emcee
from mclmc.sampler import Sampler as MCHMCSampler
from starred.optim.inference_base import InferenceBase

SUPPORTED_SAMPLER = ['emcee', 'mchmc']


class Sampler(InferenceBase):
    def __init__(self, loss_class, param_class, sampler='emcee'):
        super().__init__(loss_class, param_class)

        if sampler not in SUPPORTED_SAMPLER:
            raise NotImplementedError(f'Sampler {sampler} is not supported yet.')
        else:
            self.sampler = sampler

        self.grad_nlogp = self.value_and_gradient
        self.d = len(self._param.initial_values(as_kwargs=False))
        self.bound_up = self._param.get_bounds()[1]
        self.bound_down = self._param.get_bounds()[0]

    def sample(self, init_params, **kwargs_sampler):
        """Minimizes the loss function and returns the best fit."""

        start = time.time()

        if self.sampler == 'emcee':
            samples, logL = self._run_emcee(init_params, **kwargs_sampler)
        elif self.sampler == 'mchmc':
            samples, logL = self._run_mchmc(init_params, **kwargs_sampler)
        else:
            raise NotImplementedError(f'Minimization method {self.sampler} is not supported yet.')

        runtime = time.time() - start
        return samples, logL, runtime

    def _run_emcee(self, initial_values, walker_ratio=5, nsteps=10, sigma_init=1e-4):
        ndim = len(initial_values)
        nwalkers = walker_ratio * ndim
        p0 = initial_values + initial_values * sigma_init * np.random.randn(nwalkers, ndim)

        sampler = emcee.EnsembleSampler(nwalkers, ndim, self.log_likelihood)
        sampler.run_mcmc(p0, nsteps=nsteps, progress=True)

        samples = sampler.get_chain(flat=True)
        logprob = sampler.get_log_prob()

        return samples, logprob

    def _run_mchmc(self, initial_values, num_steps=500, num_chains=10, random_key=None, sigma_init=1e-4):
        mchmcs = MCHMCSampler(self)
        p0 = initial_values + initial_values * sigma_init * np.random.randn(num_chains, self.d)
        samples = mchmcs.sample(num_steps=num_steps, num_chains=num_chains, x_initial=p0, random_key=random_key)
        return samples, None

    def prior_draw(self, key):
        """Uniform prior"""
        return jax.random.uniform(key, shape=(self.d,), minval=self.bound_down, maxval=self.bound_up, dtype='float64')

    def transform(self, x):
        """transform x back to the original parameter. Useful if some parameter are sampled in log space for example"""
        return x
