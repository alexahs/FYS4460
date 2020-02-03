import numpy as np


def read_thermo_log(dir, filename, names_of_measurements, steps = 10000, step_window = 100):
    """
    Function for reading LAMMPS thermo dump files.

    INPUTS:
        - dir (str): full directory of log file
        - filename (str): name of log file
        - names_of_measurements (str): names of the measurements (for pattern matching, case sensitive)
        - steps (int): number of time steps in simulation
        - step_window (int): number of time steps between each write in the log file

    OUTPUT:
        - results (array): simulation results, size: (n_read_lines, n_measurement_types)

    """
    n_read_lines = int (steps/step_window) + 1
    n_measurement_types = names_of_measurements.count(" ") + 1
    n_chars = len(names_of_measurements)

    results = np.zeros((n_read_lines, n_measurement_types))

    with open(dir + filename, 'r') as infile:
        for line in infile:
            if line[:n_chars] == names_of_measurements:
                for i in range(n_read_lines):
                    results[i] = np.fromstring(infile.readline(), dtype='float', count=n_measurement_types, sep=' ')

    return results
#
