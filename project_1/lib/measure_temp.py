import numpy as np
import matplotlib.pyplot as plt
import sys, os
from lib.plot_velocity_distribution import *



def compute_temp(velocities):

    n_time_windows = 500
    temperatures = np.zeros(velocities.shape[2])


    for i in range(n_time_windows):
        temperatures[i] = np.sum(np.sum(velocities[:,:,i]**2, axis = 1))



    temperatures /= 3*4000

    # plot_velocity_distribution(velocities, vel_components = [1])

    plt.plot(range(len(temperatures)), temperatures)
    plt.show()
    # print(temperatures)



def measure_temp(data_dir):

    infile  = data_dir + "/dump.lammpstrj"
    if len(sys.argv) > 1:
        convert_dump_to_npy(data_dir, infile)


    vel_npy = data_dir + "/velocity_timeseries.npy"

    compute_temp(vel_npy)









    #
