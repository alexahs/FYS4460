import numpy as np
import matplotlib.pyplot as plt
from .load_lammps_output import *


def plot_pressure(temp_pressure):


    # print(temp_press)

    idx = np.argsort(temp_pressure[:,0])

    temp = temp_pressure[:,0][idx]
    press = temp_pressure[:,1][idx]


    plt.plot(temp, press)
    plt.show()
