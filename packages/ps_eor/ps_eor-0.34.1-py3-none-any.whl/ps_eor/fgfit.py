# Class for Foreground fitting and removal
#
# Authors: F.Mertens

import os
import time
from io import open

import json

import numpy as np

from . import fitutil
from . import datacube
from . import psutil
from . import sphcube


class FitterResult(object):
    """Fitter result container

    Attributes:
        fit (DataCube): the model
        sub (DataCube): the data - model
    """

    def __init__(self, cube_fit, cube_sub):
        self.fit = cube_fit
        self.sub = cube_sub


class GprForegroundResult(FitterResult):
    """GPR fitter result container

    Attributes:
        post_fit (DataCube): The post-fit (PCA) part of the model
        pre_fit (DataCube): The pre-fit (poly fit) part of the model
    """

    def __init__(self, gpr_res, cube_fit, cube_sub, cube_pre_fit,
                 cube_post_fit, fg_med=None, eor=None, fg_med_full=None,
                 int_fg_full=None, kern=None, cube_noise=None):
        """Encapsulate GPR foreground fitting result

        Args:
            gpr_res (GprResult): GPR fitting result
            cube_fit (DataCube): Foreground cube
            cube_sub (DataCube): Residual cube
            cube_pre_fit (DataCube): pre-fit foreground cube
            cube_post_fit (DataCube): post-fit foreground cube
        """
        self.gpr_res = gpr_res
        self.pre_fit = cube_pre_fit
        self.post_fit = cube_post_fit
        self.fg_med = fg_med
        self.eor = eor
        self.noise = cube_noise

        FitterResult.__init__(self, cube_fit, cube_sub)

        if self.gpr_res is not None:
            # Load the foreground fit with filled gaps
            fg_kern = fitutil.get_kern_startwith(self.gpr_res.model.kern, 'fg')
            self.fg_med_full = self.get_model_component(fg_kern, fill_gaps=True)

            int_fg_kern = fitutil.get_kern_startwith(self.gpr_res.model.kern, 'int_fg')
            if int_fg_kern is not None:
                self.int_fg_full = self.get_model_component(int_fg_kern, fill_gaps=True)
                self.pre_fit = self.get_model_component(int_fg_kern)
            else:
                self.int_fg_full = None

            self.kern = self.gpr_res.model.kern.copy()
        else:
            self.int_fg_full = int_fg_full
            self.fg_med_full = fg_med_full
            self.kern = kern

    def get_model_component(self, kern, include_noise=False, add_cov_err_sample=False, fill_gaps=False):
        '''Return a DataCube for the given GPR model component'''
        freqs = self.fit.freqs
        compute_at_x = None

        if fill_gaps:
            freqs = np.array(sorted(np.concatenate((freqs, psutil.get_freqs_gaps(freqs)))))
            compute_at_x = freqs[:, None] * 1e-6
        y_fit_part, cov_err = fitutil.get_model_cmpt(self.gpr_res, kern, include_noise=include_noise,
                                                     compute_at_x=compute_at_x)
        y_scale = self.gpr_res.y_scale

        cov_err = datacube.ErrorCovariance(freqs, cov_err, y_scale)

        if add_cov_err_sample:
            y_fit_part = y_fit_part + cov_err.get_sample()

        cube = self.fit.new_with_data(y_fit_part, cov_err, freqs=freqs)

        if fill_gaps:
            # weights are useless on the missing data points, so better discard them
            cube.weights = None

        return cube

    def get_model_noise(self):
        if fitutil.get_kern_startwith(self.gpr_res.model.kern, 'noise'):
            return self.get_model_component('noise', True)

        n_freqs, _ = self.fit.data.shape
        cov_err = np.zeros((n_freqs, n_freqs))
        cov_err[np.diag_indices(n_freqs)] = fitutil.get_model_noise(self.gpr_res)
        cov_err = datacube.ErrorCovariance(self.fit.freqs, cov_err, self.gpr_res.y_scale)

        return self.fit.new_with_data(np.zeros_like(self.fit.data), cov_err)

    def get_fg_model(self, add_cov_err_sample=False):
        '''Return a DataCube for the GPR FG component'''
        if self.fg_med is None or add_cov_err_sample:
            fg_med = self.get_model_component(fitutil.get_kern_startwith(self.gpr_res.model.kern, 'fg'),
                                              add_cov_err_sample=add_cov_err_sample)
            if add_cov_err_sample:
                return fg_med
            self.fg_med = fg_med
        return self.fg_med

    def get_eor_model(self, add_cov_err_sample=False):
        '''Return a DataCube for the GPR EoR component'''
        if self.eor is None or add_cov_err_sample:
            eor = self.get_model_component(fitutil.get_kern_startwith(self.gpr_res.model.kern, 'eor'),
                                           add_cov_err_sample=add_cov_err_sample)
            if add_cov_err_sample:
                return eor
            self.eor = eor
        return self.eor

    def run_on_cube(self, data_cube, n_optimize_loop=0, model=None):
        x = self.sub.freqs * 1e-6

        if model is None:
            model = self.gpr_res.model

        gpr_res = fitutil.gpr_fit_with_model(x, data_cube.data, self.gpr_res.y_scale, model,
                                             n_optimize_loop=n_optimize_loop)

        cov_err = datacube.ErrorCovariance(data_cube.freqs, gpr_res.cov_err, gpr_res.y_scale)

        cube_fit = data_cube.new_with_data(gpr_res.y_fit, cov_err)
        cube_sub = data_cube.new_with_data(gpr_res.y_sub, cov_err)
        cube_pre_fit = data_cube.new_with_data(gpr_res.y_pre_fit)
        cube_post_fit = data_cube.new_with_data(gpr_res.y_post_fit)

        return GprForegroundResult(gpr_res, cube_fit, cube_sub, cube_pre_fit, cube_post_fit)

    def test_single_parameter(self, param_name, min_value, max_value, n_optimize_loop=2,
                              tol=1e-3, verbose=False, method='bounded', brute_ns=20):
        return self.gpr_res.test_single_parameter(param_name, min_value, max_value, n_optimize_loop=n_optimize_loop,
                                                  tol=tol, verbose=verbose, method=method, brute_ns=brute_ns)

    @staticmethod
    def load(dir_path, name):
        fit = datacube.CartDataCube.load(os.path.join(dir_path, name + '.fit.h5'))
        sub = datacube.CartDataCube.load(os.path.join(dir_path, name + '.sub.h5'))
        fg_med = datacube.CartDataCube.load(os.path.join(dir_path, name + '.fg_med.h5'))
        eor = datacube.CartDataCube.load(os.path.join(dir_path, name + '.eor.h5'))
        pre_fit = datacube.CartDataCube.load(os.path.join(dir_path, name + '.pre_fit.h5'))
        post_fit = datacube.CartDataCube.load(os.path.join(dir_path, name + '.post_fit.h5'))

        fg_med_full = None
        fg_med_full_file = os.path.join(dir_path, name + '.fg_med_full.h5')
        if os.path.isfile(fg_med_full_file):
            fg_med_full = datacube.CartDataCube.load(os.path.join(dir_path, name + '.fg_med_full.h5'))

        int_fg_full = None
        int_fg_full_file = os.path.join(dir_path, name + '.int_fg_full.h5')
        if os.path.isfile(int_fg_full_file):
            int_fg_full = datacube.CartDataCube.load(os.path.join(dir_path, name + '.int_fg_full.h5'))

        noise = None
        noise_file = os.path.join(dir_path, name + '.noise.h5')
        if os.path.isfile(noise_file):
            noise = datacube.CartDataCube.load(os.path.join(dir_path, name + '.noise.h5'))

        kern = None
        kern_file = os.path.join(dir_path, name + '.kern.json')
        if os.path.isfile(kern_file):
            try:
                with open(os.path.join(dir_path, name + '.kern.json'), mode='r', encoding='utf-8') as f:
                    s = f.read()
                    kern = fitutil.GPy.kern.Kern.from_dict(json.loads(s))
            except (ValueError, TypeError):
                print('Loading kernel parameter failed')
                kern = None

        return GprForegroundResult(None, fit, sub, pre_fit, post_fit, fg_med=fg_med, eor=eor,
                                   fg_med_full=fg_med_full, int_fg_full=int_fg_full, kern=kern, cube_noise=noise)

    def save(self, dir_path, name):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.fit.save(os.path.join(dir_path, name + '.fit.h5'))
        self.sub.save(os.path.join(dir_path, name + '.sub.h5'))
        self.get_fg_model().save(os.path.join(dir_path, name + '.fg_med.h5'))
        self.get_eor_model().save(os.path.join(dir_path, name + '.eor.h5'))
        self.pre_fit.save(os.path.join(dir_path, name + '.pre_fit.h5'))
        self.post_fit.save(os.path.join(dir_path, name + '.post_fit.h5'))

        if self.fg_med_full:
            self.fg_med_full.save(os.path.join(dir_path, name + '.fg_med_full.h5'))

        if self.int_fg_full:
            self.int_fg_full.save(os.path.join(dir_path, name + '.int_fg_full.h5'))

        if self.noise:
            self.noise.save(os.path.join(dir_path, name + '.noise.h5'))

        try:
            with open(os.path.join(dir_path, name + '.kern.json'), mode='w', encoding='utf-8') as f:
                f.write(json.dumps(self.kern.to_dict()))
        except NotImplementedError:
            # Some kernel do not support yet serialization. Ignore the error.
            print('Saving kernel parameter failed')


class MixForegroundResult(FitterResult):

    def __init__(self, cube_fit, cube_sub, cube_mix, inv_trans):
        FitterResult.__init__(self, cube_fit, cube_sub)
        self.mix = cube_mix
        self.inv_trans = inv_trans

    def inverse_transform(self, mode):
        return self.fit.new_with_data(self.inv_trans(mode).T)

    def get_component(self, n):
        return self.mix.get_freq(n)


class AbstractForegroundFitter(object):

    def run(self, data_cube, data_cube_noise):
        return NotImplementedError()


class NoAction(AbstractForegroundFitter):

    def run(self, i_cube, v_cube):
        return FitterResult(i_cube.new_with_data(np.zeros_like(i_cube.data)), i_cube)


class GprForegroundFit(AbstractForegroundFitter):

    def __init__(self, gpr_config):
        """GPR foreground fitter

        Args:
            gpr_config (GprConfig): The GPR config
        """
        self.config = gpr_config

    def run(self, data_cube, data_cube_noise, rnd_seed=None):
        '''Run the foreground fitter and return a GprForegroundResult'''
        x = data_cube.freqs * 1e-6
        np.random.seed(rnd_seed)

        y = data_cube.data
        y_v = data_cube_noise.data
        ru = data_cube.ru

        gpr_res = fitutil.gpr_fit(x, y, y_v, ru, self.config)

        cov_err = datacube.ErrorCovariance(data_cube.freqs, gpr_res.cov_err, gpr_res.y_scale)

        cube_fit = data_cube.new_with_data(gpr_res.y_fit, cov_err)
        cube_sub = data_cube.new_with_data(gpr_res.y_sub, cov_err)
        cube_pre_fit = data_cube.new_with_data(gpr_res.y_pre_fit)
        cube_post_fit = data_cube.new_with_data(gpr_res.y_post_fit)

        cube_sub.set_weights(data_cube.weights)

        return GprForegroundResult(gpr_res, cube_fit, cube_sub, cube_pre_fit, cube_post_fit,
                                   cube_noise=data_cube_noise)


class ScaleNoiseGprForegroundFit(GprForegroundFit):

    def __init__(self, gpr_config):
        GprForegroundFit.__init__(self, gpr_config)

    def run(self, data_cube, data_cube_noise, rnd_seed=None):
        t = time.time()
        np.random.seed(rnd_seed)

        if self.config.use_simulated_noise:
            sefd = data_cube_noise.new_with_cov_err().estimate_sefd()
            print('Using simulated noise with sefd = %.1f Jy' % sefd)
            weights = data_cube_noise.weights.copy()
            if self.config.simulated_noise_scale_kper:
                weights.scale_with_noise_cube(data_cube_noise, sefd_poly_fit_deg=2,
                                              expected_sefd=sefd, scale_freqs=False)

            noise_i = weights.simulate_noise(sefd, data_cube_noise.meta.total_time,
                                             fake_apply_win_fct=True, hermitian=False)
            noise_i.weights = data_cube_noise.weights.copy()
            data_cube_noise = noise_i

        do_scaled_noise = not self.config.fixed_noise and self.config.heteroscedastic

        if do_scaled_noise:
            self.config.fixed_noise_scale = 1
            gpr_res = GprForegroundFit.run(self, data_cube, data_cube_noise, rnd_seed=rnd_seed)

            n_optimize_loop = self.config.noise_scale_search_n_restarts
            tol = self.config.noise_scale_search_tol
            rmin, rmax = self.config.noise_scale_search_range
            method = self.config.noise_scale_search_method
            maxiter = self.config.noise_scale_search_maxiter

            t = time.time()
            print('Testing noise-scale value with method %s...\n' % method)

            noise_scale = gpr_res.test_single_parameter('het_Gauss.variance', rmin, rmax, tol=tol,
                                                        n_optimize_loop=n_optimize_loop,
                                                        method=method, brute_ns=maxiter, verbose=True)

            print('New noise_scale:', noise_scale)
            data_cube_noise = np.sqrt(noise_scale) * data_cube_noise

            print("\nDone in %.2f s\n" % (time.time() - t))

        return GprForegroundFit.run(self, data_cube, data_cube_noise, rnd_seed=rnd_seed)


class MultiGprForegroundResult(object):

    def __init__(self, cube, cube_noise):
        self.gpr_results = []
        self.data_idx = []
        self.fit = cube.new_with_data(np.zeros_like(cube.data))
        self.sub = cube.new_with_data(np.zeros_like(cube.data))
        self.pre_fit = cube.new_with_data(np.zeros_like(cube.data))
        self.post_fit = cube.new_with_data(np.zeros_like(cube.data))
        self.cube_noise = cube_noise

    def add_res(self, gpr_res, data_idx):
        self.gpr_results.append(gpr_res)
        self.data_idx.append(data_idx)
        self.fit.data[:, data_idx] = gpr_res.fit.new_with_cov_err().data
        self.sub.data[:, data_idx] = gpr_res.sub.new_with_cov_err().data
        self.pre_fit.data[:, data_idx] = gpr_res.pre_fit.new_with_cov_err().data
        self.post_fit.data[:, data_idx] = gpr_res.post_fit.new_with_cov_err().data

    def get_model_component(self, kern, include_noise=False, add_cov_err_sample=False):
        cube = self.fit.new_with_data(np.zeros_like(self.fit.data))
        for data_idx, gpr_res in zip(self.data_idx, self.gpr_results):
            b_cube = gpr_res.get_model_component(kern, include_noise=include_noise,
                                                 add_cov_err_sample=add_cov_err_sample)
            cube.data[:, data_idx] = b_cube.new_with_cov_err().data

        return cube


class MultiBaselinesGprForegroundFit(GprForegroundFit):

    def __init__(self, gpr_config, du):
        GprForegroundFit.__init__(self, gpr_config)
        self.du = du

    def _split_cube(self, cube, idx):
        if isinstance(cube, datacube.CartDataCube):
            return datacube.CartDataCube(cube.data[:, idx], cube.uu[idx], cube.vv[idx], cube.freqs, cube.meta)
        elif isinstance(cube, sphcube.SphDataCube):
            return sphcube.SphDataCube(cube.data[:, idx], cube.ll[idx], cube.mm[idx], cube.freqs, cube.meta)
        else:
            raise TypeError('Input cube should be a CartDataCube or a SphDataCube')

    def run(self, data_cube, data_cube_noise):
        multi_gpr_res = MultiGprForegroundResult(data_cube, data_cube_noise)

        for bs, be in psutil.pairwise(np.arange(data_cube.ru.min(), data_cube.ru.max() + self.du, self.du)):
            idx = (data_cube.ru >= bs) & (data_cube.ru <= be)
            i_cube = self._split_cube(data_cube, idx)
            n_cube = self._split_cube(data_cube_noise, idx)
            bs = i_cube.ru.min()
            be = i_cube.ru.max()

            print('Running fitter for baselines %.1f - %.1f lambda (%s modes)' % (bs, be, len(i_cube.ru)))

            gpr_res = GprForegroundFit.run(self, i_cube, n_cube)
            multi_gpr_res.add_res(gpr_res, idx)

        return multi_gpr_res


class GmcaForegroundFit(AbstractForegroundFitter):

    def __init__(self, n_cmpt, mints=0, do_wave_transform=False, do_poly_fit=0):
        """GMCA foreground fitter

        Args:
            n_cmpt (int): Nbs of GMCA component
            mints (int, optional): scalar (final value of the k-mad thresholding)
            do_wave_transform (bool, optional): Perform wavelet transform in frequency before GMCA
            do_poly_fit (int, optional): Perform a polynomial fit after GMCA
        """
        self.n_cmpt = n_cmpt
        self.mints = mints
        self.do_wave_transform = do_wave_transform
        self.do_poly_fit = do_poly_fit

    def run(self, data_cube, data_cube_noise):
        '''Run the foreground fitter and return FG and residual data cubes'''
        w = 1
        if isinstance(data_cube, datacube.DataCube) and data_cube.weights is not None:
            w = data_cube.weights.data

        y = data_cube.data * w

        y_fit = fitutil.alm_gmca_fit(y, self.n_cmpt, data_cube_noise.data,
                                     self.mints, self.do_wave_transform, self.do_poly_fit)

        cube_fit = data_cube.new_with_data(y_fit / w)
        cube_sub = data_cube.new_with_data((y - y_fit) / w)

        cube_sub.set_weights(data_cube.weights)

        return FitterResult(cube_fit, cube_sub)


class PcaForegroundFit(AbstractForegroundFitter):

    def __init__(self, n_cmpt):
        """PCA foreground fitter

        Attributes:
            n_cmpt (TYPE): Nbs of PCA component
        """
        self.n_cmpt = n_cmpt

    def run(self, data_cube, data_cube_noise):
        '''Run the foreground fitter and return FG and residual data cubes'''
        y = data_cube.data

        y_fit, y_mix, inv_trans = fitutil.alm_pca_fit(y, self.n_cmpt, return_mix=True)

        cube_fit = data_cube.new_with_data(y_fit)
        cube_sub = data_cube.new_with_data(y - y_fit)
        cube_mix = data_cube.new_with_data(y_mix, freqs=np.arange(self.n_cmpt))

        cube_sub.set_weights(data_cube.weights)

        return MixForegroundResult(cube_fit, cube_sub, cube_mix, inv_trans)


class PolyForegroundFit(AbstractForegroundFitter):

    def __init__(self, deg, fit_type):
        """Polynomial foreground fitter

        Args:
            deg (int): Degree of the fitting polynomial
            fit_type (str): Either poly, bernstein, power_poly or power_bernstein
        """
        self.deg = deg
        self.fit_type = fit_type
        self.fit_fct = fitutil.get_fit_fct(self.fit_type)

    def run(self, data_cube, data_cube_noise):
        '''Run the foreground fitter and return FG and residual data cubes'''
        x = data_cube.freqs / 1e6
        y = data_cube.data
        y_v = data_cube_noise.data
        noiserms = np.std(y_v, axis=1)

        y_fit = fitutil.alm_poly_fit(x, y, noiserms, self.deg, self.fit_fct)

        cube_fit = data_cube.new_with_data(y_fit)
        cube_sub = data_cube.new_with_data(y - y_fit)

        cube_sub.set_weights(data_cube.weights)

        return FitterResult(cube_fit, cube_sub)
