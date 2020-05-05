import matplotlib.pyplot as plt
import numpy as np
from .load_lammps_output import *


def berendsen(dir, filename):

    n_time_steps = 50000
    step_window = 100

    data = read_thermo(dir, filename, 'Temp',
                       n_time_steps=n_time_steps,
                       step_window=step_window)
    #
    time = np.linspace(0, n_time_steps*0.005, data.shape[0])

    plt.plot(time, data[:,0])
    plt.xlabel(r"Time $[\tau]$")
    plt.ylabel(r"Temperature $[\epsilon/k_B]$")
    plt.title("Berensen thermostat")
    plt.show()


    return 1
