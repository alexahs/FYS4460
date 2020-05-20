from load_lammps_output import *
import lammps_logfile
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


dir = get_data_path("k")


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
    plt.plot(T_fit_vals, T_fit_vals*a + b)
    plt.scatter(-b/a, 0, label=rf'Approximate melting point $T = {-b/a:.0f}K$')
    plt.scatter(T_vals, diffusion, c="g", label="Simulated results")
    plt.xlabel("T")
    plt.ylabel("D(T)")
    plt.plot([1687, 1687], [-2.5, diffusion.max()], "b--", label=r"Experimental melting point $T = 1687$K")
    # plt.plot([3538, 3538], [0, diffusion.max()], "r--", label="Experimental boiling point")
    plt.legend()
    plt.show()

    # plt.clf()












silicon_diffusion(dir)












#
