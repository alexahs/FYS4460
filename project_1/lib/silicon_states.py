from .load_lammps_output import *
import lammps_logfile
import numpy as np
import matplotlib.pyplot as plt




"""
TODO:
Visualize systems of silicon in solid, liquid and gas states
"""


def silicon_diffusion(dir):


    files_dir = os.listdir(dir)

    log_files = []
    for file in files_dir:
        if "log.T" in file:
            log_files.append(file)

    data_dict = {}
    avg_temps = []
    for file in log_files:
        log = lammps_logfile.File(os.path.join(dir, file))

        T_temp = log.get("Temp")
        size = T_temp.shape[0]
        size_2 = size//2
        T = T_temp[size_2:]
        t = log.get("Time")[size_2:]
        msd = log.get("c_msd[4]")[size_2:]




        avg_temp = int(np.mean(T))
        avg_temps.append(avg_temp)
        data_dict["T_" + str(avg_temp)] = T
        data_dict["msd_" + str(avg_temp)] = msd


    # print(data_dict['T_1913'])
    # print(data_dict['msd_1913'])

    n_files = len(log_files)

    diffusion = np.zeros(n_files)

    print(data_dict["msd_" + str(avg_temps[0])].shape)
    print(t.shape)
    #
    for i in range(n_files):
        diffusion[i] = np.polyfit(t, data_dict["msd_" + str(avg_temps[i])], deg=1)[0]

    plt.scatter(avg_temps, diffusion, c="g", label="Simulated results")
    plt.xlabel("Temperature")
    plt.ylabel("Diffusion constant (arbitrary scale)")
    plt.plot([1687, 1687], [0, diffusion.max()], "b--", label="Experimental melting point")
    plt.plot([3538, 3538], [0, diffusion.max()], "r--", label="Experimental boiling point")
    plt.legend()
    plt.show()




















#
