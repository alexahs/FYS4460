import numpy as np
import matplotlib.pyplot as plt
import os
from load_lammps_output import *
import seaborn as sns
import lammps_logfile
plt.style.use('ggplot')

dir = get_data_path("d")

def idea_gas_law(T):
    #P=NkT/V in lj units -> T*0.01 (lattice fcc = 0.01)
    rho = 0.01
    return T*rho


def plot_pressure(dir):
    dir_files = os.listdir(dir)
    log_files = []
    for file in dir_files:
        if file[:6] == "log.T_":
            log_files.append(file)

    n_files = len(log_files)
    mean_temp = np.zeros(n_files)
    mean_press = np.zeros(n_files)

    for i, filename in enumerate(log_files):
        log = lammps_logfile.File(dir + filename)
        temp = log.get("Temp")
        press = log.get("Press")
        equil = int(len(temp)*0.5)
        mean_temp[i] = np.mean(temp[equil:-1])
        mean_press[i] = np.mean(press[equil:-1])

    idx = np.argsort(mean_temp)

    plt.plot(mean_temp[idx], mean_press[idx], label='Simulation results')
    plt.plot(mean_temp[idx], idea_gas_law(mean_temp[idx]), label='Ideal gas law')
    plt.ylabel(r"Pressure $[P\sigma^3 / \epsilon]$")
    plt.xlabel(r"Temperature $[ Tk_b/\epsilon]$")
    plt.legend()
    plt.show()

plot_pressure(dir)


def plot_pressure_grid(dir):
    dir += "press_vs_temp_density/"
    temps = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0]
    press = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
    n_temps = len(temps)
    n_rhos = len(press)

    dirs = os.listdir(dir)
    dirs = sorted(dirs)

    press_grid = np.zeros((n_rhos, n_temps))

    for i, d in enumerate(dirs):
        log_files = os.listdir(dir + d)
        n_files = len(log_files)
        mean_temp = np.zeros(n_files)
        mean_press = np.zeros(n_files)
        density = float(d[3:])

        for j, filename in enumerate(log_files):
            log = lammps_logfile.File(dir + d + "/" + filename)
            temp = log.get("Temp")
            press = log.get("Press")
            equil = int(len(temp)*7/10)
            mean_temp[j] = np.mean(temp[equil:-1])
            mean_press[j] = np.mean(press[equil:-1])


        idx = np.argsort(mean_temp)

        press_grid[i,:] = mean_press[idx]

        if density != 0.5 and density != 1.0:
            plt.plot(mean_temp[idx], mean_press[idx], label=rf'$\rho={density}$')

    plt.xlabel(r"Pressure $[P\sigma^3 / \epsilon]$")
    plt.ylabel(r"Temperature $[ Tk_b/\epsilon]$")
    plt.legend()
    plt.show()


# plot_pressure_grid(dir)



#
