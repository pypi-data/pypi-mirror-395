# Utility functions for dealing with spherical-harmonics data cubes
#
# Authors: F.Mertens


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import time
import itertools
from multiprocessing import Pool

import tables

import numpy as np
from astropy import constants as const
from scipy.special import spherical_jn as sph_jn

import healpy as hp

from scipy.interpolate import RectBivariateSpline

import numexpr as ne

# try:
#     from scipy import weave
# except ImportError:
#     import weave

# from scipy import signal
# from scipy import interpolate
from scipy.special import j1 as bessel_j1

from . import psutil


LOFAR_STAT_POS = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/statpos.data')

NUM_POOL = int(os.environ.get('OMP_NUM_THREADS', 2))

ne.set_num_threads(NUM_POOL)


def xfact(m):
    # computes (2m-1)!!/sqrt((2m)!)
    res = 1.
    for i in xrange(1, 2 * m + 1):
        if i % 2:
            res *= i  # (2m-1)!!
        res /= np.sqrt(i)  # sqrt((2m)!)
    return res


def lplm_n(l, m, x):
    # associated legendre polynomials normalized as in Ylm, from Numerical Recipes 6.7
    l, m = int(l), int(m)
    assert 0 <= m <= l and np.all(np.abs(x) <= 1.)

    norm = np.sqrt(2. * l + 1.) / np.sqrt(4. * np.pi)
    if m == 0:
        pmm = norm * np.ones_like(x)
    else:
        pmm = (-1.)**m * norm * xfact(m) * (1. - x**2.)**(m / 2.)
    if l == m:
        return pmm
    pmmp1 = x * pmm * np.sqrt(2. * m + 1.)
    if l == m + 1:
        return pmmp1
    for ll in xrange(m + 2, l + 1):
        pll = (x * (2. * ll - 1.) * pmmp1 - np.sqrt((ll - 1.)**2. - m**2.) * pmm) / np.sqrt(ll**2. - m**2.)
        pmm = pmmp1
        pmmp1 = pll
    return pll


def Ylm(l, m, phi, theta):
    # spherical harmonics
    # theta is from 0 to pi with pi/2 on equator
    l, m = int(l), int(m)
    assert 0 <= np.abs(m) <= l
    if m > 0:
        return lplm_n(l, m, np.cos(theta)) * np.exp(1J * m * phi)
    elif m < 0:
        return (-1.)**m * lplm_n(l, -m, np.cos(theta)) * np.exp(1J * m * phi)
    return lplm_n(l, m, np.cos(theta)) * np.ones_like(phi)


def Ylmr(l, m, phi, theta):
    # real spherical harmonics
    # theta is from 0 to pi with pi/2 on equator
    l, m = int(l), int(m)
    assert 0 <= np.abs(m) <= l
    if m > 0:
        return lplm_n(l, m, np.cos(theta)) * np.cos(m * phi) * np.sqrt(2.)
    elif m < 0:
        return (-1.)**m * lplm_n(l, -m, np.cos(theta)) * np.sin(-m * phi) * np.sqrt(2.)
    return lplm_n(l, m, np.cos(theta)) * np.ones_like(phi)


# TODO: port Alm2VisTransMatrix

# class Alm2VisTransMatrix(object):
#     ''' Object that encapsulate all the necessary steps to create the independents
#         transformation matrix that can be used to obtain independently the real
#         and imaginary part of the visibilities. Also have method to split and recombine
#         the alm.

#         Example:
#         trm = Alm2VisTransMatrix(ll, mm, ylm, jn)
#         alm_r, alm_i = trm.split(alm)
#         Vreal = np.dot(alm_r, trm.T_r.T)
#         Vimag = np.dot(alm_i, trm.T_i.T)
#         alm = trm.recombine(alm_r, alm_i)

#         '''

#     def __init__(self, ll, mm, ylm_set, lamb, order='C'):
#         self.lm_size = len(ll)
#         pi = np.pi

#         # t = time.time()
#         ylm_lm_even, ylm_m0_l_even, ylm_lm_odd, ylm_m0_l_odd = ylm_set

#         self.m0_l_even = get_lm_selection_index(ll, mm, ylm_m0_l_even.ll, ylm_m0_l_even.mm, keep_order=True)
#         self.m0_l_odd = get_lm_selection_index(ll, mm, ylm_m0_l_odd.ll, ylm_m0_l_odd.mm, keep_order=True)
#         self.lm_even = get_lm_selection_index(ll, mm, ylm_lm_even.ll, ylm_lm_even.mm, keep_order=True)
#         self.lm_odd = get_lm_selection_index(ll, mm, ylm_lm_odd.ll, ylm_lm_odd.mm, keep_order=True)

#         self.ll_r = np.hstack((ylm_m0_l_even.ll, ylm_lm_even.ll, ylm_lm_even.ll))
#         self.mm_r = np.hstack((ylm_m0_l_even.mm, ylm_lm_even.mm, ylm_lm_even.mm))

#         p_m0 = ((-1) ** (ylm_m0_l_even.ll // 2))[:, np.newaxis]
#         p_mp = ((-1) ** (ylm_lm_even.ll // 2))[:, np.newaxis]

#         i1 = len(ylm_m0_l_even.ll)
#         i2 = len(ylm_lm_even.ll)

#         # print "Time lm_selection %.2f s" % (time.time() - t)
#         # t = time.time()
#         self.T_r = np.zeros((len(self.ll_r), ylm_m0_l_even.data.shape[1]), order=order)
#         # print "Time T_r init %.2f s" % (time.time() - t)
#         # t = time.time()

#         if len(ylm_m0_l_even.ll) > 0:
#             jn = get_jn_fast_weave(ylm_m0_l_even.ll, ylm_m0_l_even.rb / lamb)
#             r = ylm_m0_l_even.data.real
#             ne.evaluate('4 * pi * p_m0 * r * jn', out=self.T_r[:i1, :])
#             # print "Time m0 %.2f s" % (time.time() - t)

#         # t = time.time()
#         r = ylm_lm_even.data.real
#         i = ylm_lm_even.data.imag
#         jn = get_jn_fast_weave(ylm_lm_even.ll, ylm_lm_even.rb / lamb)
#         # print "Time jn %.2f s" % (time.time() - t)

#         # t = time.time()
#         ne.evaluate('4 * pi * p_mp * 2 * r * jn', out=self.T_r[i1:i1 + i2, :])
#         # print "Time ev1 %.2f s" % (time.time() - t)

#         # t = time.time()
#         ne.evaluate('4 * pi * p_mp * -2 * i * jn', out=self.T_r[i1 + i2:i1 + i2 + i2, :])
#         # print "Time ev2 %.2f s" % (time.time() - t)

#         self.ll_i = np.hstack((ylm_m0_l_odd.ll, ylm_lm_odd.ll, ylm_lm_odd.ll))
#         self.mm_i = np.hstack((ylm_m0_l_odd.mm, ylm_lm_odd.mm, ylm_lm_odd.mm))

#         p_m0 = ((-1) ** (ylm_m0_l_odd.ll // 2))[:, np.newaxis]
#         p_mp = ((-1) ** (ylm_lm_odd.ll // 2))[:, np.newaxis]

#         i1 = len(ylm_m0_l_odd.ll)
#         i2 = len(ylm_lm_odd.ll)

#         self.T_i = np.zeros((len(self.ll_i), ylm_m0_l_even.data.shape[1]), order=order)

#         if len(ylm_m0_l_odd.ll) > 0:
#             r = ylm_m0_l_odd.data.real
#             jn = get_jn_fast_weave(ylm_m0_l_odd.ll, ylm_m0_l_odd.rb / lamb)
#             ne.evaluate('- 4 * pi * p_m0 * r * jn', out=self.T_i[:i1, :])

#         if len(ylm_lm_odd.ll) > 0:
#             r = ylm_lm_odd.data.real
#             i = ylm_lm_odd.data.imag
#             jn = get_jn_fast_weave(ylm_lm_odd.ll, ylm_lm_odd.rb / lamb)

#             ne.evaluate('-4 * pi * p_mp * 2 * r * jn', out=self.T_i[i1:i1 + i2, :])
#             ne.evaluate('-4 * pi * p_mp * -2 * i * jn', out=self.T_i[i1 + i2:i1 + i2 + i2, :])

#     def split(self, alm):
#         ''' Split the alm to be used to recover Re(V) and Im(V) independently'''
#         alm_r = np.hstack((alm.real[self.m0_l_even], alm.real[self.lm_even], alm.imag[self.lm_even]))
#         alm_i = np.hstack((alm.real[self.m0_l_odd], alm.real[self.lm_odd], alm.imag[self.lm_odd]))

#         return (alm_r, alm_i)

#     def recombine(self, alm_r, alm_i):
#         ''' Recombine alm_r and alm_i to a full, complex alm'''
#         split_r = (len(self.m0_l_even), len(self.m0_l_even) + len(self.lm_even))
#         split_i = (len(self.m0_l_odd), len(self.m0_l_odd) + len(self.lm_odd))

#         alm = np.zeros(self.lm_size, dtype=np.complex)
#         alm[self.m0_l_even] = alm_r[:split_r[0]]
#         alm[self.m0_l_odd] = alm_i[:split_i[0]]
#         alm[self.lm_even] = alm_r[split_r[0]:split_r[1]] + 1j * alm_r[split_r[1]:]
#         alm[self.lm_odd] = alm_i[split_i[0]:split_i[1]] + 1j * alm_i[split_i[1]:]

#         return alm


class AbstractSimpleMatrix(object):

    def __init__(self, n_rows, n_cols, dtype=np.dtype(np.float64)):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.dtype = dtype
        self.init_matrix()

    def init_matrix(self):
        self.data = np.zeros((self.n_rows, self.n_cols), dtype=self.dtype)
        self.build_matrix(self.data)

    def build_matrix(self, array):
        pass

    def get(self):
        return self.data


class AbstractMatrix(object):

    def __init__(self, rows, cols, dtype=np.dtype(np.float64)):
        self.rows = np.unique(rows)
        self.cols = np.unique(cols)
        self.dtype = dtype
        self.init_matrix()

    def init_matrix(self):
        self.data = np.zeros((len(self.rows), len(self.cols)), dtype=self.dtype)
        self.build_matrix(self.data)

    def build_matrix(self, array):
        pass

    def get_full(self):
        return self.data

    def get(self, rows, cols):
        rows_uniq, rev_row_idx = np.unique(rows, return_inverse=True)
        idx_row = np.where(np.in1d(self.rows, rows_uniq))[0]

        cols_uniq, rov_col_idx = np.unique(cols, return_inverse=True)
        idx_col = np.where(np.in1d(self.cols, cols_uniq))[0]

        # PERF: this take quite some time.
        return self.data[idx_row, :][rev_row_idx, :][:, idx_col][:, rov_col_idx]


class AbstractIndexedMatrix(object):

    def __init__(self, rows, cols, idx_cols, dtype=np.dtype(np.float64)):
        self.idx_cols = idx_cols
        self.rows = rows
        self.cols = cols
        self.dtype = dtype
        self.init_matrix()

    def init_matrix(self):
        self.data = np.zeros((len(self.rows), len(self.cols)), dtype=self.dtype)
        self.build_matrix(self.data)

    def build_matrix(self, array):
        pass

    def get_chunk(self, min_idx_col, max_idx_col):
        max_idx_col = min(max_idx_col, max(self.idx_cols))
        left_col = np.nonzero(self.idx_cols >= min_idx_col)[0][0]
        right_col = np.nonzero(self.idx_cols <= max_idx_col)[0][-1]

        idx_col = slice(left_col, right_col + 1)
        return idx_col, self.data[:, idx_col]

    def get(self, rows, cols):
        idx_row = np.where(np.in1d(self.rows, rows))[0]
        idx_col = np.where(np.in1d(self.cols, cols))[0]

        # PERF: this take quite some time.
        return self.data[idx_row, :][:, idx_col]


class AbstractCachedMatrix(object):

    def __init__(self, name, cache_dir, force_build=False, keep_in_mem=False, compress=None):
        self.cache_dir = cache_dir
        self.force_build = force_build
        self.name = name
        self.keep_in_mem = keep_in_mem
        self.compress = compress
        self.h5_file = None

    def init_matrix(self):
        if len(self.rows) == 0 or len(self.cols) == 0:
            self.data = np.zeros((len(self.rows), len(self.cols)), dtype=self.dtype)
            return

        atom = tables.Atom.from_dtype(self.dtype)
        hid = get_hash_list_np_array([self.rows, self.cols])

        if not os.path.exists(self.cache_dir):
            print("\nCreating cache directory")
            os.mkdir(self.cache_dir)

        cache_file = os.path.join(self.cache_dir, '%s_%s.cache' % (self.name, hid))

        if not os.path.exists(cache_file) or self.force_build:
            print('\nBuilding matrix with size: %sx%s ...' % (len(self.rows), len(self.cols)), end=' ')
            start = time.time()

            if self.compress is not None:
                filters = tables.Filters(complib=self.compress, complevel=5)
            else:
                filters = None

            cache_file_temp = cache_file + '.temp'

            with tables.open_file(cache_file_temp, 'w') as h5_file:
                array = h5_file.create_carray('/', 'data', shape=(len(self.rows), len(self.cols)),
                                              atom=atom, filters=filters)
                self.build_matrix(array)

            os.rename(cache_file_temp, cache_file)
            time.sleep(1)

            print('Done in %.2f s' % (time.time() - start))
        else:
            print('\nUsing cached matrix from disk with size: %sx%s' % (len(self.rows), len(self.cols)))

        self.h5_file = tables.open_file(cache_file, 'r')

        if self.keep_in_mem:
            start = time.time()
            print('Mapping matrix to memory...', end=' ')
            self.data = self.h5_file.root.data[:, :]
            print('Done in %.2f s' % (time.time() - start))
        else:
            self.data = self.h5_file.root.data

    def close(self):
        if self.h5_file is not None:
            self.h5_file.close()


class YlmCachedMatrix(AbstractCachedMatrix, AbstractMatrix):

    def __init__(self, ll, mm, phis, thetas, cache_dir, dtype=np.dtype(np.complex128),
                 force_build=False, keep_in_mem=False, compress=None):
        self.ll = ll
        self.mm = mm
        self.phis = phis
        self.thetas = thetas
        rows = int_pairing(ll, mm)
        cols = real_pairing(phis, thetas)

        AbstractCachedMatrix.__init__(self, 'ylm', cache_dir, force_build=force_build,
                                      keep_in_mem=keep_in_mem, compress=compress)
        AbstractMatrix.__init__(self, rows, cols, dtype)

    def build_matrix(self, array):
        pool = Pool(processes=NUM_POOL)

        results_async = [pool.apply_async(Ylm, (l, m, self.phis, self.thetas))
                         for l, m in zip(self.ll, self.mm)]
        for i, result in enumerate(results_async):
            array[i, :] = result.get()

        pool.close()

    def get(self, ll, mm, phis, thetas):
        rows = int_pairing(ll, mm)
        cols = real_pairing(phis, thetas)
        return AbstractMatrix.get(self, rows, cols)


def ft_phaser_fct(u, v, w, l, m):
    n = np.sqrt(1 - l ** 2 - m ** 2)
    return 1 / n * np.exp(-2 * np.pi * 1j * (u * l + v * m + w * n))


class FtMatrix(AbstractSimpleMatrix):

    def __init__(self, uu, vv, ww, l, m):
        self.uu = uu
        self.vv = vv
        self.ww = ww
        self.l = l
        self.m = m

        AbstractSimpleMatrix.__init__(self, len(self.uu), len(self.l), np.dtype(np.complex128))

    def build_matrix(self, array):
        pool = Pool(processes=NUM_POOL)

        # results_async = [pool.apply_async(ft_phaser_fct, (u, v, w, self.l, self.m))
        #                  for u, v, w in zip(self.uu, self.vv, self.ww)]
        results_async = [pool.apply_async(ft_phaser_fct, (self.uu, self.vv, self.ww, l, m))
                         for l, m in zip(self.l, self.m)]

        for i, result in enumerate(results_async):
            array[:, i] = result.get()

        pool.close()


class YlmChunck(object):

    def __init__(self, ll, mm, phis, thetas, rb, sort_idx_cols, data):
        self.ll = ll
        self.mm = mm
        self.phis = phis
        self.thetas = thetas
        self.rb = rb
        self.data = data
        self.sort_idx_cols = sort_idx_cols


class YlmIndexedCachedMatrix(AbstractCachedMatrix, AbstractIndexedMatrix):

    def __init__(self, ll, mm, phis, thetas, rb, cache_dir, dtype=np.dtype(np.complex128),
                 force_build=False, keep_in_mem=False, compress=None):
        self.sort_idx_cols = psutil.sort_index(rb)
        self.ll = ll
        self.mm = mm
        self.phis = phis[self.sort_idx_cols]
        self.thetas = thetas[self.sort_idx_cols]
        self.rb = rb[self.sort_idx_cols]
        rows = int_pairing(self.ll, self.mm)
        cols = real_pairing(self.phis, self.thetas)

        AbstractCachedMatrix.__init__(self, 'ylm', cache_dir, force_build=force_build,
                                      keep_in_mem=keep_in_mem, compress=compress)
        AbstractIndexedMatrix.__init__(self, rows, cols, self.rb, dtype=dtype)

    def build_matrix(self, array):
        pool = Pool(processes=NUM_POOL)

        results_async = [pool.apply_async(Ylm, (l, m, self.phis, self.thetas))
                         for l, m in zip(self.ll, self.mm)]
        for i, result in enumerate(results_async):
            array[i, :] = result.get()

        pool.close()

    def get_chunk(self, bmin, bmax):
        idx_col, data = AbstractIndexedMatrix.get_chunk(self, bmin, bmax)

        return YlmChunck(self.ll, self.mm, self.phis[idx_col],
                         self.thetas[idx_col], self.rb[idx_col],
                         self.sort_idx_cols[idx_col], data)

    def get(self, ll, mm, phis, thetas):
        rows = int_pairing(ll, mm)
        cols = real_pairing(phis, thetas)
        return AbstractIndexedMatrix.get(self, rows, cols)


class MatrixSet(list):

    def get(self, rows, cols):
        return MatrixSet([m.get(rows, cols) for m in self])

    def get_chunk(self, min_idx_col, max_idx_col):
        return MatrixSet([m.get_chunk(min_idx_col, max_idx_col) for m in self])


class SplittedYlmMatrix(MatrixSet):

    def __init__(self, ll, mm, phis, thetas, rb, cache_dir, dtype=np.dtype(np.complex128),
                 force_build=False, keep_in_mem=False, compress=None):
        lm_even = ((mm != 0) & np.logical_not(is_odd(ll))).astype(bool)
        m0_l_even = ((mm == 0) & np.logical_not(is_odd(ll))).astype(bool)
        lm_odd = ((mm != 0) & (is_odd(ll))).astype(bool)
        m0_l_odd = ((mm == 0) & (is_odd(ll))).astype(bool)

        matrices = []
        for idx in [lm_even, m0_l_even, lm_odd, m0_l_odd]:
            sel_ll = ll[idx]
            sel_mm = mm[idx]
            ylm = YlmIndexedCachedMatrix(sel_ll, sel_mm, phis, thetas, rb, cache_dir, dtype=dtype,
                                         force_build=force_build, keep_in_mem=keep_in_mem, compress=compress)
            matrices.append(ylm)

        self.phis = matrices[0].phis
        self.thetas = matrices[0].thetas
        self.rb = matrices[0].rb

        MatrixSet.__init__(self, matrices)

    def close(self):
        for m in self:
            m.close()


class JnMatrix(AbstractMatrix):

    def __init__(self, ll, ru):
        self.full_ll = ll
        self.full_ru = ru
        self.ll = np.unique(ll)
        self.ru = np.unique(ru)
        AbstractMatrix.__init__(self, self.ll, self.ru, dtype=np.dtype(np.float64))

    def build_matrix(self, array):
        pool = Pool(processes=NUM_POOL)

        results_async = [pool.apply_async(sph_jn, (max(self.ll), 2 * np.pi * r)) for r in self.ru]

        for i, result in enumerate(results_async):
            array[:, i] = result.get()[0][self.ll]

        pool.close()

    def get_full(self):
        return self.get(self.full_ll, self.full_ru)


class SplittedJnMatrix(MatrixSet):

    def __init__(self, ylm_set, lamb):
        matrices = []
        for ylm in ylm_set:
            jn = JnMatrix(ylm.ll, ylm.rb / lamb)
            matrices.append(jn)
        MatrixSet.__init__(self, matrices)


def get_lm(lmax, lmin=0, dl=1, mmin=0, mmax=-1, dm=1, neg_m=False):
    ''' Create set of ll and mm'''
    if mmax == -1:
        mmax = lmax

    ll = []
    mm = []
    all_l = np.arange(lmin, lmax + 1, dl)
    all_m = np.arange(mmin, mmax + 1, dm)
    if neg_m:
        all_m = np.concatenate([-np.arange(max(1, mmin), mmax + 1, dm)[::-1], all_m])
    for m in all_m:
        m_l = all_l[all_l >= abs(m)]
        mm.extend([m] * len(m_l))
        if m < 0:
            ll.extend(m_l[::-1])
        else:
            ll.extend(m_l)
    return np.array(ll, dtype=int), np.array(mm, dtype=int)


def strip_mm(ll, mm, mmax_fct):
    ''' Strip the mm according to the mmax_fct.

        Ex: ll, mm = strip_mm(ll, mm, lambda l: 0.5 * l) '''
    ll2 = ll[mm < np.clip(mmax_fct(ll), 1, max(ll))].astype(int)
    mm2 = mm[mm < np.clip(mmax_fct(ll), 1, max(ll))].astype(int)

    return ll2, mm2


def get_sampled_lm(lmax, lmin=0, dl=1, mmin=0, mmax=-1, dm=1, neg_m=False, m_theta_max=None):
    ll, mm = get_lm(lmin=lmin, lmax=lmax, dl=dl, mmax=mmax, mmin=mmin)

    if m_theta_max is not None:
        ll, mm = strip_mm(ll, mm, lambda l: np.sin(m_theta_max) * l)

    return ll, mm


def get_lm_selection_index(ll1, mm1, ll2, mm2, keep_order=False):
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


def merge_lm(lls, mms):
    # negative m not supported
    ll_concat = np.concatenate(lls)
    mm_concat = np.concatenate(mms)
    lmmax = np.max([ll_concat, mm_concat])

    full_ll, full_mm = get_lm(lmmax)

    idx = get_lm_selection_index(full_ll, full_mm, ll_concat, mm_concat)
    ll = full_ll[idx]
    mm = full_mm[idx]

    return ll, mm


def thetaphi2radec(thetas, phis):
    return phis, np.pi / 2. - thetas


def radec2thetaphi(ras, decs):
    return np.pi / 2. - decs, ras


def nside2radec(nside):
    thetas, phis = hp.pix2ang(nside, np.arange(hp.nside2npix(nside)))
    return thetaphi2radec(thetas, phis)


def change_coord(m, coord):
    """ Change coordinates of a HEALPIX map

    Parameters
    ----------
    m : map or array of maps
      map(s) to be rotated
    coord : sequence of two character
      First character is the coordinate system of m, second character
      is the coordinate system of the output map. As in HEALPIX, allowed
      coordinate systems are 'G' (galactic), 'E' (ecliptic) or 'C' (equatorial)

    Example
    -------
    The following rotate m from galactic to equatorial coordinates.
    Notice that m can contain both temperature and polarization.
    >>>> change_coord(m, ['G', 'C'])
    """
    # Basic HEALPix parameters
    npix = m.shape[-1]
    nside = hp.npix2nside(npix)
    ang = hp.pix2ang(nside, np.arange(npix))

    # Select the coordinate transformation
    rot = hp.Rotator(coord=reversed(coord))

    # Convert the coordinates
    new_ang = rot(*ang)
    new_pix = hp.ang2pix(nside, *new_ang)

    return m[..., new_pix]


def get_ylm(ll, mm, phis, thetas):
    return np.array([Ylm(l, m, phis, thetas) for l, m in zip(ll, mm)])


def get_jn(ll, ru):
    uniq, idx = np.unique(ll, return_inverse=True)
    return np.array([sph_jn(max(uniq), 2 * np.pi * r)[0][uniq][idx] for r in ru]).T


def get_dct(n, nk, ni=None, nki=None, s=0, sk=0, fct=np.cos):
    if ni is None:
        ni = n
    if nki is None:
        nki = nk
    a = np.linspace(0, n - 1, ni)[:, np.newaxis] + s
    b = np.linspace(0, nk - 1, nki) + sk
    return np.sqrt(2. / n) * fct(np.pi / n * a * b)


def get_dct4(n, nk, ni=None, nki=None):
    return get_dct(n, nk, ni=ni, nki=nki, s=0.5, sk=0.5)


def get_dst4(n, nk, ni=None, nki=None):
    return get_dct(n, nk, ni=ni, nki=nki, s=0.5, sk=0.5, fct=np.sin)


def get_dct2(n, nk, ni=None, nki=None):
    dct = get_dct(n, nk, ni=ni, nki=nki, s=0.5, sk=0)
    # dct = np.sqrt(2. / n) * np.cos(np.pi / n * (np.arange(n)[:, np.newaxis] + 0.5) * (np.arange(nk)))
    dct[:, 0] = dct[:, 0] / np.sqrt(2)

    return dct


def get_dct3(n, nk, ni=None, nki=None):
    dct = get_dct(n, nk, ni=ni, nki=nki, s=0, sk=0.5)
    # dct = np.sqrt(2. / n) * np.cos(np.pi / n * (np.arange(n)[:, np.newaxis]) * (np.arange(nk) + 0.5))
    dct[0, :] = 1 / np.sqrt(n)

    return dct


# TODO: port sparse_to_dense_weave_openmp
# def sparse_to_dense_weave_openmp(sparse, idx_x, idx_y):
#     nx = len(idx_x)
#     ny = len(idx_y)
#     ny_sparse = sparse.shape[1]
#     sparse = np.ascontiguousarray(sparse)
#     res = np.zeros((nx, ny))

#     code = '''
#     long i;
#     long j;
#     #pragma omp parallel for private(i) private(j)
#     for(i = 0; i < nx; i++)
#         for(j = 0; j < ny; j++)
#             res[i * ny + j] = sparse[idx_x[i] * ny_sparse + idx_y[j]];
#     '''

#     weave.inline(code, ['res', 'nx', 'ny', 'ny_sparse', 'idx_x', 'idx_y', 'sparse'],
#                  extra_compile_args=['-march=native  -O3  -fopenmp '],
#                  support_code=r"""
#                     #include <stdio.h>
#                     #include <omp.h>
#                     #include <math.h>""",
#                  libraries=['gomp'])

#     return res


# TODO: port sparse_to_dense_weave
# def sparse_to_dense_weave(sparse, idx_x, idx_y):
#     nx = len(idx_x)
#     ny = len(idx_y)
#     ny_sparse = sparse.shape[1]
#     sparse = np.ascontiguousarray(sparse)
#     res = np.zeros((nx, ny))

#     code = '''
#     long i;
#     long j;
#     for(i = 0; i < nx; i++)
#         for(j = 0; j < ny; j++)
#             res[i * ny + j] = sparse[idx_x[i] * ny_sparse + idx_y[j]];
#     '''

#     weave.inline(code, ['res', 'nx', 'ny', 'ny_sparse', 'idx_x', 'idx_y', 'sparse'])

#     return res


# TODO: port get_jn_fast_weave
# def get_jn_fast_weave(ll, ru, fct=sparse_to_dense_weave):
#     uniq, idx = np.unique(ll, return_inverse=True)
#     uniq_r, idx_r = np.unique(ru, return_inverse=True)
#     # print sph_jn(max(uniq), 2 * np.pi * uniq_r[0])
#     sparse = sph_jn(uniq[None, :], 2 * np.pi * uniq_r[:, None]).T

#     return fct(sparse, idx, idx_r)


def get_jn_fast(ll, ru):
    uniq, idx = np.unique(ll, return_inverse=True)
    uniq_r, idx_r = np.unique(ru, return_inverse=True)
    return np.array([sph_jn(max(uniq), 2 * np.pi * r)[0][uniq][idx] for r in uniq_r])[idx_r].T


def get_lm_map(alm, ll, mm):
    m_uniq = np.unique(mm)
    l_uniq = list(np.unique(ll))
    ma = np.zeros((len(m_uniq), len(l_uniq)), dtype=alm.dtype)
    for i, m in enumerate(m_uniq):
        v = alm[mm == m]
        idx = [l_uniq.index(l) for l in ll[mm == m]]
        ma[i, idx] = v
    return ma


def alm2map(alm, ll, mm, thetas, phis, ylm=None):
    if ylm is None:
        ylm = get_ylm(ll, mm, phis, thetas)
    a = np.dot(alm[mm == 0], ylm[mm == 0, :])
    b = 2 * (np.dot(alm.real[mm != 0], ylm.real[mm != 0, :]) - np.dot(alm.imag[mm != 0], ylm.imag[mm != 0, :]))
    return a + b


def get_full_alm(alm, ll, mm):
    full_ll, full_mm = get_lm(max(ll))
    full_alm = np.zeros_like(full_ll, dtype=alm.dtype)
    idx = get_lm_selection_index(full_ll, full_mm, ll, mm)
    full_alm[idx] = alm
    return full_alm


def fast_alm2map(alm, ll, mm, nside):
    if hp.Alm.getsize(max(ll)) != len(alm):
        alm = get_full_alm(alm, ll, mm)

    return hp.alm2map(alm, nside, verbose=False)


def map2alm(map, thetas, phis, ll, mm):
    # Note: hp.map2alm use jacobi iteration to improve the result
    ylm = get_ylm(ll, mm, phis, thetas)
    return 4 * np.pi / len(map) * np.dot(map, np.conj(ylm).T)


def is_odd(num):
    return num & 0x1


def alm_to_cartmap(alm, ll, mm, res, nx, ny, cache_dir='cache'):
    thxval = res * np.arange(-nx / 2., nx / 2.)
    thyval = res * np.arange(-ny / 2., ny / 2.)
    thx, thy = np.meshgrid(thxval, thyval)

    thz = np.sqrt(1 - thx ** 2 - thy ** 2)
    rs, phis, thetas = cart2sph(thx, thy, thz)

    # ylm = util.get_ylm(ll, mm, phis.flatten(), thetas.flatten())
    ylm_obj = YlmCachedMatrix(ll, mm, phis.flatten(), thetas.flatten(), cache_dir, keep_in_mem=True)
    ylm = ylm_obj.get_full()

    a = np.dot(alm[mm == 0], ylm[mm == 0, :])
    b = 2 * (np.dot(alm.real[mm != 0], ylm.real[mm != 0, :]) - np.dot(alm.imag[mm != 0], ylm.imag[mm != 0, :]))
    cart_map = a + b

    ylm_obj.close()
    del ylm

    return cart_map.reshape(nx, ny).real


def filter_cart_map(cart_map, res, umin, umax):
    m_u = 1 / res * np.linspace(-1 / 2., 1 / 2., cart_map.shape[0])
    m_v = 1 / res * np.linspace(-1 / 2., 1 / 2., cart_map.shape[1])
    m_uu, m_vv = np.meshgrid(m_u, m_v)

    m_ru = np.sqrt(m_uu ** 2 + m_vv ** 2)

    ft = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(cart_map)))
    ft[(m_ru <= umin) | (m_ru >= umax)] = 0

    return np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(ft)).real)


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


def cartmap2healpix(cart_map, res, nside):
    ''' res: resolution in radians
        nside: The healpix nside parameter, must be power of 2 and should match res '''

    nx, ny = cart_map.shape
    x = np.arcsin((np.arange(nx) - nx // 2) * res)
    y = np.arcsin((np.arange(ny) - ny // 2) * res)

    hp_map = np.zeros(hp.nside2npix(nside))
    thetas, phis = hp.pix2ang(nside, np.arange(hp.nside2npix(nside)))
    sph_x, sph_y, sph_z = sph2cart(thetas, phis)

    interp_fct = RectBivariateSpline(x, y, cart_map)

    idx = (thetas < np.arcsin(0.5 * min(nx, ny) * res))
    hp_map[idx] = interp_fct.ev(sph_x[idx], sph_y[idx])

    return hp_map


def real_pairing(a, b):
    return 2 ** a * 3 ** b


def int_pairing(a, b):
    ''' Cantor pairing function '''
    return 0.5 * (a + b) * (a + b + 1) + b


def gaussian_beam(thetas, fwhm):
    # fwhm in radians, centered at NP
    sigma = 1 / (2. * np.sqrt(2 * np.log(2))) * fwhm

    gaussian_sph = np.exp(-(0.5 * (thetas / sigma) ** 2))

    return gaussian_sph


def sinc2_beam(thetas, fwhm, null_below_horizon=True, n_sidelibe=None):
    # fwhm in radians, centered at NP
    hwhm = fwhm / 2.
    sinc_sph = (np.sin((thetas * 1.4 / hwhm)) / (thetas * 1.4 / hwhm)) ** 2

    if null_below_horizon:
        sinc_sph[thetas > np.pi / 2.] = 0

    if n_sidelibe is not None:
        sinc_sph[thetas > hwhm / 1.4 * np.pi * (n_sidelibe + 1)] = 0

    return sinc_sph


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
    else:
        return None

    return beam


def get_beam_cart(res, img_shape, beam_type, fwhm, n_sidelobe):
    nx, ny = img_shape

    thxval = res * np.arange(-nx / 2., nx / 2.)
    thyval = res * np.arange(-ny / 2., ny / 2.)
    thx, thy = np.meshgrid(thxval, thyval)

    return get_beam(np.sqrt(thx ** 2 + thy ** 2), beam_type, fwhm, n_sidelobe)


def get_cart_thetas(res, shape):
    nx, ny = shape
    thxval = res * np.arange(-nx / 2., nx / 2.)
    thyval = res * np.arange(-ny / 2., ny / 2.)
    thx, thy = np.meshgrid(thxval, thyval)

    return np.sqrt(thx ** 2 + thy ** 2)


# def cart_uv(rumin, rumax, du, rnd_w=False, freqs_mhz=None):
#     n = np.ceil(2 * rumax / du)
#     u = du * np.arange(-n // 2, n // 2)
#     v = du * np.arange(-n // 2, n // 2)
#     uu, vv = np.meshgrid(u, v)
#     uu = uu.flatten()
#     vv = vv.flatten()

#     ru = np.sqrt(uu ** 2 + vv ** 2)

#     idx = (ru > rumin) & (ru < rumax)

#     uu = uu[idx]
#     vv = vv[idx]

#     if rnd_w:
#         uthetas = np.pi / 4. + nputils.get_random().rand(*uu.shape) * np.pi / 2.
#         ww = np.sqrt(uu ** 2 + vv ** 2) * np.tan(uthetas - np.pi / 2.)
#     else:
#         ww = np.zeros_like(uu)
#         uthetas = np.ones_like(uu) * np.pi / 2.

#     if freqs_mhz is not None:
#         uu = np.array([uu] * len(freqs_mhz))
#         vv = np.array([vv] * len(freqs_mhz))
#         ww = np.array([ww] * len(freqs_mhz))

#     return uu, vv, ww


# def polar_uv(rumin, rumax, nr, nphi, rnd_w=False, freqs_mhz=None, rnd_ru=False):
#     if freqs_mhz is None:
#         freqs_mhz = [150]
#     all_ru = []
#     all_uphis = []
#     all_uthetas = []

#     if rnd_w:
#         uthetas = np.pi / 4. + nputils.get_random().rand(int(nr * nphi)) * np.pi / 2.
#     else:
#         uthetas = np.ones(nr * nphi) * np.pi / 2.

#     for freq in freqs_mhz:
#         uphis = 2 * np.pi * np.linspace(0, 1, num=nphi, endpoint=False)
#         if rnd_ru:
#             # r = nputils.get_random(int(freq)).uniform(rumin, rumax, nr)
#             r = np.linspace(rumin, rumax, num=nr)
#             r += nputils.get_random(int(freq)).randn(int(nr)) * 0.2 * (rumax - rumin) / float(nr)
#         else:
#             r = np.linspace(rumin, rumax, num=nr)
#         uphis, ru = np.meshgrid(uphis, r)
#         uphis = uphis.flatten()
#         ru = ru.flatten()

#         all_ru.append(ru)
#         all_uphis.append(uphis)
#         all_uthetas.append(uthetas)

#     return all_ru, all_uphis, all_uthetas


def lofar_uv(freqs_mhz, dec_deg, hal, har, umin, umax, timeres, include_conj=True,
             min_max_is_baselines=False):
    m2a = lambda m: np.squeeze(np.asarray(m))

    lambs = const.c.value / (np.array(freqs_mhz) * 1e6)

    timev = np.arange(hal * 3600, har * 3600, timeres)

    statpos = np.loadtxt(LOFAR_STAT_POS)
    nstat = statpos.shape[0]

    # All combinations of nant to generate baselines
    stncom = itertools.combinations(np.arange(1, nstat), 2)
    b1, b2 = zip(*stncom)

    uu = []
    vv = []
    ww = []

    for lamb in lambs:
        lamb_u = []
        lamb_v = []
        lamb_w = []

        for tt in timev:
            HA = (tt / 3600.) * (15. / 180) * np.pi - (6.8689389 / 180) * np.pi
            dec = dec_deg * (np.pi / 180)
            RM = np.matrix([[np.sin(HA), np.cos(HA), 0.0],
                            [-np.sin(dec) * np.cos(HA), np.sin(dec) * np.sin(HA), np.cos(dec)],
                            [np.cos(dec) * np.cos(HA), - np.cos(dec) * np.sin(HA), np.sin(dec)]])
            statposuvw = np.dot(RM, statpos.T).T
            bu = m2a(statposuvw[b1, 0] - statposuvw[b2, 0])
            bv = m2a(statposuvw[b1, 1] - statposuvw[b2, 1])
            bw = m2a(statposuvw[b1, 2] - statposuvw[b2, 2])

            u = bu / lamb
            v = bv / lamb
            w = bw / lamb

            if min_max_is_baselines:
                ru = np.sqrt(bu ** 2 + bv ** 2 + bw ** 2)
            else:
                ru = np.sqrt(u ** 2 + v ** 2 + w ** 2)

            idx = (ru > umin) & (ru < umax)

            lamb_u.extend(u[idx])
            lamb_v.extend(v[idx])
            lamb_w.extend(w[idx])

            if include_conj:
                lamb_u.extend(- u[idx])
                lamb_v.extend(- v[idx])
                lamb_w.extend(w[idx])

        uu.append(np.array(lamb_u))
        vv.append(np.array(lamb_v))
        ww.append(np.array(lamb_w))

    return np.array(uu), np.array(vv), np.array(ww)


def vlm2alm(vlm, ll):
    return vlm / (4 * np.pi * (-1j) ** ll)


def alm2vlm(alm, ll):
    return 4 * np.pi * alm * (-1j) ** ll


# def get_alm2vis_matrix(ll, mm, ylm_set, lamb, order='C'):
#     return Alm2VisTransMatrix(ll, mm, ylm_set, lamb, order=order)


def get_hash_np_array(array):
    writeable = array.flags.writeable
    array.flags.writeable = False
    h = hash(array.data)
    array.flags.writeable = writeable

    return h


def get_hash_list_np_array(l):
    return hash(tuple([get_hash_np_array(array) for array in l]))


if __name__ == '__main__':
    pass
