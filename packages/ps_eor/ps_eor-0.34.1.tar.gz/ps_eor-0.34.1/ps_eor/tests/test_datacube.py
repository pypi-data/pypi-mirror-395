from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os

import matplotlib
matplotlib.use('Agg')

from ps_eor import __version__
from ps_eor import datacube, psutil

import numpy as np
import astropy.constants as const

import pytest

randn = np.random.randn


def make_rnd_cartcube(nf, n):
    f1 = np.linspace(100, 110, nf) * 1e6
    uu = randn(n)
    vv = randn(n)
    meta = datacube.ImageMetaData.from_res(0.01, (100, 100))
    meta.set('PETOTTIM', 20)
    meta.set('PEINTTIM', 2)

    w1 = datacube.CartWeightCube(randn(nf, n), uu, vv, f1, meta)
    a = randn(nf, nf)
    e1 = datacube.ErrorCovariance(f1, np.dot(a, a.T), randn(n))
    c1 = datacube.CartDataCube(randn(nf, n), uu, vv, f1, meta, cov_err=e1, weights=w1)

    return c1


def make_rnd_uvfits(tmp_dir, nf, shape, res):
    f1 = np.linspace(100, 110, nf) * 1e6
    uu, vv = psutil.get_uv_grid(shape, res)
    du = np.diff(uu)[0, 0]

    wcs = datacube.pywcs.WCS(naxis=3, fix=False)
    wcs.wcs.crpix = np.array([0, 0, 0])
    wcs.wcs.crval = [0, 0, 0]
    wcs.wcs.ctype = ['U', 'V', 'F']
    wcs.wcs.cdelt = [du, du, np.diff(f1)[0]]

    fits = [str(tmp_dir / ('f%.3f.fits' % f)) for f in f1]
    data = randn(len(f1), uu.shape[0], uu.shape[1])

    for i in range(len(f1)):
        wcs.wcs.crval = [0, 0, f1[i]]
        hdu = datacube.pf.PrimaryHDU(data[i])
        hdu.header['PETOTTIM'] = 20
        hdu.header['PEINTTIM'] = 2
        hdu.header['DATE-OBS'] = '2010-08-10'
        hdu.header.update(wcs.to_header())
        hdu.writeto(fits[i], overwrite=True)

    return f1, fits, uu, vv, data


def make_rnd_imgfits(tmp_dir, df, shape, res, psf=False, freq_width=None, wscnormf=1):
    f1 = np.arange(100, 110, df) * 1e6

    if freq_width is None:
        freq_width = df

    wcs = datacube.pywcs.WCS(naxis=4, fix=False)
    wcs.wcs.crpix = np.array([0, 0, 1, 1])
    wcs.wcs.crval = [0, 0, 1, 1]
    wcs.wcs.ctype = ['RA---SIN', 'DEC--SIN', 'FREQ', 'STOKES']
    wcs.wcs.cdelt = [-np.degrees(res), np.degrees(res), freq_width * 1e6, 1]
    wcs.wcs.cunit = ['deg', 'deg', 'Hz', '']

    if psf:
        fits = [str(tmp_dir / ('f%.3f_psf.fits' % f)) for f in f1]
        data = psutil.vis_to_img(10 + abs(randn(len(f1), shape[0], shape[1])), axes=(1, 2)).real
    else:
        fits = [str(tmp_dir / ('f%.3f.fits' % f)) for f in f1]
        data = randn(len(f1), shape[0], shape[1])

    for i in range(len(f1)):
        wcs.wcs.crval = [0, 0, f1[i], 1]
        hdu = datacube.pf.PrimaryHDU(data[i][None, None, :, :])
        hdu.header['PETOTTIM'] = 20
        hdu.header['PEINTTIM'] = 2
        hdu.header['DATE-OBS'] = '2010-08-10'
        hdu.header['WSCNVIS'] = 1000
        if wscnormf is not None:
            hdu.header['WSCNORMF'] = wscnormf
        else:
            hdu.header['BMAJ'] = 3 * res
            hdu.header['BMIN'] = 3 * res
        hdu.header.update(wcs.to_header())
        hdu.writeto(fits[i], overwrite=True)

    return f1, fits, data


def test_get_common_cube():
    u1 = np.array([1, 2, 3, 4])
    u2 = np.array([1, 2, 3, 5])
    f1 = np.array([1.0001, 4]) * 1e6
    f2 = np.array([1.0002, 2, 3, 4]) * 1e6
    meta = datacube.ImageMetaData.from_res(1, (100, 100))
    c1 = datacube.CartDataCube(np.ones((len(f1), len(u1))), u1, u1, f1, meta)
    c2 = datacube.CartDataCube(np.ones((len(f2), len(u2))), u2, u2, f2, meta)

    cc1, cc2 = datacube.get_common_cube(c1, c2)
    assert np.allclose(cc1.uu, [1, 2, 3])
    assert np.allclose(cc1.vv, [1, 2, 3])
    assert np.allclose(cc2.uu, [1, 2, 3])
    assert np.allclose(cc2.vv, [1, 2, 3])
    assert np.allclose(cc1.freqs, [1000100, 4e6])
    assert np.allclose(cc2.freqs, [1000200, 4e6])
    cc1, cc2 = datacube.get_common_cube(c1, c2, only_frequency=True)
    assert np.allclose(cc1.uu, u1)
    assert np.allclose(cc1.vv, u1)
    assert np.allclose(cc2.uu, u2)
    assert np.allclose(cc2.vv, u2)
    assert np.allclose(cc1.freqs, [1000100, 4e6])
    assert np.allclose(cc2.freqs, [1000200, 4e6])


def test_window_function():
    m1 = datacube.WindowFunction('hann')
    m2 = datacube.WindowFunction('hann', circular=False)
    np.allclose(datacube.get_window('hann', 101), m1.generate_window(101)[50], rtol=1e-1, atol=1e-1)
    np.allclose(datacube.get_window('hann', 101), m2.generate_window(101)[50], rtol=1e-3, atol=1e-3)

    m1 = datacube.WindowFunction(('tukey', 0.2))
    np.allclose(datacube.get_window(('tukey', 0.2), 101), m1.generate_window(101)[50], rtol=1e-1, atol=1e-1)

    meta = datacube.ImageMetaData.from_res(1, (101, 101))
    meta.set('PEWINFCT', '(tukey,0.2)_True')
    m1 = datacube.WindowFunction.from_meta(meta)
    assert m1.name == ('tukey', 0.2)
    assert m1.circular is True
    meta.set('PEWINFCT', '(tukey,0.2)_False')
    m1 = datacube.WindowFunction.from_meta(meta)
    assert m1.name == ('tukey', 0.2)
    assert m1.circular is False

    np.allclose(datacube.get_window(('tukey', 0.2), 101), m1.generate(meta)[50], rtol=1e-3, atol=1e-3)

    meta = datacube.ImageMetaData.from_res(1, (101, 101))
    m1.to_meta(meta)
    assert meta.get('PEWINFCT') == "('tukey', 0.2)_False"

    m1 = datacube.WindowFunction('hann')
    m2 = datacube.WindowFunction('nuttall')

    meta = datacube.ImageMetaData.from_res(1, (101, 101))
    assert (m1 + m2).get_area(meta) == (m1.generate(meta) + m2.generate(meta)).mean()
    assert np.round((m1 + m2).get_area(meta, normalize=True),
                    2) == np.round((m1.generate(meta) + m2.generate(meta)).mean() / 2, 2)
    assert (m1 + m2).get_power(meta) == ((m1.generate(meta) + m2.generate(meta)) ** 2).mean()

    m3 = datacube.WindowFunction('hann')

    assert ((m1 + m2) * m3).get_area(meta) == ((m1.generate(meta) + m2.generate(meta)) * m3.generate(meta)).mean()


def test_primary_beam():
    d = 10
    alpha = 0.8
    lamb = 2.
    freq = const.c.value / lamb
    pb = datacube.PrimaryBeam(10, alpha, 'gaussian')
    fwhm = pb.get_fwhm(freq)

    assert fwhm == alpha * lamb / d

    meta = datacube.ImageMetaData.from_res(1, (101, 101))
    beam = pb.generate_beam(fwhm, meta.res, meta.shape)
    assert beam.shape == meta.shape
    assert np.allclose(pb.generate(meta, freq=freq), beam)

    pb = datacube.PrimaryBeam.from_name('lofar_hba')
    assert pb.antenna_diameter == 30.75
    pb = datacube.PrimaryBeam.from_name('lofar_lba_inner')
    assert pb.antenna_diameter == 32.25
    pb = datacube.PrimaryBeam.from_name('lofar_lba_outer')
    assert pb.antenna_diameter == 81.34
    pb = datacube.PrimaryBeam.from_name('no_pb')
    assert np.allclose(pb.generate(meta, freq=freq), np.ones(meta.shape))

    pb = datacube.PrimaryBeam.from_name('ant_20_1.01_gaussian')
    assert pb.antenna_diameter == 20
    assert pb.alpha_tapering == 1.01
    assert pb.beam_type == 'gaussian'


def test_image_meta_data():
    meta = datacube.ImageMetaData.from_res(1, (101, 101))
    meta.set('PETOTTIM', 20)
    meta.set('PEINTTIM', 2)
    assert meta.get('PETOTTIM') == 20
    assert meta.get('NOTSET', 0) == 0
    assert 'PETOTTIM' in meta
    assert meta.res == 1
    assert meta.shape == (101, 101)
    assert meta.theta_fov == 101
    assert meta.total_time == 20
    assert meta.int_time == 2

    wcs = datacube.pywcs.WCS(naxis=2, fix=False)
    wcs.wcs.crpix = np.array([100, 100])
    wcs.wcs.crval = [0, 0]
    wcs.wcs.ctype = ['X', 'Y']
    wcs.wcs.cdelt = [0.1, 0.1]
    hdu = datacube.pf.PrimaryHDU(np.ones((200, 200)))
    hdu.header['PETOTTIM'] = 20
    hdu.header['PEINTTIM'] = 2
    hdu.header['DATE-OBS'] = '2010-08-10'
    hdu.header[''] = 100
    hdu.header.update(wcs.to_header())

    meta = datacube.ImageMetaData.from_header(hdu.header, (200, 200))
    assert meta.res == np.radians(0.1)
    assert meta.shape == (200, 200)
    assert meta.total_time == 20
    assert meta.int_time == 2
    assert meta.obs_mjd == 55418
    assert np.allclose(meta.ra_dec_center_deg, [0, 0])

    meta.remove('PEINTTIM')
    assert meta.get('PEINTTIM') is None

    m1 = datacube.WindowFunction('hann')
    m1.to_meta(meta)
    assert (meta.win_fct.name, meta.win_fct.circular) == ('hann', True)
    assert np.round(meta.win_fct_area, 3) == 0.238
    assert np.round(meta.win_fct_power, 3) == 0.138

    meta.slice(50, 150, 50, 150)
    assert meta.shape == (100, 100)
    assert np.allclose(meta.wcs.wcs.crpix, (50, 50))

    assert meta.to_header()['PETOTTIM'] == 20
    assert meta.to_header(add_origin=True)['ORIGIN'] == 'ps_eor v_%s' % __version__


def test_image_cube(tmp_path):
    f = np.linspace(100, 110, 20)
    meta = datacube.ImageMetaData.from_res(0.01, (100, 100))
    d = randn(20, 100, 100)

    img = datacube.CartImageCube(d, f, meta)
    assert np.allclose(img.data, d)
    assert np.allclose(img.freqs, f)
    assert img.meta == meta

    img.trim(img.meta.theta_fov / 2)
    assert np.allclose(img.data, d[:, 25:75, 25:75])

    m1 = datacube.WindowFunction('hann')

    img.apply_window_function(m1)
    assert meta.get('PEWINFCT') == "hann_True"

    c = img.ft(0, 1000)
    cg = c.regrid()
    assert cg.data.shape == (20, 50, 50)
    assert np.allclose(cg.freqs, img.freqs)

    assert np.allclose(cg.image().data, img.data)

    fname = str((tmp_path / 'test.fits').absolute())
    img.save_to_fits(fname)
    assert os.path.isfile(fname)
    assert np.allclose(datacube.pf.getdata(fname), img.data)

    # No check here but we at least make sure that call works
    img.plot()
    img.plot_slice()


def test_datacube_creation_add_sub_mul():
    f1 = np.linspace(100, 110, 20)
    f2 = np.linspace(100, 110, 21)
    d = randn(100)

    cube1 = datacube.DataCube(d, f1)
    assert np.allclose(cube1.freqs, f1)
    assert np.allclose(cube1.data, d)

    with pytest.raises(ValueError):
        cube2 = datacube.DataCube(np.ones(100), f2)
        cube3 = cube1 + cube2

    with pytest.raises(TypeError):
        cube1 = datacube.DataCube(np.ones(100), f2 + 1)
        cube3 = cube1 + cube2

    c1 = make_rnd_cartcube(20, 100)
    c2 = make_rnd_cartcube(20, 100)

    c3 = make_rnd_cartcube(20, 100)
    c1.set_weights(c3.weights)
    assert np.allclose(c1.weights.data, c3.weights.data)

    c3 = c1.make_diff_cube()
    assert c3.data.shape == c1.data[:-1].shape
    assert c3.weights.data.shape == c1.weights.data[:-1].shape
    assert np.allclose(c3.data, np.sqrt(0.5) * np.diff(c1.data, axis=0))
    assert np.allclose(c3.weights.data, c1.weights.data[:-1])
    assert np.allclose(c3.weights.freqs, c1.weights.freqs[:-1])
    assert np.allclose(c3.freqs, c1.freqs[:-1])

    c3 = c1.make_diff_cube_interp()
    assert c3.data.shape == c1.data.shape
    assert c3.weights.data.shape == c1.weights.data.shape
    assert np.allclose(c3.data[:-1], np.sqrt(0.5) * np.diff(c1.data, axis=0))
    assert np.allclose(c3.weights.data, c1.weights.data)
    assert np.allclose(c3.weights.freqs, c1.weights.freqs)
    assert np.allclose(c3.freqs, c1.freqs)

    c3 = c1 + c2
    assert np.allclose(c3.data, c1.data + c2.data)
    assert np.allclose(c3.freqs, c1.freqs)
    assert np.allclose(c3.uu, c1.uu)
    assert np.allclose(c3.vv, c1.vv)
    assert np.allclose(c3.cov_err.data_scale, np.sqrt(c1.cov_err.data_scale ** 2 + c2.cov_err.data_scale ** 2))
    assert np.allclose(c3.cov_err.freq_cov_err, c1.cov_err.freq_cov_err + c2.cov_err.freq_cov_err)
    assert np.allclose(c3.weights.data, c1.weights.data + c2.weights.data)

    c3 = c1 - c2
    assert np.allclose(c3.data, c1.data - c2.data)
    assert np.allclose(c3.freqs, c1.freqs)
    assert np.allclose(c3.uu, c1.uu)
    assert np.allclose(c3.vv, c1.vv)
    assert np.allclose(c3.cov_err.data_scale, np.sqrt(c1.cov_err.data_scale ** 2 + c2.cov_err.data_scale ** 2))
    assert np.allclose(c3.cov_err.freq_cov_err, c1.cov_err.freq_cov_err - c2.cov_err.freq_cov_err)
    assert np.allclose(c3.weights.data, c1.weights.data + c2.weights.data)

    assert np.allclose((2.2 * c1).data, 2.2 * c1.data)
    assert np.allclose((2.2 * c1).weights.data, 2.2 * c1.weights.data)


def test_datacube_slice_filter():
    c1 = make_rnd_cartcube(20, 100)
    assert np.allclose(c1.get_slice(0, 1e9).freqs, c1.freqs)
    assert np.allclose(c1.get_slice(c1.freqs[3], 1e9).freqs, c1.freqs[3:])
    assert np.allclose(c1.get_slice(c1.freqs[3] + 1e-4, 1e9).freqs, c1.freqs[4:])
    assert np.allclose(c1.get_slice(c1.freqs[3] - 1e-4, 1e9).freqs, c1.freqs[3:])
    assert np.allclose(c1.get_slice(0, c1.freqs[10]).freqs, c1.freqs[:11])
    assert np.allclose(c1.get_slice(0, c1.freqs[10] + 1e-4).freqs, c1.freqs[:11])
    assert np.allclose(c1.get_slice(0, c1.freqs[10] - 1e-4).freqs, c1.freqs[:10])
    assert np.allclose(c1.get_slice(0, 0).freqs, [])
    assert np.allclose(c1.get_slice(1e9, 1e9).freqs, [])
    assert np.allclose(c1.get_slice(c1.freqs[3], c1.freqs[10]).freqs, c1.freqs[3:11])
    assert np.allclose(c1.get_slice(c1.freqs[3], c1.freqs[10]).freqs, c1.weights.freqs[3:11])
    assert np.allclose(c1.get_slice(c1.freqs[3], c1.freqs[10]
                                    ).cov_err.freq_cov_err, c1.cov_err.freq_cov_err[3:11, 3:11])
    assert np.allclose(c1.get_slice(c1.freqs[3], c1.freqs[10]).data, c1.data[3:11, :])
    assert np.allclose(c1.get_slice(c1.freqs[3], c1.freqs[10]).weights.data, c1.weights.data[3:11, :])

    assert c1.get_freq(c1.freqs[3]).freqs == c1.freqs[3:4]

    idx_uv = c1.uu < 0.5
    cc1 = c1.copy()
    c1.filter_uv_from_index(idx_uv)
    assert np.all(c1.uu < 0.5)
    assert np.allclose(c1.data, cc1.data[:, idx_uv])
    assert np.all(c1.weights.uu < 0.5)
    assert np.allclose(c1.weights.data, cc1.weights.data[:, idx_uv])
    assert np.allclose(c1.cov_err.data_scale, cc1.cov_err.data_scale[idx_uv])


def test_cartdatacube_load_save(tmp_path):
    freqs, fits, uu, vv, data = make_rnd_uvfits(tmp_path, 10, (100, 100), 1e-3)

    cube = datacube.CartDataCube.load_from_fits(fits, 0, 25, convert_jy2k=False)

    uu2, vv2, idx = psutil.get_ungrid_vis_idx((100, 100), 1e-3, 0, 25)

    assert np.allclose(cube.freqs, freqs)
    assert np.allclose(cube.data, data[:, idx])
    assert np.allclose(cube.uu, uu[idx])
    assert np.allclose(cube.vv, vv[idx])
    assert cube.meta.total_time == 20
    assert cube.meta.int_time == 2
    assert np.allclose(cube.meta.freq_width, 1)

    img = cube.image()
    assert img.meta.total_time == 20
    assert img.meta.int_time == 2

    cube = datacube.CartDataCube.load_from_fits(fits, 0, 25, convert_jy2k=True)
    lamb = const.c.value / freqs
    jy2k = ((1e-26 * lamb ** 2) / (2 * const.k_B.value))

    assert np.allclose(cube.data, data[:, idx] * jy2k[:, None])

    cube = make_rnd_cartcube(100, 100)
    cube.save(str(tmp_path / 'file.h5'))
    cube2 = cube.load(str(tmp_path / 'file.h5'))

    assert np.allclose(cube.data, cube2.data)
    assert np.allclose(cube.uu, cube2.uu)
    assert np.allclose(cube.vv, cube2.vv)
    assert np.allclose(cube.freqs, cube2.freqs)
    assert np.allclose(cube.weights.data, cube2.weights.data)
    assert np.allclose(cube.weights.uu, cube2.weights.uu)
    assert np.allclose(cube.weights.vv, cube2.weights.vv)
    assert np.allclose(cube.weights.freqs, cube2.weights.freqs)
    assert np.allclose(cube.cov_err.data_scale, cube2.cov_err.data_scale)
    assert np.allclose(cube.cov_err.freq_cov_err, cube2.cov_err.freq_cov_err)
    assert np.allclose(cube2.meta.freq_width, 1)
    assert cube2.meta.total_time == 20
    assert cube2.meta.int_time == 2
    assert np.allclose(cube2.meta.ra_dec_center_deg, cube.meta.ra_dec_center_deg)

    cube = cube.new_with_cov_err()
    assert cube.cov_err is None

    cube = datacube.CartDataCube.load_from_fits(fits, 0, 25, convert_jy2k=False)

    idx = np.ones_like(cube.freqs, dtype=bool)
    idx[np.random.randint(1, len(cube.freqs) - 2, 2)] = False
    idx_uv = np.ones_like(cube.uu, dtype=bool)
    idx_uv[np.random.randint(1, len(cube.uu) - 2, 10)] = False

    cube2 = cube.get_slice_from_idx(idx)
    cube2.filter_uv_from_index(idx_uv)

    assert len(cube2.freqs) == len(cube.freqs) - (~idx).sum()
    assert len(cube2.uu) == len(cube.uu) - (~idx_uv).sum()

    cube_f = cube2.make_full_cube(0, 25)

    assert np.allclose(cube.freqs, cube_f.freqs)
    assert np.allclose(cube.uu, cube_f.uu)

    d = randn(len(freqs), 100, 100)
    meta = datacube.ImageMetaData.from_res(1e-3, (100, 100))
    img = datacube.CartImageCube(d, freqs, meta)
    fov = img.meta.theta_fov
    cube = img.ft(0, 1e9)

    cube2 = cube.reduce_fov(fov / 2)
    img2 = cube2.image()
    img.trim(fov / 2)

    assert np.allclose(img2.data, img.data)
    assert cube.meta.theta_fov == fov
    assert cube2.meta.theta_fov == fov / 2
    assert img2.meta.theta_fov == fov / 2

    cube3 = cube.reduce_fov(fov / 2, low_memory=True)
    img3 = cube3.image()

    assert np.allclose(img3.data, img.data)
    assert img3.meta.theta_fov == fov / 2

    d = randn(len(freqs), 100, 100)
    meta = datacube.ImageMetaData.from_res(1e-3, (100, 100))
    img = datacube.CartImageCube(d, freqs, meta)
    cube = img.ft(0, 1e9)

    win_fct = datacube.WindowFunction('hann')
    cube2 = cube.apply_window_function(win_fct)
    img2 = cube2.image()

    img.apply_window_function(win_fct)

    assert np.allclose(img2.data, img.data)

    # call plot without testing
    cube.plot_uv()


def test_cartdatacube_avg_filter():
    cube = make_rnd_cartcube(100, 100)
    cube2 = cube.average_freqs(5)
    assert np.allclose(cube2.freqs, cube.freqs[2::5])
    cube2 = cube.average_freqs(5)
    assert np.allclose(cube2.freqs, cube.freqs[2::5])


def test_load_from_fits_image_and_psf(tmp_path):
    np.random.seed(0)
    f1, fits, data = make_rnd_imgfits(tmp_path, 0.5, (100, 100), 1e-3, freq_width=0.4)
    _, fits_psf, data_psf = make_rnd_imgfits(tmp_path, 0.5, (100, 100), 1e-3, psf=True, freq_width=0.4)

    cube = datacube.CartDataCube.load_from_fits_image_and_psf(fits, fits_psf, 100, 500, np.radians(4))
    uu, vv, _ = psutil.get_ungrid_vis_idx(cube.meta.shape, cube.meta.res, 100, 500)

    assert np.allclose(cube.uu, uu)
    assert np.allclose(cube.weights.uu, uu)
    assert np.allclose(cube.vv, vv)
    assert np.allclose(cube.freqs, f1)
    assert np.allclose(cube.meta.res, 1e-3)
    assert cube.meta.int_time == 2
    assert cube.meta.total_time == 20
    assert np.allclose(cube.meta.freq_width, 0.4e6)
    assert np.allclose(cube.weights.meta.freq_width, 0.4e6)

    cube_h = datacube.CartDataCube.load_from_fits_image_and_psf(fits, fits_psf, 100, 500, np.radians(4),
                                                                window_function=datacube.WindowFunction(
        datacube.WindowFunction.parse_winfct_str('hann'))
    )

    assert (cube_h.meta.win_fct.name, cube_h.meta.win_fct.circular) == ('hann', True)

    np.random.seed(0)
    f1, fits_n3, data_n3 = make_rnd_imgfits(tmp_path, 0.5, (100, 100), 1e-3, freq_width=0.4 / 3.)
    _, fits_psf_n3, _ = make_rnd_imgfits(tmp_path, 0.5, (100, 100), 1e-3, psf=True, freq_width=0.4 / 3.)

    cube_n3 = datacube.CartDataCube.load_from_fits_image_and_psf(fits_n3, fits_psf_n3, 100, 500, np.radians(4))

    assert np.allclose(data_n3[0, 0], data[0, 0])
    assert np.allclose(cube.data[0, 0], cube_n3.data[0, 0])
    assert np.allclose(cube.weights.data[0, 0], cube_n3.weights.data[0, 0])
    assert np.allclose(cube.estimate_sefd(), np.sqrt(3) * cube_n3.estimate_sefd())
    assert np.allclose(cube.estimate_uv_sefd().data, np.sqrt(3) * cube_n3.estimate_uv_sefd().data)
    assert np.allclose(cube.estimate_freqs_sefd(), np.sqrt(3) * cube_n3.estimate_freqs_sefd())

    cube = datacube.CartDataCube.load_from_fits_image_and_psf(fits, fits_psf, 100, 500, np.radians(4),
                                                              use_wscnormf=True)

    f1, fits, data = make_rnd_imgfits(tmp_path, 0.5, (100, 100), 1e-3, freq_width=0.4, wscnormf=None)
    _, fits_psf, data_psf = make_rnd_imgfits(tmp_path, 0.5, (100, 100), 1e-3, psf=True, freq_width=0.4, wscnormf=None)

    cube = datacube.CartDataCube.load_from_fits_image_and_psf(fits, fits_psf, 100, 500, np.radians(4),
                                                              use_wscnormf=True)


def test_datacube_filter():
    c1 = make_rnd_cartcube(20, 100)
    idx_uv = (c1.ru >= 0.2) & (c1.ru <= 0.8)
    c2 = c1.copy()
    c2.filter_uvrange(0.2, 0.8)

    assert np.allclose(c1.data[:, idx_uv], c2.data)
    assert np.allclose(c1.weights.data[:, idx_uv], c2.weights.data)
    assert c2.ru.max() <= 0.8
    assert c2.ru.min() >= 0.2
    assert c2.weights.ru.max() <= 0.8
    assert c2.weights.ru.min() >= 0.2
    assert c2.data.shape[1] == c2.uu.shape[0]
    assert c2.data.shape[1] == c2.cov_err.data_scale.shape[0]

    idx_outliers = np.random.randint(0, 2, len(c1.freqs)).astype(bool)
    c2 = c1.copy()
    c2.filter_outliers(idx_outliers)

    assert np.allclose(c1.freqs[~idx_outliers], c2.freqs)
    assert np.allclose(c1.weights.freqs[~idx_outliers], c2.weights.freqs)
    assert np.allclose(c1.data[~idx_outliers], c2.data)
    assert np.allclose(c1.weights.data[~idx_outliers], c2.weights.data)
    assert np.allclose(c1.cov_err.freq_cov_err[~idx_outliers][:, ~idx_outliers], c2.cov_err.freq_cov_err)

    c2 = c1.copy()
    idx_outliers = np.random.randint(0, 2, len(c1.freqs)).astype(bool)
    c2.data[idx_outliers, 7] = np.nan
    print(idx_outliers, c2.data[idx_outliers][:, 7])
    c2.filter_nan()
    assert np.allclose(c1.data[~idx_outliers], c2.data)


def test_meter_cube(tmp_path):
    c1 = make_rnd_cartcube(20, 100)
    c1.save(str(tmp_path / 'file.h5'))
    c2_meter = datacube.CartDataCubeMeter.load(str(tmp_path / 'file.h5'))

    mfreq = 110e6
    lamb = const.c.value / mfreq
    c2 = c2_meter.get_cube(mfreq)

    assert np.allclose(c1.uu, c2.uu * lamb)
    assert np.allclose(c1.vv, c2.vv * lamb)
    assert np.allclose(c1.weights.uu, c2.weights.uu * lamb)
    assert np.allclose(c1.weights.vv, c2.weights.vv * lamb)

    c2_meter2 = c2_meter.new_with_data(2 * c2_meter.data)

    assert np.allclose(c2_meter.data * 2, c2_meter2.data)

    c2_meter.get_baseline(mfreq, c2_meter.ru[10])
