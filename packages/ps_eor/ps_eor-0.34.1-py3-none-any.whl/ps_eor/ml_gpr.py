import os
import re
import sys
import fnmatch
from functools import lru_cache

import numpy as np

import scipy.interpolate
import scipy.stats as stats
from scipy.integrate import trapz as trapezoid

import matplotlib.pyplot as plt

import astropy.stats as astats

try:
    import GPy
    import paramz
    from paramz.transformations import Logexp
except ImportError as e:
    raise ImportError("GPy is not installed. Install with `pip install ps_eor[ml-gpr]`")

import emcee
import corner
import dynesty
import ultranest

import joblib
import progressbar

import torch
from torch import nn
from torch.utils.data import DataLoader

from sklearn.decomposition import PCA

from libpipe import settings

from . import psutil, datacube, pspec, fgfit, fitutil


CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')


class BetaVAE(nn.Module):
    ''' Base on https://github.com/AntixK/PyTorch-VAE/blob/master/models/beta_vae.py'''

    num_iter = 0

    def __init__(self, in_dim, latent_dim, hidden_dims=[20, 20, 20], beta=1, warmup_iters=100, 
                 warmup_gamma=0.001, loss_type='H', fc_hidden_dim=None, **kwargs):
        super(BetaVAE, self).__init__()

        self.latent_dim = latent_dim
        self.beta = beta
        self.warmup_iters = warmup_iters
        self.warmup_gamma = warmup_gamma
        self.loss_type = loss_type

        modules = []

        # Build Encoder
        for i_d, o_d in zip([in_dim] + hidden_dims[:-1], hidden_dims):
            modules.append(
                nn.Sequential(
                    nn.Linear(i_d, o_d),
                    nn.LeakyReLU(),
                    nn.BatchNorm1d(o_d),
                )
            )

        self.encoder = nn.Sequential(*modules)

        if fc_hidden_dim is not None:
            self.fc_mu = nn.Sequential(nn.Linear(hidden_dims[-1], fc_hidden_dim), nn.LeakyReLU(), 
                                       nn.Linear(fc_hidden_dim, latent_dim))
            self.fc_var = nn.Sequential(nn.Linear(hidden_dims[-1], fc_hidden_dim), nn.LeakyReLU(), 
                                        nn.Linear(fc_hidden_dim, latent_dim))
        else:
            self.fc_mu = nn.Linear(hidden_dims[-1], latent_dim)
            self.fc_var = nn.Linear(hidden_dims[-1], latent_dim)

        # Build Decoder
        modules = []

        self.decoder_input = nn.Linear(latent_dim, hidden_dims[-1])

        hidden_dims.reverse()

        for i in range(len(hidden_dims) - 1):
            modules.append(
                nn.Sequential(
                    nn.Linear(hidden_dims[i], hidden_dims[i + 1]),
                    nn.LeakyReLU(),
                )
            )

        modules.append(nn.Sequential(nn.Linear(hidden_dims[-1], in_dim), nn.Sigmoid()))

        self.decoder = nn.Sequential(*modules)
        self.iter_changed = False

    def encode(self, input):
        """
        Encodes the input by passing through the encoder network
        and returns the latent codes.
        :param input: (Tensor) Input tensor to encoder [N x C x H x W]
        :return: (Tensor) List of latent codes
        """
        result = self.encoder(input)

        # Split the result into mu and var components
        mu = self.fc_mu(result)
        log_var = self.fc_var(result)

        return [mu, log_var]

    def decode(self, z):
        result = self.decoder_input(z)
        result = self.decoder(result)
        return result

    def reparameterize(self, mu, logvar):
        """
        :param mu: (Tensor) Mean of the latent Gaussian
        :param logvar: (Tensor) Standard deviation of the latent Gaussian
        :return:
        """
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return eps * std + mu

    def forward(self, input, **kwargs):
        mu, log_var = self.encode(input)
        z = self.reparameterize(mu, log_var)
        return  [self.decode(z), input, mu, log_var]

    def step(self):
        self.num_iter += 1
        self.iter_changed = True

    def loss_function(self, *args, **kwargs):
        recons = args[0]
        input = args[1]
        mu = args[2]
        log_var = args[3]
        n = recons.shape[0]

        recons_loss = n * torch.nn.functional.mse_loss(recons, input)
        kld_loss = n * torch.mean(-0.5 * torch.sum(1 + log_var - mu ** 2 - log_var.exp(), dim = 1), dim = 0)

        if self.loss_type == 'H': # https://openreview.net/forum?id=Sy2fzU9gl
            loss = recons_loss + self.beta * kld_loss
        elif self.loss_type == 'W':
            beta = self.beta
            if self.num_iter < self.warmup_iters:
                beta = self.beta * (self.warmup_gamma + (1 - self.warmup_gamma) * self.num_iter / self.warmup_iters)
            loss = recons_loss + beta * kld_loss
        else:
            raise ValueError('Undefined loss type.')
        self.iter_changed = False

        return loss, recons_loss, kld_loss

    def generate(self, x, **kwargs):
        """
        Given an input image x, returns the reconstructed image
        :param x: (Tensor) [B x C x H x W]
        :return: (Tensor) [B x C x H x W]
        """

        return self.forward(x)[0]

    def generate_m(self, x):
        mu, log_var = self.encode(x)
        return self.decode(mu)


class PreProcessor(object):
    
    def process(self, ps_data, n_sigma_clip=3):
        data_sum = ps_data.sum(axis=1)
        mask_zero = ~(data_sum < 1e-20)
        print('Discarding PS with zero power:', (~mask_zero).sum())
        
        data_sum_log = np.log10(data_sum[mask_zero])
        data_sum_log[~np.isfinite(data_sum_log)] = -1e5
        mask = astats.sigma_clip(data_sum_log, sigma=3, stdfunc=psutil.robust_std).mask
        print('Discarding outliers PS:', (mask).sum())
        
        ps_data = ps_data[mask_zero][~mask]

        return ps_data / ps_data.sum(axis=1)[:, None]

    def inv(self, ps):
        return ps


class PreProcessorFlatten(PreProcessor):
    
    def __init__(self, k_mean, alpha=1):
        self.k_mean = k_mean
        self.alpha = alpha

    def process(self, ps_data, n_sigma_clip=3):
        ps_data = PreProcessor.process(self, ps_data, n_sigma_clip=n_sigma_clip)

        ps_data = ps_data / self.k_mean ** self.alpha
        norm_factor = ps_data.max()
        ps_data = ps_data / norm_factor
        
        return ps_data
        
    def inv(self, ps):
        return self.k_mean * ps


class PreProcessorLogScale(PreProcessor):
    
    def __init__(self, k_mean):
        self.k_mean = k_mean
        self.norm_factor = 1

    def process(self, ps_data, n_sigma_clip=3):
        ps_data = PreProcessor.process(self, ps_data, n_sigma_clip=n_sigma_clip)

        ps_data = np.log10(ps_data)
        self.norm_factor = (- ps_data).max()
        ps_data = - ps_data / self.norm_factor
        
        return ps_data
        
    def inv(self, ps):
        return 10 ** (-self.norm_factor * ps)


class AbstractFitter(object):

    def __init__(self, n_dim, k_mean):
        self.n_dim = n_dim
        self.k_mean = k_mean

    def encode(self, data):
        raise NotImplementedError()

    def decode(self, data):
        raise NotImplementedError()

    def reconstruct(self, data):
        raise NotImplementedError()

    def save(self, filename):
        joblib.dump(self, filename)
        
    @staticmethod
    @lru_cache(maxsize=10)
    def _cache_load(filename, mtime):
        return joblib.load(filename)

    @staticmethod
    def load(filename):
        sys.modules['ml_gpr'] = sys.modules[__name__]
        return AbstractFitter._cache_load(filename, os.stat(filename).st_mtime)


class VAEFitter(AbstractFitter):

    def __init__(self, model, optimizer, k_mean):
        self.model = model
        self.optimizer = optimizer
        self.loss = []
        self.val_loss = []
        self.all_rec_loss = []
        AbstractFitter.__init__(self, model.latent_dim, k_mean)

    def fit(self, dataloader):
        self.model.train()
        # total loss, reconstruction loss, KL loss
        running_loss = np.array([0., 0., 0.])
        for data in dataloader:
            self.optimizer.zero_grad()
            reconstruction, inp, mu, logvar = self.model.forward(data)
            loss, recons_loss, kld_loss = self.model.loss_function(reconstruction, inp, mu, logvar)
            running_loss += np.array([loss.data, recons_loss.data, kld_loss.data])
            self.all_rec_loss.append(recons_loss.data)
            loss.backward()
            self.optimizer.step()
        train_loss = running_loss / len(dataloader.dataset)
        return train_loss

    def validate(self, dataloader):
        self.model.eval()
        # total loss, reconstruction loss, KL loss
        running_loss = np.array([0., 0., 0.])
        with torch.no_grad():
            for data in dataloader:
                reconstruction, inp, mu, logvar = self.model.forward(data)
                loss, recons_loss, kld_loss = self.model.loss_function(reconstruction, inp, mu, logvar, M_N=1)
                running_loss += np.array([loss.data, recons_loss.data, kld_loss.data])
        val_loss = running_loss / len(dataloader.dataset)
        return val_loss

    def train(self, epochs, train_loader, val_loader):
        widgets = [
            "VAE Fitter ", progressbar.Percentage(), ' (',
            progressbar.SimpleProgress(), ')'
            ' ', progressbar.Bar(marker='|', left='[', right=']'),
            ' ', progressbar.ETA(),
            ' ', progressbar.DynamicMessage('Loss')
        ]
        with progressbar.ProgressBar(max_value=epochs, widgets=widgets, redirect_stdout=True) as bar:
            current_loss = np.nan
            for i in range(epochs):
                self.loss.append(self.fit(train_loader))
                self.val_loss.append(self.validate(val_loader))
                if i % 10 == 0:
                    current_loss = self.loss[-1][0]
                bar.update(i, Loss=current_loss)
                self.model.step()
        self.model.eval()

    def ensure_tensor(self, data):
        if not torch.is_tensor(data):
            return torch.DoubleTensor(data)
        return data

    def ensure_np(self, data):
        if torch.is_tensor(data):
            return data.data.numpy()
        return data

    def encode(self, data):
        return self.ensure_np(self.model.reparameterize(*self.model.encode(self.ensure_tensor(data))))

    def decode(self, latent_data):
        return self.ensure_np(self.model.decode(self.ensure_tensor(latent_data)))

    def reconstruct(self, data):
        return self.ensure_np(self.model.generate_m(self.ensure_tensor(data)))


class PCAFitter(AbstractFitter):

    def __init__(self, n_cmpt, k_mean):
        self.pca = PCA(n_components=n_cmpt)
        self.y_min = [0, 0]
        self.y_max = [0, 0]
        AbstractFitter.__init__(self, n_cmpt, k_mean)

    def train(self, train_set):
        Y = self.pca.fit_transform(train_set)
        self.y_min = Y.min(axis=0)
        self.y_max = Y.max(axis=0)

    def encode(self, data):
        return self.pca.transform(data)

    def decode(self, latent_data):
        return self.pca.inverse_transform(latent_data)

    def reconstruct(self, data):
        return self.pca.inverse_transform(self.pca.transform(data))


class VAEFitterPreProc(VAEFitter):

    def __init__(self, model, optimizer, pre_proc):
        self.model = model
        self.optimizer = optimizer
        self.loss = []
        self.val_loss = []
        self.all_rec_loss = []
        self.pre_proc = pre_proc
        AbstractFitter.__init__(self, model.latent_dim, pre_proc.k_mean)

    def train(self, epochs, train_data, frac_validation=0.1, batch_size=128):
        train_data = self.pre_proc.process(train_data.copy())

        np.random.shuffle(train_data)

        i = int(train_data.shape[0] * (1 - frac_validation))
        val_data = train_data[i:]
        train_data = train_data[:i]
        print(f'Training set: {train_data.shape[0]}, Validation set: {val_data.shape[0]}')

        train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=True)

        VAEFitter.train(self, epochs, train_loader, val_loader)
        
        return FitterResult(self, train_loader, val_loader)


class FitterResult(AbstractFitter):

    def __init__(self, fitter, train_data, test_data):
        self.fitter = fitter
        if isinstance(train_data, DataLoader):
            train_data = train_data.dataset
        if isinstance(test_data, DataLoader):
            test_data = test_data.dataset
        self.train_data = train_data
        self.test_data = test_data

    def plot_loss(self):
        if not hasattr(self.fitter, 'loss'):
            return None

        fig, ax = plt.subplots()
        ax.plot(np.array(self.fitter.loss)[:, 1], label='reconstruction loss')
        ax.plot(np.array(self.fitter.val_loss)[:, 1], label='reconstruction loss (val)')
        ax.plot(np.array(self.fitter.loss)[:, 2] * self.fitter.model.beta, label='KL loss')
        ax.set_yscale('log')
        ax.set_xlabel('Epochs')
        ax.set_ylabel('Loss')
        ax.legend()

        return fig

    def plot_latent_qq(self):
        fig, ax = plt.subplots()
        for data, data_label in zip([self.train_data, self.test_data], ['training', 'validation']):
            latent_params = self.fitter.encode(data).T

            ((osm, osr), _) = stats.probplot(latent_params[0], dist="norm")
            ax.scatter(osm, osr, s=10, label=f'Dim 0 ({data_label})')

            ((osm, osr), _) = stats.probplot(latent_params[1], dist="norm")
            ax.scatter(osm, osr, s=10, label=f'Dim 1 ({data_label})')

        ax.set_xlabel('Theoretical Quantile')
        ax.set_ylabel('Observed Quantile')
        ax.plot(osm, osm, c=psutil.red, lw=2)
        ax.legend()

        return fig

    def get_reco_ratio_train(self):
        rec = self.fitter.reconstruct(self.train_data)
        return (rec / self.train_data)

    def get_reco_ratio_val(self):
        rec = self.fitter.reconstruct(self.test_data)
        return (rec / self.test_data)

    def plot_ratio(self):
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(9, 3), sharey=True)
        ratio_train = self.get_reco_ratio_train()
        ratio_val = self.get_reco_ratio_val()

        ax1.boxplot(ratio_train, sym='')
        ax2.boxplot(ratio_val, sym='')

        med, rms = np.median(ratio_train), ratio_train.std()
        ax1.text(0.05, 0.97, f'Training set:median:{med:.3f} rms:{rms:.3f}', 
                 transform=ax1.transAxes, va='top', ha='left')

        med, rms = np.median(ratio_val), ratio_val.std()
        ax2.text(0.05, 0.97, f'Validation set:median:{med:.3f} rms:{rms:.3f}', 
                 transform=ax2.transAxes, va='top', ha='left')

        fig.tight_layout()

        return fig


def make_new_vis_cube(res, n_pix, freqs, umin, umax, kern=None, K=None, uv_bins_du=None, uv_bins=None, uv_bins_n_uni=0):
    ''' Make a datacube.CartDataCube object with data generated 
        from the frequency-frequency covariance kern.

        Either a GPy Kern object (kern) or a frequency-frequency covariance (K) can be given.

        In case of multi baselines kernels (MultiKern), you can either set
        the uv bins steps (uv_bins_du) or if the covariance is defined by a MultiKern, 
        you can set the uv bins with kern.set_uv_bins(...) before calling this function.'''
    uu, vv, _ = psutil.get_ungrid_vis_idx((n_pix, n_pix), res, umin, umax)

    meta = datacube.ImageMetaData.from_res(res, (n_pix, n_pix))
    meta.wcs.wcs.cdelt[2] = psutil.robust_freq_width(freqs)

    c = datacube.CartDataCube(np.zeros((len(freqs), len(uu)), dtype=np.complex128), uu, vv, freqs, meta)

    return make_new_from_cube(c, kern=kern, K=K, uv_bins_du=uv_bins_du, uv_bins=uv_bins, uv_bins_n_uni=uv_bins_n_uni)


def make_new_from_cube(i_cube, kern=None, K=None, uv_bins_du=None, uv_bins=None, uv_bins_n_uni=0):
    ''' Make a datacube.CartDataCube object using a template from an other datacube
        and with data generated from the GPy kern object or the frequency-frequency covariance (K).

        In case of multi baselines kernels (MultiKern), you can either set
        the uv bin width (uv_bins_du) or if the covariance is defined by a MultiKern, 
        you can set the uv bins with kern.set_uv_bins(...) before calling this function.'''
    c = i_cube.new_with_data(np.zeros_like(i_cube.data))

    assert (kern is None) ^ (K is None), 'both kern and K should not be set'

    fmhz = c.freqs * 1e-6
    if uv_bins is None:
        if uv_bins_n_uni > 0:
            uv_bins = get_n_uniform_uv_bins(i_cube.ru.min(), i_cube.ru.max(), uv_bins_n_uni)
        elif uv_bins_du != None:
            uv_bins = get_uv_bins(i_cube.ru.min(), i_cube.ru.max(), uv_bins_du)
        else:
            uv_bins = [(c.ru.min(), c.ru.max())]

    if kern is not None:
        if isinstance(kern, MultiKern):
            kern.set_uv_bins(uv_bins)
            uv_bins = kern.uv_bins
            kern.set_mean_fmhz(fmhz.mean())
        K = kern.K(fmhz[:, None], fmhz[:, None])

    if K is not None:
        if uv_bins is None:
            c.data = get_samples(fmhz, len(c.ru), K)
        else:
            for (umin, umax), Ki in zip(uv_bins, K):
                idx = (c.ru >= umin) & (c.ru <= umax)
                c.data[:, idx] = get_samples(fmhz, np.sum(idx), Ki)

    return c


def get_uv_bins(umin, umax, du):
    '''Return uv bins from umin to umax with a bin width of du'''
    return psutil.pairwise(np.arange(umin, umax + du, du))


def get_n_uniform_uv_bins(u_min, u_max, n_bins):
    ''' Return uv bins with similar nbs of cells in each bins'''
    radii_analytical = [np.sqrt(((i / n_bins) * (u_max**2 - u_min**2)) + u_min**2) for i in range(1, n_bins)]
    bin_edges_radius = np.concatenate(([u_min], radii_analytical, [u_max]))
    return psutil.pairwise(bin_edges_radius)



def get_samples(X, n, K, complex_type=True, nearest_pd=True, method='svd'):
    '''Return n samples from the freq-freq covariance K'''
    if nearest_pd and not is_positive_definite(K):
        K = nearest_postive_definite(K)
    rg = np.random.default_rng()
    d = rg.multivariate_normal(np.zeros_like(X).squeeze(), K, n, method=method).T
    if complex_type:
        d = d + 1j *rg.multivariate_normal(np.zeros_like(X).squeeze(), K, n, method=method).T
    return d


def get_multi_samples(X, ns, Ks):
    '''Return ns samples from the freq-freq multi-baselines covariance Ks'''
    return [get_samples(X, n, K) for n, K in zip(ns, Ks)]


def nearest_postive_definite(A, maxtries=10):
    """Find the nearest positive-definite matrix to input

    A Python/Numpy port of John D'Errico's `nearestSPD` MATLAB code [1], which
    credits [2].

    [1] https://www.mathworks.com/matlabcentral/fileexchange/42885-nearestspd

    [2] N.J. Higham, "Computing a nearest symmetric positive semidefinite
    matrix" (1988): https://doi.org/10.1016/0024-3795(88)90223-6
    """
    B = (A + A.T) / 2
    _, s, V = np.linalg.svd(B)

    H = np.dot(V.T, np.dot(np.diag(s), V))

    A2 = (B + H) / 2

    A3 = (A2 + A2.T) / 2

    if is_positive_definite(A3):
        return A3

    spacing = np.spacing(np.linalg.norm(A))
    I = np.eye(A.shape[0])
    k = 1
    while not is_positive_definite(A3):
        mineig = np.min(np.real(np.linalg.eigvals(A3)))
        A3 += I * (-mineig * k**2 + spacing)
        k += 1
        if k > maxtries:
            break

    return A3


def is_positive_definite(B):
    """Returns true when input is positive-definite, via Cholesky"""
    try:
        _ = GPy.util.linalg.jitchol(B, 0)
        return True
    except np.linalg.LinAlgError:
        return False


class CovarianceGenerator(object):
    
    @lru_cache(maxsize=10)
    def __init__(self, freqs, uv_bins, log_scale_interpolatation=True, padding=2, interp_kind='quadratic'):
        self.log_scale_interpolatation = log_scale_interpolatation
        self.padding = padding
        self.interp_kind = interp_kind
        self.freqs = np.array(freqs)
        self.uv_bins = np.array(uv_bins)
        z = psutil.freq_to_z(self.freqs.mean())

        uu = self.uv_bins.mean(axis=1)
        self.k_per = psutil.l_to_k(2 * np.pi * uu, z)

        r = psutil.angular_to_comoving_distance(psutil.freq_to_z(self.freqs))
        self.delta_r = abs(r - r[0])

        d_delta_r = np.diff(self.delta_r).mean()
        k_par_max = np.pi  / d_delta_r
        self.k_par = np.arange(0, padding * k_par_max, k_par_max / len(r))
        
        self.cos_r_k = np.cos(self.delta_r[None, None, :] * self.k_par[:, None, None])
        self.k = np.sqrt(self.k_per[None, :, None] ** 2 + self.k_par[:, None, None] ** 2)

    def c_nu_from_ps21_fct(self, ps3d_fct, normalize=True):
        y = ps3d_fct(self.k) * self.cos_r_k
        c_nu_nu = trapezoid(y, self.k_par, axis=0)

        if normalize:
            c_nu_nu = c_nu_nu / c_nu_nu.max()

        c_nu_nu[~np.isfinite(c_nu_nu)] = 0

        return c_nu_nu

    def c_nu_from_ps21(self, k_mean, ps3d, normalize=True):
        '''Return frequency-frequency covariance for the given baselines bins and frequency 
           given the spherically averaged power-spectra delta(k) (and not P(k)).
           Assume isotropic of the signal, which is true to some extend for the 21-cm signal.

           See https://arxiv.org/abs/astro-ph/0605546'''
        def ps_fct(k):
            if self.log_scale_interpolatation:
                return 1 / k ** 3 * 10 ** scipy.interpolate.interp1d(np.log10(k_mean), np.log10(ps3d), bounds_error=False,
                                                                     kind=self.interp_kind, fill_value='extrapolate')(np.log10(k))
            else:
                return 1 / k ** 3 * scipy.interpolate.interp1d(k_mean, ps3d, bounds_error=False, kind=self.interp_kind,
                                                               fill_value='extrapolate')(k)

        return self.c_nu_from_ps21_fct(ps_fct, normalize=normalize)


@lru_cache(maxsize=10)
def get_cached_cov_gen(freqs, uv_bins):
    return CovarianceGenerator(freqs, uv_bins)


def c_nu_to_K(freqs, c_nu_nu):
    ''' return a covariance matrix K from freq-freq covariance c_nu_nu'''
    X = (freqs * 1e-6)[:, None]
    r_1d = abs(freqs - freqs[0]) * 1e-6

    r = get_unscaled_dist(tuple(X.flatten()))

    return scipy.interpolate.interp1d(r_1d, c_nu_nu, kind='quadratic', axis=1,
                                      bounds_error=False, fill_value=0)(r)


def make_new_vis_cube_from_ps(k_mean, ps3d, res, n_pix, freqs, umin, umax, uv_bins_du=15):
    ''' Make a datacube.CartDataCube object with given power-spectra ((delta(k))).

        See also c_nu_from_ps21() and make_new_vis_cube() '''
    uv_bins = get_uv_bins(umin, umax, uv_bins_du)
    cov_gen = get_cached_cov_gen(tuple(freqs), tuple(uv_bins))
    c_nu_nu = cov_gen.c_nu_from_ps21(k_mean, ps3d, normalize=False)
    K = c_nu_to_K(freqs, c_nu_nu)

    z = psutil.freq_to_z(freqs.mean())
    r_z = psutil.cosmo.comoving_distance(z).value / psutil.cosmo.h
    norm = 0.16 / (res * n_pix) ** 4 * 1 / (np.pi * r_z ** 2)
    K = norm * K

    return make_new_vis_cube(res, n_pix, freqs, umin, umax, K=K, uv_bins_du=uv_bins_du)


@lru_cache()
def get_unscaled_dist(X, X2=None):
    X = np.array(X)[:, None]
    if X2 is None:
        Xsq = np.sum(np.square(X),1)
        r2 = -2. * np.dot(X, X.T) + (Xsq[:, None] + Xsq[None, :])
        r2[np.diag_indices(X.shape[0])] = 0.
        r2 = np.clip(r2, 0, np.inf)
        return np.sqrt(r2)
    else:
        X2 = np.array(X2)[:, None]
        #X2, = self._slice_X(X2)
        X1sq = np.sum(np.square(X),1)
        X2sq = np.sum(np.square(X2),1)
        r2 = -2.*np.dot(X, X2.T) + (X1sq[:,None] + X2sq[None,:])
        r2 = np.clip(r2, 0, np.inf)
        return np.sqrt(r2)


class MultiKern(GPy.kern.Kern):
    ''' Multi Baseline Kernel. '''

    def __init__(self, *args, **kargs):
        self.uv_bins = [[0, 1e4]]
        self.mean_fmhz = 120
        self.uv_ps_fct = lambda u: 0 * u + 1

    def set_uv_bins(self, uv_bins):
        ''' Set the uv bins for this kernel. '''
        self.uv_bins = uv_bins
        self.parameters_changed()

    def set_mean_fmhz(self, mean_fmhz):
        self.mean_fmhz = mean_fmhz
        self.parameters_changed()

    def set_uv_ps_fct(self, uv_ps_fct):
        self.uv_ps_fct = uv_ps_fct
        self.parameters_changed()

    def add(self, other, name='sum'):
        assert isinstance(other, MultiKern), "only kernels can be added to kernels..."
        return MultiAdd([self, other], name=name)

    def prod(self, other, name='prod'):
        assert isinstance(other, MultiKern), "only kernels can be multiplied with other kernels..."
        return MultiProd([self, other], name=name)

    def copy_params(self, other):
        [self.unlink_parameter(k) for k in self.params]
        self.params = [k.copy() for k in other.params]
        self.link_parameters(*self.params)
        self._connect_parameters()
        self._connect_fixes()
        self._notify_parent_change()
        self.uv_bins = other.uv_bins

    @staticmethod
    def _parse_set_prior_from_dict(param, d):
        klasses = GPy.core.parameterization.priors.Prior.__subclasses__()
        [klasses.extend(k.__subclasses__()) for k in klasses[:]]

        all_priors_classes = {k.__name__: k for k in klasses}
        if 'prior' in d:
            re_match = re.match(r'(\w+)\s*\((.*)\)', d['prior'])
            if not re_match or len(re_match.groups()) != 2:
                raise ValueError(f"Error parsing prior: {d['prior']}")
            prior_class, args = re_match.groups()
            if prior_class == 'Fixed':
                param.constrain_fixed(value=float(args))
            elif prior_class in all_priors_classes:
                param.unconstrain()
                klass = all_priors_classes[prior_class]
                param.set_prior(klass(*[float(k.strip()) for k in args.split(',')]))
            else:
                raise ValueError(f"Error parsing prior, unknown class name: {d['prior']}")
        if 'log_scale' in d and d['log_scale']:
            param.constrain(Exponent10())

        return param

    @staticmethod
    def _parse_set_params_from_dict(params, d):
        for param in params.parameters:
            if param.name in d:
                MultiKern._parse_set_prior_from_dict(param, d[param.name])
            elif param.is_fixed:
                continue
            else:
                raise ValueError(f"Error parameter missing from configuration: {param.hierarchy_name()}")
        return params

    @staticmethod
    def load_from_dict(name, d):
        raise NotImplementedError()


class MultiAdd(MultiKern, GPy.kern.Add):

    def __init__(self, sub_kerns, name='sum'):
        for kern in sub_kerns:
            assert isinstance(kern, MultiKern)
        GPy.kern.Add.__init__(self, sub_kerns, name=name)
        MultiKern.__init__(self)
        self.set_uv_bins(sub_kerns[0].uv_bins)
        self.set_mean_fmhz(sub_kerns[0].mean_fmhz)
        self.set_uv_ps_fct(sub_kerns[0].uv_ps_fct)

    def set_uv_ps_fct(self, uv_ps_fct):
        for k_part in self.parts:
            k_part.set_uv_ps_fct(uv_ps_fct)
        MultiKern.set_uv_ps_fct(self, uv_ps_fct)

    def set_uv_bins(self, uv_bins):
        for k_part in self.parts:
            k_part.set_uv_bins(uv_bins)
        MultiKern.set_uv_bins(self, uv_bins)

    def set_mean_fmhz(self, mean_fmhz):
        for k_part in self.parts:
            k_part.set_mean_fmhz(mean_fmhz)
        MultiKern.set_mean_fmhz(self, mean_fmhz)


class MultiProd(MultiKern, GPy.kern.Prod):

    def __init__(self, sub_kerns, name='prod'):
        for kern in sub_kerns:
            assert isinstance(kern, MultiKern)
        GPy.kern.Prod.__init__(self, sub_kerns, name=name)
        MultiKern.__init__(self)
        self.set_uv_bins(sub_kerns[0].uv_bins)
        self.set_mean_fmhz(sub_kerns[0].mean_fmhz)
        self.set_uv_ps_fct(sub_kerns[0].uv_ps_fct)

    def set_uv_ps_fct(self, uv_ps_fct):
        for k_part in self.parts:
            k_part.set_uv_ps_fct(uv_ps_fct)
        MultiKern.set_uv_ps_fct(self, uv_ps_fct)

    def set_uv_bins(self, uv_bins):
        for k_part in self.parts:
            k_part.set_uv_bins(uv_bins)
        MultiKern.set_uv_bins(self, uv_bins)

    def set_mean_fmhz(self, mean_fmhz):
        for k_part in self.parts:
            k_part.set_mean_fmhz(mean_fmhz)
        MultiKern.set_mean_fmhz(self, mean_fmhz)


class Stationary(object):
    
    # Use faster and cached version of _unscaled_dist
    def _unscaled_dist(self, X, X2=None):
        if X2 is not None:
            X2 = tuple(X2.flatten()) 
        return get_unscaled_dist(tuple(X.flatten()), X2)


class AbstractMLKern(Stationary, MultiKern, GPy.kern.Kern):
    ''' ML Kernel implementation '''

    def __init__(self, latent_dim, name='ml_kern', param_values=[]):
        ''' Initialize a VAE kernel with ml_decoder given the dimension of the latent space latent_dim, 
            and the k_mean of the traing sets (ps3d_k_mean).'''
        GPy.kern.Kern.__init__(self, 1, 0, name)
        self.latent_dim = latent_dim
        self.params = [GPy.core.parameterization.Param(f'x{i + 1}', 0, ) for i in range(self.latent_dim)]
        self.params.append(GPy.core.parameterization.Param('variance', 1, Logexp()))
        self.link_parameters(*self.params)
        for i, pvalue in zip(range(self.latent_dim), param_values):
            setattr(self, f'x{i + 1}', pvalue)
        self.params_call = []
        MultiKern.__init__(self)

    def set_latent_space_normal_prior(self, nsigma=1):
        ''' Convenient function to set a Gaussian prior on the latent space parameters '''
        for param in self.parameters[:-1]:
            param.set_prior(GPy.core.parameterization.priors.Gaussian(0, nsigma))

    def set_variance_log10_prior(self, lower, upper):
        ''' Convenient function to set a Log10 prior on the variance parameters '''
        self.variance.unconstrain()
        self.variance.set_prior(Log10Uniform(lower, upper))
        self.variance.constrain(Exponent10())

    def copy(self):
          raise NotImplementedError()

    def get_norm_cov_1d(self, freqs, params):
        raise NotImplementedError()

    def K(self, X, X2=None):
        freqs = X.squeeze() * 1e6
        norm_cov_1d = self.get_norm_cov_1d(freqs, np.array(self.params[:-1]).T)
        r_1d = abs(freqs - freqs[0]) * 1e-6

        r = self._unscaled_dist(X, X2)

        cov = scipy.interpolate.interp1d(r_1d, norm_cov_1d, kind='quadratic', axis=1,
                                         bounds_error=False, fill_value=0)(r)

        return self.params[-1][0] * cov


class VAEKern(AbstractMLKern, MultiKern):
    ''' ML Kernel implementation '''

    def __init__(self, ml_decoder, latent_dim, ps3d_k_mean, name='vae_kern', param_values=[]):
        ''' Initialize a VAE kernel with ml_decoder given the dimension of the latent space latent_dim, 
            and the k_mean of the traing sets (ps3d_k_mean).'''
        self.ml_decoder = ml_decoder
        self.ps3d_k_mean = ps3d_k_mean
        AbstractMLKern.__init__(self, latent_dim, name=name, param_values=param_values)

    def copy(self):
        c = VAEKern(self.ml_decoder, self.latent_dim, self.ps3d_k_mean, name=self.name)
        c.copy_params(self)

        return c

    def get_norm_cov_1d(self, freqs, params):
        cov_gen = get_cached_cov_gen(tuple(freqs), tuple(self.uv_bins))
        ps3d = self.ml_decoder.predict(params).squeeze()
        ps3d = self.ps3d_k_mean ** 1 * ps3d

        return cov_gen.c_nu_from_ps21(self.ps3d_k_mean, ps3d)

    @staticmethod
    def load_from_dict(name, d):
        from tensorflow import keras

        decoder = keras.models.load_model(d['decoder_filename'])
        kern = VAEKern(decoder, d['latent_dim'], d['ps3d_k_mean'], name=name)
        return MultiKern._parse_set_params_from_dict(kern, d)


class VAEKernTorch(AbstractMLKern, MultiKern):
    ''' ML Kernel implementation '''

    def __init__(self, vae_fitter, name='vae_kern', param_values=[]):
        ''' Initialize a VAE kernel with ml_decoder given the dimension of the latent space latent_dim, 
            and the k_mean of the traing sets (ps3d_k_mean).'''
        self.fitter_res = vae_fitter
        self.ps3d_k_mean = vae_fitter.k_mean
        if not isinstance(self.fitter_res, VAEFitterPreProc):
            self.pre_proc = PreProcessorFlatten(self.ps3d_k_mean)
        else:
            self.pre_proc = self.fitter_res.pre_proc
        AbstractMLKern.__init__(self, vae_fitter.n_dim, name=name, param_values=param_values)

    def copy(self):
        c = VAEKernTorch(self.fitter_res, name=self.name)
        c.copy_params(self)

        return c

    def get_norm_cov_1d(self, freqs, params):
        cov_gen = get_cached_cov_gen(tuple(freqs), tuple(self.uv_bins))
        ps3d = self.pre_proc.inv(self.fitter_res.decode(params).squeeze())

        return cov_gen.c_nu_from_ps21(self.ps3d_k_mean, ps3d)

    @staticmethod
    def load_from_dict(name, d):
        vae_fitter = VAEFitter.load(d['fitter_filename'])
        kern = VAEKernTorch(vae_fitter, name=name)
        return MultiKern._parse_set_params_from_dict(kern, d)


class PCAKern(AbstractMLKern, MultiKern):
    ''' ML Kernel implementation '''

    def __init__(self, pca_fitter, name='pca_kern', param_values=[]):
        ''' Initialize a VAE kernel with ml_decoder given the dimension of the latent space latent_dim, 
            and the k_mean of the traing sets (ps3d_k_mean).'''
        self.fitter_res = pca_fitter
        self.ps3d_k_mean = pca_fitter.k_mean
        AbstractMLKern.__init__(self, pca_fitter.n_dim, name=name, param_values=param_values)

    def copy(self):
        c = PCAKern(self.fitter_res, name=self.name)
        c.copy_params(self)

        return c

    def set_latent_space_prior(self):
        ''' Convenient function to set a Gaussian prior on the latent space parameters '''
        for param, mini, maxi in zip(self.parameters[:-1], self.fitter_res.y_min, self.fitter_res.y_max):
            param.set_prior(Uniform(mini, maxi))

    def get_norm_cov_1d(self, freqs, params):
        cov_gen = get_cached_cov_gen(tuple(freqs), tuple(self.uv_bins))
        ps3d = self.fitter_res.decode(params).squeeze()
        ps3d = self.ps3d_k_mean ** 1 * ps3d

        return cov_gen.c_nu_from_ps21(self.ps3d_k_mean, ps3d)

    @staticmethod
    def load_from_dict(name, d):
        pca_fitter = PCAKern.load(d['fitter_filename'])
        kern = PCAKern(pca_fitter, name=name)
        return MultiKern._parse_set_params_from_dict(kern, d)


class MultiStationaryKern(MultiKern):
    ''' extension of kernel for regression in multiple baselines range'''

    def __init__(self, kern_class, variance=1, lengthscale=1, ls_alpha=0, var_alpha=0, theta_rad=0.1, delay_buffer_us=0,
                 name='mkern', wedge_parametrization=False, ls_is_period=False, latitude_deg=90, uv_min=None,
                 uv_max=None, use_uv_ps=False, l_max: float = 1e8, uv_break: float =0.1):
        MultiKern.__init__(self)
        self.kern_class = kern_class
        self.kerns = []
        kern_class.__init__(self, 1, variance=variance, lengthscale=lengthscale, name=name)
        
        self.wedge_parametrization = wedge_parametrization
        self.ls_is_period = ls_is_period
        self.latitude_deg = latitude_deg
        self.uv_max = uv_max
        self.uv_min = uv_min
        self.use_uv_ps = use_uv_ps
        self.l_max = l_max
        self.uv_break = uv_break

        if not self.use_uv_ps:
            self.var_alpha = GPy.core.parameterization.Param('var_alpha', var_alpha)
            self.var_alpha.constrain_fixed(var_alpha)
            self.link_parameters(self.var_alpha)

        if wedge_parametrization:
            self.theta_rad = GPy.core.parameterization.Param('theta_rad', theta_rad)
            self.delay_buffer_us = GPy.core.parameterization.Param('delay_buffer_us', delay_buffer_us)
            self.link_parameters(self.delay_buffer_us)
            self.link_parameters(self.theta_rad)

            self.lengthscale.constrain_fixed(1)
            self.delay_buffer_us.constrain_fixed(delay_buffer_us)
        else:
            self.ls_alpha = GPy.core.parameterization.Param('ls_alpha', ls_alpha)
            self.ls_alpha.constrain_fixed(ls_alpha)
            self.link_parameters(self.ls_alpha)

    @classmethod
    def load_from_dict(cls, name, d):
        wedge_parametrization = d.get('wedge_parametrization', False)
        latitude_deg = d.get('latitude_deg', 90)
        uv_max = d.get('uv_max', None)
        uv_min = d.get('uv_min', None)
        use_uv_ps = d.get('use_uv_ps', False)
        l_max = d.get('l_max', 1e8)
        uv_break = d.get('uv_break', 0.1)
        kern = cls(name=name, wedge_parametrization=wedge_parametrization, latitude_deg=latitude_deg, 
                   uv_min=uv_min, uv_max=uv_max, use_uv_ps=use_uv_ps, l_max=l_max, uv_break=uv_break)
        return MultiKern._parse_set_params_from_dict(kern, d)

    def set_var_alpha_prior(self, lower, upper):
        ''' Convenient function to set a Uniform prior on the var_alpha parameters '''
        self.var_alpha.unconstrain()
        self.var_alpha.set_prior(Uniform(lower, upper))

    def set_ls_alpha_prior(self, lower, upper):
        ''' Convenient function to set a Uniform prior on the ls_alpha parameters '''
        assert not self.wedge_parametrization
        self.ls_alpha.unconstrain()
        self.ls_alpha.set_prior(Uniform(lower, upper))

    def set_variance_prior(self, lower, upper):
        ''' Convenient function to set a Uniform prior on the variance parameters '''
        self.variance.unconstrain()
        self.variance.set_prior(Uniform(lower, upper))

    def set_variance_log10_prior(self, lower, upper):
        ''' Convenient function to set a Log10 prior on the variance parameters '''
        self.variance.unconstrain()
        self.variance.set_prior(Log10Uniform(lower, upper))
        self.variance.constrain(Exponent10())

    def set_lengthscale_prior(self, lower, upper):
        ''' Convenient function to set a Uniform prior on the lengthscale parameters '''
        assert not self.wedge_parametrization
        self.lengthscale.unconstrain()
        self.lengthscale.set_prior(Uniform(lower, upper))

    def set_theta_rad_prior(self, lower, upper):
        assert self.wedge_parametrization
        self.theta_rad.unconstrain()
        self.theta_rad.set_prior(Uniform(lower, upper))

    def parameters_changed(self):
        if self.kerns is None or len(self.uv_bins) != len(self.kerns):
            self.kerns = [self.kern_class(1) for _ in range(len(self.uv_bins))]
        u_min = np.clip(self.uv_bins[0][0], 10, 1e3)
        u_means = np.array([(umax + umin) / 2 for umin, umax in self.uv_bins])
        l_m = self.lengthscale[0]

        if self.use_uv_ps:
            if callable(self.uv_ps_fct):
                var = self.uv_ps_fct(u_means)
            else:
                print('Warning: use_data_angular_ps is True, but no uv_ps_fct set')
                var = [1] * len(u_means)
        else:
            var = (u_means / u_min) ** self.var_alpha

        var_norm = 1 / np.mean(var * u_means / u_means.mean())
        var = self.variance[0] * var_norm * var
        for i, u_mean in enumerate(u_means):
            if self.uv_max and u_mean >= self.uv_max:
                self.kerns[i].variance = 1e-20
                self.kerns[i].lengthscale = 1e-8
                continue
            if self.uv_min and u_mean <= self.uv_min:
                self.kerns[i].variance = 1e-20
                self.kerns[i].lengthscale = 1e-8
                continue                
            if self.wedge_parametrization:
                lat_term = np.cos(np.radians(self.latitude_deg))
                delays_fct = lambda u: self.delay_buffer_us + (np.sin(self.theta_rad) + lat_term) * u / (self.mean_fmhz)
            else:
                delays_fct = lambda u:  (1 + self.ls_alpha * 1e-3 * l_m * (u - u_min)) / l_m
            ll = 1 / delays_fct(u_mean)
            l_max = min(self.l_max, 1 / delays_fct(self.uv_break))
            if self.ls_is_period and self.wedge_parametrization:
                ll = ll / (2 * np.pi)
            self.kerns[i].lengthscale = np.clip(abs(ll), 1e-8, l_max)
            self.kerns[i].variance = var[i]

    def K(self, X, X2=None):
        return np.array([k.K(X, X2) for k in self.kerns])


class RBF(Stationary, GPy.kern.RBF):
    pass


class Matern32(Stationary, GPy.kern.Matern32):
    pass


class Matern52(Stationary, GPy.kern.Matern52):
    pass


class Exponential(Stationary, GPy.kern.Exponential):
    pass


class Cosine(Stationary, GPy.kern.Cosine):
    pass


class RatQuad(Stationary, GPy.kern.RatQuad):
    pass


class RatQuad2(Stationary, GPy.kern.RatQuad):
    
    def K_of_r(self, r):
        r2 = np.square(r)
        return self.variance * np.exp(-self.power * np.log1p(r2 / (2. * self.power)))


class MRBF(MultiStationaryKern, MultiKern, RBF):

    def __init__(self, name='mrbf', **kargs):
        MultiStationaryKern.__init__(self, RBF, name=name, **kargs)


class MMat32(MultiStationaryKern, MultiKern, Matern32):

    def __init__(self, name='mmat32', **kargs):
        MultiStationaryKern.__init__(self, Matern32, name=name, **kargs)


class MMat52(MultiStationaryKern, MultiKern, Matern52):

    def __init__(self, name='mmat52', **kargs):
        MultiStationaryKern.__init__(self, Matern52, name=name, **kargs)


class MExponential(MultiStationaryKern, MultiKern, Exponential):

    def __init__(self, name='mexp', **kargs):
        MultiStationaryKern.__init__(self, Exponential, name=name, **kargs)


class MCosine(MultiStationaryKern, MultiKern, Cosine):

    def __init__(self, **kargs):
        MultiStationaryKern.__init__(self, Cosine, ls_is_period=True, **kargs)


class MRatQuad(MultiStationaryKern, MultiKern, RatQuad):

    def __init__(self, name='mratquad', **kargs):
        power = kargs.pop('power', 2)
        MultiStationaryKern.__init__(self, RatQuad, name=name, **kargs)
        self.power = power

    def parameters_changed(self):
        MultiStationaryKern.parameters_changed(self)
        for k in self.kerns:
            k.power = self.power

class MRatQuad2(MultiStationaryKern, MultiKern, RatQuad2):

    def __init__(self, name='mratquad2', **kargs):
        power = kargs.pop('power', 2)
        MultiStationaryKern.__init__(self, RatQuad2, name=name, **kargs)
        self.power = power

    def parameters_changed(self):
        MultiStationaryKern.parameters_changed(self)
        for k in self.kerns:
            k.power = self.power


class MWhiteHeteroscedastic(MultiKern, GPy.kern.Kern):

    def __init__(self, variance=1, X=None, name='noise'):
        MultiKern.__init__(self)
        GPy.kern.Kern.__init__(self, 1, 0, name)
        self.set_variance(variance, X)
        self.alpha = GPy.core.parameterization.Param('alpha', 1)
        self.alpha.constrain_fixed()
        self.link_parameters(self.alpha)

    def set_variance(self, variance, X):
        assert np.isscalar(variance) or (len(self.uv_bins) == len(variance))
        if not np.isscalar(variance):
            assert X is not None, 'X positions must be informed with Heteroscedastic noise'
        self.variance = variance
        self.X = X

    def K(self, X, X2=None):
        if X2 is None:
            X2 = X
        if np.isscalar(self.variance):
            variance = self.variance
        else:
            x_interp = scipy.interpolate.interp1d(self.X[:, 0], self.variance, bounds_error=False, fill_value='extrapolate')
            variance = x_interp(X[np.in1d(X, X2)][:, 0])

        Ks = np.zeros((len(self.uv_bins), len(X), len(X2)))
        Ks[:, np.in1d(X, X2), np.in1d(X2, X)] = variance

        return self.alpha[0] * Ks


class Uniform(GPy.core.parameterization.priors.Prior):
    ''' Uniform prior '''

    domain = GPy.priors._REAL

    def __new__(cls, *args):
        return object.__new__(cls)

    def __init__(self, l, u):
        self.lower = l
        self.upper = u

    def __str__(self):
        return "[{:.2g}, {:.2g}]".format(self.lower, self.upper)

    def lnpdf(self, x):
        region = (x >= self.lower) * (x <= self.upper)
        return np.log(region * np.e)

    def lnpdf_grad(self, x):
        return np.zeros(x.shape)

    def rvs(self, n):
        return np.random.uniform(self.lower, self.upper, size=n)


class Log10Uniform(GPy.core.parameterization.priors.Prior):
    ''' Log10 prior '''

    domain = GPy.priors._POSITIVE

    def __new__(cls, *args):
        return object.__new__(cls)

    def __init__(self, l, u):
        self.lower = l
        self.upper = u

    def __str__(self):
        return "Log10[{:.2g}, {:.2g}]".format(self.lower, self.upper)

    def lnpdf(self, x):
        region = (x >= 10 ** self.lower) * (x <= 10 ** self.upper)
        return np.log(region * np.e)

    def lnpdf_grad(self, x):
        return np.zeros(x.shape)

    def rvs(self, n):
        return 10 ** np.random.uniform(self.lower, self.upper, size=n)


class Exponent10(paramz.transformations.Transformation):
    domain = paramz.transformations._POSITIVE

    def f(self, x):
        return 10 ** x

    def finv(self, x):
        return np.log10(x)

    def initialize(self, f):
        return np.abs(f)

    def log_jacobian(self, model_param):
        return np.log10(model_param)

    def __str__(self):
        return 'exp10'


def get_prior_transform_ppf(prior):
    if isinstance(prior, Uniform):
        return lambda x: (prior.upper - prior.lower) * x + prior.lower
    elif isinstance(prior, Log10Uniform):
        return lambda x: stats.loguniform.ppf(x, 10 ** prior.lower, 10 ** prior.upper)
    elif isinstance(prior, GPy.core.parameterization.priors.Gaussian):
        return lambda x: stats.norm.ppf(x, loc=prior.mu, scale=prior.sigma)
    elif isinstance(prior, GPy.core.parameterization.priors.Gamma):
        return lambda x: stats.gamma.ppf(x, a=prior.a, scale=1 / prior.b)
    raise Exception(f'Error: ppf not defined for prior {prior}')


class GPRegressor:
    ''' Simple GPR. See e.g. http://www.gaussianprocess.org/gpml/chapters/RW2.pdf'''

    def __init__(self, Y, K, W=None):
        self.K = K
        self.Y = Y
        self.W = W
        if W is not None:
            self.YW = self.Y * self.W
        else:
            self.YW = self.Y
        self.fit()

    def fit(self):
        self.L_ = GPy.util.linalg.jitchol(self.K, maxtries=100)
        self.alpha_, _ = GPy.util.linalg.dpotrs(self.L_, self.Y, lower=1)

    def predict(self, K_p=None, K_p_p=None):
        if K_p is None:
            K_p = self.K
            K_p_p = self.K
        else:
            assert K_p_p is not None, "K_p_p needs to be given when predicting at different X"
        y_mean = K_p.T.dot(self.alpha_)
        v, _ = GPy.util.linalg.dpotrs(self.L_, K_p, lower=1)
        y_cov = K_p_p - K_p.T.dot(v)
        return y_mean, y_cov

    def log_marginal_likelihood(self):
        return - 0.5 * (self.Y.size * np.log(2 * np.pi) + 2 * self.Y.shape[1] * np.sum(np.log(np.diag(self.L_)))
            + np.sum(self.alpha_ * self.YW))


class MultiData(object):
    ''' Object encapsulating a CartDataCube for use in MultiGPRegressor.
        Optionally, you can also set the corresponding noise_cube, the uv_bin width
        (or alternatively the uv_bins), and the normalization factor. If the later is not 
        set it will be computed so that the variance of the real part of the data is 1. '''

    def __init__(self, i_cube, noise_cube=1, uv_bins_du=25, norm_factor=None, uv_bins=None, uv_bins_n_uni=0):
        self.i_cube = i_cube
        self.X = (i_cube.freqs * 1e-6)[:, None]
        
        if norm_factor is None:
            norm_factor = np.sqrt(1 / i_cube.data.real.var())
        self.norm_factor = norm_factor

        if uv_bins is None:
            if uv_bins_n_uni > 0:
                uv_bins = get_n_uniform_uv_bins(i_cube.ru.min(), i_cube.ru.max(), uv_bins_n_uni)
            elif uv_bins_du != None:
                uv_bins = get_uv_bins(i_cube.ru.min(), i_cube.ru.max(), uv_bins_du)
            else:
                uv_bins = [(i_cube.ru.min(), i_cube.ru.max())]
        self.uv_bins = uv_bins
        self.noise_cube = noise_cube

    def c2f(self, c, axis=1):
        return np.concatenate([c.real, c.imag], axis=axis)

    def f2c(self, f):
        return f[:, :f.shape[1] // 2] + 1j * f[:, f.shape[1] // 2:]

    def get_split_idx(self):
        return [(self.i_cube.ru >= umin) & (self.i_cube.ru <= umax) for umin, umax in self.uv_bins]

    def split(self, i_cube=None):
        if i_cube is None:
            i_cube = self.i_cube

        return [self.c2f(i_cube.data[:, idx] * self.norm_factor) for idx in self.get_split_idx()]

    def get_noise_variance_split(self):
        if np.isscalar(self.noise_cube):
            return self.noise_cube * self.norm_factor ** 2
        elif isinstance(self.noise_cube, datacube.NoiseStdCube):
            return [Y.mean(axis=1) ** 2 for Y in self.split(self.noise_cube)]
        else:
            return [Y.var(axis=1) for Y in self.split(self.noise_cube)]

    def get_uv_ps_fct(self, uv_bins_du=None, uv_log_poly_deg=4):
        if uv_bins_du is None:
            uv_bins_du = psutil.robust_du(self.i_cube.uu, self.i_cube.vv)
        return fitutil.fit_cl_cube_poly(self.i_cube, du=uv_bins_du, poly_deg=uv_log_poly_deg, log=True)[0]

    def get_uv_weight_split(self):
        if hasattr(self.noise_cube, 'weights') and isinstance(self.noise_cube.weights, datacube.CartWeightCube):
            w = self.noise_cube.weights.get()
        elif isinstance(datacube.CartWeightCube, self.i_cube.weights):
            w = self.i_cube.weights.get()
        else:
            w = np.ones_like(self.i_cube.data)
        w = np.sum(w, axis=0)
        return [self.c2f((w[idx] + 1j * w[idx]) / np.mean(w[idx]), axis=0) for idx in self.get_split_idx()]

    def get_freqs(self, fill_gaps=False):
        freqs = self.i_cube.freqs
        if fill_gaps:
            freqs = np.array(sorted(np.concatenate((freqs, psutil.get_freqs_gaps(freqs)))))
        return freqs

    def gen_cube(self, Ys_and_covYs, fill_gaps=False):
        freqs_p = self.get_freqs(fill_gaps=fill_gaps)
        if fill_gaps:
            freqs_p = np.array(sorted(np.concatenate((freqs_p, psutil.get_freqs_gaps(freqs_p)))))
        X_p = (freqs_p * 1e-6)[:, None]
        data = np.zeros((len(freqs_p), self.i_cube.data.shape[1]), dtype=self.i_cube.data.dtype)
        cube = self.i_cube.new_with_data(data, freqs=freqs_p)

        idxs = [(cube.ru >= umin) & (cube.ru <= umax) for umin, umax in self.uv_bins]
        for (Y, covY), idx in zip(Ys_and_covYs, idxs):
            cube.data[:, idx] = self.f2c(Y) + get_samples(X_p, idx.sum(), covY)
        return 1 / self.norm_factor * cube


class MultiGPRegressor(GPy.core.model.Model):
    ''' Extension of GPRegressor to support multi-baselines.'''

    def __init__(self, multi_data: MultiData, kern_model: MultiKern, kern_noise=None, name='mgp', use_uv_weight=False):
        ''' Initialze a MultiGPRegressor. Inputs:

            multi_data: a MultiData object
            kern_model: the covariance model for the underlying signal (including foregrounds but without noise)
            kern_noise (optional): the noise Kern object. If not set, it will be set to a MWhiteHeteroscedastic.

            The uv_bins of kern_model and kern_noise will be set to the uv_bins of multi_data.
            Also, the noise variance will be set using the noise_cube of multi_data.
            '''
        super(MultiGPRegressor, self).__init__(name=name)

        if kern_noise is None:
            kern_noise = MWhiteHeteroscedastic(name='noise')

        kern_model.set_uv_bins(multi_data.uv_bins)
        kern_noise.set_uv_bins(multi_data.uv_bins)
        kern_model.set_mean_fmhz(multi_data.X.mean())
        kern_noise.set_mean_fmhz(multi_data.X.mean())
        kern_model.set_uv_ps_fct(multi_data.get_uv_ps_fct())
        kern_noise.set_variance(multi_data.get_noise_variance_split(), multi_data.X)

        self.multi_data = multi_data
        self.kern_model = kern_model
        self.kern_noise = kern_noise
        self.update_kern()

        self.X = multi_data.X
        self.Ys = multi_data.split()
        if use_uv_weight:
            self.Ws = multi_data.get_uv_weight_split()
        else:
            self.Ws = [None] * len(self.Ys)

        self.gp_regressors = None
        self.link_parameters(self.kern)
        self.kern_noise.add_observer(self, self.update_kern)
        self.kern_model.add_observer(self, self.update_kern)

    def update_kern(self, *args, **kargs):
        self.kern = self.kern_model + self.kern_noise

    def fit(self):
        Ks = self.kern.K(self.X)
        if Ks.ndim == 2 and self.Ys.ndim == 2:
            self.gp_regressors = [GPRegressor(self.Ys, Ks, self.Ws)]
        else:
            self.gp_regressors = [GPRegressor(Y, K, W) for K, Y, W in zip(Ks, self.Ys, self.Ws)]

    def predict(self, kern=None, fill_gaps=False):
        assert self.gp_regressors is not None
        if kern is None:
            kern = self.kern_model
        if fill_gaps:
            freqs_p = self.multi_data.get_freqs(fill_gaps=fill_gaps)
            X_p = (freqs_p * 1e-6)[:, None]
            Ks_p = kern.K(self.X, X_p)
            Ks_p_p = kern.K(X_p, X_p)
        else:
            Ks_p = kern.K(self.X, self.X)
            Ks_p_p = Ks_p
        if Ks_p.ndim == 2:
            Ks_p = np.repeat(Ks_p[None], len(self.Ys), axis=0)
            Ks_p_p = np.repeat(Ks_p_p[None], len(self.Ys), axis=0)
        return self.multi_data.gen_cube([gp_regressor.predict(K_p, K_p_p) for K_p, K_p_p, gp_regressor in zip(Ks_p, Ks_p_p, self.gp_regressors)],
                                         fill_gaps=fill_gaps)

    def get_interpolated_i_cube(self):
        full_predicted_cube = self.predict(self.kern, fill_gaps=True)
        idx = np.in1d(self.multi_data.get_freqs(True), self.multi_data.get_freqs(False))
        full_predicted_cube.data[idx] = self.multi_data.i_cube.data
        return full_predicted_cube

    def log_marginal_likelihood(self):
        assert self.gp_regressors is not None
        return np.sum([gp_regressor.log_marginal_likelihood() for gp_regressor in self.gp_regressors])


def get_kern_part(kern: GPy.kern.Kern, name: str):
    if kern.name == name:
        return kern

    kern_list = []
    for n in name.split(';'):
        for k in kern.parts:
            if fnmatch.fnmatch(k.name, n):
                kern_list.append(k)
    if len(kern_list) == 0:
        return None
    elif len(kern_list) == 1:
        return kern_list[0]
    return GPy.kern.Add(kern_list)


class MCMCSamples(object):

    sampler_method = 'mcmc'

    def __init__(self, samples, log_prob, n_burn=50, clip_nsigma=6, discard_walkers_nsigma=10, autocorr_time=None):
        self.samples = samples
        self.log_prob = log_prob
        self.n_burn = n_burn
        self.clip_nsigma = clip_nsigma
        self.discard_walkers_nsigma = discard_walkers_nsigma
        if autocorr_time is None:
            autocorr_time = np.zeros(self.samples.shape[0])
        self.autocorr_time = autocorr_time

    def get(self):
        samples = self.samples[self.n_burn:]
        log_prob = self.log_prob[self.n_burn:]
        max_log_prob = log_prob.max(axis=0)
        mask = max_log_prob > np.median(max_log_prob) - self.discard_walkers_nsigma * np.median(log_prob.std(axis=0))
        if (~mask).sum() > 0:
            print(f'Discarding {(~mask).sum()} walkers')

        samples = samples[:, mask, :].reshape(-1, samples.shape[-1])        
        log_prob = log_prob[:, mask].flatten()

        samples_outliers = np.zeros_like(samples)
        for i in range(samples.shape[1]):
            m = np.median(samples[:, i])
            s = psutil.robust_std(samples[:, i])
            samples_outliers[abs(samples[:, i] - m) > self.clip_nsigma * s, i] = 1
            
        mask = (samples_outliers.sum(axis=1) == 0)
        return samples[mask], log_prob[mask]

    def save(self, filename):
        d = {'samples': self.samples, 'log_prob': self.log_prob, 'n_burn': self.n_burn, 'autocorr_time': self.autocorr_time,
             'clip_nsigma': self.clip_nsigma, 'discard_walkers_nsigma': self.discard_walkers_nsigma}
        psutil.save_dict_to_h5(filename, d)

    @staticmethod
    def load(filename):
        d = psutil.load_dict_from_h5(filename)

        return MCMCSamples(d['samples'], d['log_prob'], n_burn=d['n_burn'], clip_nsigma=d['clip_nsigma'],
                           discard_walkers_nsigma=d['discard_walkers_nsigma'], autocorr_time=d['autocorr_time'])


class NestedSamples(dynesty.results.Results):

    sampler_method = 'nested'

    def __init__(self, d):
        dynesty.results.Results.__init__(self, d)

    def get(self, resample_equal=True):
        if not resample_equal:
            return self.samples, self.logl

        weights = np.exp(self.logwt - self.logz[-1])
        i_rs = dynesty.utils.resample_equal(np.arange(self.samples.shape[0]), weights)

        return self.samples[i_rs], self.logl[i_rs]

    def save(self, filename):
        d = self.asdict()
        # we can not save python object
        for k, v in d.copy().items():
            if np.array(v).dtype == 'object':
                del d[k]
        psutil.save_dict_to_h5(filename, d)

    @staticmethod
    def load(filename):
        d = psutil.load_dict_from_h5(filename)

        return NestedSamples(d)


class SamplerResult(object):

    def __init__(self, gp, samples):
        self.gp = gp
        self.samples = samples

    def get_parameter_names(self):
        self.gp.kern._ensure_fixes()
        return ['.'.join(s.split('.')[2:]) for s in self.gp.kern.parameter_names_flat().squeeze()]
    
    def get_n_params(self):
        return len(self.gp.kern.optimizer_array)

    def get_parameter_samples(self, param_name):
        names = self.get_parameter_names()
        if not param_name in names:
            raise ValueError(f'Parameter name {param_name} not valid.')
        samples, _ = self.samples.get()

        return samples[:, names.index(param_name)]

    def plot_samples(self):
        n_params = self.get_n_params()

        ncols = 4
        nrows = int(np.ceil(n_params / ncols))

        fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(12, 1 + 2.2 * nrows), sharex=True)

        is_mcmc = isinstance(self.samples, MCMCSamples)

        names = self.get_parameter_names()

        for j, ax in zip(range(n_params), axs.flatten()):
            if is_mcmc:
                y = self.samples.samples[:, :, j]
            else:
                y = self.samples.samples[:, j]
            ax.plot(y, c='tab:orange', alpha=0.6)

            if is_mcmc:
                ax.axvline(self.samples.autocorr_time[j], c=psutil.black, ls=':')
                ax.axvline(5 * self.samples.autocorr_time[j], c=psutil.black, ls='--')

            # if (np.median(y) < 1) and np.all(y.flatten() > 1e-8):
            #     ax.set_yscale('log')

            txt = f'{names[j]}\nmed:{np.median(y):.4f} std:{astats.mad_std(y):.4f}'
            ax.text(0.05, 0.97, txt, transform=ax.transAxes, va='top', ha='left')

        fig.tight_layout(pad=0.15)

        return fig

    def plot_samples_likelihood(self, p_true=None):
        n_params = self.get_n_params()

        ncols = 4
        nrows = int(np.ceil(n_params / ncols))

        fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(12, 1 + 2.5 * nrows), sharey=True)

        samples, log_prob = self.samples.get()
        i = np.arange(samples.shape[0])

        names = self.get_parameter_names()

        for j, ax in zip(range(n_params), axs.flatten()):
            x = samples[:, j]
            ax.scatter(x, - log_prob, marker='+', c=i, cmap='viridis')
            if p_true is not None:
                ax.axvline(p_true[j], c='tab:orange', ls='--')
            txt = f'{names[j]}\nmed:{np.median(x):.4f} std:{astats.mad_std(x):.4f}'
            ax.text(0.05, 0.97, txt, transform=ax.transAxes, va='top', ha='left')
        fig.tight_layout(pad=0.15)

        return fig

    def plot_corner(self, fig=None, plot_prior=True, **kargs_corner):
        samples, _ = self.samples.get()
        c = corner.corner(samples, plot_datapoints=False, smooth=0.8, 
                             quantiles=(0.16, 0.84), labels=self.get_parameter_names(), fig=fig, **kargs_corner)

        if plot_prior:
            axes = np.array(c.axes).reshape((self.get_n_params(), self.get_n_params()))

            pp = ParamaterPriors(self.gp.kern)
            prior_quantiles = pp.prior_transform(np.array([[0.0015, 0.025, 0.16, 0.84, 0.975, 0.9985],] * self.get_n_params()))

            for i, qs in enumerate(prior_quantiles):
                ax = axes[i, i]
                ax.axvspan(qs[0], qs[-1], color=psutil.green, alpha=0.08)
                ax.axvspan(qs[1], qs[-2], color=psutil.green, alpha=0.08)
                ax.axvspan(qs[2], qs[-3], color=psutil.green, alpha=0.08)

        return c

    def select_random_sample(self, samples=None):
        if samples is None:
            samples, _ = self.samples.get()
        i = np.random.randint(0, samples.shape[0], 1)[0]
        m_oa = samples[i].copy()
        self.gp.kern.optimizer_array = m_oa
        self.gp.fit()

    def generate_data_cubes(self, n_pick, kern_name='eor', fill_gaps=False):
        # Determine the parameters index of the portion of the kernel that will be predicted
        k = self.gp.kern.copy()
        k.optimizer_array = np.arange(len(k.optimizer_array))
        k_part = get_kern_part(k, kern_name)

        if k_part is None:
            raise Exception(f'kern_name {kern_name} does not return any valid components')

        k_part_idx = np.round(k_part.optimizer_array).astype(int)
        samples, _ = self.samples.get()

        for i in range(n_pick):
            self.select_random_sample(samples)
            k_part.optimizer_array = self.gp.kern.optimizer_array[k_part_idx]
            yield self.gp.predict(k_part, fill_gaps=fill_gaps)

    def get_interpolated_i_cube(self):
        self.select_random_sample()
        return self.gp.get_interpolated_i_cube()

    def get_ps_stack(self, ps_gen, kbins, n_pick=100, kern_name='eor', subtract_from=None, fill_gaps=False):
        ps_stacker = pspec.PsStacker(ps_gen, kbins)
        pr = psutil.progress_report(n_pick)
        
        for j, c_rec in enumerate(self.generate_data_cubes(n_pick, kern_name=kern_name, fill_gaps=fill_gaps)):
            pr(j)
            if subtract_from is not None:
                c_rec = subtract_from - c_rec
            ps_stacker.add(c_rec)

        return ps_stacker


class AbstractSampler(object):

    def __init__(self, gp):
        self.gp = gp
        self.pp = ParamaterPriors(gp.kern)
        self.ndim = len(gp.kern.optimizer_array)

    def get_parameter_names(self):
        self.gp.kern._ensure_fixes()
        return ['.'.join(s.split('.')[2:]) for s in self.gp.kern.parameter_names_flat().squeeze()]

    def get_result(self):
        raise NotImplementedError()

    def log_marginal_likelihood(self, p):
        self.gp.kern.optimizer_array = p
        self.gp.fit()
        logz = self.gp.log_marginal_likelihood()
        return logz

    def prior_transform(self, uu):
        return self.pp.prior_transform(uu)


class MCMCSampler(AbstractSampler):
    ''' MCMC sampler for GPR '''

    def __init__(self, gp, n_walkers, emcee_moves='stretch', debug=False):
        '''gp: a MultiGPRegressor object'''

        if emcee_moves == 'stretch':
            moves = emcee.moves.StretchMove()
        elif emcee_moves == 'kde':
            moves = emcee.moves.KDEMove()
        else:
            moves = emcee_moves

        self.debug = debug
        self.n_walkers = n_walkers

        AbstractSampler.__init__(self, gp)
        self.sampler = emcee.EnsembleSampler(self.n_walkers, self.ndim, self.lnprob, moves=moves)

    def lnprob(self, p):
        self.gp.kern.optimizer_array = p
        if not np.isfinite(self.gp.kern.log_prior()):
            return - np.inf

        self.gp.fit()

        log_marginal_likelihood = self.gp.log_marginal_likelihood()
        log_prior = self.gp.kern.log_prior()

        if self.debug:
            print(self.gp.kern.param_array, log_marginal_likelihood, log_prior)

        return log_marginal_likelihood + log_prior

    def run(self, n_steps, verbose=False, live_update=False):
        pos = []
        for i in range(self.n_walkers):
            self.gp.kern.randomize()
            pos.append(self.gp.kern.optimizer_array.tolist())

        if live_update:
            from IPython import display

            ncols = 4
            nrows = int(np.ceil((self.ndim + 1) / ncols))

            fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(12, 1 + 2.2 * nrows), sharex=True)
            hdisplay = display.display("", display_id=True)
            p_names = self.get_parameter_names() + ['likelihood']

            prior_quantiles = self.pp.prior_transform(np.array([[0.0015, 0.025, 0.16, 0.84, 0.975, 0.9985],] * self.ndim))

            for i, ax in zip(range(self.ndim + 1), axs.flatten()):
                for k in range(self.n_walkers):
                    ax.plot([], c='tab:orange', alpha=0.6)
                ax.text(0.05, 0.97, f'{p_names[i]}:', transform=ax.transAxes, va='top', ha='left')
                if i < self.ndim:
                    ax.axhspan(prior_quantiles[i, 0], prior_quantiles[i, -1], color=psutil.green, alpha=0.08)
                    ax.axhspan(prior_quantiles[i, 1], prior_quantiles[i, -2], color=psutil.green, alpha=0.08)
                    ax.axhspan(prior_quantiles[i, 2], prior_quantiles[i, -3], color=psutil.green, alpha=0.08)
            fig.tight_layout(pad=0.15)

        try:
            pr = psutil.progress_report(n_steps)
            for i, _ in enumerate(self.sampler.sample(pos, iterations=n_steps)):
                pr(i)
                if verbose and i % 20 == 0 and i != 0:
                    log_prob = self.sampler.get_log_prob()[:, -20:]
                    chain = self.sampler.chain[:, -20:]
                    print('Last 20:')
                    print('Median:', ', '.join([f'{k:.3f}' for k in np.median(chain, axis=(0, 1))]))
                    print('Mean:', ', '.join([f'{k:.3f}' for k in np.mean(chain, axis=(0, 1))]))
                    print('Min:', ', '.join([f'{k:.3f}' for k in np.min(chain, axis=(0, 1))]))
                    print('Max:', ', '.join([f'{k:.3f}' for k in np.max(chain, axis=(0, 1))]))
                    print('Rms:', ', '.join([f'{k:.3f}' for k in np.std(chain, axis=(0, 1))]))
                    print(f'Likelihood: {log_prob.mean():.2f} +-{log_prob.std():-2f}')

                if live_update and i % 10 == 0:  # and i != 0:
                    chain = self.sampler.get_chain()

                    for j in range(self.ndim + 1):
                        if j < self.ndim:
                            data = chain[:, :, j]
                        else:
                            data = self.sampler.get_log_prob()
                        for k in range(self.n_walkers):
                            fig.axes[j].lines[k].set_data((np.arange(chain.shape[0]), data[:, k]))
                        # if (np.median(data) < 1) and np.all(data.flatten() > 1e-8):
                        #     fig.axes[j].set_yscale('log')

                        fig.axes[j].relim()
                        fig.axes[j].autoscale_view()
                        fig.axes[j].texts[0].set_text(f'{p_names[j]}: med:{np.median(data[:, -20:]):.4f}')
                    hdisplay.update(fig)

        except KeyboardInterrupt:
            print('KeyboardInterrupt')

        if live_update:
            plt.close(fig)

        return self.get_result()

    def get_result(self, n_burn=50, clip_nsigma=6, discard_walkers_nsigma=10):
        samples = MCMCSamples(self.sampler.get_chain(), self.sampler.get_log_prob(), n_burn=n_burn,
                              clip_nsigma=clip_nsigma, discard_walkers_nsigma=discard_walkers_nsigma,
                              autocorr_time=self.sampler.get_autocorr_time(tol=0))
        return SamplerResult(self.gp, samples)


class ParamaterPriors(object):

    def __init__(self, kern):
        self.prior_fct = {}
        self.constraint_fct = {}
        for p, name in zip(kern.flattened_parameters, kern.parameter_names()):
            if not p.is_fixed:
                priors = list(p.priors.items())
                constraints = list(p.constraints.items())
                if not priors:
                    print(f'Error: a prior is required for parameter {p}')
                    continue
                self.prior_fct[name] = get_prior_transform_ppf(priors[0][0])
                if len(constraints) > 0:
                    self.constraint_fct[name] = constraints[0][0].finv

    def ppf(self, name, x):
        p = self.prior_fct[name](x)
        if name in self.constraint_fct:
            p = self.constraint_fct[name](p)
        return p

    def prior_transform(self, uu):
        return np.array([self.ppf(name, u) for name, u in zip(self.prior_fct.keys(), uu)])


class NestedSampler(AbstractSampler):
    
    def __init__(self, gp, nlive=500, bound='multi', sample='auto', **kargs_dynesty):
        AbstractSampler.__init__(self, gp)
        self.sampler = dynesty.NestedSampler(self.log_marginal_likelihood, self.prior_transform, self.ndim, nlive=nlive,
                                             bound=bound, sample=sample, **kargs_dynesty)

    def run(self, live_update=False, **kargs_dynesty):
        if live_update:
            from IPython import display

            ncols = 4
            nrows = int(np.ceil((self.ndim + 1) / ncols))
            all_samples = []
            all_lnlik = []

            fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(12, 1 + 2.2 * nrows), sharex=True)
            hdisplay = display.display("", display_id=True)
            p_names = self.get_parameter_names() + ['likelihood']

            prior_quantiles = self.pp.prior_transform(np.array([[0.0015, 0.025, 0.16, 0.84, 0.975, 0.9985],] * self.ndim))

            for i, ax in zip(range(self.ndim + 1), axs.flatten()):
                ax.plot([], c='tab:orange', alpha=0.6, ls='', marker='+')
                ax.text(0.05, 0.97, f'{p_names[i]}:', transform=ax.transAxes, va='top', ha='left')
                if i < self.ndim:
                    ax.axhspan(prior_quantiles[i, 0], prior_quantiles[i, -1], color=psutil.green, alpha=0.08)
                    ax.axhspan(prior_quantiles[i, 1], prior_quantiles[i, -2], color=psutil.green, alpha=0.08)
                    ax.axhspan(prior_quantiles[i, 2], prior_quantiles[i, -3], color=psutil.green, alpha=0.08)
            fig.tight_layout(pad=0.15)

            def _update_fct(results, niter, ncall, **kargs):
                all_samples.append(results[2])
                all_lnlik.append(results[3])

                if niter % 500 == 0:
                    for j in range(self.ndim + 1):
                        if j < self.ndim:
                            data = np.array(all_samples)[:, j]
                        else:
                            data = np.array(all_lnlik)
                        fig.axes[j].lines[0].set_data((np.arange(data.shape[0]), data))
                        fig.axes[j].relim()
                        fig.axes[j].autoscale_view()
                        fig.axes[j].texts[0].set_text(f'{p_names[j]}: med:{np.median(data[-20:]):.4f}')
                    hdisplay.update(fig)
                if niter % 5 == 0:
                    dynesty.results.print_fn(results, niter, ncall, **kargs)

            print_func = _update_fct
        else:
            print_func = None

        if live_update:
            plt.close(fig)

        self.sampler.run_nested(print_func=print_func, **kargs_dynesty)

        return self.get_result()

    def get_result(self):
        return SamplerResult(self.gp, NestedSamples(self.sampler.results.asdict()))


class UltraNestNestedSampler(AbstractSampler):

    def __init__(self, gp, nlive=500, bound='multi', **kargs_ultranest):
        self.nlive = nlive
        
        AbstractSampler.__init__(self, gp)
        self.sampler = ultranest.ReactiveNestedSampler(self.get_parameter_names(), self.log_marginal_likelihood,
                                                       self.prior_transform, **kargs_ultranest)
        self.sampler_results = None

    def run(self, live_update=False, **kargs_ultranest):
        viz_callback = 'auto'
        if not live_update:
            viz_callback = None
        
        try:
            res = self.sampler.run(min_num_live_points=self.nlive, viz_callback=viz_callback, **kargs_ultranest)
        except KeyboardInterrupt:
            print('KeyboardInterrupt during sampling ...')

        d = {}
        d['nlive'] = self.nlive
        d['niter'] = res['niter']
        d['ncall'] = res['ncall']
        d['ncall'] = res['ncall']
        d['samples'] = res['weighted_samples']['points']
        d['samples_u'] = res['weighted_samples']['upoints']
        d['samples_id'] = 0
        d['logwt'] = res['weighted_samples']['logw'] + res['weighted_samples']['logl']
        d['logl'] = res['weighted_samples']['logl']
        d['logz'] = [res['logz'],]
        d['logzerr'] = res['logzerr']

        self.sampler_results = d
        
        return self.get_result()

    def get_result(self):
        return SamplerResult(self.gp, NestedSamples(self.sampler_results))



class MLGPRConfigFile(settings.BaseSettings):

    DEFAULT_SETTINGS = os.path.join(CONFIG_DIR, 'default_ml_gpr_settings.toml')

    def _load_kerns_from_dict(self, k_names, label_prefix):
        all_kern_class = {k.__name__: k for k in MultiKern.__subclasses__()}
        kerns = []
        kern_prod = False
        for name in k_names:
            if name.strip() in ['.', 'x', '*']:
                assert len(kerns) > 0, 'List of kernel should not start with an operation'
                kern_prod = True
                continue
            if name.strip() ==  '+':
                assert len(kerns) > 0, 'List of kernel should not start with an operation'
                continue
            if not name in self:
                raise ValueError(f'{name} not defined in {self.get_file()}')
            assert self[name]['type'] in all_kern_class, f"Kernel type {self[name]['type']} unknown"
            label = name
            if not label.startswith(label_prefix + '_'):
                label = f'{label_prefix}_{name}'
            k = all_kern_class[self[name]['type']].load_from_dict(label, self[name])
            if kern_prod:
                kerns[-1] = kerns[-1].prod(k, name=f'{label_prefix}_mul')
                kern_prod = False
            else:
                kerns.append(k)

        return MultiAdd(kerns, name=f'{label_prefix}_sum')

    def get_kern(self):
        k_fg = self._load_kerns_from_dict(self.kern.fg, 'fg')
        k_eor = self._load_kerns_from_dict(self.kern.eor, 'eor')
        k_noise = MultiKern._parse_set_params_from_dict(MWhiteHeteroscedastic(), self.kern.noise)

        return k_fg, k_eor, k_noise

    @staticmethod
    def load_from_string_with_defaults(string):
        config = MLGPRConfigFile.get_defaults()
        config += MLGPRConfigFile.load_from_string(string, check_args=False)

        return config


class MLGPRForegroundFitter(fgfit.AbstractForegroundFitter):

    def __init__(self, ml_gpr_config: MLGPRConfigFile):
        self.config = ml_gpr_config

    def process_noise_cube(self, noise_cube, sefd_poly_fit_deg=0, sefd_filter_n_bins=0):
        # Subtract n PCA component from the noise cube ?
        if self.config.kern.noise.estimate_baseline_noise_remove_n_pca > 0:
            fitter = fgfit.PcaForegroundFit(self.config.kern.noise.estimate_baseline_noise_remove_n_pca)
            noise_cube = fitter.run(noise_cube, noise_cube).sub

        # Take the channel difference ?
        if self.config.kern.noise.estimate_baseline_noise_from_channel_diff:
            noise_cube = noise_cube.make_diff_cube_interp()

        # Use simulated cube (with estimated SEFD from noise cube at this stage) ?
        if self.config.kern.noise.use_simulated_noise_cube:
            if self.config.kern.noise.use_sefd_freqs_estimate:
                sefd = noise_cube.estimate_freqs_sefd(sefd_poly_fit_deg=1)
                print(f'Using simulated noise with mean SEFD={sefd.mean():.1f} Jy')
            else:
                sefd = noise_cube.estimate_sefd()
                print(f'Using simulated noise with SEFD={sefd:.1f} Jy')

            w = noise_cube.weights.copy()
            if self.config.kern.noise.scale_baseline_noise:
                w.scale_with_noise_cube(noise_cube, sefd_poly_fit_deg=sefd_poly_fit_deg, sefd_filter_n_bins=sefd_filter_n_bins)

            if self.config.kern.noise.use_noise_std:
                noise_cube = w.get_noise_std_cube(sefd, noise_cube.meta.total_time, fake_apply_win_fct=True)
                noise_cube = (1 / np.sqrt(2) * (noise_cube + 1j * noise_cube))
                noise_cube.weights = w
            else:
                noise_cube = w.simulate_noise(sefd, noise_cube.meta.total_time, fake_apply_win_fct=True)

        return noise_cube

    def run(self, data_cube, data_cube_noise, live_update=False, verbose=False):
        if self.config.pre_proc_remove_freq_mean:
            print('Removing the mean along the frequency dimension')
            data_cube_fit = data_cube.new_with_data(np.ones_like(data_cube.data) * np.mean(data_cube.data, axis=0))
            data_cube = data_cube - data_cube_fit

        k_fg, k_eor, k_noise = self.config.get_kern()
        m_data = MultiData(data_cube, noise_cube=data_cube_noise, uv_bins_du=self.config.kern.uv_bins_du,
                           uv_bins_n_uni=self.config.kern.uv_bins_n_uni)

        gp = MultiGPRegressor(m_data, k_fg + k_eor, k_noise, use_uv_weight=self.config.gp.use_uv_weight)
        if self.config.sampler_method == 'mcmc':
            sampler = MCMCSampler(gp, self.config.mcmc.n_walkers, emcee_moves=self.config.mcmc.move)
            sampler.run(self.config.mcmc.n_steps, verbose=verbose, live_update=live_update)
            result = sampler.get_result(n_burn=self.config.mcmc.n_burn)
        elif self.config.sampler_method == 'nested':
            sampler = NestedSampler(gp, nlive=self.config.nested.nlive, bound=self.config.nested.bound,
                                    sample=self.config.nested.sample)
            result = sampler.run(live_update=live_update)
        elif self.config.sampler_method == 'ultranest':
            sampler = UltraNestNestedSampler(gp, nlive=self.config.ultranest.nlive)
            result = sampler.run(live_update=live_update)
        else:
            raise Exception(f'Error: {self.config.sampler_method} is not a correct sampler method.')

        return MLGPRResult(result, self.config)


class MLGPRResult(object):

    def __init__(self, sampler_result: SamplerResult, ml_gpr_config: MLGPRConfigFile):
        self.config = ml_gpr_config
        self.sampler_result = sampler_result

    @staticmethod
    def load(save_dir, save_name, sampler_method='mcmc'):
        config = MLGPRConfigFile.load_with_defaults(os.path.join(save_dir, save_name + '.config.parset'), 
                                                    check_args=False)

        i_cube = datacube.CartDataCube.load(os.path.join(save_dir, save_name + '.data.h5'))
        if config.kern.noise.use_noise_std:
            noise_cube = datacube.NoiseStdCube.load(os.path.join(save_dir, save_name + '.noise.h5'))
        else:
            noise_cube = datacube.CartDataCube.load(os.path.join(save_dir, save_name + '.noise.h5'))

        k_fg, k_eor, k_noise = config.get_kern()

        m_data = MultiData(i_cube, noise_cube, uv_bins_du=config.kern.uv_bins_du, 
                           uv_bins_n_uni=config.kern.uv_bins_n_uni)
        gp = MultiGPRegressor(m_data, k_fg + k_eor, k_noise)

        if sampler_method == 'mcmc':
            samples_file = os.path.join(save_dir, save_name + '.mcmc_samples.h5')
            mcmc_file = os.path.join(save_dir, save_name + '.mcmc.h5')

            if os.path.exists(samples_file):
                samples = MCMCSamples.load(samples_file)
            else:
                sampler = emcee.backends.HDFBackend(mcmc_file)
                samples = MCMCSamples(sampler.get_chain(), sampler.get_log_prob(), n_burn=config.mcmc.n_burn,
                                      autocorr_time=sampler.get_autocorr_time(tol=0))
        elif sampler_method in ['nested', 'ultranest']:
            samples_file = os.path.join(save_dir, save_name + '.nested_samples.h5')
            samples = NestedSamples.load(samples_file)
        else:
            raise Exception(f'Sampler method {sampler_method} incorrect')

        return MLGPRResult(SamplerResult(gp, samples), config)

    def save(self, save_dir, save_name):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.sampler_result.gp.multi_data.i_cube.save(os.path.join(save_dir, save_name + '.data.h5'))
        self.sampler_result.gp.multi_data.noise_cube.save(os.path.join(save_dir, save_name + '.noise.h5'))
        self.config.save(os.path.join(save_dir, save_name + '.config.parset'))

        self.sampler_result.samples.save(f'{save_dir}/{save_name}.{self.sampler_result.samples.sampler_method}_samples.h5')

    def get_ps(self, ps_gen, kbins, kern_name, n_pick=50, subtract_from=None, fill_gaps=False):
        return self.sampler_result.get_ps_stack(ps_gen, kbins, kern_name=kern_name,
                                                subtract_from=subtract_from, n_pick=n_pick, fill_gaps=fill_gaps)

    def get_ps_fg(self, ps_gen, kbins, n_pick=50, fill_gaps=False):
        return self.get_ps(ps_gen, kbins, 'fg*', n_pick, fill_gaps=fill_gaps)

    def get_ps_eor(self, ps_gen, kbins, n_pick=50, fill_gaps=False):
        return self.get_ps(ps_gen, kbins, 'eor*', n_pick, fill_gaps=fill_gaps)

    def get_ps_res(self, ps_gen, kbins, n_pick=50, fill_gaps=False):
        if fill_gaps:
            i_cube = self.get_interpolated_i_cube()
        else:
            i_cube = self.get_data_cube()
        return self.get_ps(ps_gen, kbins, 'fg*', n_pick, subtract_from=i_cube, fill_gaps=fill_gaps)

    def get_scaled_noise_cube(self):
        if 'noise.alpha' in self.sampler_result.get_parameter_names():
            noise_scale = np.nanmedian(self.sampler_result.get_parameter_samples('noise.alpha'))
            return np.sqrt(noise_scale) * self.get_noise_cube()
        else:
            alpha = self.config.get_kern()[-1].alpha
            if alpha.is_fixed:
                return np.sqrt(alpha.values[0]) * self.get_noise_cube()

        return self.get_noise_cube()

    def get_noise_cube(self):
        return self.sampler_result.gp.multi_data.noise_cube

    def get_data_cube(self):
        return self.sampler_result.gp.multi_data.i_cube

    def get_interpolated_i_cube(self):
        return self.sampler_result.get_interpolated_i_cube()

    def get_component_cubes(self, n_cubes, kern_name='eor', subtract_from=None, fill_gaps=False):
        for c_rec in self.sampler_result.generate_data_cubes(n_cubes, kern_name=kern_name, fill_gaps=fill_gaps):
            if subtract_from is not None:
                c_rec = subtract_from - c_rec
            yield c_rec

    def get_component_cube(self, kern_name='eor', subtract_from=None, fill_gaps=False):
        return [*self.get_component_cubes(1, kern_name=kern_name, subtract_from=subtract_from, fill_gaps=fill_gaps)]

    def get_residual_cubes(self, n_cubes, fill_gaps=False):
        if fill_gaps:
            d = self.get_interpolated_i_cube()
        else:
            d = self.get_data_cube()

        for cube in self.get_component_cubes(n_cubes, 'fg*', subtract_from=d, fill_gaps=fill_gaps):
            yield cube

    def get_residual_cube(self, fill_gaps=False):
        return [*self.get_residual_cubes(1, fill_gaps=fill_gaps)][0]


class MLGPRInjResult(MLGPRResult):

    def __init__(self, sampler_result: SamplerResult, ml_gpr_config: MLGPRConfigFile, data_inj: datacube.CartDataCube):
        MLGPRResult.__init__(self, sampler_result, ml_gpr_config)
        self.data_inj = data_inj

    def get_inj_cube(self):
        return self.data_inj

    @staticmethod
    def load(save_dir, save_name, data_inj, sampler_method='mcmc'):
        ml_res = MLGPRResult.load(save_dir, save_name, sampler_method=sampler_method)
        return MLGPRInjResult(ml_res.sampler_result, ml_res.config, data_inj)
