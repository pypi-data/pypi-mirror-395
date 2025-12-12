# Function for image based Power spectra estimation
#
# Authors: F.Mertens

from __future__ import division
from __future__ import absolute_import
from os import uname

import numpy as np

from scipy import stats

from . import psutil


def get_cart_pb_corr(beam_type, beam_fwhm, res, img_shape):
    """Get primary beam correction factor for image based PS."""
    nx, ny = img_shape

    thxval = res * np.arange(-nx / 2., nx / 2.)
    thyval = res * np.arange(-ny / 2., ny / 2.)
    thx, thy = np.meshgrid(thxval, thyval)

    fov_map = (res * nx) * (res * ny)
    beam_map = psutil.get_beam(np.sqrt(thx ** 2 + thy ** 2), beam_type, beam_fwhm, None)
    pb_corr = fov_map / (beam_map ** 2).mean()

    return pb_corr


def get_cross_power_spectra_nw(ft_cube1, ft_cube2, uu, vv, el):
    """Compute the spatial cross power spectra

    Args:
        ft_cube1 (n_freqs, n_vis): Visibilities cube 1
        ft_cube2 (n_freqs, n_vis): Visibilities cube 2
        uu (n_vis): U in wavelength
        vv (n_vis): V in wavelength
        el (n_el): The l modes at which the power spectra will be computed

    Returns:
        n_freqs, n_el: The spatial power spectra
    """
    ru = np.sqrt(uu ** 2 + vv ** 2)

    l = [(a - (b - a) / 2., b + (b - a) / 2.) for a, b in psutil.pairwise(el)]
    bins_edges = np.array([k[0] for k in l] + [l[-2][1], l[-1][1]]) / (2 * np.pi)

    ps, _, _ = stats.binned_statistic(ru, (np.conj(ft_cube1) * ft_cube2).real, 'mean', bins_edges)
    bins_mcount, _, _ = stats.binned_statistic(ru, np.ones_like(ru), 'sum', bins_edges)

    ps_err = np.sqrt(2 / bins_mcount) * ps

    return ps, ps_err


def get_cross_power_spectra(ft_cube1, ft_cube2, uu, vv, el, weight_cube=None, return_complex=False, uniform_bins=False):
    """Compute the spatial cross power spectra

    Args:
        ft_cube1 (n_freqs, n_vis): Visibilities cube 1
        ft_cube2 (n_freqs, n_vis): Visibilities cube 2
        uu (n_vis): U in wavelength
        vv (n_vis): V in wavelength
        el (n_el): The l modes at which the power spectra will be computed
        weight_cube (n_freqs, n_vis): The weight cube. This should be the product of weight_cube for the cube 1 and cube 2.

    Returns:
        n_freqs, n_el: The spatial power spectra
    """
    ru = np.sqrt(uu ** 2 + vv ** 2)

    if uniform_bins:
        d_el = el[1] - el[0]
        bins_edges = np.arange(el[0] - d_el / 2, el[-1] + d_el, d_el) / (2 * np.pi)
    else:
        bins_edges = np.array([el[0] - 1] + [a + (b - a) / 2. for a, b in psutil.pairwise(el)] + [el[-1] + 1]) / (2 * np.pi)

    ps_cube = (np.conj(ft_cube1) * ft_cube2)

    if not return_complex:
        ps_cube = ps_cube.real

    if weight_cube is not None:
        # w = weight_cube.mean(axis=0) ** 2
        # w = np.repeat(w[np.newaxis, :], ps_cube.shape[0], axis=0)
        w = weight_cube
    else:
        w = np.ones_like(ps_cube)

    ps = []
    ps_err = []
    n_eff = []
    ps_w = []

    indices = np.digitize(ru, bins_edges)
    with np.errstate(divide='ignore', invalid='ignore'):
        for i in np.arange(len(bins_edges) - 1) + 1:
            p = np.nansum(w[:, indices == i] * ps_cube[:, indices == i], axis=1) / np.sum(w[:, indices == i], axis=1)
            p_err = np.sqrt(2 * np.sum(w[:, indices == i] ** 2 * p[:, None] **
                                       2, axis=1) / np.sum(w[:, indices == i], axis=1) ** 2)
            ps.append(p)
            ps_err.append(p_err)
            n_eff.append(np.sum(w[:, indices == i], axis=1) ** 2 / np.sum(w[:, indices == i] ** 2, axis=1))
            ps_w.append(np.sum(w[:, indices == i], axis=1))

    return np.array(ps).T, np.array(ps_err).T, np.array(n_eff).T, np.array(ps_w).T


def get_power_spectra(ft_cube, uu, vv, el, weight_cube=None, return_complex=False, uniform_bins=False):
    """Compute the spatial power spectra

    Args:
        ft_cube (n_freqs, n_vis): Visibilities cube
        uu (n_vis): U in wavelength
        vv (n_vis): V in wavelength
        el (n_el): The l modes at which the power spectra will be computed

    Returns:
    n_freqs, n_el: The spatial power spectra
    """
    return get_cross_power_spectra(ft_cube, ft_cube, uu, vv, el, weight_cube=weight_cube, 
                                   return_complex=return_complex, uniform_bins=uniform_bins)


def get_2d_cross_power_spectra(delay, dft_cube1, dft_cube2, uu, vv, el, half=True, weight_cube=None, 
                               return_complex=False, uniform_bins=False):
    """Compute the 2D spatial/frequency power spectra

    Args:
        delay (n_delays): Delays
        dft_cube1 (n_delays, n_vis): delay visibilities cube 1
        dft_cube2 (n_delays, n_vis): delay visibilities cube 2
        uu (n_vis): U in wavelength
        vv (n_vis): V in wavelength
        el (n_el): The l modes at which the power spectra will be computed
        half (bool, optional): Compute only positive delay PS

    Returns:
        delay (M), 2D PS (M, n_el)
    """

    ps2d, ps2d_err, n_eff, ps_w = get_cross_power_spectra(dft_cube1, dft_cube2, uu, vv, el, 
                                                          weight_cube=weight_cube,
                                                          return_complex=return_complex, uniform_bins=uniform_bins)

    if half:
        M = len(delay)
        delay = delay[M // 2 + 1:]
        if psutil.is_odd(M):
            ps2d = 0.5 * (ps2d[M // 2 + 1:] + ps2d[:M // 2][::-1])
            ps2d_err = 0.5 * np.sqrt(ps2d_err[M // 2 + 1:] ** 2 + ps2d_err[:M // 2][::-1] ** 2)
            n_eff = n_eff[M // 2 + 1:] + n_eff[:M // 2][::-1]
            ps_w = ps_w[M // 2 + 1:] + ps_w[:M // 2][::-1]
        else:
            ps2d = 0.5 * (ps2d[M // 2 + 1:] + ps2d[1:M // 2][::-1])
            ps2d_err = 0.5 * np.sqrt(ps2d_err[M // 2 + 1:] ** 2 + ps2d_err[1:M // 2][::-1] ** 2)
            n_eff = n_eff[M // 2 + 1:] + n_eff[1:M // 2][::-1]
            ps_w = ps_w[M // 2 + 1:] + ps_w[1:M // 2][::-1]

    return delay, ps2d, ps2d_err, n_eff, ps_w


def get_2d_power_spectra(delay, dft_cube, uu, vv, el, half=True, weight_cube=None, uniform_bins=False):
    """Compute the 2D spatial/frequency power spectra

    Args:
        delay (n_delays): Delays
        dft_cube (n_delays, n_vis): delay visibilities cube
        uu (n_vis): U in wavelength
        vv (n_vis): V in wavelength
        el (n_el): The l modes at which the power spectra will be computed
        half (bool, optional): Compute only positive delay PS

    Returns:
        delay (M), 2D PS (M, n_el)
    """
    return get_2d_cross_power_spectra(delay, dft_cube, dft_cube, uu, vv, el, half=half, 
                                      weight_cube=weight_cube, uniform_bins=uniform_bins)


def get_vis_count(ks, kbins):
    return stats.binned_statistic(ks.flatten(), np.ones_like(ks).flatten(), 'sum', kbins)[0]


def get_3d_cross_power_spectre_nw(dft_cube1, dft_cube2, kbins, k_per, k_par, return_complex=False):
    """Compute the 3D (spherically averaged) power spectra

    Args:
        dft_cube1 (n_delays, n_vis): delay visibilities cube 1
        dft_cube2 (n_delays, n_vis): delay visibilities cube 2
        kbins (n_bins + 1): k bins for which the PS will be computed
        k_per (n_delays, n_vis): k perpendicular for the full cube
        k_par (n_delays, n_vis): k parallel for the full cube

    Returns:
        k_mean (n_bins): Mean of the k bins
        dsp (n_bins): 3D power spectra
        dsp_err (n_bins): sampling variance
    """
    M = dft_cube1.shape[0]
    ks = np.sqrt(k_per ** 2 + k_par ** 2)

    bins_mcount, _, _ = stats.binned_statistic(ks.flatten(), np.ones_like(ks).flatten(),
                                               'sum', kbins)

    k_mean, _, _ = stats.binned_statistic(ks.flatten(), ks.flatten(), 'mean', kbins)

    ps_cube = (np.conj(dft_cube1) * dft_cube2)

    if not return_complex:
        ps_cube = ps_cube.real

    if psutil.is_odd(M):
        ps_cube = 0.5 * (ps_cube[M // 2 + 1:] + ps_cube[:M // 2][::-1])
    else:
        ps_cube = 0.5 * (ps_cube[M // 2 + 1:] + ps_cube[1:M // 2][::-1])

    bins_mcount = 2 * bins_mcount

    dsp, _, _ = stats.binned_statistic(ks.flatten(), ps_cube.flatten(), 'mean', kbins)

    k_norm = k_mean ** 3 / (2 * np.pi ** 2)
    dsp = dsp * k_norm

    dsp_err = np.sqrt(2 / bins_mcount) * dsp

    return k_mean, dsp, dsp_err


def get_3d_cross_power_spectre(dft_cube1, dft_cube2, kbins, k_per, k_par, weight_cube=None,
                               uu=None, vv=None, w_square=False, return_complex=False):
    """Compute the 3D (spherically averaged) power spectra

    Args:
        dft_cube1 (n_delays, n_vis): delay visibilities cube 1
        dft_cube2 (n_delays, n_vis): delay visibilities cube 2
        kbins (n_bins + 1): k bins for which the PS will be computed
        k_per (n_delays, n_vis): k perpendicular for the full cube
        k_par (n_delays, n_vis): k parallel for the full cube
        weight_cube (n_freqs, n_vis): The weight cube. This should be the product of weight_cube for the cube 1 and cube 2.

    Returns:
        k_mean (n_bins): Mean of the k bins
        dsp (n_bins): 3D power spectra
        dsp_err (n_bins): sampling variance
    """
    M = dft_cube1.shape[0]
    ks = np.sqrt(k_per ** 2 + k_par ** 2)

    ps_cube = (np.conj(dft_cube1) * dft_cube2)

    if not return_complex:
        ps_cube = ps_cube.real

    w = weight_cube
    if w is None:
        w = 1 * np.ones_like(ps_cube)

    if (k_par < 0).sum() == 0:
        w = w[M // 2 + 1:]
        if psutil.is_odd(M):
            ps_cube = 0.5 * (ps_cube[M // 2 + 1:] + ps_cube[:M // 2][::-1])
        else:
            ps_cube = 0.5 * (ps_cube[M // 2 + 1:] + ps_cube[1:M // 2][::-1])

    k_mean = []
    k_std = []
    dsp = []
    dsp_err = []
    n_eff = []

    indices = np.digitize(ks, kbins)

    for i in np.arange(len(kbins) - 1) + 1:
        w_b = w[indices == i]
        p = np.nansum(w_b * ps_cube[indices == i]) / np.sum(w_b)
        p_err = np.sqrt(2 * np.sum(w_b ** 2 * p ** 2) / np.sum(w_b) ** 2)

        k_mean_b = psutil.nanaverage(ks[indices == i], w_b)
        k_mean.append(k_mean_b)
        k_std.append(psutil.nanaverage((ks[indices == i] - k_mean_b) ** 2, w_b) ** .5)

        dsp.append(p)
        dsp_err.append(p_err)
        n_eff.append(np.sum(w_b) ** 2 / np.sum(w_b ** 2))

    k_mean = np.array(k_mean)
    k_std = np.array(k_std)
    n_eff = np.array(n_eff)
    k_norm = k_mean ** 3 / (2 * np.pi ** 2)
    dsp = np.array(dsp) * k_norm
    dsp_err = np.array(dsp_err) * k_norm / np.sqrt(2)

    return k_mean, k_std, dsp, dsp_err, n_eff


def get_3d_power_spectre(dft_cube, kbins, k_per, k_par):
    """Compute the 3D (spherically averaged) power spectra

    Args:
        dft_cube (n_delays, n_vis): Description
        kbins (n_bins + 1): k bins for which the PS will be computed
        k_per (n_delays, n_vis): k perpendicular for the full cube
        k_par (n_delays, n_vis): k parallel for the full cube

    Returns:
        k_mean (n_bins): Mean of the k bins
        dsp (n_bins): 3D power spectra
        dsp_err (n_bins): sampling variance
    """

    return get_3d_cross_power_spectre(dft_cube, dft_cube, kbins, k_per, k_par)
