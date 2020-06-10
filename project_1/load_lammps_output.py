import numpy as np
import sys
import os
from tqdm import tqdm

def get_data_path(exercise):
    root_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(root_dir, "sim_files", str(exercise) + "/")

def get_dump_params(dir, lmp_suffix='.lmp',
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
                    print("Unable to convert _{}_ to integer".format(var_val))
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

    params = get_dump_params(dir)

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
              n_time_steps = None,
              step_window = None,
              save_to_npy = False):

    """
    Naive function for reading lammps dumpfiles.
    Dumped items must contain ID and type.
    """


    if n_time_steps is None and step_window is None:
        params = get_dump_params(dir)
        n_time_steps = params['TIME_STEPS']
        step_window = params['DUMP_STEP']

    n_info_lines = 9

    with open(dir + filename, 'r') as infile:
        for i in range(3):
            skipline = infile.readline()
        n_atoms = infile.readline()
        try:
            n_atoms = int(n_atoms)
        except:
            print(f"n_atoms could not be converted to int: {n_atoms}")
        for i in range(4):
            skipline = infile.readline()

        item_str = infile.readline()
        items = item_str.split(" ")[4:-1]


    n_observables = len(items)

    n_time_windows = int(n_time_steps/step_window)

    results = np.zeros((n_atoms, n_observables, n_time_windows))

    print(f'Reading dump of items: {items}')
    print(f"# of time steps: {n_time_steps}")
    print(f"# of atoms:      {n_atoms}")
    with open(dir + filename, 'r') as infile:
        for t in tqdm(range(n_time_windows)):
            for _ in range(n_info_lines):
                skipline = infile.readline()

            for i in range(n_atoms):
                results[i,:,t] = np.fromstring(infile.readline(),
                                               dtype='float',
                                               count=n_observables + 2,
                                               sep=' ')[2:]
        infile.close()

    if save_to_npy:
        filename = "dump"
        for item in items:
            filename += "_" + item
        filename += ".npy"
        savefile = dir + filename
        np.save(savefile, results)
        print('Dump saved to %s' %savefile)

    return results







    #
