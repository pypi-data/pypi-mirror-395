# Class for dealing with spherical-harmonics data cubes
#
# Authors: F.Mertens


from __future__ import division
from __future__ import absolute_import

import copy
from collections import defaultdict

import numpy as np

import healpy as hp

import matplotlib.pyplot as plt

from scipy.signal import get_window
from scipy.interpolate import interp1d

from astropy.coordinates import ICRS

import tables

from . import psutil
from . import sphutil
from . import datacube


class SphMetaData(object):

    def __init__(self, metadata):
        self.data = defaultdict(list, metadata)

    def __add__(self, other):
        assert self.data['INT_TIME'] == other.data['INT_TIME']
        assert self.data['COORD_SYS'] == other.data['COORD_SYS']

        new = self.copy()
        for key in ['MJD_OBS', 'RADEC_OBS', 'TIME_OBS', 'WIN_FCT', 'WIN_FCT_FWHM', 'WEIGHTS']:
            new.data[key].extend(other.get(key))

        return new

    @property
    def nside(self):
        return self.get('NSIDE')

    @property
    def int_time(self):
        return self.get('INT_TIME')

    @property
    def total_time(self):
        return self.get('TOTAL_TIME')

    @property
    def freq_width(self):
        return self.get('FREQ_WIDT')

    @property
    def win_fct(self):
        return SphWindowFunction.from_meta(self)

    @staticmethod
    def new_obs(mjd_obs, radec_obs, time_obs, int_time, nside, win_fct, fwhm, freq_width, coord_sys='ICRS', weight=1):
        data = defaultdict(list)
        data['INT_TIME'] = int_time
        data['NSIDE'] = nside
        data['COORD_SYS'] = coord_sys
        data['FREQ_WIDT'] = freq_width
        data['ORIGIN'] = 'ps_eor v_%s' % datacube.__version__
        new = SphMetaData(data)
        new.add_obs(mjd_obs, radec_obs, time_obs, win_fct, fwhm, weight)

        return new

    def add_obs(self, mjd_obs, radec_obs, time_obs, win_fct, fwhm, weight=1):
        self.data['MJD_OBS'].append(mjd_obs)
        self.data['RADEC_OBS'].append(radec_obs)
        self.data['TIME_OBS'].append(time_obs)
        self.data['WIN_FCT'].append(win_fct)
        self.data['WIN_FCT_FWHM'].append(fwhm)
        self.data['WEIGHTS'].append(weight)

    def iter_obs(self, keys):
        for i in range(len(self.data['MJD_OBS'])):
            yield [self.data[key][i] for key in keys]

    def get(self, key):
        return self.data[key]

    def add_weight(self, weight):
        self.data['WEIGHTS'] = (weight * np.array(self.data['WEIGHTS'])).tolist()

    def items(self):
        return list(self.data.items())

    def copy(self):
        return SphMetaData(copy.deepcopy(self.data))


class NoMask(datacube.Mask):

    def __init__(self):
        datacube.Mask.__init__(self, [self])

    def generate(self, meta_data):
        return np.ones(hp.nside2npix(meta_data.get('NSIDE')))


class NoPrimaryBeam(datacube.BasePrimaryBeam, NoMask):

    def __init__(self):
        datacube.BasePrimaryBeam.__init__(self, [self])


class SphWindowFunction(datacube.Mask):

    def __init__(self, name, ra_dec, fwhm, weight=1, primary_beam=None):
        self.name = name
        self.ra_dec = ra_dec
        self.fwhm = fwhm
        self.weight = weight
        self.primary_beam = primary_beam
        datacube.Mask.__init__(self, [self])

    @staticmethod
    def from_meta(meta, primary_beam=None):
        win_fcts = []
        for win_fct, win_fct_fwhm, ra_dec, weight in meta.iter_obs(['WIN_FCT', 'WIN_FCT_FWHM', 'RADEC_OBS', 'WEIGHTS']):
            if win_fct is None:
                win_fcts.append(NoMask())
            else:
                name = datacube.WindowFunction.parse_winfct_str(win_fct.split('_')[0])
                win_fcts.append(SphWindowFunction(name, ra_dec, win_fct_fwhm, weight, primary_beam=primary_beam))
        return datacube.Mask(win_fcts)

    def generate_window(self, nside, pb_fwhm=None, oversample=2):
        thetas, phis = hp.pix2ang(nside, np.arange(hp.nside2npix(nside)))
        n = psutil.get_next_even(oversample * (np.pi / 2.) / hp.nside2resol(nside))
        yp = get_window(self.name, n)[n // 2:]
        xp = np.linspace(0, 0.5 * self.fwhm, len(yp))
        win_map = interp1d(xp, yp, fill_value=0, bounds_error=False)(thetas)
        if self.primary_beam is not None and pb_fwhm is not None:
            pb_map = psutil.get_beam(thetas, self.primary_beam.beam_type, pb_fwhm, n_sidelobe=None)
            win_map = win_map * pb_map

        ra, dec = self.ra_dec
        win_map = hp.Rotator(rot=(180 + ra, -dec + 90), inv=True).rotate_map_pixel(win_map)

        return self.weight * win_map

    def generate(self, meta_data, freq=None):
        if self.primary_beam is not None:
            pb_fwhm = self.primary_beam.get_fwhm(freq=freq)
        else:
            pb_fwhm = None
        return self.generate_window(meta_data.get('NSIDE'), pb_fwhm=pb_fwhm)


class SphDataCube(datacube.DataCube):

    def __init__(self, alm_cube, ll, mm, freqs, meta, cov_err=None, weights=None):
        self.ll = ll
        self.mm = mm
        self.ru = self.ll / (2 * np.pi)
        self.meta = meta

        datacube.DataCube.__init__(self, alm_cube, freqs, cov_err=cov_err, weights=weights)

    def get_unique_xy(self):
        return self.ll + 1e-6 * self.mm

    @staticmethod
    def from_cartcube(cube, nside, lmax, reproject_order='bilinear'):
        import reproject

        fwcs = cube.meta.wcs.copy()
        fwcs = fwcs.dropaxis(2)
        fwcs = fwcs.dropaxis(2)

        img_cube = cube.regrid().image().data.real
        hmaps = []
        pr = psutil.progress_report(img_cube.shape[0])
        for i, img in enumerate(img_cube):
            pr(i)
            hmaps.append(reproject.reproject_to_healpix((img, fwcs), ICRS(), nside=nside,
                                                        order=reproject_order)[0])
        hmaps = np.array(hmaps)
        hmaps[np.isnan(hmaps)] = 0

        alms = np.array([hp.map2alm(hmap, int(lmax)) for hmap in hmaps])
        ll, mm = sphutil.get_lm(int(lmax))

        meta = SphMetaData.new_obs(cube.meta.to_header()['MJD-OBS'], fwcs.wcs.crval, cube.meta.total_time,
                                   cube.meta.int_time, nside, cube.meta.get('PEWINFCT', 'boxcar'),
                                   cube.meta.theta_fov, cube.meta.freq_width)

        return SphDataCube(alms, ll, mm, cube.freqs, meta)

    def new_with_data(self, data, cov_err=None, weights=None, freqs=None):
        if freqs is None:
            freqs = self.freqs

        return SphDataCube(data, self.ll, self.mm, freqs, self.meta, cov_err=cov_err, weights=weights)

    def filter_outliers(self, outliers):
        self.freqs = self.freqs[~outliers]
        self.data = self.data[~outliers]

        if self.cov_err is not None:
            self.cov_err.filter_outliers(outliers)

    def filter_uv_from_index(self, idx_uv):
        datacube.DataCube.filter_uv_from_index(self, idx_uv)
        self.mm = self.mm[idx_uv]
        self.ll = self.ll[idx_uv]
        self.ru = self.ru[idx_uv]

    def filter_uvrange(self, umin, umax):
        idx_uv = (self.ru >= umin) & (self.ru <= umax)
        self.filter_uv_from_index(idx_uv)

    def filter_lm(self, lmin, lmax):
        idx_uv = (self.ll >= lmin) & (self.ll <= lmax)
        self.filter_uv_from_index(idx_uv)

    def filter_m_theta_max(self, theta_max):
        idx_uv = self.mm < np.clip(np.sin(theta_max) * self.ll, 1, max(self.ll))
        self.filter_uv_from_index(idx_uv)

    @staticmethod
    def load(filename):
        """Load alm from filename"""
        with tables.open_file(filename, 'r') as h5_file:
            alm_cube = h5_file.root.alm_cube.data.read()
            freqs = h5_file.root.alm_cube.freqs.read()
            ll = h5_file.root.alm_cube.ll.read()
            mm = h5_file.root.alm_cube.mm.read()

            attrs = h5_file.root.alm_cube.data.attrs
            meta = SphMetaData(dict([(k, psutil.safe_decode_bytes(attrs[k]))
                                     for k in attrs._f_list() if k[0].isupper()]))

            # Compat for dataset created before FREQ_WIDT
            if 'FREQ_WIDT' not in meta.data:
                meta.data = psutil.robust_freq_width(freqs)

            if 'cov_err' in h5_file.root:
                cov_err = datacube.ErrorCovariance.load_from_hd5(h5_file.root.cov_err)
            else:
                cov_err = None

        return SphDataCube(alm_cube, ll, mm, freqs, meta, cov_err=cov_err)

    def save(self, filename):
        """Save alm_cube to filename in h5 format"""
        with tables.open_file(filename, 'w') as h5_file:
            group = h5_file.create_group("/", 'alm_cube', 'Alm cube (n_freqs, n_modes')
            h5_file.create_array(group, 'data', self.data, "Spherical harmonics (K)")
            h5_file.create_array(group, 'freqs', self.freqs, "Frequencies (Hz)")
            h5_file.create_array(group, 'll', self.ll, "l mode")
            h5_file.create_array(group, 'mm', self.mm, "m mode")

            for key, value in self.meta.items():
                h5_file.root.alm_cube.data.attrs[key] = value

            if self.cov_err is not None:
                group = h5_file.create_group("/", 'cov_err', 'Covariance error')
                self.cov_err.save_to_hd5(h5_file, group)

    def plot_lm(self, fmhz='med', action_fct=None, ax=None, title=None, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        alm = self.data

        if action_fct is None:
            if fmhz == 'med':
                fmhz = self.freqs[0] + (self.freqs[-1] - self.freqs[0]) / 2.
            elif fmhz == 'first':
                fmhz = self.freqs[0]
            elif fmhz == 'first':
                fmhz = self.freqs[-1]

            i = np.argmin(abs(self.freqs - fmhz * 1e6))
            alm = alm[i]
        else:
            alm = action_fct(alm, axis=0)

        alm_map = sphutil.get_lm_map(alm, self.ll, self.mm)

        cbs = psutil.ColorbarSetting(psutil.ColorbarInnerPosition(location=2, height="80%", pad=1))

        extent = (min(self.ll), max(self.ll), min(self.mm), max(self.mm))

        im_mappable = ax.imshow(alm_map.real, extent=extent, aspect='auto', **kargs)
        cbs.add_colorbar(im_mappable, ax)

        ax.set_xlabel('l')
        ax.set_ylabel('m')

        if title is not None:
            ax.set_title(title)

    def regrid(self):
        # No regrid for sph cubes
        return self

    def image(self, mask_corrected=False, mask_correction_threshold=0.1):
        data = np.asarray(self.data, order='C')
        hmaps = np.array([sphutil.fast_alm2map(k, self.ll, self.mm, self.meta.nside) for k in data])

        if mask_corrected:
            mask = self.meta.win_fct.generate(self.meta)
            th = mask_correction_threshold
            hmaps[:, mask > th * mask.max()] = hmaps[:, mask > th * mask.max()] / mask[None, mask > th * mask.max()]
            hmaps[:, mask < th * mask.max()] = 0

        return SphImageCube(hmaps, self.freqs, self.meta)


class SphImageCube(datacube.ImageCube):

    def __init__(self, hmaps, freqs, meta):
        datacube.ImageCube.__init__(self, hmaps, freqs, meta)

    def apply_window_function(self, win_fct, add_to_meta=True):
        win_mask = win_fct.generate(self.meta)
        self.data = self.data * win_mask
        if add_to_meta:
            if self.meta.data['WIN_FCT'] == [None] * len(self.meta.data['WIN_FCT']):
                self.meta = SphMetaData.new_obs(0, win_fct.ra_dec, 0, self.meta.int_time, self.meta.nside,
                                                win_fct.name, win_fct.fwhm, self.meta.freq_width, weight=1)
            else:
                self.meta.add_obs(0, win_fct.ra_dec, 0, win_fct.name, win_fct.fwhm, weight=1)

    def ft(self, umin, umax):
        lmax = int(2 * np.pi * umax)
        alms = np.array([hp.map2alm(k, lmax) for k in self.data], order='C')
        ll, mm = sphutil.get_lm(lmax)

        cube = SphDataCube(alms, ll, mm, self.freqs, self.meta)
        cube.filter_uvrange(umin, umax)

        return cube

    def plot(self, fmhz='med', action_fct=None, dpar=None, dmer=None, title='',
             vmax=None, vmin=None, ax=None, auto_scale_quantiles=None, coord='CG', **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        d = self.data

        if action_fct is None:
            if fmhz == 'med':
                fmhz = self.freqs[0] + (self.freqs[-1] - self.freqs[0]) / 2.
            elif fmhz == 'first':
                fmhz = self.freqs[0]
            elif fmhz == 'first':
                fmhz = self.freqs[-1]

            i = np.argmin(abs(self.freqs - fmhz * 1e6))
            d = d[i]
        else:
            d = action_fct(d, axis=0)

        if vmin is not None:
            kargs['min'] = vmin
        if vmax is not None:
            kargs['max'] = vmax

        if auto_scale_quantiles is not None:
            kargs['min'] = np.quantile(d, auto_scale_quantiles[0])
            kargs['max'] = np.quantile(d, auto_scale_quantiles[1])

        plt.sca(ax)
        hp.mollview(d, hold=True, title=title, coord=coord, **kargs)
        hp.graticule(dpar=dpar, dmer=dmer, coord='C', verbose=False)
        hp.graticule(dpar=dpar, dmer=dmer, coord='G', alpha=0.5, c=psutil.blue, verbose=False)

    def plot_slice(self, ax=None, min_dec=-20, npix=1000):
        if ax is None:
            fig, ax = plt.subplots()

        ra, dec = np.radians(np.array(self.meta.data['RADEC_OBS']).mean(axis=0))
        if ra < 0:
            ra = 2 * np.pi + ra

        decs = np.radians(np.linspace(min_dec, 90, npix))

        ras = ra * np.ones_like(decs)
        thetas, phis = sphutil.radec2thetaphi(ras, decs)
        idx1 = hp.ang2pix(128, thetas, phis)

        ras = (ra + np.pi) * np.ones_like(decs)
        thetas, phis = sphutil.radec2thetaphi(ras, decs)
        idx2 = hp.ang2pix(128, thetas, phis)[::-1]

        extent = [min_dec, 180 - min_dec, self.freqs[0] * 1e-6, self.freqs[-1] * 1e-6]

        im = ax.imshow(np.hstack([self.data[:, idx1], self.data[:, idx2]]), aspect='auto', extent=extent)
        ax.axvline(np.degrees(dec), c=psutil.black, ls='--')
        ax.set_ylabel('Freqs (MHz)')
        ax.set_xlabel('DEC (RA = %.1f deg) [deg]' % (np.degrees(ra)))

        cbs = psutil.ColorbarSetting(psutil.ColorbarOutterPosition(width='3%'))
        cbs.add_colorbar(im, ax)

    def copy(self):
        return SphImageCube(self.data.copy(), self.freqs, self.meta.copy())


class SphDataCubeCombiner(object):

    def __init__(self):
        self.data = None
        self.freqs = None
        self.weights = None
        self.ll = None
        self.mm = None
        self.meta = None

    def get_inter_idx(self, freqs1, freqs2):
        f1 = datacube._fmhz(freqs1)
        f2 = datacube._fmhz(freqs2)
        freqs = np.intersect1d(f1, f2)
        return np.in1d(f1, freqs), np.in1d(f2, freqs)

    def add(self, cube, weight):
        if self.data is None:
            self.data = weight * cube.data
            self.freqs = cube.freqs.copy()
            self.weights = [weight]
            self.meta = cube.meta.copy()
            self.meta.add_weight(weight)
            self.ll = cube.ll.copy()
            self.mm = cube.mm.copy()
        else:
            idx1, idx2 = self.get_inter_idx(self.freqs, cube.freqs)
            self.data = self.data[idx1]
            self.freqs = self.freqs[idx1]
            self.data += weight * cube.data[idx2]
            self.weights.append(weight)

            cube_meta = cube.meta.copy()
            cube_meta.add_weight(weight)
            self.meta = self.meta + cube_meta

    def get(self):
        # normalize so the sum of weights is one
        sum_weight = float(np.sum(self.weights))
        data = self.data.copy() / sum_weight
        meta = self.meta.copy()
        meta.add_weight(1 / sum_weight)

        return SphDataCube(data, self.ll, self.mm, self.freqs.copy(), meta)
