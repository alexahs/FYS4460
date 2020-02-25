import numpy as np
import sys
import os
from tqdm import tqdm



def get_params(dir, lmp_suffix='.lmp',
                       env_start = '#assign params',
                       env_stop = '#end assign params',
                       verbose = False):

    files = np.array(os.listdir(dir))
    params = {}
    lmp_script = None

    for f in files:
        if f[-4:] == lmp_suffix:
            lmp_script = f
            break

    if lmp_script == None:
        print('LAMMPS script not found in {}'.format(dir))
        exit(1)
    else:
        if verbose:
            print('Looking up parameters from {}..'.format(lmp_script))


    with open(dir + lmp_script, 'r') as infile:
        infile.readline()
        while True:
            words = infile.readline().split()
            if words[0] == env_stop.split()[0]:
                break
            else:
                var_name = words[1]
                var_val = words[-1]
                try:
                    params[var_name] = int(var_val)
                except:
                    print("Unable to convert {} to integer".format(var_val))
                    exit(1)
    infile.close()

    if verbose:
        print('Parameters:')
        for key in params:
            print(key, params[key])

    return params





def read_thermo(dir, filename, names_of_measurements):
    """
    Function for reading LAMMPS thermo log files.

    Parameters:
        dir : string
            full directory of log file.
        filename : string
            name of the log file.
        names_of_measurements : string
            names of the measurements (for pattern matching, case sensitive).

    Returns:
        results : array
            contains the quantities read from the log file.
    """

    params = get_params(dir)

    n_time_steps = params['TIME_STEPS']
    step_window = params['THERMO_STEP']


    n_read_lines = int (n_time_steps/step_window) + 1
    n_types = names_of_measurements.count(" ") + 1
    n_chars = len(names_of_measurements)

    results = np.zeros((n_read_lines, n_types))

    with open(dir + filename, 'r') as infile:
        for line in infile:
            if line[:n_chars] == names_of_measurements:
                for i in range(n_read_lines):
                    results[i] = np.fromstring(infile.readline(), dtype='float', count=n_types, sep=' ')
        infile.close()

    return results


def read_dump(dir, filename,
              n_atoms = 4000,
              n_info_lines = 9,
              n_types = 3,
              dims = 3,
              save_to_npy = False):

    params = get_params(dir)
    n_time_steps = params['TIME_STEPS']
    step_window = params['DUMP_STEP']

    n_time_windows = int(n_time_steps/step_window)

    results = np.zeros((n_atoms, dims, n_time_windows))


    print('Loading dump..')
    with open(dir + filename, 'r') as infile:
        for t in tqdm(range(n_time_windows)):
            for _ in range(n_info_lines):
                skipline = infile.readline()

            for i in range(n_atoms):
                results[i,:,t] = np.fromstring(infile.readline(),
                                               dtype='float',
                                               count=n_types,
                                               sep=' ')
        infile.close()

    if save_to_npy:
        savefile = dir + 'dump.npy'
        np.save(savefile, results)
        print('Dump saved to %s' %savefile)

    return results









    #
