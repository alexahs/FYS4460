from load_lammps_output import *
import lammps_logfile
import numpy as np
import matplotlib.pyplot as plt
import natsort
plt.style.use('ggplot')


dir = get_data_path("l")


def silicon_diffusion(dir):


    files_dir = os.listdir(dir)

    log_files = []
    for file in files_dir:
        if "log.T" in file:
            log_files.append(file)

    log_files = np.sort(log_files)
    # data_dict = {}
    # avg_temps = []
    msd_vals = []
    T_vals = []
    for file in log_files:
        log = lammps_logfile.File(os.path.join(dir, file))

        T = log.get("Temp")
        # size = T_temp.shape[0]
        # size_2 = size//2
        # T = T_temp[size_2:]
        t = log.get("Time")#[size_2:]
        msd = log.get("c_msd[4]")#[size_2:]



        #
        avg_temp = int(np.mean(T[int(len(T)/4):]))
        # avg_temps.append(avg_temp)
        # data_dict["T_" + str(avg_temp)] = T
        # data_dict["msd_" + str(avg_temp)] = msd

        msd_vals.append(msd)
        T_vals.append(T[0])

        # plt.plot(t, msd, label=f'T={avg_temp}')

    n_files = len(log_files)

    for i in range(n_files):
        plt.plot(t, msd_vals[i], label=f'T={T_vals[i]}')
    plt.legend()
    plt.xlabel(r"$t$")
    plt.ylabel(r"$\langle r^2(t) \rangle$")
    plt.show()
    plt.clf()


    diffusion = np.zeros(n_files)

    # plt.plot()

    #
    idx1 = int(len(t)/2)
    idx2 = int(len(t)/10)
    for i in range(n_files):
        # diffusion[i] = np.polyfit(t[:-5], data_dict["msd_" + str(avg_temps[i])][:-5], deg=1)[0]/6
        # diffusion[i] = np.polyfit(t[:-idx], msd_vals[i][:-idx], deg=1)[0] / 6
        diffusion[i] = np.polyfit(t[-idx1:-idx2], msd_vals[i][-idx1:-idx2], deg=1)[0] / 6
    #
    a, b = np.polyfit(T_vals, diffusion, deg=1)
    T_fit_vals = np.linspace(0, 8000, len(T_vals))
    # plt.plot(T_vals, np.linspace(0, T_vals[-1], len(T_vals))*a + b, label='Line fit')
    # plt.plot(T_fit_vals, T_fit_vals*a + b)
    # plt.scatter(-b/a, 0, label=rf'Approximate melting point $T = {-b/a:.0f}K$')
    plt.scatter(T_vals, diffusion, c="g")#, label="Simulated results")
    plt.xlabel("T")
    plt.ylabel("D(T)")
    # plt.plot([1687, 1687], [-2.5, diffusion.max()], "b--", label=r"Experimental melting point $T = 1687$K")
    # plt.plot([3538, 3538], [0, diffusion.max()], "r--", label="Experimental boiling point")
    plt.legend()
    plt.show()

    # plt.clf()



# silicon_diffusion(dir + "/run3")


def read_rdf_dump(dir, filename,
                  n_time_steps = 4000,
                  step_window = 10,
                  n_bins = 50,
                  n_info_lines = 3):
    """
    Function for reading radial distribution g(r) values produced by
    <<compute myRDF all rdf 50>>
    <<fix 2 all ave/time 100 1 100 c_myRDF[*] file tmp.rdf mode vector>>
    commands in lammps.

    Returns: array of radial distances and avg g(r)
    """
    params = get_dump_params(dir)
    n_time_windows = params['TIME_STEPS']
    step_window = params['THERMO_STEP']
    # n_time_windows = int(n_time_steps/step_window) +1

    radials = np.zeros((n_bins, n_time_windows))
    bin_distances = np.zeros(n_bins)



    with open(dir + filename, 'r') as infile:
        for skip in range(n_info_lines+1):
            skipline = infile.readline()

        #get bin distances and g(r) in first time window
        for i in range(n_bins):
            linestr = np.fromstring(infile.readline(),
                                           dtype='float',
                                           count=3,
                                           sep=' ')

            bin_distances[i] = float(linestr[1])
            radials[i, 0] = float(linestr[2])


        #get g(r) for remaining time windows
        for t in range(1, n_time_windows):
            skipline = infile.readline()

            for i in range(n_bins):
                radials[i, t] = np.fromstring(infile.readline(),
                                               dtype='float',
                                               count=3,
                                               sep=' ')[2]

        infile.close()
    #end readfile



    avg_radials = np.mean(radials, axis=1)

    return bin_distances, avg_radials




def plot_radial_distribution(dir,
                             n_time_steps = 4000,
                             step_window = 50,
                             n_bins = 50,
                             n_info_lines = 3):

    dir_files = os.listdir(dir)
    log_files = []

    for file in dir_files:
        if file[:7] == "log.rdf":
            log_files.append(file)


    # log_files = np.sort(log_files)
    log_files = natsort.natsorted(log_files)

    print(log_files)

    # T_init_vals = list(range(20, 300, 20))

    for i, file in enumerate(log_files):
        # T_init = float(file[10:])
        T = int(file[10:])
        # T = T_init_vals[i]
        log = lammps_logfile.File(dir + f"log.rdf_T_{T}")
        # T = log.get("Temp")
        # idx = len(T) / 2
        bins, radials = read_rdf_dump(dir, file)
        # T_mean = np.mean(T)
        plt.plot(bins, radials/radials[-1], label=f"T={T:d}")

    plt.legend(loc=1)
    plt.xlabel(r"$r$")
    plt.ylabel(r"$g(r)$")
    plt.show()


plot_radial_distribution(dir + "radial_data/")




















#
