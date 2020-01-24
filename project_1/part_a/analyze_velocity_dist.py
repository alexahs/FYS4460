import numpy as np
import matplotlib.pyplot as plt
import sys, time



def convert_dump_to_npy_timeseries(input_file, outfile_prefix=""):
    n_atoms = 4000
    n_timesteps = 5000
    steps_per_window = 10
    n_time_windows = int(n_timesteps/steps_per_window)
    dims = 3
    n_info_lines = 9

    vel_timeseries = np.zeros((n_atoms, dims, n_time_windows))
    magnitude_timeseries = np.zeros((n_atoms, n_time_windows))

    for t in range(n_time_windows):
        start_read = t*(n_atoms + n_info_lines) + n_info_lines
        vel_timeseries[:,:,t] = np.loadtxt(input_file, skiprows=start_read, usecols=(1, 2, 3), max_rows=n_atoms)
        magnitude_timeseries[:, t] = np.sum(np.abs(vel_timeseries[:,:,t])**2, axis=1)**(1./2)
        print("t: ", t)


    # infile = open(input_file, 'r')
    # n_lines = 0
    # for t in range(n_time_windows):
    #     print("t: ", t)
    #     for _ in range(n_info_lines):
    #         trash = infile.readline()
    #     vel_timeseries[,:,]



    i = 0
    t = 0
    with open(input_file, 'r') as infile:
        for _ in range(n_info_lines):
            trash = infile.readline()
        line = infile.readline()

        vel_timeseries[i,:] = np.genfromtxt()




    np.save(outfile_prefix + 'magnitude_timeseries.npy', magnitude_timeseries)
    np.save(outfile_prefix + 'velocity_timeseries.npy', vel_timeseries)



def plot_hist(arr, component=2, n_bins=20):

    n_steps = arr.shape[-1]
    final_hist, _ = np.histogram(arr[:,component,-1], bins=n_bins)
    hist_series = np.zeros(arr.shape[-1])

    for t in range(n_steps):
            current_hist, _ = np.histogram(arr[:, component, t], bins=n_bins)
            hist_series[t] = np.sum(current_hist*final_hist)


    hist_series /= np.sum(final_hist**2)

    plt.plot(range(n_steps), hist_series)
    plt.show()



def main():
    try:
        convert_dump = int(sys.argv[1])
    except:
        convert_dump = None


    if convert_dump == 1:
        infile = "dump.lammpstrj"
        convert_dump_to_npy_timeseries(infile)


    vel_npy = "velocity_timeseries.npy"
    magn_npy = "magnitude_timeseries.npy"

    magnitude_timeseries = np.load(magn_npy)
    velocity_timeseries = np.load(vel_npy)

    plot_hist(velocity_timeseries)





if __name__ == '__main__':
    main()


















    #
