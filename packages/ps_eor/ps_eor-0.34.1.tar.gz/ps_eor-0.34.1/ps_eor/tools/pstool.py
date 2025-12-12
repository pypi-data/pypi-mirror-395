#!/usr/bin/env python

import os
import sys
import time
import itertools

import click

import numpy as np

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import astropy.constants as const

from ps_eor import __version__

# lazy loaded:
# All ps_eor modules
# astropy.units as u in gen_vis_cube


mpl.rcParams['image.cmap'] = 'Spectral_r'
mpl.rcParams['image.origin'] = 'lower'
mpl.rcParams['image.interpolation'] = 'nearest'
mpl.rcParams['axes.grid'] = True

t_file = click.Path(exists=True, dir_okay=False)
t_dir = click.Path(exists=True, file_okay=False)

MIN_EOR_BW_MHZ = 2


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command('gen_vis_cube')
@click.argument('img_list', type=t_file)
@click.argument('psf_list', type=t_file)
@click.option('--output_name', '-o', help='Output filename', default='datacube.h5', show_default=True)
@click.option('--theta_fov', help='Trim image to FoV (in degrees)', default='4', type=str, show_default=True)
@click.option('--umin', help='Min baseline (in lambda)', default=50, type=float, show_default=True)
@click.option('--umax', help='Max baseline (in lambda)', default=250, type=float, show_default=True)
@click.option('--threshold', '-w', help='Filter all visibilities with weights below T times the max weights',
              default=0.01, type=float, show_default=True)
@click.option('--int_time', '-i', help='Integration time of a single visibility', type=str)
@click.option('--total_time', '-t', help='Total time of observation', type=str)
@click.option('--trim_method', '-m', help="Trim method: 'a': after normalization, 'b': before normalization",
              default='a', type=click.Choice(['a', 'b']), show_default=True)
@click.option('--use_wscnormf', help='Use WSCNORMF to normalize the visibility, and does not use the PSF', is_flag=True)
@click.option('--win_function', help='Apply a window function on the trimmed image')
def gen_vis_cube(img_list, psf_list, output_name, theta_fov, umin, umax, threshold, int_time, total_time,
                 trim_method, use_wscnormf, win_function):
    ''' Create a datacube from image and psf fits files.

        \b
        IMG_LIST: Listing of input fits image files
        PSF_LIST: Listing of input fits psf files
    '''
    import astropy.units as u
    from ps_eor import datacube, psutil

    if int_time is not None:
        int_time = u.Quantity(int_time, u.s).to(u.s).value

    if total_time is not None:
        total_time = u.Quantity(total_time, u.s).to(u.s).value

    imgs = np.atleast_1d(np.loadtxt(img_list, dtype=str))
    psfs = np.atleast_1d(np.loadtxt(psf_list, dtype=str))

    print('Loading %s files ...' % len(imgs))

    imgs = psutil.sort_by_fits_key(imgs, 'CRVAL3')
    psfs = psutil.sort_by_fits_key(psfs, 'CRVAL3')

    win_fct = None
    if win_function:
        name = datacube.WindowFunction.parse_winfct_str(win_function)
        win_fct = datacube.WindowFunction(name)
        print('Using mask: %s' % win_fct)

    if theta_fov.endswith('lamb'):
        mfreq = psutil.get_fits_key(imgs, 'CRVAL3').mean()
        lamb = 299792458. / mfreq
        theta_fov = float(theta_fov[:-4]) * lamb
    else:
        theta_fov = float(theta_fov)

    data_cube = datacube.CartDataCube.load_from_fits_image_and_psf(imgs, psfs, umin, umax,
                                                                   np.radians(theta_fov),
                                                                   int_time=int_time, total_time=total_time,
                                                                   min_weight_ratio=threshold,
                                                                   trim_method=trim_method,
                                                                   use_wscnormf=use_wscnormf,
                                                                   window_function=win_fct)

    print('Saving to: %s' % output_name)
    data_cube.save(output_name)


@main.command('even_odd_to_sum_diff')
@click.argument('even', type=t_file)
@click.argument('odd', type=t_file)
@click.argument('sum')
@click.argument('diff')
def even_odd_to_sum_diff(even, odd, sum, diff):
    ''' Create SUM / DIFF datacubes from EVEN / ODD datacubes '''
    from ps_eor import datacube

    even = datacube.CartDataCube.load(even)
    odd = datacube.CartDataCube.load(odd)
    
    sum_c = (0.5 * (even + odd))
    sum_c.weights = 2 * sum_c.weights
    sum_c.save(sum)

    diff_c = (0.5 * (even - odd))
    diff_c.weights = 2 * diff_c.weights
    diff_c.save(diff)

    print('All done')


@main.command('diff_cube')
@click.argument('cube1', type=t_file)
@click.argument('cube2', type=t_file)
@click.option('--out_file', '-o', help='output file name', default='diff_cube.h5',
              type=click.Path(file_okay=False), show_default=True)
def diff_cube(cube1, cube2, out_file):
    ''' Compute the difference between CUBE1 and CUBE2 '''
    from ps_eor import datacube

    cube1 = datacube.CartDataCube.load(cube1)
    cube2 = datacube.CartDataCube.load(cube2)

    print('Saving diff cube: %s ...' % out_file)

    cube1, cube2 = datacube.get_common_cube(cube1, cube2)
    (cube1 - cube2).save(out_file)


@main.command('run_flagger')
@click.argument('file_i', type=t_file)
@click.argument('file_v', type=t_file)
@click.argument('flag_config', type=t_file)
@click.option('--output_dir', '-o', type=t_dir, help='Output directory', default='.')
def run_flagger(file_i, file_v, flag_config, output_dir):
    ''' Run flagger on datacubes and save flag.

        \b
        FILE_I: Input Stoke I datacube
        FILE_V: Input Stoke V datacube
        FLAG_CONFIG: Flagger configuration file
    '''
    from ps_eor import datacube, flagger, psutil

    print('Loading cube ...')
    i_cube = datacube.CartDataCube.load(file_i)
    v_cube = datacube.CartDataCube.load(file_v)

    print('Running flagger ...')
    flagger_runner = flagger.FlaggerRunner.load(flag_config)
    flagger_runner.run(i_cube, v_cube)

    out_flag_name = psutil.append_postfix(os.path.basename(file_i), 'flag')
    out_flag_plot_name = psutil.append_postfix(os.path.basename(file_i), 'flag').replace('.h5', '.pdf')

    print('Saving flags to: %s ...' % out_flag_name)
    fig = flagger_runner.plot()
    fig.savefig(os.path.join(output_dir, out_flag_plot_name))
    flagger_runner.flag.save(os.path.join(output_dir, out_flag_name))

    print('All done!')


@main.command('make_ps')
@click.argument('file_i', type=t_file)
@click.argument('file_v', type=t_file)
@click.argument('file_dt', required=False, type=t_file)
@click.option('--flag_config', '-f', help='Flagging configuration parset', type=t_file)
@click.option('--eor_bins_list', '-e', help='Listing of EoR redshift bins', type=t_file)
@click.option('--ps_conf', '-c', help='Power Spectra configuration parset', type=t_file)
@click.option('--output_dir', '-o', help='Output directory', default='.', type=click.Path(file_okay=False))
@click.option('--plots_output_dir', '-po', help='Output directory for plots', default='.',
              type=click.Path(file_okay=False))
def make_ps(file_i, file_v, file_dt, flag_config, eor_bins_list, ps_conf, output_dir, plots_output_dir):
    ''' Produce power-spectra of datacubes

        \b
        FILE_I: Input Stoke I datacube
        FILE_V: Input Stoke V datacube
        FILE_DT: Optional input time-diffence datacube
        '''
    from ps_eor import datacube, pspec, flagger, psutil

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(plots_output_dir):
        os.makedirs(plots_output_dir)

    print('Loading data ...')
    i_cube = datacube.DataCube.load(file_i)
    v_cube = datacube.DataCube.load(file_v)

    if not eor_bins_list:
        eor_bins_list = pspec.EorBinList()
        eor_bins_list.add_freq('0', i_cube.freqs[0] * 1e-6, i_cube.freqs[-1] * 1e-6)

    ps_builder = pspec.PowerSpectraBuilder(ps_conf, eor_bins_list)
    ps_conf = ps_builder.ps_config

    i_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)
    v_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)

    dt_i_cube = None
    if file_dt is not None:
        dt_i_cube = datacube.DataCube.load(file_dt)
        dt_i_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)

    if flag_config is not None:
        print('Running flagger ...')
        flagger_runner = flagger.FlaggerRunner.load(flag_config)
        i_cube, v_cube = flagger_runner.run(i_cube, v_cube)
        if dt_i_cube is not None:
            dt_i_cube = flagger_runner.apply_last(dt_i_cube)

        fig = flagger_runner.plot()
        fig.savefig(os.path.join(plots_output_dir, 'flagger.pdf'))

    ps_conf.el = 2 * np.pi * np.arange(i_cube.ru.min(), i_cube.ru.max(), ps_conf.du)

    for eor_name in ps_builder.eor_bin_list.get_all_names():
        eor = ps_builder.eor_bin_list.get(eor_name, freqs=i_cube.freqs)

        if not eor or eor.bw_total < MIN_EOR_BW_MHZ * 1e6:
            continue

        ps_gen = ps_builder.get(i_cube, eor_name)

        plot_out_dir = os.path.join(plots_output_dir, 'eor%s_u%s-%s' %
                                    (eor_name, int(ps_conf.umin), int(ps_conf.umax)))
        out_dir = os.path.join(output_dir, 'eor%s_u%s-%s' % (eor_name, int(ps_conf.umin), int(ps_conf.umax)))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        if not os.path.exists(plot_out_dir):
            os.makedirs(plot_out_dir)

        kbins = np.logspace(np.log10(ps_gen.kmin), np.log10(ps_conf.kbins_kmax), ps_conf.kbins_n)

        if ps_conf.empirical_weighting:
            v_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube), sefd_poly_fit_deg=ps_conf.empirical_weighting_polyfit_deg,
                sefd_filter_n_bins=ps_conf.empirical_weighting_n_bins)
            i_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube), sefd_poly_fit_deg=ps_conf.empirical_weighting_polyfit_deg,
                sefd_filter_n_bins=ps_conf.empirical_weighting_n_bins)

        print('\nGenerating power spectra for EoR bin:', eor.name)
        print('Frequency range: %.2f - %.2f MHz (%i SB)\n' % (eor.fmhz[0], eor.fmhz[-1], len(eor.fmhz)))
        print('Mean redshift: %.2f (%.2f MHz)\n' % (eor.z, eor.mfreq * 1e-6))

        for cube, stokes in zip([i_cube, v_cube, dt_i_cube], ['I', 'V', 'dt_V']):
            if cube is None:
                continue

            fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))
            ps = ps_gen.get_ps(cube)
            ps2d = ps_gen.get_ps2d(cube)
            ps3d = ps_gen.get_ps3d(kbins, cube)

            ps.plot(ax=ax1)
            ps2d.plot(ax=ax2, wedge_lines=[90, 45], z=eor.z)

            ps.save_to_txt(os.path.join(out_dir, 'ps_%s.txt' % stokes))
            ps2d.save_to_txt(os.path.join(out_dir, 'ps2d_%s.txt' % stokes))
            ps3d.save_to_txt(os.path.join(out_dir, 'ps3d_%s.txt' % stokes))

            fig.tight_layout()
            fig.savefig(os.path.join(plot_out_dir, 'ps_%s.pdf' % stokes))

        fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(12, 5))
        ps_gen.get_cl(i_cube).plot_kper(ax=ax1, c=psutil.blue, l_lambda=True, normalize=True, label='I')
        ps_gen.get_cl(i_cube.make_diff_cube_interp()).plot_kper(
            ax=ax1, c=psutil.orange, l_lambda=True, normalize=True, label='dI')
        ps_gen.get_cl(v_cube.make_diff_cube_interp()).plot_kper(
            ax=ax1, c=psutil.green, l_lambda=True, normalize=True, label='dV')
        # ax1.axvline(250, ls='--', c=psutil.dblack)
        ax1.set_xscale('log')

        ps_gen.get_variance(i_cube).plot(ax=ax2, c=psutil.blue, label='I')
        ps_gen.get_variance(i_cube.make_diff_cube_interp()).plot(ax=ax2, c=psutil.orange, label='dI')
        ps_gen.get_variance(v_cube.make_diff_cube_interp()).plot(ax=ax2, c=psutil.green, label='dV')

        if dt_i_cube is not None:
            ps_gen.get_cl(dt_i_cube).plot_kper(ax=ax1, ls='--', c=psutil.black,
                                               l_lambda=True, normalize=True, label='th_noise')
            ps_gen.get_variance(dt_i_cube).plot(ax=ax2, ls='--', c=psutil.black, label='th_noise')

        lgd = fig.legend(*ax1.get_legend_handles_labels(), bbox_to_anchor=(0.5, 1), loc="lower center", ncol=4)
        fig.tight_layout(pad=0.4)
        fig.savefig(os.path.join(plot_out_dir, 'variance_cl.pdf'), bbox_extra_artists=(lgd,), bbox_inches='tight')


@main.command('vis_to_sph')
@click.argument('vis_cube', type=t_file)
@click.argument('sph_cube', type=click.Path(dir_okay=False))
@click.option('--umin', help='Min baseline (in lambda)', default=0, type=float)
@click.option('--umax', help='Max baseline (in lambda)', default=1000, type=float)
@click.option('--nside', '-n', help='Nside (if not set, default to 1/3 of lmax', type=int)
@click.option('--flagfile', '-f', help='Flag to be applied to visibility cube before transformation', type=t_file)
def vis_to_sph(vis_cube, sph_cube, umin, umax, nside, flagfile):
    ''' Load visibilities datacubes VIS_CUBE, transform to sph datacube and save to SPH_CUBE '''
    from ps_eor import datacube, sphcube, flagger

    cube = datacube.CartDataCube.load(vis_cube)

    if flagfile is not None:
        print('Applying flag ...')
        flag = flagger.Flag.load(flagfile)
        cube = flag.apply(cube)

    cube.filter_uvrange(umin, umax)

    lmax = int(np.floor(2 * np.pi * cube.ru.max()))

    if nside is None:
        nside = int(2 ** (np.ceil(np.log2(lmax / 3.))))

    out_cube = sphcube.SphDataCube.from_cartcube(cube, nside, lmax)
    out_cube.save(sph_cube)


def do_gpr(i_cube, v_cube, gpr_config_i, gpr_config_v, rnd_seed=1, noise_cube=None):
    from ps_eor import fgfit

    t = time.time()
    np.random.seed(rnd_seed)

    gpr_config_v = fgfit.fitutil.GprConfig.load(gpr_config_v)
    gpr_config_i = fgfit.fitutil.GprConfig.load(gpr_config_i)

    print('Running GPR for Stokes V ...\n')

    gpr_v_noise = v_cube
    if noise_cube is not None:
        gpr_v_noise = noise_cube

    gpr_fit = fgfit.GprForegroundFit(gpr_config_v)
    gpr_res_v = gpr_fit.run(v_cube, gpr_v_noise, rnd_seed=rnd_seed)

    print("\nDone in %.2f s\n" % (time.time() - t))

    t = time.time()
    print('Running GPR for Stokes I ...\n')

    gpr_i_noise = gpr_res_v.sub
    if noise_cube is not None:
        gpr_i_noise = noise_cube

    gpr_fit = fgfit.ScaleNoiseGprForegroundFit(gpr_config_i)
    gpr_res_i = gpr_fit.run(i_cube, gpr_i_noise, rnd_seed=rnd_seed)

    print("\nDone in %.2f s\n" % (time.time() - t))

    return gpr_res_i, gpr_res_v


def do_ml_gpr(i_cube, noise_cube, ml_gpr_config, ps_conf, rnd_seed=1):
    from ps_eor import ml_gpr

    print('Running ML-GPR for Stokes I ...\n')
    t = time.time()

    fitter = ml_gpr.MLGPRForegroundFitter(ml_gpr_config)
    noise_cube = fitter.process_noise_cube(noise_cube, sefd_poly_fit_deg=ps_conf.empirical_weighting_polyfit_deg,
                                           sefd_filter_n_bins=ps_conf.empirical_weighting_n_bins)

    ml_gpr_res = fitter.run(i_cube, noise_cube, verbose=True)

    print(f"\nDone in {(time.time() - t):.2f} second\n")

    return ml_gpr_res


def plot_img_and_freq_slice(eor, data_cube, ax1, ax2, name):
    img_cube = eor.get_slice(data_cube).regrid().image()

    img_cube.plot(ax=ax1, auto_scale_quantiles=(0.1, 0.999))
    img_cube.plot_slice(ax=ax2)

    ax1.text(0.03, 0.94, name, transform=ax1.transAxes, ha='left', fontsize=10)
    ax2.text(0.03, 0.94, name, transform=ax2.transAxes, ha='left', fontsize=10)


def save_img_and_ps(ps_gen, eor, kbins, cmpts, names, filename_img, filename_ps, cycler=None):
    fig, axs = plt.subplots(ncols=2, nrows=len(cmpts), figsize=(11, 3.5 * len(cmpts)))
    fig2, axs2 = plt.subplots(ncols=2, nrows=2, figsize=(10, 7))
    axs2 = axs2.flatten()

    if cycler is None:
        cycler = mpl.rcParams['axes.prop_cycle'] * mpl.cycler('linestyle', ['-'])

    for i, (cmpt, name, prop) in enumerate(zip(cmpts, names, cycler)):
        plot_img_and_freq_slice(eor, cmpt, axs[i, 0], axs[i, 1], name)

        ps_gen.get_ps3d(kbins, cmpt).plot(ax=axs2[0], label=name, c=prop['color'], ls=prop['linestyle'])
        ps_gen.get_ps2d(cmpt).plot_kpar(ax=axs2[1], label=name, c=prop['color'], ls=prop['linestyle'])
        ps_gen.get_ps2d(cmpt).plot_kper(ax=axs2[2], label=name, c=prop['color'], ls=prop['linestyle'])
        ps_gen.get_variance(cmpt).plot(ax=axs2[3], label=name, c=prop['color'], ls=prop['linestyle'])

    lgd = fig2.legend(*axs2[0].get_legend_handles_labels(),
                      bbox_to_anchor=(0.5, 1.02), loc="upper center", ncol=len(cmpts))

    fig.tight_layout()
    fig2.tight_layout()
    fig.savefig(filename_img)
    fig2.savefig(filename_ps, bbox_extra_artists=(lgd,), bbox_inches='tight')


def save_ps2d(ps_gen, ps, ps2d, title, filename, **kargs):
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))
    ps.plot(ax=ax1, **kargs)
    ps2d.plot(ax=ax2, wedge_lines=[45, 90], z=ps_gen.eor.z, **kargs)
    fig._plotutils_colorbars[ax2].ax.set_xlabel(r'$\mathrm{K^2\,h^{-3}\,cMpc^3}$')

    ax1.text(0.03, 0.92, title, transform=ax1.transAxes, ha='left', fontsize=11)
    ax2.text(0.03, 0.92, title, transform=ax2.transAxes, ha='left', fontsize=11)
    fig.tight_layout()
    fig.savefig(filename)


def get_ratios(ps_gen, ps2d_ratio):
    ratio = np.median(ps2d_ratio.data)
    ratio_high = np.median((ps2d_ratio.data)[ps_gen.k_par > 0.8])
    ratio_low = np.median((ps2d_ratio.data)[ps_gen.k_par < 0.6])

    return ratio, ratio_high, ratio_low


@main.command('run_gpr')
@click.argument('file_i', type=t_file)
@click.argument('file_v', type=t_file)
@click.argument('gpr_config_i', type=t_file)
@click.argument('gpr_config_v', type=t_file)
@click.option('--flag_config', '-f', type=t_file, help='GPR configuration parset for Stokes I')
@click.option('--eor_bins_list', '-e', type=t_file, help='Listing of EoR redshift bins')
@click.option('--ps_conf', '-c', type=t_file, help='Power spectra configuration file')
@click.option('--output_dir', '-o', help='Output directory', default='.')
@click.option('--plots_output_dir', '-po', help='Output directory for the figures')
@click.option('--no_plot', help='Skip plotting', is_flag=True)
@click.option('--rnd_seed', help='Set a random seed', default=3, type=int)
@click.option('--noise_cube', 'file_noise_cube', help='Specify a noise cube (otherwise GPR residual of Stokes V is used)', default=None, type=t_file)
def run_gpr(file_i, file_v, gpr_config_i, gpr_config_v, flag_config, eor_bins_list, ps_conf,
            output_dir, plots_output_dir, no_plot, rnd_seed, file_noise_cube):
    ''' Run GPR & generate power spectra

    \b
    FILE_I: Input Stoke I datacube
    FILE_V: Input Stoke V datacube
    GPR_CONFIG_I: GPR configuration parset for Stokes I
    GPR_CONFIG_V: GPR configuration parset for Stokes V
    '''
    from ps_eor import datacube, pspec, flagger, psutil

    if plots_output_dir is None:
        plots_output_dir = output_dir

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(plots_output_dir):
        os.makedirs(plots_output_dir)

    print('Loading data ...')
    i_cube = datacube.DataCube.load(file_i)
    v_cube = datacube.DataCube.load(file_v)

    ps_builder = pspec.PowerSpectraBuilder(ps_conf, eor_bins_list)
    ps_conf = ps_builder.ps_config

    i_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)
    v_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)

    if flag_config:
        print('Running flagger ...')
        flagger_runner = flagger.FlaggerRunner.load(flag_config)
        i_cube, v_cube = flagger_runner.run(i_cube, v_cube)

        if not no_plot:
            fig = flagger_runner.plot()
            fig.savefig(os.path.join(plots_output_dir, 'flagger_gpr.pdf'))

    if file_noise_cube is not None:
        noise_cube = datacube.DataCube.load(file_noise_cube)
        noise_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)
        if flag_config:
            noise_cube = flagger_runner.apply_last(noise_cube)

    ps_conf.el = 2 * np.pi * np.arange(i_cube.ru.min(), i_cube.ru.max(), ps_conf.du)

    for eor_name in ps_builder.eor_bin_list.get_all_names():
        eor = ps_builder.eor_bin_list.get(eor_name, freqs=i_cube.freqs)

        if not eor or eor.bw_total < MIN_EOR_BW_MHZ * 1e6:
            continue

        ps_gen = ps_builder.get(i_cube, eor_name)

        out_dir = os.path.join(output_dir, 'eor%s_u%s-%s' % (eor_name, int(ps_conf.umin), int(ps_conf.umax)))
        plot_out_dir = os.path.join(plots_output_dir, 'eor%s_u%s-%s' %
                                    (eor_name, int(ps_conf.umin), int(ps_conf.umax)))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        if not os.path.exists(plot_out_dir):
            os.makedirs(plot_out_dir)

        ps_gen_fg = ps_builder.get(i_cube, eor_name, window_fct='hann', rmean_freqs=True)

        if ps_conf.empirical_weighting:
            sefd = v_cube.make_diff_cube().estimate_sefd()
            poly_deg = ps_conf.empirical_weighting_polyfit_deg
            v_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube.make_diff_cube()), sefd_poly_fit_deg=poly_deg, expected_sefd=sefd,
                sefd_filter_n_bins=ps_conf.empirical_weighting_n_bins)
            i_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube.make_diff_cube()), sefd_poly_fit_deg=poly_deg, expected_sefd=sefd,
                sefd_filter_n_bins=ps_conf.empirical_weighting_n_bins)

        kbins = np.logspace(np.log10(ps_gen.kmin), np.log10(ps_conf.kbins_kmax), ps_conf.kbins_n)

        print('\nRunning GPR for EoR bin:', eor.name)
        print('Frequency range: %.2f - %.2f MHz (%i SB)\n' % (eor.fmhz[0], eor.fmhz[-1], len(eor.fmhz)))
        print('Mean redshift: %.2f (%.2f MHz)\n' % (eor.z, eor.mfreq * 1e-6))

        print('Saving GPR result...\n')

        eor_bin_noise_cube = None
        if file_noise_cube is not None:
            eor_bin_noise_cube = eor.get_slice_fg(noise_cube)

        gpr_res, gpr_res_v = do_gpr(eor.get_slice_fg(i_cube), eor.get_slice_fg(v_cube),
                                    gpr_config_i, gpr_config_v, noise_cube=eor_bin_noise_cube, rnd_seed=rnd_seed)

        gpr_res_v.save(out_dir, 'gpr_res_V')
        gpr_res.save(out_dir, 'gpr_res_I')

        # Saving residuals I and V PS
        ps2d_i_res = ps_gen.get_ps2d(gpr_res.sub)
        ps2d_v_res = ps_gen.get_ps2d(gpr_res_v.sub)
        ps_i_res = ps_gen.get_ps(gpr_res.sub)
        ps_v_res = ps_gen.get_ps(gpr_res_v.sub)
        ps3d_i_res = ps_gen.get_ps3d(kbins, gpr_res.sub)
        ps3d_v_res = ps_gen.get_ps3d(kbins, gpr_res_v.sub)
        ps3d_noise_i = ps_gen.get_ps3d(kbins, gpr_res.noise)
        ps3d_rec = ps_gen.get_ps3d_with_noise(kbins, gpr_res.sub, gpr_res.noise)

        ratio, ratio_high, ratio_low = get_ratios(ps_gen, ps2d_i_res / ps2d_v_res)
        ratio_txt = 'Ratio I / V (med: %.2f / %.2f / %.2f)' % (ratio, ratio_high, ratio_low)
        print(ratio_txt)

        ps2d_i_res.save_to_txt(os.path.join(out_dir, 'ps2d_I_residual.txt'))
        ps2d_v_res.save_to_txt(os.path.join(out_dir, 'ps2d_V_residual.txt'))

        ps3d_i_res.save_to_txt(os.path.join(out_dir, 'ps3d_I_residual.txt'))
        ps3d_v_res.save_to_txt(os.path.join(out_dir, 'ps3d_V_residual.txt'))
        ps3d_rec.save_to_txt(os.path.join(out_dir, 'ps3d_I_minus_V.txt'))
        ps3d_noise_i.save_to_txt(os.path.join(out_dir, 'ps3d_I_noise.txt'))

        up = ps3d_rec.get_upper()
        k_up = ps3d_rec.k_mean[np.nanargmin(up)]
        upper_limit = '2 sigma upper limit: (%.1f)^2 mK^2 at k = %.3f' % (np.nanmin(up), k_up)
        print(upper_limit)

        if no_plot:
            continue

        print('Plotting results ...\n')

        # Plotting GPR results
        save_ps2d(ps_gen, ps_i_res, ps2d_i_res, 'Stokes I residual',
                  os.path.join(plot_out_dir, 'ps2d_I_residual.pdf'))
        save_ps2d(ps_gen, ps_v_res, ps2d_v_res, 'Stokes V residual',
                  os.path.join(plot_out_dir, 'ps2d_V_residual.pdf'))

        save_ps2d(ps_gen, ps_i_res / ps_v_res, ps2d_i_res / ps2d_v_res, 'I residual / V residual',
                  os.path.join(plot_out_dir, 'ps2d_I_over_V_residual.pdf'), vmin=1, vmax=10)

        save_ps2d(ps_gen, ps_i_res / ps_v_res, ps2d_i_res / ps_gen.get_ps2d(gpr_res.noise), 'I residual / noise',
                  os.path.join(plot_out_dir, 'ps2d_I_over_noise.pdf'), vmin=0.5, vmax=10)

        cmpts = [i_cube, v_cube, gpr_res.fit, gpr_res.sub, gpr_res_v.sub]
        names = ['I', 'V', 'I fg', 'I residual', 'V residual']
        cycler = mpl.cycler('color', [psutil.lblue, psutil.lgreen, psutil.red, psutil.dblue, psutil.dgreen]) \
            + mpl.cycler('linestyle', ['-', '-', ':', '-', '-'])
        save_img_and_ps(ps_gen_fg, eor, kbins, cmpts, names,
                        os.path.join(plot_out_dir, 'img_I_V_residuals.pdf'),
                        os.path.join(plot_out_dir, 'ps_I_V_residuals.pdf'), cycler)

        cmpts = [gpr_res.pre_fit, gpr_res.get_fg_model(), gpr_res.get_eor_model(), gpr_res.sub, gpr_res.noise]
        names = ['fg int', 'fg mix', 'eor', 'I residual', 'noise I']

        if gpr_res.post_fit.data.mean() != 0:
            cmpts.append(gpr_res.post_fit)
            names.append('fg pca')

        save_img_and_ps(ps_gen_fg, eor, kbins, cmpts, names,
                        os.path.join(plot_out_dir, 'img_gpr_cmpts.pdf'),
                        os.path.join(plot_out_dir, 'ps_gpr_cmpts.pdf'))

        # PS3D plot
        fig, ax = plt.subplots()
        ps3d_i_res.plot(label='I residual', ax=ax, nsigma=2, c=psutil.dblue)
        ps3d_noise_i.plot(label='noise I', ax=ax, nsigma=2, c=psutil.green)
        ps3d_rec.plot(label='I residual - noise', ax=ax, nsigma=2, c=psutil.orange)

        ax.legend()
        fig.savefig(os.path.join(plot_out_dir, 'ps3d.pdf'), bbox_inches='tight')


def ensure_symlink(source, link_name):
    """
    Ensure that a symbolic link exists and points to the source.
    If the link is broken or points to a different location, it will be recreated.
    """
    # Check if the link exists
    if os.path.islink(link_name):
        # Check if the link is broken or points to a different source
        if not os.path.exists(link_name) or os.readlink(link_name) != source:
            os.remove(link_name)  # Remove the broken or outdated link
            os.symlink(source, link_name)  # Create a new symlink
    elif not os.path.exists(link_name):
        # If the link does not exist at all, create it
        os.symlink(source, link_name)
    else:
        # The link_name exists and is not a link (e.g., a file or directory)
        raise FileExistsError(f"Path exists and is not a symlink: '{link_name}'")


@main.command('run_ml_gpr')
@click.argument('file_i', type=t_file)
@click.argument('file_v', type=t_file)
@click.argument('ml_gpr_config_file', type=t_file)
@click.option('--flag_config', '-f', type=t_file, help='GPR configuration parset for Stokes I')
@click.option('--eor_bins_list', '-e', type=t_file, help='Listing of EoR redshift bins')
@click.option('--ps_conf', '-c', type=t_file, help='Power spectra configuration file')
@click.option('--output_dir', '-o', help='Output directory', default='.')
@click.option('--plots_output_dir', '-po', help='Output directory for the figures')
@click.option('--no_plot', help='Skip plotting', is_flag=True)
@click.option('--rnd_seed', help='Set a random seed', default=3, type=int)
@click.option('--file_noise', help='Input noise datacube. If not set, Stokes V frequency diff will be used.',
              type=t_file)
def run_ml_gpr(file_i, file_v, ml_gpr_config_file, flag_config, eor_bins_list, ps_conf,
               output_dir, plots_output_dir, no_plot, rnd_seed, file_noise):
    ''' Run GPR & generate power spectra

    \b
    FILE_I: Input Stoke I datacube
    FILE_V: Input Stoke V datacube
    GPR_CONFIG_I: GPR configuration parset for Stokes I
    '''
    from ps_eor import datacube, pspec, flagger, psutil, ml_gpr

    if plots_output_dir is None:
        plots_output_dir = output_dir

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(plots_output_dir):
        os.makedirs(plots_output_dir)

    print(f'Loading configuration file {ml_gpr_config_file} ...')
    ml_gpr_config = ml_gpr.MLGPRConfigFile.load_with_defaults(ml_gpr_config_file, check_args=False)

    print('Loading data ...')
    i_cube = datacube.DataCube.load(file_i)
    v_cube = datacube.DataCube.load(file_v)

    if not eor_bins_list:
        eor_bins_list = pspec.EorBinList()
        eor_bins_list.add_freq('0', i_cube.freqs[0] * 1e-6, i_cube.freqs[-1] * 1e-6)

    ps_builder = pspec.PowerSpectraBuilder(ps_conf, eor_bins_list)
    ps_conf = ps_builder.ps_config

    i_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)
    v_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)

    if flag_config:
        print('Running flagger ...')
        flagger_runner = flagger.FlaggerRunner.load(flag_config)
        i_cube, v_cube = flagger_runner.run(i_cube, v_cube)

        if not no_plot:
            fig = flagger_runner.plot()
            fig.savefig(os.path.join(plots_output_dir, 'flagger_gpr.pdf'))
    else:
        flagger_runner = None

    # Get noise cube either from provided file_noise, from Stokes I or from Stokes V
    if file_noise is not None:
        noise_cube = datacube.DataCube.load(file_noise)
        noise_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)
        if flagger_runner is not None:
            noise_cube = flagger_runner.apply_last(noise_cube)
    elif ml_gpr_config.kern.noise.estimate_baseline_noise_from_stokes == 'V':
        noise_cube = v_cube
    elif ml_gpr_config.kern.noise.estimate_baseline_noise_from_stokes == 'I':
        noise_cube = i_cube
    else:
        print('Error: estimate_baseline_noise_from_stokes must be I or V or noise cube needs to be provided')
        return

    ps_conf.el = 2 * np.pi * np.arange(i_cube.ru.min(), i_cube.ru.max(), ps_conf.du)

    k_fg, k_eor, k_noise = ml_gpr_config.get_kern()

    print(f'\nKern FG\n{k_fg}')
    print(f'Kern 21-cm\n{k_eor}')
    print(f'Kern noise\n{k_noise}')

    for eor_name in ps_builder.eor_bin_list.get_all_names():
        eor = ps_builder.eor_bin_list.get(eor_name, freqs=i_cube.freqs)

        if not eor or eor.bw_total < MIN_EOR_BW_MHZ * 1e6:
            continue

        ps_gen = ps_builder.get(i_cube, eor_name)

        out_dir = os.path.join(output_dir, 'eor%s_u%s-%s' % (eor_name, int(ps_conf.umin), int(ps_conf.umax)))
        plot_out_dir = os.path.join(plots_output_dir, 'eor%s_u%s-%s' %
                                    (eor_name, int(ps_conf.umin), int(ps_conf.umax)))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        if not os.path.exists(plot_out_dir):
            os.makedirs(plot_out_dir)

        link_plots_out_dir = os.path.join(out_dir, 'results')
        # if not os.path.exists(link_plots_out_dir):
        #     os.symlink(plot_out_dir, link_plots_out_dir)
        ensure_symlink(plot_out_dir, link_plots_out_dir)

        ps_gen_fg = ps_builder.get(i_cube, eor_name, window_fct='hann', rmean_freqs=True)

        if ps_conf.empirical_weighting:
            sefd = v_cube.make_diff_cube().estimate_sefd()
            poly_deg = ps_conf.empirical_weighting_polyfit_deg
            n_bins = ps_conf.empirical_weighting_n_bins
            v_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube.make_diff_cube()), sefd_poly_fit_deg=poly_deg, sefd_filter_n_bins=n_bins, expected_sefd=sefd)
            i_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube.make_diff_cube()), sefd_poly_fit_deg=poly_deg, sefd_filter_n_bins=n_bins, expected_sefd=sefd)

        kbins = np.logspace(np.log10(ps_gen.kmin), np.log10(ps_conf.kbins_kmax), ps_conf.kbins_n)

        print('\nRunning ML GPR for EoR bin:', eor.name)
        print('Frequency range: %.2f - %.2f MHz (%i SB)\n' % (eor.fmhz[0], eor.fmhz[-1], len(eor.fmhz)))
        print('Mean redshift: %.2f (%.2f MHz)\n' % (eor.z, eor.mfreq * 1e-6))

        i_cube_slice = eor.get_slice_fg(i_cube)
        n_cube_slice = eor.get_slice_fg(noise_cube)
        ml_gpr_res = do_ml_gpr(i_cube_slice, n_cube_slice, ml_gpr_config, ps_conf, rnd_seed=rnd_seed)

        # Saving result
        ml_gpr_res.save(out_dir, 'ml_gpr_res_I')

        # Get results
        scaled_noise_cube = ml_gpr_res.get_scaled_noise_cube()
        ps_fg = ml_gpr_res.get_ps_fg(ps_gen_fg, kbins)
        ps_eor = ml_gpr_res.get_ps_eor(ps_gen, kbins)
        ps_residual = ml_gpr_res.get_ps_res(ps_gen, kbins)

        # Saving 2D and 3D residuals I and noise PS
        ratio, ratio_high, ratio_low = get_ratios(ps_gen, ps_residual.get_ps2d() / ps_gen.get_ps2d(scaled_noise_cube))
        ratio_txt = 'Ratio I/noise (med: %.2f / %.2f / %.2f)' % (ratio, ratio_high, ratio_low)
        print(ratio_txt)

        ps_residual.get_ps2d().save(os.path.join(out_dir, 'ps2d_I_residual.mc.h5'))
        ps_eor.get_ps2d().save(os.path.join(out_dir, 'ps2d_eor.mc.h5'))
        ps_fg.get_ps2d().save(os.path.join(out_dir, 'ps2d_fg.mc.h5'))

        ps3d_noise = ps_gen.get_ps3d(kbins, scaled_noise_cube)
        ps3d_res = ps_residual.get_ps3d()
        ps3d_rec = (ps3d_res - ps3d_noise)

        ps3d_res.save(os.path.join(out_dir, 'ps3d_I_residual.mc.h5'))
        ps3d_rec.save(os.path.join(out_dir, 'ps3d_I_minus_noise.mc.h5'))
        ps3d_noise.save_to_txt(os.path.join(out_dir, 'ps3d_I_noise.txt'))

        up = ps3d_rec.get_upper()
        k_up = ps3d_rec.k_mean[np.nanargmin(up)]
        upper_limit = '2 sigma upper limit: (%.1f)^2 mK^2 at k = %.3f' % (np.nanmin(up), k_up)
        print(upper_limit)

        if no_plot:
            continue

        print('Plotting results ...\n')

        # Plotting MCMC results
        ml_gpr_res.sampler_result.plot_corner().savefig(os.path.join(plot_out_dir, 'mcmc_corner.pdf'))
        ml_gpr_res.sampler_result.plot_samples().savefig(os.path.join(plot_out_dir, 'mcmc_samples.pdf'))
        ml_gpr_res.sampler_result.plot_samples_likelihood().savefig(os.path.join(plot_out_dir, 'mcmc_samples_likelihood.pdf'))

        # Plotting GPR results
        save_ps2d(ps_gen, ps_residual.get_ps(), ps_residual.get_ps2d(), 'Stokes I residual',
                  os.path.join(plot_out_dir, 'ps2d_I_residual.pdf'))

        save_ps2d(ps_gen, ps_residual.get_ps() / ps_gen.get_ps(scaled_noise_cube),
                  ps_residual.get_ps2d() / ps_gen.get_ps2d(scaled_noise_cube), 'I residual / noise',
                  os.path.join(plot_out_dir, 'ps2d_I_over_noise.pdf'), vmin=0.5, vmax=10)

        fp = pspec.FourPanelPsResults(ps_gen, kbins)
        fp.add_cube(i_cube, 'I', ps_gen=ps_gen_fg, c=psutil.lblue)
        fp.add_cube(v_cube, 'V', c=psutil.lgreen)
        fp.add_cube(n_cube_slice, 'Input noise', c=psutil.red)
        fp.add_ps_stacker(ps_residual, 'I residual', c=psutil.dblue)
        fp.done(ncol_legend=4)
        fp.savefig(os.path.join(plot_out_dir, 'ps_I_V_residuals.pdf'))

        fp = pspec.FourPanelPsResults(ps_gen, kbins)
        fp.add_cube(i_cube, 'I', ps_gen=ps_gen_fg, c=psutil.lblue)
        fp.add_ps_stacker(ps_fg, 'FG', c=psutil.dblue)
        fp.add_ps_stacker(ps_eor, '21-cm', c=psutil.orange)
        fp.add_cube(scaled_noise_cube, 'noise', c=psutil.green)
        fp.done(ncol_legend=4)
        fp.savefig(os.path.join(plot_out_dir, 'ps_gpr_cmpts.pdf'))

        # PS3D plot
        fig, ax = plt.subplots()
        ps3d_res.plot(label='I residual', ax=ax, c=psutil.dblue)
        ps3d_noise.plot(label='noise I', ax=ax, c=psutil.green)
        ps3d_rec.plot(label='I residual - noise', ax=ax, c=psutil.orange)

        ax.legend()
        fig.savefig(os.path.join(plot_out_dir, 'ps3d.pdf'), bbox_inches='tight')


@main.command('run_ml_gpr_inj')
@click.argument('file_i', type=t_file)
@click.argument('file_v', type=t_file)
@click.argument('ml_gpr_config_file', type=t_file)
@click.option('--flag_config', '-f', type=t_file, help='GPR configuration parset for Stokes I')
@click.option('--eor_bins_list', '-e', type=t_file, help='Listing of EoR redshift bins')
@click.option('--ps_conf', '-c', type=t_file, help='Power spectra configuration file')
@click.option('--output_dir', '-o', help='Output directory', default='.')
@click.option('--rnd_seed', help='Set a random seed', default=3, type=int)
@click.option('--file_noise', help='Input noise datacube. If not set, Stokes V frequency diff will be used.',
              type=t_file)
@click.option('--vae_kern_name', help='VAE kernel name in the ML-GPR config file', default='eor_vae')
@click.option('--amplitude', '-a', help='Variance of the injected signal with respect to the nosie variance', default=1.0)
@click.option('--x1', help='X1 parameter of the injected signal', default=0.0)
@click.option('--x2', help='X2 parameter of the injected signal', default=0.0)
def run_ml_gpr_inj(file_i, file_v, ml_gpr_config_file, flag_config, eor_bins_list, ps_conf,
                   output_dir, rnd_seed, file_noise, vae_kern_name, amplitude, x1, x2):
    ''' Run GPR on data + injected signal

    \b
    FILE_I: Input Stoke I datacube
    FILE_V: Input Stoke V datacube
    GPR_CONFIG_I: GPR configuration parset for Stokes I
    '''
    from ps_eor import datacube, pspec, flagger, psutil, ml_gpr

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f'Loading configuration file {ml_gpr_config_file} ...')
    ml_gpr_config = ml_gpr.MLGPRConfigFile.load_with_defaults(ml_gpr_config_file, check_args=False)

    print('Loading data ...')
    i_cube = datacube.DataCube.load(file_i)
    v_cube = datacube.DataCube.load(file_v)

    if not eor_bins_list:
        eor_bins_list = pspec.EorBinList()
        eor_bins_list.add_freq('0', i_cube.freqs[0] * 1e-6, i_cube.freqs[-1] * 1e-6)

    ps_builder = pspec.PowerSpectraBuilder(ps_conf, eor_bins_list)
    ps_conf = ps_builder.ps_config

    i_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)
    v_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)

    if flag_config:
        print('Running flagger ...')
        flagger_runner = flagger.FlaggerRunner.load(flag_config)
        i_cube, v_cube = flagger_runner.run(i_cube, v_cube)
    else:
        flagger_runner = None

    # Get noise cube either from provided file_noise, from Stokes I or from Stokes V
    if file_noise is not None:
        noise_cube = datacube.DataCube.load(file_noise)
        noise_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)
        if flagger_runner is not None:
            noise_cube = flagger_runner.apply_last(noise_cube)
    elif ml_gpr_config.kern.noise.estimate_baseline_noise_from_stokes == 'V':
        noise_cube = v_cube
    elif ml_gpr_config.kern.noise.estimate_baseline_noise_from_stokes == 'I':
        noise_cube = i_cube
    else:
        print('Error: estimate_baseline_noise_from_stokes must be I or V or noise cube needs to be provided')
        return

    k_fg, k_eor, k_noise = ml_gpr_config.get_kern()

    print(f'\nKern FG\n{k_fg}')
    print(f'Kern 21-cm\n{k_eor}')
    print(f'Kern noise\n{k_noise}')    

    for eor_name in ps_builder.eor_bin_list.get_all_names():
        eor = ps_builder.eor_bin_list.get(eor_name, freqs=i_cube.freqs)

        if not eor or eor.bw_total < MIN_EOR_BW_MHZ * 1e6:
            continue

        ps_gen = ps_builder.get(i_cube, eor_name)
        kbins = np.logspace(np.log10(ps_gen.kmin), np.log10(ps_conf.kbins_kmax), ps_conf.kbins_n)

        umin = int(ps_conf.umin)
        umax =int(ps_conf.umax)
        out_dir = os.path.join(output_dir, f'inj_eor{eor_name}_u{umin}-{umax}_a{amplitude:.3f}_x1{x1:.3f}_x2{x2:.3f}')

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        print('\nRunning ML GPR for EoR bin:', eor.name)
        print('Frequency range: %.2f - %.2f MHz (%i SB)\n' % (eor.fmhz[0], eor.fmhz[-1], len(eor.fmhz)))
        print('Mean redshift: %.2f (%.2f MHz)\n' % (eor.z, eor.mfreq * 1e-6))

        i_cube_slice = eor.get_slice_fg(i_cube)
        n_cube_slice = eor.get_slice_fg(noise_cube)

        k_eor = ml_gpr.get_kern_part(ml_gpr_config.get_kern()[1], vae_kern_name)
        k_eor.x1 = x1
        k_eor.x2 = x2
        c_injected = ml_gpr.make_new_from_cube(i_cube_slice, kern=k_eor, uv_bins_du=ml_gpr_config.kern.uv_bins_du,
                                               uv_bins_n_uni=ml_gpr_config.kern.uv_bins_n_uni)

        if isinstance(n_cube_slice, datacube.NoiseStdCube):
            c_injected.data = c_injected.data * (amplitude * n_cube_slice.data.mean() ** 2 / c_injected.data.var()) ** .5
        else:
            c_injected.data = c_injected.data * (amplitude * n_cube_slice.data.var() / c_injected.data.var()) ** .5

        i_cube_slice = i_cube_slice + c_injected

        ml_gpr_res = do_ml_gpr(i_cube_slice, n_cube_slice, ml_gpr_config, ps_conf, rnd_seed=rnd_seed)

        # Saving result
        ml_gpr_res.save(out_dir, 'ml_gpr_res_I')
        c_injected.save(f'{out_dir}/c_injected.h5')

        # Plotting MCMC results
        ml_gpr_res.sampler_result.plot_corner().savefig(os.path.join(out_dir, 'mcmc_corner.pdf'))
        ml_gpr_res.sampler_result.plot_samples().savefig(os.path.join(out_dir, 'mcmc_samples.pdf'))

        # Get results
        scaled_noise_cube = ml_gpr_res.get_scaled_noise_cube()
        ps_eor = ml_gpr_res.get_ps_eor(ps_gen, kbins, n_pick=500)
        ps_residual = ml_gpr_res.get_ps_res(ps_gen, kbins, n_pick=500)

        ps3d_noise = ps_gen.get_ps3d(kbins, scaled_noise_cube)

        ps_residual.save(out_dir, 'ps3d_I_residual')
        ps_eor.save(out_dir, 'ps3d_I_eor')
        ps3d_noise.save_to_txt(os.path.join(out_dir, 'ps3d_I_noise.txt'))

        fp = pspec.FourPanelPsResults(ps_gen, kbins)
        fp.add_ps_stacker(ps_residual, 'residual', c=psutil.blue)
        fp.add_ps_stacker(ps_eor, '21-cm', c=psutil.orange)
        fp.add_cube(scaled_noise_cube, 'noise', c=psutil.black)
        fp.add_cube(c_injected, 'injected', c=psutil.green)
        fp.done(ncol_legend=4)
        fp.savefig(os.path.join(out_dir, 'ps_injected.pdf'))


@main.command('combine')
@click.argument('file_list', type=t_file)
@click.option('--umin', help='Minimum baseline in lambda', type=float, default=10, show_default=True)
@click.option('--umax', help='Maximum baseline in lambda', type=float, default=1000, show_default=True)
@click.option('--weights_mode', '-w', help='Weights mode', type=str, default='full', show_default=True)
@click.option('--inhomogeneous', '-ih', help='Combine non homogeneous', is_flag=True)
@click.option('--pre_flag', help='Pre-combine flagging parset', type=t_file)
@click.option('--post_flag', help='Post-combine flagging parset', type=t_file)
@click.option('--scale_with_noise', '-s', help='Scale weights with noise estimated from Stokes V', is_flag=True)
@click.option('--output_template', '-o', help='Output template name. %STOKES% and %NUM% will be replaced',
              default='c_cube_%STOKES%_%NUM%.h5', show_default=True, type=click.Path(resolve_path=True))
@click.option('--output_multi_template', '-om',
              help='Output template name for multi cube. %STOKES% and %NUM% will be replaced.',
              default=None, type=click.Path(resolve_path=True))
@click.option('--save_intermediate', '-si', help='Save intermediate combined nights', is_flag=True)
def combine(file_list, umin, umax, weights_mode, inhomogeneous, pre_flag, post_flag, scale_with_noise,
            output_template, output_multi_template, save_intermediate):
    ''' Combine all datacubes listed in FILE_LIST

        \b
        FILE_LIST is a text file with 4 columns, whitespace separated:

        \b
        OBS_ID CUBE1_I CUBE1_V CUBE1_DT
        OBS_ID CUBE2_I CUBE2_V CUBE2_DT
        ... '''
    from ps_eor import datacube, flagger

    file_list = np.loadtxt(file_list, dtype=str)

    i_cubes = []
    v_cubes = []
    dt_cubes = []
    sefds = []
    night_ids = []

    for night_id, file_i, file_v, file_dt in file_list:
        i_cube = datacube.CartDataCube.load(file_i)
        v_cube = datacube.CartDataCube.load(file_v)
        dt_cube = datacube.CartDataCube.load(file_dt)

        i_cube.filter_uvrange(umin, umax)
        v_cube.filter_uvrange(umin, umax)
        dt_cube.filter_uvrange(umin, umax)

        if pre_flag:
            flagger_runner = flagger.FlaggerRunner.load(pre_flag)
            i_cube, v_cube = flagger_runner.run(i_cube, v_cube)
            dt_cube = flagger_runner.apply_last(dt_cube)

        noise_cube = v_cube.make_diff_cube()
        sefds.append(noise_cube.estimate_sefd())

        i_cubes.append(i_cube)
        v_cubes.append(v_cube)
        dt_cubes.append(dt_cube)
        night_ids.append(night_id)

    expected_sefd = np.mean(sefds)

    print('Mean sefd=%.1f' % expected_sefd)

    combiner_i = datacube.DataCubeCombiner(umin, umax, weighting_mode=weights_mode,
                                           inhomogeneous=inhomogeneous)
    combiner_v = datacube.DataCubeCombiner(umin, umax, weighting_mode=weights_mode,
                                           inhomogeneous=inhomogeneous)
    combiner_dt = datacube.DataCubeCombiner(umin, umax, weighting_mode=weights_mode,
                                            inhomogeneous=inhomogeneous)

    if output_multi_template is not None:
        multi_i = datacube.MultiNightsCube(inhomogeneous=inhomogeneous)
        multi_v = datacube.MultiNightsCube(inhomogeneous=inhomogeneous)
        multi_dt = datacube.MultiNightsCube(inhomogeneous=inhomogeneous)

    for i, (night_id, i_cube, v_cube, dt_cube, sefd) in enumerate(zip(night_ids, i_cubes, v_cubes, dt_cubes, sefds)):
        i_str = '%03d' % (i + 1)
        print('%s, sefd=%.1f' % (night_id, sefd))
        noise_cube = v_cube.make_diff_cube()

        if scale_with_noise:
            i_cube.weights.scale_with_noise_cube(noise_cube, sefd_poly_fit_deg=3, expected_sefd=expected_sefd)
            v_cube.weights.scale_with_noise_cube(noise_cube, sefd_poly_fit_deg=3, expected_sefd=expected_sefd)
            dt_cube.weights.scale_with_noise_cube(noise_cube, sefd_poly_fit_deg=3, expected_sefd=expected_sefd)

        combiner_i.add(i_cube, night_id)
        combiner_v.add(v_cube, night_id)
        combiner_dt.add(dt_cube, night_id)

        if output_multi_template is not None:
            multi_i.add(i_cube, night_id)
            multi_v.add(v_cube, night_id)
            multi_dt.add(dt_cube, night_id)

        if save_intermediate or i == len(night_ids) - 1:
            c_i_cube = combiner_i.get()
            c_v_cube = combiner_v.get()
            c_dt_cube = combiner_dt.get()

            if post_flag:
                flagger_runner = flagger.FlaggerRunner.load(post_flag)
                c_i_cube, c_v_cube = flagger_runner.run(c_i_cube, c_v_cube)
                c_dt_cube = flagger_runner.apply_last(c_dt_cube)

            out_i = output_template.replace('%STOKES%', 'I').replace('%NUM%', i_str)
            out_v = output_template.replace('%STOKES%', 'V').replace('%NUM%', i_str)
            out_dt = output_template.replace('%STOKES%', 'dt_V').replace('%NUM%', i_str)

            for out in [out_i, out_v, out_dt]:
                if not os.path.exists(os.path.dirname(out)):
                    os.makedirs(os.path.dirname(out))

            c_i_cube.save(out_i)
            c_v_cube.save(out_v)
            c_dt_cube.save(out_dt)

    if output_multi_template is not None:
        multi_i.done()
        multi_v.done()
        multi_dt.done()

        m_i_cube = multi_i.concat()
        m_v_cube = multi_v.concat()
        m_dt_cube = multi_dt.concat()

        out_i = output_multi_template.replace('%STOKES%', 'I').replace('%NUM%', i_str)
        out_v = output_multi_template.replace('%STOKES%', 'V').replace('%NUM%', i_str)
        out_dt = output_multi_template.replace('%STOKES%', 'dt_V').replace('%NUM%', i_str)

        for out in [out_i, out_v, out_dt]:
            if not os.path.exists(os.path.dirname(out)):
                os.makedirs(os.path.dirname(out))

        m_i_cube.save(out_i)
        m_v_cube.save(out_v)
        m_dt_cube.save(out_dt)

    print('All done !')


@main.command('combine_sph')
@click.argument('file_list', type=t_file)
@click.option('--pre_flag', help='Pre-combine flagging parset', type=t_file)
@click.option('--post_flag', help='Post-combine flagging parset', type=t_file)
@click.option('--output_template', '-o', help='Output template name. %STOKES% and %NUM% will be replaced',
              default='c_cube_%STOKES%_%NUM%.h5', show_default=True, type=click.Path(resolve_path=True))
@click.option('--save_intermediate', '-si', help='Save intermediate combined nights', is_flag=True)
def combine_sph(file_list, pre_flag, post_flag, output_template, save_intermediate):
    ''' Combine all sph datacubes listed in FILE_LIST

        \b
        FILE_LIST is a text file with 4 columns, whitespace separated:

        \b
        OBS_ID CUBE1_I CUBE1_V CUBE1_DT
        OBS_ID CUBE2_I CUBE2_V CUBE2_DT
        ... '''
    from ps_eor import sphcube, flagger, psutil

    file_list = np.loadtxt(file_list, dtype=str)

    i_cubes = []
    v_cubes = []
    dt_cubes = []
    rms_noises = []
    night_ids = []

    for night_id, file_i, file_v, file_dt in file_list:
        i_cube = sphcube.SphDataCube.load(file_i)
        v_cube = sphcube.SphDataCube.load(file_v)
        dt_cube = sphcube.SphDataCube.load(file_dt)

        flagger_runner = flagger.FlaggerRunner.load(pre_flag)
        i_cube, v_cube = flagger_runner.run(i_cube, v_cube)
        dt_cube = flagger_runner.apply_last(dt_cube)

        noise_cube = v_cube.make_diff_cube()
        rms_noises.append(psutil.mad(noise_cube.data))

        i_cubes.append(i_cube)
        v_cubes.append(v_cube)
        dt_cubes.append(dt_cube)
        night_ids.append(night_id)

    combiner_i = sphcube.SphDataCubeCombiner()
    combiner_v = sphcube.SphDataCubeCombiner()
    combiner_dt = sphcube.SphDataCubeCombiner()

    for i, (night_id, i_cube, v_cube, dt_cube, rms_noise) in enumerate(zip(night_ids, i_cubes, v_cubes,
                                                                           dt_cubes, rms_noises)):
        weight = 1 / rms_noise ** 2
        i_str = '%03d' % (i + 1)
        print('%s, rms noise = %s K' % (night_id, rms_noise))

        combiner_i.add(i_cube, weight)
        combiner_v.add(v_cube, weight)
        combiner_dt.add(dt_cube, weight)

        if save_intermediate or i == len(night_ids) - 1:
            c_i_cube = combiner_i.get()
            c_v_cube = combiner_v.get()
            c_dt_cube = combiner_dt.get()

            if post_flag:
                flagger_runner = flagger.FlaggerRunner.load(post_flag)
                c_i_cube, c_v_cube = flagger_runner.run(c_i_cube, c_v_cube)
                c_dt_cube = flagger_runner.apply_last(c_dt_cube)

            out_i = output_template.replace('%STOKES%', 'I').replace('%NUM%', i_str)
            out_v = output_template.replace('%STOKES%', 'V').replace('%NUM%', i_str)
            out_dt = output_template.replace('%STOKES%', 'dt_V').replace('%NUM%', i_str)

            for out in [out_i, out_v, out_dt]:
                if not os.path.exists(os.path.dirname(out)):
                    os.makedirs(os.path.dirname(out))

            print(out_i)

            c_i_cube.save(out_i)
            c_v_cube.save(out_v)
            c_dt_cube.save(out_dt)


def isfloat(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


class FloatRangeType(click.ParamType):
    name = 'float_range'

    def convert(self, value, param, ctx):
        if isfloat(value):
            return float(value)
        if '-' in value:
            v_s = value.split('-')
            if len(v_s) == 2 and isfloat(v_s[0]) and isfloat(v_s[1]) and float(v_s[1]) > float(v_s[0]):
                return (float(v_s[0]), float(v_s[1]))
        self.fail(f"{value!r} is not a valid float or a range of float", param, ctx)


@main.command('simu_uv')
@click.argument('instru', type=click.Choice(['ska_low', 'ska_low_aastar', 'ska_low_aa2', 'nenufar', 'nenufar_80', 'nenufar_52', 'lofar_hba', 'a12_hba',
                                             'a12_lba', 'mwa1', 'hera', 'hera_56', 'hera_120', 'hera_208', 'hera_320', 'dex'], 
                                             case_sensitive=False))
@click.argument('z', type=FloatRangeType())
@click.option('--out_filename', '-o', help='Base filename of the output file', type=str, default='simu_uv',
              show_default=True)
@click.option('--umin', help='Minimum baseline', default=None, type=int)
@click.option('--umax', help='Maximum baseline', default=None, type=int)
@click.option('--dec_deg', help='Target declination, in degrees (or "drift" for drift scan mode) (default is telescope latitude)', default=None)
@click.option(
    '--fov',
    help='Field of View side size (in deg), or "pb_fwhm" to set the FoV as the FWHM of the primary beam, '
         'or "pb_fwhm_tapered" to use 3×PB_FWHM with a Blackman–Harris window.',
    default=None, type=str
)
@click.option('--bandwidth', help='Bandwidth, in MHz', default=51 * 195.3 * 1e-3, type=float, show_default=True)
@click.option('--df', help='Spectral resolution, in kHz', default=195.3, type=float, show_default=True)
@click.option('--total_time', help='Total observing time (in hours)', default=10, type=float, show_default=True)
@click.option('--int_time', help='Integration time (in second)', default=100, type=float, show_default=True)
@click.option('--res', help='Image resolution in degrees. If not given a default 4x oversampling will be used',
              default=None, type=float)
@click.option('--allow_intra_baselines', help='Allow baselines which share the same electronic cabinet.', is_flag=True)
# z float or min-max-step
# freqs range between fmhz_min - bw/2 and fmhz_max +- bw/2
# output on file for each redshift
def simu_uv(instru, z, out_filename, umin, umax, dec_deg, fov, bandwidth, df, total_time, int_time, 
            res, allow_intra_baselines):
    ''' Compute gridded UV coverage at redshift Z for instrument INSTRU.

    INSTRU can be any of: ska_low, nenufar or lofar_hba.
    Z can be a single number or two numbers separated by ','
    '''
    from ps_eor import psutil, obssimu, datacube

    assert total_time < 24, 'total_time of one night must be < 24 hours'

    if isinstance(z, tuple):
        fmhz_lower = psutil.z_to_freq(z[1]) * 1e-6
        fmhz_upper = psutil.z_to_freq(z[0]) * 1e-6
        freqs = np.arange(fmhz_lower - bandwidth / 2, fmhz_upper + bandwidth / 2, df * 1e-3) * 1e6
        z_str = f'{z[0]:.1f}-{z[1]:.1f}'
    else:
        fmhz = psutil.z_to_freq(z) * 1e-6
        freqs = np.arange(fmhz - bandwidth / 2, fmhz + bandwidth / 2, df * 1e-3) * 1e6
        z_str = f'{z:.1f}'

    telescop = obssimu.Telescope.from_name(instru)

    if dec_deg == 'drift' or telescop.only_drift_mode:
        dec_deg = telescop.location.geodetic[1].deg
        if total_time > 0.25:
            print('Warning: drift mode but total time > 15 min, are you sure ?')
    elif dec_deg == None:
        dec_deg = telescop.location.geodetic[1].deg
    else:
        dec_deg = float(dec_deg)

    # optimal observation crossing the meridian at half time
    telescop_simu = obssimu.TelescopeSimu(telescop, freqs, dec_deg, - total_time / 2, total_time / 2, umin,
                                          umax, int_time, not allow_intra_baselines)

    print(f'Computing gridded UV configuration for instrument {telescop.name}')
    print(f'Simulating {total_time} hour long observation with {int_time} s integration time')
    print(f'Pointing : {dec_deg:.1f} deg, HA between {- total_time / 2:.2f} hr and {total_time / 2:.2f} hr')
    print(f'Redshift z = {z_str}')
    print(f'{len(freqs)} frequency channels between {freqs.min() * 1e-6:.1f} and {freqs.max() * 1e-6:.1f} MHz')
    print(f'Frequency resolution: {df:.1f} kHz')
    print(f'Baseline range: {telescop_simu.umin} - {telescop_simu.umax} lambda (discarding intra-baselines: {telescop_simu.remove_intra_baselines})')

    if telescop.redundant_array:
        uv_simu = telescop_simu.redundant_gridding()
        print(f'Redundant baselines: {uv_simu.weights.data.shape[1]}')
    else:
        win_fct = None

        if fov is None:
            fov = telescop.fov

        elif fov == 'pb_fwhm':
            pb = datacube.PrimaryBeam.from_name(telescop.pb_name)
            fov = np.degrees(pb.get_fwhm(freqs.mean()))

        elif fov in ['pb_fwhm_tapered', 'tapered_pb_fwhm']:
            pb = datacube.PrimaryBeam.from_name(telescop.pb_name)

            fwhm_deg = np.degrees(pb.get_fwhm(freqs.mean()))
            fov = 3.0 * fwhm_deg
            win_fct = datacube.WindowFunction('blackmanharris', circular=True)

            print('Using tapered FoV:')
            print(f'  PB : {pb}')
            print(f'  PB FWHM : {fwhm_deg:.2f} deg')
            print('  Window  : Blackman–Harris')

        else:
            try:
                fov = float(fov)
            except Exception:
                print('fov should be a float, "pb_fwhm", or "pb_fwhm_tapered"')
                return 1

        print(f'FoV: {fov:.1f} degrees')

        if res is not None:
            osamp_factor = int(np.round(1 / (telescop_simu.umax * np.radians(res))))
        else:
            osamp_factor = 4

        uv_simu = telescop_simu.image_gridding(fov, osamp_factor, min_weight=0, win_fct=win_fct)

        print(f'Image size: {uv_simu.weights.meta.shape}')
        print(f'Image resolution: {np.degrees(uv_simu.weights.meta.res) * 60:.2f} arcmin (oversampling: {osamp_factor})')

    name = f'{out_filename}_{telescop.name}_z{z_str}_{total_time}h'

    fig, ax = plt.subplots(figsize=(5, 4))
    uv_simu.weights.plot_uv(uv_lines=[], ax=ax, norm='log')
    ax.set_xlabel('U [lambda]')
    ax.set_ylabel('V [lambda]')
    ax.set_title('Gridded UV coverage at mid frequency')
    fig.tight_layout()
    fig.savefig(f'{name}.pdf')

    print(f'Saving UV coverage to {name}.h5 ...')
    uv_simu.save(f'{name}.h5')


@main.command('simu_noise_img')
@click.argument('uv_simu_h5', type=t_file)
@click.argument('total_time_hour', type=float)
@click.option('--out_filename', '-o', help='Base filename of the output file', type=str, default='simu_noise')
@click.option('--min_weight', help='Minimum number of visibilities in a uv-cell', default=10, type=int, show_default=True)
def simu_noise_img(uv_simu_h5, total_time_hour, out_filename, min_weight):
    ''' Compute noise fits cube from a simulated UV coverage UV_SIMU_H5 for TOTAL_TIME_HOUR observation. '''

    from ps_eor import datacube, psutil, obssimu

    simu_gridded = obssimu.SimuGridded.load(uv_simu_h5)
    freqs = simu_gridded.weights.freqs
    uv_simu = simu_gridded.get_slice(freqs[0], freqs[-1])

    if uv_simu.telescope_simu.telescop.redundant_array:
        print('Image noise cube simulation not implemented for redundant arrays')
        return

    print(f'Simulating thermal noise with mean SEFD = {uv_simu.get_sefd().mean()} Jy ...')
    print(f'{len(freqs)} frequency channels between {freqs.min() * 1e-6:.1f} and {freqs.max() * 1e-6:.1f} MHz')
    noise_cube = uv_simu.weights.simulate_noise(uv_simu.get_sefd(), total_time_hour * 3600, hermitian=False)
    noise_cube.filter_min_weight(min_weight, replace=True)
    noise_img = noise_cube.image()
    print(f'RMS noise @ mid frequency {noise_img.data[len(freqs) // 2].std()} Kelvin')

    name = f'{out_filename}_{uv_simu.name}_z{uv_simu.z:.1f}_{total_time_hour}h.fits'
    print(f'Saving noise cube to {name} ...')
    noise_img.save_to_fits(name)


@main.command('simu_noise_ps')
@click.argument('uv_simu_h5', type=t_file)
@click.argument('total_time_hour', type=float)
@click.option('--out_filename', '-o', help='Base filename of the output file', type=str, default='simu_noise')
@click.option('--kmin', help='Minimum k-mode. Default is the minimum k-mode accessible', default=None,
              type=float, show_default=False)
@click.option('--kmax', help='Maximum k-mode', default=0.5, type=float, show_default=True)
@click.option('--nks', help='Number of modes', default=7, type=int, show_default=True)
@click.option('--filter_kpar_min', help='Filter mode below kpar_min', default=None, type=float)
@click.option('--filter_wedge_theta', help='Filter mode below the wedge line', default=0, type=float)
@click.option('--sefd', help='System Equivalent Flux Density (Jy)', default=None, type=float)
@click.option('--n_incoherent_avg', help='Number of incoherent averaging', default=1, type=int)
@click.option('--min_weight', help='Minimum number of visibilities in a uv-cell', default=10, type=int, show_default=True)
def simu_noise_ps(uv_simu_h5, total_time_hour, out_filename, kmin, kmax, nks, 
                  filter_kpar_min, filter_wedge_theta, sefd, n_incoherent_avg, min_weight):
    ''' Compute noise PS from a simulated UV coverage UV_SIMU_H5 for TOTAL_TIME_HOUR observation. '''

    from ps_eor import datacube, psutil, obssimu

    simu_gridded = obssimu.SimuGridded.load(uv_simu_h5)
    freqs = simu_gridded.weights.freqs
    uv_simu = simu_gridded.get_slice(freqs[0], freqs[-1])

    ps_gen = uv_simu.get_ps_gen(filter_kpar_min, filter_wedge_theta)
    telescop = uv_simu.telescope_simu.telescop
    telescop_simu = uv_simu.telescope_simu

    print(f'Using telescope configuration {telescop.name}.')
    print(f'Baseline range: {telescop_simu.umin} - {telescop_simu.umax} lambda (discarding intra-baselines: {telescop_simu.remove_intra_baselines})')

    if kmin is None:
        kmin = ps_gen.kmin
    kbins = np.logspace(np.log10(kmin), np.log10(kmax), nks)

    if sefd is None:
        sefd = uv_simu.get_sefd()
        print(f'Simulating thermal noise with mean SEFD = {sefd.mean():.1f} Jy ...')
    else:
        print(f'Simulating thermal noise with SEFD = {sefd:.1f} Jy ...')

    print(f'{len(freqs)} frequency channels between {freqs.min() * 1e-6:.1f} and {freqs.max() * 1e-6:.1f} MHz')
    noise_std = uv_simu.get_noise_std_cube(total_time_hour * 3600, sefd=sefd, min_weight=min_weight)
    pss = {}
    pss['ps'] = ps_gen.get_ps(noise_std)
    pss['ps2d'] = ps_gen.get_ps2d(noise_std)
    pss['ps3d'] = ps_gen.get_ps3d(kbins, noise_std)

    print('Generating power-spectra ...')

    for ps_name, ps in pss.items():
        if n_incoherent_avg > 1:
            ps.err = ps.err / np.sqrt(n_incoherent_avg)
            ps.w = n_incoherent_avg * ps.w
            ps.n_eff = n_incoherent_avg * ps.n_eff

        name = f'{out_filename}_{ps_name}_{uv_simu.name}_z{uv_simu.z:.1f}_{total_time_hour}h'

        print(f'Saving {ps_name} to {name}.[txt/pdf] ...')

        fig, ax = plt.subplots(figsize=(5, 4))
        ps.plot(ax, label='Noise')

        if ps_name == 'ps3d':
            ax.plot(ps.k_mean, 2 * ps.err * 1e6, label='2-sigma sensitivity')
            ax.legend()

        fig.tight_layout()
        fig.savefig(f'{name}.pdf')

        ps.save_to_txt(f'{name}.txt')


@main.command('simu_noise_ps_zrange')
@click.argument('uv_simu_h5', type=t_file)
@click.argument('total_time_hour', type=float)
@click.argument('k', type=float)
@click.option('--out_filename', '-o', help='Base filename of the output file', type=str, default='simu_noise')
@click.option('--bandwidth', help='Bandwidth, in MHz', default=51 * 195.3 * 1e-3, type=float, show_default=True)
@click.option('--delta_z', help='Redshift step', default=0.5, type=float, show_default=True)
@click.option('--dk_over_k', help='k bin size in dk/k', default=0.4, type=float, show_default=True)
@click.option('--filter_kpar_min', help='Filter mode below kpar_min', default=None, type=float)
@click.option('--filter_wedge_theta', help='Filter mode below the wedge line', default=0, type=float)
@click.option('--min_weight', help='Minimum number of visibilities in a uv-cell', default=10, type=int, show_default=True)
@click.option('--smooth', help='Smooth the resulting sensitivity curve', is_flag=True)
@click.option('--n_incoherent_avg', help='Number of incoherent averaging', default=1, type=int)
# allow for multiple uv_simu_h5
# add k_min
def simu_noise_ps_zrange(uv_simu_h5, total_time_hour, k, out_filename, bandwidth, delta_z, dk_over_k,
                         filter_kpar_min, filter_wedge_theta, min_weight, smooth, n_incoherent_avg):
    ''' Compute noise PS from a simulated UV coverage UV_SIMU_H5 for TOTAL_TIME_HOUR observation at k of K.'''
    from ps_eor import psutil, obssimu
    from scipy.signal import savgol_filter

    simu_gridded = obssimu.SimuGridded.load(uv_simu_h5)
    z_max = np.round(psutil.freq_to_z(simu_gridded.weights.freqs.min() + bandwidth / 2 * 1e6), 1)
    z_min = np.round(psutil.freq_to_z(simu_gridded.weights.freqs.max() - bandwidth / 2 * 1e6), 1)
    zs = np.arange(z_min, z_max + delta_z, delta_z)

    k_bin = [(1 - dk_over_k / 2) * k, (1 + dk_over_k / 2) * k]

    print(f'Generating PS at k = {k}, k_bin = {k_bin[0]:.3f} - {k_bin[1]:.3f}, z = {z_min} - {z_max}')

    pks = []
    pks_err = []

    for z in zs:
        mfreq = psutil.z_to_freq(z)
        uv_simu_z = simu_gridded.get_slice(mfreq - bandwidth / 2 * 1e6, mfreq + bandwidth / 2 * 1e6)

        freqs = uv_simu_z.weights.freqs
        ps_gen = uv_simu_z.get_ps_gen(filter_kpar_min, filter_wedge_theta)

        print(f'Redshift z = {z}')
        print(f'Simulating thermal noise with mean SEFD = {uv_simu_z.get_sefd().mean():.1f} Jy ...')
        print(f'{len(freqs)} frequency channels between {freqs.min() * 1e-6:.1f} and {freqs.max() * 1e-6:.1f} MHz')

        noise_std = uv_simu_z.get_noise_std_cube(total_time_hour * 3600, min_weight=min_weight)

        ps3d = ps_gen.get_ps3d(k_bin, noise_std)
        if n_incoherent_avg > 1:
            ps3d.err = ps3d.err / np.sqrt(n_incoherent_avg)

        pks.append(ps3d.data[0] * 1e6)
        pks_err.append(ps3d.err[0] * 1e6)

    pks_err = np.array(pks_err)
    pks = np.array(pks)

    if smooth:
        w_l = min(int(psutil.get_next_odd(2 / delta_z)), int(psutil.get_previous_odd(len(zs))))
        pks = 10 ** savgol_filter(np.log10(pks), w_l, 1)
        pks_err = 10 ** savgol_filter(np.log10(pks_err), w_l, 1)

    array_data = np.array([zs, [k_bin[0]] * len(zs), [k_bin[1]] * len(zs), [k] * len(zs), pks, pks_err]).T
    header = f'Spherically averaged power-spectra {simu_gridded.name} {total_time_hour}h\n'
    header += f'Parameters: BW={bandwidth:.1f} MHz, kpar_min={filter_kpar_min}, filter_wedge={filter_wedge_theta} deg, dk/k={dk_over_k}\n'
    header += (r'z, k_min (h cMpc^-1), k_max (h cMpc^-1), k_mean (h cMpc^-1), \Delta^2 (mK^2), \Delta_err^2 (mK^2)')

    name = f'{out_filename}_ps_{simu_gridded.name}_z{z_min:.1f}-{z_max:.1f}_{total_time_hour}h_k{k}'
    np.savetxt(f'{name}.txt', array_data, fmt='%14.4f', header=header, delimiter=' ')

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(zs, pks, label=f'Noise at k={k}')
    ax.plot(zs, 2 * pks_err, label=f'2-sigma sensitivity at k={k}')
    ax.set_yscale('log')
    ax.set_xlabel('Redshift')
    ax.set_ylabel(r'$\Delta^2 (k)\,[\mathrm{mK^2}]$')
    ax.legend()
    fig.tight_layout()
    fig.savefig(f'{name}.pdf')


if __name__ == '__main__':
    main()
