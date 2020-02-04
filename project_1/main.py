import numpy as np
import matplotlib.pyplot as plt
import sys, os
from lib import *
plt.style.use('ggplot')



def get_sim_path(part, sim):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    #ex root_dir + "/sim_files/part_a/sim1/"

    return root_dir + "/sim_files/part_" + str(part) + "/sim" + str(sim) + "/"


def main():

    dir = get_sim_path("a", 1)

    # analyze_dt(dir)

    vel = read_dump(dir, "dump.lammpstrj", n_time_steps=5000)
    # vel = np.load(dir + "dump.npy")

    # plot_velocity_distribution(vel)



    exit(1)









if __name__ == '__main__':
    main()
