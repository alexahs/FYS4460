import numpy as np
import matplotlib.pyplot as plt
from .load_lammps_output import *


def plot_temp_press(dir):

    temp_press = read_thermo_log(dir=dir, filename = "log.lammps", names_of_measurements = "Temp Press")

    print(temp_press)

    idx = np.argsort(temp_press[:,0])

    temp = temp_press[:,0][idx]
    press = temp_press[:,1][idx]


    plt.plot(temp, press)
    plt.show()
