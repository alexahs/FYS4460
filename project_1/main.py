import numpy as np
import matplotlib.pyplot as plt
import sys, os
from lib import *


def get_sim_path(part, sim):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    #ex root_dir + "/sim_files/part_a/sim1/"

    return root_dir + "/sim_files/part_" + str(part) + "/sim" + str(sim) + "/"


def main():

    dir = get_sim_path("b", 1)

    analyze_dt(dir)

    # analyze_velocity_distribution(dir_part_a)
    # analyze_dt(dir_part_b)
    # measure_temp(dir_part_c)

    # temp_press = read_thermo_log(dir=dir, filename = "log.lammps", names_of_measurements = "Temp Press")

    # print(temp_press)

    # plot_temp_press(dir=dir)

    # vel = read_dump(dir, "dump.lammpstrj", n_time_steps=5000, save_to_npy=True)
    # vel = np.load(dir + "dump.npy")
    # analyze_velocity_distribution(vel, vel_component=1)

    exit(1)









if __name__ == '__main__':
    main()
