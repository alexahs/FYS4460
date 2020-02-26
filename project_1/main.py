import numpy as np
import matplotlib.pyplot as plt
import sys, os
import lammps_logfile
from lib import *
plt.style.use('ggplot')



# def get_sim_path(part, sim):
#     root_dir = os.path.dirname(os.path.abspath(__file__))
#
#     #ex root_dir + "/sim_files/part_a/sim1/"
#
#     return os.path.join(root_dir, "sim_files", str(part), "sim" + str(sim))
#
#
# def get_file_path(dir, filename):
#     return os.path.join(os.path.dirname(__file__), dir, filename)





def main():

    project_root_dir = os.path.dirname(os.path.abspath(__file__))

    dir = get_sim_path(project_root_dir, "k", 1)


    # plot_radial_distribution(dir)
    # estimate_diffusion(dir)
    # berendsen(dir, filename='log.lammps')
    # get_variables(dir)

    # data = read_thermo(dir, "log.T_400", "Temp")
    # print(data)






    filename = "log.T_4000_scale_0.99"


    silicon_diffusion(dir)


    # log = lammps_logfile.File(get_file_path(dir, filename))
    # plt.plot()
    # print(log.get("Time"))
    # keywords = log.get_keywords()




if __name__ == '__main__':
    main()
