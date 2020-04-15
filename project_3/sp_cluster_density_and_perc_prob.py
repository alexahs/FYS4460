import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as sp
from skimage import measure
plt.style.use('ggplot')


def spanning_cluster_density(m):
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

    ax1.set_xlabel(r'Probability $p$')
    ax1.set_ylabel(r'Percolation Probability $\Pi(p, L)$')
    ax1.legend()
    ax2.set_xlabel(r'Probability $p$')
    ax2.set_ylabel(r'Spanning Cluster Density $P(p, L)$')
    # ax2.legend()
    plt.show()


# if __name__ == '__main__':
#
#     L_arr = np.array([2**i for i in range(1, 8)]).astype(int)
#     p_arr = np.linspace(0.1, 0.9, 100)
#     n_samples = 1000
#     plot_percolation_probability(L_arr, p_arr, n_samples)
#     # plot_spanning_cluster_density()
