import numpy as np
import matplotlib.pyplot as plt
import os
from .load_lammps_output import *





def estimate_diffusion(dir):

    dir_files = os.listdir(dir)

    log_files = []

    for file in dir_files:
        if file[:7] == "log.msd":
            log_files.append(file)


    log_files = np.sort(log_files)
    names_of_measurements = "c_msd[4]"
    n_time_steps = 10000
    step_window = 100
    n_steps = int(n_time_steps/step_window)+1


    n_files = len(log_files)

    msd_array = np.zeros((n_steps, n_files))

    for i, filename in enumerate(log_files):
        msd_array[:,i] = np.squeeze(read_thermo(dir, log_files[i],
                                     names_of_measurements,
                                     n_time_steps,
                                     step_window))

        plt.plot(range(n_steps), msd_array[:,i])

    plt.show()




    t0 = 0
    t1 = n_steps
    t = np.linspace(t0, t1 , t1-t0)

    D_vals = np.zeros(n_files)
    temp_vals = np.zeros(n_files)
    for i in range(n_files):
        D_vals[i] = np.polyfit(t, msd_array[t0:t1,i], deg=1)[0]
        temp_vals[i] = float(log_files[i][10:])

    D_vals/100

    plt.scatter(temp_vals, D_vals)
    plt.show()



#
