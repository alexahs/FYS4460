import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import measurements
import scipy.ndimage as sp
from pylab import *
plt.style.use('ggplot')

def perc_demo():
    pVals = np.linspace(0.1, 0.9, 9)
    L = 4
    z = np.random.random((L, L))

    fig, ax = plt.subplots()
    ax.matshow(z, cmap='binary')
    for (i, j), Z in np.ndenumerate(z):
        ax.text(j, i, '{:0.2f}'.format(Z), ha='center', va='center',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
    plt.show()
    plt.clf()

    fig, axs = plt.subplots(3, 3)
    pIdx = 0
    for i in range(3):
        for j in range(3):
            p = pVals[pIdx]
            system = z < p
            pIdx += 1
            axs[i, j].imshow(system, cmap='binary')
            axs[i, j].set_xticks([])
            axs[i, j].set_yticks([])
            axs[i, j].set_title(f"p={p:0.1f}")

    plt.show()

# perc_demo()





def visualize_clusters():
    L = 10
    p = 0.5
    z = rand(L,L)
    system = z<p
    labels, n_features = measurements.label(system)
    # b = arange(labels.max() + 1)
    # shuffle(b)
    # shuffledLabels = b[labels]
    # cmap = plt.cm.viridis
    # cmap.set_under('w')
    area = measurements.sum(system, labels, index=arange(labels.max() + 1))
    areaImg = area[labels]
    cmap = plt.cm.viridis
    cmap.set_under('black')
    imshow(areaImg, origin='lower', cmap=cmap, vmin=0.1, interpolation='none')
    colorbar()
    show()


# visualize_clusters()


def visualize_clusters2():
    pVals = [0.57, 0.58, 0.59, 0.6]
    L = 100
    z = np.random.random((L, L))

    fig, axs = plt.subplots(2, 2)
    cmap = plt.cm.viridis
    cmap.set_under('black')
    idx = 0
    for i in range(2):
        for j in range(2):
            p = pVals[idx]
            print(p)
            system = z < p
            labels, n_features = measurements.label(system)
            area = measurements.sum(system, labels, index=arange(labels.max() + 1))
            areaImg = area[labels]
            axs[i, j].imshow(areaImg, origin='lower', cmap=cmap, vmin=0.1, interpolation='none')
            axs[i, j].set_xticks([])
            axs[i, j].set_yticks([])
            axs[i, j].set_title(f"p={p:0.2f}")
            idx += 1

    # colorbar()
    show()

# visualize_clusters2()




def G_nsp_1d(s, p):
    return p**s

def s_xi(p):
    return -1/np.log(p)


def plot_nsp1d():
    s = np.logspace(0, 6, 100)
    pVals = [0.9, 0.99, 0.999]
    fig, axs = plt.subplots(2)
    linestyles = ['.', '--', '-.']
    i = 0
    for p in pVals:
        axs[0].loglog(s, G_nsp_1d(s, p), linestyles[i] ,label=f'p={p}')
        axs[1].loglog(s/s_xi(p), G_nsp_1d(s, p), linestyles[i] ,label=f'p={p}')
        i += 1


    axs[0].legend()
    axs[0].set_xlabel(r'$s$')
    axs[0].set_ylabel(r'$n(s,p)(1-p)^{-2}$')
    axs[1].set_xlabel(r'$s/s_\xi$')
    axs[1].set_ylabel(r'$n(s,p)(1-p)^{-2}$')
    plt.show()

plot_nsp1d()



















#
