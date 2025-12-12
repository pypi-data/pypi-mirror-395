# Collection of functions
#
# Authors: F.Mertens

import re
import os
import sys
import time
import copy
import functools
import itertools
import configparser

from scipy import stats
from scipy.sparse import diags
from scipy.signal import get_window

import numpy as np

import h5py


NUM_POOL = int(os.environ.get('OMP_NUM_THREADS', 2))

try:
    import pyfftw
    fft = lambda *args, **kargs: pyfftw.interfaces.numpy_fft.fft(*args, threads=NUM_POOL, **kargs)
    fft2 = lambda *args, **kargs: pyfftw.interfaces.numpy_fft.fft2(*args, threads=NUM_POOL, **kargs)
    ifft2 = lambda *args, **kargs: pyfftw.interfaces.numpy_fft.ifft2(*args, threads=NUM_POOL, **kargs)
    # print("Using FFTW with %s threads" % NUM_POOL)
except Exception:
    fft = np.fft.fft
    fft2 = np.fft.fft2
    ifft2 = np.fft.ifft2
    print("Warning: using slower numpy fft's functions. Consider installing pyfftw.")

from matplotlib import ticker
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1 import make_axes_locatable

from scipy.special import j1 as bessel_j1

from astropy.cosmology import Planck15 as cosmo
import astropy.units as u
import astropy.constants as const

# Andre pstransform cosmology
# from astropy.cosmology import LambdaCDM
# cosmo = LambdaCDM(69.32, 0.2865, 0.713413)

f21 = 1.4204057 * 1e9 * u.Hz

color_cycle = ['#3465a4', '#4e9a06', '#cc0000', '#F57900', '#75507b', '#EDD400', '#555753']
blue, green, red, orange, magenta, yellow, black = color_cycle

color_cycle_light = ['#729FCF', '#8AE234', '#EF2929', '#FCAF3E', '#AD7FA8', '#FCE94F', '#888A85']
lblue, lgreen, lred, lorange, lmagenta, lyellow, lblack = color_cycle_light

color_cycle_dark = ['#204A87', '#4E9A06', '#A40000', '#CE5C00', '#5C3566', '#C4A000', '#2E3436']
dblue, dgreen, dred, dorange, dmagenta, dyellow, dblack = color_cycle_dark


def set_cosmology(new_cosmo):
    global cosmo
    cosmo = new_cosmo


class FastHeaderReader(list):

    _RE_FITS_HEADER_LINE = re.compile(r"^([^=]{8})=([ ]*'.*'[ ]*|[ ]*[0-9.\-\+E]+[ ]*|[ ]*NAN[ ]*|[ ]*[TF][ ]*)/?(.*)$")

    def __init__(self, file, keys=None):
        self.file = file
        self.keys = keys
        self.read()

    def read(self):
        with open(self.file, mode='rb') as fd:
            for i in range(100):
                line = fd.read(80).decode("utf-8")
                if not line.strip() or line.strip() == 'END':
                    break
                key = line[:8].rstrip()
                if self.keys and key not in self.keys:
                    continue
                if key == 'COMMENT' or key == 'HISTORY':
                    continue
                match = self._RE_FITS_HEADER_LINE.match(line)
                if match is None:
                    continue
                    # raise Exception("Error while parsing '%s' at line '%s'" % (self.file, line))
                (key, value, comment) = match.groups()
                value = value.strip()
                key = key.strip()
                if comment.strip() != '':
                    comment = comment.rstrip()
                self.append({"key": key, "value": value, "comment": comment,
                             "offset": 80 * i, "newline": ''})
                if self.keys:
                    self.keys.remove(key)
                    if not self.keys:
                        break

    def __get_line(self, key):
        for line in self:
            if key == line['key']:
                return line
        raise Exception("No key '%s' in the header" % key)

    def __format_value(self, value):
        if value == 'T':
            return True
        elif value == 'F':
            return False
        elif value[0] == "'":
            value = value[1:-1].rstrip()
            if value == '':
                value = ' '
            return value
        return float(value)

    def get_value(self, key):
        return self.__format_value(self.get_raw_value(key))

    def get_raw_value(self, key):
        return self.__get_line(key)['value']

    def get_comment(self, key):
        return self.__get_line(key)['comment'].lstrip()

    def get_keys(self):
        return [a['key'] for a in self]

    def has_key(self, key):
        return bool(key in self.get_keys())

    def get_items(self):
        return [(a['key'], self.__format_value(a['value'])) for a in self]


class QueueFunction(object):

    def __init__(self, n_max, func, *args, **kargs):
        self.func = func
        self.n_max = n_max
        self.res = []
        self.queue = []
        self.args = args
        self.kargs = kargs

    def check_queue(self, n_max):
        if len(self.queue) >= n_max:
            # print 'Processing queue ...'
            self.res.append(self.func(self.queue, *self.args, **self.kargs))
            self.queue = []

    def add(self, a):
        self.queue.append(a)
        self.check_queue(self.n_max)

    def done(self):
        self.check_queue(1)
        return np.vstack(self.res)


class SimpleConfig(object):

    def __init__(self):
        if not hasattr(self, 'config'):
            self.config = dict()

    def __getattr__(self, key):
        if key == 'config':
            try:
                self.config
            except Exception:
                raise AttributeError()

        assert key in self.config
        return self.get(key)

    def add(self, key, default, type):
        self.config[key] = [default, type]

    def get(self, key):
        return self.config[key][0]

    def set(self, key, value):
        assert key in self.config
        type_fct = self.config[key][1]
        if value == 'None' and type_fct is not str:
            self.config[key][0] = None
        else:
            if type_fct == bool:
                type_fct = str2bool

            self.config[key][0] = type_fct(value)

    def parse_dict(self, dict, check_existing=False):
        for key, value in dict.items():
            if not check_existing and key not in self.config:
                continue
            self.set(key, value)

    def parse_from_file(self, filename, section, check_existing=True):
        config = configparser.RawConfigParser()
        config.read(filename)
        items = dict(config.items(section))
        self.parse_dict(items, check_existing=check_existing)

    def copy(self):
        new = self.__class__()
        new.config = copy.deepcopy(self.config)

        return new


def bin_data(x, y, nbins, stat='mean'):
    """Use stats.binned_statistic to bin data

    Args:
        x (array): values that will be binned
        y (array): The values on which the statistic will be computed
        nbins (TYPE): The number of bins or the bins if sequence.

    Returns:
        (array, array, array): The bins, the mean of y for each bins, the std pf y for each bins.
    """
    m, bins_edges, _ = stats.binned_statistic(x, y, stat, nbins)
    s, _, _ = stats.binned_statistic(x, y, np.std, nbins)
    bins = np.array([(a + b) / 2. for a, b in pairwise(bins_edges)])

    return bins, m, s


def plot_binned(x, y, nbins, **kargs):
    ''' Plot binned data '''
    bins, m, s = bin_data(x, y, nbins)
    plt.errorbar(bins, m, s / np.sqrt(nbins), **kargs)


def safe_sum(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    return a + b


def safe_diff(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    return a - b


def safe_decode_bytes(s):
    if isinstance(s, (bytes, np.bytes_)):
        return s.decode('UTF-8')
    elif isinstance(s, list):
        return [safe_decode_bytes(k) for k in s]
    return s


def nanaverage(d, w, axis=None):
    return np.nansum(d * w, axis=axis) / np.nansum(w, axis=axis)


def linear_fct(p1, p2):
    a = (p2[1] - p1[1]) / float(p2[0] - p1[0])
    b = p1[1] - a * p1[0]
    return lambda x: a * x + b


def freq_to_z(freq):
    '''Convert 21 cm line frequency to redshift'''
    return (f21 / freq).decompose().value - 1


def z_to_freq(z):
    return f21.value / (z + 1)


def delay_to_k(delay, z, unit=u.Mpc):
    '''Convert delay to inverse co-moving distance in h Mpc^-1 '''
    return 2 * np.pi * delay / freqency_to_comoving_distance(z, unit=unit)


def k_to_delay(k, z, unit=u.Mpc):
    '''Convert delay to inverse co-moving distance in h Mpc^-1 '''
    return k * freqency_to_comoving_distance(z, unit=unit) / (2 * np.pi)


def l_to_k(ll, z, unit=u.Mpc):
    return ll / angular_to_comoving_distance(z, unit=unit)


def k_to_l(k, z, unit=u.Mpc):
    return k * angular_to_comoving_distance(z, unit=unit)


def angular_to_comoving_distance(z, unit=u.Mpc):
    '''Return angular to co-moving distance conversion factor'''
    return cosmo.comoving_transverse_distance(z).to(unit).value * cosmo.h


def freqency_to_comoving_distance(z, unit=u.Mpc):
    '''Return frequency to co-moving distance conversion factor'''
    return ((const.c * (1 + z) ** 2) / (cosmo.H(z) * f21)).to(unit * u.Hz ** -1).value * cosmo.h


def wedge_fct(theta, z, k_per):
    '''Delay line for a source at theta radians from the phase center, From Dillon 2013 '''
    dm = cosmo.comoving_transverse_distance(z)
    return np.sin(theta) * (dm * cosmo.H(z) / (const.c * (1 + z))).decompose().value * k_per


def most_common_element(arr):
    # Get unique elements and their counts in the array
    unique_elements, counts = np.unique(arr, return_counts=True)

    # Find the index of the element with the maximum count
    most_common_index = np.argmax(counts)
    
    return unique_elements[most_common_index]


def robust_du(uu, vv):
    du = most_common_element(np.diff(np.unique(abs(uu))))
    dv = most_common_element(np.diff(np.unique(abs(vv))))

    return np.max([du, dv])

def nudft(x, y, M=None, w=None, dx=None):
    """Non uniform discrete Fourier transform

    Args:
        x (array): x axis
        y (array): y axis
        M (int, optional): Number of Fourier components that will be computed, default to len(x)
        w (array, optional): Tapper

    Returns:
        (array, array): k modes, Fourier transform of y
    """
    if M is None:
        M = len(x)

    if dx is None:
        dx = robust_freq_width(x)

    if w is not None:
        y = y * w

    df = 1 / (dx * M)
    k = df * np.arange(-(M // 2), M - (M // 2))

    X = np.exp(2 * np.pi * 1j * k * x[:, np.newaxis])

    return k, np.tensordot(y, X.conj().T, axes=[0, 1]).conj().T


def lssa_cov(x, C, M, dx=None):
    if dx is None:
        dx = robust_freq_width(x)

    W = np.linalg.pinv(C)

    k = np.fft.fftshift(np.fft.fftfreq(M, float(dx)))

    A = np.exp(-2. * np.pi * 1j * k * x[:, np.newaxis]) / len(x)

    return np.linalg.pinv(np.dot(np.dot(A.real.T, W), A.real))


def lssa_diag_cov(x, d, M=None, dx=None):
    if M is None:
        M = len(x)

    if dx is None:
        dx = robust_freq_width(x)

    k = np.fft.fftshift(np.fft.fftfreq(M, float(dx)))
    A = np.exp(-2. * np.pi * 1j * k * x[:, np.newaxis]) / len(x)

    t = np.tensordot((A.conj().T[:, :, None] / d[None, :]), A, axes=(1, 0)).transpose(0, 2, 1)
    diag_t = 1 / abs(t[np.arange(M), np.arange(M)])

    return k, diag_t


def do_weighted_lssa(A, y, w):
    n_x, n_k = A.shape
    n_modes = y.shape[1]

    w = w.astype(np.complex128)
    w.imag = w.real

    d = np.zeros((n_k, n_modes), dtype=np.complex128)

    for i in xrange(n_modes):
        C = diags(w[:, i])
        A_C = C.T.dot(A).T
        Y = np.dot(np.linalg.pinv(np.dot(A_C, A)), A_C)
        d[:, i] = np.dot(y[:, i].T, Y.T).T

    return d


def lssa(x, y, M, w=None, weights=None, dx=None):
    """Least-squares spectral analysis

    Args:
        x (array): x axis
        y (array): y axis
        M (int, optional): Number of Fourier components that will be computed, default to len(x)
        w (array, optional): Tapper
        weights (array, optional): Weights

    Returns:
        (array, array): k modes, Fourier transform of y
    """
    if dx is None:
        dx = robust_freq_width(x)

    k = np.fft.fftshift(np.fft.fftfreq(M, float(dx)))

    if w is not None:
        y = y * w  # [:, np.newaxis]

    A = np.exp(-2. * np.pi * 1j * k * x[:, np.newaxis]) / M

    if weights is None:
        Y = np.dot(np.linalg.pinv(np.dot(A.conj().T, A)), A.conj().T)
        d = np.tensordot(y.conj().T, Y.conj().T, axes=[1, 0]).conj().T
    else:
        d = do_weighted_lssa(A, y, weights)

    return k, d


def ufft(x, y, M=None, w=None, weights=None, dx=None):
    """SImple FFT

    Args:
        x (array): x axis
        y (array): y axis
        M (int, optional): Number of Fourier components that will be computed, default to len(x)
        w (array, optional): Tapper
        weights (array, optional): Weights

    Returns:
        (array, array): k modes, Fourier transform of y
    """
    if M is None:
        M = len(x)

    if dx is None:
        dx = robust_freq_width(x)

    k = np.fft.fftshift(np.fft.fftfreq(M, float(dx)))

    if w is not None:
        y = y * w  # [:, np.newaxis]

    d = np.fft.fftshift(fft(np.fft.fftshift(y), axis=0, n=M))

    return k, d


def get_delay(freqs, M=None, dx=None, half=True):
    ''' Convert frequencies to delay '''
    if dx is None:
        dx = robust_freq_width(freqs)
    if M is None:
        M = len(freqs)

    df = 1 / (dx * M)
    delay = df * np.arange(-(M // 2), M - (M // 2))

    if half:
        M = len(delay)
        delay = delay[M // 2 + 1:]

    return delay


def delay_transform_cube(freqs, ft_cube, M=None, window=None, dx=None,
                         method='nudft', weights=None, rmean_axis=None):
    '''Frequency -> delay transform ft_cube'''
    if method == 'nudft':
        delay, dft_cube = nudft(freqs, rmean(ft_cube, axis=rmean_axis), M=M, w=window, dx=dx)
    elif method == 'lssa':
        delay, dft_cube = lssa(freqs, rmean(ft_cube, axis=rmean_axis), M=M, w=window, dx=dx)
    elif method == 'wlssa':
        delay, dft_cube = lssa(freqs, rmean(ft_cube, axis=rmean_axis), M=M, w=window, dx=dx, weights=weights)
    elif method == 'ufft':
        delay, dft_cube = ufft(freqs, rmean(ft_cube, axis=rmean_axis), M=M, w=window, dx=dx, weights=weights)
    else:
        print("'method' should be one of: nudft, lssa, wlssa, ufft")
    # dft_cube[delay == 0] = np.mean(ft_cube, axis=0)

    return delay, dft_cube


def vis_to_img(vis_map, axes=None):
    if axes is not None:
        norm = np.prod(np.array(vis_map.shape)[list(axes)])
    else:
        norm = np.prod(vis_map.shape)

    return np.fft.ifftshift(ifft2(np.fft.fftshift(vis_map, axes=axes), axes=axes), axes=axes) * norm


def img_to_vis(cart_map, axes=None):
    if axes is not None:
        norm = 1 / float(np.prod(np.array(cart_map.shape)[list(axes)]))
    else:
        norm = 1 / float(np.prod(cart_map.shape))

    return np.fft.fftshift(fft2(np.fft.ifftshift(cart_map, axes=axes), axes=axes), axes=axes) * norm


def ft_cart_map(cart_map, res, umin, umax):
    ''' FT cart_map, keep non-zero visibilities between umin and umax.

    Returns:
        uu (n_vis), vv (n_vis), vis (n_vis)'''
    uu, vv, idx = get_ungrid_vis_idx(cart_map.shape, res, umin, umax)
    vis = img_to_vis(cart_map)

    return uu.flatten(), vv.flatten(), vis[idx].flatten()


def ft_cart_cube(cart_cube, res, umin, umax):
    ft_cube = []
    uu, vv, idx = get_ungrid_vis_idx(cart_cube[0].shape, res, umin, umax)
    for i in range(cart_cube.shape[0]):
        ft = img_to_vis(cart_cube[i])
        ft_cube.append(ft[idx].flatten())

    return uu.flatten(), vv.flatten(), np.array(ft_cube)


def get_uv_grid(shape, res):
    g_u = np.arange(-shape[0] // 2, shape[0] // 2) * 1 / (res * shape[0])
    g_v = np.arange(-shape[1] // 2, shape[1] // 2) * 1 / (res * shape[1])
    return np.meshgrid(g_u, g_v)


def get_regrid_vis_idx(uu, vv, res, shape):
    g_uu, g_vv = get_uv_grid(shape, res)

    # index of gridded vis:
    x = (np.round(g_uu, decimals=4) + 1e-6 * np.round(g_vv, decimals=4)).flatten()

    # index of non-gridded vis:
    y = np.round(uu, decimals=4) + 1e-6 * np.round(vv, decimals=4)

    idx_x = np.argsort(x)
    sorted_x = x[idx_x]
    idx_y = np.searchsorted(sorted_x, y)
    idx = idx_x[idx_y]

    return g_uu, g_vv, idx


def get_ungrid_vis_idx(shape, res, umin, umax):
    g_uu, g_vv = get_uv_grid(shape, res)

    g_ru = np.sqrt(g_uu ** 2 + g_vv ** 2)

    idx = (g_ru >= umin) & (g_ru <= umax)

    return g_uu[idx], g_vv[idx], idx


def regrid_vis(vis, uu, vv, res, shape):
    ''' Regrid vis to a regular grid'''
    g_uu, g_vv, idx = get_regrid_vis_idx(uu, vv, res, shape)
    g_vis = np.zeros_like(g_uu, dtype=np.complex128).flatten()
    g_vis[idx] = vis
    g_vis = g_vis.reshape(*g_uu.shape)

    return g_uu, g_vv, g_vis


def sort_by_sb(files):
    key_fct = lambda a: re.search('SB([0-9]{3})', a).groups()[0]
    return sorted(files, key=key_fct)


def get_fits_key(files, key):
    return np.array([FastHeaderReader(f, keys=[key]).get_value(key) for f in files])


def sort_by_fits_key(files, key):
    values = get_fits_key(files, key)
    files_values = sorted(list(zip(files, values)), key=lambda k: k[1])
    return list(zip(*files_values))[0]


def slice2index(slices):
    index = []
    for point in zip(*[[k.start, k.stop] for k in slices]):
        index.extend(point)
    return index


def resize(array, shape, padding_mode='center', output_index=False):
    '''
    Resize the array 'array' to match shape 'shape'.

    For each dimension, if shape is smaller than array size, array is cut
    depending of padding_mode

    Padding mode: 'center', 'right', 'left'.

    If padding is impair, pad more to the left than to the right.

    :param array:
    :param shape:
    :param padding_mode:

    @UT: TODO:
    '''
    if array.ndim != len(shape):
        raise ValueError("array and like should have the same dimension")

    array = np.asarray(array)

    padding_slice = []
    index_slice = []

    for dim in range(array.ndim):
        diff = (array.shape[dim] - shape[dim])
        if padding_mode == 'right':
            nleft = int(abs(diff))
            nright = None
        elif padding_mode == 'left':
            nleft = None
            nright = int(-abs(diff))
        else:
            nleft = int(abs(np.floor(diff / 2.)))
            nright = int(-abs(np.ceil(diff / 2.)))
        if nleft == 0:
            nleft = None
        if nright == 0:
            nright = None
        if diff > 0:
            index_slice.append(slice(nleft, nright))
            padding_slice.append(slice(None))
        elif diff < 0:
            index_slice.append(slice(None))
            padding_slice.append(slice(nleft, nright))
        else:
            index_slice.append(slice(None))
            padding_slice.append(slice(None))

    # check if we need to reallocate (i.e., if new data are needed)
    if padding_slice == [slice(None)] * array.ndim:
        res = array[index_slice]
    else:
        res = np.zeros(shape, dtype=array.dtype)

        res[padding_slice] = array[index_slice]

    if output_index is True:
        return res, slice2index(padding_slice), slice2index(index_slice)
    return res


def get_random(seed=None):
    if seed is None:
        return np.random
    return np.random.RandomState(seed)


def int_pairing(a, b):
    ''' Cantor pairing function '''
    return 0.5 * (a + b) * (a + b + 1) + b


def get_selection_index(ll1, mm1, ll2, mm2, keep_order=False):
    ''' Return the index of all modes (ll2, mm2) into (ll, mm).'''
    x = np.array([l + 1 / (m + 1.) for l, m in zip(ll1, mm1)])

    if keep_order:
        y = np.array([l + 1 / (m + 1.) for l, m in zip(ll2, mm2)])
        idx_x = np.argsort(x)
        sorted_x = x[idx_x]
        idx_y = np.searchsorted(sorted_x, y)
        idx = idx_x[idx_y]
    else:
        y = np.unique(np.array([l + 1 / (m + 1.) for l, m in zip(ll2, mm2)]))
        idx = np.where(np.in1d(x, y, assume_unique=False))[0]

    return idx


def plot_cart_map(cart_map, theta_max, ax=None, title=None, theta_lines=[], show_degrees=False, **kargs):
    if ax is None:
        fig, ax = plt.subplots()

    cbs = ColorbarSetting(ColorbarOutterPosition())

    if show_degrees:
        extent = np.degrees(np.array([-theta_max, theta_max, -theta_max, theta_max]))
    else:
        extent = np.array([-theta_max, theta_max, -theta_max, theta_max])

    im_mappable = ax.imshow(cart_map, extent=extent, **kargs)
    cbs.add_colorbar(im_mappable, ax)
    if show_degrees:
        ax.set_xlabel('l [deg]')
        ax.set_ylabel('m [deg]')
    else:
        ax.set_xlabel('l')
        ax.set_ylabel('m')

    if title is not None:
        ax.set_title(title)

    for theta in theta_lines:
        if not show_degrees:
            theta = np.sin(np.radians(theta))
        ax.add_artist(plt.Circle([0, 0], theta, ls='--', fc=None, ec=lblack, fill=False))


class ColorbarInnerPosition(object):

    def __init__(self, orientation="horizontal", width="5%", height="50%", location=1, pad=0.5,
                 tick_position=None):
        '''
        width, height: inch if number, percentage of parent axes if string (like '5%')
        pad: points
        location are :
        'upper right' : 1,
        'upper left' : 2,
        'lower left' : 3,
        'lower right' : 4,
        'right' : 5,
        'center left' : 6,
        'center right' : 7,
        'lower center' : 8,
        'upper center' : 9,
        'center' : 10,
        '''
        self.orientation = orientation
        if orientation == 'vertical':
            self.width = width
            self.height = height
            if tick_position is None:
                tick_position = 'left'
        else:
            self.width = height
            self.height = width
            if tick_position is None:
                tick_position = 'bottom'
        self.location = location
        self.pad = pad
        self.tick_position = tick_position

    def get_cb_axes(self, ax):
        cax = inset_axes(ax, width=self.width, height=self.height, loc=self.location, borderpad=self.pad)
        return cax

    def post_creation(self, colorbar):
        if self.orientation == 'vertical':
            if self.tick_position == 'left':
                colorbar.ax.yaxis.set_ticks_position(self.tick_position)
                colorbar.ax.yaxis.set_label_position(self.tick_position)
        else:
            if self.tick_position == 'top':
                colorbar.ax.xaxis.set_ticks_position(self.tick_position)
                colorbar.ax.xaxis.set_label_position(self.tick_position)

    def get_orientation(self):
        return self.orientation


class ColorbarOutterPosition(object):

    def __init__(self, width="5%", pad="3%", location="right"):
        ''''
        width: inch if number, percentage of parent axes if string (like '5%')
        pad: inch if number, percentage of parent axes if string (like '5%')
        location: top, bottom, right, left
        '''
        self.width = width
        self.pad = pad
        self.location = location

    def get_cb_axes(self, ax):
        divider = make_axes_locatable(ax)
        cax = divider.append_axes(self.location, self.width, pad=self.pad)
#        cax.axis[:].toggle(ticklabels=False)
#        cax.axis[self.location].toggle(ticklabels=True)
        return cax

    def get_orientation(self):
        if self.location in ['left', 'right']:
            return "vertical"
        return "horizontal"

    def post_creation(self, colorbar):
        pass


class ColorbarSetting(object):

    def __init__(self, cb_position=None, ticks_locator=None, ticks_formatter=None, cmap='jet'):
        if cb_position is None:
            cb_position = ColorbarOutterPosition()
        self.cb_position = cb_position
        self.ticks_locator = ticks_locator
        self.ticks_formatter = ticks_formatter
        self.cmap = cmap

    def add_colorbar(self, mappable, ax):
        fig = ax.get_figure()
        cb = fig.colorbar(mappable, ticks=self.ticks_locator, format=self.ticks_formatter,
                          orientation=self.cb_position.get_orientation(), cax=self.cb_position.get_cb_axes(ax))
        self.cb_position.post_creation(cb)
        if not hasattr(fig, '_plotutils_colorbars'):
            fig._plotutils_colorbars = dict()
        fig._plotutils_colorbars[ax] = cb
        return cb

    def get_cmap(self):
        return self.cmap


class LogScalarFormatter(ticker.Formatter):

    def __init__(self, min_x):
        self.min_x = min_x

    def __call__(self, x, pos):
        decimalplaces = int(np.ceil(np.maximum(-np.log10(x), 0)))

        formatstring = '{{:.{:1d}f}}'.format(decimalplaces)
        s = np.array(formatstring.format(x))
        s[x <= self.min_x] = ''

        return s


class Cache(object):

    def __init__(self, fct, hash_fct=None):
        self.fct = fct
        self.invalidate()
        if hash_fct is None:
            self.hash_fct = self.get_hash
        else:
            self.hash_fct = hash_fct

    def get_hash(self, *args, **kargs):
        args_check = []
        for i, arg in enumerate(args):
            if isinstance(arg, (list, np.ndarray)):
                arg = tuple(arg)
            args_check.append(arg)
        return tuple(args_check + list(kargs.items()))

    def invalidate(self):
        self.cache = dict()

    def get(self, *args, **kargs):
        args_hash = self.hash_fct(*args, **kargs)
        if args_hash not in self.cache:
            self.cache[args_hash] = self.fct(*args, **kargs)
        return self.cache[args_hash]


class AbstractFct(object):

    def __init__(self, p0):
        self.p0 = p0

    @staticmethod
    def fct(x, p):
        pass

    def __call__(self, x):
        return self.fct(x, *self.p0)

    def get_text_equ(self, label=''):
        return "None"

    def error(self, x, y):
        return (self(x) - y).std(ddof=1) / np.sqrt(len(x))

    @staticmethod
    def fit(x, y):
        pass


class LinearFct(AbstractFct):

    def __init__(self, a, b, ea=None, eb=None):
        self.a = a
        self.b = b
        self.ea = ea
        self.eb = eb
        AbstractFct.__init__(self, [a, b])

    @staticmethod
    def fct(x, a, b):
        return a * np.asarray(x) + b

    def inverse_fct(self, y, a, b):
        if a != 0:
            return (y - b) / a
        return 0

    def get_text_equ(self, label='y'):
        return "$%s = %.5f x + %.2f$" % (label, self.a, self.b)

    @staticmethod
    def fit(x, y, sigma=None):
        x = np.asarray(x)
        y = np.asarray(y)

        w = None
        if sigma is not None:
            w = 1 / np.array(sigma)
        b, a = np.polynomial.polynomial.polyfit(x, y, 1, w=w)

        fct = LinearFct(a, b)
        RMSE = (fct(x) - y).std(ddof=2)
        Sxx = (x ** 2).sum() - len(x) * x.mean() ** 2
        ea = RMSE / np.sqrt(Sxx)
        eb = RMSE * np.sqrt(1 / len(x) + x.mean() ** 2 / Sxx)

        return LinearFct(a, b, ea=ea, eb=eb)


def polynomial_fit(x, y, y_err, degree):
    # Perform the polynomial fit
    coefficients = np.polyfit(x, y, degree, w=1/y_err)

    # Return the polynomial function
    def fitted_function(x):
        return np.polyval(coefficients, x)

    return fitted_function

def polynomial_fit_log(x, y, y_err, degree):
    # Take the logarithm of x, y, and y_err
    log_x = np.log(x)
    log_y = np.log(y)
    log_y_err = y_err / y  # Errors in log scale are proportional to y

    # Perform the polynomial fit in log scale
    log_coefficients = np.polyfit(log_x, log_y, degree, w=1/log_y_err)

    # Return the fitted function in original scale
    def fitted_function(x):
        return np.exp(np.polyval(log_coefficients, np.log(x)))

    return fitted_function


class PowerFct1(AbstractFct):

    def __init__(self, a, b, ea=None, eb=None):
        self.a = a
        self.b = b
        self.ea = ea
        self.eb = eb
        AbstractFct.__init__(self, [a, b])

    @staticmethod
    def fct(x, a, b):
        return b * np.asarray(x) ** a

    @staticmethod
    def fit(x, y, sigma=None):
        logx = np.log(x)
        logy = np.log(y)
        linfct = LinearFct.fit(logx, logy)
        return PowerFct1(linfct.a, np.exp(linfct.b), ea=linfct.ea, eb=np.abs(1 / linfct.b) * linfct.eb)


def rmean(data, axis=0):
    '''Remove the mean in direction axis'''
    return data - np.mean(data, axis=axis)


def is_number(x):
    return isinstance(x, (int, float, complex))


def gaussian_fwhm_to_sigma(fwhm):
    return 1 / (2. * np.sqrt(2 * np.log(2))) * fwhm


def gaussian_beam(thetas, fwhm):
    # fwhm in radians, centered at NP
    sigma = gaussian_fwhm_to_sigma(fwhm)

    gaussian_sph = np.exp(-(0.5 * (thetas / sigma) ** 2))

    return gaussian_sph


def pairwise(iterable):
    '''s -> (s0,s1), (s1,s2), (s2, s3), ...'''
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))


def nwise(iterable, n):
    "s -> (s0,s1, s2), (s1,s2, s3), (s2, s3, s4), ..."
    ilist = itertools.tee(iterable, n)
    for i, it in enumerate(ilist):
        for i in range(i):
            next(it, None)
    return list(zip(*ilist))


def _get_next_previous_oddeven(n, testeven, next=True):
    if isinstance(n, np.ndarray):
        if not n.dtype == int:
            n = n.astype(int)
        if (n % 2 == testeven).any():
            m = n.copy()
            if next:
                m[(n % 2 == testeven)] += 1
            else:
                m[(n % 2 == testeven)] -= 1
            return m
        return n
    else:
        if not isinstance(n, int):
            n = int(n)
        if n % 2 == testeven:
            if next:
                return n + 1
            return n - 1
        return n


def get_next_even(n):
    return _get_next_previous_oddeven(n, True)


def get_next_odd(n):
    return _get_next_previous_oddeven(n, False)


def get_previous_even(n):
    return _get_next_previous_oddeven(n, True, next=False)


def get_previous_odd(n):
    return _get_next_previous_oddeven(n, False, next=False)


def is_odd(num):
    return num & 0x1


def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")


def str2floatlist(s):
    s = s.strip('([)]')
    return [float(k.strip()) for k in s.split(',')]


def sinc2_beam(thetas, fwhm, null_below_horizon=True, n_sidelibe=None):
    # fwhm in radians, centered at NP
    hwhm = fwhm / 2.
    sinc_sph = (np.sin((thetas * 1.4 / hwhm)) / (thetas * 1.4 / hwhm)) ** 2

    if null_below_horizon:
        sinc_sph[thetas > np.pi / 2.] = 0

    if n_sidelibe is not None:
        sinc_sph[thetas > hwhm / 1.4 * np.pi * (n_sidelibe + 1)] = 0

    return sinc_sph


def cos2_beam(thetas, fwm):
    """
    Computes an achromatic primary beam pattern based on a cos^2(theta) dependence.

    The beam is maximal at the boresight (theta = 0), smoothly falls off with increasing 
    angle, and is null for theta > pi/2 (angles beyond the horizon).

    Parameters:
    -----------
    thetas : numpy.ndarray
        Array of angles from the boresight (in radians), where:
        - theta = 0 corresponds to the boresight (directly overhead).
        - theta = pi/2 corresponds to the horizon.
        - Values beyond pi/2 are automatically set to 0.
    
    fwm : float
        Dummy parameter representing the full width at maximum (FWM).
        This parameter is not used in the computation but included for compatibility.

    Returns:
    --------
    numpy.ndarray
        The primary beam pattern values corresponding to the input angles.
        - The values are normalized, with the maximum at the boresight (cos^2(0) = 1).
        - The values are set to 0 for theta > pi/2.
    """
    beam = np.cos(thetas) ** 2
    beam[thetas > np.pi / 2] = 0
    return beam


def bessel_beam(thetas, fwhm):
    beam = (2 / np.pi * fwhm / thetas * bessel_j1(np.pi * thetas / fwhm)) ** 2
    beam[thetas == 0] = 1
    return beam


def tophat_beam(thetas, width):
    # width in radians, centered at NP
    return (thetas <= width / 2.)


def get_beam(thetas, beam_type, fwhm, n_sidelobe):
    if beam_type == 'gaussian':
        beam = gaussian_beam(thetas, fwhm)
    elif beam_type == 'sinc2':
        beam = sinc2_beam(thetas, fwhm, n_sidelibe=n_sidelobe)
    elif beam_type == 'bessel':
        beam = bessel_beam(thetas, fwhm)
    elif beam_type == 'tophat':
        beam = tophat_beam(thetas, fwhm)
    elif beam_type == 'cos2':
        beam = cos2_beam(thetas, fwhm)
    else:
        return None

    return beam


@functools.lru_cache(maxsize=20, typed=False)
def get_beam_cart(res, img_shape, beam_type, fwhm, n_sidelobe=None):
    nx, ny = img_shape

    thxval = res * np.arange(-nx / 2., nx / 2.)
    thyval = res * np.arange(-ny / 2., ny / 2.)
    thx, thy = np.meshgrid(thxval, thyval)

    return get_beam(np.sqrt(thx ** 2 + thy ** 2), beam_type, fwhm, n_sidelobe)


@functools.lru_cache(maxsize=20, typed=False)
def generate_2d_window(window_name, nx, circular=False):
    w = get_window(window_name, nx)
    if circular:
        m = (nx - 1) // 2
        x = np.linspace(-m, m, nx)
        xx, yy = np.meshgrid(x, x)
        w2d = np.interp(np.sqrt(xx ** 2 + yy ** 2), x, w)
    else:
        w2d = np.outer(w, w)

    return w2d
  

def robust_std_idl(inputData, Zero=False, axis=None, dtype=None):
    """
    Robust estimator of the standard deviation of a data set.
    Based on the robust_sigma function from the AstroIDL User's Library.

    Args:
        inputData (TYPE): Description
        Zero (bool, optional): Description
        axis (None, optional): Description
        dtype (None, optional): Description
    """

    __epsilon = 1.0e-20

    if axis is not None:
        fnc = lambda x: robust_std_idl(x, dtype=dtype)
        sigma = np.apply_along_axis(fnc, axis, inputData)
    else:
        data = inputData.ravel()
        if type(data).__name__ == "MaskedArray":
            data = data.compressed()
        if dtype is not None:
            data = data.astype(dtype)

        if Zero:
            data0 = 0.0
        else:
            data0 = np.median(data)
        maxAbsDev = np.median(np.abs(data - data0)) / 0.6745
        if maxAbsDev < __epsilon:
            maxAbsDev = (np.abs(data - data0)).mean() / 0.8000
        if maxAbsDev < __epsilon:
            sigma = 0.0
            return sigma

        u = (data - data0) / 6.0 / maxAbsDev
        u2 = u**2.0
        good = np.where(u2 <= 1.0)
        good = good[0]
        if len(good) < 3:
            print("WARNING:  Distribution is too strange to compute standard deviation")
            sigma = -1.0
            return sigma

        numerator = ((data[good] - data0)**2.0 * (1.0 - u2[good])**2.0).sum()
        nElements = (data.ravel()).shape[0]
        denominator = ((1.0 - u2[good]) * (1.0 - 5.0 * u2[good])).sum()
        sigma = nElements * numerator / (denominator * (denominator - 1.0))
        if sigma > 0:
            sigma = np.sqrt(sigma)
        else:
            sigma = 0.0

    return sigma


def robust_std(x, axis=None):
    '''
    Robust estimate of std of noise in df/f
    '''
    if np.iscomplexobj(x):
        std_r = robust_std(x.real, axis=axis)
        std_i = robust_std(x.imag, axis=axis)

        return np.sqrt(std_r ** 2 + std_i ** 2)
    if axis is not None:
        fnc = lambda x: robust_std(x)
        return np.apply_along_axis(fnc, axis, x)
    else:
        # first pass removing big pos peaks
        # x = x[x < 1.5 * np.abs(x.min(axis=axis))]
        MAD = np.median(np.abs(x - np.median(x)))
        rstd = 1.4826 * MAD

        # # second pass removing remaining pos and neg peaks
        if rstd != 0:
            x = x[abs(x - np.median(x)) < 3 * rstd]
            MAD = np.median(np.abs(x - np.median(x)))

        return 1.4826 * MAD


def mad(x, axis=None):
    if np.iscomplexobj(x):
        return np.sqrt(mad(x.real, axis=axis) ** 2 + mad(x.imag, axis=axis) ** 2)
    if axis is not None:
        center = np.apply_over_axes(np.nanmedian, x, axis)
    else:
        center = np.nanmedian(x)
    return np.nanmedian(abs(x - center), axis=axis) / 0.6735


def sph2cart(theta, phi, r=None):
    """Convert spherical coordinates to 3D cartesian
    theta, phi, and r must be the same size and shape, if no r is provided
            then unit sphere coordinates are assumed (r=1)
    theta: colatitude/elevation angle, 0(north pole) =< theta =< pi (south pole)
    phi: azimuthial angle, 0 <= phi <= 2pi
    r: radius, 0 =< r < inf
    returns X, Y, Z arrays of the same shape as theta, phi, r
    see: http://mathworld.wolfram.com/SphericalCoordinates.html
    """
    if r is None:
        r = np.ones_like(theta)  # if no r, assume unit sphere radius

    # elevation is pi/2 - theta
    # azimuth is ranged (-pi, pi]
    X = r * np.cos((np.pi / 2.) - theta) * np.cos(phi - np.pi)
    Y = r * np.cos((np.pi / 2.) - theta) * np.sin(phi - np.pi)
    Z = r * np.sin((np.pi / 2.) - theta)

    return X, Y, Z


def cart2sph(X, Y, Z):
    """Convert 3D cartesian coordinates to spherical coordinates
    X, Y, Z: arrays of the same shape and size
    returns r: radius, 0 =< r < inf
            phi: azimuthial angle, 0 <= phi <= 2pi
            theta: colatitude/elevation angle, 0(north pole) =< theta =< pi (south pole)
    see: http://mathworld.wolfram.com/SphericalCoordinates.html
    """
    r = np.sqrt(X**2. + Y**2. + Z**2.)
    phi = np.arctan2(Y, X) + np.pi  # convert azimuth (-pi, pi] to phi (0, 2pi]
    theta = np.pi / 2. - np.arctan2(Z, np.sqrt(X**2. + Y**2.))  # convert elevation [pi/2, -pi/2] to theta [0, pi]

    return r, phi, theta


class OnlineVariance(object):
    """
    Welford's algorithm computes the sample variance incrementally.

    Based on http://stackoverflow.com/questions/5543651/computing-standard-deviation-in-a-stream
    """

    def __init__(self):
        self.n = 0
        self.mean = 0.
        self._M2 = 0.0

    def add(self, data):
        self.n += 1
        self.delta = data - self.mean
        self.mean += self.delta / self.n
        self._M2 += self.delta * (data - self.mean)
        self.variance = self._M2 / (self.n)

    @property
    def std(self):
        return np.sqrt(self.variance)


class OnlineVarianceComplex(object):

    def __init__(self):
        self.real = OnlineVariance()
        self.imag = OnlineVariance()

    def add(self, data):
        self.real.add(data.real)
        self.imag.add(data.imag)


def fill_gaps(cube, gaps, fill_with=np.nan):
    '''Fill cube missing frequencies with NaN '''
    alm_filled = []
    for i, alm in enumerate(cube):
        alm_filled.append(alm)
        if i < len(gaps) and gaps[i] > 0:
            alm_filled.extend([np.ones_like(cube[0]) * fill_with] * gaps[i])

    return np.array(alm_filled)


def get_gaps(freqs):
    '''Return numbers of missing frequencies'''
    df = robust_freq_width(freqs)
    return np.array(np.round(np.diff(freqs) / df) - 1).astype(int)


def get_freqs_gaps(freqs):
    '''Return missing frequencies '''
    df = robust_freq_width(freqs)
    gaps = np.array(np.round(np.diff(freqs) / df) - 1).astype(int)
    freqs_gaps = []
    for i, freq in enumerate(freqs):
        if i < len(gaps) and gaps[i] > 0:
            freqs_gaps.extend(freq + df * (np.arange(gaps[i]) + 1))
            # freqs_gaps.extend([np.ones_like(alm_cube[0]) * fill_with] * gaps[i])

    return np.array(freqs_gaps)


def get_freq_slice(freqs, freq_start, freq_end):
    if freq_start > np.max(freqs) and freq_end > np.max(freqs):
        return slice(0, 0)

    if freq_start < np.min(freqs) and freq_end < np.min(freqs):
        return slice(0, 0)

    i_start = np.nonzero(freqs >= freq_start)[0][0]
    if freq_end >= np.max(freqs):
        i_end = len(freqs)
    else:
        i_end = np.nonzero(freqs <= freq_end)[0][-1] + 1

    return slice(i_start, i_end)


def robust_freq_width(freqs):
    '''Return frequency width, robust to gaps in freqs'''
    dfs = np.diff(freqs)
    m, idx, c = np.unique(np.round(dfs * 1e-3) * 1e3, return_counts=True, return_inverse=True)
    return dfs[np.where(idx == np.argmax(c))].mean()


def freq_to_index(freqs, start=1):
    '''Return index separated by frequency width '''
    df = robust_freq_width(freqs)
    return np.round((freqs - freqs[0]) / (df)).astype(int) + start


def get_weights_outliers(freqs, weights, ratio=0.2, poly_fit_deg=1):
    mw = weights.mean(axis=1)
    # First pass to filter obvious outiliers
    if mad(mw) != 0:
        mask = abs(mw - np.median(mw)) < 5 * mad(mw)
    else:
        mask = slice(None)
    mw_fct = np.poly1d(np.polyfit(freqs[mask], mw[mask], poly_fit_deg))

    return (mw / mw_fct(freqs)) < ratio


def get_sefd_outliers(freqs, sefd, ratio=0.75, poly_fit_deg=2, min_ratio=0.2):
    # First pass to filter obvious outiliers
    if mad(sefd) != 0:
        mask = abs(sefd - np.median(sefd)) < 5 * mad(sefd)
    else:
        mask = slice(None)
    mw_fct = np.poly1d(np.polyfit(freqs[mask], sefd[mask], poly_fit_deg))

    return ((mw_fct(freqs) / sefd) < ratio) | ((sefd / mw_fct(freqs)) < min_ratio)


def filter_outliers(array, idx_outliers):
    return array[~idx_outliers]


def progress_report(n):
    t = time.time()

    def report(i):
        print("\r", end=' ')
        eta = ""
        if i > 0:
            remaining = (np.round((time.time() - t) / float(i) * (n - i)))
            eta = "(ETA: %s)" % time.strftime("%H:%M:%S", time.localtime(time.time() + remaining))
        if i == n - 1:
            eta = "(Total: %.2f s)" % (time.time() - t)
        print("Progress: %s / %s %s" % (i + 1, n, eta), end=' ')
        sys.stdout.flush()
        if i == n - 1:
            print("")

    return report


def progress_tracker(n):
    t = time.time()

    def get_progress(i):
        eta = ""
        if i > 0:
            remaining = (np.round((time.time() - t) / float(i) * (n - i)))
            eta = " (ETA: %s)" % time.strftime("%H:%M:%S", time.localtime(time.time() + remaining))
        return "%s / %s%s" % (i + 1, n, eta)

    return get_progress


def append_postfix(filename, postfix):
    base, ext = os.path.splitext(filename)
    return "%s_%s%s" % (base, postfix, ext)


def get_cov_r(cov_matrix, dx, bins):
    n = cov_matrix.shape[0]
    a, b = np.indices((n, n))
    r = (abs(a - np.arange(n)) * dx).flatten()
    cov_matrix = cov_matrix.flatten()
    nans = np.isnan(cov_matrix)
    r = r[~nans]
    cov_matrix = cov_matrix[~nans]
    cov_m, bins, _ = stats.binned_statistic(r, cov_matrix, bins=bins)
    m_bins = np.mean(np.vstack([bins[1:], bins[:-1]]), axis=0)
    return m_bins, cov_m


def save_dict_to_h5(filename, d):
    with h5py.File(filename, 'w') as hf:
        for name, value in d.items():
            hf.create_dataset(name, data=value)


def load_dict_from_h5(filename):
    d = dict()
    with h5py.File(filename, 'r') as hf:
        for name, value in hf.items():
            if value.ndim > 0:
                d[name] = value[:]
            else:
                if value.dtype == 'object':
                    d[name] = value.asstr()[()]
                else:
                    d[name] = value[()]
    return d
