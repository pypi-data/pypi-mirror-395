# Function and class to estimate experiments sensitivity
#
# Authors: F.Mertens


import os
import itertools
from enum import Enum, auto

import numpy as np

import scipy.interpolate

from astropy import units
import astropy.constants as const
from astropy.coordinates import EarthLocation

from fast_histogram import histogram2d

INSTRU_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instru')


class CoordinateType(Enum):
    """Enumeration of coordinate systems used to interpret station positions."""

    ENU = auto()   # East-North-Up (local topocentric)
    ECEF = auto()  # Earth-Centered, Earth-Fixed (global geodetic)
    XYZ = auto()   # Rotated Cartesian XYZ used for UVW conversion


def enu_to_ecef(location, enu):
    """ Convert ENU coordinates to ECEF coordinates.

    Args:
        location (astropy.coordinates.EarthLocation): Reference geodetic location.
        enu (np.ndarray): ENU coordinates, shape (N, 3), in meters.

    Returns:
        np.ndarray: ECEF coordinates, shape (N, 3), in meters.
    """
    e, n, u = np.hsplit(enu, 3)

    lon = location.geodetic[0].to(units.rad).value
    lat = location.geodetic[1].to(units.rad).value
    alt = location.geodetic[2].to(units.m).value

    x, y, z = lla_to_ecef(lat, lon, alt)
    sin_lat, cos_lat = np.sin(lat), np.cos(lat)
    sin_lon, cos_lon = np.sin(lon), np.cos(lon)

    X = x - sin_lon * e - sin_lat * cos_lon * n + cos_lat * cos_lon * u
    Y = y + cos_lon * e - sin_lat * sin_lon * n + cos_lat * sin_lon * u
    Z = z + cos_lat * n + sin_lat * u

    return np.hstack([X, Y, Z])


def ecef_to_xyz_matrix(long_rad):
    """ Rotation matrix from ECEF to interferometric XYZ.

    Args:
        long_rad (float): Longitude in radians.

    Returns:
        np.ndarray: 3×3 rotation matrix.
    """
    return np.array([
        [ np.cos(long_rad),  np.sin(long_rad), 0],
        [-np.sin(long_rad),  np.cos(long_rad), 0],
        [0,                  0,                1]
    ])


def lla_to_ecef(lat, lon, alt):
    """Convert latitude, longitude, altitude to ECEF coordinates (WGS84).

    Args:
        lat (float): Geodetic latitude in radians.
        lon (float): Geodetic longitude in radians.
        alt (float): Height above ellipsoid in meters.

    Returns:
        tuple of float: Cartesian ECEF coordinates (x, y, z) in meters.
    """
    WGS84_a = 6378137.0
    WGS84_b = 6356752.31424518

    N = WGS84_a**2 / np.sqrt(
        WGS84_a**2 * np.cos(lat)**2 + WGS84_b**2 * np.sin(lat)**2
    )

    x = (N + alt) * np.cos(lat) * np.cos(lon)
    y = (N + alt) * np.cos(lat) * np.sin(lon)
    z = ((WGS84_b**2 / WGS84_a**2) * N + alt) * np.sin(lat)

    return x, y, z


def xyz_to_uvw_matrix(ha_rad, dec_rad):
    """Compute the rotation matrix from celestial coordinates (HA, Dec) to UVW.

    Args:
        ha_rad (float): Hour angle in radians.
        dec_rad (float): Declination in radians.

    Returns:
        np.ndarray: 3x3 transformation matrix from XYZ to UVW.
    """
    return np.array([
        [ np.sin(ha_rad),                      np.cos(ha_rad),                      0.0],
        [-np.sin(dec_rad) * np.cos(ha_rad),   np.sin(dec_rad) * np.sin(ha_rad),   np.cos(dec_rad)],
        [ np.cos(dec_rad) * np.cos(ha_rad),  -np.cos(dec_rad) * np.sin(ha_rad),   np.sin(dec_rad)]
    ])


class Telescope(object):
    """Abstract base class representing a generic radio telescope configuration.

    This class defines the key parameters and methods that any telescope subclass
    should implement or override, such as retrieving station positions and computing
    effective area or SEFD.

    Attributes:
        name (str): Name identifier of the telescope.
        pb_name (str): Name of the primary beam model.
        n_elements_per_stations (int): Number of antenna elements per station.
        only_drift_mode (bool): Whether the telescope supports only drift-scan mode.
        redundant_array (bool): Whether the array has a redundant layout.
        redundant_baselines (list of float): List of redundant baseline lengths (in meters).
        umin (float): Minimum baseline length in wavelengths.
        umax (float): Maximum baseline length in wavelengths.
        coord_type (CoordinateType): Coordinate system used for station positions.
        location (EarthLocation): Geodetic location of the array reference center.
    """

    name = 'none'
    pb_name = name
    n_elements_per_stations = 1
    only_drift_mode = False
    redundant_array = False
    redundant_baselines = []
    umin = 0
    umax = 10000
    coord_type = CoordinateType.ENU
    location = EarthLocation(lon=6.8670 * units.deg, lat=52.9088 * units.deg, height=15.0 * units.m)

    def get_stat_pos_file(self):
        """Return the path to the file containing station positions.

        Returns:
            str: Path to the file (should be overridden in subclasses).
        """
        pass


    def get_sefd(self, freq):
        """Compute the per-pol System Equivalent Flux Density (SEFD) at given frequency.

        Args:
            freq (np.ndarray or float): Frequency in Hz.

        Returns:
            np.ndarray or float: SEFD in Jy. Must be overridden by subclasses.
        """
        pass

    def get_i_sefd(self, freq):
        """Compute the Stokes I System Equivalent Flux Density (SEFD) at given frequency.

        Args:
            freq (np.ndarray or float): Frequency in Hz.

        Returns:
            np.ndarray or float: SEFD in Jy. Must be overridden by subclasses.
        """

        return 1 / np.sqrt(2) * self.get_sefd(freq)

    def sky_temperature(self, freq, tsys_sky=60, temp_power_law_index=2.55):
        """Compute sky temperature using a power-law approximation.

        Args:
            freq (np.ndarray or float): Frequency in Hz.
            tsys_sky (float, optional): Sky temperature at 1 m wavelength (default: 60 K).
            temp_power_law_index (float, optional): Spectral index (default: 2.55).

        Returns:
            np.ndarray or float: Estimated sky temperature in Kelvin.
        """
        lamb = const.c.value / freq
        return tsys_sky * lamb ** temp_power_law_index

    def get_dipole_aeff(self, freq, distance_between_dipole):
        """Compute effective area of a dipole.

        Args:
            freq (np.ndarray or float): Frequency in Hz.
            distance_between_dipole (float): Physical spacing between dipoles in meters.

        Returns:
            np.ndarray or float: Effective area in m².
        """
        lamb = const.c.value / freq
        return np.min([lamb ** 2 / 3, np.ones_like(lamb) * np.pi * distance_between_dipole ** 2 / 4.], axis=0)

    def get_dish_aeff(self, freq, diameter, efficiency):
        """Compute effective area of a parabolic dish.

        Args:
            freq (np.ndarray or float): Frequency in Hz.
            diameter (float): Diameter of the dish in meters.
            efficiency (float): Aperture efficiency factor (typically ~0.7–0.8).

        Returns:
            np.ndarray or float: Effective area in m².
        """
        lamb = const.c.value / freq
        return lamb ** 2 / (4 * np.pi) * efficiency * (np.pi * diameter / lamb) ** 2

    @staticmethod
    def from_name(name):
        """Instantiate a telescope object by name.

        Args:
            name (str): Name of the telescope (e.g., 'ska_low', 'lofar_hba').

        Returns:
            Telescope: Instance of the corresponding Telescope subclass.

        Raises:
            ValueError: If no matching telescope subclass is found.
        """
        klasses = Telescope.__subclasses__()
        [klasses.extend(k.__subclasses__()) for k in klasses[:]]

        for klass in klasses:
            if hasattr(klass, 'name') and klass.name == name:
                return klass()

        raise ValueError('No telescope with name: %s' % name)


class DEx(Telescope):
    """Conceptual lunar dipole array with square grid layout."""

    name = 'dex'
    umin = 0.5
    umax = 25
    fov = 120
    du = 1
    only_drift_mode = True
    pb_name = name
    pb_name = 'ant_5_1.02_gaussian'
    coord_type = CoordinateType.ENU
    location = EarthLocation(lon=116.67081524 * units.deg, lat=-26.70122102627586 * units.deg, height=0.0 * units.m)

    def __init__(self, n_antenna_side=32, sep_antenna=6):
        Telescope.__init__(self)
        self.sep_antenna = sep_antenna
        self.n_antenna_side = n_antenna_side

    def get_stat_pos(self):
        grid_indices = np.arange(0, self.n_antenna_side)
        p_east, p_north = np.meshgrid(self.sep_antenna * grid_indices, self.sep_antenna * grid_indices)
        
        east = p_east.flatten()
        north = p_north.flatten()
        up = np.zeros_like(east)

        return np.vstack((east, north, up)).T

    def get_sefd(self, freq, tsys_sky=60):
        tsys = self.sky_temperature(freq, tsys_sky)
        a_eff = self.get_dipole_aeff(freq, self.sep_antenna)
        return 2 * const.k_B.value / a_eff * 1e26 * tsys


class SkaLow(Telescope):
    """SKA-Low Phase 1 array (AA4)."""

    name = 'ska_low'
    umin = 30
    umax = 250
    fov = 3
    du = 8
    pb_name = name
    coord_type = CoordinateType.ENU
    location = EarthLocation.from_geodetic(116.7644482, -26.82472208, 365.0, ellipsoid="WGS84")

    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'ska1_low_enu_statpos.data')

    def get_sefd(self, freq, tsys_sky=60):
        # Specification extracted from SKA LFAA Station design report document (https://arxiv.org/pdf/2003.12744v2.pdf).
        # See Page 22 of the report. SKALA v4 is actually expected to be better than the spec.
        freqs_spec = np.array([50, 80, 110, 140, 160, 220]) * 1e6
        a_eff_over_tsys_spec = 1 * np.array([0.14, 0.46, 1.04, 1.15, 1.2, 1.2])
        def t_sky_fct(freqs): return tsys_sky * (3e8 / freqs) ** 2.55
        a_eff_fct = scipy.interpolate.interp1d(freqs_spec, a_eff_over_tsys_spec * t_sky_fct(freqs_spec), 
                                               kind='slinear', bounds_error=False, fill_value='extrapolate')

        return 2 * const.k_B.value * 1e26 * t_sky_fct(freq) / a_eff_fct(freq)


class SkaLowAAstar(SkaLow):
    """SKA-Low AA* layout."""

    name = 'ska_low_aastar'

    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'ska1_low_aastar_enu_statpos.data')


class SkaLowAA2(SkaLow):
    """SKA-Low AA2 layout."""

    name = 'ska_low_aa2'

    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'ska1_low_aa2_enu_statpos.data')


class LofarHBA(Telescope):
    """LOFAR High-Band Antenna (HBA) core array."""

    name = 'lofar_hba'
    umin = 50
    umax = 250
    fov = 4
    du = 8
    n_elements_per_stations = 2
    pb_name = name
    coord_type = CoordinateType.ECEF
    location = EarthLocation(lon=6.8670 * units.deg, lat=52.9088 * units.deg, height=15.0 * units.m)

    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'lofar_statpos.data')

    def get_sefd(self, freq):
        # Typical observed SEFD ~ 130-160 MHz @ NCP (see https://old.astron.nl/radio-observatory/astronomers/lofar-imaging-capabilities-sensitivity/sensitivity-lofar-array/sensiti)
        return 4000


class A12HBA(Telescope):
    """AARTFAAC-12 LOFAR HBA subarray with 48-element stations."""

    name = 'a12_hba'
    umin = 10
    umax = 200
    fov = 24
    du = 2
    pb_name = name
    n_elements_per_stations = 48
    coord_type = CoordinateType.ECEF
    location = EarthLocation(lon=6.8670 * units.deg, lat=52.9088 * units.deg, height=15.0 * units.m)

    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'aartfaac_a12_hba_statpos.data')

    def get_sefd(self, freq):
        # Typical observed SEFD of LOFAR-HBA between ~ 130-160 MHz @ NCP (see https://old.astron.nl/radio-observatory/astronomers/lofar-imaging-capabilities-sensitivity/sensitivity-lofar-array/sensiti)
        # LOFAR-HBA core is composed of 24 tiles. So S_tile = S_station * 24
        return 4000 * 24


class A12LBA(Telescope):
    """AARTFAAC-12 LOFAR LBA subarray with wide FoV and drift scan."""

    name = 'a12_lba'
    umin = 20
    umax = 40
    fov = 120
    du = 1
    pb_name = 'ant_1.9_1.1_gaussian'
    n_elements_per_stations = 48
    only_drift_mode = True
    coord_type = CoordinateType.ECEF
    location = EarthLocation(lon=6.8670 * units.deg, lat=52.9088 * units.deg, height=15.0 * units.m)

    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'aartfaac_a12_lba_statpos.data')

    def get_sefd(self, freq, tsys_sky=60):
        distance_between_dipole = 7
        tsys = self.sky_temperature(freq, tsys_sky)
        a_eff = self.get_dipole_aeff(freq, distance_between_dipole)

        return 2 * const.k_B.value / a_eff * 1e26 * tsys


class MWA1(Telescope):
    """First-phase MWA core layout."""

    name = 'mwa1'
    umin = 18
    umax = 80
    fov = 30
    du = 2
    pb_name = 'ant_4_1.05_gaussian'
    only_drift_mode = False
    coord_type = CoordinateType.ECEF
    location = EarthLocation(lon=116.67044463048276 * units.deg, lat=-26.70122102627586 * units.deg, height=377.8 * units.m)


    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'mwa_rev1_statpos.data')

    def get_sefd(self, freq, tsys_sky=60):
        distance_between_dipole = 1.1
        n_dipole_per_stations = 4 * 4
        tsys = self.sky_temperature(freq, tsys_sky)
        a_eff = n_dipole_per_stations * self.get_dipole_aeff(freq, distance_between_dipole)

        return 2 * const.k_B.value / a_eff * 1e26 * tsys


class HERA(Telescope):
    """HERA telescope core array with redundant hexagonal layout."""

    name = 'hera'
    pb_name = 'ant_14_1.1_gaussian'
    only_drift_mode = True
    redundant_array = True
    redundant_baselines = np.array([14.6, 25.28794179, 29.2, 38.62796914, 43.8, 
                                    50.57588358, 52.64104862, 58.4, 63.63992458, 
                                    66.90560515, 73., 75.86382537, 77.25593828, 
                                    81.2893597, 87.6])
    umin = 4
    umax = 200
    du = 1
    coord_type = CoordinateType.ENU
    hera_location = EarthLocation(lon=21.43 * units.deg, lat=-30.72 * units.deg, height=1050.0 * units.m)

    def __init__(self, hex_num=11, split_core=True, sep=14.6):
        self.hex_num = hex_num
        self.split_core = split_core
        self.sep = sep

    def get_stat_pos(self):
        # Taken from https://github.com/HERA-Team/hera_sim/blob/main/hera_sim/antpos.py. Credit: HERA team.
        positions = []
        for row in range(self.hex_num - 1, -self.hex_num + self.split_core, -1):
            # adding self.split_core deletes a row if it's true
            for col in range(2 * self.hex_num - abs(row) - 1):
                x_pos = self.sep * ((2 - (2 * self.hex_num - abs(row))) / 2 + col)
                y_pos = row * self.sep * np.sqrt(3) / 2
                positions.append([x_pos, y_pos, 0])
                
        # basis vectors (normalized to self.sep)
        up_right = self.sep * np.asarray([0.5, np.sqrt(3) / 2, 0])
        up_left = self.sep * np.asarray([-0.5, np.sqrt(3) / 2, 0])

        # split the core if desired
        if self.split_core:
            new_pos = []
            for pos in positions:
                # find out which sector the antenna is in
                theta = np.arctan2(pos[1], pos[0])
                if pos[0] == 0 and pos[1] == 0:
                    new_pos.append(pos)
                elif -np.pi / 3 < theta < np.pi / 3:
                    new_pos.append(np.asarray(pos) + (up_right + up_left) / 3)
                elif np.pi / 3 <= theta < np.pi:
                    new_pos.append(np.asarray(pos) + up_left - (up_right + up_left) / 3)
                else:
                    new_pos.append(pos)
            # update the positions
            positions = new_pos

        return np.array(positions)

    def get_sefd(self, freq, tsys_sky=60):
        d = 14
        eff = 0.78
        trxc = 100

        lamb = const.c.value / freq
        a_eff = self.get_dish_aeff(freq, d, eff)
        tsys = tsys_sky * lamb ** 2.55 + trxc
        return 2 * const.k_B.value / a_eff * 1e26 * tsys


class HERA56(HERA):
    """HERA sub-array with 56 antennas."""

    name = 'hera_56'

    def __init__(self):
        HERA.__init__(self, 5)


class HERA120(HERA):
    """HERA sub-array with 120 antennas."""

    name = 'hera_120'

    def __init__(self):
        HERA.__init__(self, 7)


class HERA208(HERA):
    """HERA sub-array with 208 antennas."""

    name = 'hera_208'

    def __init__(self):
        HERA.__init__(self, 9)


class HERA320(HERA):
    """HERA full array with 320 antennas."""

    name = 'hera_320'

    def __init__(self):
        HERA.__init__(self, 11)


class NenuFAR(Telescope):
    """Full NenuFAR array in Nançay (France)."""

    name = 'nenufar'
    pb_name = 'nenufar'
    umin = 6
    umax = 60
    fov = 16
    du = 4
    coord_type = CoordinateType.ECEF
    location = EarthLocation(lon=2.192400 * units.deg, lat=47.376511 * units.deg, height=182.096 * units.m)

    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'nenufar_full_statpos.data')

    def inst_temperature(self, freq):
        """ Instrument temperature at a given frequency ``freq``.

            From: https://github.com/AlanLoh/nenupy/blob/master/nenupy/instru/instru.py
        """
        lna_sky = np.array([
            5.0965, 2.3284, 1.0268, 0.4399, 0.2113, 0.1190, 0.0822, 0.0686,
            0.0656, 0.0683, 0.0728, 0.0770, 0.0795, 0.0799, 0.0783, 0.0751,
            0.0710, 0.0667, 0.0629, 0.0610, 0.0614, 0.0630, 0.0651, 0.0672,
            0.0694, 0.0714, 0.0728, 0.0739, 0.0751, 0.0769, 0.0797, 0.0837,
            0.0889, 0.0952, 0.1027, 0.1114, 0.1212, 0.1318, 0.1434, 0.1562,
            0.1700, 0.1841, 0.1971, 0.2072, 0.2135, 0.2168, 0.2175, 0.2159,
            0.2121, 0.2070, 0.2022, 0.1985, 0.1974, 0.2001, 0.2063, 0.2148,
            0.2246, 0.2348, 0.2462, 0.2600, 0.2783, 0.3040, 0.3390, 0.3846,
            0.4425, 0.5167, 0.6183, 0.7689, 1.0086, 1.4042, 2.0732
        ])
        lna_freqs = (np.arange(71) + 15) * 1e6
        return self.sky_temperature(freq) * scipy.interpolate.interp1d(lna_freqs, lna_sky,
                                                                       bounds_error=False,
                                                                       fill_value='extrapolate')(freq)

    def get_sefd(self, freq, tsys_sky=60):
        distance_between_dipole = 5.5
        n_dipole_per_stations = 19
        tsys = self.sky_temperature(freq, tsys_sky) + self.inst_temperature(freq)
        a_eff = n_dipole_per_stations * self.get_dipole_aeff(freq, distance_between_dipole)

        return 2 * const.k_B.value / a_eff * 1e26 * tsys


class NenuFAR80(NenuFAR):
    """Subset of NenuFAR using 80 mini-arrays."""

    name = 'nenufar_80'

    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'nenufar80_statpos.data')


class OVROLWA(Telescope):
    """OVRO-LWA dipole array in California with large FoV."""

    name = 'ovro_lwa'
    umin = 2
    umax = 60
    fov = 120
    du = 1
    pb_name = 'ant_1.9_1.1_gaussian'
    only_drift_mode = True
    coord_type = CoordinateType.ENU
    location = EarthLocation(lon=118.275 * units.deg, lat=37.2337 * units.deg, height=1222.0 * units.m)

    def get_stat_pos_file(self):
        return os.path.join(INSTRU_DIR, 'ovro-lwa_enu_statpos.data')

    def get_sefd(self, freq, tsys_sky=60):
        distance_between_dipole = 5
        tsys = self.sky_temperature(freq, tsys_sky)
        a_eff = self.get_dipole_aeff(freq, distance_between_dipole)

        return 2 * const.k_B.value / a_eff * 1e26 * tsys


class TelescopeSimu(object):
    """
    Simulates the UV coverage of a telescope array during an observation.

    This class combines the telescope configuration (antenna layout, beam model)
    with observing parameters (declination, hour angle range, frequency channels)
    to compute gridded baseline weights for EoR-like observations.

    Use `simu_uv`, `redundant_gridding` or `image_gridding` to generate UV coverage
    and create input for sensitivity or power spectrum estimation.
    """
    def __init__(self, telescop: Telescope, freqs, dec_deg, hal, har, umin=None, umax=None, timeres=100, remove_intra_baselines=True):
        """
        Parameters
        ----------
        telescop : Telescope
            Telescope instance describing the array layout and instrument model.
        freqs : array_like
            Array of observing frequencies in Hz.
        dec_deg : float
            Target declination in degrees.
        hal : float
            Start hour angle of the observation (in hours).
        har : float
            End hour angle of the observation (in hours).
        umin : float, optional
            Minimum baseline in lambda. Defaults to telescope-defined value.
        umax : float, optional
            Maximum baseline in lambda. Defaults to telescope-defined value.
        timeres : float, optional
            Temporal resolution in seconds. Default is 100 s.
        remove_intra_baselines : bool, optional
            Whether to remove intra-station baselines for dense arrays. Default is True.
        """
        self.telescop = telescop
        self.freqs = freqs
        self.dec_deg = dec_deg
        self.hal = hal
        self.har = har
        self.umin = umin
        if self.umin is None:
            self.umin = telescop.umin
        self.umax = umax
        if self.umax is None:
            self.umax = telescop.umax
        self.timeres = timeres
        self.remove_intra_baselines = remove_intra_baselines

    @staticmethod
    def from_dict(d, freqs):
        def get_d_value(name, default=None):
            if default is None and not name in d:
                raise ValueError(f'{name} missing to initialize TelescopeSimu')
            return d.get(name, default)

        instru = get_d_value('PEINSTRU')
        dec_deg = get_d_value('PEOBSDEC')
        hal = get_d_value('PEOBSHAL')
        har = get_d_value('PEOBSHAR')
        timeres = get_d_value('PEOBSRES')
        remove_intra_baselines = get_d_value('PEREMINT')

        telescop = Telescope.from_name(instru)

        umin = get_d_value('PEOBSUMI', telescop.umin)
        umax = get_d_value('PEOBSUMA', telescop.umax)

        return TelescopeSimu(telescop, freqs, dec_deg, hal, har, umin=umin, umax=umax, 
                             timeres=timeres, remove_intra_baselines=remove_intra_baselines)

    def to_dict(self):
        return {'PEINSTRU': self.telescop.name, 'PEOBSDEC': self.dec_deg, 'PEOBSHAL': self.hal, 'PEOBSHAR': self.har,
                'PEOBSUMI': self.umin, 'PEOBSUMA': self.umax, 'PEOBSRES': self.timeres, 
                'PEREMINT': self.remove_intra_baselines}

    def get_XYZ_positions(self):
        """Get station positions in XYZ coordinates based on telescope's coordinate type.

        Returns:
            np.ndarray: Transformed positions in XYZ coordinates with shape (N, 3).
        """
        statpos = self.telescop.get_stat_pos()
        coord_type = self.telescop.coord_type
        location = self.telescop.location
        long_rad = location.lon.to(units.rad).value

        if coord_type == CoordinateType.ENU:
            # ENU → ECEF → XYZ
            ecef = enu_to_ecef(location, statpos)
            R = ecef_to_xyz_matrix(long_rad)
            return ecef @ R.T

        elif coord_type == CoordinateType.ECEF:
            # ECEF → XYZ
            R = ecef_to_xyz_matrix(long_rad)
            return statpos @ R.T

        elif coord_type == CoordinateType.XYZ:
            return statpos

        else:
            raise ValueError(f"Unsupported coordinate type: {coord_type}")

    def simu_uv(self, include_conj=True):
        """
        Simulate UVW coordinates for the telescope during the observation.

        Parameters
        ----------
        include_conj : bool, optional
            If True, also include the complex conjugate baselines (-u, -v). Default is True.

        Returns
        -------
        tuple of np.ndarray
            Arrays of u, v, w coordinates in meters.
        """
        from ps_eor import psutil

        def m2a(m): return np.squeeze(np.asarray(m))

        lambs = const.c.value / self.freqs
        umin_meter = (self.umin * lambs).min()
        umax_meter = (self.umax * lambs).max()

        timev = np.arange(self.hal * 3600, self.har * 3600, self.timeres)

        statpos = self.telescop.get_stat_pos()
        nstat = statpos.shape[0]

        print('Simulating UV coverage ...')

        # All combinations of nant to generate baselines
        stncom = np.array(list(itertools.combinations(np.arange(0, nstat), 2)))
        print(f'Number of elements: {nstat}')
        print(f'Number of baselines: {stncom.shape[0]}')

        if self.remove_intra_baselines and self.telescop.n_elements_per_stations > 1:
            n_stations = nstat // self.telescop.n_elements_per_stations
            station_id = np.repeat(np.arange(n_stations), self.telescop.n_elements_per_stations)

            stncom_stations = np.array(list(itertools.combinations(station_id, 2)))
            idx = np.array([a == b for a, b, in stncom_stations]).astype(bool)
            stncom = stncom[~idx]
            print(f'Discarding {idx.sum()} intra-baselines')

        b1, b2 = zip(*stncom)

        uu = []
        vv = []
        ww = []

        pr = psutil.progress_report(len(timev))
        i = 0

        for tt in timev:
            pr(i)
            ha_rad = (tt / 3600.) * (15. / 180) * np.pi
            dec_rad = self.dec_deg * (np.pi / 180)
            
            XYZ = self.get_XYZ_positions()

            # from XYZ (rotated ECEF) to UVW
            R = xyz_to_uvw_matrix(ha_rad, dec_rad)
            UVW = XYZ @ R.T

            bu = m2a(UVW[b1, 0] - UVW[b2, 0])
            bv = m2a(UVW[b1, 1] - UVW[b2, 1])
            bw = m2a(UVW[b1, 2] - UVW[b2, 2])

            ru = np.sqrt(bu ** 2 + bv ** 2)
            idx = (ru > umin_meter) & (ru < umax_meter)

            uu.extend(bu[idx])
            vv.extend(bv[idx])
            ww.extend(bw[idx])

            if include_conj:
                uu.extend(- bu[idx])
                vv.extend(- bv[idx])
                ww.extend(bw[idx])

            i += 1

        return np.array(uu), np.array(vv), np.array(ww)

    def redundant_gridding(self, max_distance=1):
        """
        Grid baselines using a clustering algorithm, useful for redundant arrays.

        Parameters
        ----------
        max_distance : float, optional
            Maximum distance (in meters) between baselines to be considered equivalent. Default is 1.

        Returns
        -------
        SimuGridded
            Object containing the gridded weights cube and associated metadata.
        """
        import sklearn.cluster
        from ps_eor import psutil, datacube

        uu_meter, vv_meter, _ = self.simu_uv()

        X = np.array([uu_meter, vv_meter]).T
        c = sklearn.cluster.DBSCAN(eps=max_distance, min_samples=1)
        c.fit(X)

        c_id, idx, counts = np.unique(c.labels_, return_index=True, return_counts=True)

        uu_meter_grid = uu_meter[idx]
        vv_meter_grid = vv_meter[idx]

        meta = datacube.ImageMetaData.from_res(0.01, (100, 100))
        meta.wcs.wcs.cdelt[2] = psutil.robust_freq_width(self.freqs)
        meta.set('PEINTTIM', self.timeres)
        meta.set('PETOTTIM', (self.har - self.hal) * 3600)

        w_cube = datacube.CartWeightsCubeMeter(np.repeat(counts[None, :], len(self.freqs), 0), 
                                               uu_meter_grid, vv_meter_grid, self.freqs, meta)

        return SimuGridded(w_cube, self)

    def image_gridding(self, fov_deg, oversampling_factor=4, min_weight=10, win_fct=None):
        """
        Grid baselines onto a regular image grid using a simple binning scheme.

        This method computes a gridded UV sampling (weights) from the simulated baselines
        for each frequency channel. The resulting weights represent only the UV sampling
        density (redundancy) and are not modified by any window function.

        If a window function is provided via `win_fct`, it is attached to the output metadata
        for later use (e.g. for noise rescaling or power spectrum estimation), but it is NOT
        applied to the gridded weights at this stage.

        Parameters
        ----------
        fov_deg : float
            Field of view (in degrees) used to compute the UV cell spacing.
        oversampling_factor : int, optional
            Controls the UV grid resolution: res = 1 / (oversampling_factor * umax).
            Default is 4.
        min_weight : int, optional
            Minimum number of visibilities in a UV cell to include it. Default is 10.
        win_fct : WindowFunction, optional
            Window function to be stored in the metadata for later use. The window is
            not applied to the weights here.

        Returns
        -------
        SimuGridded
            Object containing the gridded weight cube and associated metadata.
        """
        from ps_eor import psutil, datacube

        uu_meter, vv_meter, _ = self.simu_uv()

        du = 1 / np.radians(fov_deg)
        res = 1 / (oversampling_factor * self.umax)
        n_u = int(np.ceil(1 / (res * du)))
        shape = (n_u, n_u)

        g_uu, g_vv = psutil.get_uv_grid(shape, res)

        ranges = [g_uu.min() - du / 2, g_uu.max() + du / 2]

        print('Gridding UV coverage ...')
        weights = []
        pr = psutil.progress_report(len(self.freqs))
        for i, lamb in enumerate(const.c.value / self.freqs):
            pr(i)
            w = histogram2d(uu_meter / lamb, vv_meter / lamb, bins=n_u, range=[ranges] * 2)
            weights.append(w)

        weights = np.array(weights)
        weights = weights.reshape(len(self.freqs), -1)
        g_uu = g_uu.flatten()
        g_vv = g_vv.flatten()
        ru = np.sqrt(g_uu ** 2 + g_vv ** 2)

        idx = (weights.min(axis=0) >= min_weight) & (ru >= self.umin) & (ru <= self.umax)
        weights = weights[:, idx]
        g_uu = g_uu[idx]
        g_vv = g_vv[idx]

        meta = datacube.ImageMetaData.from_res(res, shape)
        meta.wcs.wcs.cdelt[2] = psutil.robust_freq_width(self.freqs)
        meta.set('PEINTTIM', self.timeres)
        meta.set('PETOTTIM', (self.har - self.hal) * 3600)

        # Attach window function to metadata (do NOT modify weights here)
        if win_fct is not None:
            win_fct.to_meta(meta)

        w_cube = datacube.CartWeightCube(weights, g_uu, g_vv, self.freqs, meta)

        return SimuGridded(w_cube, self)


class SimuGridded(object):
    """Container for gridded telescope simulation weights and associated metadata."""

    def __init__(self, weights, telescope_simu):
        """
        Initialise the SimuGridded object.

        Args:
            weights: A CartWeightCube or CartWeightsCubeMeter object containing gridded weights.
            telescope_simu: A TelescopeSimu object describing the telescope configuration.
        """
        from ps_eor import psutil
        self.weights = weights
        self.telescope_simu = telescope_simu
        self.name = self.telescope_simu.telescop.name
        self.z = psutil.freq_to_z(self.weights.freqs.mean())

    def save(self, filename):
        """
        Save the current object to a file.

        Args:
            filename (str): Path to the file where the data should be saved.
        """
        self.weights.meta.update(self.telescope_simu.to_dict())
        self.weights.save(filename)

    @staticmethod
    def load(filename):
        """
        Load a SimuGridded object from a file.

        Args:
            filename (str): Path to the saved file.

        Returns:
            SimuGridded: The loaded object.
        """
        from ps_eor import datacube
        weights = datacube.CartWeightCube.load(filename)
        telescope_simu = TelescopeSimu.from_dict(weights.meta.kargs, weights.freqs)

        if telescope_simu.telescop.redundant_array:
            weights = datacube.CartWeightsCubeMeter(weights.data, weights.uu, weights.vv, weights.freqs,
                                                    weights.meta, weights.uv_scale)

        return SimuGridded(weights, telescope_simu)

    def get_slice(self, freq_start=None, freq_end=None):
        """
        Extract a frequency slice of the gridded weights.

        If the weights are a CartWeightsCubeMeter, a CartWeightsCube is produced.

        Args:
            freq_start (float, optional): Starting frequency in Hz. Defaults to the first frequency.
            freq_end (float, optional): Ending frequency in Hz. Defaults to the last frequency.

        Returns:
            SimuGridded: A new instance with the selected frequency range.
        """
        from ps_eor import datacube
        if freq_start is None:
            freq_start = self.weights.freqs[0]
        if freq_end is None:
            freq_end = self.weights.freqs[-1]

        weights = self.weights.get_slice(freq_start, freq_end)

        if isinstance(weights, datacube.CartWeightsCubeMeter):
            m_freq = (freq_end + freq_start) / 2.
            weights = weights.get_cube(m_freq)

        return SimuGridded(weights, self.telescope_simu)

    def get_sefd(self):
        """
        Compute the per-pol system equivalent flux density (SEFD) across frequencies.

        Returns:
            np.ndarray: Array of SEFD values (Jy).
        """
        return np.atleast_1d(self.telescope_simu.telescop.get_sefd(self.weights.freqs))

    def get_i_sefd(self):
        """Compute the Stokes I System Equivalent Flux Density (SEFD) at given frequency.

        Args:
            freq (np.ndarray or float): Frequency in Hz.

        Returns:
            np.ndarray or float: SEFD in Jy. Must be overridden by subclasses.
        """

        return 1 / np.sqrt(2) * self.get_sefd()

    def get_ps_gen(self, filter_kpar_min=None, filter_wedge_theta=0):
        """
        Create a power spectrum generator for the current telescope configuration and weights.

        Args:
            filter_kpar_min (float, optional): Minimum k_parallel value for filtering.
            filter_wedge_theta (float, optional): Foreground wedge angle in radians.

        Returns:
            PowerSpectraCart: A power spectrum computation object.
        """
        from ps_eor import pspec, datacube

        du = 0.75 / self.weights.meta.theta_fov

        if self.telescope_simu.telescop.redundant_array:
            mfreq = self.weights.freqs.mean()
            b = self.telescope_simu.telescop.redundant_baselines
            el = 2 * np.pi * b / (const.c.value / mfreq)
        else:
            el = 2 * np.pi * (np.arange(self.weights.ru.min(), self.weights.ru.max(), du))

        ps_conf = pspec.PowerSpectraConfig(el, window_fct='boxcar')
        ps_conf.filter_kpar_min = filter_kpar_min
        ps_conf.filter_wedge_theta = filter_wedge_theta
        ps_conf.du = self.telescope_simu.telescop.du
        ps_conf.umin = self.telescope_simu.umin
        ps_conf.umax = self.telescope_simu.umax
        ps_conf.weights_by_default = True

        eor_bin_list = pspec.EorBinList(self.weights.freqs)
        eor_bin_list.add_freq(1, self.weights.freqs.min() * 1e-6, self.weights.freqs.max() * 1e-6)
        eor = eor_bin_list.get(1, self.weights.freqs)
        pb = datacube.PrimaryBeam.from_name(self.telescope_simu.telescop.pb_name)

        return pspec.PowerSpectraCart(eor, ps_conf, pb)

    def get_noise_std_cube(self, total_time_sec, sefd=None, min_weight=1):
        """
        Compute the thermal noise standard deviation cube.

        This method estimates the standard deviation of the thermal noise in each (u,v,ν) pixel
        given the SEFD and integration time. The returned object allows for generating noise
        realisations via `generate_noise_cube()`.

        If a window function was attached to the weights metadata at the gridding stage
        (key 'PEWINFCT'), the corresponding window-equivalent noise rescaling is automatically
        applied by delegating to `CartWeightCube.get_noise_std_cube` with
        `fake_apply_win_fct=True`. If no window is present, the noise is left unmodified.

        Args:
            total_time_sec (float): Total integration time in seconds.
            sefd (np.ndarray, optional): Stokes I System Equivalent Flux Density values [Jy] for each frequency.
                If None, values are computed from the telescope simulation.
            min_weight (float): Minimum weight threshold used to mask unreliable pixels.

        Returns:
            NoiseStdCube: Cube containing thermal noise standard deviations per pixel.
        """
        if sefd is None:
            sefd = self.get_i_sefd()

        fake_apply_win_fct = 'PEWINFCT' in self.weights.meta

        noise_std = self.weights.get_noise_std_cube(sefd, total_time_sec, fake_apply_win_fct=fake_apply_win_fct)
        noise_std.filter_min_weight(min_weight)

        return noise_std
