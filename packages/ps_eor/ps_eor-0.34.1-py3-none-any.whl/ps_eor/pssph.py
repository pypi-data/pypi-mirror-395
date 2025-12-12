# Function for spherical harmonics Power spectra estimation
#
# Authors: F.Mertens

from __future__ import division
from __future__ import absolute_import

import numpy as np

from scipy import stats

from . import psutil


def get_cross_power_spectra(alm1, alm2, ll, mm):
    assert alm1.shape == alm2.shape

    l_uniq = np.unique(ll)
    dim = alm1.ndim
    if dim == 1:
        alm1 = alm1[np.newaxis, :]
    ps = np.array([np.sum(np.abs(np.conj(alm1[:, ll == l]) * alm2[:, ll == l]), axis=1) / (l + 1) for l in l_uniq]).T
    if dim == 1:
        ps = ps[0]
    return ps


def get_power_spectra(alm, ll, mm):
    return get_cross_power_spectra(alm, alm, ll, mm)


def get_2d_cross_power_spectra(dft_alm1, dft_alm2, ll, mm, half=True):
    ps2d = get_cross_power_spectra(dft_alm1, dft_alm2, ll, mm)

    if half:
        M = ps2d.shape[0]
        if psutil.is_odd(M):
            ps2d = 0.5 * (ps2d[M // 2 + 1:] + ps2d[:M // 2][::-1])
        else:
            ps2d = 0.5 * (ps2d[M // 2 + 1:] + ps2d[1:M // 2][::-1])

    return ps2d


def get_2d_power_spectra(dft_alm, ll, mm, half=True):
    return get_2d_cross_power_spectra(dft_alm, dft_alm, ll, mm, half=half)


def get_3d_ps_sample_count(k_par, k_per, el, bins, f_sky):
    el_full = np.arange(int(min(el)), int(max(el)))
    k_per_full = el_full * k_per[1] / el[1]
    k_full = np.sqrt(k_per_full ** 2 + k_par[:, np.newaxis] ** 2)
    mcount = np.repeat((2 * el_full + 1.)[np.newaxis, :], len(k_par), axis=0)
    bins_mcount, _, _ = stats.binned_statistic(k_full.flatten(), mcount.flatten(), 'sum', bins)

    return bins_mcount * f_sky


def get_3d_power_spectra(ps2d, k_per, k_par, el, f_sky, bins, k_par_start=0):
    k = np.sqrt(k_per ** 2 + k_par[k_par_start:, np.newaxis] ** 2)

    k_mean, _, _ = stats.binned_statistic(k.flatten(), k.flatten(), 'mean', bins)
    k_norm = k_mean ** 3 / (2 * np.pi ** 2)

    dsp, bins, _ = stats.binned_statistic(k.flatten(), ps2d[k_par_start:].flatten(), 'mean', bins)
    dsp = dsp * k_norm

    bins_mcount = get_3d_ps_sample_count(k_par, k_per, el, bins, f_sky)

    dsp_err = np.sqrt(2. / bins_mcount) * dsp

    return dsp, dsp_err, k_mean
