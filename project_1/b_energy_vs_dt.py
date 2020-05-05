import numpy as np
import matplotlib.pyplot as plt
import sys, os
import lammps_logfile
from load_lammps_output import *
plt.style.use('ggplot')

dir = get_data_path("b")


def energy_vs_dt(dir):
    items = os.listdir(dir)
    log_files = []
    for name in items:
        if name[:6] == "log.dt":
            log_files.append(name)

    log_files = sorted(log_files)
    n_files = len(log_files)


    for file in log_files:
        log = lammps_logfile.File(dir + file)
        dt = float(file[7:])
        time = log.get("v_time")
        etot = log.get("TotEng")
        plt.plot(time, etot, label=rf"$\Delta t = {dt}$")

    plt.legend()
    plt.xlabel(r"Time $[\tau]$")
    plt.ylabel(r"Energy $[\epsilon]$")
    plt.show()

energy_vs_dt(dir)
