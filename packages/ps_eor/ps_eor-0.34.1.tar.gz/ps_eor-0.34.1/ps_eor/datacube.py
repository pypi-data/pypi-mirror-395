# Class for data cube handling
#
# Authors: F.Mertens

import re
import tables
import warnings

import numpy as np
import scipy.interpolate
from scipy.stats import binned_statistic
from scipy.signal import get_window

import matplotlib.pyplot as plt

import astropy.io.fits as pf
import astropy.wcs as pywcs
import astropy.constants as const

from . import psutil
from . import __version__


def _fmhz(freqs, precision=3):
    return np.round(freqs * 1e-6, precision)


def get_common_idx(cube1, cube2):
    freqs = np.intersect1d(_fmhz(cube1.freqs), _fmhz(cube2.freqs))
    idx1 = np.in1d(_fmhz(cube1.freqs), freqs)
    idx2 = np.in1d(_fmhz(cube2.freqs), freqs)

    a = cube1.get_unique_xy()
    b = cube2.get_unique_xy()
    z = np.intersect1d(a, b)
    idx1_uv = np.in1d(a, z)
    idx2_uv = np.in1d(b, z)

    return idx1, idx1_uv, idx2, idx2_uv


def get_common_cube(cube1, cube2, only_frequency=False):
    idx1, idx1_uv, idx2, idx2_uv = get_common_idx(cube1, cube2)

    c1 = cube1.get_slice_from_idx(idx1)
    c2 = cube2.get_slice_from_idx(idx2)

    if not only_frequency:
        c1.filter_uv_from_index(idx1_uv)
        c2.filter_uv_from_index(idx2_uv)

    return c1, c2


def concatenate_datacubes(cubes):
    assert len(cubes) > 1
    assert np.alltrue([isinstance(cube, DataCube) for cube in cubes])
    assert np.alltrue([np.allclose(cubes[0].uu, cube.uu) for cube in cubes[1:]])
    assert np.alltrue([np.allclose(cubes[0].vv, cube.vv) for cube in cubes[1:]])

    data = np.concatenate([c.data for c in cubes])
    weights_data = np.concatenate([c.weights.data for c in cubes])
    freqs = np.concatenate([c.freqs for c in cubes])
    weights = CartWeightCube(weights_data, cubes[0].uu, cubes[0].vv, freqs, cubes[0].meta)

    return CartDataCube(data, cubes[0].uu, cubes[0].vv, freqs, cubes[0].meta, weights=weights)


class Mask(object):

    def __init__(self, masks=[]):
        self.masks = masks

    def __mul__(self, other):
        return MaskProd(self, other)

    def __add__(self, other):
        return Mask(self.masks + other.masks)

    def generate(self, meta_data):
        return np.sum([m.generate(meta_data) for m in self.masks], axis=0)

    def get_power(self, meta_data):
        return (self.generate(meta_data) ** 2).mean()

    def get_area(self, meta_data, normalize=False):
        mask = self.generate(meta_data)
        area = mask.mean()
        if normalize:
            area = area / float(mask.max())
        return area


class MaskProd(Mask):

    def __init__(self, m1, m2):
        self.m1s = m1.masks
        self.m2s = m2.masks
        if len(self.m1s) == 1 and len(self.m2s):
            self.m1s = [self.m1s[0]] * len(self.m2s)
        elif len(self.m2s) == 1 and len(self.m1s):
            self.m2s = [self.m2s[0]] * len(self.m1s)

    def __add__(self):
        return NotImplementedError()

    def __mul__(self):
        return NotImplementedError()

    def generate(self, meta_data):
        if len(self.m1s) == len(self.m2s):
            return np.sum([m1.generate(meta_data) * m2.generate(meta_data)
                           for m1, m2 in zip(self.m1s, self.m2s)], axis=0)
        elif len(self.m1s) == 1 and len(self.m2s) > 1:
            m1_map = self.m1s[0].generate(meta_data)
            return np.sum([m1_map * m2.generate(meta_data) for m2 in self.m2s], axis=0)
        elif len(self.m2s) == 1 and len(self.m1s) > 1:
            m2_map = self.m2s[0].generate(meta_data)
            return np.sum([m2_map * m1.generate(meta_data) for m1 in self.m1s], axis=0)
        else:
            return NotImplementedError()


class WindowFunction(Mask):

    def __init__(self, name, circular=True):
        self.name = name
        self.circular = circular
        Mask.__init__(self, [self])

    def __str__(self):
        return 'WindowFunction(%s, circular=%s)' % (self.name, self.circular)

    @staticmethod
    def parse_winfct_str(s):
        s = s.strip()
        if ',' in s:
            s, o = s.strip('() ').split(',')
            return (re.sub(r'\W+', '', s), float(o))
        else:
            return s

    @staticmethod
    def from_meta(image_meta):
        if 'PEWINFCT' in image_meta:
            s = image_meta.get('PEWINFCT')
            n, c = s.split('_')
            name = WindowFunction.parse_winfct_str(n)
            circular = psutil.str2bool(c)
            return WindowFunction(name, circular)
        else:
            return WindowFunction('boxcar')

    def to_meta(self, image_meta):
        image_meta.set('PEWINFCT', '%s_%s' % (self.name, self.circular))

    def generate_window(self, nx):
        return psutil.generate_2d_window(self.name, nx, circular=self.circular)

    def generate(self, meta_data):
        return self.generate_window(meta_data.shape[0])


class BasePrimaryBeam(Mask):

    name = 'pb'

    def __init__(self, masks, freq=None):
        self.freq = freq
        Mask.__init__(self, masks)

    def set_freq(self, freq):
        self.freq = freq

    def get_freq(self, freq=None):
        if freq is not None:
            return freq
        return self.freq


class PrimaryBeam(BasePrimaryBeam):

    def __init__(self, antenna_diameter, alpha_tapering, beam_type, freq=None):
        self.antenna_diameter = antenna_diameter
        self.alpha_tapering = alpha_tapering
        self.beam_type = beam_type
        BasePrimaryBeam.__init__(self, [self], freq=freq)

    def __str__(self):
        return 'PrimaryBeam(%sm, alpha=%s, %s)' % (self.antenna_diameter, self.alpha_tapering, self.beam_type)

    @staticmethod
    def from_name(name):
        if name.startswith('ant_'):
            _, diameter, alpha, beam_type = name.split('_')
            return PrimaryBeam(float(diameter), float(alpha), beam_type)

        klasses = BasePrimaryBeam.__subclasses__()
        [klasses.extend(k.__subclasses__()) for k in klasses[:]]

        for klass in klasses:
            if hasattr(klass, 'name') and klass.name == name:
                return klass()

        raise ValueError('No primary beam with name: %s' % name)

    def get_fwhm(self, freq=None):
        freq = self.get_freq(freq)
        assert freq is not None
        lamb = const.c.value / freq
        return self.alpha_tapering * lamb / self.antenna_diameter

    def generate_beam(self, fwhm, res, shape):
        return psutil.get_beam_cart(res, tuple(shape), self.beam_type, fwhm, n_sidelobe=None)

    def generate(self, meta_data, freq=None):
        fwhm = self.get_fwhm(freq=freq)
        return self.generate_beam(fwhm, meta_data.res, meta_data.shape)


class LofarHBAPrimaryBeam(PrimaryBeam):

    name = 'lofar_hba'

    def __init__(self):
        PrimaryBeam.__init__(self, 30.75, 1.25, 'gaussian')


class AartfaacA12HBAPrimaryBeam(PrimaryBeam):

    name = 'a12_hba'

    def __init__(self):
        PrimaryBeam.__init__(self, 5, 1.02, 'gaussian')


class LofarLBAInnerPrimaryBeam(PrimaryBeam):

    name = 'lofar_lba_inner'

    def __init__(self):
        PrimaryBeam.__init__(self, 32.25, 1.1, 'gaussian')


class LofarLBAOuterPrimaryBeam(PrimaryBeam):

    name = 'lofar_lba_outer'

    def __init__(self):
        PrimaryBeam.__init__(self, 81.34, 1.1, 'gaussian')


class SkaLowPrimaryBeam(PrimaryBeam):

    name = 'ska_low'

    def __init__(self):
        PrimaryBeam.__init__(self, 38, 1.0335, 'bessel')


class NenuFARPrimaryBeam(PrimaryBeam):

    name = 'nenufar'

    def __init__(self):
        PrimaryBeam.__init__(self, 25, 1.02, 'gaussian')


class NoPrimaryBeam(BasePrimaryBeam):

    name = 'no_pb'

    def __init__(self):
        BasePrimaryBeam.__init__(self, [self])

    def generate(self, meta_data, freq=None):
        return np.ones(meta_data.shape)


class ErrorCovariance(object):

    def __init__(self, freqs, freq_cov_err, data_scale):
        """Error covariance matrix for a data cube

        Args:
            freqs (n_freqs): Frequencies in Hz
            freq_cov_err (n_freqs, n_freqs): Error covariance
            data_scale (n_data): Scaling factor for each data points
        """
        self.freqs = freqs
        self.freq_cov_err = freq_cov_err
        self.data_scale = data_scale

    def __hash__(self):
        return hash(tuple(np.concatenate((self.freq_cov_err.flatten(), self.data_scale.flatten()))))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __add__(self, other):
        assert np.allclose(self.freqs, other.freqs)
        data_scale = np.sqrt(self.data_scale ** 2 + other.data_scale ** 2)

        return ErrorCovariance(self.freqs, self.freq_cov_err + other.freq_cov_err, data_scale)

    def __sub__(self, other):
        assert np.allclose(self.freqs, other.freqs)
        data_scale = np.sqrt(self.data_scale ** 2 + other.data_scale ** 2)

        return ErrorCovariance(self.freqs, self.freq_cov_err - other.freq_cov_err, data_scale)

    def __mul__(self, other):
        assert psutil.is_number(other)
        return ErrorCovariance(self.freqs, self.freq_cov_err, other * self.data_scale)

    def __rmul__(self, other):
        return self.__mul__(other)

    def get_slice_from_idx(self, idx_freqs):
        # print idx_freqs.shape
        # print idx_freqs.shape
        # print 'get_slice', self.freq_cov_err.shape, self.freq_cov_err[idx_freqs, idx_freqs].shape
        return ErrorCovariance(self.freqs[idx_freqs], self.freq_cov_err[idx_freqs][:, idx_freqs], self.data_scale)

    def get_slice(self, freq_start, freq_end):
        ''' Return an ErrorCovariance for the given frequency slice'''
        idx_freqs = psutil.get_freq_slice(self.freqs, freq_start, freq_end)

        return self.get_slice_from_idx(idx_freqs)

    def get_sample(self):
        ''' Get a random sample (n_freqs, n_data)'''
        n_freqs = self.freq_cov_err.shape[0]
        n_modes = len(self.data_scale)
        err_r = np.random.multivariate_normal(np.zeros(n_freqs), self.freq_cov_err, n_modes).T * self.data_scale.real
        err_i = np.random.multivariate_normal(np.zeros(n_freqs), self.freq_cov_err, n_modes).T * self.data_scale.imag
        return err_r + 1j * err_i

    def get_delay_cov(self, M, dx=None, empirical=True):
        if empirical:
            err = np.random.multivariate_normal(np.zeros(len(self.freqs)), self.freq_cov_err, 1000).T
            d_err = np.var(psutil.nudft(self.freqs, err, M, dx=dx)[1], axis=1)
        else:
            d_err = np.diag(abs(psutil.lssa_cov(self.freqs * 1e-6, self.freq_cov_err, M, dx=dx)))

        return d_err[:, None] * (self.data_scale.real[None, :]) ** 2
        # return np.repeat(d_err[:, None] * self.data_scale.real.mean() ** 2, len(self.data_scale), axis=1)

    @staticmethod
    def load_from_hd5(h5_group):
        freqs = h5_group.freqs.read()
        freq_cov_err = h5_group.freq_cov_err.read()
        data_scale = h5_group.data_scale.read()

        return ErrorCovariance(freqs, freq_cov_err, data_scale)

    def save_to_hd5(self, h5_file, group):
        h5_file.create_array(group, 'freqs', self.freqs, "Frequencies (Hz)")
        h5_file.create_array(group, 'freq_cov_err', self.freq_cov_err, "Freq cov error")
        h5_file.create_array(group, 'data_scale', self.data_scale, "Data scale")

    def filter_outliers(self, outliers):
        self.freqs = self.freqs[~outliers]
        self.freq_cov_err = self.freq_cov_err[~outliers][:, ~outliers]

    def copy(self):
        return ErrorCovariance(self.freqs, self.freq_cov_err.copy(), self.data_scale.copy())


class ImageMetaData(object):

    allowed_keys = ['BMAJ', 'BMIN', 'BPA', 'WSCNORMF', 'WEIGHTS', 'NIGHTS', 'ORIGIN']

    def __init__(self, wcs, shape, **kargs):
        """Container for image meta-data

        Args:
            wcs (WCS): The wcs of the image
            shape (int, int): Shape of the image
            **kargs: Additional keywords to store
        """
        self.wcs = wcs
        self.shape = shape
        self.kargs = kargs

    def __str__(self):
        args = (np.degrees(self.res) * 60., self.shape, np.degrees(self.theta_fov))
        return 'Meta(res=%.3f arcmin, shape=%s, fov=%.2f deg)' % args

    def __contains__(self, name):
        return name in self.kargs

    def set(self, name, value):
        """Add a keyword to this container """
        self.kargs[name] = value

    def get(self, name, default=None):
        return self.kargs.get(name, default)

    def remove(self, name):
        if name in self:
            del self.kargs[name]

    def update(self, d):
        self.kargs.update(d)

    @property
    def res(self):
        return abs(np.radians(self.wcs.wcs.cdelt[0]))

    @property
    def theta_fov(self):
        return self.shape[0] * self.res

    @property
    def total_time(self):
        return self.get('PETOTTIM', 1)

    @property
    def int_time(self):
        return self.get('PEINTTIM', 1)

    @property
    def freq_width(self):
        return abs(self.wcs.wcs.cdelt[2])

    @property
    def chan_width(self):
        return abs(self.get('PECHWIDT', self.wcs.wcs.cdelt[2]))

    @property
    def obs_mjd(self):
        return self.wcs.wcs.mjdobs

    @property
    def ra_dec_center_deg(self):
        return self.wcs.wcs.crval[:2]

    @property
    def win_fct(self):
        return WindowFunction.from_meta(self)

    @property
    def win_fct_power(self):
        return WindowFunction.from_meta(self).get_power(self)

    @property
    def win_fct_area(self):
        return WindowFunction.from_meta(self).get_area(self)

    def slice(self, x_s, x_e, y_s, y_e):
        """Trim the image <=> img[x_s:x_e, y_s:y_e]"""
        s = [slice(None)] * (self.wcs.naxis - 2) + [slice(x_s, x_e), slice(y_s, y_e)]
        self.wcs = self.wcs.slice(s)
        self.shape = (x_e - x_s, y_e - y_s)

    def average_freqs(self, n_freqs):
        self.wcs.wcs.cdelt[2] = n_freqs * self.wcs.wcs.cdelt[2]

    def items(self, add_origin=False):
        """Returns the meta data as a (key, value) list"""
        header = dict(self.to_header(add_origin=add_origin))
        header.update({'shape': self.shape})
        return list(header.items())

    def to_header(self, add_origin=False):
        '''Return the meta data as an FITS header '''
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            header = self.wcs.to_header()
            header.update(self.kargs)

        if add_origin:
            header['ORIGIN'] = 'ps_eor v_%s' % __version__

        return header

    @staticmethod
    def from_res(res, shape, **kargs):
        '''Create a minimal ImageMetaData using res and shape alone'''
        wcs = pywcs.WCS(naxis=4)
        wcs.wcs.crpix = np.concatenate((np.array(shape) // 2, np.array([1, 1])))
        wcs.wcs.crval = [0, 0, 1, 1]
        wcs.wcs.ctype = ['RA---SIN', 'DEC--SIN', 'FREQ', 'STOKES']
        wcs.wcs.cdelt = [-np.degrees(res), np.degrees(res), 1, 1]
        wcs.wcs.cunit = ['deg', 'deg', 'Hz', '']
        wcs._naxis = [shape[0], shape[1], 1, 1]

        meta = ImageMetaData(wcs, shape)

        for key, value in kargs.items():
            if key in ImageMetaData.allowed_keys or key.startswith('PE') or key.startswith('WSC'):
                meta.set(key, value)

        return meta

    @staticmethod
    def from_header(header, shape):
        '''Create an ImageMetaData from an image FITS header'''
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            wcs = pywcs.WCS(header)

        header['NAXIS1'] = shape[0]
        header['NAXIS2'] = shape[1]
        for i in range(3, wcs.naxis + 1):
            header['NAXIS%i' % i] = 1

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            wcs = pywcs.WCS(header)

        meta = ImageMetaData(wcs, shape)
        for key in header.keys():
            if key in ImageMetaData.allowed_keys or key.startswith('PE') or key.startswith('WSC'):
                meta.set(key, header[key])

        return meta

    def copy(self):
        return ImageMetaData(self.wcs.copy(), list(self.shape), **self.kargs)


class ImageCube(object):

    def __init__(self, image_cube, freqs, meta):
        self.data = image_cube.real
        self.freqs = freqs
        self.meta = meta

    def get_slice(self, freq_start, freq_end):
        ''' Return a CartDataCube for the given frequency slice'''
        freq_slice = psutil.get_freq_slice(self.freqs, freq_start, freq_end)

        return CartImageCube(self.data[freq_slice], self.freqs[freq_slice], self.meta.copy())

    def get_freq(self, freq):
        i = np.nonzero(self.freqs >= freq)[0][0]

        return CartImageCube(self.data[i:i + 1], self.freqs[i:i + 1], self.meta.copy())


class CartImageCube(ImageCube):

    def __init__(self, image_cube, freqs, meta):
        """Image cube

        Args:
            image_cube (n_freqs, nx, ny): image cube array
            freqs (n_freqs): Frequencies (in Hz)
            res (float): Resolution (in radians)
        """
        ImageCube.__init__(self, image_cube, freqs, meta)

    def trim(self, new_theta_fov):
        """Trim the image INPLACE!

        Args:
            new_theta_fov (float): new FoV in radians
        """
        n = new_theta_fov / self.meta.res
        nx, ny = self.meta.shape
        i = int((nx - n) / 2.)
        if i > 0:
            self.data = self.data[:, i:nx - i, i:ny - i]
            self.meta.slice(i, nx - i, i, ny - i)

    def apply_window_function(self, win_fct, add_to_meta=True):
        win_mask = win_fct.generate(self.meta)
        self.data = self.data * win_mask
        if add_to_meta:
            win_fct.to_meta(self.meta)

    def ft(self, umin, umax):
        """Fourier transform image cube and return a CartDataCube.

        Args:
            umin (float): Min U in wavelength
            umax (float): Max U in wavelength

        Returns:
            CartDataCube: a new visibility cube.
        """
        uu, vv, ft_cube = psutil.ft_cart_cube(self.data, self.meta.res, umin, umax)

        return CartDataCube(ft_cube, uu, vv, self.freqs, self.meta.copy())

    def save_to_fits(self, fname, overwrite=True):
        """Save the image as a FITS files"""
        hdu = pf.PrimaryHDU(self.data[None].real)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            hdu.header.update(self.meta.to_header(add_origin=True))

        hdu.header["BUNIT"] = "K"
        hdu.header["BTYPE"] = "Intensity"

        hdu.header["CRVAL3"] = self.freqs[0]
        hdu.header["CDELT3"] = self.meta.freq_width

        hdu.writeto(fname, overwrite=overwrite)

    def plot(self, fmhz='med', action_fct=None, theta_lines=[], ax=None, title=None,
             auto_scale_quantiles=None, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        d = self.data

        if action_fct is None:
            if fmhz == 'med':
                fmhz = (self.freqs[0] + (self.freqs[-1] - self.freqs[0]) / 2.) * 1e-6
            elif fmhz == 'first':
                fmhz = self.freqs[0] * 1e-6
            elif fmhz == 'last':
                fmhz = self.freqs[-1] * 1e-6

            i = np.argmin(abs(self.freqs - fmhz * 1e6))
            d = d[i]
        else:
            d = action_fct(d, axis=0)

        theta_max = np.clip(0.5 * self.meta.theta_fov, 0, 1)
        show_degrees = theta_max < 0.4

        if auto_scale_quantiles is not None:
            kargs['vmin'] = np.quantile(d, auto_scale_quantiles[0])
            kargs['vmax'] = np.quantile(d, auto_scale_quantiles[1])

        psutil.plot_cart_map(d, theta_max, ax=ax, title=title, theta_lines=theta_lines,
                             show_degrees=show_degrees, **kargs)

    def plot_slice(self, ax=None, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        islice = self.data[:, :, self.meta.shape[0] // 2]

        cbs = psutil.ColorbarSetting(psutil.ColorbarOutterPosition(width='3%'))
        theta_max = np.clip(0.5 * self.meta.theta_fov, 0, 1)
        show_degrees = theta_max < 0.4
        if show_degrees:
            theta_max = np.degrees(theta_max)

        extent = np.array([-theta_max, theta_max, min(self.freqs) * 1e-6, max(self.freqs) * 1e-6])
        im_mappable = ax.imshow(islice.real, extent=extent, aspect='auto', **kargs)

        cbs.add_colorbar(im_mappable, ax)
        ax.set_ylabel('Freqs (MHz)')

        if show_degrees:
            ax.set_xlabel('m (l = 0) [deg]')
        else:
            ax.set_xlabel('m (l = 0)')

    def copy(self):
        return CartImageCube(self.data.copy(), self.freqs, self.meta.copy())


class GriddedCartDataCube(object):

    def __init__(self, g_vis, g_uu, g_vv, freqs, meta):
        """Gridded visibilities cube

        Args:
            g_vis (n_freqs, n_u, n_v): gridded visibilities cube array
            g_uu (n_u, n_v): U in lambda
            g_vv (n_u, n_v): V in lambda
            freqs (n_freqs): Frequencies in Hz
            res (float): Resolution in radians
        """
        self.data = g_vis
        self.g_uu = g_uu
        self.g_vv = g_vv
        self.freqs = freqs
        self.meta = meta

    def image(self, res=None, low_memory=False):
        du = abs(self.g_uu[0, 1] - self.g_uu[0, 0])
        s = None
        meta = self.meta.copy()
        data = self.data

        if res is not None:
            nu = int(1 / res / du)
            s = (nu, nu)
            meta = ImageMetaData.from_res(res, s, **meta.kargs)
            data = np.array([psutil.resize(k, s) for k in data])

        ft_fct = lambda data, axes: psutil.vis_to_img(data, axes=axes)
        image_cube = ft_fct(data, (1, 2))

        return CartImageCube(image_cube, self.freqs, meta)


class DataCubeCombiner(object):

    def __init__(self, umin, umax, weighting_mode='uv', inhomogeneous=False, w_square=False):
        self.cube = None
        self.weighting_mode = weighting_mode
        self.total_weights = None
        self.total_weights_psf = None
        self.total_time = 0
        self.umin = umin
        self.umax = umax
        self.inhomogeneous = inhomogeneous
        self.w_square = w_square
        self.night_ids = []
        self.freqs_n_nights = []

    def _get_weights(self, cube, with_uv_scale=True):
        if self.weighting_mode == 'uv':
            w = np.median(cube.weights.get(with_uv_scale=with_uv_scale), axis=0)
        elif self.weighting_mode == 'full':
            w = cube.weights.get(with_uv_scale=with_uv_scale)
        elif self.weighting_mode == 'global':
            w = np.median(cube.weights.get(with_uv_scale=with_uv_scale))
        elif self.weighting_mode == 'none':
            w = 1
        else:
            assert False, "'%s' incorrect" % self.weighting_mode

        if self.w_square:
            w = w ** 2

        return np.atleast_2d(w)

    def _add(self, a, b, idx1_d1, idx1_d2):
        a_1 = a[idx1_d1]
        a_1[:, idx1_d2] = a_1[:, idx1_d2] + b
        a[idx1_d1] = a_1

        return a

    def add(self, cube, night_id):
        self.night_ids.append(night_id)

        if self.cube is None:
            if self.inhomogeneous:
                cube = cube.make_full_cube(self.umin, self.umax)

            weights = self._get_weights(cube)
            self.cube = cube.new_with_data(weights * cube.data)

            self.total_weights = weights
            self.total_weights_psf = cube.weights.get(with_uv_scale=False)
            self.total_time = self.cube.meta.total_time
            self.freqs_n_nights = np.ones(len(self.cube.freqs))
        else:
            idx1, idx1_uv, idx2, idx2_uv = get_common_idx(self.cube, cube)
            cube = cube.get_slice_from_idx(idx2)
            cube.filter_uv_from_index(idx2_uv)
            weights = self._get_weights(cube)

            if np.squeeze(weights).ndim == 2:
                idx1_w = idx1
            else:
                idx1_w = slice(None)
            if np.squeeze(weights).ndim >= 1:
                idx1_w_uv = idx1_uv
            else:
                idx1_w_uv = slice(None)

            if not self.inhomogeneous:
                self.cube = self.cube.get_slice_from_idx(idx1)
                self.cube.filter_uv_from_index(idx1_uv)

                self.cube.data = self.cube.data + weights * cube.data
                self.cube.weights = self.cube.weights + cube.weights
                self.total_weights_psf = self.total_weights_psf[idx1][:, idx1_uv] \
                    + cube.weights.get(with_uv_scale=False)

                self.total_weights = self.total_weights[idx1_w][:, idx1_w_uv] + weights
                self.freqs_n_nights = self.freqs_n_nights[idx1] + 1
            else:
                self.cube.data = self._add(self.cube.data, weights * cube.data, idx1, idx1_uv)
                self.cube.weights.data = self._add(self.cube.weights.data, cube.weights.data, idx1, idx1_uv)
                self.total_weights_psf = self._add(
                    self.total_weights_psf, cube.weights.get(with_uv_scale=False), idx1, idx1_uv)

                self.total_weights = self._add(self.total_weights, weights, idx1_w, idx1_w_uv)
                self.freqs_n_nights[idx1] += 1

            self.total_time += cube.meta.total_time

    def get(self, min_n_nights=None):
        if self.cube is None:
            return self.cube

        cube = self.cube.new_with_data(np.divide(self.cube.data, self.total_weights,
                                                 where=self.total_weights != 0), weights=self.cube.weights)
        cube.meta.set('PETOTTIM', self.total_time)
        cube.weights.meta.set('PETOTTIM', self.total_time)
        cube.meta.set('NIGHTS', ','.join(self.night_ids))
        cube.meta.set('PECMODE', self.weighting_mode)
        cube.meta.set('PECHOMO', not self.inhomogeneous)

        tw_psf_m = self.total_weights_psf.mean(axis=0)
        uv_scale = abs(np.divide(cube.weights.data.mean(axis=0), tw_psf_m, where=tw_psf_m != 0))
        cube.weights.uv_scale = uv_scale[None, :]
        cube.weights.data = self.total_weights_psf
        cube.weights.freqs_n_nights = self.freqs_n_nights

        if min_n_nights is not None:
            print('Filter:', cube.freqs[self.freqs_n_nights < min_n_nights])
            cube.filter_outliers(self.freqs_n_nights < min_n_nights)

        idx_zero = cube.weights.data.mean(axis=1) != 0
        cube = cube.get_slice_from_idx(idx_zero)

        return cube


class DataCube(object):

    def __init__(self, data, freqs, cov_err=None, weights=None):
        self.freqs = freqs
        self.data = data
        self.cov_err = cov_err
        self.weights = weights

    def __add_sub__(self, other, sub=False):
        if not np.allclose(self.freqs, other.freqs):
            raise TypeError('The two DataCube must have the same frequencies channels')

        if sub:
            cov_err = psutil.safe_diff(self.cov_err, other.cov_err)
            weights = psutil.safe_sum(self.weights, other.weights)
            return self.new_with_data(self.data - other.data, cov_err, weights)

        cov_err = psutil.safe_sum(self.cov_err, other.cov_err)
        weights = psutil.safe_sum(self.weights, other.weights)
        return self.new_with_data(self.data + other.data, cov_err, weights)

    def __sub__(self, other):
        return self.__add_sub__(other, True)

    def __add__(self, other):
        return self.__add_sub__(other, False)

    def __mul__(self, other):
        assert psutil.is_number(other)

        cov_err = None
        if self.cov_err is not None:
            cov_err = other * self.cov_err

        weights = None
        if self.weights is not None:
            weights = other * self.weights

        return self.new_with_data(other * self.data, cov_err, weights)

    def __rmul__(self, other):
        return self.__mul__(other)

    def get_unique_xy(self):
        raise NotImplementedError()

    def set_weights(self, weights_cube):
        if weights_cube is None:
            self.weights = None
        else:
            self.weights = weights_cube.copy()

    def new_with_data(self, data, cov_err=None, weights=None, freqs=None):
        raise NotImplementedError()

    def get_slice_from_idx(self, idx_freqs):
        cov_err = None
        if self.cov_err is not None:
            cov_err = self.cov_err.get_slice_from_idx(idx_freqs)

        weights = None
        if self.weights is not None:
            weights = self.weights.get_slice_from_idx(idx_freqs)

        return self.new_with_data(self.data[idx_freqs], cov_err=cov_err, weights=weights, freqs=self.freqs[idx_freqs])

    def get_slice(self, freq_start, freq_end):
        ''' Return a CartDataCube for the given frequency slice'''
        idx_freqs = psutil.get_freq_slice(self.freqs, freq_start, freq_end)

        return self.get_slice_from_idx(idx_freqs)

    def get_freq(self, freq):
        i = np.nonzero(self.freqs >= freq)[0][0]

        return self.get_slice_from_idx(slice(i, i + 1))

    def filter_uv_from_index(self, idx_uv):
        self.data = self.data[:, idx_uv]
        if self.cov_err is not None:
            self.cov_err.data_scale = self.cov_err.data_scale[idx_uv].copy()
        if self.weights is not None:
            self.weights.filter_uv_from_index(idx_uv)

    def make_diff_cube(self):
        data = np.sqrt(0.5) * np.diff(self.data, axis=0)

        weights = None
        if self.weights is not None:
            weights = self.weights.new_with_data(self.weights.data[:-1], freqs=self.freqs[:-1])

        return self.new_with_data(data, weights=weights, freqs=self.freqs[:-1])

    def make_diff_cube_interp(self):
        data = np.sqrt(0.5) * np.diff(self.data, axis=0)
        data = np.vstack([data, data[-2:-1]])

        return self.new_with_data(data)

    def copy(self):
        ce = None
        if self.cov_err is not None:
            ce = self.cov_err.copy()
        w = None
        if self.weights is not None:
            w = self.weights.copy()
        return self.new_with_data(self.data.copy(), ce, w)

    @staticmethod
    def load(filename):
        with tables.open_file(filename, 'r') as h5_file:
            if hasattr(h5_file.root, 'ft_cube'):
                return CartDataCube.load(filename)
            elif hasattr(h5_file.root, 'alm_cube'):
                from .sphcube import SphDataCube
                return SphDataCube.load(filename)
            else:
                raise ValueError('File %s is not of a supported format' % filename)

    def new_with_cov_err(self):
        if self.cov_err is None:
            return self.copy()
        return self.new_with_data(self.data + self.cov_err.get_sample())


class CartDataCube(DataCube):

    def __init__(self, data, uu, vv, freqs, meta, cov_err=None, weights=None):
        """Non-gridded visibilities cube

        Args:
            data (n_freqs, n_vis): visibilities cube array
            uu (n_vis): U in lambda
            vv (n_vis): V in lambda
            freqs (n_freqs): Frequencies in Hz
            res (float): Resolution of the original images
            nx (int): Nbs X pixels of the original images
            ny (int): Nbs Y pixels of the original images
            cov_err (ErrorCovariance, optional): Error covariance for this cube
        """
        self.uu = uu
        self.vv = vv
        self.meta = meta

        self.ru = np.sqrt(uu ** 2 + vv ** 2)

        DataCube.__init__(self, data, freqs, cov_err, weights)

    def __add_sub__(self, other, sub=False):
        if not np.allclose(self.meta.theta_fov, other.meta.theta_fov):
            print(f'Warning: The two datacubes does not have the same FoV {self.meta.theta_fov} vs {other.meta.theta_fov}')
        elif not np.allclose(self.meta.win_fct_power, other.meta.win_fct_power):
            print(f'Warning: The two datacubes does not have the same window fct {self.meta.win_fct_power} vs {other.meta.win_fct_power}')
        elif not np.allclose(self.meta.chan_width, other.meta.chan_width):
            print(f'Warning: The two datacubes does not have the same channel width {self.meta.chan_width} vs {other.meta.chan_width}')
        return DataCube.__add_sub__(self, other, sub=sub)

    def get_unique_xy(self):
        return np.round(self.uu, decimals=2) + 1e-6 * np.round(self.vv, decimals=2)

    @staticmethod
    def load_from_fits(files, umin, umax, convert_jy2k=True):
        freqs = []
        data_cube = []
        pr = psutil.progress_report(len(files))
        for i, file in enumerate(files):
            pr(i)
            hdu = pf.open(file)[0]
            data = hdu.data.squeeze()
            shape = data.shape
            du = hdu.header['CDELT1']
            freq = hdu.header['CRVAL3']
            fov = 1 / du
            res = fov / shape[0]

            if convert_jy2k:
                lamb = const.c.value / freq
                jy2k = ((1e-26 * lamb ** 2) / (2 * const.k_B.value))
                data = data * jy2k

            uu, vv, idx = psutil.get_ungrid_vis_idx(shape, res, umin, umax)
            data_cube.append(data[idx])
            freqs.append(freq)

        meta = ImageMetaData.from_res(res, shape, **hdu.header)

        return CartDataCube(np.array(data_cube), uu, vv, np.array(freqs), meta)

    @staticmethod
    def load_from_fits_image(files, umin, umax, theta_fov, imager_scale_factor=None,
                             convert_jy2k=True, compat_wscnormf='old_normpsf',
                             int_time=None, total_time=None,
                             window_function=None, data_dtype=np.complex128):
        """
        For each files do the following:
           - Read Fits image file
           - Trim image to theta_fov
           - Convert image from Jy/PSF to K, using imager_scale_factor or WSCNORMF
             attribute to get PSF "solid angle" (otherwise use Gaussian approx of the PSF)
           - FFT image per frequencies to get visibilities
           - Keep only non-zero visibilities between umin and umax.

           Return a CartDataCube object

        Args:
            files (n_files): List of Fits files to read
            umin (float): Min U in wavelength
            umax (float): Max U in wavelength
            theta_fov (float, optional): Fov in radians
            imager_scale_factor (None, optional): Explicitly set f_norm, following the formula
                omega_psf = (pixres) ** 2 * f_norm.
            convert_jy2k (bool, optional): Do Jy/PSF -> K conversion. Default to True.
            compat_wscnormf (str, optional): Compatibility for old/incorrect WSCNORMF:
                - 'old_normpsf': for normalizepsf < 16/06/2017
                - 'old_wsclean': for wslclean < 16/06/2017

        Returns:
            TYPE: Description
    """
        ft_cube = []
        freqs = []
        pr = psutil.progress_report(len(files))
        omega_gauss_warning = False
        compat_warning = False
        idx_ft = None
        meta = None

        if theta_fov is not None:
            theta_fov = 2 * np.sin(theta_fov / 2.)

        for i, file in enumerate(files):
            pr(i)
            hdu = pf.open(file)[0]
            header = hdu.header
            data = hdu.data.astype(data_dtype)

            res = abs(np.radians(header['CDELT1']))

            freq_start = header['CRVAL3']
            df = header['CDELT3']
            nf = header['NAXIS3']
            freq_end = freq_start + (nf - 1) * df
            fits_freqs = np.linspace(freq_start, freq_end, nf)

            lamb = const.c.value / fits_freqs

            cart_map = np.squeeze(data)

            if cart_map.ndim == 2:
                cart_map = cart_map[None, :, :]

            _, nx, ny = cart_map.shape

            if convert_jy2k:
                if 'WSCNORMF' in header and imager_scale_factor is None:
                    if compat_wscnormf == 'old_normpsf':
                        imager_scale_factor = header['WSCNORMF']
                        if not compat_warning:
                            print('Warning: using WSCNORMF as obtained by normpsf < 16/06/2017')
                    elif compat_wscnormf == 'old_wsclean':
                        imager_scale_factor = (nx * ny) / header['WSCNORMF'] / 4.
                        if not compat_warning:
                            print('Warning: using WSCNORMF as obtained by wsclean < 16/06/2017')
                    else:
                        imager_scale_factor = (nx * ny) / header['WSCNORMF']

                if imager_scale_factor is not None:
                    omega = imager_scale_factor * res ** 2
                else:
                    bmaj = header['BMAJ']
                    bmin = header['BMIN']
                    omega = np.radians(bmaj) * np.radians(bmin) * np.pi / (4 * np.log(2))
                    imager_scale_factor = omega / (res ** 2)
                    if not omega_gauss_warning:
                        omega_gauss_warning = True
                        print('Warning: WSCNORMF not found, using Gaussian approx. of the PSF (%.2f)'
                              % imager_scale_factor)

                jy2k = ((1e-26 * lamb ** 2) / (2 * const.k_B.value))
                jypsf2K = jy2k / omega
                cart_map = cart_map * jypsf2K[:, None, None]

            if theta_fov is not None:
                n = theta_fov / res

                i = int((nx - n) / 2.)
                if i > 0:
                    cart_map = cart_map[:, i:-i, i:-i]

            if window_function is not None:
                mask = window_function.generate_window(cart_map.shape[1])
                cart_map = cart_map * mask[None, :, :]

            if meta is None:
                meta = ImageMetaData.from_header(header, (nx, ny))

                if theta_fov is not None and i > 0:
                    meta.slice(i, nx - i, i, ny - i)

                if window_function is not None:
                    window_function.to_meta(meta)

            if idx_ft is None:
                uu, vv, idx_ft = psutil.get_ungrid_vis_idx(cart_map.shape[1:], res, umin, umax)

            ft = psutil.img_to_vis(cart_map, axes=(1, 2))

            uu = uu.flatten()
            vv = vv.flatten()

            for freq, ft_slice in zip(fits_freqs, ft):
                ft_cube.append(ft_slice[idx_ft])
                freqs.append(freq)

        if int_time is not None and 'PEINTTIM' not in meta:
            meta.set('PEINTTIM', int_time)

        if total_time is not None and 'PETOTTIM' not in meta:
            meta.set('PETOTTIM', total_time)

        return CartDataCube(np.array(ft_cube), uu, vv, np.array(freqs), meta)

    @staticmethod
    def load_from_fits_image_and_psf(files, files_psf, umin, umax, theta_fov, int_time=None, total_time=None,
                                     convert_jy2k=True, min_weight_ratio=0.01, trim_method='before',
                                     use_wscnormf=False, compat_wscnormf='old_normpsf', window_function=None,
                                     abs_min_weight=0.5, data_dtype=np.complex128):
        if use_wscnormf:
            ft_I_cube = CartDataCube.load_from_fits_image(files, umin, umax, theta_fov, compat_wscnormf=compat_wscnormf,
                                                          convert_jy2k=convert_jy2k, total_time=total_time,
                                                          int_time=int_time, window_function=window_function,
                                                          data_dtype=data_dtype)

            weight_cube = CartWeightCube.load_from_fits_psf(files_psf, umin, umax, int_time, total_time,
                                                            theta_fov=theta_fov, output_psf_cube=False,
                                                            window_function=window_function,
                                                            data_dtype=data_dtype)

            ft_I_cube.set_weights(weight_cube)

            return ft_I_cube

        b_theta_fov = None
        if trim_method in ['b', 'before']:
            b_theta_fov = theta_fov

        ft_I_cube = CartDataCube.load_from_fits_image(files, umin, umax, b_theta_fov, imager_scale_factor=1,
                                                      convert_jy2k=convert_jy2k,
                                                      total_time=total_time, int_time=int_time,
                                                      window_function=window_function, data_dtype=data_dtype)

        ft_psf_cube, weight_cube = CartWeightCube.load_from_fits_psf(files_psf, umin, umax, int_time, total_time,
                                                                     theta_fov=b_theta_fov, output_psf_cube=True,
                                                                     window_function=window_function)

        f = 1 / float(ft_I_cube.meta.shape[0] ** 2)
        with np.errstate(divide='ignore', invalid='ignore'):
            d_over_psf = np.where(ft_psf_cube.data != 0, np.divide(ft_I_cube.data, ft_psf_cube.data), 0)
        ft_I_rw_cube = ft_I_cube.new_with_data(d_over_psf * f, weights=weight_cube)

        if min_weight_ratio > 0:
            min_weight = min_weight_ratio * ft_I_rw_cube.weights.get().min(axis=0).max()
            min_weight = np.max([abs_min_weight, min_weight])
            ft_I_rw_cube.filter_min_weight(min_weight, replace=False)

        if trim_method in ['after', 'a']:
            ft_I_rw_cube = ft_I_rw_cube.reduce_fov(theta_fov, umin=umin, umax=umax)

        return ft_I_rw_cube

    @staticmethod
    def load_from_hd5(h5_group):
        ft_cube = h5_group.data.read()
        freqs = h5_group.freqs.read()
        uu = h5_group.uu.read()
        vv = h5_group.vv.read()
        attrs = h5_group.data.attrs
        header = dict([(k, psutil.safe_decode_bytes(attrs[k])) for k in attrs._f_list() if k[0].isupper()])

        if 'WCSAXES' in attrs:
            meta = ImageMetaData.from_header(header, attrs.shape)
        else:
            if 'shape' not in attrs:
                shape = (attrs.nx, attrs.ny)
            else:
                shape = attrs.shape
            meta = ImageMetaData.from_res(attrs.res, shape, **header)

        return CartDataCube(ft_cube, uu, vv, freqs, meta)

    @staticmethod
    def load(filename):
        """Load ft_cube from filename"""
        with tables.open_file(filename, 'r') as h5_file:
            cart_cube = CartDataCube.load_from_hd5(h5_file.root.ft_cube)
            if 'cov_err' in h5_file.root:
                cart_cube.cov_err = ErrorCovariance.load_from_hd5(h5_file.root.cov_err)
            if 'weights' in h5_file.root:
                cart_cube.weights = CartWeightCube.load_from_hd5(h5_file.root.weights)

        return cart_cube

    @staticmethod
    def join_cubes(cubes):
        j_cube = cubes[0]
        for cube in cubes[1:]:
            idx_new = ~np.in1d(_fmhz(cube.freqs), _fmhz(j_cube.freqs))
            j_cube.data = np.vstack([j_cube.data, cube.data[idx_new]])
            j_cube.freqs = np.concatenate([j_cube.freqs, cube.freqs[idx_new]])

        if cubes[0].weights is not None:
            weights = CartWeightCube.join_cubes([c.weights for c in cubes])
        else:
            weights = None

        return CartDataCube(j_cube.data, j_cube.uu, j_cube.vv, j_cube.freqs, j_cube.meta, weights=weights)

    def save_to_hd5(self, h5_file, group):
        h5_file.create_array(group, 'data', self.data, "Visibilities (K)")
        h5_file.create_array(group, 'freqs', self.freqs, "Frequencies (Hz)")
        h5_file.create_array(group, 'uu', self.uu, "U (lambda)")
        h5_file.create_array(group, 'vv', self.vv, "V (lambda)")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for key, value in self.meta.items(add_origin=True):
                group.data.attrs[key] = value

    def save(self, filename):
        """Save ft_cube to filename in h5 format"""
        with tables.open_file(filename, 'w') as h5_file:
            group = h5_file.create_group("/", 'ft_cube', 'Visibilty cube (n_freqs, n_vis)')
            self.save_to_hd5(h5_file, group)

            if self.cov_err is not None:
                group = h5_file.create_group("/", 'cov_err', 'Covariance error')
                self.cov_err.save_to_hd5(h5_file, group)

            if self.weights is not None:
                group = h5_file.create_group("/", 'weights', 'Weights cube (n_freqs, n_vis)')
                self.weights.save_to_hd5(h5_file, group)

    def new_with_data(self, data, cov_err=None, weights=None, freqs=None, interpolate_weights=True):
        """Create a new CartDataCube using data and cov_err"""
        if freqs is None:
            freqs = self.freqs

        if weights is None:
            weights = self.weights

        assert data.shape[0] == len(freqs)
        assert data.shape[1] == len(self.uu)

        if weights is not None:
            weights = weights.copy()

            if weights.data.shape[0] != len(freqs):
                w = scipy.interpolate.interp1d(weights.freqs, weights.data, bounds_error=False, 
                                               fill_value='extrapolate', axis=0)(freqs)
                weights = weights.new_with_data(w, freqs=freqs)

        return CartDataCube(data, self.uu, self.vv, freqs, self.meta.copy(),
                            cov_err=cov_err, weights=weights)

    def make_full_cube(self, umin, umax, output_idx=False):
        freqs = np.array(sorted(np.concatenate((self.freqs, psutil.get_freqs_gaps(self.freqs)))))
        uu, vv, _ = psutil.get_ungrid_vis_idx(self.meta.shape, self.meta.res, umin, umax)

        weights = None
        if self.weights is not None:
            weights = self.weights.make_full_cube(umin, umax)

        cube = CartDataCube(np.zeros((len(freqs), len(uu)), dtype=np.complex128),
                            uu, vv, freqs, self.meta.copy(), weights=weights)

        idx1, idx1_uv, idx2, idx2_uv = get_common_idx(cube, self)

        data_f = cube.data[idx1]
        data_f[:, idx1_uv] = self.data
        cube.data[idx1] = data_f

        if output_idx:
            return cube, idx1, idx1_uv

        return cube

    def estimate_sefd(self, sefd_jansky=True):
        assert self.weights is not None

        return self.weights.estimate_sefd(self, sefd_jansky=sefd_jansky)

    def estimate_uv_sefd(self, sefd_jansky=True):
        assert self.weights is not None

        return self.weights.estimate_uv_sefd(self, sefd_jansky=sefd_jansky)

    def estimate_freqs_sefd(self, sefd_jansky=True, sefd_poly_fit_deg=0):
        assert self.weights is not None

        sefd = self.weights.estimate_freqs_sefd(self, sefd_jansky=sefd_jansky)

        if sefd_poly_fit_deg > 0:
            sefd_fct = np.poly1d(np.polyfit(np.log(self.freqs), np.log(sefd), sefd_poly_fit_deg))
            sefd = np.exp(sefd_fct(np.log(self.freqs)))

        return sefd

    def get_hermitian_index(self):
        idx1_a = (self.uu > 0)
        idx1_b = ((self.uu == 0) & (self.vv > 0))

        idx2_a = psutil.get_selection_index(self.uu, self.vv, - self.uu[idx1_a],
                                            - self.vv[idx1_a], True)
        idx2_b = psutil.get_selection_index(self.uu, self.vv, self.uu[idx1_b],
                                            - self.vv[idx1_b], True)

        idx1 = np.concatenate([np.where(idx1_a)[0], np.where(idx1_b)[0]])
        idx2 = np.concatenate([idx2_a, idx2_b])

        return idx1, idx2

    def regrid(self):
        ''' Grid the visibilities and return a GriddedCartDataCube '''
        nx, ny = self.meta.shape
        g_uu, g_vv, idx = psutil.get_regrid_vis_idx(self.uu, self.vv, self.meta.res, self.meta.shape)

        g_data = np.zeros((self.freqs.size, g_uu.size), dtype=np.complex128)
        g_data[:, idx] = self.data
        g_data = g_data.reshape((self.freqs.size, nx, ny))

        return GriddedCartDataCube(g_data, g_uu, g_vv, self.freqs, self.meta.copy())

    def image(self):
        return self.regrid().image()

    def reduce_fov(self, new_fov, low_memory=False, umin=None, umax=None):
        """Reduce FoV by regridding, imaging, trimming and FTing back. The error covariance
        is estimated from Monte Carlo.

        Args:
            new_fov (float): New FoV.
            mc_n_samples (int, optional): Number of MC samples
            low_memory (bool, optional): Reduce FoV frequency by frequency,
                avoiding imaging the full cube. Error propagation will NOT be perform.

        Returns:
            CartDataCube: a new CartDataCube
        """
        if new_fov >= self.meta.theta_fov:
            return self

        if umin is None:
            umin = np.round(self.ru.min(), 2)
        if umax is None:
            umax = np.round(self.ru.max(), 2)

        if self.weights is not None:
            new_weights = self.weights.reduce_fov(new_fov, low_memory=low_memory, umin=umin, umax=umax)

        if not low_memory:
            img_cube = self.regrid().image()
            img_cube.trim(new_fov)
            new_cube = img_cube.ft(umin, umax)
        else:
            trimmed_cubes = []
            for freq in self.freqs:
                img_cube = self.get_freq(freq).regrid().image()
                img_cube.trim(new_fov)
                trimmed_cubes.append(img_cube.ft(umin, umax))

            data = np.array([c.data[0] for c in trimmed_cubes])
            freqs = np.array([c.freqs[0] for c in trimmed_cubes])
            new_cube = CartDataCube(data, trimmed_cubes[0].uu, trimmed_cubes[0].vv, freqs,
                                    trimmed_cubes[0].meta)

        if self.weights is not None:
            new_cube.set_weights(new_weights)

        return new_cube

    def apply_window_function(self, win_fct, umin=None, umax=None, add_to_meta=True):
        if umin is None:
            umin = np.round(self.ru.min(), 2)
        if umax is None:
            umax = np.round(self.ru.max(), 2)

        if self.weights is not None:
            new_weights = self.weights.apply_window_function(win_fct, umin=umin, umax=umax, add_to_meta=add_to_meta)

        img_cube = self.regrid().image()
        img_cube.apply_window_function(win_fct, add_to_meta=add_to_meta)
        new_cube = img_cube.ft(umin, umax)

        if self.weights is not None:
            new_cube.set_weights(new_weights)

        return new_cube

    def filter_uvrange(self, umin, umax):
        idx_uv = (self.ru >= umin) & (self.ru <= umax)
        self.filter_uv_from_index(idx_uv)

    def filter_outliers(self, idx_outliers):
        ''' Filter out outliers given by idx_outliers'''
        self.freqs = self.freqs[~idx_outliers]
        self.data = self.data[~idx_outliers]

        if self.cov_err is not None:
            self.cov_err.filter_outliers(idx_outliers)

        if self.weights is not None:
            self.weights.filter_outliers(idx_outliers)

    def filter_freqs_from_other(self, other):
        idx1 = np.in1d(_fmhz(self.freqs), _fmhz(other.freqs))
        self.filter_outliers(~idx1)

    def filter_nan(self):
        idx_nan = np.any(np.isnan(self.data), 1)
        if len(self.freqs[idx_nan]) > 0:
            print('SB with NaN:', self.freqs[idx_nan])
            self.filter_outliers(idx_nan)

    def filter_min_weight(self, min_weight, replace=False, verbose=True):
        if self.weights is not None and min_weight > 0:
            if replace:
                idx_uv = self.weights.get() >= min_weight
                n_filt = np.sum(~idx_uv)
                n_tot = float(len(self.uu) * len(self.freqs))
                if verbose:
                    print('Filtering %s visibilities (%.2f %%)' % (n_filt, n_filt / n_tot * 100))
                self.data[~idx_uv] = 0
                self.weights.data[~idx_uv] = 0
            else:
                idx_uv = np.median(self.weights.get(), axis=0) >= min_weight
                n_filt = np.sum(~idx_uv)
                n_tot = float(len(self.uu))
                if verbose:
                    print('Filtering %s modes (%.2f %%)' % (n_filt, n_filt / n_tot * 100))
                self.filter_uv_from_index(idx_uv)

    def filter_sefd_uv(self, max_sefd, min_sefd=0):
        sefd = self.estimate_uv_sefd().data.mean(axis=0)
        idx_uv = (sefd >= min_sefd) & (sefd <= max_sefd)
        n_filt = np.sum(~idx_uv)
        n_tot = float(len(self.uu))
        print('Filtering %s modes (%.2f %%)' % (n_filt, n_filt // n_tot * 100))

        self.filter_uv_from_index(idx_uv)

        return idx_uv

    def filter_uv_from_index(self, idx_uv):
        DataCube.filter_uv_from_index(self, idx_uv)
        self.uu = self.uu[idx_uv]
        self.vv = self.vv[idx_uv]
        self.ru = self.ru[idx_uv]

    def average_freqs(self, n_freqs):
        freqs = self.freqs
        bins = np.arange(len(freqs) // n_freqs)
        digi = np.repeat(bins, n_freqs)[:len(freqs)]

        new_freqs = np.array([freqs[digi == k].mean() for k in bins])

        if self.weights is not None:
            w = self.weights.data
        else:
            w = np.ones_like(self.data)

        new_data = np.array([(self.data[digi == k, :] * w[digi == k, :]).sum(axis=0) /
                             w[digi == k, :].sum(axis=0) for k in bins])

        new_weight_cube = None

        if self.weights is not None:
            new_w = np.array([w[digi == k, :].sum(axis=0) for k in bins])
            new_weight_cube = CartWeightCube(new_w, self.weights.uu, self.weights.vv, new_freqs, self.weights.meta)

        avg_cube = self.new_with_data(new_data, weights=new_weight_cube, freqs=new_freqs)
        avg_cube.meta = self.meta.copy()
        avg_cube.meta.average_freqs(n_freqs)

        return avg_cube

    def average_same_uv(self):

        def binsum(x, y):
            return np.array([np.bincount(x, k) for k in y])

        x = np.round(self.uu, decimals=2) + 1e-6 * np.round(self.vv, decimals=2)
        x_u, idx, idx_r = np.unique(x, return_index=True, return_inverse=True)
        w = binsum(idx_r, self.weights.get())
        w_psf = binsum(idx_r, self.weights.data.real)
        dw = binsum(idx_r, self.weights.get() * self.data.real) + 1j * \
            binsum(idx_r, self.weights.get() * self.data.imag)
        # w = self.data.weights.get()[:, idx]
        d = dw / w
        uv_scale = w.mean(axis=0) / w_psf.mean(axis=0)

        uu = self.uu[idx]
        vv = self.vv[idx]

        weights = CartWeightCube(w_psf, uu, vv, self.freqs, self.meta, uv_scale=uv_scale[None, :])
        cube = CartDataCube(d, uu, vv, self.freqs, self.meta, weights=weights)

        return cube

    def plot_uv(self, fmhz='med', action_fct=None, uv_lines=[50, 100, 150, 200, 250], ax=None,
                apply_uv_scale=False, title=None, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        d = self.data
        if apply_uv_scale:
            d = self.get()

        if action_fct is None:
            if fmhz == 'med':
                fmhz = (self.freqs[0] + (self.freqs[-1] - self.freqs[0]) / 2.) * 1e-6
            elif fmhz == 'first':
                fmhz = self.freqs[0] * 1e-6
            elif fmhz == 'last':
                fmhz = self.freqs[-1] * 1e-6

            i = np.argmin(abs(self.freqs - fmhz * 1e6))
            d = d[i]
        else:
            d = action_fct(d, axis=0)

        cbs = psutil.ColorbarSetting(psutil.ColorbarOutterPosition())
        im_mappable = ax.scatter(self.uu, self.vv, c=d.real, **kargs)
        cbs.add_colorbar(im_mappable, ax)

        ax.set_xlabel('U (lambda)')
        ax.set_ylabel('V (lambda)')

        for uv in uv_lines:
            ax.add_artist(plt.Circle([0, 0], uv, ls='--', fc=None, ec=psutil.lblack, fill=False))

        if title is not None:
            ax.set_title(title)


class CartDataCubeMeter(CartDataCube):

    def get_cube(self, mfreq):
        lamb = const.c.value / mfreq

        weights = None
        if self.weights is not None:
            weights = self.weights.get_cube(mfreq)

        return CartDataCube(self.data, self.uu / lamb, self.vv / lamb,
                            self.freqs, self.meta, cov_err=self.cov_err,
                            weights=weights)

    def get_baseline(self, mfreq, baseline):
        i = np.nonzero(np.round(baseline, 2) == np.round(self.ru, 2))[0]
        if len(i) == 0:
            print('No baseline with length %s m' % baseline)
            return None

        cube = self.get_cube(mfreq)
        cube.uu = cube.uu[i[0]:i[0] + 1]
        cube.vv = cube.vv[i[0]:i[0] + 1]
        cube.ru = cube.ru[i[0]:i[0] + 1]
        cube.data = cube.data[:, i[0]:i[0] + 1]

        if self.weights is not None:
            cube.weights = self.weights.get_baseline(mfreq, baseline)
            cube.weights.uv_scale = cube.weights.uv_scale[:, i[0]:i[0] + 1]

        return cube

    def new_with_data(self, data, cov_err=None, weights=None, freqs=None):
        if freqs is None:
            freqs = self.freqs

        if weights is None:
            weights = self.weights

        assert data.shape[0] == len(freqs)
        assert data.shape[1] == len(self.uu)

        if weights is not None:
            weights = weights.copy()

        return CartDataCubeMeter(data, self.uu, self.vv, freqs, self.meta.copy(),
                                 cov_err=cov_err, weights=weights)

    @staticmethod
    def load(filename):
        cube = CartDataCube.load(filename)
        weights = None
        if cube.weights is not None:
            weights = CartWeightsCubeMeter(cube.weights.data, cube.uu, cube.vv, cube.freqs,
                                           cube.meta, cube.weights.uv_scale)

        return CartDataCubeMeter(cube.data, cube.uu, cube.vv, cube.freqs, cube.meta, weights=weights)


class MultiNightsCube(object):

    def __init__(self, cubes=None, nights=None, inhomogeneous=False):
        if cubes is None:
            cubes = []
            nights = []
        self.cubes = cubes
        self.nights = nights
        self.inhomogeneous = inhomogeneous

    def __iter__(self):
        for c in self.cubes:
            yield c

    def concat(self):
        data = np.hstack([c.data for c in self.cubes])
        weights_data = np.hstack([c.weights.data for c in self.cubes])
        uu = np.tile(self.uu, len(self.nights))
        vv = np.tile(self.vv, len(self.nights))

        weights = CartWeightCube(weights_data, uu, vv, self.freqs, self.meta)

        cube = CartDataCube(data, uu, vv, self.freqs, self.meta, weights=weights)
        cube.origin = np.repeat(self.nights, len(self.uu))

        return cube

    @property
    def data(self):
        return np.dstack([c.data for c in self.cubes])

    @property
    def uu(self):
        return self.cubes[0].uu

    @property
    def vv(self):
        return self.cubes[0].vv

    @property
    def ru(self):
        return self.cubes[0].ru

    @property
    def freqs(self):
        return self.cubes[0].freqs

    @property
    def meta(self):
        return self.cubes[0].meta

    def get_slice_from_idx(self, idx_freqs):
        for i in np.arange(len(self.cubes)):
            self.cubes[i] = self.cubes[i].get_slice_from_idx(idx_freqs)

        return self

    def get_slice(self, freq_start, freq_end):
        ''' Return an ErrorCovariance for the given frequency slice'''
        idx_freqs = psutil.get_freq_slice(self.freqs, freq_start, freq_end)

        return self.get_slice_from_idx(idx_freqs)

    def add(self, cube, night):
        if len(self.cubes) > 0 and not self.inhomogeneous:
            self.cubes[0], cube = get_common_cube(self.cubes[0], cube)

        self.cubes.append(cube)
        self.nights.append(night)

    def done(self):
        for i in np.arange(len(self.cubes) - 1) + 1:
            _, self.cubes[i] = get_common_cube(self.cubes[0], self.cubes[i])


class MultiDataInfo(object):

    def __init__(self, filename):
        self.d = {}
        for n, s, e, d in np.loadtxt(filename, str):
            self.d[n] = (float(s), float(e), float(d))

    def start(self, night):
        return self.d[night][0]

    def end(self, night):
        return self.d[night][1]

    def duration(self, night):
        return self.d[night][2]


class NoiseStdCube(CartDataCube):
    
    def __init__(self, data, uu, vv, freqs, meta, weights=None):
        CartDataCube.__init__(self, data, uu, vv, freqs, meta, weights=weights)

    def __add_sub__(self, other, sub=False):
        if not isinstance(other, NoiseStdCube):
            raise TypeError('NoiseStdCube object can not be combined with another type.')
        return CartDataCube.__add_sub__(self, other, sub=sub)

    def generate_noise_cube(self, hermitian=True):
        """
        Generate a complex Gaussian noise cube in uv space.

        If `hermitian=True`, enforce Hermitian symmetry
        V(-u, -v) = conj(V(u, v)) so that the corresponding
        image after iFFT is real.
        """
        if np.iscomplexobj(self.data):
            std_real = self.data.real
            std_imag = self.data.imag
        else:
            std_real = std_imag = self.data.real / np.sqrt(2)
        data = (np.random.normal(scale=std_real) + 1j * np.random.normal(scale=std_imag))

        if hermitian:
            idx1, idx2 = self.get_hermitian_index()
            data[:, idx2] = np.conj(data[:, idx1])

        return CartDataCube(data, self.uu, self.vv, self.freqs, self.meta.copy(), weights=self.weights.copy())
        
    def new_with_data(self, data, cov_err=None, weights=None, freqs=None):
        if freqs is None:
            freqs = self.freqs

        if weights is None:
            weights = self.weights

        assert data.shape[0] == len(freqs)
        assert data.shape[1] == len(self.uu)

        if weights is not None:
            weights = weights.copy()

        return NoiseStdCube(data, self.uu, self.vv, freqs, self.meta.copy(), weights=weights)

    @staticmethod
    def load(filename):
        d = CartDataCube.load(filename)
        return NoiseStdCube(d.data, d.uu, d.vv, d.freqs, d.meta, weights=d.weights)


class CartWeightCube(CartDataCube):

    def __init__(self, weight_cube, uu, vv, freqs, meta, uv_scale=None, freqs_n_nights=None):
        CartDataCube.__init__(self, weight_cube, uu, vv, freqs, meta)
        if uv_scale is None:
            self.unscale()
        else:
            self.uv_scale = uv_scale
        if freqs_n_nights is None:
            self.freqs_n_nights = np.ones(len(self.freqs))
        else:
            self.freqs_n_nights = freqs_n_nights

    def __add_sub__(self, other, sub=False):
        a = self.copy_with_applied_uv_scale()
        b = other.copy_with_applied_uv_scale()
        return CartDataCube.__add_sub__(a, b, sub=sub)

    def get(self, with_uv_scale=True):
        if with_uv_scale:
            return abs(self.data * self.uv_scale)
        return abs(self.data)

    def copy_with_applied_uv_scale(self):
        new = self.new_with_data(self.data * self.uv_scale)
        new.unscale()
        return new

    def filter_uv_from_index(self, idx_uv):
        CartDataCube.filter_uv_from_index(self, idx_uv)
        self.uv_scale = self.uv_scale[:, idx_uv]

    def get_slice_from_idx(self, idx):
        cube = CartDataCube.get_slice_from_idx(self, idx)
        cube.freqs_n_nights = self.freqs_n_nights.copy()[idx]

        return cube

    def filter_outliers(self, idx_outliers):
        ''' Filter out outliers given by idx_outliers'''
        CartDataCube.filter_outliers(self, idx_outliers)
        self.freqs_n_nights = self.freqs_n_nights[~idx_outliers]

    def make_full_cube(self, umin, umax):
        cube, idx1, idx1_uv = CartDataCube.make_full_cube(self, umin, umax, output_idx=True)
        uv_scale = np.ones((1, cube.data.shape[1]))
        uv_scale[:, idx1_uv] = self.uv_scale

        return CartWeightCube(cube.data, cube.uu, cube.vv, cube.freqs, cube.meta, uv_scale=uv_scale)

    def reduce_fov(self, new_theta_fov, low_memory=False, umin=None, umax=None):
        new_cube = CartDataCube.reduce_fov(self, new_theta_fov, low_memory=low_memory, umin=umin, umax=umax)

        return CartWeightCube(new_cube.data, new_cube.uu, new_cube.vv, new_cube.freqs, new_cube.meta)

    def apply_window_function(self, win_fct, umin=None, umax=None, mc_n_samples=2000, add_to_meta=True):
        new_cube = CartDataCube.apply_window_function(self, win_fct, umin=umin, umax=umax, add_to_meta=add_to_meta)

        return CartWeightCube(new_cube.data, new_cube.uu, new_cube.vv, new_cube.freqs, new_cube.meta)

    @staticmethod
    def load_from_fits_psf(files, umin, umax, int_time=None, total_time=None, theta_fov=None, low_memory=False,
                           output_psf_cube=False, window_function=None, data_dtype=np.complex128):
        cart_cube = CartDataCube.load_from_fits_image(files, umin, umax, theta_fov,
                                                      convert_jy2k=False,
                                                      window_function=window_function, data_dtype=data_dtype)
        if 'PEINTTIM' not in cart_cube.meta:
            assert int_time is not None
            cart_cube.meta.set('PEINTTIM', int_time)

        if 'PETOTTIM' not in cart_cube.meta:
            assert total_time is not None
            cart_cube.meta.set('PETOTTIM', total_time)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            header = pf.getheader(files[0])

        if 'WSCENVIS' in header:
            w_key = 'WSCENVIS'
        elif 'WSCNVIS' in header:
            w_key = 'WSCNVIS'
        elif 'WEIGHT' in header:
            w_key = 'WEIGHT'
        else:
            print('Error: no normalization factor found in header.')
            return None

        cart_cube.meta.set('PEWKEY', w_key)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            n_vis = np.array([pf.getheader(file)[w_key] for file in files])

        # In the uv plane, we have two times n_vis visibilities because the transposed is repeated
        weights = cart_cube.data * n_vis[:, None] * 2

        weight_cube = CartWeightCube(weights, cart_cube.uu, cart_cube.vv, cart_cube.freqs, cart_cube.meta)
        if output_psf_cube:
            return cart_cube, weight_cube

        return weight_cube

    @staticmethod
    def load(filename):
        d = CartDataCube.load(filename)
        return CartWeightCube(d.data, d.uu, d.vv, d.freqs, d.meta)

    @staticmethod
    def load_from_hd5(h5_group):
        d = CartDataCube.load_from_hd5(h5_group)
        uv_scale = None
        if hasattr(h5_group, 'uv_scale'):
            uv_scale = h5_group.uv_scale.read()
        freqs_n_nights = None
        if hasattr(h5_group, 'freqs_n_nights'):
            freqs_n_nights = h5_group.freqs_n_nights.read()
        return CartWeightCube(d.data, d.uu, d.vv, d.freqs, d.meta, uv_scale=uv_scale,
                              freqs_n_nights=freqs_n_nights)

    def save_to_hd5(self, h5_file, group):
        CartDataCube.save_to_hd5(self, h5_file, group)
        h5_file.create_array(group, 'uv_scale', self.uv_scale, "UV scale")
        h5_file.create_array(group, 'freqs_n_nights', self.freqs_n_nights, "Number of nights")

    @staticmethod
    def from_noise_cube(noise_cube, delta_u):
        d_ru = np.arange(noise_cube.ru.min(), noise_cube.ru.max(), delta_u)
        d_ru = np.concatenate([[0], d_ru[1:-1], [np.inf]])
        noise_scale = np.ones_like(noise_cube.ru, dtype=float)
        for ru_min, ru_max in psutil.pairwise(d_ru):
            idx = (noise_cube.ru >= ru_min) & (noise_cube.ru <= ru_max)
            noise_scale[idx] = psutil.mad(noise_cube.data[:, idx])

        noise_scale = noise_scale / noise_scale.mean()
        noise_scale = np.repeat(noise_scale[None, :], len(noise_cube.freqs), axis=0)

        # TODO: scale the noise_cube better
        meta = noise_cube.meta.copy()
        meta.set('PEINTTIM', 10)
        meta.set('PETOTTIM', 10)

        return CartWeightCube(1 / noise_scale ** 2, noise_cube.uu, noise_cube.vv,
                              noise_cube.freqs, meta)

    def estimate_sefd(self, noise_cube, sefd_jansky=True, axis=None):
        df = self.meta.chan_width
        int_time = self.meta.int_time

        w = abs(self.get_slice(noise_cube.freqs[0], noise_cube.freqs[-1]).data)
        w[w == 0] = np.nan
        sefd = noise_cube.data * (2 * df * int_time * 1) ** 0.5 * w ** 0.5

        # noise in Kelvin is for the image FoV
        if sefd_jansky:
            lamb = const.c.value / noise_cube.freqs
            fov = (self.meta.shape[0] * self.meta.res) ** 2
            jy2k = ((1e-26 * lamb ** 2) / (2 * const.k_B.value)) / fov
            sefd = sefd / jy2k[:, None]

        # Correct for the spatial-coherence introduce by the spatial tapering/window
        sefd = sefd / self.meta.win_fct_power ** .5

        return psutil.mad(sefd, axis=axis)

    def estimate_uv_sefd(self, noise_cube, sefd_jansky=True):
        sefd = self.estimate_sefd(noise_cube, sefd_jansky=sefd_jansky, axis=0)

        return CartDataCube(sefd[None, :], self.uu, self.vv, np.array([self.freqs.mean()]), self.meta.copy())

    def estimate_freqs_sefd(self, noise_cube, sefd_jansky=True):
        return self.estimate_sefd(noise_cube, sefd_jansky=sefd_jansky, axis=1)

    def scale_with_noise_cube(self, noise_cube, sefd_poly_fit_deg=0, sefd_filter_n_bins=0, expected_sefd=None, scale_freqs=False):
        sefd_uv = self.estimate_uv_sefd(noise_cube).data
        if expected_sefd is None:
            expected_sefd = np.nanmedian(sefd_uv)

        self.uv_scale = (expected_sefd / sefd_uv) ** 2

        if sefd_poly_fit_deg > 0:
            mask = np.isfinite(self.uv_scale[0])
            uv_fct = np.poly1d(np.polyfit(np.log(self.ru[mask]), np.log(self.uv_scale[0, mask]),
                                          sefd_poly_fit_deg))

            self.uv_scale = np.exp(uv_fct(np.log(self.ru))[None, :])

        if sefd_filter_n_bins > 0:
                m_sefd, _, _ = binned_statistic(self.ru, self.uv_scale, bins=sefd_filter_n_bins)
                m_ru, _, _ = binned_statistic(self.ru, self.ru, bins=sefd_filter_n_bins)
                self.uv_scale = scipy.interpolate.interp1d(m_ru, m_sefd, bounds_error=False, 
                                                           kind='slinear', fill_value='extrapolate')(self.ru)

        if scale_freqs:
            sefd_freqs = self.estimate_freqs_sefd(noise_cube)
            self.uv_scale = self.uv_scale * (np.nanmedian(sefd_freqs) / sefd_freqs)[:, None] ** 2

        self.uv_scale[~np.isfinite(self.uv_scale)] = 1

    def random_scale(self, max_ratio=2, hermitian=True):
        shape = self.uv_scale.shape
        self.uv_scale = 10 ** (np.log10(max_ratio) / 0.5 * (np.random.random(shape) - 0.5))
        if hermitian:
            idx1, idx2 = self.get_hermitian_index()
            self.uv_scale[:, idx1] = self.uv_scale[:, idx2]

    def unscale(self):
        self.uv_scale = np.ones((1, len(self.uu)))

    def simulate_noise(self, sefd, time, hermitian=True, weights_uncertainity_ratio=None,
                       sefd_jansky=True, fake_apply_win_fct=False):
        df = self.meta.chan_width
        int_time = self.meta.int_time
        total_time = self.meta.total_time
        f = time / total_time

        # noise_rms = sefd / (2 * df * int_time * f) ** 0.5
        noise_rms = np.atleast_1d(sefd / (2 * df * int_time * f) ** 0.5)[:, None]

        # noise_rms for each complex part
        noise_rms = np.sqrt(0.5) * noise_rms

        if fake_apply_win_fct:
            # Scale noise_rms as if a spatial tapering had been applied.
            noise_rms = noise_rms * self.meta.win_fct_power ** .5

        if sefd_jansky:
            lamb = const.c.value / self.freqs
            fov = (self.meta.shape[0] * self.meta.res) ** 2
            jy2k = ((1e-26 * lamb ** 2) / (2 * const.k_B.value)) / fov
            noise_rms = jy2k[:, None] * noise_rms

        w = self.get() ** 0.5
        s = self.data.shape

        if weights_uncertainity_ratio is not None:
            w_scale = 10 ** (np.log10(weights_uncertainity_ratio) / 0.5 * (np.random.random(w.shape) - 0.5))
            if hermitian:
                idx1, idx2 = self.get_hermitian_index()
                w_scale[idx1] = w_scale[idx2]
            w = w * w_scale

        if hermitian:
            idx1, idx2 = self.get_hermitian_index()

            hs = (self.data.shape[0], len(idx1))
            noise_data = np.zeros_like(self.data, dtype=np.complex128)
            noise_data[:, idx1] = noise_rms / w[:, idx1] * \
                (np.random.randn(*hs) + 1j * np.random.randn(*hs))
            noise_data[:, idx2] = np.conj(noise_data[:, idx1])
        else:
            noise_data = noise_rms / w * (np.random.randn(*s) + 1j * np.random.randn(*s))

        weights = self.new_with_data(self.data * f)

        noise_cube = CartDataCube(noise_data, self.uu, self.vv, self.freqs.copy(),
                                  self.meta.copy(), weights=weights)
        if not fake_apply_win_fct:
            noise_cube.meta.remove('PEWINFCT')
            noise_cube.weights.meta.remove('PEWINFCT')

        return noise_cube

    def get_noise_std_cube(self, sefd, time, fake_apply_win_fct=False):
        df = self.meta.chan_width
        int_time = self.meta.int_time
        total_time = self.meta.total_time
        f = time / total_time

        noise_rms = np.atleast_1d(sefd / (2 * df * int_time * f) ** 0.5)

        lamb = const.c.value / self.freqs
        fov = (self.meta.shape[0] * self.meta.res) ** 2
        jy2k = ((1e-26 * lamb ** 2) / (2 * const.k_B.value)) / fov
        noise_rms = (jy2k * noise_rms)[:, None]

        w = self.get() ** 0.5
        noise_rms = noise_rms / w

        if fake_apply_win_fct:
            # Scale noise_rms as if a spatial tapering had been applied.
            noise_rms = noise_rms * self.meta.win_fct_power ** .5

        weights = self.new_with_data(self.data * f)

        noise_cube = NoiseStdCube(noise_rms, self.uu, self.vv, self.freqs.copy(),
                                  self.meta.copy(), weights=weights)
        if not fake_apply_win_fct:
            noise_cube.meta.remove('PEWINFCT')
            noise_cube.weights.meta.remove('PEWINFCT')

        return noise_cube

    def new_with_data(self, data, cov_err=None, weights=None, freqs=None):
        """Create a new CartWeightCube using data and cov_err"""
        if freqs is None:
            freqs = self.freqs

        assert data.shape[0] == len(freqs)
        assert data.shape[1] == len(self.uu)
        assert data.shape[1] == self.uv_scale.shape[1]

        return CartWeightCube(data, self.uu, self.vv, freqs, self.meta.copy(),
                              uv_scale=self.uv_scale.copy())

    @staticmethod
    def join_cubes(cubes):
        j_cube = CartDataCube.join_cubes([c.copy_with_applied_uv_scale() for c in cubes])

        return CartWeightCube(j_cube.data, j_cube.uu, j_cube.vv, j_cube.freqs, j_cube.meta.copy(), uv_scale=None)

    def copy(self):
        return CartWeightCube(self.data.copy(), self.uu.copy(), self.vv.copy(), self.freqs.copy(),
                              self.meta.copy(), uv_scale=self.uv_scale.copy(),
                              freqs_n_nights=self.freqs_n_nights.copy())


class CartWeightsCubeMeter(CartWeightCube, CartDataCubeMeter):

    def get_cube(self, mfreq):
        lamb = const.c.value / mfreq

        return CartWeightCube(self.data, self.uu / lamb, self.vv / lamb,
                              self.freqs, self.meta, uv_scale=self.uv_scale)

    def new_with_data(self, data, cov_err=None, weights=None, freqs=None):
        if freqs is None:
            freqs = self.freqs

        assert data.shape[0] == len(freqs)
        assert data.shape[1] == len(self.uu)
        assert data.shape[1] == self.uv_scale.shape[1]

        return CartWeightsCubeMeter(data, self.uu, self.vv, freqs, self.meta.copy(),
                                    uv_scale=self.uv_scale.copy())

    def copy(self):
        return CartWeightsCubeMeter(self.data.copy(), self.uu.copy(), self.vv.copy(), self.freqs.copy(),
                                    self.meta.copy(), uv_scale=self.uv_scale.copy(),
                                    freqs_n_nights=self.freqs_n_nights.copy())
