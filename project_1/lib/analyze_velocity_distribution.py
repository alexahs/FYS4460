import numpy as np
import matplotlib.pyplot as plt
import sys, time




def convert_dump_to_npy_timeseries(data_dir, input_file, outfile_prefix="", n_atoms = 4000, n_timesteps = 5000, steps_per_window = 10):

    n_time_windows = int(n_timesteps/steps_per_window)
    dims = 3
    n_info_lines = 9

    vel_timeseries = np.zeros((n_atoms, dims, n_time_windows))
    magnitude_timeseries = np.zeros((n_atoms, n_time_windows))


    infile = open(input_file, 'r')

    for t in range(n_time_windows):
        print('t: ', t)
        for _ in range(n_info_lines):
            trash = infile.readline()

        for i in range(n_atoms):
            vel_timeseries[i,:,t] = np.fromstring(infile.readline()[1:], dtype='float', count=3, sep=' ')


    np.save(data_dir + outfile_prefix + 'magnitude_timeseries.npy', magnitude_timeseries)
    np.save(data_dir + outfile_prefix + 'velocity_timeseries.npy', vel_timeseries)



def plot_hist(arr, component=1, n_bins=20):

    n_steps = arr.shape[-1]
    final_hist, _ = np.histogram(arr[:,component,-1], bins=n_bins)
    hist_series = np.zeros(arr.shape[-1])

    for t in range(n_steps):
            current_hist, _ = np.histogram(arr[:, component, t], bins=n_bins)
            hist_series[t] = np.sum(current_hist*final_hist)


    hist_series /= np.sum(final_hist**2)

    plt.plot(range(n_steps), hist_series)
    plt.show()



def analyze_velocity_distribution(data_dir):
    try:
        convert_dump = int(sys.argv[1])
    except:
        convert_dump = None



    if convert_dump == 1:
        infile = data_dir + "/dump.lammpstrj"
        convert_dump_to_npy_timeseries(data_dir, infile)


    vel_npy = data_dir + "/velocity_timeseries.npy"
    magn_npy = data_dir + "/magnitude_timeseries.npy"

    magnitude_timeseries = np.load(magn_npy)
    velocity_timeseries = np.load(vel_npy)

    plot_hist(velocity_timeseries)





# if __name__ == '__main__':
    # analyze_velocity_distribution()
