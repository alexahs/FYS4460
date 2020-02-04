import numpy as np
import matplotlib.pyplot as plt
from .load_lammps_output import *




def plot_velocity_distribution(arr, vel_component = 1, n_bins = 20):

    n_steps = arr.shape[-1]
    final_hist, _ = np.histogram(arr[:,vel_component,-1], bins=n_bins)
    hist_series = np.zeros(arr.shape[-1])


    for t in range(n_steps):
        current_hist, _ = np.histogram(arr[:, vel_component, t], bins=n_bins)
        hist_series[t] = np.sum(current_hist*final_hist)


    hist_series /= np.sum(final_hist**2)

    plt.plot(range(n_steps), hist_series)
    # plt.xlabel()
    plt.ylabel(r"Normalized inner product of $h_i(t)$")
    plt.show()



# if __name__ == '__main__':
    # analyze_velocity_distribution()
