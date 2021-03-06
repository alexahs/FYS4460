import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as sp
from skimage import measure
from numba import jit
from tqdm import tqdm
plt.style.use('ggplot')

def analytic_2x2_P(p):
    return (2-p)*p**2



def analytic_2x2_Pi(p):
    return p**2*(p-2)**2

def spanning_cluster_density(m, single_perc = False):
    nx, ny = m.shape
    labels, n_features = sp.measurements.label(m)
    regions = measure.regionprops(labels)
    density = 0
    for region in regions:

        x_start, y_start, x_stop, y_stop = region.bbox
        dx = x_stop - x_start
        dy = y_stop - y_start

        if dx == nx or dy == ny:
            density += region.extent
            if single_perc:
                break

    return density

def plot_percolation_probability(L_arr, p_arr, n_samples):
    fig, (ax1, ax2) = plt.subplots(2)


    for L in L_arr:
        Pi_arr = np.zeros(len(p_arr))
        density_arr = np.zeros(len(p_arr))
        for p, prob in enumerate(p_arr):
            for i in range(n_samples):
                z = np.random.random((L,L))
                m = z<prob
                density = spanning_cluster_density(m)
                density_arr[p] += density
                if density > 0:
                    Pi_arr[p] += 1

        Pi_arr /= n_samples
        density_arr /= n_samples
        ax1.plot(p_arr, Pi_arr, label=f'L={L}')
        ax2.plot(p_arr, density_arr, label=f'L={L}')

    # ax1.plot(p_arr, analytic_2x2_Pi(p_arr), label='Exact')
    # ax2.plot(p_arr, analytic_2x2_P(p_arr), label='Exact')
    ax1.set_xlabel(r'Probability $p$')
    ax1.set_ylabel(r'Percolation Probability $\Pi(p, L)$')
    ax1.legend()
    ax2.set_xlabel(r'Probability $p$')
    ax2.set_ylabel(r'Spanning Cluster Density $P(p, L)$')
    # ax2.legend()
    plt.show()

# plot_percolation_probability()


def plot_P_pc_L():
    L_arr = np.array([2**i for i in range(1, 9)]).astype(int)
    pc = 0.59275
    n_samples = 1000
    density_arr = np.zeros(len(L_arr))
    for i in tqdm(range(n_samples)):
        for j, L in enumerate(L_arr):
            z = np.random.random((L,L))
            m = z<pc
            density = spanning_cluster_density(m)
            density_arr[j] += density

    density_arr /= n_samples
    np.save("exam_P_func_L.npy", np.vstack((L_arr, density_arr)))
    plt.plot(L_arr, density_arr, 'o-')
    plt.xlabel(r"$L$")
    plt.ylabel(r"$P(p_c, L)$")
    plt.show()



if __name__ == '__main__':
    plot_P_pc_L()
    # L_arr = np.array([2**i for i in range(1, 8)]).astype(int)
    # L_arr = [2]
    # p_arr = np.linspace(0.1, 0.9, 50)
    # n_samples = 1000
    # plot_percolation_probability(L_arr, p_arr, n_samples)
    # plot_spanning_cluster_density()
