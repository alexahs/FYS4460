import numpy as np
import matplotlib.pyplot as plt
import sys, os
from .load_lammps_output import *



def analyze_dt(dir):


    items = os.listdir(dir)


    filenames = []
    for name in items:
        if name[:6] == "log.dt":
            filenames.append(name)

    filenames = sorted(filenames)
    n_files = len(filenames)
    n_read_lines = 101
    n_types = 4

    quantities = "Temp PotEng KinEng TotEng"

    measurements = np.zeros((n_read_lines, n_types, n_files))
    for i in range(n_files):
        measurements[:,:,i] = read_thermo(dir, filenames[i], quantities)


    for i in range(n_files):
        label = "%s" %filenames[i][4:]
        # plt.plot(list(range(measurements.shape[0])), measurements[:,1, i], label='PotEng')
        # plt.plot(list(range(measurements.shape[0])), measurements[:,2, i], label='KinEng')
        plt.plot(list(range(measurements.shape[0])), measurements[:,3, i], label=label) #totEng


    plt.xlabel(r"$t_i$")
    plt.ylabel(r"Total energy $E/\epsilon$")
    plt.legend()
    plt.show()
