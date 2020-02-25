import numpy as np
import matplotlib.pyplot as plt
import os
from .load_lammps_output import *



def read_rdf_dump(dir, filename,
                  n_time_steps = 10000,
                  step_window = 100,
                  n_bins = 50,
                  n_info_lines = 3):
    """
    Function for reading radial distribution g(r) values produced by
    <<compute myRDF all rdf 50>>
    <<fix 2 all ave/time 100 1 100 c_myRDF[*] file tmp.rdf mode vector>>
    commands in lammps.

    Returns: array of radial distances and avg g(r)
    """

    n_time_windows = int(n_time_steps/step_window) +1

    radials = np.zeros((n_bins, n_time_windows))
    bin_distances = np.zeros(n_bins)



    with open(dir + filename, 'r') as infile:
        for skip in range(n_info_lines+1):
            skipline = infile.readline()

        #get bin distances and g(r) in first time window
        for i in range(n_bins):
            linestr = np.fromstring(infile.readline(),
                                           dtype='float',
                                           count=3,
                                           sep=' ')

            bin_distances[i] = float(linestr[1])
            radials[i, 0] = float(linestr[2])


        #get g(r) for remaining time windows
        for t in range(1, n_time_windows):
            skipline = infile.readline()

            for i in range(n_bins):
                radials[i, t] = np.fromstring(infile.readline(),
                                               dtype='float',
                                               count=3,
                                               sep=' ')[2]

        infile.close()
    #end readfile



    avg_radials = np.mean(radials, axis=1)

    return bin_distances, avg_radials


def plot_radial_distribution(dir,
                             n_time_steps = 10000,
                             step_window = 100,
                             n_bins = 50,
                             n_info_lines = 3):

    dir_files = os.listdir(dir)
    log_files = []

    for file in dir_files:
        if file[:7] == "tmp.rdf":
            log_files.append(file)


    log_files = np.sort(log_files)
    # print(log_files)
    
    for file in log_files:
        bins, radials = read_rdf_dump(dir, file)
        plt.plot(bins, radials, label="T=" + file[10:])

    plt.legend()
    plt.xlabel(r"Radial distance")
    plt.ylabel(r"$g(r)$")
    plt.show()
