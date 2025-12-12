# Function for simulating and injecting EoR-like signal
#
# Authors: F.Mertens

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import numpy as np
import pandas as pd

import astropy.io.fits as pf

from scipy import interpolate

from . import psutil
from . import pspec
from . import datacube
from . import fitutil

import GPy


class SimuEorInjector(object):

    def __init__(self, night_id, eor_bin, fitter, fitter_v, data_i, data_v,
                 eor_ls_range=(0.4, 0.8), eor_var_range=(0.05, 0.1)):
        """EoR simulation and injection.eor_bin

        The EoR is simulated by a Gaussian Process with an Exponential covariance
        kernel with length_scale uniformly distributed between eor_ls_range and variance
        uniformly distributed between eor_var_range time the variance of Stokes V.
        While this is not a true EoR simulation this reproduces quite well its frequency
        behavior which is what we are exploiting in the fitting process.

        Args:
            night_id (str): Night ID
            eor_bin (EorBin): Frequency bin window
            fitter (AbstractForegroundFitter): Stokes I foreground fitter
            fitter_v (AbstractForegroundFitter): Stokes V foreground fitter
            data_i (DataCube): Stokes I data cube
            data_v (DataCube): Stokes V data cube
            eor_ls_range (tuple, optional): Range of length-scale for the EoR simulation
            eor_var_range (tuple, optional): Description
        """
        self.night_id = night_id
        self.eor_bin = eor_bin
        self.fitter = fitter
        self.fitter_v = fitter_v
        self.eor_ls_range = eor_ls_range
        self.eor_var_range = eor_var_range
        cols_name = ['night_id', 'eor_bin', 'eor_ls', 'eor_var', 'k',
                     'ratio', 'ratio_iv', 'excess_noise']
        self.ratios = pd.DataFrame(columns=cols_name)
        self.data_sub_list = []
        self.data_sub_diff_list = []
        self.data_eor_list = []
        self.ls_list = []
        self.var_list = []
        self.data_i = data_i
        self.data_v = data_v

    def initial_run(self):
        data_i_fg = self.eor_bin.get_slice_fg(self.data_i)
        data_v_fg = self.eor_bin.get_slice_fg(self.data_v)
        self.gpr_res_v = self.fitter_v.run(data_v_fg, data_v_fg)
        self.gpr_res = self.fitter.run(data_i_fg, self.gpr_res_v.sub)
        if isinstance(self.fitter.config, fitutil.GprConfig) and self.fitter.config.heteroscedastic \
                and not self.fitter.config.fixed_noise:
            noise_scale = self.gpr_res.test_single_parameter('het_Gauss.variance', 0.2, 4, tol=1e-5,
                                                             n_optimize_loop=4)
            self.fitter.config.fixed_noise_scale = noise_scale
            self.gpr_res = self.fitter.run(data_i_fg, self.gpr_res_v.sub)

    def get_eor_cube(self, cube, v_eor, ls_eor):
        kern_eor = GPy.kern.Exponential(1, lengthscale=ls_eor, variance=v_eor)

        y_eor = get_gp_samples(self.eor_bin.fmhz_fg, len(cube.uu), kern_eor)
        return cube.new_with_data(y_eor)

    def run(self, n, ps_gen, kbins, verbose=True):
        """Run EoR injection simulation n times """
        data_i_fg = self.eor_bin.get_slice_fg(self.data_i)
        data_v_fg = self.eor_bin.get_slice_fg(self.data_v)

        # if isinstance(self.fitter, fgfit.GprForegroundFit):
        #     var_eor = fitutil.get_model_parameter(self.gpr_res.gpr_res.model.kern, 'eor')[0]
        #     self.fitter.config.eor_kern.variance.constrain_bounded(0.25 * var_eor, 1.5 * var_eor)
        #     self.fitter.config.eor_kern.variance = var_eor

        pr = psutil.progress_report(n)
        for i in range(n):
            pr(i)
            ls = np.random.uniform(self.eor_ls_range[0], self.eor_ls_range[1])
            var = np.random.uniform(self.eor_var_range[0], self.eor_var_range[1])

            data_eor = self.get_eor_cube(data_i_fg, var * np.var(data_v_fg.data), ls)
            data_i_eor = data_i_fg + data_eor

            res = self.fitter.run(data_i_eor, self.gpr_res_v.sub)

            # print res.gpr_res.model

            self.data_sub_list.append(res.sub)
            self.data_eor_list.append(data_eor)

            dcube = res.sub - self.gpr_res.sub
            # dcube.cov_err.data_scale = dcube.cov_err.data_scale.mean() * np.ones_like(dcube.cov_err.data_scale)
            data_eor.set_weights(dcube.weights)

            ps3d_rec_diff = ps_gen.get_ps3d(kbins, dcube)
            ps3d_simu_eor = ps_gen.get_ps3d(kbins, data_eor)
            ratio = ps3d_rec_diff.data / ps3d_simu_eor.data

            if verbose:
                print('ls=%.2f, var=%5f' % (ls, var))
                print('Ratios:', ratio)

            self.data_sub_diff_list.append(dcube)

            self.ls_list.append(ls)
            self.var_list.append(var)

    def get_ps(self, ps_gen):
        ps = ps_gen.get_ps(self.data_sub_list[0])
        all_sub_ps = [ps_gen.get_ps(sub).data for sub in self.data_sub_list]
        all_sub_diff_ps = [ps_gen.get_ps(diff).data for diff in self.data_sub_diff_list]
        all_eor_ps = [ps_gen.get_ps(sub).data for sub in self.data_eor_list]

        sub_ps = pspec.SpatialPowerSpectra(np.median(all_sub_ps, axis=0),
                                           psutil.robust_std(all_sub_ps, axis=0),
                                           ps.freqs, ps.el, ps.k_per)

        sub_diff_ps = pspec.SpatialPowerSpectra(np.median(all_sub_diff_ps, axis=0),
                                                psutil.robust_std(all_sub_diff_ps, axis=0),
                                                ps.freqs, ps.el, ps.k_per)

        eor_ps = pspec.SpatialPowerSpectra(np.median(all_eor_ps, axis=0),
                                           psutil.robust_std(all_eor_ps, axis=0),
                                           ps.freqs, ps.el, ps.k_per)

        return sub_ps, sub_diff_ps, eor_ps

    def get_ps2d(self, ps_gen):
        ps2d = ps_gen.get_ps2d(self.data_sub_list[0])
        all_sub_ps2d = [ps_gen.get_ps2d(sub).data for sub in self.data_sub_list]
        all_sub_diff_ps = [ps_gen.get_ps2d(diff).data for diff in self.data_sub_diff_list]
        all_eor_ps2d = [ps_gen.get_ps2d(sub).data for sub in self.data_eor_list]

        sub_ps2d = pspec.CylindricalPowerSpectra(np.median(all_sub_ps2d, axis=0),
                                                 psutil.robust_std(all_sub_ps2d, axis=0),
                                                 ps2d.delay, ps2d.el, ps2d.k_per, ps2d.k_par)

        sub_diff_ps2d = pspec.CylindricalPowerSpectra(np.median(all_sub_diff_ps, axis=0),
                                                      psutil.robust_std(all_sub_diff_ps, axis=0),
                                                      ps2d.delay, ps2d.el, ps2d.k_per, ps2d.k_par)

        eor_ps2d = pspec.CylindricalPowerSpectra(np.median(all_eor_ps2d, axis=0),
                                                 psutil.robust_std(all_eor_ps2d, axis=0),
                                                 ps2d.delay, ps2d.el, ps2d.k_per, ps2d.k_par)

        return sub_ps2d, sub_diff_ps2d, eor_ps2d

    def get_ps3d(self, ps_gen, kbins):
        ps3d = ps_gen.get_ps3d(kbins, self.data_sub_list[0])
        all_sub_ps3d = [ps_gen.get_ps3d(kbins, sub).data for sub in self.data_sub_list]
        all_sub_diff_ps = [ps_gen.get_ps3d(kbins, diff).data for diff in self.data_sub_diff_list]
        all_eor_ps3d = [ps_gen.get_ps3d(kbins, sub).data for sub in self.data_eor_list]

        sub_ps3d = pspec.SphericalPowerSpectra(np.median(all_sub_ps3d, axis=0),
                                               psutil.robust_std(all_sub_ps3d, axis=0),
                                               kbins, ps3d.k_mean)

        sub_diff_ps3d = pspec.SphericalPowerSpectra(np.median(all_sub_diff_ps, axis=0),
                                                    psutil.robust_std(all_sub_diff_ps, axis=0),
                                                    kbins, ps3d.k_mean)

        eor_ps3d = pspec.SphericalPowerSpectra(np.median(all_eor_ps3d, axis=0),
                                               psutil.robust_std(all_eor_ps3d, axis=0),
                                               kbins, ps3d.k_mean)

        return sub_ps3d, sub_diff_ps3d, eor_ps3d

    def generate_ratios(self, ps_gen, kbins):
        """Generate statistics on the simulation.

        It returns a pandas DataFrame, one line per simulation, with the following columns:

        night_id: night ID
        eor_bin: EorBin name
        eor_ls: length-scale of the EoR simulated signal
        eor_var: variance of the EoR simulated signal
        k: k at which the PS3D is computed
        ratio: ratio between input and recovered EoR signal
        ratio_iv: ratio between Stokes I residual and Stokes V
        excess_noise: excess noise compute in k bin [1, 1.5]

        Args:
            ps_gen (BasePowerSpectra): A power spectra object.
            kbins (TYPE): The k bins on which stats will be computed

        Returns:
            DataFrame: pandas DataFrame with statistics on the simulation
        """
        # ps_gen.config.cov_err_n_samples = 100
        ps3d_sub = ps_gen.get_ps3d(kbins, self.gpr_res.sub)
        ps3d_sub_v = ps_gen.get_ps3d(kbins, self.gpr_res_v.sub)

        ps3d_high = ps_gen.get_ps3d([1, 1.5], self.gpr_res.sub)
        ps3d_high_v = ps_gen.get_ps3d([1, 1.5], self.gpr_res_v.sub)

        self.ratio_iv = ps3d_sub.data / ps3d_sub_v.data
        self.excess_noise_ratio = ps3d_high.data[0] / ps3d_high_v.data[0]

        pr = psutil.progress_report(len(self.data_eor_list))
        i = 0
        for simu_eor, simu_rec, ls, var in zip(self.data_eor_list, self.data_sub_diff_list,
                                               self.ls_list, self.var_list):
            pr(i)
            ps3d_rec_diff = ps_gen.get_ps3d(kbins, simu_rec)
            ps3d_simu_eor = ps_gen.get_ps3d(kbins, simu_eor)
            ratio = ps3d_rec_diff.data / ps3d_simu_eor.data

            self._add_res(ps3d_sub.k_mean, ratio, ls, var)
            i += 1

        return self.ratios

    def _add_res(self, ks, ratios, ls, var):
        for i in range(len(ks)):
            self.ratios.loc[len(self.ratios)] = [self.night_id, self.eor_bin.name, ls, var,
                                                 ks[i], ratios[i], self.ratio_iv[i],
                                                 self.excess_noise_ratio]


class SimuFitter(object):

    def __init__(self, simu_gen, ps_gen, pre_fitter, fitter):
        self.simu_gen = simu_gen
        self.ps_gen = ps_gen
        self.eor = ps_gen.eor
        self.pre_fitter = pre_fitter
        self.fitter = fitter

    def run(self, ls_fg, var_fg, ls_eor, var_eor, test_no_eor=False):
        self.simu = self.simu_gen.simu(ls_fg, var_fg, ls_eor, var_eor)

        if self.pre_fitter is not None:
            gpr_res_pre = self.pre_fitter.run(self.eor.get_slice_fg(self.simu.obs),
                                              self.eor.get_slice_fg(self.simu.noise))

            self.gpr_res = self.fitter.run(self.eor.get_slice_fg(self.simu.obs) - gpr_res_pre.fit,
                                           self.eor.get_slice_fg(self.simu.noise))
        else:
            if test_no_eor:
                self.fitter.config.include_eor = False
                self.gpr_res = self.fitter.run(self.eor.get_slice_fg(self.simu.obs),
                                               self.eor.get_slice_fg(self.simu.noise))
                log_lik_no_eor = self.gpr_res.gpr_res.model.log_likelihood()
                self.fitter.config.include_eor = True

            self.gpr_res = self.fitter.run(self.eor.get_slice_fg(self.simu.obs),
                                           self.eor.get_slice_fg(self.simu.noise))
            log_lik_eor = self.gpr_res.gpr_res.model.log_likelihood()

            if test_no_eor:
                return log_lik_no_eor, log_lik_eor

            return log_lik_eor, log_lik_eor

    def get_eor_model(self):
        k_eor = fitutil.get_kern_startwith(self.gpr_res.gpr_res.model.kern, 'eor')
        ds = self.gpr_res.sub.cov_err.data_scale.mean().real / self.simu.noise.data.std()
        var_res, ls_res = k_eor.param_array

        return ls_res, var_res * ds ** 2

    def get_ps3d_sub(self, kbins):
        return self.ps_gen.get_ps3d(kbins, self.gpr_res.sub)

    def get_ps3d_noise(self, kbins, with_excess=True):
        n = self.simu.noise
        if with_excess:
            n = self.simu.noise + self.simu.excess
        return self.ps_gen.get_ps3d(kbins, n)

    def get_ps3d_eor(self, kbins):
        return self.ps_gen.get_ps3d(kbins, self.simu.eor)

    def get_ps3d_rec(self, kbins):
        return self.ps_gen.get_ps3d_with_noise(kbins, self.gpr_res.sub, self.simu.noise + self.simu.excess)

    def get_ps3d_eor_rec(self, kbins):
        if hasattr(self.gpr_res, 'get_eor_model'):
            return self.ps_gen.get_ps3d(kbins, self.gpr_res.get_eor_model())
        else:
            return self.get_ps3d_rec(self, kbins)

    def get_ps3d_fg_err(self, kbins):
        fg_cube = self.eor.get_slice_fg(self.simu.fg) + self.eor.get_slice_fg(self.simu.fg_med)
        return self.ps_gen.get_ps3d(kbins, fg_cube - self.gpr_res.fit, with_cov_err=-1)


class SimuMC(object):

    def __init__(self, simu_gen, ps_gen, fitter, n_simu, ls_fg, var_fg,
                 ls_eor, var_eor, kbins, kbins_l=[0, 0.2, 0.4, 0.6]):
        self.simu_gen = simu_gen
        self.ps_gen = ps_gen
        self.fitter = fitter
        self.n_simu = n_simu
        self.ls_fg = ls_fg
        self.var_fg = var_fg
        self.ls_eor = ls_eor
        self.var_eor = var_eor
        self.kbins = kbins
        self.kbins_l = kbins_l

        cols_name = ['ls_fg', 'ls_eor', 'var_fg', 'var_eor', 'ls_eor_rec', 'var_eor_rec',
                     'log_lik_eor`', 'log_lik_no_eor', 'k', 'ps_sub', 'ps_noise', 'ps_eor',
                     'ps_rec_eor', 'ps_fg_err']

        self.table_large = pd.DataFrame(columns=cols_name)
        self.table_small = pd.DataFrame(columns=cols_name)

    def _store_table(self, table, params, simu_gpr, kbins):
        ps3d_sub = simu_gpr.get_ps3d_sub(kbins).data
        ps3d_noise = simu_gpr.get_ps3d_noise(kbins).data
        ps3d_eor = simu_gpr.get_ps3d_eor(kbins).data
        ps3d_eor_rec = simu_gpr.get_ps3d_rec(kbins).data
        ps3d_fg_err = simu_gpr.get_ps3d_fg_err(kbins).data

        k_mean = simu_gpr.get_ps3d_sub(kbins).k_mean

        print(ps3d_eor_rec / ps3d_eor)

        p = np.repeat([params], len(k_mean), axis=0)
        r = np.vstack([k_mean, ps3d_sub, ps3d_noise, ps3d_eor, ps3d_eor_rec, ps3d_fg_err]).T

        for line in np.hstack([p, r]):
            table.loc[len(table)] = line

    def run(self, verbose=True):
        pt = psutil.progress_tracker(self.n_simu)

        for i in range(self.n_simu):
            ls_fg = self.ls_fg.get()
            ls_eor = self.ls_eor.get()
            var_fg = self.var_fg.get()
            var_eor = self.var_eor.get()

            simu_gpr = SimuFitter(self.simu_gen, self.ps_gen, None, self.fitter)
            log_lik_eor, log_lik_no_eor = simu_gpr.run(ls_fg, var_fg, ls_eor, var_eor)

            ps3d_sub = simu_gpr.get_ps3d_sub(self.kbins_l).data
            ps3d_noise = simu_gpr.get_ps3d_noise(self.kbins_l).data
            ps3d_eor = simu_gpr.get_ps3d_eor(self.kbins_l).data
            ps3d_eor_rec = simu_gpr.get_ps3d_eor_rec(self.kbins_l).data

            ls_res, var_res = simu_gpr.get_eor_model()

            if verbose:
                print('Res: %s | %.2f -> %.2f | %.2f -> %.2f -- %s' % (ls_fg, ls_eor, ls_res, np.sqrt(var_eor),
                                                                       np.sqrt(var_res), pt(i)))

                print('  Ratio I-V:', ', '.join(['%.2f' % k for k in (ps3d_sub - ps3d_noise) / ps3d_eor]))
                print('  Ratio EoR:', ', '.join(['%.2f' % k for k in ps3d_eor_rec / ps3d_eor]))

            params = [ls_fg, ls_eor, var_fg, var_eor, ls_res, var_res, log_lik_eor, log_lik_no_eor]
            self._store_table(self.table_large, params, simu_gpr, self.kbins_l)
            self._store_table(self.table_small, params, simu_gpr, self.kbins)


class SimuCubeGenerator(object):

    def get(self):
        return NotImplementedError()


class SimuUniqueCube(SimuCubeGenerator):

    def __init__(self, cube):
        self.cube = cube

    def get(self, *args):
        return self.cube


class SimuCubeFct(SimuCubeGenerator):

    def __init__(self, fct):
        self.fct = fct

    def get(self, *args):
        return self.fct(*args)


class SimuRandomPoly(SimuCubeGenerator):

    def __init__(self, freqs, res, fov, umin, umax, gen_domain=[-1., 1.], gen_range=1, max_taper=1e1, min_order=None):
        nx = int(np.round(fov / res))
        self.meta = datacube.ImageMetaData.from_res(res, (nx, nx))
        self.uu, self.vv, _ = psutil.get_ungrid_vis_idx((nx, nx), res, umin, umax)
        self.gen_domain = gen_domain
        self.gen_range = gen_range
        self.freqs = freqs
        self.max_taper = max_taper
        self.min_order = min_order

    @staticmethod
    def from_cube(cube, gen_domain=[-1., 1.], gen_range=1, max_taper=1e1, min_order=None):
        return SimuRandomPoly(cube.freqs, cube.meta.res, cube.meta.theta_fov, cube.ru.min(), cube.ru.max(),
                              gen_domain=gen_domain, gen_range=gen_range, max_taper=max_taper, min_order=min_order)

    def get(self, variance, order):
        x = np.linspace(self.gen_domain[0], self.gen_domain[1], len(self.freqs))

        A = np.vstack([x ** k for k in np.arange(0, order + 1)]).T
        t = 1 / np.logspace(0, np.log10(self.max_taper), num=order + 1)
        C = (2 * (np.random.rand(order + 1, len(self.uu)) - 0.5))

        M = np.ones_like(C)
        if self.min_order is not None:
            orders = np.random.randint(self.min_order, order + 1, size=len(self.uu))
            for i in range(len(self.uu)):
                M[orders[i] + 1:, i] = 0

        Y = np.dot(A, C * M * t[:, None])

        data = (Y - Y.mean()) / Y.std() * variance ** 0.5

        return datacube.CartDataCube(data, self.uu, self.vv, self.freqs, self.meta)


class SimuRandomSin(SimuCubeGenerator):

    def __init__(self, freqs, res, fov, umin, umax, per_max=100, n_sin=100):
        nx = int(np.round(fov / res))
        self.meta = datacube.ImageMetaData.from_res(res, (nx, nx))
        self.uu, self.vv, _ = psutil.get_ungrid_vis_idx((nx, nx), res, umin, umax)
        self.freqs = freqs
        self.per_max = per_max
        self.n_sin = n_sin

    @staticmethod
    def from_cube(cube, per_max=100, n_sin=100):
        return SimuRandomSin(cube.freqs, cube.meta.res, cube.meta.theta_fov, cube.ru.min(), cube.ru.max(),
                             per_max=per_max, n_sin=n_sin)

    def get(self, variance, per_min):
        n_modes = len(self.uu)
        t = per_min + (self.per_max - per_min) * np.random.random((self.n_sin, n_modes))
        v = np.random.randn(self.n_sin, n_modes)

        data = (v[:, :, None] * np.sin(2 * np.pi * self.freqs * 1e-6 / t[:, :, None])).sum(axis=0).T
        data = data / data.std() * variance ** 0.5

        return datacube.CartDataCube(data, self.uu, self.vv, self.freqs, self.meta)


class SimuGPCube(SimuCubeGenerator):

    def __init__(self, freqs, kern, res, fov, umin, umax):
        nx = int(np.round(fov / res))
        self.meta = datacube.ImageMetaData.from_res(res, (nx, nx))
        self.uu, self.vv, _ = psutil.get_ungrid_vis_idx((nx, nx), res, umin, umax)
        self.ru = np.sqrt(self.uu ** 2 + self.vv ** 2)
        self.kern = kern
        self.freqs = freqs

    @staticmethod
    def from_cube(cube, kern):
        return SimuGPCube(cube.freqs, kern, cube.meta.res, cube.meta.theta_fov,
                          cube.ru.min(), cube.ru.max() + 0.001)

    def get(self, variance, lengthscale):
        if variance == 0:
            return datacube.CartDataCube(np.zeros((len(self.freqs), len(self.uu))), self.uu,
                                         self.vv, self.freqs, self.meta)
        if isinstance(lengthscale, AbstractParameter):
            if not isinstance(variance, AbstractParameter):
                variance = Constant(variance)
            data = np.zeros((len(self.freqs), len(self.uu)), dtype=np.complex128)
            for i in range(len(self.uu)):
                if isinstance(lengthscale, FctParameter):
                    self.kern.lengthscale = lengthscale.get(self.ru[i])
                else:
                    self.kern.lengthscale = lengthscale.get()

                if isinstance(variance, FctParameter):
                    self.kern.variance = abs(variance.get(self.ru[i])) / 2.
                else:
                    self.kern.variance = abs(variance.get()) / 2.

                data[:, i] = get_gp_samples(self.freqs * 1e-6, 1, self.kern)[:, 0]
                # data[:, i] = data[:, i] * self.kern.variance / data[:, i].var()
            data = data * self.kern.variance / data.var()
        else:
            self.kern.lengthscale = lengthscale
            self.kern.variance = variance / 2.
            data = get_gp_samples(self.freqs * 1e-6, len(self.uu), self.kern)
            data = data * variance / data.var()
        return datacube.CartDataCube(data, self.uu, self.vv, self.freqs, self.meta)


class SimuWhiteNoise(SimuCubeGenerator):

    def __init__(self, freqs, res, shape, umin, umax, var):
        self.uu, self.vv, _ = psutil.get_ungrid_vis_idx(shape, res, umin, umax)
        self.meta = datacube.ImageMetaData.from_res(res, shape)
        self.freqs = freqs
        self.var = var

    def get(self):
        noise = np.sqrt(np.atleast_1d(self.var)[:, None]) * (np.random.randn(len(self.freqs), len(self.uu)) +
                                                             1j * np.random.randn(len(self.freqs), len(self.uu)))
        return datacube.CartDataCube(noise, self.uu, self.vv, self.freqs, self.meta)


class SimuNoiseFromWeightCube(SimuCubeGenerator):

    def __init__(self, weight_cube_file, sefd, time, theta_fov, umin, umax, scale_factor=1):
        self.weight_cube = datacube.CartWeightCube.load(weight_cube_file)
        self.sefd = sefd
        self.time = time
        self.theta_fov = theta_fov
        self.umin = umin
        self.umax = umax
        self.scale_factor = scale_factor

    def get(self):
        noise_cube = self.scale_factor * self.weight_cube.simulate_noise(self.sefd, self.time)
        if np.round(self.theta_fov, 3) < np.round(noise_cube.meta.theta_fov, 3):
            noise_cube = noise_cube.reduce_fov(self.theta_fov)

        noise_cube.filter_uvrange(self.umin, self.umax)

        return noise_cube


class SimuFromImageCube(datacube.CartDataCube):

    def __init__(self, fits_cube_file, fits_start_freq, fits_df, fits_res,
                 freqs, theta_fov, umin, umax, pb_fwhm=None, interp_kind='quadratic'):
        self.fits_cube_file = fits_cube_file
        self.fits_start_freq = fits_start_freq
        self.fits_df = fits_df
        self.fits_res = fits_res
        self.freqs = freqs
        self.theta_fov = theta_fov
        self.umin = umin
        self.umax = umax
        self._cube_cache = None
        self.pb_fwhm = pb_fwhm
        self.interp_kind = interp_kind

    def get(self, *args):
        if not self._cube_cache:
            if isinstance(self.fits_cube_file, np.ndarray):
                cube = self.fits_cube_file
            else:
                cube = pf.getdata(self.fits_cube_file).squeeze()
            nf, nx, ny = cube.shape
            cube_freqs = np.arange(self.fits_start_freq, self.fits_start_freq + self.fits_df * nf, self.fits_df)

            cube_meta = datacube.ImageMetaData.from_res(self.fits_res, (nx, ny))
            i_cube = datacube.CartImageCube(cube, cube_freqs, cube_meta)
            i_cube.trim(self.theta_fov)
            v_cube = i_cube.ft(self.umin, self.umax)

            if self.pb_fwhm is not None:
                beam = psutil.get_beam_cart(v_cube.meta.res, v_cube.meta.shape, 'gaussian', self.pb_fwhm)
                pb_scale = np.sqrt((beam ** 2).mean())
            else:
                pb_scale = 1

            data = pb_scale * interpolate.interp1d(v_cube.freqs, v_cube.data,
                                                   kind=self.interp_kind, axis=0)(self.freqs)

            self._cube_cache = datacube.CartDataCube(data, v_cube.uu, v_cube.vv, self.freqs, v_cube.meta)

        if len(args) > 0:
            var_scale = args[0] / self._cube_cache.data.var()
        else:
            var_scale = 1

        return var_scale ** 0.5 * self._cube_cache


class SimuGRFCube(object):

    def __init__(self, freqs, grf_ps_fct, freq_fct, res, fov, umin, umax):
        nx = int(np.round(fov / res))
        self.meta = datacube.ImageMetaData.from_res(res, (nx, nx))
        self.uu, self.vv, _ = psutil.get_ungrid_vis_idx((nx, nx), res, umin, umax)
        self.ru = np.sqrt(self.uu ** 2 + self.vv ** 2)
        self.freqs = freqs
        self.grf_ps_fct = grf_ps_fct
        self.freq_fct = freq_fct

    def get(self, variance):
        data_i = self.grf_ps_fct(2 * np.pi * self.ru) * np.random.randn(len(self.uu))
        data_r = self.grf_ps_fct(2 * np.pi * self.ru) * np.random.randn(len(self.uu))
        data = self.freq_fct(self.freqs)[:, None] * (data_r + 1j * data_i)[None, :]
        data = np.sqrt(variance / data.var()) * data
        return datacube.CartDataCube(data, self.uu, self.vv, self.freqs, self.meta)


class Simulation(object):

    def __init__(self, obs, fg, fg_med, eor, noise, excess=None):
        self.obs = obs
        self.fg = fg
        self.fg_med = fg_med
        self.noise = noise
        self.eor = eor
        self.excess = excess


class SimulationGenerator(object):

    def __init__(self, fg_gen, fg_med_gen, eor_gen, noise_gen, excess_gen=None):
        self.fg_gen = fg_gen
        self.fg_med_gen = fg_med_gen
        self.eor_gen = eor_gen
        self.noise_gen = noise_gen
        self.excess_gen = excess_gen

    def simu(self, ls_fg, var_fg, ls_eor, var_eor):
        np.random.seed()

        fg = self.fg_gen.get()
        noise = self.noise_gen.get()
        if self.excess_gen is not None:
            excess = self.excess_gen.get()
        else:
            excess = noise.new_with_data(np.zeros_like(noise.data))
        var_noise = noise.data.var()
        eor = self.eor_gen.get(var_eor * var_noise, ls_eor)
        fg_med = self.fg_med_gen.get(var_fg * var_noise, ls_fg)

        # Normalize cubes
        noise = noise.new_with_data(noise.get_slice(fg.freqs[0], fg.freqs[-1]).data, freqs=fg.freqs)
        fg_med = fg_med.new_with_data(fg_med.get_slice(fg.freqs[0], fg.freqs[-1]).data, freqs=fg.freqs)
        eor = eor.new_with_data(eor.get_slice(fg.freqs[0], fg.freqs[-1]).data, freqs=fg.freqs)
        excess = excess.new_with_data(excess.get_slice(fg.freqs[0], fg.freqs[-1]).data, freqs=fg.freqs)

        obs = fg + fg_med + eor + noise + excess
        return Simulation(obs, fg, fg_med, eor, noise, excess)


class AbstractParameter(object):

    def __call__(self):
        return self.get()

    def get(self, shape=None):
        pass


class Constant(AbstractParameter):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def get(self, shape=None):
        if shape is None:
            return self.value
        a = np.empty(shape)
        a.fill(self.value)
        return a


class FctParameter(AbstractParameter):

    def __init__(self, fct, label=''):
        self.fct = fct
        self.label = label

    def __str__(self):
        return self.label

    def get(self, *args):
        return self.fct(*args)


class ListValues(AbstractParameter):

    def __init__(self, values, label=''):
        self.values = values
        self.i = -1
        self.label = label

    def __str__(self):
        return self.label

    def get(self):
        self.i = (self.i + 1) % len(self.values)
        return self.values[self.i]


class RandomUniform(AbstractParameter):

    def __init__(self, min, max, seed=None, label=''):
        self.max = max
        self.min = min
        self.seed = seed
        self.label = label

    def __str__(self):
        return self.label

    def get(self, shape=None):
        if self.min == self.max:
            return Constant(self.min).get(shape)
        return psutil.get_random(seed=self.seed).uniform(self.min, self.max, size=shape)


class RandomNormal(AbstractParameter):

    def __init__(self, mean, sigma, seed=None):
        self.mean = mean
        self.sigma = sigma
        self.seed = seed

    def get(self, shape=None):
        if self.sigma == 0:
            return Constant(self.mean).get(shape)
        return psutil.get_random(seed=self.seed).normal(self.mean, self.sigma, size=shape)


def get_gp_samples(x, m, kern):
    """Simulate a signal from a Gaussian Process with given kernel

    Args:
        x (list): Frequencies
        m (int): Number of modes/visibilities to simulated
        kern (GPy Kernel): The covariance function / kernel

    Returns:
        (n_freqs, n_modes): an array of simulated data
    """
    real = np.random.multivariate_normal(np.zeros_like(x), kern.K(x[:, None], x[:, None]), m).T
    imag = np.random.multivariate_normal(np.zeros_like(x), kern.K(x[:, None], x[:, None]), m).T
    return real + 1j * imag
