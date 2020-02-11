import numpy as np
import matplotlib.pyplot as plt
import os
from .load_lammps_output import *


def idea_gas_law(T):
    #P=NkT/V in lj units -> T*0.01 (lattice fcc = 0.01)
    rho = 0.01
    return T*rho


def plot_pressure(dir):


    dir_files = os.listdir(dir)

    log_files = []

    for file in dir_files:
        if file[:6] == "log.T_":
            log_files.append(file)


    names_of_measurements = "Temp Press"
    n_time_steps = 10000
    step_window = 100

    n_files = len(log_files)
    mean_temp = np.zeros(n_files)
    mean_press = np.zeros(n_files)


    for i, filename in enumerate(log_files):
        data = read_thermo(dir, filename,
                           names_of_measurements,
                           n_time_steps,
                           step_window)
        #
        # data.shape = (101, 2)
        mean_temp[i] = np.mean(data[-10:-1, 0])
        mean_press[i] = np.mean(data[-10:-1, 1])
        # print(data[90:-1,0])

    idx = np.argsort(mean_temp)

    print(mean_press[idx])
    print(mean_temp[idx])

    plt.plot(mean_temp[idx], mean_press[idx], label='simulated')
    plt.plot(mean_temp[idx], idea_gas_law(mean_temp[idx]), label='P=NkT/V')
    plt.xlabel(r"Pressure $[\epsilon/k_b]$")
    plt.ylabel(r"Temperature $[\sigma^3 / \epsilon]$")
    plt.legend()
    plt.show()

    # print(temp_press)

    # idx = np.argsort(temp_pressure[:,0])
    #
    # temp = temp_pressure[:,0][idx]
    # press = temp_pressure[:,1][idx]


    # plt.plot(temp, press)
    # plt.show()
