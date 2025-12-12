# Class for Power spectra estimation
#
# Authors: F.Mertens

import os
import operator
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from scipy import stats
from scipy.signal import get_window

import astropy.units as u

import h5py

from . import psutil
from . import pscart
from . import pssph
from . import sphcube
from . import datacube


MPL_VERSION = mpl.__version__.split('.')

# compatibility for MPL <= 3.2
if int(MPL_VERSION[0]) + 0.1 * int(MPL_VERSION[1]) >= 3.3:
    nonpos_arg = {'nonpositive': 'clip'}
else:
    nonpos_arg = {'nonposy': 'clip'}


class EorBin(object):

    def __init__(self, name, freqs, freqs_fg, M=None):
        """Frequency bin window

        Args:
            name (str): Name of the frequency bin
            freqs (array): The frequencies of the eor bin
            freqs_fg (array): The frequencies used for FG fitting
        """
        self.name = name
        self.freqs = freqs
        self.fmhz = self.freqs / 1e6
        self.freqs_fg = freqs_fg
        self.fmhz_fg = self.freqs_fg / 1e6

        # The mean frequency of the bin
        self.mfreq = self.freqs[0] + (self.freqs[-1] - self.freqs[0]) / 2.

        # Redshift for the mean frequency
        self.z = psutil.freq_to_z(self.mfreq * u.Hz)

        # Frequency channel width
        self.df = psutil.robust_freq_width(self.freqs)

        # Band width
        self.bw = (len(self.freqs) - 1) * self.df
        self.bw_total = (self.freqs[-1] - self.freqs[0])

        # This is the number of k_par that will be computed
        self.M = M
        if self.M is None:
            self.M = int(np.round(self.bw_total / self.df))

    def get_slice(self, data_cube):
        return data_cube.get_slice(self.freqs[0], self.freqs[-1])

    def get_slice_fg(self, data_cube):
        return data_cube.get_slice(self.freqs_fg[0], self.freqs_fg[-1])


class EorBinList(object):

    def __init__(self, freqs=None):
        """List of frequency bin window

        Args:
            freqs (array): All frequencies
        """
        self.windows = dict()
        self.freqs = freqs

    def add_freq(self, name, fmhz_start, fmhz_end, fmhz_fg_start=None, fmhz_fg_end=None):
        """Add a frequency bin window defined by starting and ending frequency (in MHz!)

        Args:
            name (str): Name of the frequency bin window
            fmhz_start (float): Starting frequency, in MHz
            fmhz_end (float): Ending frequency, in MHz
            fmhz_fg_start (float, optional): Starting fg frequency, in MHz
            fmhz_fg_end (float, optional): Ending fg frequency, in MHz
        """
        if fmhz_fg_start is None:
            fmhz_fg_start = fmhz_start
        if fmhz_fg_end is None:
            fmhz_fg_end = fmhz_end
        self.windows[name] = [fmhz_start, fmhz_end, fmhz_fg_start, fmhz_fg_end]

    def get(self, name, freqs=None):
        """Get a frequency bin window

        Args:
            name (str): Name of the frequency bin window

        Returns:
            EoRwindow: The frequency bin window
        """
        if freqs is None:
            freqs = self.freqs

        assert name in self.windows, "Error No EoR bin with name '%s'" % name
        assert freqs is not None, "The frequencies need to be supplied either at the " \
                                  "initialization of the object or at the method level."

        fmhz = freqs * 1e-6
        fmhz_start, fmhz_end, fmhz_fg_start, fmhz_fg_end = self.windows[name]
        slice_bin = psutil.get_freq_slice(fmhz, fmhz_start, fmhz_end)
        slice_bin_fg = psutil.get_freq_slice(fmhz, fmhz_fg_start, fmhz_fg_end)

        if not len(freqs[slice_bin]) > 1:
            print(f'Warning: datacube frequency range ({fmhz.min():.1f}-{fmhz.max():.1f} MHz) does not match EoR window {fmhz_start:.1f}-{fmhz_end:.1f}) MHz')
            return None

        return EorBin(name, freqs[slice_bin], freqs[slice_bin_fg])

    def get_all(self, freqs=None):
        for name in self.get_all_names():
            yield self.get(name, freqs=freqs)

    def get_all_names(self):
        return list(self.windows.keys())

    def save(self, filename):
        array = np.array([[k] + v for (k, v) in self.windows.items()])
        columns = ['name', 'fmhz_start', 'fmhz_end', 'fmhz_fg_start', 'fmhz_fg_end']
        np.savetxt(filename, array, header=','.join(columns), delimiter=',', fmt='%s')

    @staticmethod
    def load(filename):
        eor_bin_list = EorBinList()
        for w in np.atleast_2d(np.loadtxt(filename, str, delimiter=',')):
            eor_bin_list.windows[w[0]] = w[1:].astype(float)

        return eor_bin_list


class MultiNightsPowerSpectraGenerator(object):

    def __init__(self, ps_gen, with_cov_err=False):
        self.ps_gen = ps_gen
        self.with_cov_err = with_cov_err

    def _pre_process(self, multi_cube, ft_nights=False):
        if ft_nights:
            all_ft = np.fft.fftshift(np.fft.fft(multi_cube.data, axis=2), axes=2)
            m_ft_cubes = [multi_cube.cubes[i].new_with_data(all_ft[:, :, i]) for i in range(len(multi_cube.nights))]
            fft_f = np.fft.fftfreq(len(multi_cube.nights))
            return datacube.MultiNightsCube(m_ft_cubes, multi_cube.nights), fft_f, 'k_nights'
        else:
            return multi_cube, multi_cube.nights, 'Nights'

    def get_variance(self, multi_cube, ft_nights=False, fill_gaps=True):
        multi_cube, y, ylabel = self._pre_process(multi_cube, ft_nights=ft_nights)
        ps = [self.ps_gen.get_variance(c, with_cov_err=self.with_cov_err) for c in multi_cube]
        d = np.array([p.data for p in ps])
        e = np.array([p.err for p in ps])
        if fill_gaps:
            d = psutil.fill_gaps(d.T, psutil.get_gaps(ps[0].freqs * 1e6)).T
            e = psutil.fill_gaps(e.T, psutil.get_gaps(ps[0].freqs * 1e6)).T
        return MultiNight2DPowerSpectra(d, e, ps[0].freqs * 1e-6, 'Frequency [MHz]', y, ylabel)

    def get_ps2d_kpar(self, multi_cube, ft_nights=False):
        multi_cube, y, ylabel = self._pre_process(multi_cube, ft_nights=ft_nights)
        ps = [self.ps_gen.get_ps2d(c, with_cov_err=self.with_cov_err) for c in multi_cube]
        d = np.array([p.data.mean(axis=1) for p in ps])
        e = np.array([p.err.mean(axis=1) for p in ps])
        return MultiNight2DPowerSpectra(d, e, ps[0].k_par, r'$k_{\parallel}\,[\mathrm{h\,cMpc^{-1}}]$]', y, ylabel)

    def get_ps2d_kper(self, multi_cube, ft_nights=False):
        multi_cube, y, ylabel = self._pre_process(multi_cube, ft_nights=ft_nights)
        ps = [self.ps_gen.get_ps2d(c, with_cov_err=self.with_cov_err) for c in multi_cube]
        d = np.array([p.data.mean(axis=0) for p in ps])
        e = np.array([p.err.mean(axis=0) for p in ps])
        return MultiNight2DPowerSpectra(d, e, ps[0].k_per, r'$k_{\bot}\,[\mathrm{h\,cMpc^{-1}}]$', y, ylabel)

    def get_ps3d(self, kbins, multi_cube, ft_nights=False):
        multi_cube, y, ylabel = self._pre_process(multi_cube, ft_nights=ft_nights)
        ps = [self.ps_gen.get_ps3d(kbins, c, with_cov_err=self.with_cov_err) for c in multi_cube]
        d = np.array([p.data * 1e6 for p in ps])
        e = np.array([p.err * 1e6 for p in ps])
        return MultiNight2DPowerSpectra(d, e, ps[0].k_mean, r'$\Delta^2 (k)\,[\mathrm{mK^2}]$', y, ylabel)

    def get_ps3d_with_noise(self, kbins, multi_cube, multi_cube_noise, ft_nights=False):
        multi_cube, y, ylabel = self._pre_process(multi_cube, ft_nights=ft_nights)
        ps = [self.ps_gen.get_ps3d_with_noise(kbins, c, c_n, with_cov_err=self.with_cov_err)
              for c, c_n in zip(multi_cube, multi_cube_noise)]
        d = np.array([p.data * 1e6 for p in ps])
        e = np.array([p.err * 1e6 for p in ps])
        return MultiNight2DPowerSpectra(d, e, ps[0].k_mean, r'$\Delta^2 (k)\,[\mathrm{mK^2}]$', y, ylabel)


class PowerSpectraConfig(psutil.SimpleConfig):

    def __init__(self, el=None, window_fct='hann', ft_method='nudft', ps2d_pos_only=True):
        """Power spectra estimator configuration

        Args:
            el (n_modes): The l modes at which the power spectra will be computed
            window_fct (str): The window function that will be used for the frequency -> delay transform.delay.self
                Allowed window types (see scipy.get_window): boxcar, triang, blackman, hamming, hann,
                bartlett, flattop, parzen, bohman, blackmanharris, nuttall, barthann
            ft_method (str, optional): Method used for the frequency -> delay transform.
                Either nudft or lssa. Default to nudft.
            ps2d_pos_only (bool, optional): Compute only positive delay PS
        """
        psutil.SimpleConfig.__init__(self)
        # Delay transform config
        self.add('window_fct', 'hann', str)
        self.add('ft_method', 'nudft', str)
        self.add('rmean_freqs', False, bool)
        self.add('ps2d_pos_only', True, bool)

        # Weighting config
        self.add('weights_by_default', True, bool)
        self.add('empirical_weighting', False, bool)
        self.add('empirical_weighting_polyfit_deg', 3, int)
        self.add('empirical_weighting_n_bins', 0, int)

        # uv filtering config
        self.add('filter_kpar_min', None, float)
        self.add('filter_wedge_theta', 0, float)
        self.add('umin', 50, float)
        self.add('umax', 250, float)
        self.add('du', 10, float)
        self.add('uniform_u_bins', False, bool)

        # Spherically average kbins config
        self.add('kbins_kmax', 0.6, float)
        self.add('kbins_n', 6, int)

        # Primary beam
        self.add('primary_beam', 'lofar_hba', str)

        # Other
        self.add('psf_weights_square', True, bool)
        self.add('cov_err_n_samples', 10, int)
        self.add('df', None, float)
        self.add('n_lssa_ratio', 1., float)

        self.add('rmean_axis', None, int)

        self._el = el
        self.set('ps2d_pos_only', ps2d_pos_only)
        self.set('ft_method', ft_method)
        self.set('window_fct', window_fct)

    @property
    def el(self):
        if self._el is not None:
            el = self._el
        elif self.uniform_u_bins:
            el = 2 * np.pi  * (np.arange(self.umin + self.du / 2, self.umax, self.du))
        else:
            el = 2 * np.pi * (np.arange(self.umin, self.umax, self.du))
        return el

    @el.setter
    def el(self, value):
        self._el = value

    @property
    def rmean_axis(self):
        if self.rmean_freqs:
            return 0
        return None

    @staticmethod
    def load(filename):
        config = PowerSpectraConfig()
        config.parse_from_file(filename, 'PowerSpectraConfig')

        return config

    def copy(self):
        new = psutil.SimpleConfig.copy(self)
        if self._el is not None:
            new._el = self._el.copy()

        return new


class PowerSpectraBuilder(object):

    def __init__(self, ps_config=None, eor_bin_list=None):
        if ps_config is None:
            ps_config = PowerSpectraConfig()
        elif not isinstance(ps_config, PowerSpectraConfig):
            ps_config = PowerSpectraConfig.load(ps_config)

        if eor_bin_list is not None and not isinstance(eor_bin_list, EorBinList):
            eor_bin_list = EorBinList.load(eor_bin_list)

        self.ps_config = ps_config
        self.eor_bin_list = eor_bin_list

    def get(self, cube, eor_bin_name=None, z=None, fmhz_range=None, **kargs):
        assert (eor_bin_name is not None) + (z is not None) + (fmhz_range is not None) <= 1, 'Only one of eor_bin_name, z or fmhz_range may be given.'
        
        if eor_bin_name is not None and self.eor_bin_list is not None:
            eor = self.eor_bin_list.get(eor_bin_name, freqs=cube.freqs)
        else:
            fmhz = cube.freqs * 1e-6
            if z is not None:
                mfreq = psutil.z_to_freq(z) * 1e-6
                fmin = mfreq - 5
                fmax = mfreq + 5
            elif fmhz_range is not None:
                fmin, fmax = fmhz_range
            else:
                fmin = fmhz.min()
                fmax = fmhz.max()
            slice_bin = psutil.get_freq_slice(fmhz, fmin, fmax)
            if len(fmhz[slice_bin]) <= 3:
                print(f'Warning: The datacube has only {len(fmhz[slice_bin])} frequency channel for the chosen frequency bin.')
            eor = EorBin(0, cube.freqs[slice_bin], cube.freqs[slice_bin])

        ps_config = self.ps_config.copy()
        ps_config.parse_dict(kargs)

        pb = datacube.PrimaryBeam.from_name(ps_config.primary_beam)

        if isinstance(cube, datacube.CartDataCube):
            ps_gen = PowerSpectraCart(eor, ps_config, pb)
        elif isinstance(cube, sphcube.SphDataCube):
            ps_gen = PowerSpectraSph(eor, ps_config, pb)
        else:
            raise ValueError('Cube is not of a supported format')

        return ps_gen


class BasePowerSpectra(object):

    def __init__(self, eor_bin, ps_config, primary_beam):
        """Base power spectra estimator class.

        Power spectra is defined by:
            P(k) = (X^2 Y) / (Omega B) V^2(k)

        with:
            X: angular to comoving distance
            Y: frequency to comoving distance
            Omega: Primary beam normalization factor
            B: Frequency bandwidth normalization factor

        Args:
            eor_bin (EorBin): An EoR bin
            ps_config (PowerSpectraConfig): A PS configuration
            primary_beam (PrimaryBeam): The primary beam of the instrument
        """

        self.config = ps_config

        self.eor = eor_bin
        self.el = self.config.el
        self.ft_method = self.config.ft_method
        self.udist = u.Mpc

        self.primary_beam = primary_beam
        self.primary_beam.set_freq(self.eor.mfreq)

        self.set_redshift(self.eor.z)

        self._setup_cache()

    def _setup_cache(self):
        self.ps_cov_cache = psutil.Cache(self._get_ps_cov_err)
        self.ps2d_cov_cache = psutil.Cache(self._get_ps2d_cov_err)
        self.ps3d_cov_cache = psutil.Cache(self._get_ps3d_cov_err)
        self.window_cache = psutil.Cache(self._compute_window)

    def _compute_delays(self):
        self.delay = psutil.get_delay(self.eor.freqs, M=self.eor.M, half=self.config.ps2d_pos_only,
                                      dx=self.config.df)

        self.k_per = psutil.l_to_k(self.el, self.z)
        self.k_par = psutil.delay_to_k(self.delay, self.z)

        self.all_k = np.sqrt(self.k_per ** 2 + self.k_par[:, np.newaxis] ** 2)
        self.kmin = self.all_k.min()

        if self.config.filter_wedge_theta > 0:
            wedge_kpar = psutil.wedge_fct(np.radians(self.config.filter_wedge_theta), self.z, self.k_per)
            if self.config.filter_kpar_min is not None:
                wedge_kpar += self.config.filter_kpar_min
            wedge = np.array([abs(self.k_par) < w_b for w_b in wedge_kpar]).T
            self.kmin = self.all_k[~wedge].min()

        self.ps2d_pos_only = self.config.ps2d_pos_only

    def _compute_window(self, freqs, window_fct):
        mask = psutil.fill_gaps(np.ones_like(freqs), psutil.get_gaps(freqs), fill_with=0)
        window = (get_window(window_fct, len(mask)) * mask)[:, np.newaxis]
        window = window[mask > 0]

        return window

    def set_redshift(self, z):
        self.z = z
        self.X = psutil.angular_to_comoving_distance(self.z, self.udist)
        self.Y = psutil.freqency_to_comoving_distance(self.z, self.udist)
        self._compute_delays()

    def get_window_fct(self, data_cube):
        if self.config.window_fct is None:
            return None
        return self.window_cache.get(data_cube.freqs, self.config.window_fct)

    def get_window_fct_norm(self, data_cube):
        if self.config.window_fct is None:
            return 1
        return 1 / (self.get_window_fct(data_cube) ** 2).mean()

    def get_weights(self, data_cube, weighted='default', delay_transform=False, cov_err=None):
        if weighted == 'default':
            weighted = self.config.weights_by_default
        if weighted and data_cube.weights is not None:
            weights = self.eor.get_slice(data_cube.weights).get()

            if delay_transform:
                w = np.mean(weights, axis=0)[np.newaxis, :]
                k_par = psutil.delay_to_k(psutil.get_delay(data_cube.freqs, M=self.eor.M,
                                                           dx=self.config.df, half=False), self.z)
                weights = np.repeat(w, len(k_par), axis=0)

                if self.config.filter_kpar_min is not None or self.config.filter_wedge_theta > 0:
                    k_per = psutil.l_to_k(2 * np.pi * data_cube.ru, self.z)
                    # all_k = np.sqrt(k_per ** 2 + k_par[:, np.newaxis] ** 2)
                    wedge_kpar = psutil.wedge_fct(np.radians(self.config.filter_wedge_theta), self.z, k_per)
                    if self.config.filter_kpar_min is not None:
                        wedge_kpar += self.config.filter_kpar_min
                    wedge = np.array([abs(k_par) < w_b for w_b in wedge_kpar]).T
                    weights[wedge] = 0

            return weights ** (1 + int(self.config.psf_weights_square))
        return None

    def _get_ps_cov_err(self, data_cube, cov_err, n_samples, **kargs):
        return np.mean([self.get_ps(data_cube.new_with_data(cov_err.get_sample(),
                                                            weights=data_cube.weights), **kargs).data
                        for i in range(n_samples)], axis=0)

    def _get_ps2d_cov_err(self, data_cube, cov_err, n_samples, **kargs):
        return np.mean([self.get_ps2d(data_cube.new_with_data(cov_err.get_sample(),
                                                              weights=data_cube.weights), **kargs).data
                        for i in range(n_samples)], axis=0)

    def _get_ps3d_cov_err(self, data_cube, cov_err, n_samples, kbins, **kargs):
        return np.mean([self.get_ps3d(kbins, data_cube.new_with_data(cov_err.get_sample(),
                                                                     weights=data_cube.weights,
                                                                     cov_err=data_cube.cov_err),
                                      with_cov_err=False, **kargs).data for i in range(n_samples)], axis=0)

    def get_ps_cov_err(self, data_cube):
        if data_cube.cov_err is not None:
            ps_cov_err = self.ps_cov_cache.get(data_cube, data_cube.cov_err, self.config.cov_err_n_samples)
            return SpatialPowerSpectra(ps_cov_err, np.zeros_like(ps_cov_err), self.eor.freqs, self.el, self.k_per)

    def get_ps2d_cov_err(self, data_cube):
        if data_cube.cov_err is not None:
            ps_cov_err = self.ps2d_cov_cache.get(data_cube, data_cube.cov_err, self.config.cov_err_n_samples)
            return CylindricalPowerSpectra(ps_cov_err, np.zeros_like(ps_cov_err),
                                           self.delay, self.el, self.k_per, self.k_par)

    def get_ps3d_cov_err(self, kbins, data_cube):
        if data_cube.cov_err is not None:
            ps = self.get_ps3d(kbins, data_cube, False)
            ps_cov_err = self.ps3d_cov_cache.get(data_cube, data_cube.cov_err, self.config.cov_err_n_samples, kbins)
            return SphericalPowerSpectra(ps_cov_err, np.zeros_like(ps_cov_err), kbins, ps.k_mean, n_eff=ps.n_eff)

    def get_ps_norm(self, data_cube):
        '''Normalization factor for spatial PS'''
        return NotImplementedError()

    def get_omega(self, *args):
        '''Primary Beam normalization factor'''
        return NotImplementedError()

    def get_ps2d(self, data_cube, **kargs):
        return NotImplementedError()

    def get_ps(self, data_cube, **kargs):
        return NotImplementedError()

    def get_variance(self, data_cube, **kargs):
        return NotImplementedError()

    def get_ps3d(self, kbins, data_cube, **kargs):
        return NotImplementedError()

    def get_cross_ps2d(self, kbins, data_cube1, data_cube2, **kargs):
        return NotImplementedError()

    def get_cross_ps(self, kbins, data_cube1, data_cube2, **kargs):
        return NotImplementedError()

    def get_cross_variance(self, kbins, data_cube1, data_cube2, **kargs):
        return NotImplementedError()

    def get_ps2d_norm(self, data_cube):
        '''Normalization factor for 2D (spacial/frequency) PS'''
        B = (len(data_cube.freqs) - 1) / data_cube.meta.freq_width
        return self.get_ps_norm(data_cube) * self.Y / B * self.get_window_fct_norm(data_cube)

    def get_coherence_ps2d(self, ft_cube1, ft_cube2, with_cov_err=False, cross_square=True,
                           weighted='default'):
        ''' Return 2D coherence of ft_cube1 and ft_cube2 (n_freqs, n_vis) '''
        cross = self.get_cross_ps2d(ft_cube1, ft_cube2, with_cov_err, weighted=weighted)
        ps2d_1 = self.get_ps2d(ft_cube1, with_cov_err=with_cov_err, weighted=weighted)
        ps2d_2 = self.get_ps2d(ft_cube2, with_cov_err=with_cov_err, weighted=weighted)

        if cross_square:
            cross_coh = cross.data ** 2 / (ps2d_1.data * ps2d_2.data)
        else:
            cross_coh = cross.data / np.sqrt(ps2d_1.data * ps2d_2.data)

        return CylindricalPowerSpectra(cross_coh, np.zeros_like(cross.data),
                                       self.delay, self.el, self.k_per, self.k_par)

    def get_coherence_ps(self, ft_cube1, ft_cube2, with_cov_err=False, weighted='default'):
        ''' Return 2D coherence of ft_cube1 and ft_cube2 (n_freqs, n_vis) '''
        cross = self.get_cross_ps(ft_cube1, ft_cube2, with_cov_err, weighted=weighted)
        ps2d_1 = self.get_ps(ft_cube1, with_cov_err=with_cov_err, weighted=weighted)
        ps2d_2 = self.get_ps(ft_cube2, with_cov_err=with_cov_err, weighted=weighted)

        cross_coh = cross.data ** 2 / (ps2d_1.data * ps2d_2.data)

        return SpatialPowerSpectra(cross_coh, np.zeros_like(cross.data),
                                   cross.freqs, self.el, self.k_per)

    def get_coherence_variance(self, ft_cube1, ft_cube2, with_cov_err=False, weighted='default'):
        ''' Return 2D coherence of ft_cube1 and ft_cube2 (n_freqs, n_vis) '''
        cross = self.get_cross_variance(ft_cube1, ft_cube2, with_cov_err, weighted=weighted)
        var_1 = self.get_variance(ft_cube1, with_cov_err=with_cov_err, weighted=weighted)
        var_2 = self.get_variance(ft_cube2, with_cov_err=with_cov_err, weighted=weighted)

        return Variance(cross.data ** 2 / (var_1.data * var_2.data), np.zeros_like(cross.data),
                        cross.freqs)

    def get_coherence_ps3d(self, kbins, ft_cube1, ft_cube2, with_cov_err=False,
                           cross_square=True, weighted='default'):
        ''' Return 2D coherence of ft_cube1 and ft_cube2 (n_freqs, n_vis) '''
        cross = self.get_cross_ps3d(kbins, ft_cube1, ft_cube2, with_cov_err, weighted=weighted)
        ps3d_1 = self.get_ps3d(kbins, ft_cube1, with_cov_err=with_cov_err, weighted=weighted)
        ps3d_2 = self.get_ps3d(kbins, ft_cube2, with_cov_err=with_cov_err, weighted=weighted)

        if cross_square:
            cross_coh = cross.data ** 2 / (ps3d_1.data * ps3d_2.data)
        else:
            cross_coh = cross.data / np.sqrt(ps3d_1.data * ps3d_2.data)

        return SphericalPowerSpectra(cross_coh, np.zeros_like(cross.data),
                                     kbins, ps3d_1.k_mean)

    def get_coherence_ps3d_from_sum_diff(self, kbins, ft_cube1, ft_cube2, ft_cube_sum,
                                         ft_cube_diff, with_cov_err=True):
        ''' Return 2D coherence of ft_cube1 and ft_cube2 (n_freqs, n_vis) '''
        cross = (self.get_ps3d(kbins, ft_cube_sum, with_cov_err) - self.get_ps3d(kbins, ft_cube_diff, with_cov_err))
        ps3d_1 = self.get_ps3d(kbins, ft_cube1, with_cov_err)
        ps3d_2 = self.get_ps3d(kbins, ft_cube2, with_cov_err)

        return SphericalPowerSpectra(cross.data ** 2 / (ps3d_1.data * ps3d_2.data), np.zeros_like(cross.data),
                                     kbins, ps3d_1.k_mean)

    def get_coherence_ps2d_from_sum_diff(self, ft_cube1, ft_cube2, ft_cube_sum, ft_cube_diff, with_cov_err=True):
        cross = (self.get_ps2d(ft_cube_sum, with_cov_err).data - self.get_ps2d(ft_cube_diff, with_cov_err).data)
        ps2d_1 = self.get_ps2d(ft_cube1, with_cov_err).data
        ps2d_2 = self.get_ps2d(ft_cube2, with_cov_err).data

        return CylindricalPowerSpectra(cross ** 2 / (ps2d_1 * ps2d_2), np.zeros_like(cross),
                                       self.delay, self.el, self.k_per, self.k_par)

    def get_coherence_variance_from_sum_diff(self, ft_cube1, ft_cube2, ft_cube_sum, ft_cube_diff,
                                             with_cov_err=True):
        cross = (self.get_variance(ft_cube_sum, with_cov_err) - self.get_variance(ft_cube_diff,
                                                                                  with_cov_err))
        ps2d_1 = self.get_variance(ft_cube1, with_cov_err).data
        ps2d_2 = self.get_variance(ft_cube2, with_cov_err).data

        return Variance(cross.data ** 2 / (ps2d_1 * ps2d_2), np.zeros_like(cross.data), cross.freqs)

    def get_cross_ps2d_from_sum_diff(self, ft_cube_sum, ft_cube_diff, with_cov_err=True):
        ps_sum = self.get_ps2d(ft_cube_sum, with_cov_err)
        ps_diff = self.get_ps2d(ft_cube_diff, with_cov_err)
        cross = (ps_sum.data - ps_diff.data)
        cross_err = np.sqrt(ps_sum.err ** 2 + ps_diff.err ** 2)

        return CylindricalPowerSpectra(cross, cross_err, self.delay, self.el,
                                       self.k_per, self.k_par)

    def get_cross_variance_from_sum_diff(self, ft_cube_sum, ft_cube_diff, with_cov_err=True):
        ps_sum = self.get_variance(ft_cube_sum, with_cov_err)
        ps_diff = self.get_variance(ft_cube_diff, with_cov_err)
        cross = (ps_sum.data - ps_diff.data)
        cross_err = np.sqrt(ps_sum.err ** 2 + ps_diff.err ** 2)

        return Variance(cross, cross_err, ps_sum.freqs)

    def get_cross_ps3d_from_sum_diff(self, kbins, ft_cube_sum, ft_cube_diff, with_cov_err=True):
        ps_sum = self.get_ps3d(kbins, ft_cube_sum, with_cov_err)
        ps_diff = self.get_ps3d(kbins, ft_cube_diff, with_cov_err)
        cross = (ps_sum.data - ps_diff.data)
        cross_err = np.sqrt(ps_sum.err ** 2 + ps_diff.err ** 2)

        return SphericalPowerSpectra(cross, cross_err, kbins, ps_sum.k_mean)

    def delay_transform(self, data_cube):
        ''' Delay transform data_cube '''
        if isinstance(data_cube, datacube.NoiseStdCube):
            delay, dft_cube_sq = psutil.lssa_diag_cov(data_cube.freqs, data_cube.data ** 2, 
                                                   M=self.eor.M, dx=self.config.df)
            # Take into account the spectral tapering window function which is not
            # applied here, but is still corrected for later in the code. 
            dft_cube = (dft_cube_sq / self.get_window_fct_norm(data_cube)) ** .5
        else:
            weights = self.get_weights(data_cube, True)
            window = self.get_window_fct(data_cube)

            delay, dft_cube = psutil.delay_transform_cube(data_cube.freqs, data_cube.data, M=self.eor.M,
                                                          method=self.ft_method, dx=self.config.df,
                                                          window=window, weights=weights,
                                                          rmean_axis=self.config.rmean_axis)

            if self.config.filter_kpar_min is not None or self.config.filter_wedge_theta > 0:
                k_par = psutil.delay_to_k(delay, self.z)
                k_per = psutil.l_to_k(2 * np.pi * data_cube.ru, self.z)

                wedge_kpar = psutil.wedge_fct(np.radians(self.config.filter_wedge_theta), self.z, k_per)
                if self.config.filter_kpar_min is not None:
                    wedge_kpar += self.config.filter_kpar_min

                wedge = np.array([abs(k_par) < w_b for w_b in wedge_kpar]).T
                dft_cube[wedge] = np.nan

        return delay, dft_cube

    def _handle_cov_err(self, ps, ps_err, ps_cov_fct, data_cube, with_cov_err, *args, **kargs):
        if with_cov_err and data_cube.cov_err is not None:
            ps_cov_err = ps_cov_fct.get(data_cube, data_cube.cov_err,
                                        self.config.cov_err_n_samples, *args, **kargs)
            err_factor = ps_err / ps
            if with_cov_err < 0:
                return abs(ps - ps_cov_err), abs(ps - ps_cov_err) * err_factor
            return ps + ps_cov_err, (ps + ps_cov_err) * err_factor
        return ps, ps_err

    def _handle_cov_err_cross(self, ps, ps_err, ps_cov_fct, data_cube1, data_cube2,
                              with_cov_err, *args, **kargs):
        if with_cov_err and data_cube1.cov_err is not None:
            ps_cov_err = ps_cov_fct.get(data_cube1, 0.5 * (data_cube1.cov_err + data_cube2.cov_err),
                                        self.config.cov_err_n_samples, *args, **kargs)
            err_factor = ps_err / ps
            if with_cov_err < 0:
                return abs(ps - ps_cov_err), abs(ps - ps_cov_err) * err_factor
            return ps + ps_cov_err, (ps + ps_cov_err) * err_factor
        return ps, ps_err


class PowerSpectraCart(BasePowerSpectra):

    def __init__(self, eor_bin, ps_config, primary_beam):
        """PowerSpectraGenerator class for image base PS computation

        Power spectra is defined by:
            P(k) = (X^2 Y) / (Omega B) V^2(k)

        with:
            X: angular to comoving distance
            Y: frequency to comoving distance
            Omega: Primary beam normalization factor
            B: Frequency bandwidth

        Args:
            eor_bin (EorBin): An EoR bin
            ps_config (PowerSpectraConfig): A PS configuration
            primary_beam (PrimaryBeam): The primary beam of the instrument
        """
        BasePowerSpectra.__init__(self, eor_bin, ps_config, primary_beam)

    def get_ps_norm(self, data_cube):
        '''Normalization factor for spatial PS'''
        return self.X ** 2 / self.get_omega(data_cube.meta)

    def get_ps_err_norm(self, data_cube, with_pb=False):
        mask = datacube.WindowFunction.from_meta(data_cube.meta)
        if with_pb:
            mask = mask * self.primary_beam
        return 1 / (mask.get_area(data_cube.meta, normalize=True) ** 0.5)

    def get_omega(self, data_cube_meta):
        '''Primary Beam normalization factor'''
        nx, ny = data_cube_meta.shape
        res = data_cube_meta.res

        mask = self.primary_beam * datacube.WindowFunction.from_meta(data_cube_meta)

        return mask.get_power(data_cube_meta) / ((res * nx) * (res * ny))

    def get_ps2d(self, data_cube, with_cov_err=True, weighted='default'):
        ''' Return cylindrically averaged power spectra of data_cube'''
        data_cube = self.eor.get_slice(data_cube)
        ps2d_norm = self.get_ps2d_norm(data_cube)
        ps2d_err_norm = self.get_ps_err_norm(data_cube)
        f_delay, dft_cube = self.delay_transform(data_cube)

        weight_cube = self.get_weights(data_cube, weighted, delay_transform=True)

        delay, ps2d, ps2d_err, n_eff, ps2d_w = pscart.get_2d_power_spectra(f_delay, dft_cube, data_cube.uu,
                                                                           data_cube.vv, self.el,
                                                                           half=self.ps2d_pos_only,
                                                                           weight_cube=weight_cube,
                                                                           uniform_bins=self.config.uniform_u_bins)

        ps2d = ps2d * ps2d_norm
        ps2d_err = ps2d_err * ps2d_norm * ps2d_err_norm
        ps2d, ps2d_err = self._handle_cov_err(ps2d, ps2d_err, self.ps2d_cov_cache, data_cube,
                                              with_cov_err, weighted=weighted)

        return CylindricalPowerSpectra(ps2d, ps2d_err, delay, self.el, self.k_per, self.k_par,
                                       n_eff=n_eff, ps2d_w=ps2d_w)

    def get_cross_ps2d(self, data_cube1, data_cube2, with_cov_err=True, weighted='default', return_complex=False):
        ''' Return 2D cross power spectra of data_cube1 and data_cube2'''
        data_cube1 = self.eor.get_slice(data_cube1)
        data_cube2 = self.eor.get_slice(data_cube2)
        ps2d_norm = self.get_ps2d_norm(data_cube1)
        ps2d_err_norm = self.get_ps_err_norm(data_cube1)

        f_delay, dft_cube1 = self.delay_transform(data_cube1)
        f_delay, dft_cube2 = self.delay_transform(data_cube2)

        w1 = self.get_weights(data_cube1, weighted, delay_transform=True)
        w2 = self.get_weights(data_cube2, weighted, delay_transform=True)
        if w1 is None or w2 is None:
            weight_cube = None
        else:
            weight_cube = np.sqrt(w1 * w2)

        delay, ps2d, ps2d_err, n_eff, ps2d_w = pscart.get_2d_cross_power_spectra(f_delay, dft_cube1, dft_cube2,
                                                                                 data_cube1.uu,
                                                                                 data_cube1.vv, self.el,
                                                                                 half=self.ps2d_pos_only,
                                                                                 weight_cube=weight_cube,
                                                                                 return_complex=return_complex,
                                                                                 uniform_bins=self.config.uniform_u_bins)

        _, _, ps2d_1_err, _, _ = pscart.get_2d_cross_power_spectra(f_delay, dft_cube1, dft_cube1, data_cube1.uu,
                                                                   data_cube1.vv, self.el, half=self.ps2d_pos_only,
                                                                   weight_cube=weight_cube,
                                                                   uniform_bins=self.config.uniform_u_bins)

        _, _, ps2d_2_err, _, _ = pscart.get_2d_cross_power_spectra(f_delay, dft_cube1, dft_cube1, data_cube1.uu,
                                                                   data_cube1.vv, self.el, half=self.ps2d_pos_only,
                                                                   weight_cube=weight_cube,
                                                                   uniform_bins=self.config.uniform_u_bins)

        ps2d = ps2d * ps2d_norm
        ps2d_err = np.sqrt(ps2d_1_err * ps2d_2_err) * ps2d_norm * ps2d_err_norm
        ps2d, ps2d_err = self._handle_cov_err_cross(ps2d, ps2d_err, self.ps2d_cov_cache,
                                                    data_cube1, data_cube2, with_cov_err,
                                                    weighted=weighted)

        return CylindricalPowerSpectra(ps2d, ps2d_err, delay, self.el, self.k_per, self.k_par,
                                       n_eff=n_eff, ps2d_w=ps2d_w)

    def get_ps(self, data_cube, with_cov_err=True, weighted='default'):
        ''' Return spatial power spectra of data_cube'''
        data_cube = self.eor.get_slice(data_cube)
        ps_norm = self.get_ps_norm(data_cube)
        ps_err_norm = self.get_ps_err_norm(data_cube)

        weight_cube = self.get_weights(data_cube, weighted)

        ps, ps_err, n_eff, ps_w = pscart.get_power_spectra(data_cube.data, data_cube.uu, data_cube.vv, self.el,
                                                           weight_cube=weight_cube,
                                                           uniform_bins=self.config.uniform_u_bins)

        ps = ps * ps_norm
        ps_err = ps_err * ps_norm * ps_err_norm

        ps, ps_err = self._handle_cov_err(ps, ps_err, self.ps_cov_cache, data_cube,
                                          with_cov_err, weighted=weighted)

        return SpatialPowerSpectra(ps, ps_err, data_cube.freqs, self.el, self.k_per, n_eff=n_eff, ps_w=ps_w)

    def get_cl(self, data_cube, with_cov_err=True, weighted='default'):
        ''' Return spatial power spectra of data_cube'''
        ps = self.get_ps(data_cube, with_cov_err=with_cov_err, weighted=weighted)
        ps.data = ps.data / self.X ** 2
        ps.err = ps.err / self.X ** 2
        ps.cl = True
        return ps

    def get_cross_ps(self, data_cube1, data_cube2, with_cov_err=True, weighted='default', return_complex=False):
        ''' Return spatial power spectra of data_cube'''
        data_cube1 = self.eor.get_slice(data_cube1)
        data_cube2 = self.eor.get_slice(data_cube2)
        ps_norm = self.get_ps_norm(data_cube1)
        ps2d_err_norm = self.get_ps_err_norm(data_cube1)

        w1 = self.get_weights(data_cube1, weighted)
        w2 = self.get_weights(data_cube2, weighted)
        if w1 is None or w2 is None:
            weight_cube = None
        else:
            weight_cube = np.sqrt(w1 * w2)

        ps, ps_err, n_eff, ps_w = pscart.get_cross_power_spectra(data_cube1.data, data_cube2.data, data_cube1.uu,
                                                                 data_cube1.vv, self.el, weight_cube=weight_cube,
                                                                 return_complex=return_complex,
                                                                 uniform_bins=self.config.uniform_u_bins)

        _, ps_1_err, _, _ = pscart.get_cross_power_spectra(data_cube1.data, data_cube1.data, data_cube1.uu,
                                                           data_cube1.vv, self.el, weight_cube=weight_cube,
                                                           uniform_bins=self.config.uniform_u_bins)

        _, ps_2_err, _, _ = pscart.get_cross_power_spectra(data_cube2.data, data_cube2.data, data_cube1.uu,
                                                           data_cube1.vv, self.el, weight_cube=weight_cube,
                                                           uniform_bins=self.config.uniform_u_bins)

        ps = ps * ps_norm
        ps_err = np.sqrt(ps_1_err * ps_2_err) * ps_norm * ps2d_err_norm

        ps, ps_err = self._handle_cov_err_cross(ps, ps_err, self.ps_cov_cache, data_cube1,
                                                data_cube2, with_cov_err, weighted=weighted)

        return SpatialPowerSpectra(ps, ps_err, data_cube1.freqs, self.el, self.k_per, n_eff=n_eff, ps_w=ps_w)

    def get_variance(self, data_cube, with_cov_err=True, weighted='default'):
        cl = self.get_cl(data_cube, with_cov_err=with_cov_err, weighted=weighted)
        var = np.nansum(cl.data * cl.el * (cl.el.max() - cl.el.min()), axis=1) / (2 * np.pi * len(cl.el))
        var_err = np.nansum((cl.err * cl.el * (cl.el.max() - cl.el.min())) ** 2,
                            axis=1) ** 0.5 / (2 * np.pi * len(cl.el))

        return Variance(var, var_err, cl.freqs)

    def get_cross_variance(self, data_cube1, data_cube2, with_cov_err=True, weighted='default'):
        ps = self.get_cross_ps(data_cube1, data_cube2, with_cov_err=with_cov_err, weighted=weighted)
        n_freqs = float(len(ps.freqs))
        var = 1 / n_freqs * ps.data.sum(axis=1)
        var_err = 1 / n_freqs * np.sqrt((ps.err ** 2).sum(axis=1))

        return Variance(var, var_err, ps.freqs)

    def get_ps3d(self, kbins, data_cube, with_cov_err=True, weighted='default'):
        ''' Return spherically averaged power spectra of data_cube for kbins'''
        data_cube = self.eor.get_slice(data_cube)
        data_cube.filter_uvrange(self.config.umin, self.config.umax)

        ps2d_norm = self.get_ps2d_norm(data_cube)
        ps_err_norm = self.get_ps_err_norm(data_cube)
        _, dft_cube = self.delay_transform(data_cube)

        weight_cube = self.get_weights(data_cube, weighted, delay_transform=True,
                                       cov_err=data_cube.cov_err)

        k_per_full = psutil.l_to_k(data_cube.ru * 2 * np.pi, self.z)

        k_per = np.repeat(k_per_full[np.newaxis, :], len(self.k_par), axis=0)
        k_par = np.repeat(self.k_par[:, np.newaxis], len(data_cube.ru), axis=1)

        k_mean, k_std, dsp, dsp_err, n_eff = pscart.get_3d_cross_power_spectre(
            dft_cube, dft_cube, kbins, k_per, k_par, weight_cube=weight_cube)

        dsp = dsp * ps2d_norm
        dsp_err = dsp_err * ps2d_norm * ps_err_norm

        dsp, dsp_err = self._handle_cov_err(dsp, dsp_err, self.ps3d_cov_cache, data_cube,
                                            with_cov_err, kbins, weighted=weighted)

        return SphericalPowerSpectra(dsp, dsp_err, kbins, k_mean, k_std=k_std, n_eff=n_eff)

    def get_ps3d_with_noise(self, kbins, ft_cube, noise_cube, with_cov_err=True, weighted='default'):
        a = self.get_ps3d(kbins, ft_cube, with_cov_err=with_cov_err, weighted=weighted)
        n = self.get_ps3d(kbins, noise_cube, with_cov_err=with_cov_err, weighted=weighted)

        return a - n

    def get_cross_ps3d(self, kbins, data_cube1, data_cube2, with_cov_err=True, weighted='default', return_complex=False):
        ''' Return spherically averaged power spectra of data_cube for kbins'''
        data_cube1 = self.eor.get_slice(data_cube1)
        data_cube2 = self.eor.get_slice(data_cube2)
        data_cube1.filter_uvrange(self.config.umin, self.config.umax)
        data_cube2.filter_uvrange(self.config.umin, self.config.umax)

        ps2d_norm = self.get_ps2d_norm(data_cube1)
        ps_err_norm = self.get_ps_err_norm(data_cube1)
        _, dft_cube2 = self.delay_transform(data_cube1)
        _, dft_cube1 = self.delay_transform(data_cube2)

        w1 = self.get_weights(data_cube1, weighted, delay_transform=True)
        w2 = self.get_weights(data_cube2, weighted, delay_transform=True)
        if w1 is None or w2 is None:
            weight_cube = None
        else:
            weight_cube = np.sqrt(w1 * w2)

        k_per_full = psutil.l_to_k(data_cube1.ru * 2 * np.pi, self.z)

        k_per = np.repeat(k_per_full[np.newaxis, :], len(self.k_par), axis=0)
        k_par = np.repeat(self.k_par[:, np.newaxis], len(data_cube1.ru), axis=1)

        k_mean, k_std, dsp, dsp_err, n_eff = pscart.get_3d_cross_power_spectre(dft_cube1, dft_cube2, kbins,
                                                                               k_per, k_par, weight_cube=weight_cube,
                                                                               return_complex=return_complex)
        _, _, _, dsp1_err, _ = pscart.get_3d_cross_power_spectre(
            dft_cube1, dft_cube1, kbins, k_per, k_par, weight_cube=weight_cube)
        _, _, _, dsp2_err, _ = pscart.get_3d_cross_power_spectre(
            dft_cube2, dft_cube2, kbins, k_per, k_par, weight_cube=weight_cube)

        dsp = dsp * ps2d_norm
        dsp_err = np.sqrt(dsp1_err * dsp2_err) * ps2d_norm * ps_err_norm

        dsp, dsp_err = self._handle_cov_err_cross(dsp, dsp_err, self.ps3d_cov_cache,
                                                  data_cube1, data_cube2, with_cov_err,
                                                  kbins, weighted=weighted)

        return SphericalPowerSpectra(dsp, dsp_err, kbins, k_mean, n_eff=n_eff, k_std=k_std)


class PowerSpectraSph(BasePowerSpectra):

    def __init__(self, eor_bin, ps_config, primary_beam):
        """PowerSpectraGenerator class for alm PS computation

        Power spectra is defined by:
            P(k) = (X^2 Y) / (Omega B) V^2(k)

        with:
            X: angular to comoving distance
            Y: frequency to comoving distance
            Omega: Primary beam normalization factor
            B: Frequency bandwidth

        Args:
            eor_bin (EorBin): An EoR bin
            ps_config (PowerSpectraConfig): A PS configuration
            primary_beam (PrimaryBeam): The primary beam of the instrument
        """

        BasePowerSpectra.__init__(self, eor_bin, ps_config, primary_beam)

    def get_ps_norm(self, alm_cube):
        # Normalization factor for 1D (spacial/frequency) PS
        return self.X ** 2 / self.get_omega(alm_cube.meta)

    def get_omega(self, cube_meta):
        '''Primary Beam normalization factor'''
        mask = sphcube.SphWindowFunction.from_meta(cube_meta, primary_beam=self.primary_beam)
        omega = mask.get_power(cube_meta)

        return omega

    def get_fsky(self, cube_meta):
        mask = sphcube.SphWindowFunction.from_meta(cube_meta, primary_beam=self.primary_beam)
        return mask.get_area(cube_meta, normalize=True)

    def get_ps2d(self, alm_cube, with_cov_err=True):
        ''' Return cylindrically averaged power spectra of alm_cube (n_freqs, n_modes)'''
        alm_cube = self.eor.get_slice(alm_cube)
        ps2d_norm = self.get_ps2d_norm(alm_cube)
        f_delay, dft_alm_cube = self.delay_transform(alm_cube)

        delay = psutil.get_delay(alm_cube.freqs, M=self.eor.M, dx=self.config.df, half=self.ps2d_pos_only)
        ps2d = pssph.get_2d_power_spectra(dft_alm_cube, alm_cube.ll, alm_cube.mm, half=self.ps2d_pos_only)

        ps2d = ps2d * ps2d_norm

        data_el = np.unique(alm_cube.ll)
        f_sky = self.get_fsky(alm_cube.meta)
        f_sky = min(1, 2 * f_sky ** 0.5)

        el = self.el
        bins = np.array([el[0] - 1] + [a + (b - a) / 2. for a, b in psutil.pairwise(el)] + [el[-1] + 1])

        ps2d, _, _ = pscart.stats.binned_statistic(data_el, ps2d, bins=bins)
        ps2d_err = np.sqrt(2 / ((2 * el + 1) * f_sky)) * ps2d

        k_per = psutil.l_to_k(el, self.z)

        ps2d, ps2d_err = self._handle_cov_err(ps2d, ps2d_err, self.ps2d_cov_cache, alm_cube, with_cov_err)

        return CylindricalPowerSpectra(ps2d, ps2d_err, delay, el, k_per, self.k_par)

    def get_ps(self, alm_cube, with_cov_err=True):
        ''' Return spatial power spectra of alm_cube (n_freqs, n_modes)'''

        alm_cube = self.eor.get_slice(alm_cube)
        ps_norm = self.get_ps_norm(alm_cube)

        ps = pssph.get_power_spectra(alm_cube.data, alm_cube.ll, alm_cube.mm)
        ps = ps * ps_norm

        data_el = np.unique(alm_cube.ll)
        f_sky = self.get_fsky(alm_cube.meta)
        f_sky = min(1, 2 * f_sky ** 0.5)

        el = self.el
        bins = np.array([el[0] - 1] + [a + (b - a) / 2. for a, b in psutil.pairwise(el)] + [el[-1] + 1])

        ps, _, _ = pscart.stats.binned_statistic(data_el, ps, bins=bins)
        ps_err = np.sqrt(2 / ((2 * el + 1) * f_sky)) * ps

        k_per = psutil.l_to_k(el, self.z)

        ps, ps_err = self._handle_cov_err(ps, ps_err, self.ps_cov_cache, alm_cube, with_cov_err)

        return SpatialPowerSpectra(ps, ps_err, self.eor.freqs, el, k_per)

    def get_ps3d(self, kbins, alm_cube, with_cov_err=True):
        ''' Return spherically averaged power spectra of alm_cube (n_freqs, n_modes) '''
        alm_cube = self.eor.get_slice(alm_cube)

        ps2d = self.get_ps2d(alm_cube, with_cov_err=with_cov_err)

        f_sky = self.get_fsky(alm_cube.meta)

        ps3d, ps3d_err, k_mean = pssph.get_3d_power_spectra(ps2d.data, ps2d.k_per, ps2d.k_par,
                                                            self.el, f_sky, kbins)

        return SphericalPowerSpectra(ps3d, ps3d_err, kbins, k_mean)

    def get_ps3d_with_noise(self, kbins, ft_cube, noise_cube, with_cov_err=True):
        a = self.get_ps3d(kbins, ft_cube, with_cov_err=with_cov_err)
        n = self.get_ps3d(kbins, noise_cube, with_cov_err=with_cov_err)

        return a - n

    def get_cl(self, alm_cube, with_cov_err=True):
        ''' Return spatial power spectra of data_cube'''
        ps = self.get_ps(alm_cube, with_cov_err=with_cov_err)
        ps.data = ps.data / self.X ** 2
        ps.err = ps.err / self.X ** 2
        ps.cl = True
        return ps

    def get_variance(self, alm_cube, with_cov_err=True):
        cl = self.get_cl(alm_cube, with_cov_err=with_cov_err)
        var = (cl.data * cl.el * (cl.el.max() - cl.el.min())).sum(axis=1) / (2 * np.pi * len(cl.el))
        var_err = ((cl.err * cl.el * (cl.el.max() - cl.el.min())) ** 2).sum(axis=1) ** 0.5 / (2 * np.pi * len(cl.el))

        return Variance(var, var_err, cl.freqs)


class PowerSpectraMath(object):

    def __add__(self, other):
        return self.new_with_data(self.data + other.data, np.sqrt(self.err ** 2 + other.err ** 2), self.w + other.w)

    def __sub__(self, other):
        return self.new_with_data(self.data - other.data, np.sqrt(self.err ** 2 + other.err ** 2), self.w + other.w)

    def __mul__(self, other):
        if psutil.is_number(other):
            return self.new_with_data(other * self.data, other * self.err, other * self.w)
        elif isinstance(other, (list, np.ndarray)) and len(other) == len(self.data):
            return self.new_with_data(np.array(other) * self.data, np.array(other) * self.err, self.w + other.w)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        a = self.data
        ea = self.err
        b = other.data
        eb = other.err
        return self.new_with_data(a / b, abs(a / b) * np.sqrt((ea / a) ** 2 + (eb / b) ** 2), self.w + other.w)

    def temp_conversion(self, d, e, mkelvin=False, kelvin_square=False):
        if mkelvin:
            d = d * 1e6
            e = e * 1e6
        if not kelvin_square:
            d = np.sqrt(d)
            e = e / (2 * d)

        d = np.clip(d, 1e-10, 1e99)

        temp_unit = '%sK%s' % ('m' * mkelvin, '^2' * kelvin_square)
        return d, e, temp_unit


class Variance(PowerSpectraMath):

    def __init__(self, var, var_err, freqs, var_w=1):
        self.data = var
        self.err = var_err
        self.w = var_w
        self.freqs = freqs

    def freq_binning(self, df):
        assert df > psutil.robust_freq_width(self.freqs)

        fbins = np.arange(self.freqs.min(), self.freqs.max() + df, df)
        d, _, _ = stats.binned_statistic(self.freqs, self.data, bins=fbins)
        f, _, _ = stats.binned_statistic(self.freqs, self.freqs, bins=fbins)
        fct_err = lambda a: 1 / len(a) * np.sqrt((a ** 2).sum())
        e, _, _ = stats.binned_statistic(self.freqs, self.err, bins=fbins, statistic=fct_err)

        return Variance(d, e, f)

    def new_with_data(self, var, var_err, var_w=1):
        return Variance(var, var_err, self.freqs, var_w=1)

    def plot(self, ax=None, df=None, nsigma=1, title=None, mkelvin=True, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        if df is not None:
            v = self.freq_binning(df)
            d = v.data
            e = v.err
            f = v.freqs
        else:
            d = self.data
            e = self.err
            f = self.freqs

        if mkelvin:
            d = d * 1e6
            e = e * 1e6

        ax.errorbar(f * 1e-6, d, nsigma * e, **kargs)
        ax.set_yscale('log', **nonpos_arg)
        ax.set_xlabel(r"$\mathrm{Frequency\,[MHz]}$")

        if mkelvin:
            ax.set_ylabel(r"$\mathrm{Variance\,[mK^2]}$")
        else:
            ax.set_ylabel(r"$\mathrm{Variance\,[K^2]}$")

        if title is not None:
            ax.set_title(title)


class SpatialPowerSpectra(PowerSpectraMath):

    def __init__(self, ps, ps_err, freqs, el, k_per, cl=False, n_eff=None, ps_w=1):
        """Spatial power spectra

        Args:
            ps (n_freqs, n_el): power spectra
            freqs (n_freqs): Frequencies
            el (n_el): l modes
            k_per (n_el): k_per
        """
        self.data = ps
        self.err = ps_err
        self.freqs = freqs
        self.el = el
        self.k_per = k_per
        self.cl = cl
        self.n_eff = n_eff
        self.w = ps_w

        if self.n_eff is None:
            self.n_eff = np.zeros_like(self.data)

    def new_with_data(self, ps, ps_err, ps_w=1):
        return SpatialPowerSpectra(ps, ps_err, self.freqs, self.el, self.k_per, cl=self.cl, ps_w=ps_w)

    def plot(self, ax=None, title=None, k_only=True, fill_gap=True, text=None,
             log_norm=True, l_lambda=False, normalize=False, imaginary_part=False, **kargs):
        """Plot the power spectra

        Args:
            ax (None, optional): Axis to use, if None create a new figure
            log_norm (bool, optional): Plot intensity in log norm
        """
        if ax is None:
            fig, ax = plt.subplots()

        fmhz = self.freqs * 1e-6

        if not self.cl and self.k_per is not None:
            extent = (min(self.k_per), max(self.k_per), min(fmhz), max(fmhz))
            ax.set_xlabel(r'$k_{\bot}\,[\mathrm{h\,cMpc^{-1}]}$')
            if not k_only:
                axb = ax.twiny()
                axb.set_xlim(min(self.el), max(self.el))
                axb.set_xlabel(r'$\ell$')
        else:
            if l_lambda:
                x = self.el / (2 * np.pi)
                ax.set_xlabel(r'$|\mathbf{u}|\,[\lambda]$')
            else:
                x = self.el
                ax.set_xlabel(r'$\ell$')
            extent = (min(x), max(x), min(fmhz), max(fmhz))

        if fill_gap:
            ps = psutil.fill_gaps(self.data, psutil.get_gaps(self.freqs * 1e6))
        else:
            ps = self.data

        if imaginary_part:
            if not np.iscomplexobj(ps):
                print('Warning: PS is not complex. Use return_complex=True to produce complex cross-spectra.')
            ps = ps.imag
        else:
            ps = ps.real

        if normalize:
            if self.cl:
                ps = self.el * (self.el + 1) * ps
            else:
                ps = self.k_per ** 2 * ps / (2 * np.pi)

        if log_norm and 'norm' not in kargs:
            kargs['norm'] = LogNorm(vmin=kargs.get('vmin'), vmax=kargs.get('vmax'))
            kargs['vmin'] = None
            kargs['vmax'] = None

        cbs = psutil.ColorbarSetting(psutil.ColorbarOutterPosition())

        im_mappable = ax.imshow(ps, aspect='auto', extent=extent, **kargs)
        cbs.add_colorbar(im_mappable, ax)
        ax.set_ylabel("Frequency (MHz)")

        if not k_only:
            # Hack to fix the second axes (http://stackoverflow.com/questions/34979781)
            fig.canvas.draw()
            axb.set_position(ax.get_position())

        if title is not None:
            ax.set_title(title)

        if text is not None:
            ax.text(0.03, 0.92, text, transform=ax.transAxes, ha='left', fontsize=11)

    def plot_kper(self, ax=None, nsigma=0, fill_std=False, normalize=False, mkelvin=True,
                  kelvin_square=True, weighted=True, l_lambda=False, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        if weighted and isinstance(self.w, np.ndarray):
            y = psutil.nanaverage(self.data, self.w, axis=0)
            y_err = np.sqrt(np.nansum((self.err * self.w) ** 2, axis=0)) / np.nansum(self.w, axis=0)
        else:
            y = np.nanmean(self.data, axis=0)
            y_err = np.sqrt(np.nansum(self.err ** 2, axis=0)) / len(self.freqs)

        y, y_err, temp_unit = self.temp_conversion(y, y_err, mkelvin=mkelvin, kelvin_square=kelvin_square)

        if normalize:
            if self.cl:
                y = self.el * (self.el + 1) * y
                y_err = self.el * (self.el + 1) * y_err
            else:
                y = self.k_per ** 2 * y / (2 * np.pi)
                y_err = self.k_per ** 2 * y_err / (2 * np.pi)

        if self.cl:
            x = self.el
            ax.set_xlabel(r'$\ell$')
            if normalize:
                ax.set_ylabel(r'$\ell (\ell + 1) C_{\ell}\,[\mathrm{%s}]$' % temp_unit)
            else:
                ax.set_ylabel(r'$C_{\ell}\,[\mathrm{%s}]$' % temp_unit)
        else:
            x = self.k_per
            ax.set_xlabel(r'$k_{\bot}\,[\mathrm{h\,cMpc^{-1}}]$')
            if normalize:
                ax.set_ylabel(r'$\Delta^2 (k_{\bot})\,[\mathrm{%s}]$' % temp_unit)
            else:
                ax.set_ylabel(r'$P(k_{\bot})\,[\mathrm{%s\,h^{-3}\,cMpc^3}]$' % temp_unit)

        if l_lambda:
            x = self.el / (2 * np.pi)
            ax.set_xlabel(r'$|\mathbf{u}|\,[\lambda]$')

        if fill_std and nsigma > 0:
            ax.fill_between(x, y - nsigma * y_err, y + nsigma * y_err,
                            alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
            ax.plot(x, y, **kargs)
        elif nsigma > 0:
            ax.errorbar(x, y, nsigma * y_err, **kargs)
        else:
            ax.plot(x, y, **kargs)
        ax.set_yscale('log', **nonpos_arg)

    def save_to_txt(self, filename):
        k_pers, freqs = np.meshgrid(self.k_per, self.freqs)
        ru, _ = np.meshgrid(self.el / (2 * np.pi), self.freqs)
        freqs = freqs * 1e-6

        array_data = np.array([freqs.T.flatten(), k_pers.T.flatten(), ru.flatten(),
                               self.data.flatten(), self.err.flatten(), self.n_eff.flatten()]).T

        header = 'Spatial Power Spectra n_freqs=%s, n_kper=%s\n' % (len(self.freqs), len(self.k_per))
        header += ('Freq (MHz), k_per (h cMpc^-1), Baseline (lambda), '
                   'P (K^2 h^-2 cMpc^2), P_err (K^2 h^-2 cMpc^2), N_eff\n')

        np.savetxt(filename, array_data, fmt='%14.8f', header=header, delimiter=' ')

    @staticmethod
    def load(filename, z=None):
        array = np.loadtxt(filename).T
        if array.shape[0] == 4:
            freqs, k_pers, data, err = array
            k_per = np.unique(k_pers)
            freqs = np.unique(freqs) * 1e6
            data = data.reshape(len(freqs), len(k_per))
            err = err.reshape(len(freqs), len(k_per))
            n_eff = None

            if z is not None:
                ll = psutil.k_to_l(k_per, z)
            else:
                ll = k_per
        else:
            freqs, k_pers, ru, data, err, n_eff = array
            k_per = np.unique(k_pers)
            freqs = np.unique(freqs) * 1e6
            data = data.reshape(len(freqs), len(k_per))
            err = err.reshape(len(freqs), len(k_per))
            n_eff = n_eff.reshape(len(freqs), len(k_per))
            ll = 2 * np.pi * np.unique(ru)

        return SpatialPowerSpectra(data, err, freqs, ll, k_per, n_eff=n_eff)


class CylindricalPowerSpectra(PowerSpectraMath):

    def __init__(self, ps2d, ps2d_err, delay, el, k_per, k_par, n_eff=None, ps2d_w=1):
        """Cylindrically averaged power spectra.

        Args:
            ps2d (n_delay, n_el): power spectra
            delay (n_delay): delays (in second)
            el (n_el): l modes
            k_per (n_el): k per
            k_par (n_delay): k par
        """
        self.data = ps2d
        self.err = ps2d_err
        self.delay = delay * 1e6
        self.el = el
        self.k_per = k_per
        self.k_par = k_par
        self.n_eff = n_eff
        self.w = ps2d_w

        if self.n_eff is None:
            self.n_eff = np.zeros_like(self.data)

    def new_with_data(self, ps2d, ps2d_err, ps2d_w=1):
        return CylindricalPowerSpectra(ps2d, ps2d_err, self.delay, self.el, self.k_per,
                                       self.k_par, ps2d_w=ps2d_w)

    def plot(self, ax=None, title=None, k_only=True, log_norm=True, colorbar=True,
             log_axis=False, ax_cb=None, text=None, dimensionless=False,
             wedge_lines=[], z=None, imaginary_part=False, **kargs):
        """Plot the 2D power spectra

        Args:
            ax (None, optional): Axis to use, if None create a new figure
            title (None, optional): Title of the Axis
            k_only (bool, optional): Plot only k_per, k_par. Default: True
            log_norm (bool, optional): Plot intensity in log norm
            colorbar (bool, optional): Add a colorbar
            log_axis (bool, optional): Plot axis in log norm
        """
        if ax is None:
            fig, ax = plt.subplots()
        pad = '5%'

        if self.k_par.min() <= 0 and log_axis:
            print('Negative k_par: disabling log_axis')
            log_axis = False

        if self.k_per is not None:
            extent = (min(self.k_per), max(self.k_per), min(self.k_par), max(self.k_par))
            ax.set_xlabel(r'$k_{\bot}\,\mathrm{[h\,cMpc^{-1}]}$')
            ax.set_ylabel(r'$k_{\parallel}\,\mathrm{[h\,cMpc^{-1}]}$')
            if not k_only:
                axb = ax.twiny()
                axb.set_xlim(min(self.el), max(self.el))
                axc = ax.twinx()
                axc.set_ylim(min(self.delay), max(self.delay))
                axb.set_xlabel('l')
                axc.set_ylabel("Delay (us)")
                pad = '15%'
        else:
            extent = (min(self.el), max(self.el), min(self.delay), max(self.delay))
            ax.set_xlabel('l')
            ax.set_ylabel("Delay (us)")

        if log_norm and 'norm' not in kargs:
            kargs['norm'] = LogNorm(vmin=kargs.get('vmin'), vmax=kargs.get('vmax'))
            kargs['vmin'] = None
            kargs['vmax'] = None

        if colorbar:
            cbs = psutil.ColorbarSetting(psutil.ColorbarOutterPosition(pad=pad))

        if dimensionless:
            k = np.sqrt(self.k_par[:, None] ** 2 + self.k_per[None, :] ** 2)
            data = self.data * k ** 3 / (2 * np.pi ** 2)
        else:
            data = self.data

        if imaginary_part:
            if not np.iscomplexobj(data):
                print('Warning: PS is not complex. Use return_complex=True to produce complex cross-spectra.')
            data = data.imag
        else:
            data = data.real

        if log_axis:
            x = np.log10(self.k_per)
            y = np.log10(self.k_par)
            xx, yy = np.meshgrid(x, y)
            im_mappable = ax.pcolormesh(xx, yy, data, **kargs)

            # Set the ticks to be in log scale
            major = np.arange(np.floor(x.min()), np.ceil(x.max()))
            minor = (major[:, None] + np.log10(np.arange(2, 10))).flatten()
            ax.set_xticks(major)
            ax.set_xticks(minor, minor=True)

            major = np.arange(np.floor(y.min()), np.ceil(y.max()))
            minor = (major[:, None] + np.log10(np.arange(2, 10))).flatten()
            ax.set_yticks(major)
            ax.set_yticks(minor, minor=True)

            ax.set_xlim(x.min(), x.max())
            ax.set_ylim(y.min(), y.max())

            ax.set_xticklabels([r'$\mathregular{10^{%d}}$' % v for v in ax.get_xticks()])
            ax.set_yticklabels([r'$\mathregular{10^{%d}}$' % v for v in ax.get_yticks()])
        else:
            im_mappable = ax.imshow(data, aspect='auto', extent=extent, **kargs)

        if colorbar:
            if ax_cb is None:
                ax_cb = ax
            cbs.add_colorbar(im_mappable, ax_cb)

        if not k_only:
            # Hack to fix the second axes (http://stackoverflow.com/questions/34979781)
            ax.get_figure().canvas.draw()
            axb.set_position(ax.get_position())
            axc.set_position(ax.get_position())

        if title is not None:
            ax.set_title(title)

        if text is not None:
            ax.text(0.03, 0.92, text, transform=ax.transAxes, ha='left', fontsize=11)

        for wedge in wedge_lines:
            ax.set_autoscale_on(False)
            if log_axis:
                ax.plot(np.log10(self.k_per), np.log10(psutil.wedge_fct(np.radians(wedge), z,
                                                                        self.k_per)),
                        c='grey', ls='-', lw=0.8)
            else:
                ax.plot(self.k_per, psutil.wedge_fct(np.radians(wedge), z, self.k_per),
                        c='grey', ls='-', lw=0.8)

    def plot_kpar(self, ax=None, nsigma=0, fill_std=False, delay=False, weighted=True, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        if weighted and isinstance(self.w, np.ndarray):
            y = psutil.nanaverage(self.data, self.w, axis=1)
            y_err = np.sqrt(np.nansum((self.err * self.w) ** 2, axis=1)) / np.nansum(self.w, axis=1)
        else:
            y = np.nanmean(self.data, axis=1)
            y_err = np.sqrt(np.nansum(self.err ** 2, axis=1)) / len(self.k_per)

        if delay:
            x = self.delay
        else:
            x = self.k_par

        if fill_std and nsigma > 0:
            ax.fill_between(x, y - nsigma * y_err, y + nsigma * y_err,
                            alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
            ax.plot(x, y, **kargs)
        elif nsigma > 0:
            ax.errorbar(x, y, nsigma * y_err, **kargs)
        else:
            ax.plot(x, y, **kargs)
        ax.set_yscale('log', **nonpos_arg)

        if delay:
            ax.set_xlabel('Delay (us)')
        else:
            ax.set_xlabel(r'$k_{\parallel}\,[\mathrm{h\,cMpc^{-1}}]$')

        ax.set_ylabel(r'$P(k_{\parallel})\,[\mathrm{K^2\,h^{-3}\,cMpc^3}]$')

    def plot_kper(self, ax=None, nsigma=0, fill_std=False, normalize=False, weighted=True, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        if weighted and isinstance(self.w, np.ndarray):
            y = psutil.nanaverage(self.data, self.w, axis=0)
            y_err = np.sqrt(np.nansum((self.err * self.w) ** 2, axis=0)) / np.nansum(self.w, axis=0)
        else:
            y = np.nanmean(self.data, axis=0)
            y_err = np.sqrt(np.nansum(self.err ** 2, axis=0)) / len(self.k_par)

        if normalize:
            y = self.k_per ** 2 * y / (2 * np.pi)
            y_err = self.k_per ** 2 * y_err / (2 * np.pi)

        if fill_std and nsigma > 0:
            ax.fill_between(self.k_per, y - nsigma * y_err, y + nsigma * y_err,
                            alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
            ax.plot(self.k_per, y, **kargs)
        elif nsigma > 0:
            ax.errorbar(self.k_per, y, nsigma * y_err, **kargs)
        else:
            ax.plot(self.k_per, y, **kargs)
        ax.set_yscale('log', **nonpos_arg)

        ax.set_xlabel(r'$k_{\bot}\,[\mathrm{h\,cMpc^{-1}}]$')

        if normalize:
            ax.set_ylabel(r'$\Delta^2 (k_{\bot})\,[\mathrm{K^2}]$')
        else:
            ax.set_ylabel(r'$P(k_{\bot})\,[\mathrm{K^2\,h^{-3}\,cMpc^3}]$')

    def save_to_txt(self, filename):
        k_pers, k_pars = np.meshgrid(self.k_per, self.k_par)
        ru, delay = np.meshgrid(self.el / (2 * np.pi), self.delay)
        array_data = np.array([k_pars.flatten(), k_pers.flatten(),
                               delay.flatten(), ru.flatten(),
                               self.data.flatten(), self.err.flatten(),
                               self.n_eff.flatten()]).T
        header = 'Cylindrically averaged Power Spectra n_kper=%s, n_kpar=%s\n' % (len(self.k_per), len(self.k_par))
        header += ('k_par (h cMpc^-1), k_per (h cMpc^-1), Delay (us), Baseline (lambda), '
                   'P (K^2 h^-3 cMpc^3), P_err (K^2 h^-3 cMpc^3), N_eff\n')
        np.savetxt(filename, array_data, fmt='%14.8f', header=header, delimiter=' ')

    @staticmethod
    def load(filename, z=None):
        array = np.loadtxt(filename).T
        if array.shape[0] == 4:
            k_pars, k_pers, data, err = array
            k_par = np.unique(k_pars)
            k_per = np.unique(k_pers)
            data = data.reshape(len(k_par), len(k_per))
            err = err.reshape(len(k_par), len(k_per))
            n_eff = None

            if z is not None:
                delay = psutil.k_to_delay(k_par, z)
                ll = psutil.k_to_l(k_per, z)
            else:
                delay = k_par
                ll = k_per
        else:
            k_pars, k_pers, delay, ru, data, err, n_eff = array
            k_par = np.unique(k_pars)
            k_per = np.unique(k_pers)
            data = data.reshape(len(k_par), len(k_per))
            err = err.reshape(len(k_par), len(k_per))
            n_eff = n_eff.reshape(len(k_par), len(k_per))
            delay = 1e-6 * np.unique(delay)
            ll = 2 * np.pi * np.unique(ru)

        return CylindricalPowerSpectra(data, err, delay, ll, k_per, k_par, n_eff=n_eff)


class SphericalPowerSpectra(PowerSpectraMath):

    def __init__(self, ps3d, ps3d_err, k_bins, k_mean, ps3d_q16=None, ps3d_q84=None, n_eff=None, k_std=None):
        self.data = ps3d
        self.err = ps3d_err
        self.q16 = ps3d_q16
        self.q84 = ps3d_q84
        self.k_bins = k_bins
        self.k_mean = k_mean
        self.n_eff = n_eff
        self.k_std = k_std
        self.w = 1

        if self.k_std is None:
            self.k_std = np.zeros_like(self.k_mean)

        if self.n_eff is None:
            self.n_eff = np.zeros_like(self.k_mean)

        if self.q16 is not None:
            self.err = (self.q84 - self.q16) / 2.

    def new_with_data(self, ps3d, ps3d_err, ps3d_w=1):
        return SphericalPowerSpectra(ps3d, ps3d_err, self.k_bins, self.k_mean, n_eff=self.n_eff, k_std=self.k_std)

    def get(self, mkelvin=True, kelvin_square=False):
        d, e, unit = self.temp_conversion(self.data, self.err, mkelvin=mkelvin, kelvin_square=kelvin_square)
        return d, e

    def get_upper(self, nsigma=2, mkelvin=True, kelvin_square=False):
        d, e = self.get(mkelvin=mkelvin, kelvin_square=True)

        if kelvin_square:
            return d + nsigma * e
        else:
            return np.sqrt(d + nsigma * e)

    def plot(self, ax=None, nsigma=2, marker='+', mkelvin=True, kelvin_square=True,
             title=None, fill_std=False, kerr_as_kbins=False, imaginary_part=False, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        d, e, temp_unit = self.temp_conversion(self.data, self.err, mkelvin=mkelvin, kelvin_square=kelvin_square)

        if imaginary_part:
            if not np.iscomplexobj(d):
                print('Warning: PS is not complex. Use return_complex=True to produce complex cross-spectra.')
            d = d.imag
        else:
            d = d.real

        if fill_std and nsigma > 0:
            if self.q16 is not None and nsigma == 1:
                q16, _, _ = self.temp_conversion(self.q16, self.err, mkelvin=mkelvin, kelvin_square=kelvin_square)
                q84, _, _ = self.temp_conversion(self.q84, self.err, mkelvin=mkelvin, kelvin_square=kelvin_square)
                ax.fill_between(self.k_mean, q16, q84, alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
                ax.plot(self.k_mean, d, marker=marker, **kargs)
            else:
                ax.fill_between(self.k_mean, np.clip(d - nsigma * e, 1e-10, 1e99), d + nsigma * e,
                                alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
                ax.plot(self.k_mean, d, marker=marker, **kargs)
        elif nsigma > 0:
            if kerr_as_kbins:
                k_err = np.stack([self.k_mean - self.k_bins[0:-1], self.k_bins[1:] - self.k_mean])
                ax.errorbar(self.k_mean, d, yerr=nsigma * e, xerr=k_err, marker=marker, **kargs)
            else:
                ax.errorbar(self.k_mean, d, yerr=nsigma * e, marker=marker, **kargs)
        else:
            ax.plot(self.k_mean, d, marker=marker, **kargs)

        ax.set_yscale('log', **nonpos_arg)
        ax.set_xscale('log')

        ax.set_ylabel(r'$\Delta%s (k)\,[\mathrm{%s}]$' % ('^2' * kelvin_square, temp_unit))
        ax.set_xlabel(r'$k\,[\mathrm{h\,cMpc^{-1}}]$')

        ax.set_xlim(self.k_bins.min(), self.k_bins.max())

        if title is not None:
            ax.set_title(title)

    def save_to_txt(self, filename):
        array_data = np.array([self.k_bins[:-1], self.k_bins[1:], self.k_mean,
                               self.k_std, self.data * 1e6, self.err * 1e6, self.n_eff]).T
        header = 'Spherically averaged Power Spectra n_k=%s\n' % (len(self.k_mean))
        header += (r'k_min (h cMpc^-1), k_max (h cMpc^-1), k_mean (h cMpc^-1), k_std (h cMpc^-1), '
                   r'\Delta^2 (mK^2), \Delta_err^2 (mK^2), N_eff\n')
        np.savetxt(filename, array_data, fmt='%14.8f', header=header, delimiter=' ')

    @staticmethod
    def load_from_txt(filename):
        array = np.loadtxt(filename).T
        if array.shape[0] == 3:
            k_mean, data, err = array
            kbins = np.hstack([k_mean, k_mean[-1]])
            k_std = None
            n_eff = None
        elif array.shape[0] == 7:
            k_min, k_max, k_mean, k_std, data, err, n_eff = array
            kbins = np.hstack([k_min, k_max[-1]])
        else:
            raise ValueError('Format of input file incorrect')

        return SphericalPowerSpectra(data * 1e-6, err * 1e-6, kbins, k_mean, n_eff=n_eff, k_std=k_std)


class FourPanelPsResults(object):

    def __init__(self, ps_gen, kbins, figsize=(10, 8)):
        self.ps_gen = ps_gen
        self.kbins = kbins
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(ncols=2, nrows=2, figsize=figsize)
        self.lgd = None

    def add_cube(self, cube, label, ps_gen=None, **kargs):
        if ps_gen is None:
            ps_gen = self.ps_gen
        ps_gen.get_variance(cube).plot(ax=self.ax1, label=label, **kargs)
        ps_gen.get_ps3d(self.kbins, cube).plot(ax=self.ax2, label=label, **kargs)
        ps_gen.get_ps2d(cube).plot_kpar(ax=self.ax3, label=label, **kargs)
        ps_gen.get_ps2d(cube).plot_kper(ax=self.ax4, label=label, **kargs)

    def add_cube_ps_diff(self, cube1, cube2, label, ps_gen=None, **kargs):
        if ps_gen is None:
            ps_gen = self.ps_gen
        (ps_gen.get_variance(cube1) - ps_gen.get_variance(cube2)).plot(ax=self.ax1, label=label, **kargs)
        (ps_gen.get_ps2d(cube1) - ps_gen.get_ps2d(cube2)).plot_kpar(ax=self.ax3, label=label, **kargs)
        (ps_gen.get_ps2d(cube1) - ps_gen.get_ps2d(cube2)).plot_kper(ax=self.ax4, label=label, **kargs)
        ps_gen.get_ps3d_with_noise(self.kbins, cube1, cube2).plot(ax=self.ax2, label=label, **kargs)

    def add_ps_stacker(self, ps_stacker, label, **kargs):
        ps_stacker.get_variance().plot(ax=self.ax1, label=label, **kargs)
        ps_stacker.get_ps3d().plot(ax=self.ax2, label=label, **kargs)
        ps_stacker.get_ps2d().plot_kpar(ax=self.ax3, label=label, **kargs)
        ps_stacker.get_ps2d().plot_kper(ax=self.ax4, label=label, **kargs)

    def done(self, ncol_legend=3):
        self.lgd = self.fig.legend(*self.ax1.get_legend_handles_labels(),
                                   bbox_to_anchor=(0.5, 1.04), loc="upper center", ncol=ncol_legend)
        self.fig.tight_layout()

    def savefig(self, filename, **kargs):
        if self.lgd is None:
            print('Warning: run done() before savefig()')
        else:
            self.fig.savefig(filename, bbox_extra_artists=(self.lgd,), bbox_inches='tight')


class ThreePanelPsResults(object):

    def __init__(self, ps_gen, kbins, figsize=(10, 5), norm_factor=1, n_cols=1, dpi=100):
        self.ps_gen = ps_gen
        self.kbins = kbins
        self.norm_factor = norm_factor
        self.fig, self.axs = plt.subplots(ncols=n_cols, nrows=3, figsize=figsize, squeeze=False, sharey='row', dpi=dpi)
        self.lgd = None

    def add_cube(self, cube, label, ps_gen=None, col=0, **kargs):
        if ps_gen is None:
            ps_gen = self.ps_gen
        (self.norm_factor * ps_gen.get_ps3d(self.kbins, cube)).plot(ax=self.axs[0, col], label=label, **kargs)
        (self.norm_factor * ps_gen.get_ps2d(cube)).plot_kpar(ax=self.axs[1, col], label=label, **kargs)
        (self.norm_factor * ps_gen.get_ps2d(cube)).plot_kper(ax=self.axs[2, col], label=label, **kargs)

    def add_cube_ps_diff(self, cube1, cube2, label, ps_gen=None, col=0, **kargs):
        if ps_gen is None:
            ps_gen = self.ps_gen
        (self.norm_factor * (ps_gen.get_ps2d(cube1) - ps_gen.get_ps2d(cube2))).plot_kpar(ax=self.axs[0, col], label=label, **kargs)
        (self.norm_factor * (ps_gen.get_ps2d(cube1) - ps_gen.get_ps2d(cube2))).plot_kper(ax=self.axs[1, col], label=label, **kargs)
        (self.norm_factor * ps_gen.get_ps3d_with_noise(self.kbins, cube1, cube2)).plot(ax=self.axs[2, col], label=label, **kargs)

    def add_ps_stacker(self, ps_stacker, label, col=0, **kargs):
        (self.norm_factor * ps_stacker.get_ps3d()).plot(ax=self.axs[0, col], label=label, **kargs)
        (self.norm_factor * ps_stacker.get_ps2d()).plot_kpar(ax=self.axs[1, col], label=label, **kargs)
        (self.norm_factor * ps_stacker.get_ps2d()).plot_kper(ax=self.axs[2, col], label=label, **kargs)

    def done(self, ncol_legend=3, col_legend=0, **kargs):
        self.lgd = self.fig.legend(*self.axs[0, col_legend].get_legend_handles_labels(),
                                   bbox_to_anchor=(0.5, 1.04), loc="upper center", ncol=ncol_legend, **kargs)
        for ax in self.axs[:, 1:].flatten():
            ax.set_ylabel('')
        self.fig.tight_layout()

    def savefig(self, filename, **kargs):
        if self.lgd is None:
            print('Warning: run done() before savefig()')
        else:
            self.fig.savefig(filename, bbox_extra_artists=(self.lgd,), bbox_inches='tight')


class MultiNight2DPowerSpectra(PowerSpectraMath):

    def __init__(self, ps, err, x, xlabel, y, ylabel):
        self.data = ps
        self.err = err
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = ylabel

    def new_with_data(self, data, err):
        return MultiNight2DPowerSpectra(data, err, self.x, self.xlabel, self.y, self.ylabel)

    def plot(self, ax=None, log_norm=True, colorbar=True, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        if log_norm and 'norm' not in kargs:
            kargs['norm'] = LogNorm(vmin=kargs.get('vmin'), vmax=kargs.get('vmax'))
            kargs['vmin'] = None
            kargs['vmax'] = None

        cbs = psutil.ColorbarSetting(psutil.ColorbarOutterPosition())

        if isinstance(self.y[0], str):
            extent = (min(self.x), max(self.x), 0, len(self.y))
        else:
            extent = (min(self.x), max(self.x), min(self.y), max(self.y))

        im_mappable = ax.imshow(self.data, aspect='auto', extent=extent, **kargs)
        if colorbar:
            cbs.add_colorbar(im_mappable, ax)

        if isinstance(self.y[0], str):
            ax.set_yticks(np.arange(len(self.y)) + 0.5)
            ax.set_yticklabels(self.y)

        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)


class PowerSpectraMC(object):

    def __init__(self, all_ps):
        self.all_ps = all_ps
        self.med = np.median(np.array([ps.data for ps in self.all_ps]), axis=0)
        self.std = psutil.robust_std(np.array([ps.data for ps in self.all_ps]), axis=0)
        self.q16 = np.quantile(np.array([ps.data for ps in self.all_ps]), .16, axis=0)
        self.q84 = np.quantile(np.array([ps.data for ps in self.all_ps]), .84, axis=0)
        self.q2_5 = np.quantile(np.array([ps.data for ps in self.all_ps]), .025, axis=0)
        self.q97_5 = np.quantile(np.array([ps.data for ps in self.all_ps]), .975, axis=0)
        self.p0 = self.all_ps[0]

    def __operation__(self, other, op):
        all_ps = []
        for ps in self.all_ps:
            if isinstance(other, PowerSpectraMC):
                all_ps.append(op(ps, np.random.choice(other.all_ps)))
            else:
                all_ps.append(op(ps, other.new_with_data(np.random.normal(other.data, other.err), other.err)))

        return self.__class__(all_ps)

    def __add__(self, other):
        return self.__operation__(other, operator.add)

    def __sub__(self, other):
        return self.__operation__(other, operator.sub)

    def __mul__(self, other):
        if psutil.is_number(other):
            return self.__class__([k.new_with_data(other * k.data, other * k.err, other * k.w) for k in self.all_ps])
        else:
            return self.__operation__(other, operator.mul)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        return self.__operation__(other, operator.truediv)

    def get_data(self, mkelvin=False):
        a = 1
        temp_unit = 'K'
        if mkelvin:
            a = 1e6
            temp_unit = 'mK'

        return a * self.med, a * self.q16, a * self.q84, a * self.q2_5, a * self.q97_5, temp_unit



class SphericalPowerSpectraMC(PowerSpectraMC, SphericalPowerSpectra):

    def __init__(self, ps3d_all):
        PowerSpectraMC.__init__(self, ps3d_all)
        SphericalPowerSpectra.__init__(self, self.med, self.std, self.p0.k_bins, self.p0.k_mean,
                                             n_eff=self.p0.n_eff, k_std=self.p0.k_std,
                                             ps3d_q16=self.q16, ps3d_q84=self.q84)

    def get_upper(self, nsigma=2, mkelvin=True, kelvin_square=False):
        if nsigma == 1:
            u = self.q84
        elif nsigma == 2:
            u = self.q97_5
        else:
            raise ValueError('nsigma must be 1 or 2')
        if mkelvin:
            u = u * 1e6
        if not kelvin_square:
            u = np.sqrt(u)

        return u

    def plot(self, ax=None, show68=True, show95=True, marker='+', mkelvin=True,
             title=None, kerr_as_kbins=False, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        d, q16, q84, q2_5, q97_5, temp_unit = self.get_data(mkelvin=mkelvin)

        if show68:
            ax.fill_between(self.k_mean, q16, q84, alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
        if show95:
            ax.fill_between(self.k_mean, q2_5, q97_5, alpha=0.5 * kargs.get('alpha', 0.5), color=kargs.get('c', None))

        ax.plot(self.k_mean, d, marker=marker, **kargs)

        ax.set_yscale('log', **nonpos_arg)
        ax.set_xscale('log')

        ax.set_ylabel(r'$\Delta^2 (k)\,[\mathrm{%s}^2]$' % temp_unit)
        ax.set_xlabel(r'$k\,[\mathrm{h\,cMpc^{-1}}]$')

        ax.set_xlim(self.k_bins.min(), self.k_bins.max())

        if title is not None:
            ax.set_title(title)

    def save(self, filename):
        data = [p.data for p in self.all_ps]
        err = [p.err for p in self.all_ps]
        a = [self.k_bins, self.k_mean, self.k_std, data, err, self.n_eff]
        with h5py.File(filename, 'w') as hf:
            for d, l in zip(a, ['k_bins', 'k_mean', 'k_std', 'data', 'err', 'n_eff']):
                if d is not None:
                    hf.create_dataset(l, data=d)
        self.save_to_txt(os.path.splitext(filename)[0] + '.txt')

    def save_to_txt(self, filename):
        array_data = np.array([self.k_bins[:-1], self.k_bins[1:], self.k_mean,
                               self.k_std, self.med * 1e6, self.q2_5 * 1e6, self.q16 * 1e6, 
                               self.q84 * 1e6, self.q97_5 * 1e6, self.n_eff]).T
        header = 'Spherically averaged Power Spectra n_k=%s\n' % (len(self.k_mean))
        header += (r'k_min (h cMpc^-1), k_max (h cMpc^-1), k_mean (h cMpc^-1), k_std (h cMpc^-1), '
                   r'\Delta^2 (mK^2), \Delta_q2.5^2 (mK^2), \Delta_q16^2 (mK^2), \Delta_q84^2 (mK^2), \Delta_q97.5^2 (mK^2), N_eff\n')
        np.savetxt(filename, array_data, fmt='%14.8f', header=header, delimiter=' ')

    @staticmethod
    def load(filename):
        with h5py.File(filename, 'r') as hf:
            data = hf.get('data')[:]
            err = hf.get('err')[:]
            k_bins = hf.get('k_bins')[:]
            k_mean = hf.get('k_mean')[:]
            k_std = hf.get('k_std', default=None)
            if k_std is not None:
                k_std = k_std[()]
            n_eff = hf.get('n_eff', default=None)
            if n_eff is not None:
                n_eff = n_eff[()]
        all_ps = [SphericalPowerSpectra(d, e, k_bins, k_mean, n_eff=n_eff, k_std=k_std)
                  for d, e in zip(data, err)]

        return SphericalPowerSpectraMC(all_ps)


class CylindricalPowerSpectraMC(PowerSpectraMC, CylindricalPowerSpectra):

    def __init__(self, all_ps2d):
        PowerSpectraMC.__init__(self, all_ps2d)
        CylindricalPowerSpectra.__init__(self, self.med, self.std, self.p0.delay, self.p0.el, self.p0.k_per, 
                                               self.p0.k_par, n_eff=self.p0.n_eff, ps2d_w=self.p0.w)

    def plot_kpar(self, ax=None, show68=True, show95=True, delay=False, weighted=True, mkelvin=False, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        d, q16, q84, q2_5, q97_5, temp_unit = self.get_data(mkelvin=mkelvin)

        if weighted and isinstance(self.w, np.ndarray):
            y, q16, q84, q2_5, q97_5 = psutil.nanaverage(np.array([d, q16, q84, q2_5, q97_5]),
                                                         self.w[None], axis=2)
        else:
            y, q16, q84, q2_5, q97_5 = np.nanmean([d, q16, q84, q2_5, q97_5], axis=2)

        if delay:
            x = self.delay
        else:
            x = self.k_par

        if show68:
            ax.fill_between(x, q16, q84, alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
        if show95:
            ax.fill_between(x, q2_5, q97_5, alpha=0.5 * kargs.get('alpha', 0.5), color=kargs.get('c', None))

        ax.plot(x, y, **kargs)

        ax.set_yscale('log', **nonpos_arg)

        if delay:
            ax.set_xlabel('Delay (us)')
        else:
            ax.set_xlabel(r'$k_{\parallel}\,[\mathrm{h\,cMpc^{-1}}]$')

        ax.set_ylabel(r'$P(k_{\parallel})\,[\mathrm{%s^2\,h^{-3}\,cMpc^3}]$' % temp_unit)

    def plot_kper(self, ax=None, show68=True, show95=True, normalize=False, weighted=True, mkelvin=False, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        d, q16, q84, q2_5, q97_5, temp_unit = self.get_data(mkelvin=mkelvin)

        if weighted and isinstance(self.w, np.ndarray):
            y, q16, q84, q2_5, q97_5 = psutil.nanaverage(np.array([d, q16, q84, q2_5, q97_5]),
                                                         self.w[None], axis=1)
        else:
            y, q16, q84, q2_5, q97_5 = np.nanmean([d, q16, q84, q2_5, q97_5], axis=1)

        if normalize:
            n = self.k_per ** 2 / (2 * np.pi)
            y, q16, q84, q2_5, q97_5 = [n * k for k in (y, q16, q84, q2_5, q97_5)]

        x = self.k_per

        if show68:
            ax.fill_between(x, q16, q84, alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
        if show95:
            ax.fill_between(x, q2_5, q97_5, alpha=0.5 * kargs.get('alpha', 0.5), color=kargs.get('c', None))

        ax.plot(x, y, **kargs)

        ax.set_yscale('log', **nonpos_arg)

        ax.set_xlabel(r'$k_{\bot}\,[\mathrm{h\,cMpc^{-1}}]$')

        if normalize:
            ax.set_ylabel(r'$\Delta^2 (k_{\bot})\,[\mathrm{%s^2}]$' % temp_unit)
        else:
            ax.set_ylabel(r'$P(k_{\bot})\,[\mathrm{%s^2\,h^{-3}\,cMpc^3}]$' % temp_unit)

    def save(self, filename):
        data = [p.data for p in self.all_ps]
        err = [p.err for p in self.all_ps]
        a = [self.delay, self.el, self.k_per, self.k_par, data, err, self.w]
        with h5py.File(filename, 'w') as hf:
            for d, l in zip(a, ['delay', 'el', 'k_per', 'k_par', 'data', 'err', 'ps2d_w']):
                hf.create_dataset(l, data=d)

    @staticmethod
    def load(filename):
        with h5py.File(filename, 'r') as hf:
            data = hf.get('data')[:]
            err = hf.get('err')[:]
            el = hf.get('el')[:]
            delay = hf.get('delay')[:]
            k_per = hf.get('k_per')[:]
            k_par = hf.get('k_par')[:]
            ps2d_w = hf.get('ps2d_w')[()]
        all_ps = [CylindricalPowerSpectra(d, e, delay, el, k_per, k_par, ps2d_w=ps2d_w)
                  for d, e in zip(data, err)]

        return CylindricalPowerSpectraMC(all_ps)


class VarianceMC(PowerSpectraMC, Variance):

    def __init__(self, all_var):
        PowerSpectraMC.__init__(self, all_var)
        Variance.__init__(self, self.med, self.std, self.p0.freqs, var_w=self.p0.w)

    def plot(self, ax=None, show68=True, show95=True, mkelvin=True, title=None, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        d, q16, q84, q2_5, q97_5, temp_unit = self.get_data(mkelvin=mkelvin)
        f = self.freqs * 1e-6

        if show68:
            ax.fill_between(f, q16, q84, alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
        if show95:
            ax.fill_between(f, q2_5, q97_5, alpha=0.5 * kargs.get('alpha', 0.25), color=kargs.get('c', None))

        ax.plot(f, d, **kargs)

        ax.set_yscale('log', **nonpos_arg)
        ax.set_xlabel(r"$\mathrm{Frequency\,[MHz]}$")

        ax.set_ylabel(r"$\mathrm{Variance\,[%s^2]}$" % temp_unit)

        if title is not None:
            ax.set_title(title)

    def save(self, filename):
        data = [p.data for p in self.all_ps]
        err = [p.err for p in self.all_ps]
        a = [self.freqs, data, err]
        with h5py.File(filename, 'w') as hf:
            for d, l in zip(a, ['freqs', 'data', 'err']):
                hf.create_dataset(l, data=d)

    @staticmethod
    def load(filename):
        with h5py.File(filename, 'r') as hf:
            data = hf.get('data')[:]
            err = hf.get('err')[:]
            freqs = hf.get('freqs')[:]
        all_ps = [Variance(d, e, freqs) for d, e in zip(data, err)]

        return VarianceMC(all_ps)


class SpatialPowerSpectraMC(PowerSpectraMC, SpatialPowerSpectra):

    def __init__(self, all_var):
        PowerSpectraMC.__init__(self, all_var)
        SpatialPowerSpectra.__init__(self, self.med, self.std, self.p0.freqs, self.p0.el, 
                                           self.p0.k_per, cl=self.p0.cl, n_eff=self.p0.n_eff, ps_w=self.p0.w)

    def plot_kper(self, ax=None, show68=True, show95=True, normalize=False,
                  weighted=True, l_lambda=False, mkelvin=True, **kargs):
        if ax is None:
            fig, ax = plt.subplots()

        d, q16, q84, q2_5, q97_5, temp_unit = self.get_data(mkelvin=mkelvin)

        if weighted and isinstance(self.w, np.ndarray):
            y, q16, q84, q2_5, q97_5 = psutil.nanaverage(np.array([d, q16, q84, q2_5, q97_5]), self.w[None], axis=1)
        else:
            y, q16, q84, q2_5, q97_5 = np.nanmean([d, q16, q84, q2_5, q97_5], axis=1)

        if normalize:
            if self.cl:
                n = self.el * (self.el + 1)
            else:
                n = self.k_per ** 2 / (2 * np.pi)
            y, q16, q84, q2_5, q97_5 = [n * k for k in (y, q16, q84, q2_5, q97_5)]

        if self.cl:
            x = self.el
            ax.set_xlabel(r'$\ell$')
            if normalize:
                ax.set_ylabel(r'$\ell (\ell + 1) C_{\ell}\,[\mathrm{%s}]$' % temp_unit)
            else:
                ax.set_ylabel(r'$C_{\ell}\,[\mathrm{%s}]$' % temp_unit)
        else:
            x = self.k_per
            ax.set_xlabel(r'$k_{\bot}\,[\mathrm{h\,cMpc^{-1}}]$')
            if normalize:
                ax.set_ylabel(r'$\Delta^2 (k_{\bot})\,[\mathrm{%s}]$' % temp_unit)
            else:
                ax.set_ylabel(r'$P(k_{\bot})\,[\mathrm{%s\,h^{-3}\,cMpc^3}]$' % temp_unit)

        if l_lambda:
            x = self.el / (2 * np.pi)
            ax.set_xlabel(r'$|\mathbf{u}|\,[\lambda]$')

        if show68:
            ax.fill_between(x, q16, q84, alpha=kargs.get('alpha', 0.5), color=kargs.get('c', None))
        if show95:
            ax.fill_between(x, q2_5, q97_5, alpha=0.5 * kargs.get('alpha', 0.25), color=kargs.get('c', None))

        ax.plot(x, y, **kargs)

        ax.set_yscale('log', **nonpos_arg)


    def save(self, filename):
        data = [p.data for p in self.all_ps]
        err = [p.err for p in self.all_ps]
        a = [self.freqs, data, err, self.el, self.k_per, self.w]
        with h5py.File(filename, 'w') as hf:
            for d, l in zip(a, ['freqs', 'data', 'err', 'el', 'k_per', 'ps_w']):
                hf.create_dataset(l, data=d)

    @staticmethod
    def load(filename):
        with h5py.File(filename, 'r') as hf:
            data = hf.get('data')[:]
            err = hf.get('err')[:]
            freqs = hf.get('freqs')[:]
            el = hf.get('el')[:]
            k_per = hf.get('k_per')[:]
            ps_w = hf.get('ps_w')[()]

        all_ps = [SpatialPowerSpectra(d, e, freqs, el, k_per) for d, e in zip(data, err)]

        return VarianceMC(all_ps)


class PsStacker(object):

    def __init__(self, ps_gen, kbins):
        self.all_ps3d = []
        self.all_ps = []
        self.all_ps2d = []
        self.all_var = []
        self.ps_gen = ps_gen
        self.kbins = kbins

    def add(self, cube):
        if self.ps_gen is None or self.kbins is None:
            print('Warning: can not add a datacube to a loaded PsStacker')
            return

        self.all_ps3d.append(self.ps_gen.get_ps3d(self.kbins, cube))
        self.all_ps.append(self.ps_gen.get_ps(cube))
        self.all_ps2d.append(self.ps_gen.get_ps2d(cube))
        self.all_var.append(self.ps_gen.get_variance(cube))

    def get_ps(self):
        return SpatialPowerSpectraMC(self.all_ps)

    def get_ps2d(self):
        return CylindricalPowerSpectraMC(self.all_ps2d)

    def get_variance(self):
        return VarianceMC(self.all_var)

    def get_ps3d(self):
        return SphericalPowerSpectraMC(self.all_ps3d)

    def save(self, dir_path, name):
        self.get_ps3d().save(os.path.join(dir_path, f'{name}.ps3d.h5'))
        self.get_ps2d().save(os.path.join(dir_path, f'{name}.ps2d.h5'))
        self.get_variance().save(os.path.join(dir_path, f'{name}.variance.h5'))
        self.get_ps().save(os.path.join(dir_path, f'{name}.ps.h5'))

    @staticmethod
    def load(dir_path, name):
        ps_stacker = PsStacker(None, None)
        ps_stacker.all_ps3d = SphericalPowerSpectraMC.load(os.path.join(dir_path, f'{name}.ps3d.h5')).all_ps
        ps_stacker.all_ps2d = CylindricalPowerSpectraMC.load(os.path.join(dir_path, f'{name}.ps2d.h5')).all_ps
        ps_stacker.all_ps = SpatialPowerSpectraMC.load(os.path.join(dir_path, f'{name}.ps.h5')).all_ps
        ps_stacker.all_var = VarianceMC.load(os.path.join(dir_path, f'{name}.variance.h5')).all_ps

        return ps_stacker
