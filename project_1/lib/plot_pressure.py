import numpy as np
import matplotlib.pyplot as plt
import os
from .load_lammps_output import *


def plot_pressure(dir):

    # print(os.listdir(dir))

    dir_files = os.listdir(dir)

    log_files = []

    for file in dir_files:
        if file[:6] == "log.T_":
            log_files.append(file)


    names_of_measurements = "Temp Press"
    n_time_steps = 10000
    step_window = 100


    for i, filename in enumerate(log_files):
        data = read_thermo(dir, filename,
                           names_of_measurements,
                           n_time_steps,
                           step_window)
        #
        # data.shape = (101, 2)
        mean_temp = np.mean(data[90:-1,0], axis=0)
        mean_press = np.mean(data[90:-1,1], axis=0)
        print(mean_temp.shape)

    # print(temp_press)

    # idx = np.argsort(temp_pressure[:,0])
    #
    # temp = temp_pressure[:,0][idx]
    # press = temp_pressure[:,1][idx]


    # plt.plot(temp, press)
    # plt.show()
