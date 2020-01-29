import numpy as np
import matplotlib.pyplot as plt
import sys, os
from lib.analyze_velocity_distribution import *




def convert_dump_to_npy(data_dir, input_file, n_atoms = 4000, n_timesteps = 10000, steps_per_window = 10):

    n_time_windows = int(n_timesteps/steps_per_window)
    dims = 3
    n_info_lines = 9

    vel_timeseries = np.zeros((n_atoms, dims, n_time_windows))


    infile = open(input_file, 'r')

    pc0 = 0
    for t in range(n_time_windows):
        for _ in range(n_info_lines):
            trash = infile.readline()

        for i in range(n_atoms):
            vel_timeseries[i,:,t] = np.fromstring(infile.readline()[1:], dtype='float', count=3, sep=' ')

        pc = int((t / n_time_windows)*100)
        if pc0 != pc:
            pc0 = pc
            print(pc, "%")

    outfile = 'velocity_timeseries.npy'

    np.save(data_dir + outfile, vel_timeseries)
    print("dump converted to " + data_dir + outfile)

    return None

def compute_temp(filename, n_time_windows = 1000):


    velocities = np.load(filename)


    temperatures = np.zeros(velocities.shape[2])

    for i in range(n_time_windows):
        temperatures[i] = np.sum(np.sum(velocities[:,:,i]**2, axis = 1))



    temperatures /= 3

    plot_hist(velocities, component=0)




def measure_temp(data_dir):

    infile  = data_dir + "/dump.lammpstrj"
    if len(sys.argv) > 1:
        convert_dump_to_npy(data_dir, infile)


    vel_npy = data_dir + "/velocity_timeseries.npy"

    compute_temp(vel_npy)









    #
