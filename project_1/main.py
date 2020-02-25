import numpy as np
import matplotlib.pyplot as plt
import sys, os
from lib import *
plt.style.use('ggplot')



def get_sim_path(part, sim):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    #ex root_dir + "/sim_files/part_a/sim1/"

    return root_dir + "/sim_files/" + str(part) + "/sim" + str(sim) + "/"


def main():

    dir = get_sim_path("g", 1)


    plot_radial_distribution(dir)
    # estimate_diffusion(dir)
    # berendsen(dir, filename='log.lammps')
    # get_variables(dir)

    # data = read_thermo(dir, "log.T_400", "Temp")
    # print(data)







if __name__ == '__main__':
    main()
