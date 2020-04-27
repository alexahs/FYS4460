import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as sp
import os
from skimage import measure
from sp_cluster_density_and_perc_prob import *
from power_law_distributions import *
from tqdm import tqdm
import time
import datetime
plt.style.use('ggplot')

ts = time.time()
ts_formatted =  datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')




def cluster_number_density(L, p, n_samples, n_bins, logbase=10, log_max=None, remove_zeros=False):
    areas = []
    for i in tqdm(range(n_samples)):
        z = np.random.random((L, L))
        m = z<p
        labels, n_features = sp.measurements.label(m)
        regions = measure.regionprops(labels)
        for region in regions:
            x_start, y_start, x_stop, y_stop = region.bbox
            dx = x_stop - x_start
            dy = y_stop - y_start
            if dx != L and dy != L:
                areas.append(region.area)

    s, N_s = log_bin(areas, n_bins=n_bins, base=logbase, log_max=log_max)
    nsp = N_s/(n_samples*L**2)
    # print("RM",remove_zeros)
    if remove_zeros:
        idx = np.where(nsp > 1e-15)[0]
        return s[idx], nsp[idx]
    else:
        return s, nsp



def plot_nsp1():
    pc = 0.59275
    p_below = np.linspace(0.4, pc, 4)
    p_above = np.linspace(0.6, 0.65, 4)
    p_vals = np.concatenate((p_below, p_above))
    print(p_vals)
    L = 200
    n_samples = 1000
    n_bins = 20
    logbase = 10

    for i, p in tqdm(enumerate(p_vals)):
        s, nsp = cluster_number_density(L, p, n_samples, n_bins, logbase)
        plt.loglog(s, nsp, label=f'p={p:.5f}')
        np.save(f"./data/nsp_varying_p/nsp_p{p:.5f}_L{L}.npy", np.vstack((s, nsp)))


    plt.xlabel(r's')
    plt.ylabel(r'n(s,p)')
    plt.legend()
    plt.show()

def plot_nsp2():
    pc = 0.59275
    L_vals = [2**k for k in range(4, 10)]
    n_samples = 1000
    n_bins = 20
    logbase = 10
    for i, L in tqdm(enumerate(L_vals)):
        s, nsp = cluster_number_density(L, pc, n_samples, n_bins, logbase)
        np.save(f"./data/nsp_varying_L/nsp_p{pc:.5f}_L{L}.npy", np.vstack((s, nsp)))
        plt.loglog(s, nsp, label=f'L={L}')
        if L == L_vals[-1]:
            tau, _ = np.polyfit(np.log(s), np.log(nsp), deg=1)
            plt.loglog(s, s**tau, 'k--', label=r'Fit of $n(s,p)\propto s^{%.3f}$' %tau)
            tau *= -1
            print(f"tau={tau}")

    plt.xlabel(r's')
    plt.ylabel(r'n(s,p)')
    plt.legend()
    plt.show()

def run_nsp_vs_s(L, n_samples, n_bins):
    pc = 0.59275
    eps = 1e-14
    # p_vals = [0.45, 0.50, 0.54, 0.57, 0.58]
    p_vals = [0.45, 0.50, 0.54, 0.57, 0.58]
    # L = 2**6
    # n_samples = 1000
    # n_bins = 40
    logbase = 1.3
    remove_zeros = False
    s, nc = cluster_number_density(L, pc, n_samples, n_bins, logbase, remove_zeros=remove_zeros)
    log_max = np.log(s[-1])/np.log(logbase)
    nonzero = np.where(nc > eps)[0]
    dirID = f"run_bins{n_bins}_L{L}_samples{n_samples}_{ts_formatted}"
    os.mkdir(f"./data/s_xi/{dirID}")
    plt.loglog(s[nonzero], nc[nonzero], label=f'p={pc:.5f}')
    np.save(f"./data/s_xi/{dirID}/nsp_vs_alls_p{pc:.5f}_L{L}.npy", np.vstack((s[nonzero], nc[nonzero])))
    sxi_vals = []
    F_vals = []
    p_array = []
    # print("S1", s)
    for i, p in tqdm(enumerate(p_vals)):
        s, n = cluster_number_density(L, p, n_samples, n_bins, logbase, log_max, remove_zeros)
        nonzero = np.where(n > eps)[0]
        plt.loglog(s[nonzero], n[nonzero], label=f"p={p}")
        np.save(f"./data/s_xi/{dirID}/nsp_vs_alls_p{p:.5f}_L{L}.npy", np.vstack((s[nonzero], n[nonzero])))

        temp_sxi = []
        temp_n = []
        for i in range(len(n)):
            if n[i] > eps and nc[i] > eps:
                if n[i]/nc[i] <= 0.5:
                    temp_sxi.append(s[i])
                    temp_n.append(n[i])


        if len(temp_n)> 0:
            idx = np.argmax(temp_n)
            F = temp_n[idx]
            sxi = temp_sxi[idx]
            sxi_vals.append(sxi)
            F_vals.append(F)
            p_array.append(p)
            plt.loglog(sxi, F, 'ko')

    np.save(f"./data/s_xi/{dirID}/nsp_vs_sxi_L{L}_nsamp{n_samples}.npy", np.vstack((sxi_vals, F_vals)))
    np.save(f"./data/s_xi/{dirID}/sxi_vs_p_L{L}_nsamp{n_samples}.npy", np.vstack((p_array, sxi_vals)))
    plt.legend()
    plt.xlabel(r'$s$')
    plt.ylabel(r'$n(s,p)$')
    plt.show()
    plt.clf()
    plt.plot(p_array, sxi_vals, "-o")
    plt.xlabel(r"$p$")
    plt.ylabel(r"$s_\xi$")
    plt.xlim(0.4, 0.7)
    plt.show()

def load_and_plot_sxi(L, n_samples):
    pc = 0.59275
    data_dir = "./data/s_xi/"
    run_dirs = os.listdir(data_dir)
    # L = 128
    # nsamp = 500
    fileno = 0
    run_dir = [d for d in run_dirs if str(L) in d and str(n_samples) in d][fileno]
    files = os.listdir(data_dir + run_dir)
    nsp_vs_s_files = [file for file in files if "nsp_vs_alls" in file]
    nsp_vs_sxi_file = [file for file in files if "nsp_vs_sxi" in file][0]
    sxi_vs_p_file = [file for file in files if "sxi_vs_p" in file][0]
    # print(nsp_vs_s)
    # print(nsp_vs_sxi)
    # print(sxi_vs_p)
    os.chdir(data_dir + run_dir)
    for filename in nsp_vs_s_files:
        data = np.load(filename)
        p_start = filename.index("p0") + 1
        p_stop = filename.index("_L")
        p = float(filename[p_start:p_stop])
        plt.loglog(data[0], data[1], label=f"p={p}")


    nsp_vs_sxi = np.load(nsp_vs_sxi_file)
    sxi_vs_p = np.load(sxi_vs_p_file)

    print(sxi_vs_p)

    a, b = np.polyfit(np.log10(sxi_vs_p[1]), np.log10(np.abs(sxi_vs_p[1]-pc)), deg=1)

    sigma = -1/a
    print(f"Sigma = {sigma}")
    # plt.plot(np.log10(nsp_vs_sxi[0]), np.log10(np.abs(sxi_vs_p[0]-pc)**a))

    plt.loglog(nsp_vs_sxi[0], nsp_vs_sxi[1], 'ko', label=r"$F(s/s_{xi}) = 0.5$")
    plt.legend()
    plt.show()
    plt.clf()

    plt.plot(sxi_vs_p[0], sxi_vs_p[1], '-o')
    plt.show()



L = 2**9
n_samples = 1000
n_bins = 30

# plot_nsp3()
# run_nsp_vs_s(L=L, n_samples=n_samples, n_bins=n_bins)
load_and_plot_sxi(L=L, n_samples=n_samples)






# plot_nsp2()


# cluster_number_density(50, 0.55, 100)

# plot_nsp1()
