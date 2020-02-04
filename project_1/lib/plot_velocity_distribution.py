import numpy as np
import matplotlib.pyplot as plt
from .load_lammps_output import *




def plot_velocity_distribution(velocities, vel_components = [0, 1, 2], n_bins = 20):

    n_steps = velocities.shape[-1]
    labels = [r"$v_x$", r"$v_y$", r"$v_z$"]

    print(n_steps)

    for i in vel_components:
        final_hist, _ = np.histogram(velocities[:,i,-1], bins=n_bins)
        hist_series = np.zeros(velocities.shape[-1])
        for t in range(n_steps):
            current_hist, _ = np.histogram(velocities[:, i, t], bins=n_bins)
            hist_series[t] = np.sum(current_hist*final_hist)

        hist_series /= np.sum(final_hist**2)
        plt.plot(range(n_steps), hist_series, label=labels[i])


    plt.legend()
    plt.xlabel(r"$t_i$")
    plt.ylabel(r"Normalized inner product of $h_i(t)$")
    plt.show()



# if __name__ == '__main__':
    # analyze_velocity_distribution()
