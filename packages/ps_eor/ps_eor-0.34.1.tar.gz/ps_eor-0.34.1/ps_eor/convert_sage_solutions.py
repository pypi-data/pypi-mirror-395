#! /usr/bin/env python
import os
import glob
import numpy as np

from casacore import tables

def get_ms_info(ms_file):
    ms=tables.table(ms_file)

    timerange = [np.amin(ms.getcol('TIME_CENTROID')), np.amax(ms.getcol('TIME_CENTROID'))]
    timestep = ms.getcell('INTERVAL', 0)
    
    pointing = tables.table(ms.getkeyword('FIELD')).getcell('PHASE_DIR', 0);    
    stations = tables.table(ms.getkeyword('ANTENNA')).getcol('NAME')
    station_pos = tables.table(ms.getkeyword('ANTENNA')).getcol('POSITION')

    return (timerange, timestep, pointing.flatten(), stations, station_pos)



@click.command()
@click.version_option(__version__)
@click.argument('ms_list', type=str)
@click.argument('out_dir', type=str)
def main(ms_list, out_dir):
    alldatas = []
    freqs = []
    ms_files = [k.strip().split() for k in open(ms_list).readlines() if k.strip()]
    obs_id = os.path.basename(ms_files[0]).strip('_')[0]
    ms_sols = [k + '.solutions' for k in ms_files]

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    
    timerange, timestep, pointing, stations, station_pos = get_ms_info(ms_files[0])
    
    for ms_sol in ms_sols:
        with open(ms_sol) as f:
            for i in range(3):
                a = f.readline()
            freq, bw, timestep, nStations, nClust, nClustEff = tuple([float(i) for i in a.split()])
        data = np.loadtxt(fname, skiprows=3, usecols=tuple(range(1, int(nClustEff) + 1)), unpack=True)
        datas = []
        for i in range(int(nClustEff)):
            a = data[i].reshape((-1, int(nStations), 4, 2))
            cdata = a[:, :, :, 0] + 1.j * a[:, :, :, 1]
            datas.append(cdata)
        freqs.append(freq)
        alldatas.append(datas)
    
    mysorted = zip(*sorted(zip(freqs, alldatas)))

    cdata = (np.array(mysorted[1])[:, args.cluster[0]:args.cluster[1]]).transpose((2, 3, 0, 4, 1))
    data = np.zeros(cdata.shape + (2,), dtype=np.float64)
    data[:, :, :, :, :, 0] = np.real(cdata)
    data[:, :, :, :, :, 1] = np.imag(cdata)
    timestep = (timerange[1] - timerange[0]) / (data.shape[0] - 1)

    np.savez("%s/%s" % (out_dir, obs_id),
            freqs=np.array(mysorted[0]) * 1.e6, 
            timerange=timerange, 
            timestep=timestep, 
            stations=stations, 
            stat_pos=station_pos, 
            pointing=pointing)
    np.save("%s/%s" % (out_dir, obs_id), data)

if __name__ == '__main__':
    main()
