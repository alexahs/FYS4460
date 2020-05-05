import numpy as np
import matplotlib.pyplot as plt
from load_lammps_output import *
import lammps_logfile
plt.style.use('ggplot')

dir = get_data_path("a")
dumpfile = 'dump.lammpstrj'
# velocities = read_dump(dir, dumpfile, save_to_npy=True)
npyfile = 'dump_x_y_z_vx_vy_vz.npy'

velocities = np.load(dir + npyfile)[:,3:,:] #[n_atoms, n_observables, n_time_windows]


def plot_velocity_time_development(velocities, vel_components = [0, 1, 2], n_bins = 20):

    n_steps = velocities.shape[-1]
    labels = [r"$v_x$", r"$v_y$", r"$v_z$"]

    dump_step = 10

    for i in vel_components:
        final_hist, _ = np.histogram(velocities[:,i,-1], bins=n_bins)
        hist_series = np.zeros(velocities.shape[-1])
        for t in range(n_steps):
            current_hist, _ = np.histogram(velocities[:, i, t], bins=n_bins)
            hist_series[t] = np.sum(current_hist*final_hist)

        hist_series /= np.sum(final_hist**2)
        plt.plot(range(0, n_steps*dump_step, dump_step), hist_series, label=labels[i])


    plt.legend()
    plt.xlabel(r"$t_i$")
    plt.ylabel(r"Normalized inner product of $h_i(t)$")
    plt.show()


def plot_init_and_last_velocity(vel, n_bins=20):
    fig, axs = plt.subplots(2, 3, sharey=True)
    plt.rcParams["patch.force_edgecolor"] = True
    components = [r"$v_x$", r"$v_y$", r"$v_z$"]
    magnitude_init = np.sqrt(np.sum(vel[:,:,0]**2, axis=1))
    for i in range(3):
        vel_component = vel[:,i,0]
        axs[0, i].hist(vel_component, bins=n_bins, alpha=0.7, facecolor='green', density=1)
        # axs[0, i].set_xlabel(components[i])

    for i in range(3):
        vel_component = vel[:,i,-1]
        axs[1, i].hist(vel_component, bins=n_bins, alpha=0.7, facecolor='green', density=1)
        axs[1, i].set_xlabel(components[i])

    axs[1, 0].set_ylabel("Distribution density")
    plt.show()



plot_init_and_last_velocity(velocities)

plot_velocity_time_development(velocities)












#
