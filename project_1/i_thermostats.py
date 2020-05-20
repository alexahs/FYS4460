import numpy as np
import matplotlib.pyplot as plt
import sys, os
import lammps_logfile
from load_lammps_output import *
plt.style.use('ggplot')


dir = get_data_path("i")

def plot_thermostat(dir):


    log_be = lammps_logfile.File(dir + "log.berendsen")
    log_nh = lammps_logfile.File(dir + "log.nosehoover")

    T_be = log_be.get("Temp")
    T_nh = log_nh.get("Temp")
    t = np.linspace(0, len(T_be)*0.005, len(T_be))

    plt.plot(t, T_be, label='Berendsen')
    plt.plot(t, T_nh, label='Nosé-Hoover')
    plt.xlabel(r"t")
    plt.ylabel(r"T")
    plt.legend()
    plt.show()


plot_thermostat(dir)
