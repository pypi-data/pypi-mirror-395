#!/usr/bin/env python

import sys

import click
import numpy as np

from scipy.interpolate import BPoly


parser = ArgumentParser(description="Convert B-pol solution file to gain solution in npy format")
parser.add_argument('z_sol_file', help='Input Z solution file in txt format')
parser.add_argument('meta_data_file', help='Meta data file in npz format')
parser.add_argument('--eff_nr', help='File describing Number of effective clusters per clusters', required=False,
                    default=None)

@click.command()
@click.argument('z_sol_file', type=str)
@click.argument('meta_data_file', type=str)
@click.option('-e', '--eff_nr', type=str, default=None)
def main(z_sol_file, meta_data_file, eff_nr):
    print('Reading z solutions ...')

    with open(z_sol_file) as f:
        for i, line in enumerate(f.readlines()):
            if i == 2:
                _, p_order, n_stat, n_clus, n_eff_clus = line.strip().split()
                p_order = int(p_order)
                n_stat = int(n_stat)
                n_clus = int(n_clus)
                n_eff_clus = int(n_eff_clus)
                break

    z_sol = np.loadtxt(z_sol_file, skiprows=3)

    print('Reading meta data ...')

    meta_data = np.load(meta_data_file)
    n_freqs = len(meta_data['freqs'])

    print(f'Data with {n_stat} stations, {n_clus} clusters, {n_eff_clus} eff. clusters,, {p_order} poly order, {n_freqs} subbands')

    assert z_sol.shape[1] - 1 == n_eff_clus

    if n_eff_clus != n_clus:
        if not eff_nr:
            print('n_clus != n_eff_clus; eff_nr required !')
            sys.exit(0)
        eff_nr = np.load(eff_nr)

        assert len(eff_nr) == n_clus
        assert eff_nr.sum() == n_eff_clus

        eff_nr_idx = []
        i = 0
        for n_eff in eff_nr:
            eff_nr_idx.extend(np.arange(i + n_eff - 1, i - 1, -1).astype(int))
            i += n_eff
        eff_nr_idx = np.array(eff_nr_idx)

    x = np.linspace(0, 1, n_freqs)

    a_poly_sol = []

    print('Converting z solutions ...')

    for i_c in np.arange(n_eff_clus):
        z_sol_mat = z_sol[:, i_c + 1].reshape((-1, p_order, n_stat, 4, 2))
        z_sol_mat = z_sol_mat.transpose((1, 0, 2, 3, 4))

        poly_sol = BPoly(z_sol_mat[:, None], [0, 1])(x)

        poly_sol = poly_sol.transpose((1, 0, 2, 3, 4))
        poly_sol = poly_sol.transpose((0, 2, 1, 3, 4))

        a_poly_sol.append(poly_sol)

    a_poly_sol = np.stack(a_poly_sol, -1)
    a_poly_sol = a_poly_sol.transpose((0, 1, 2, 3, 5, 4))

    if n_eff_clus != n_clus:
        a_poly_sol = a_poly_sol[:, :, :, :, eff_nr_idx, :]

    if args.output_name is not None:
        output_name = args.output_name
    else:
        output_name = args.z_sol_file + '.npy'

    print('Saving to %s ...' % output_name)

    np.save(output_name, a_poly_sol)

    print('All done !')


if __name__ == '__main__':
    main()
