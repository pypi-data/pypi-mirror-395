# Datacube flagger
#
# Authors: F.Mertens

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import tables
import inspect
import configparser

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from . import psutil
from . import datacube
from . import sphcube
from . import fgfit


class BaseFlagger(psutil.SimpleConfig):

    def __init__(self, **kargs):
        psutil.SimpleConfig.__init__(self)
        self.add('name', 'Flagger', str)
        self.add('action', 'filter', str)
        self.parse_dict(kargs)

    def do_flag(self, i_cube, v_cube, verbose=True):
        return NotImplementedError()

    def is_applicable(self, i_cube):
        return True


class BaseUVFlagger(BaseFlagger):

    def __init__(self, **kargs):
        BaseFlagger.__init__(self, **kargs)

    def do_flag(self, i_cube, v_cube, verbose=True):
        uv_idx = self.get_outliers(i_cube, v_cube)
        if uv_idx is not None:
            n_filter = uv_idx.sum()
            n_tot = len(uv_idx)
            if verbose:
                print('%s: %s %s / %s (%.1f %%)' % (self.name, self.action, n_filter,
                                                    n_tot, n_filter / float(n_tot) * 100))
            if self.action == 'zero_weight':
                i_cube.weights.data[:, uv_idx] = 0
                v_cube.weights.data[:, uv_idx] = 0
            elif self.action == 'filter':
                i_cube.filter_uv_from_index(~uv_idx)
                if v_cube != i_cube:
                    v_cube.filter_uv_from_index(~uv_idx)

        return i_cube, v_cube


class BaseFreqsFlagger(BaseFlagger):

    def __init__(self, **kargs):
        BaseFlagger.__init__(self, **kargs)

    def do_flag(self, i_cube, v_cube, verbose=True):
        freqs_idx = self.get_outliers(i_cube, v_cube)
        if freqs_idx is not None:
            n_filter = freqs_idx.sum()
            n_tot = len(freqs_idx)
            if verbose:
                print('%s: %s %s / %s (%.1f %%)' % (self.name, self.action, n_filter,
                                                    n_tot, n_filter / float(n_tot) * 100))
            if self.action == 'zero_weight':
                i_cube.weights.data[freqs_idx] = 0
                v_cube.weights.data[freqs_idx] = 0
            elif self.action == 'filter':
                i_cube = i_cube.get_slice_from_idx(~freqs_idx)
                if v_cube != i_cube:
                    v_cube = v_cube.get_slice_from_idx(~freqs_idx)

        return i_cube, v_cube


class FixedFreqsFlagger(BaseFreqsFlagger):

    def __init__(self, **kargs):
        BaseFreqsFlagger.__init__(self, **kargs)
        # Frequencies list coma separated in MHz , e.g. 121.3,123.1
        self.add('freqs', '', str)
        self.add('ratio_min_v_var', 0, float)
        self.add('ratio_min_v_var_poly_sub', 4, float)
        self.parse_dict(kargs)

    def get_outliers(self, i_cube, v_cube):
        fmhz = i_cube.freqs * 1e-6
        fwidth = psutil.robust_freq_width(i_cube.freqs) * 1e-6
        fct_norm = lambda f: np.round((f - fmhz[0]) / fwidth).astype(int)

        norm_fmhz = fct_norm(fmhz)
        idxs = []

        for s in self.freqs.split(','):
            if '-' in s:
                a, b = s.split('-')
                idxs.append(np.in1d(norm_fmhz, np.arange(fct_norm(float(a)), fct_norm(float(b)))))
            else:
                idxs.append(np.in1d(norm_fmhz, fct_norm(float(s))))

        idx_full = np.sum(idxs, axis=0).astype(bool)                
        if self.ratio_min_v_var == 0:
            return idx_full

        idx_outside = ~idx_full

        fitter = fgfit.PolyForegroundFit(self.ratio_min_v_var_poly_sub, 'power_poly')
        fit_res = fitter.run(v_cube, v_cube)
        v_var_outside = fit_res.sub.data[idx_outside].var()

        outliers = np.zeros_like(fmhz)
        for idx in idxs:
            if fit_res.sub.data[idx].var() / v_var_outside > self.ratio_min_v_var:
                outliers += idx

        return outliers.astype(bool)


class UVDirectionFlagger(BaseUVFlagger):

    def __init__(self, **kargs):
        BaseUVFlagger.__init__(self, **kargs)
        self.add('direction_deg', 0, float)
        self.add('extend', 0.8, float)
        self.parse_dict(kargs)

    def get_outliers(self, i_cube, v_cube):
        du = self.extend * np.median(np.diff(i_cube.uu))
        d_rad = np.radians(self.direction_deg) % np.pi
        theta = np.arctan2(i_cube.uu, i_cube.vv) % np.pi
        d = (theta - d_rad - np.pi / 2) % np.pi

        uv_idx = (d > (np.pi / 2 - np.arctan(du / i_cube.ru))) & (d < (np.pi / 2 + np.arctan(du / i_cube.ru)))

        return uv_idx

    def is_applicable(self, i_cube):
        return isinstance(i_cube, datacube.CartDataCube)


class SigmaClipper(psutil.SimpleConfig):

    def __init__(self, **kargs):
        psutil.SimpleConfig.__init__(self)
        self.add('nsigma', 5, float)
        self.add('detrend_poly_deg', 2, int)
        self.add('detrend_nsigma_clip', 10, float)
        self.add('stokes', 'V', str)
        self.add('sefd', True, bool)
        self.parse_dict(kargs)

    def get_sigma_clip_mask(self, x, y):
        med = np.nanmedian(y)
        rms = psutil.mad(y)
        # plt.figure()

        if self.detrend_poly_deg > 0:
            mask = abs(y - med) < self.detrend_nsigma_clip * rms
            mw_fct = np.poly1d(np.polyfit(x[mask], y[mask], self.detrend_poly_deg))
            # plt.scatter(x, y)
            # plt.plot(x, mw_fct(x))
            y = y - mw_fct(x)
            med = np.nanmedian(y[mask])
            rms = psutil.mad(y[mask])

        # plt.scatter(x, y)
        # plt.axhline(med)
        # plt.axhline(med + self.nsigma * rms)
        # plt.savefig(self.name + '.png')

        return (y - med) > self.nsigma * rms


class FreqsSigmaClipFlagger(SigmaClipper, BaseFreqsFlagger):

    def __init__(self, **kargs):
        BaseFreqsFlagger.__init__(self, **kargs)
        SigmaClipper.__init__(self, **kargs)

    def get_outliers(self, i_cube, v_cube):
        if self.stokes == 'I':
            cube = i_cube
        else:
            cube = v_cube

        if self.sefd:
            y = cube.estimate_freqs_sefd()
        else:
            y = cube.data.std(axis=1)

        return self.get_sigma_clip_mask(i_cube.freqs, y)

    def is_applicable(self, i_cube):
        if self.sefd:
            return isinstance(i_cube, datacube.CartDataCube)
        else:
            return True


class FreqsWeightsFlagger(BaseFreqsFlagger):

    def __init__(self, **kargs):
        BaseFreqsFlagger.__init__(self, **kargs)
        self.add('ratio', 0.6, float)
        self.add('trend_poly_deg', 2, int)
        self.parse_dict(kargs)

    def get_outliers(self, i_cube, v_cube):
        weights = np.median(v_cube.weights.get(), axis=1)
        mask = weights > 0

        med = np.median(weights[mask])
        rms = psutil.mad(weights[mask])
        mask = abs(weights - med) < 5 * rms

        mw_fct = np.poly1d(np.polyfit(i_cube.freqs[mask], weights[mask], self.trend_poly_deg))

        return weights / mw_fct(i_cube.freqs) < self.ratio

    def is_applicable(self, i_cube):
        return isinstance(i_cube, datacube.CartDataCube)


class UVWeightsFlagger(BaseUVFlagger):

    def __init__(self, **kargs):
        BaseUVFlagger.__init__(self, **kargs)
        self.add('threshold', 0.01, float)
        self.parse_dict(kargs)

    def get_outliers(self, i_cube, v_cube):
        min_weights = v_cube.weights.get().min(axis=0)

        return min_weights < self.threshold * min_weights.max()

    def is_applicable(self, i_cube):
        return isinstance(i_cube, datacube.CartDataCube)


class UVSigmaClipFlagger(SigmaClipper, BaseUVFlagger):

    def __init__(self, **kargs):
        BaseUVFlagger.__init__(self, **kargs)
        SigmaClipper.__init__(self, **kargs)

    def get_outliers(self, i_cube, v_cube):
        if self.stokes == 'I':
            cube = i_cube
        elif self.stokes == 'dI':
            cube = i_cube.make_diff_cube()
        elif self.stokes == 'dV':
            cube = v_cube.make_diff_cube()
        else:
            cube = v_cube

        if self.sefd:
            y = cube.estimate_uv_sefd().data[0]
        else:
            y = cube.data.std(axis=0)

        return self.get_sigma_clip_mask(i_cube.ru, y)

    def is_applicable(self, i_cube):
        return isinstance(i_cube, datacube.CartDataCube)


class LMThetaMaxFlagger(BaseUVFlagger):

    def __init__(self, **kargs):
        BaseUVFlagger.__init__(self, **kargs)
        self.add('th_in', 0.5, float)
        self.add('relative_threshold', 0.001, float)
        self.parse_dict(kargs)

    def get_outliers(self, i_cube, v_cube):
        ml_r = i_cube.mm / (1. * i_cube.ll)
        var_df_i = i_cube.data.var(axis=0)
        th = self.relative_threshold * var_df_i[ml_r < self.th_in].mean()
        th_max = np.arcsin(np.median(sorted(ml_r[var_df_i < th])[:20]))

        idx_uv = i_cube.mm > np.clip(np.sin(th_max) * i_cube.ll, 1, max(i_cube.ll))

        return idx_uv

    def is_applicable(self, i_cube):
        return isinstance(i_cube, sphcube.SphDataCube)


class Flag(object):

    def __init__(self, freqs, uu, vv, idx_uv, idx_uv_zero_weights, idx_freqs, idx_freqs_zero_weights):
        self.freqs = freqs
        self.uu = uu
        self.vv = vv
        self.idx_uv = idx_uv
        self.idx_freqs = idx_freqs
        self.idx_uv_zero_weights = idx_uv_zero_weights
        self.idx_freqs_zero_weights = idx_freqs_zero_weights

    def save(self, filename):
        with tables.open_file(filename, 'w') as h5_file:
            group = h5_file.create_group("/", 'flag', 'Flag metadata')
            h5_file.create_array(group, 'idx_uv', self.idx_uv, "Idx flag UV")
            h5_file.create_array(group, 'idx_uv_zero_weights', self.idx_uv_zero_weights, "Idx zero weights UV")
            h5_file.create_array(group, 'idx_freqs', self.idx_freqs, "Idx flag freqs")
            h5_file.create_array(group, 'idx_freqs_zero_weights', self.idx_freqs_zero_weights, "Idx zero weights freqs")
            h5_file.create_array(group, 'freqs', self.freqs, "Frequencies (Hz)")
            h5_file.create_array(group, 'uu', self.uu, "U (lambda)")
            h5_file.create_array(group, 'vv', self.vv, "V (lambda)")

    @staticmethod
    def load(filename):
        with tables.open_file(filename, 'r') as h5_file:
            idx_uv = h5_file.root.flag.idx_uv.read()
            idx_uv_zero_weights = h5_file.root.flag.idx_uv_zero_weights.read()
            idx_freqs = h5_file.root.flag.idx_freqs.read()
            idx_freqs_zero_weights = h5_file.root.flag.idx_freqs_zero_weights.read()
            freqs = h5_file.root.flag.freqs.read()
            uu = h5_file.root.flag.uu.read()
            vv = h5_file.root.flag.vv.read()

        return Flag(freqs, uu, vv, idx_uv, idx_uv_zero_weights, idx_freqs, idx_freqs_zero_weights)

    def apply(self, cube):
        assert np.allclose(cube.freqs, self.freqs)
        assert len(cube.ru) == len(self.uu)

        cube = cube.copy()
        cube.filter_uv_from_index(self.idx_uv)
        cube = cube.get_slice_from_idx(self.idx_freqs)

        if cube.weights is not None:
            cube.weights.data[self.idx_freqs_zero_weights] = 0
            cube.weights.data[:, self.idx_uv_zero_weights] = 0

        return cube


class FlaggerRunner(object):

    def __init__(self, verbose=True, min_weights=2):
        self.flaggers = []
        self.original_i_cube = None
        self.original_v_cube = None
        self.filtered_i_cube = None
        self.filtered_v_cube = None
        self.flag = None
        self.verbose = verbose
        self.min_weights = min_weights

    def add(self, flagger):
        self.flaggers.append(flagger)

    def run(self, i_cube, v_cube):
        i_cube_before_flagging = i_cube.copy()
        if self.min_weights is not None:
            i_cube.filter_min_weight(self.min_weights, verbose=self.verbose)
            v_cube.filter_min_weight(self.min_weights, verbose=self.verbose)
        self.original_i_cube = i_cube.copy()
        self.original_v_cube = v_cube.copy()
        for flagger in self.flaggers:
            if flagger.is_applicable(i_cube):
                i_cube, v_cube = flagger.do_flag(i_cube, v_cube, verbose=self.verbose)
        self.filtered_i_cube = i_cube
        self.filtered_v_cube = v_cube

        idx_freqs, idx_uv, _, _ = datacube.get_common_idx(i_cube_before_flagging, self.filtered_i_cube)

        if self.filtered_i_cube.weights is not None:
            idx_uv_zero_weights = (self.filtered_i_cube.weights.get().sum(axis=0) == 0)
            idx_freqs_zero_weights = (self.filtered_i_cube.weights.get().sum(axis=1) == 0)
        else:
            idx_uv_zero_weights = None
            idx_freqs_zero_weights = None

        if isinstance(i_cube_before_flagging, datacube.CartDataCube):
            self.flag = Flag(i_cube_before_flagging.freqs, i_cube_before_flagging.uu, i_cube_before_flagging.vv,
                             idx_uv, idx_uv_zero_weights, idx_freqs, idx_freqs_zero_weights)
        elif isinstance(i_cube_before_flagging, sphcube.SphDataCube):
            self.flag = Flag(i_cube_before_flagging.freqs, i_cube_before_flagging.ll, i_cube_before_flagging.mm,
                             idx_uv, idx_uv_zero_weights, idx_freqs, idx_freqs_zero_weights)
        else:
            raise ValueError('Cube is not of a supported format')

        return self.filtered_i_cube, self.filtered_v_cube

    def apply_last(self, cube):
        return self.flag.apply(cube)

    def plot(self, figsize=(10, 12), **fig_kargs):
        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(ncols=2, nrows=3, figsize=figsize, **fig_kargs)

        idx1, idx1_uv, _, _ = datacube.get_common_idx(self.original_i_cube, self.filtered_i_cube)
        freqs_idx_filtered = ~idx1
        uv_idx_filtered = ~idx1_uv

        if self.filtered_i_cube.weights is not None:
            freqs_idx_zero_w = self.filtered_i_cube.weights.data.sum(axis=1) == 0
            uv_idx_zero_w = self.filtered_i_cube.weights.data.sum(axis=0) == 0

        ax1.plot(self.original_i_cube.freqs * 1e-6, self.original_i_cube.data.var(axis=1),
                 c=psutil.lblue, label='I before')
        ax1.plot(self.original_i_cube.freqs * 1e-6, self.original_v_cube.data.var(axis=1),
                 c=psutil.lorange, label='V before')
        ax1.plot(self.filtered_i_cube.freqs * 1e-6, self.filtered_i_cube.data.var(axis=1),
                 c=psutil.dblue, label='I after')
        ax1.plot(self.filtered_v_cube.freqs * 1e-6, self.filtered_v_cube.data.var(axis=1),
                 c=psutil.dorange, label='V after')

        ax1.plot(self.original_i_cube.freqs[freqs_idx_filtered] * 1e-6,
                 self.original_v_cube.data.var(axis=1)[freqs_idx_filtered],
                 marker='x', ls='', c=psutil.black)

        if self.filtered_i_cube.weights is not None:
            ax1.plot(self.filtered_i_cube.freqs[freqs_idx_zero_w] * 1e-6,
                     self.filtered_i_cube.data.var(axis=1)[freqs_idx_zero_w],
                     marker='+', ls='', c=psutil.black)

        ax1.set_yscale('log')
        ax1.set_xlabel('Freqs [MHz]')
        ax1.set_ylabel('Variance [Unormalized]')
        ax1.legend()

        ax2.plot(self.original_i_cube.freqs * 1e-6, self.original_v_cube.make_diff_cube_interp().estimate_freqs_sefd(),
                 c=psutil.lorange, label='dV before')
        ax2.plot(self.original_i_cube.freqs * 1e-6, self.original_i_cube.make_diff_cube_interp().estimate_freqs_sefd(),
                 c=psutil.lblue, label='dI before')
        ax2.plot(self.filtered_v_cube.freqs * 1e-6, self.filtered_v_cube.make_diff_cube_interp().estimate_freqs_sefd(),
                 c=psutil.lorange, label='dV after')
        ax2.plot(self.filtered_i_cube.freqs * 1e-6, self.filtered_i_cube.make_diff_cube_interp().estimate_freqs_sefd(),
                 c=psutil.dblue, label='dI after')

        ax2.plot(self.original_i_cube.freqs[freqs_idx_filtered] * 1e-6,
                 self.original_v_cube.make_diff_cube_interp().estimate_freqs_sefd()[freqs_idx_filtered],
                 marker='x', ls='', c=psutil.black)

        ax2.set_yscale('log')
        ax2.set_xlabel('Freqs [MHz]')
        ax2.set_ylabel('SEFD [Unormalized]')
        ax2.legend()

        if isinstance(self.original_i_cube, datacube.CartDataCube):
            self.original_v_cube.weights.plot_uv(ax=ax3)
            ax3.set_title('Weights')
            self.original_v_cube.estimate_uv_sefd().plot_uv(ax=ax4)
            ax4.set_title('SEFD V')
            self.original_i_cube.make_diff_cube().estimate_uv_sefd().plot_uv(ax=ax5)
            ax5.set_title('SEFD d_nu I')
            self.original_v_cube.make_diff_cube().estimate_uv_sefd().plot_uv(ax=ax6)
            ax6.set_title('SEFD d_nu V')

            for ax in [ax3, ax4, ax5, ax6]:
                ax.scatter(self.original_i_cube.uu[uv_idx_filtered],
                           self.original_i_cube.vv[uv_idx_filtered], c=psutil.black, s=40, marker='x')
                if self.filtered_i_cube.weights is not None:
                    ax.scatter(self.filtered_i_cube.uu[uv_idx_zero_w],
                               self.filtered_i_cube.vv[uv_idx_zero_w], c=psutil.black, s=40, marker='+')
        elif isinstance(self.original_i_cube, sphcube.SphDataCube):
            self.original_i_cube.plot_lm(ax=ax3, action_fct=np.mean)
            ax3.set_title('Mean Stokes I')
            self.original_v_cube.plot_lm(ax=ax4, action_fct=np.var, norm=LogNorm())
            ax4.set_title('Var V')
            self.original_i_cube.make_diff_cube().plot_lm(ax=ax5, action_fct=np.var, norm=LogNorm())
            ax5.set_title('Var d_nu I')
            self.original_v_cube.make_diff_cube().plot_lm(ax=ax6, action_fct=np.var, norm=LogNorm())
            ax6.set_title('Var d_nu I')
            for ax in [ax3, ax4, ax5, ax6]:
                ax.scatter(self.original_i_cube.ll[uv_idx_filtered],
                           self.original_i_cube.mm[uv_idx_filtered], c=psutil.black, s=40, marker='x')

        else:
            raise ValueError('Cube is not of a supported format')

        fig.tight_layout()

        return fig

    @staticmethod
    def load(filename):
        config = configparser.RawConfigParser()
        config.read(filename)
        flagger_runner = FlaggerRunner()

        assert config.has_option('flagger', 'pipeline'), "Secton 'flagger' missing from %s" % filename

        for flagger_name in config.get('flagger', 'pipeline').split(','):
            flagger_name = flagger_name.strip()
            if len(flagger_name) > 0:
                items = dict(config.items(flagger_name))

                assert 'type' in items, "No type found for '%s'" % flagger_name
                assert items['type'] in globals(), "Type '%s' incorrect" % items['type']

                klass = globals()[items['type']]

                assert inspect.isclass(klass), "Type '%s' incorrect" % items['type']
                del items['type']
                items['name'] = flagger_name
                flagger = klass(**items)
                flagger_runner.add(flagger)

        return flagger_runner
