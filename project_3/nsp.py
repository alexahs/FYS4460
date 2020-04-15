import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as sp
from skimage import measure
from sp_cluster_density_and_perc_prob import *
from power_law_distributions import *
from tqdm import tqdm
plt.style.use('ggplot')




def cluster_number_density(L, p, n_samples, n_bins, logbase=10):
    areas = []
    for i in range(n_samples):
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

    s, N_s = log_bin(areas, n_bins=n_bins)
    nsp = N_s/(n_samples*L**2)
    idx = np.where(nsp > 1e-15)[0]
    return s[idx], nsp[idx]


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

plot_nsp2()


# cluster_number_density(50, 0.55, 100)

# plot_nsp1()
