import numpy as np
import matplotlib.pyplot as plt
import sys, os
import lammps_logfile
from load_lammps_output import *
import natsort
plt.style.use('ggplot')

dir = get_data_path("m") + "data/"


def read_rdf_dump(dir, filename,
                  n_time_steps = 1000,
                  step_window = 10,
                  n_bins = 50,
                  n_info_lines = 3):
    """
    Function for reading radial distribution g(r) values produced by
    <<compute myRDF all rdf 50>>
    <<fix 2 all ave/time 100 1 100 c_myRDF[*] file tmp.rdf mode vector>>
    commands in lammps.

    Returns: array of radial distances and avg g(r)
    """
    params = get_dump_params(dir)
    n_time_windows = params['TIME_STEPS']
    step_window = params['THERMO_STEP']
    # n_time_windows = int(n_time_steps/step_window) +1

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
                             n_time_steps = 5000,
                             step_window = 100,
                             n_bins = 50,
                             n_info_lines = 3):

    dir_files = os.listdir(dir)
    log_files = []

    for file in dir_files:
        if file[:7] == "log.rdf":
            log_files.append(file)


    # log_files = np.sort(log_files)
    log_files = natsort.natsorted(log_files)

    print(log_files)

    # T_init_vals = list(range(20, 300, 20))

    for i, file in enumerate(log_files):
        # T_init = float(file[10:])
        T = int(file[10:])
        # T = T_init_vals[i]
        log = lammps_logfile.File(dir + f"log.rdf_T_{T}")
        # T = log.get("Temp")
        # idx = len(T) / 2
        bins, radials = read_rdf_dump(dir, file)
        # T_mean = np.mean(T)
        plt.plot(bins, radials/radials[-1], label=f"T={T:d}")

    plt.legend(loc=1)
    plt.xlabel(r"$r$")
    plt.ylabel(r"$g(r)$")
    plt.show()


# plot_radial_distribution(dir)

def plot_diffusion(dir):

    dir_files = os.listdir(dir)

    log_files = []

    for file in dir_files:
        if file[:7] == "log.msd":
            log_files.append(file)


    msd_vals = []
    T_vals = []
    dt = 1.0

    log_files = natsort.natsorted(log_files)

    for i, filename in enumerate(log_files):
        log = lammps_logfile.File(dir + filename)
        msd = log.get("c_msd[4]", run_num=0)
        # print(msd)
        msd_vals.append(msd)
        T_vals.append(str(filename[10:]))

    t_vals = np.linspace(0, len(msd_vals[0])*10, len(msd_vals[0]))


    for i in range(len(log_files)):
        plt.plot(t_vals, msd_vals[i], label=f'T={T_vals[i]}')

    plt.xlabel(r"$t$ [fs]")
    plt.ylabel(r"$\langle r^2(t) \rangle$ [A$^2$]")
    plt.legend()
    plt.show()



    D_vals = []

    idx = 20
    for i in range(len(log_files)):
        D_vals.append(np.polyfit(t_vals[-idx:], msd_vals[i][-idx:], deg=1)[0] / 6)

    plt.scatter(T_vals, D_vals)
    plt.xlabel(r"$T$ [K]")
    plt.ylabel(r"$D(T)$ [A$^2$/fs]")
    plt.show()



#

plot_diffusion(dir)
