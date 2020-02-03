import numpy as np
import matplotlib.pyplot as plt
import sys, os
# from lib.analyze_velocity_distribution import *
# from lib.analyze_dt import *
# from lib.measure_temp import *
# from lib.read_thermo_log import *
from lib import *


def get_sim_path(part, sim):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    #ex root_dir + "/sim_files/part_a/sim1/"

    return root_dir + "/sim_files/part_" + str(part) + "/sim" + str(sim) + "/"


def main():

    dir = get_sim_path("d", 1)

    # analyze_velocity_distribution(dir_part_a)
    # analyze_dt(dir_part_b)
    # measure_temp(dir_part_c)

    # temp_press = read_thermo_log(dir=dir, filename = "log.lammps", names_of_measurements = "Temp Press")

    # print(temp_press)

    plot_temp_press(dir=dir)


    exit(1)









if __name__ == '__main__':
    main()
