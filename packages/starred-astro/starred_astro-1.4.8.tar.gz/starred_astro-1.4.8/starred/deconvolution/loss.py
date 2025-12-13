import warnings
import jax.numpy as jnp
import jax
import numpy as np

from ..utils.jax_utils import decompose, scale_norms, get_l1_norm


class Loss(object):
    """
    Class that manages the (auto-differentiable) loss function, defined as:
    L = - log(likelihood) - log(regularization) - log(positivity) - log(prior)

    Note that gradient, hessian, etc. are computed in the ``InferenceBase`` class.

    """

    _supported_ll = ('l2_norm')
    _supported_regul_source = ('l1_starlet', 'l1_starlet_pts_rw')

    def __init__(self, data, deconv_class, param_class, sigma_2,
                 regularization_terms='l1_starlet', regularization_strength_scales=1.0, regularization_strength_hf=1.0,
                 regularization_strength_pts_source=0., regularization_strength_positivity=0.,
                 regularization_strength_positivity_ps=0.,
                 regularization_strength_flux_uniformity=0.,
                 regularize_full_model=False, W=None, prior=None):
        """
        :param data: array containing the observations
        :param deconv_class: deconvolution class from ``starred.deconvolution.deconvolution``
        :param param_class: parameters class from ``starred.deconvolution.parameters``
        :param sigma_2: array containing the square of the noise maps
        :param N: number of observations stamps
        :type N: int
        :param regularization_terms: Choose the type of regularization 'l1_starlet' or 'l1_starlet_pts_rw'
        :type regularization_terms: str
        :param regularization_strength_scales: Lagrange parameter that weights intermediate scales in the transformed domain 
        :type regularization_strength_scales: float
        :param regularization_strength_hf: Lagrange parameter weighting the highest frequency scale
        :type regularization_strength_hf: float
        :param regularization_strength_positivity: Lagrange parameter weighting the positivity of the background. 0 means no positivity constrain.
        :type regularization_strength_positivity: float
        :param regularization_strength_positivity_ps: Lagrange parameter weighting the positivity of the point sources. 0 means no positivity constrain.
        :type regularization_strength_positivity: float
        :param regularization_strength_pts_source: Lagrange parameter regularising the point source channel.
        :type regularization_strength_pts_source: float
        :param regularization_strength_flux_uniformity: Lagrange parameter regularising scatter in the fluxes of each point source
        :param W: weight matrix. Shape (n_scale, n_pix*subsampling_factor, n_pix*subsampling_factor)
        :type W: jax.numpy.array
        :param regularize_full_model: option to regularise just the background (False) or background + point source channel (True)
        :type regularize_full_model: bool
        :param prior: Prior class containing Gaussian prior on the free parameters
        :type prior: Prior class

        """

        # We wish to store our data directly in the format needed by jax.
        # so, determine the desired precision based on jax's config
        if jax.config.read("jax_enable_x64"):
            dtype = jnp.float64
        else:
            dtype = jnp.float32
        self._data = data.astype(dtype)
        self._sigma_2 = sigma_2.astype(dtype)

        self.W = W
        if W is not None:
            self.W = W.astype(dtype)
        self._deconv = deconv_class
        self._data = self._data.reshape(self._deconv.epochs,
                                        self._deconv.image_size,
                                        self._deconv.image_size)
        self._sigma_2 = self._sigma_2.reshape(self._deconv.epochs,
                                              self._deconv.image_size,
                                              self._deconv.image_size)

        self._param = param_class
        self.epochs = self._deconv.epochs
        self.n_sources = self._deconv.M
        self.regularize_full_model = regularize_full_model
        self.prior = prior

        self._init_likelihood()
        self._init_prior()
        self._init_regularizations(regularization_terms, regularization_strength_scales, regularization_strength_hf,
                                   regularization_strength_positivity, regularization_strength_positivity_ps,
                                   regularization_strength_pts_source, regularization_strength_flux_uniformity)

        self._validate()

    # @partial(jit, static_argnums=(0,))
    def __call__(self, args):
        return self.loss(args)

    def loss(self, args):
        """Defined as the negative log(likelihood*regularization)."""
        kwargs = self._param.args2kwargs(args)
        neg_log = - self._log_likelihood(kwargs)
        if self._st_src_lambda != 0 or self._st_src_lambda_hf !=0 :
            neg_log -= self._log_regul(kwargs)
        if self._pos_lambda != 0:
            neg_log -= self._log_regul_positivity(kwargs)
        if self._pos_lambda_ps != 0.:
            neg_log -= self._log_regul_positivity_ps(kwargs)
        if self.prior is not None:
            neg_log -= self._log_prior(kwargs)
        if self._lambda_pts_source != 0.:
            neg_log -= self._log_regul_pts_source(kwargs)
        if self._lambda_flux_scatter != 0.:
            neg_log -= self._log_regul_flux_uniformity(kwargs)

        return jnp.nan_to_num(neg_log, nan=1e15, posinf=1e15, neginf=1e15)

    @property
    def data(self):
        """Returns the observations array."""
        return self._data.astype(dtype=np.float32)

    @property
    def sigma_2(self):
        """Returns the noise map array."""
        return self._sigma_2.astype(dtype=np.float32)

    def _init_likelihood(self):
        """Intialization of the data fidelity term of the loss function."""
        self._log_likelihood = self._log_likelihood_chi2

    def _init_prior(self):
        """
        Initialization of the prior likelihood
        """
        if self.prior is None:
            self._log_prior =  lambda x: 0.
        else :
            self._log_prior = self._log_prior_gaussian

    def _init_regularizations(self, regularization_terms, regularization_strength_scales, regularization_strength_hf,
                              regularization_strength_positivity, regularization_strength_positivity_ps,
                              regularization_strength_pts_source, regularization_strength_flux_uniformity):
        """Intialization of the regularization terms of the loss function."""
        regul_func_list = []
        # add the log-regularization function to the list
        regul_func_list.append(getattr(self, '_log_regul_' + regularization_terms))

        if regularization_terms == 'l1_starlet' or regularization_terms == 'l1_starlet_pts_rw':
            n_pix_src = min(*self._data[0, :, :].shape) * self._deconv._upsampling_factor
            self.n_scales = int(np.log2(n_pix_src))  # maximum allowed number of scales
            if self.W is None:  # old fashion way
                if regularization_strength_scales != 0 and regularization_strength_hf != 0:
                    warnings.warn('lambda is not normalized. Provide the weight map !')
                wavelet_norms = scale_norms(self.n_scales)[:-1]  # ignore coarsest scale
                self._st_src_norms = jnp.expand_dims(wavelet_norms, (1, 2)) * jnp.ones((n_pix_src, n_pix_src))
            else:
                self._st_src_norms = self.W[:-1]  # ignore the coarsest scale
            self._st_src_lambda = float(regularization_strength_scales)
            self._st_src_lambda_hf = float(regularization_strength_hf)

        # compute l1 norm of a pts source of amp = 1
        if self._deconv.M > 0:
            self.l1_pts = self._init_l1_pts()
        else:
            self.l1_pts = 0.

        # positivity term
        self._pos_lambda = float(regularization_strength_positivity)
        self._pos_lambda_ps = float(regularization_strength_positivity_ps)

        # regularization strenght of the pts source channel
        self._lambda_pts_source = float(regularization_strength_pts_source)

        # regularization: discourage too much flux scatter
        self._lambda_flux_scatter = float(regularization_strength_flux_uniformity)

        # build the composite function (sum of regularization terms)
        self._log_regul = lambda kw: sum([func(kw) for func in regul_func_list])

    def _init_l1_pts(self):
        one_pts = self._deconv.shifted_gaussians([0.], [0.], [1.], source_ID=[0])
        pts_im_starlet = decompose(one_pts, self.n_scales)[:-1]  # ignore coarsest scale
        return jnp.sum(self._st_src_norms * jnp.abs(pts_im_starlet))

    def _log_likelihood_chi2(self, kwargs):
        """Computes the data fidelity term of the loss function using the L2 norm."""
        model = self._deconv.model(kwargs)
        return - 0.5 * jnp.sum((model - self._data) ** 2 / self._sigma_2)

    def _log_regul_l1_starlet(self, kwargs):
        """
        Computes the regularization terms as the sum of:
        
        - the L1 norm of the Starlet transform of the highest frequency scale, and
        - the L1 norm of the Starlet transform of all remaining scales (except the coarsest).
        """
        if self.regularize_full_model:
            toreg, _ = self._deconv.getDeconvolved(kwargs, epoch=None)
        else :
            _, toreg = self._deconv.getDeconvolved(kwargs, epoch=None)
        st = decompose(toreg, self.n_scales)[:-1]  # ignore coarsest scale
        st_weighted_l1_hf = jnp.sum(self._st_src_norms[0] * jnp.abs(st[0]))  # first scale (i.e. high frequencies)
        st_weighted_l1 = jnp.sum(self._st_src_norms[1:] * jnp.abs(st[1:]))  # other scales
        tot_l1_reg = - (self._st_src_lambda_hf * st_weighted_l1_hf + self._st_src_lambda * st_weighted_l1)

        return (tot_l1_reg / self._deconv._upsampling_factor ** 2) * self.epochs

    def _log_regul_positivity(self, kwargs):
        """
        Computes the posivity constraint term. A penalty is applied if the epoch with the smallest background mean has negative pixels.

        :param kwargs:
        """
        h = self._deconv._get_background(kwargs)
        sum_pos = -jnp.where(h < 0., h, 0.).sum()
        return - self._pos_lambda * sum_pos * self.epochs

    def _log_regul_positivity_ps(self, kwargs):
        """
        Computes the posivity constraint term for the point sources. A penalty is applied if one of the point sources have negative amplitude.

        :param kwargs:
        """
        fluxes = jnp.array(kwargs['kwargs_analytic']['a'])
        sum_pos = -jnp.where(fluxes < 0., fluxes, 0.).sum()
        return - self._pos_lambda * sum_pos * self.epochs

    def _log_regul_pts_source(self, kwargs):
        """
        Penalty term to the pts source, to compensate for the fact that the pts source channel is not regularized

        :param kwargs: dictionary containing all keyword arguments
        """
        pts_source_channel = self._deconv.getPts_source(kwargs, epoch=None)
        st = decompose(pts_source_channel, self.n_scales)[:-1]  # ignore coarsest scale
        st_weighted_l1 = jnp.sum(self._st_src_norms * jnp.abs(st))  # other scales
        tot_l1_reg = - self._lambda_pts_source * st_weighted_l1

        return (tot_l1_reg / self._deconv._upsampling_factor ** 2) * self.epochs

    def _log_prior_gaussian(self, kwargs):
        """
        A flexible term in the likelihood to impose a Gaussian prior on any parameters of the model.

        :param kwargs: dictionary containing all keyword arguments
        """
        return self.prior.logL(kwargs)

    def _log_regul_flux_uniformity(self, kwargs):
        reshaped_fluxes = kwargs['kwargs_analytic']['a'].reshape(-1, self.n_sources).T
        mean_absolute_flux = jnp.mean(jnp.abs(reshaped_fluxes), axis=1, keepdims=True) + 1e-8
        normalized_fluxes = reshaped_fluxes / mean_absolute_flux
        # focus on short-term scatter: differences between consecutive epochs
        # (assumes epochs sorted by time, as they should be)
        diffs = normalized_fluxes[:, 1:] - normalized_fluxes[:, :-1]  # delta between epochs
        variance = jnp.var(diffs, axis=1)
        scatter = jnp.sqrt(variance + 1e-8)  # stabilize standard deviation

        return -self._lambda_flux_scatter * jnp.sum(scatter) * self.epochs

    def _validate(self):
        """Check if the data and noise maps are valid."""

        assert jnp.isnan(self._data.any()) == False, 'Data contains NaNs'
        assert jnp.isnan(self._sigma_2.any()) == False, 'Noise map contains NaNs'

        # check if noise maps contains negative values
        assert (self._sigma_2 <= 0).any() == False, 'Noise map contains negative or 0 values'

        # check that everything have the correct dimension
        nepoch, npix, npix = self._data.shape
        nepoch_sigma, npix_sigma, npix_sigma = self._sigma_2.shape

        assert nepoch == nepoch_sigma, 'Data and noise maps have different number of epochs'
        assert npix == npix_sigma, 'Data and noise maps have different number of pixels'
        assert npix == self._deconv.image_size, 'Data and Deconvolution class have different number of pixels'
        assert nepoch == self._deconv.epochs, 'Data and Deconvolution class have different number of epochs'

        # check flux uniformity regularization: cannot use if only one epoch!
        if self._lambda_flux_scatter > 0. and self._deconv.epochs == 1:
            raise AssertionError("Cannot use a regularization depending on fluxes across epochs with only one epoch! "
                                 "Add more epochs or set regularization_strength_flux_uniformity to 0.")

    def reduced_chi2(self, kwargs):
        """
        Return the reduced chi2, given some model parameters

        :param kwargs: dictionary containing all keyword arguments
        """
        return -2 * self._log_likelihood_chi2(kwargs) / (self._deconv.image_size ** 2) / self._deconv.epochs

    def update_weights(self, W):
        """Updates the weight matrix W."""

        self._st_src_norms = W[:-1]
        self.W = W

    def update_lambda_pts_source(self, kwargs):
        """Update lambda_pts regularization according to the new model, according to Appendix C of Millon et al. (2024).

        :param kwargs: dictionary containing all keyword arguments
        """

        deconvolved, background = self._deconv.getDeconvolved(kwargs)
        l1p_sum = 0
        for i in range(self._deconv.M):
            pts_im = self._deconv.getPts_source(kwargs, epoch=None, source_ID=[i])
            l1p_sum += - get_l1_norm(pts_im, self.W[:-1], self.n_scales) / self._deconv._upsampling_factor ** 2

        l1_bkg = - get_l1_norm(background, self.W[:-1], self.n_scales) / self._deconv._upsampling_factor ** 2
        l1_f = - get_l1_norm(deconvolved, self.W[:-1], self.n_scales) / self._deconv._upsampling_factor ** 2

        new_lambda_pts_source = float(self._st_src_lambda * (l1_f - l1_bkg) / l1p_sum)
        self._lambda_pts_source = new_lambda_pts_source

        return new_lambda_pts_source


class Prior(object):
    def __init__(self, prior_analytic=None, prior_background=None, prior_sersic=None):
        """

        :param prior_analytic: list of [param_name, mean, 1-sigma priors]
        :param prior_background: list of [param_name, mean, 1-sigma priors]
        :param prior_sersic: list of [param_name, mean, 1-sigma priors]
        """
        self._prior_analytic = prior_analytic
        self._prior_background = prior_background
        self._prior_sersic = prior_sersic

    def logL(self, kwargs):
        logL = 0
        logL += self.prior_kwargs(kwargs['kwargs_analytic'], self._prior_analytic)
        logL += self.prior_kwargs(kwargs['kwargs_background'], self._prior_background)
        logL += self.prior_kwargs(kwargs['kwargs_sersic'], self._prior_sersic)

        return logL

    @staticmethod
    def prior_kwargs(kwargs, prior):
        """
        Return gaussian prior weights

        :param kwargs: keyword argument
        :param prior: List containing [param_name, mean, 1-sigma priors]
        :return: logL
        """
        if prior is None:
            return 0
        logL = 0
        for i in range(len(prior)):
            param_name, value, sigma = prior[i]
            model_value = kwargs[param_name]
            dist = (model_value - value) ** 2 / sigma ** 2 / 2
            logL -= np.sum(dist)
        return logL

