import numpy as np
import matplotlib.pyplot as plt
import sys, os
import lammps_logfile
from load_lammps_output import *
plt.style.use('ggplot')

dir = get_data_path("c")

def compute_temp(velocities):

    n_time_windows = 500
    temperatures = np.zeros(velocities.shape[2])


    for i in range(n_time_windows):
        temperatures[i] = np.sum(np.sum(velocities[:,:,i]**2, axis = 1))



    temperatures /= 3*4000

    # plot_velocity_distribution(velocities, vel_components = [1])

    plt.plot(range(len(temperatures)), temperatures)
    plt.show()
    # print(temperatures)



def measure_temp(data_dir):

    infile  = data_dir + "/dump.lammpstrj"
    if len(sys.argv) > 1:
        convert_dump_to_npy(data_dir, infile)


    vel_npy = data_dir + "/velocity_timeseries.npy"

    compute_temp(vel_npy)


def equipartition_theorem(Ek, N):
    return 2*Ek/(3)


def plot_system_temperature(dir):
    items = os.listdir(dir)
    log_files = []
    for name in items:
        if name[:13] == "log.boundary_":
            log_files.append(name)

    log_files = sorted(log_files)
    n_files = len(log_files)


    for file in log_files:
        with open(dir + file, "r") as infile:
            contents = infile.readlines()
            i = 0
            while i < len(contents):
                if "on 4 procs for 5000 steps with" in contents[i]:
                    words = contents[i].split(" ")
                    n_atoms = int(words[-2])
                    break
                i += 1

        log = lammps_logfile.File(dir + file)
        time = log.get("v_time")
        Ek = log.get("KinEng")
        T = log.get("Temp")
        std = np.std(T[int(1/5*len(T)):])
        plt.plot(time, T, label=rf'# of atoms: {n_atoms}. $\sigma_T = {std:.4f}$')

    plt.legend()
    plt.xlabel(r"Time $[\tau]$")
    plt.ylabel(r"Temperature $[Tk_b/\epsilon]$")
    plt.show()


    #

plot_system_temperature(dir)
