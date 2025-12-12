# Utilities function for Foreground fitting and removal
#
# Authors: F.Mertens

import functools

import numpy as np

from scipy.special import comb
from scipy import stats
from scipy.optimize import minimize_scalar, brute, fmin

from sklearn.decomposition import PCA

from . import psutil, pscart

import re

class _MissingGPY:
    def __getattr__(self, name):
        raise ImportError(
            "GPy is not installed. Install with `pip install ps_eor[ml-gpr]` "
        )
    def __call__(self, *a, **k):
        raise ImportError(
            "GPy is not installed. Install with `pip install ps_eor[ml-gpr]` "
        )

try:
    import GPy
    import paramz

    HAS_GPY = True
except ImportError:
    GPy = _MissingGPY()
    paramz = _MissingGPY()

    HAS_GPY = False


class GprConfig(object):

    def __init__(self):
        ''' GPR fitting configuration '''

        # The covariance kernel used to represent the FG
        self.fg_kern = GPy.kern.Matern32(1, name='fg_med')
        self.fg_kern.lengthscale.constrain_bounded(5, 20, warning=False)

        self.int_fg_kern = None

        # Whatever to include or not the EoR kernel during the fitting
        self.include_eor = True
        # The covariance kernel used to represent the EoR
        self.eor_kern = GPy.kern.Exponential(1, name='eor_exp')

        # Perform a first GPR run with a post PCA run then do a second GPR run
        # with this PCA component removed.
        self.first_run_pca_n = 0

        # Perform a polynomial fit before GPR
        self.pre_poly_fit_deg = 0
        self.pre_poly_fit_type = 'power_poly'

        # Perform a PCA fit before GPR
        self.pre_pca_n = 0

        # Perform a PCA fit after GPR
        self.post_pca_n = 0

        # Remove the mean in frequency direction
        self.r_mean = False

        self.heteroscedastic = True
        self.fixed_noise = True
        self.fixed_noise_scale = 1.
        self.noise_scale_search_method = 'brute'
        self.noise_scale_search_range = [0.25, 4]
        self.noise_scale_search_tol = 1e-3
        self.noise_scale_search_n_restarts = 2
        self.noise_scale_search_maxiter = 15
        self.use_simulated_noise = False
        self.simulated_noise_scale_kper = True

        self.num_restarts = 10

        self.verbose = True

        # Deprecated
        self.noise_scale_delta_l = 50
        self.gpr_n_samples = 10
        self.num_processes = 1

        # Global scale factor. Generally one. Decrease it (e.g. 1e-2) to reach very deep precision
        self.data_scale_factor = 1.

    @staticmethod
    def load(filename):
        config = GprConfig()
        with open(filename, 'r', encoding='utf-8') as config_file:
            for line in config_file.readlines():
                if line.strip().startswith('#') or line.strip() == '':
                    continue
                arg, _, val = re.match(r'(\w+)\s*(\=|\:)(.+)', line).groups()
                arg = arg.strip()
                val = val.strip()

                if arg == 'int_fg_kern':
                    config.int_fg_kern = parse_gpr_kern_str(val, 'int_fg')
                elif arg == 'fg_kern':
                    config.fg_kern = parse_gpr_kern_str(val, 'fg')
                elif arg == 'eor_kern':
                    config.eor_kern = parse_gpr_kern_str(val, 'eor')
                elif hasattr(config, arg):
                    if type(getattr(config, arg)) is bool:
                        type_fct = psutil.str2bool
                    elif isinstance(getattr(config, arg), (list, np.ndarray)):
                        type_fct = psutil.str2floatlist
                    else:
                        type_fct = type(getattr(config, arg))
                    setattr(config, arg, type_fct(val))
                else:
                    print('Warning: GPR config %s invalid' % arg)

        # Check consistency
        if config.int_fg_kern is not None and (config.pre_poly_fit_deg + config.pre_pca_n) > 0:
            raise ValueError('Only one of int_fg_kern/pre_poly_fit_deg/pre_pca_n is possible')

        return config


class GprResult(object):

    def __init__(self, model, y_fit, y_sub, y_pre_fit, y_post_fit, cov_err, y_scale):
        ''' Encapsulate the GPR fit result '''
        self.y_fit = y_fit
        self.y_sub = y_sub
        self.model = model
        self.y_pre_fit = y_pre_fit
        self.y_post_fit = y_post_fit
        self.cov_err = cov_err
        self.y_scale = y_scale

    def test_single_parameter(self, param_name, min_value, max_value, n_optimize_loop=2,
                              tol=1e-3, verbose=False, method='bounded', brute_ns=20):
        model = self.model.copy()
        p = get_model_parameter(model, param_name)

        def func(v):
            if v < 0:
                return 1e99

            p.constrain_fixed(v)
            model.optimize_restarts(n_optimize_loop, verbose=False)

            if verbose:
                print('Test:', v, - model.log_likelihood() - model.log_prior())

            return - model.log_likelihood() - model.log_prior()

        def brute_finish(fct, pos, args):
            return fmin(fct, pos, xtol=tol, ftol=tol, maxiter=brute_ns, full_output=1, disp=0)

        if method == 'brute':
            res = brute(func, [(min_value, max_value)], Ns=brute_ns, finish=brute_finish)
            x0 = res[0]
        elif method == 'bounded':
            res = minimize_scalar(func, tol=tol, bounds=[min_value, max_value], method='bounded')
            x0 = res.x
        else:
            res = minimize_scalar(func, bracket=[min_value, max_value], tol=tol, method=method)
            x0 = res.x

        return x0


if HAS_GPY:
    class HeteroScaleGaussian(GPy.likelihoods.Likelihood):
        """
        Gaussian likelihood
        :param variance: variance value of the Gaussian distribution
        :param N: Number of data points
        :type N: int
        """

        def __init__(self, variance, gp_link=None, variance_scale=1., name='het_Gauss'):
            if gp_link is None:
                gp_link = GPy.likelihoods.link_functions.Identity()

            if not isinstance(gp_link, GPy.likelihoods.link_functions.Identity):
                print("Warning, Exact inference is not implemeted for non-identity link functions,\
                if you are not already, ensure Laplace inference_method is used")

            super(HeteroScaleGaussian, self).__init__(gp_link, name=name)

            self.variance_scale = GPy.core.parameterization.Param('variance_scale',
                                                                  variance_scale, paramz.transformations.Logexp())
            self.variance = variance
            self.link_parameter(self.variance_scale)

            if isinstance(gp_link, GPy.likelihoods.link_functions.Identity):
                self.log_concave = True

            self.fct_done = []

        def gaussian_variance(self, Y_metadata=None):
            return self.variance_scale * self.variance.flatten()

        def update_gradients(self, grad):
            # print self.variance_scale.values[0]
            self.variance_scale.gradient = grad

        def exact_inference_gradients(self, dL_dKdiag, Y_metadata=None):
            return dL_dKdiag.sum()

        def predictive_values(self, mu, var, full_cov=False, Y_metadata=None):
            if full_cov:
                if var.ndim == 2:
                    var += np.eye(var.shape[0]) * self.variance_scale * self.variance
                if var.ndim == 3:
                    var += np.atleast_3d(np.eye(var.shape[0]) * self.variance_scale * self.variance)
            else:
                var += self.variance_scale * self.variance
            return mu, var

        def predictive_mean(self, mu, sigma):
            return mu

        def predictive_variance(self, mu, sigma, predictive_mean=None):
            return self.variance_scale * self.variance + sigma**2

        def predictive_quantiles(self, mu, var, quantiles, Y_metadata=None):
            return [stats.norm.ppf(q / 100.) * np.sqrt(var + self.variance_scale * self.variance) + mu for q in quantiles]


    class GPHeteroScaleRegression(GPy.core.GP):

        def __init__(self, X, Y, noise_variance, kernel=None, Y_metadata=None):

            Ny = Y.shape[0]

            if Y_metadata is None:
                Y_metadata = {'output_index': np.arange(Ny)[:, None]}
            else:
                assert Y_metadata['output_index'].shape[0] == Ny

            if kernel is None:
                kernel = GPy.kern.RBF(X.shape[1])

            # Likelihood
            likelihood = HeteroScaleGaussian(noise_variance)
            inference = GPy.inference.latent_function_inference.exact_gaussian_inference.ExactGaussianInference()

            super(GPHeteroScaleRegression, self).__init__(X, Y, kernel, likelihood, Y_metadata=Y_metadata,
                                                          inference_method=inference)


    class WhiteHetero(GPy.kern.White):
        def __init__(self, input_dim, variance=1., variance_fixe=1., active_dims=None, name='noise_hetero_scale'):
            """
            A heteroscedastic White kernel (nugget/noise).
            It defines one variance (nugget) per input sample.
            Prediction excludes any noise learnt by this Kernel, so be careful using this kernel.
            You can plot the errors learnt by this kernel by something similar as:
            plt.errorbar(m.X, m.Y, yerr=2*np.sqrt(m.kern.white.variance))
            """
            super(WhiteHetero, self).__init__(input_dim, variance, active_dims, name)
    #         self.variance = GPy.core.parameterization.Param('variance', variance, paramz.transformations.Logexp())
            self.variance_fixe = variance_fixe
    #         self.link_parameters(self.variance)

        def Kdiag(self, X):
            print(X.shape[0], self.variance_fixe.shape[0])
            if X.shape[0] == self.variance_fixe.shape[0]:
                # If the input has the same number of samples as
                # the number of variances, we return the variances
                #             print
                return self.variance * self.variance_fixe
            return 0.

        def K(self, X, X2=None):
            return np.eye(X.shape[0]) * self.variance * self.variance_fixe
    #         print X.shape[0],self.variance_fixe.shape[0]
            if X2 is None and X.shape[0] == self.variance_fixe.shape[0]:
                return np.eye(X.shape[0]) * self.variance * self.variance_fixe
            else:
                return np.zeros((X.shape[0], X2.shape[0]))

        def psi2(self, Z, variational_posterior):
            return np.zeros((Z.shape[0], Z.shape[0]), dtype=np.float64)

        def psi2n(self, Z, variational_posterior):
            return np.zeros((1, Z.shape[0], Z.shape[0]), dtype=np.float64)

        def update_gradients_full(self, dL_dK, X, X2=None):
            if X2 is None:
                self.variance.gradient = 1 * np.trace(dL_dK)
            else:
                self.variance.gradient = 0.

        def update_gradients_diag(self, dL_dKdiag, X):
            self.variance.gradient = 1 * dL_dKdiag.sum()

        def update_gradients_expectations(self, dL_dpsi0, dL_dpsi1, dL_dpsi2, Z, variational_posterior):
            self.variance.gradient = 1 * dL_dpsi0.sum()


    class RatExp(GPy.kern.src.stationary.Stationary):
        def __init__(self, input_dim, variance=1., lengthscale=None, power=2., ARD=False,
                     active_dims=None, name='RatExp'):
            from paramz.transformations import Logexp

            super(RatExp, self).__init__(input_dim, variance, lengthscale, ARD, active_dims, name)
            self.power = GPy.core.parameterization.Param('power', power, Logexp())
            self.link_parameters(self.power)
            self.alpha = 2

        def K_of_r(self, r):
            return self.variance * (1 + r ** self.alpha / 2) ** -self.power

        def dK_dr(self, r):
            return - self.variance * self.power * 2 ** self.power * (r ** self.alpha + 2) ** (-self.power - 1)

        def update_gradients_full(self, dL_dK, X, X2=None):
            super(RatExp, self).update_gradients_full(dL_dK, X, X2)
            r = self._scaled_dist(X, X2) ** self.alpha
            dK_dpow = - self.variance * 2 ** self.power * (r + 2) ** -self.power * np.log(r / 2 + 1)
            self.power.gradient = np.sum(dL_dK * dK_dpow)

        def update_gradients_diag(self, dL_dKdiag, X):
            super(RatExp, self).update_gradients_diag(dL_dKdiag, X)
            self.power.gradient = 0.


    class GammaExp(GPy.kern.src.stationary.Stationary):
        def __init__(self, input_dim, variance=1., lengthscale=None, ls2=1., ARD=False, active_dims=None, name='GammaExp'):
            from paramz.transformations import Logexp

            super(GammaExp, self).__init__(input_dim, variance, lengthscale, ARD, active_dims, name)
            self.ls2 = GPy.core.parameterization.Param('ls2', ls2, Logexp())
            self.link_parameters(self.ls2)
            self.ls2 = self.lengthscale

        def K_of_r(self, r):
            a = self.lengthscale / self.ls2
            return self.variance * (np.exp(- r) + np.exp(- r * a))

        def dK_dr(self, r):
            a = self.lengthscale / self.ls2
            return - self.variance * (a * np.exp(- r * a) + np.exp(- r))

        def update_gradients_full(self, dL_dK, X, X2=None):
            super(GammaExp, self).update_gradients_full(dL_dK, X, X2)
            r = self._scaled_dist(X, X2)
            a = self.lengthscale / self.ls2
            dK_dpow = - self.variance * r * np.exp(- r ** a)
            grad = np.sum((dL_dK * dK_dpow))
            self.ls2.gradient = grad

        def update_gradients_diag(self, dL_dKdiag, X):
            super(GammaExp, self).update_gradients_diag(dL_dKdiag, X)
            self.ls2.gradient = 0.


    class ExpSum(GPy.kern.src.stationary.Stationary):
        def __init__(self, input_dim, variance=1., lengthscale=None, power=1., ARD=False, active_dims=None, name='ExpSum'):
            from paramz.transformations import Logexp

            super(ExpSum, self).__init__(input_dim, variance, lengthscale, ARD, active_dims, name)
            self.power = GPy.core.parameterization.Param('power', power, Logexp())
            self.link_parameters(self.power)
            self.power.constrain_bounded(1, 5)
            # self.power.constrain_fixed(1)

        def K_of_r(self, r):
            a = self.power
            k = self.variance * 1 / r * (np.exp(-r) - np.exp(-a * r))
            k[np.isnan(k)] = 10
            return k

        def dK_dr(self, r):
            a = self.power
            dk = self.variance * (- np.exp(-r) * r + a * np.exp(-a * r) * r - np.exp(-r) + np.exp(-a * r)) / r ** 2
            dk[np.isnan(dk)] = 10
            return dk

        def update_gradients_full(self, dL_dK, X, X2=None):
            super(ExpSum, self).update_gradients_full(dL_dK, X, X2)
            r = self._scaled_dist(X, X2)
            a = self.power
            dK_dpow = np.exp(-a * r)
            grad = np.nansum((dL_dK * dK_dpow))
            self.power.gradient = grad

        def update_gradients_diag(self, dL_dKdiag, X):
            super(ExpSum, self).update_gradients_diag(dL_dKdiag, X)
            self.power.gradient = 0.
else:
    HeteroScaleGaussian = _MissingGPY
    GPHeteroScaleRegression = _MissingGPY
    WhiteHetero = _MissingGPY
    RatExp = _MissingGPY
    GammaExp = _MissingGPY
    ExpSum = _MissingGPY


def get_kern_startwith(kern, name):
    ''' Return a subset of kern with there name starting with "name"'''
    kern_list = []
    for k in kern.parts:
        if k.name.startswith(name):
            kern_list.append(k)
    if len(kern_list) == 0:
        return None
    return GPy.kern.Add(kern_list)


def get_model_parameter(model, param_name):
    for p in model.flattened_parameters:
        if param_name in p.hierarchy_name():
            return p


def parse_gpr_kern_str(full_str, name_start):

    re_kern = r"(\w+)\(([.0-9-=\sGalnN\[\];]+),([.0-9-=\sGalnN\[\];]+)\)"
    re_kern_3hp = r"(\w+)\(([.0-9-=\sGalnN\[\];]+),([.0-9-=\sGalnN\[\];]+),([.0-9-=\s]+)\)"
    re_prior = r"(\w+)\[([.0-9-=\s]+)\;([.0-9-=\s]+)\;([.0-9-=\s]+)\]"

    all_k = None

    def process_arg(kern_arg, s):
        s = s.strip()
        prior_m = re.match(re_prior, s)
        if prior_m is not None:
            prior_name, exp, var, init = prior_m.groups()
            exp = float(exp.strip())
            var = float(var.strip())
            init = float(init.strip())
            if prior_name.strip() == 'Ga':
                prior = GPy.priors.Gamma.from_EV(exp, var)
            elif prior_name.strip() == 'lnN':
                prior = GPy.priors.LogGaussian(np.log10(exp), var)
            kern_arg.set_prior(prior, warning=False)
            kern_arg = init
        elif s.startswith('='):
            kern_arg.constrain_fixed(float(s[1:].strip()), warning=False)
        elif '-' in s:
            ss = s.split('-')
            kern_arg.constrain_bounded(float(ss[0].strip()), float(ss[-1].strip()), warning=False)
            if len(ss) == 3:
                kern_arg = float(ss[1])
        else:
            kern_arg = float(s)
        return kern_arg

    all_k = None

    for s in full_str.split('+'):
        s = s.strip()
        r1 = re.match(re_kern, s)
        r2 = re.match(re_kern_3hp, s)

        if r1 is not None:
            k_name, var_s, ls_s = r1.groups()
            p_s = None
        elif r2 is not None:
            k_name, var_s, ls_s, p_s = r2.groups()
        else:
            raise Exception("Error parsing gpr configuration '%s'" % s)

        if k_name == 'RatExp':
            kern = RatExp(1)
        elif k_name == 'GammaExp':
            kern = GammaExp(1)
        elif k_name == 'ExpSum':
            kern = ExpSum(1)
        elif k_name == 'RBFCos':
            rbf = GPy.kern.RBF(1, name='per_rbf')
            # for the Cosine kernel, lengthscale = period / 2 pi
            per = GPy.kern.Cosine(1, name='per_cos')
            kern = GPy.kern.Prod([rbf * per], name='per')
        elif k_name == 'RBFsquare':
            rbf1 = GPy.kern.RBF(1, name='rbf_a')
            # for the Cosine kernel, lengthscale = period / 2 pi
            rbf2 = GPy.kern.RBF(1, name='rbf_b')
            kern = GPy.kern.Prod([rbf1 * rbf2], name='rbf')
        else:
            kern = getattr(GPy.kern, k_name)(1)

        if k_name == 'RBFCos':
            kern.per_rbf.variance = process_arg(kern.per_rbf.variance, var_s)
            kern.per_cos.variance.constrain_fixed(1, warning=False)
            kern.per_rbf.lengthscale = process_arg(kern.per_rbf.lengthscale, ls_s)
            kern.per_cos.lengthscale = process_arg(kern.per_cos.lengthscale, p_s)
        elif k_name == 'RBFsquare':
            kern.rbf_a.variance = process_arg(kern.rbf_a.variance, var_s)
            kern.rbf_b.variance.constrain_fixed(1, warning=False)
            kern.rbf_a.lengthscale = process_arg(kern.rbf_a.lengthscale, ls_s)
            kern.rbf_b.lengthscale = process_arg(kern.rbf_b.lengthscale, p_s)
        else:
            kern.variance = process_arg(kern.variance, var_s)
            kern.lengthscale = process_arg(kern.lengthscale, ls_s)
            if hasattr(kern, 'power') and r2 is not None:
                kern.power = process_arg(kern.power, p_s)

        kern.name = name_start + '_' + kern.name

        if all_k is not None:
            all_k += kern
        else:
            all_k = kern

    return all_k


def get_ps_err_from_cov_err(ps2d_fct, cov_err, y_scale, num_samples=20):
    ''' Return the power spectra from the given covariance error'''
    all_ps = []
    n_freqs = cov_err.shape[0]
    n_modes = len(y_scale)
    for i in range(num_samples):
        err_r = np.random.multivariate_normal(np.zeros(n_freqs), cov_err, n_modes).T * y_scale.real
        err_i = np.random.multivariate_normal(np.zeros(n_freqs), cov_err, n_modes).T * y_scale.imag
        all_ps.append(ps2d_fct(err_r + 1j * err_i))

    return np.mean(all_ps, axis=0)


def get_model_cmpt(gpr_result, kern, include_noise=True, compute_at_x=None):
    model = gpr_result.model.copy()

    if isinstance(kern, str):
        kern = get_kern_startwith(model.kern, kern)

    if compute_at_x is None:
        x = model.X
    else:
        x = compute_at_x
        assert not include_noise, "compute_at_x not possible with include_noise"

    y_metadata = {'output_index': np.arange(len(x))[:, None]}

    y_fit_part_flat, cov_err = model.predict(x, full_cov=True, kern=kern, Y_metadata=y_metadata,
                                             include_likelihood=include_noise)

    y_fit_part = y_fit_part_flat[:, :gpr_result.y_scale.shape[0]].astype(complex) * gpr_result.y_scale.real
    y_fit_part += 1j * y_fit_part_flat[:, gpr_result.y_scale.shape[0]:] * gpr_result.y_scale.imag

    return y_fit_part, cov_err


def get_model_noise(gpr_result):
    return gpr_result.model.likelihood.gaussian_variance(gpr_result.model.Y_metadata).flatten()


def run_gpr(x, y, y_v, kern, verbose=True, heteroscedastic=True, num_restarts=10,
            fixed_noise=True, fixed_noise_scale=1, num_processes=1):
    ''' Low level GPR, simple wrapper over GPy for convenience'''
    y_metadata = {'output_index': np.arange(len(x))[:, None]}

    if heteroscedastic:
        # likelihood = GPy.likelihoods.HeteroscedasticGaussian(y_metadata)
        # mean_fct = GPy.mappings.Linear(1, y.shape[1])
        # model= GPy.core.GP(x[:, np.newaxis], y, kern, likelihood, mean_function=mean_fct,
        #     Y_metadata=y_metadata)
        if fixed_noise:
            model = GPy.models.GPHeteroscedasticRegression(x[:, np.newaxis], y, kern, Y_metadata=y_metadata)
            model.het_Gauss.variance.constrain_fixed(y_v.var(axis=1)[:, None])
        else:
            # kern += WhiteHetero(1, 1, np.var(y_v, axis=1))
            # model = GPy.models.GPHeteroscedasticRegression(x[:, np.newaxis], y, kern, Y_metadata=y_metadata)
            # model.het_Gauss.variance.constrain_fixed(0.01 * y_v.var(axis=1)[:, None])

            model = GPHeteroScaleRegression(x[:, np.newaxis], y, y_v.var(axis=1)[:, None], kern)
            model.het_Gauss.variance_scale.constrain_fixed(fixed_noise_scale)
    else:
        model = GPy.models.GPRegression(x[:, np.newaxis], y, kern)
        if fixed_noise:
            model.Gaussian_noise.variance.constrain_fixed(y_v.var())

    model.optimize_restarts(num_restarts=num_restarts, verbose=False,
                            num_processes=num_processes, parallel=num_processes > 1)

    if verbose:
        print('GPR: fitted model:')
        print(model)

    k_fg = get_kern_startwith(model.kern, 'fg')
    k_int_fg = get_kern_startwith(model.kern, 'int_fg')

    if k_int_fg is not None:
        k_fg = k_int_fg + k_fg

    y_fit, y_cov = model.predict(x[:, np.newaxis], full_cov=True, kern=k_fg,
                                 Y_metadata=y_metadata, include_likelihood=False)

    return model, y_fit, y_cov


def gpr_fit_with_model(x, y, data_scale, model, n_optimize_loop=0):
    y_flat = np.hstack((y.real, y.imag))
    scale_flat = np.hstack((data_scale.real, data_scale.imag))
    model = model.copy()
    model.set_Y((y_flat / scale_flat))

    k_fg = get_kern_startwith(model.kern, 'fg')
    k_int_fg = get_kern_startwith(model.kern, 'int_fg')

    if k_int_fg is not None:
        k_fg = k_int_fg + k_fg

    if n_optimize_loop > 0:
        model.optimize_restarts(n_optimize_loop, verbose=False)

    y_flat_fit, cov_err = model.predict(x[:, np.newaxis], full_cov=True, kern=k_fg,
                                        Y_metadata=model.Y_metadata, include_likelihood=False)

    y_flat_fit = y_flat_fit * scale_flat

    scale = scale_flat[:y.shape[1]].astype(complex)
    scale += 1j * scale_flat[y.shape[1]:]

    y_fit = y_flat_fit[:, :y.shape[1]].astype(complex)
    y_fit += 1j * y_flat_fit[:, y.shape[1]:]

    return GprResult(model, y_fit, y - y_fit, np.zeros_like(y_fit),
                     np.zeros_like(y_fit), cov_err, scale)


def gpr_fit_part(x, y, y_v, ru, gpr_config):
    '''Perform a single GPR on data y

    Args:
        x (n_freqs): Frequencies
        y (n_freqs, n_data): data cube
        y_v (n_freqs, n_data): noise data cube
        ru (n_data): Baseline equivalent (can be l mode) in lambda
        gpr_config (GprConfig): GPR configuration

    Returns:
        GprResult: GPR result
    '''
    if gpr_config.r_mean:
        # y = psutil.rmean(y)
        y = y - y.mean()
        if gpr_config.verbose:
            print('GPR: removing frequency mean')

    # Pre GPR run: either poly or PCA fit
    if gpr_config.pre_poly_fit_deg > 0:
        if gpr_config.verbose:
            print('GPR: running pre %s (deg %s) fit' % (gpr_config.pre_poly_fit_type, gpr_config.pre_poly_fit_deg))
        fit_fct = get_fit_fct(gpr_config.pre_poly_fit_type)
        y_pre_fit = alm_poly_fit(x, y, y_v.std(axis=1),
                                 deg=gpr_config.pre_poly_fit_deg,
                                 fit_fct=fit_fct)
    elif gpr_config.pre_pca_n > 0:
        if gpr_config.verbose:
            print('GPR: running pre PCA (%s cmpts) fit' % gpr_config.pre_pca_n)
        y_pre_fit = alm_pca_fit(y, gpr_config.pre_pca_n, verbose=gpr_config.verbose)
    else:
        y_pre_fit = np.zeros_like(y)

    # Flatten the data
    y_flat = np.hstack((y.real - y_pre_fit.real, y.imag - y_pre_fit.imag))
    y_v_flat = np.hstack((y_v.real, y_v.imag))

    if gpr_config.include_eor:
        kern = gpr_config.fg_kern + gpr_config.eor_kern
    else:
        kern = gpr_config.fg_kern + GPy.kern.White(1)
        # kern.white.variance.constrain_fixed(1e-50)

    if gpr_config.int_fg_kern is not None:
        kern = kern + gpr_config.int_fg_kern

    # The GPR model assume uniform noise for all l modes. This is not the case here, so we scale
    # it to have it as flat as possible, while trying to avoid introducing features.
    # d_ru = np.arange(ru.min(), ru.max(), gpr_config.noise_scale_delta_l / (2 * np.pi))
    # d_ru = np.concatenate([[0], d_ru[1:-1], [np.inf]])
    # noise_scale = np.ones_like(ru, dtype=float)
    noise_scale = psutil.mad(y_v, axis=0)
    # for ru_min, ru_max in psutil.pairwise(d_ru):
    #     idx = (ru >= ru_min) & (ru <= ru_max)
    #     noise_scale[idx] = psutil.robust_std(y_v.real[:, idx])
    #     noise_scale[idx] = np.std(y_v.real[:, idx])
    noise_scale = noise_scale / noise_scale.mean()
    noise_scale_flat = np.hstack((noise_scale, noise_scale))

    # scale_flat = 100 * y_v_flat.std() * noise_scale_flat
    scale_flat = gpr_config.data_scale_factor * y_flat.std() * noise_scale_flat

    # Run GPR
    if gpr_config.verbose:
        print('GPR: running GPR')
    model, y_flat_fit, cov_err = run_gpr(x, (y_flat / scale_flat), (y_v_flat / scale_flat), kern,
                                         verbose=gpr_config.verbose,
                                         num_restarts=gpr_config.num_restarts,
                                         heteroscedastic=gpr_config.heteroscedastic,
                                         fixed_noise=gpr_config.fixed_noise,
                                         fixed_noise_scale=gpr_config.fixed_noise_scale,
                                         num_processes=gpr_config.num_processes)

    # Unflat and rescale the data
    y_flat_fit = y_flat_fit * scale_flat

    scale = scale_flat[:y.shape[1]].astype(complex)
    scale += 1j * scale_flat[y.shape[1]:]

    y_fit = y_flat_fit[:, :y.shape[1]].astype(complex)
    y_fit += 1j * y_flat_fit[:, y.shape[1]:]

    y_fit += y_pre_fit

    # Post PCA run
    if gpr_config.post_pca_n > 0:
        if gpr_config.verbose:
            print('GPR: running post PCA (%s cmpts) fit' % gpr_config.post_pca_n)

        # n_freqs = cov_err.shape[0]
        # n_modes = len(scale)
        # err_r = np.random.multivariate_normal(np.zeros(n_freqs), cov_err, n_modes).T * scale.real
        # err_i = np.random.multivariate_normal(np.zeros(n_freqs), cov_err, n_modes).T * scale.imag
        # sample = err_r + 1j * err_i

        y_post_fit = alm_pca_fit(y - y_fit, gpr_config.post_pca_n, verbose=gpr_config.verbose)
        y_fit = y_fit + y_post_fit
    else:
        y_post_fit = np.zeros_like(y)

    y_sub = y - y_fit

    gpr_res = GprResult(model, y_fit, y_sub, y_pre_fit, y_post_fit, cov_err, scale)

    return gpr_res


def gpr_fit(x, y, y_v, ru, gpr_config):
    '''Perform a two pass GPR on data y, when first_run_pca_n is True

    Args:
        x (n_freqs): Frequencies
        y (n_freqs, n_data): data cube
        y_v (n_freqs, n_data): noise data cube
        ru (n_data): Baseline equivalent (can be l mode) in lambda
        gpr_config (GprConfig): GPR configuration

    Returns:
        GprResult: GPR result
    '''

    if gpr_config.first_run_pca_n > 0:
        # First run
        if gpr_config.verbose:
            print('\nGPR: first run')
        post_pca_n = gpr_config.post_pca_n
        include_eor = gpr_config.include_eor
        gpr_config.post_pca_n = gpr_config.first_run_pca_n
        gpr_config.include_eor = False
        gpr_res = gpr_fit_part(x, y, y_v, ru, gpr_config)

        first_run_pca = gpr_res.y_post_fit

        # Second run
        if gpr_config.verbose:
            print('\nGPR: second run')
        gpr_config.post_pca_n = post_pca_n
        gpr_config.include_eor = include_eor
        gpr_res = gpr_fit_part(x, y - first_run_pca, y_v, ru, gpr_config)

        gpr_res.first_run_pca = first_run_pca
        gpr_res.y_fit += first_run_pca
        gpr_res.y_post_fit += first_run_pca
    else:
        gpr_res = gpr_fit_part(x, y, y_v, ru, gpr_config)

    return gpr_res


def inv_pca(X, Y, pca, mode):
    if mode is None:
        return pca.inverse_transform(Y[:, :])
    if mode is not None:
        idx = slice(mode, mode + 1)
    else:
        idx = slice(None)
    if pca.whiten:
        s = np.sqrt(pca.explained_variance_[idx, np.newaxis])
    else:
        s = 1
    return np.dot(Y[:, idx], s * pca.components_[idx, :]) + pca.mean_[:]


def inv_pca_complex(X_real, X_imag, Y_real, Y_imag, pca_real, pca_imag, n_mode):
    Xrec_real = inv_pca(X_real, Y_real, pca_real, n_mode)
    Xrec_imag = inv_pca(X_imag, Y_imag, pca_imag, n_mode)

    return Xrec_real + 1j * Xrec_imag


def alm_pca_fit(alm, n_cmpt, verbose=True, return_mix=False):
    """Perform an n_cmpt PCA fit on data """
    X_real = alm.T.real
    X_imag = alm.T.imag
    pca_real = PCA(n_components=n_cmpt, whiten=True)
    pca_imag = PCA(n_components=n_cmpt, whiten=True)

    Y_real = pca_real.fit_transform(X_real)
    Y_imag = pca_imag.fit_transform(X_imag)

    if verbose:
        print('PCA: Percentage of variance explained:', pca_real.explained_variance_ratio_)

    inv_trans = functools.partial(inv_pca_complex, X_real, X_imag, Y_real, Y_imag, pca_real, pca_imag)

    alm_pca_fitted = inv_trans(None).T

    if return_mix:
        return alm_pca_fitted, (Y_real + 1j * Y_imag).T, inv_trans

    return alm_pca_fitted


def gmca_fit(X, n_cmpt, mints=0, do_wave_transform=False, do_poly_fit=0, X_n=None):
    """Perform an n_cmpt GMCA fit on real value X array """
    from pyGMCA.bss.amca import pyAMCA as pam
    from libwise import wtutils
    # from pyredwave import RedWave
    # from libwise import wtutils
    # from gmca import AGMCA
    # reload(AGMCA)
    n_scales = 6

    if do_wave_transform:
        # rw = RedWave(X, 0, isometric=True)
        # Xw = rw.forward(X)
        Xw = np.hstack(wtutils.wavedec(X, 'b1', n_scales, dec=wtutils.uiwt, axis=0, boundary='symm'))
    else:
        Xw = X

    # dS = AGMCA.dS
    # dS['n'] = n_cmpt
    # dS['t'] = Xw.shape[1]
    # dS['m'] = Xw.shape[0]

    # aS = AGMCA.aS
    # aS['kSMax'] = 0

    # norm = np.linalg.norm(Xw, axis=0)
    # perc = np.percentile(norm[norm > AGMCA.mad(norm)], 50)  # Do not trust the largest entries
    # X3 = Xw.copy()
    # X3[:, norm > perc] = 0
    # R = np.dot(X3, X3.T)
    # D, V = np.linalg.eig(R)
    # A = V[:, 0:dS['n']]
    # A = np.random.randn(dS['m'], dS['n'])

    # S, A = rGMCA()
    # S, A = AGMCA.AMCA(Xw, A, dS, aS, 0)
    # S, A, _ = AGMCA.rGMCA(X, A, dS, aS)

    S, A = pam.AMCA(Xw, n_cmpt, mints=mints)

    # import gmcalab
    # reload(gmcalab)
    # res = gmcalab.GMCA(Xw.T, n=n_cmpt, UseP=1, mints=0, Init=1)
    # S = res['sources']
    # A = res['mixmat']

    if do_wave_transform:
        # Y = rw.backward(np.dot(A, S).real)
        Y = wtutils.waverec(np.split(np.dot(A, S).real, n_scales + 1, axis=1),
                            'b1', rec=wtutils.uiwt_inv, axis=0, boundary='symm')
    else:
        Y = np.dot(A, S).real

    if do_poly_fit > 0:
        Y = alm_poly_fit(np.arange(X.shape[0]), Y, np.ones(X.shape[0]), do_poly_fit,
                         fit_fct=bernstein_fit)

    return Y


def alm_gmca_fit(alm, n_cmpt, alm_n, mints=0, do_wave_transform=False, do_poly_fit=0):
    """Perform an n_cmpt GMCA fit on complex value X array """
    Yr = gmca_fit(alm.real, n_cmpt, mints=mints, do_wave_transform=do_wave_transform,
                  do_poly_fit=do_poly_fit, X_n=alm_n)
    Yi = gmca_fit(alm.imag, n_cmpt, mints=mints, do_wave_transform=do_wave_transform,
                  do_poly_fit=do_poly_fit, X_n=alm_n)

    return Yr + 1j * Yi


def bernstein_poly(i, n, x):
    return comb(n, i) * (x ** (n - i)) * (1 - x)**i


def poly_fit(x, y, noiserms, deg, min_deg=0, full_cov=False):
    C_Dinv = np.diagflat(1 / noiserms ** 2)
    A = np.vstack([x ** k for k in np.arange(min_deg, deg + 1)]).T

    lhs = np.dot(np.dot(A.T, C_Dinv), A)
    rhs = np.dot(np.dot(A.T, C_Dinv), y)

    s = np.linalg.solve(lhs, rhs)
    y_s = np.dot(A, s)

    if full_cov:
        cov_sigma = np.dot(np.dot(A, np.linalg.inv(lhs)), A.T)
    else:
        cov_sigma = np.sqrt(np.diag(np.linalg.inv(lhs)))

    return s, y_s, cov_sigma


def bernstein_fit(x, y, noiserms, deg, full_cov=False):
    ber_basis = []
    for j in range(deg):
        for i in range(j + 1):
            ber_basis.append(bernstein_poly(i, j, x))

    C_Dinv = np.diagflat(1 / noiserms ** 2)
    A = np.vstack(ber_basis).T

    lhs = np.dot(np.dot(A.T, C_Dinv), A)
    rhs = np.dot(np.dot(A.T, C_Dinv), y)

    s = np.linalg.solve(lhs, rhs)

    if full_cov:
        cov_sigma = np.dot(np.dot(A, np.linalg.pinv(lhs)), A.T)
    else:
        cov_sigma = np.sqrt(np.diag(np.linalg.inv(lhs)))

    y_s = np.dot(A, s)

    return s, y_s, cov_sigma


def powerlaw_fit(x, y, noiserms, deg, min_deg=0, bernstein=False, offset=True, output_parameters=False):
    if x[0] > 0:
        x = x / x[0]
    sgn = np.sign(np.mean(y))
    y_m = y * sgn
    if offset:
        offset = - 10 * min(np.min(y), -0.05)
    else:
        offset = 0
    y_m += offset

    if bernstein:
        s, y_s, cov_sigma = bernstein_fit(np.log(x), np.log(y_m), noiserms, deg)
    else:
        s, y_s, cov_sigma = poly_fit(np.log(x), np.log(y_m), noiserms, deg, min_deg=min_deg)
    y_s = sgn * (np.exp(y_s) - offset)

    if output_parameters:
        return y_s, s

    return y_s


def powerlaw_fit_bernstein(x, y, noiserms, deg):
    return powerlaw_fit(x, y, noiserms, deg, bernstein=True)


def get_fit_fct(fit_type):
    if fit_type == 'poly':
        return poly_fit
    elif fit_type == 'bernstein':
        return bernstein_fit
    elif fit_type == 'power_poly':
        return powerlaw_fit
    elif fit_type == 'power_bernstein':
        return powerlaw_fit_bernstein
    else:
        print("Error: fit_type '%s' invalid" % fit_type)


def alm_poly_fit(freqs, alm, noiserms, deg, fit_fct=powerlaw_fit, **kargs):
    res = fit_fct(freqs, alm, noiserms, deg, **kargs)

    if len(res) == 3:
        res = res[1]

    return res


def fit_cl_cube_poly(cube, du=10, poly_deg=4, log=True):
    uv_bins = np.arange(cube.ru.min(), cube.ru.max(), du)
    uv_mean = np.array([(a + b) / 2 for (a, b) in psutil.pairwise(uv_bins)])
    if cube.weights is not None:
        w = cube.weights.data
    else:
        w = None
    ps, ps_err, _, _ = pscart.get_cross_power_spectra(cube.data, cube.data, cube.uu, cube.vv, 2 * np.pi * uv_mean, weight_cube=w, uniform_bins=True)
    ps = ps.real.mean(axis=0)
    ps_err = ps_err.real.mean(axis=0)
    
    if log:
        fit_fct = psutil.polynomial_fit_log(uv_mean, ps, ps_err, poly_deg)
    else:
        fit_fct = psutil.polynomial_fit(uv_mean, ps, ps_err, poly_deg)
    
    return fit_fct, uv_mean, ps, ps_err
