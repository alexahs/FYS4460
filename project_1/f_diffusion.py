import numpy as np
import matplotlib.pyplot as plt
import sys, os
import lammps_logfile
from load_lammps_output import *
plt.style.use('ggplot')

dir = get_data_path("f")

def estimate_diffusion(dir):

    dir_files = os.listdir(dir)

    log_files = []

    for file in dir_files:
        if file[:7] == "log.msd":
            log_files.append(file)


    msd_vals = []
    T_vals = []
    dt = 0.005 # in units tau = 2.1569e3 fs

    log_files = np.sort(log_files)

    for i, filename in enumerate(log_files):
        log = lammps_logfile.File(dir + filename)
        msd = log.get("c_msd[4]")
        msd_vals.append(msd)
        T_vals.append(str(filename[10:]))

    t_vals = np.linspace(0, len(msd_vals[0])*100*dt, len(msd_vals[0]))


    for i in range(len(log_files)):
        plt.plot(t_vals, msd_vals[i], label=f'T={T_vals[i]}')

    plt.xlabel(r"$t$ $[\tau]$")
    plt.ylabel(r"$\langle r^2(t) \rangle$ $[\sigma^2]$")
    plt.legend()
    plt.show()



    D_vals = []


    for i in range(len(log_files)):
        D_vals.append(np.polyfit(t_vals[-5:], msd_vals[i][-5:], deg=1)[0] / 6)

    plt.scatter(T_vals, D_vals)
    plt.xlabel(r"$T$ $[\epsilon/k_B]$")
    plt.ylabel(r"$D(T)$ $[\sigma^2/ \tau]$")
    plt.show()



#

estimate_diffusion(dir)
