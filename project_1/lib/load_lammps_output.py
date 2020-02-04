import numpy as np
import sys
from tqdm import tqdm


def read_thermo(dir, filename,
                names_of_measurements,
                n_time_steps = 10000,
                step_window = 100):
    """
    Function for reading LAMMPS thermo log files.

    Parameters:
        dir : string
            full directory of log file.
        filename : string
            name of the log file.
        names_of_measurements : string
            names of the measurements (for pattern matching, case sensitive).
        n_time_steps : int
            number of time steps in simulation
        step_window : int
            number of time steps between each write in the log file.

    Returns:
        results : array
            contains the quantities read from the log file.
    """

    n_read_lines = int (n_time_steps/step_window) + 1
    n_types = names_of_measurements.count(" ") + 1
    n_chars = len(names_of_measurements)

    results = np.zeros((n_read_lines, n_types))

    with open(dir + filename, 'r') as infile:
        for line in infile:
            if line[:n_chars] == names_of_measurements:
                for i in range(n_read_lines):
                    results[i] = np.fromstring(infile.readline(), dtype='float', count=n_types, sep=' ')

    return results


def read_dump(dir, filename,
              n_time_steps = 10000,
              step_window = 10,
              n_atoms = 4000,
              n_info_lines = 9,
              n_types = 3,
              dims = 3,
              read_atom_id = False,
              save_to_npy = False):

    n_time_windows = int(n_time_steps/step_window)

    results = np.zeros((n_atoms, dims, n_time_windows))

    start_read = 0 if read_atom_id == True else 1

    pc0 = 0
    with open(dir + filename, 'r') as infile:
        for t in tqdm(range(n_time_windows)):
            # print("t= ", t, "/", n_time_windows)
            for _ in range(n_info_lines):
                skipline = infile.readline()

            for i in range(n_atoms):
                results[i,:,t] = np.fromstring(infile.readline()[start_read:],
                                               dtype='float',
                                               count=n_types,
                                               sep=' ')

    if save_to_npy:
        np.save(dir + 'dump.npy', results)

    return results







    #
