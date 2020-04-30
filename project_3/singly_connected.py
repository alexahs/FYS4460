import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as sp
import os
from skimage import measure
from sp_cluster_density_and_perc_prob import *
from power_law_distributions import *
from tqdm import tqdm
from walk import walk
plt.style.use('ggplot')

# L = 100
# pc = 0.59275

def generate_percolating_cluster(L, p):

    perc = []
    iter = 0

    while (len(perc) == 0):

        iter += 1
        if iter > 100:
            print("Couldn't make percolating cluster")
            exit()

        z = np.random.random((L,L))
        m = z <=p

        labels, n_features = sp.measurements.label(m)

        perc_x = np.intersect1d(labels[0,:], labels[-1,:])
        perc = perc_x[np.where(perc_x > 0)]

    perc_cluster = (labels == perc[0])


    return perc_cluster

def plot_geometry(perc):

    left, right = walk(perc)
    singly_connected = left*right
    backbone = left + right

    plt.figure()
    plt.imshow(perc)

    plt.figure()
    plt.imshow(singly_connected)

    plt.figure()
    plt.imshow(backbone)

    plt.figure()
    plt.imshow(right)

    plt.figure()
    plt.imshow(left)

    plt.show()

# perc = generate_percolating_cluster(L, pc)
# plot_geometry(perc)
# print(perc)



def estimate_Dsc(produce_data = False):

    pc = 0.59275
    nsamp = 100
    if produce_data:
        L_vals = [2**k for k in range(4, 11)]
        M_vals = np.zeros(len(L_vals))

        for i, L in tqdm(enumerate(L_vals)):
            for n in tqdm(range(nsamp)):
                perc = generate_percolating_cluster(L, pc)
                left, right = walk(perc)
                bonds = np.array(left*right, dtype=bool)
                M_cs = np.sum(bonds)
                M_vals[i] += M_cs
        M_vals /= nsamp
        np.save("data/singly_connected/M_SC.npy", np.vstack((L_vals, M_vals)))

    else:
        data = np.load("data/singly_connected/M_SC.npy")
        L_vals = data[0]
        M_vals = data[1]


    a, b = np.polyfit(np.log10(L_vals),np.log10(M_vals), deg=1)

    print(f"D_CS = {a}")

    plt.loglog(L_vals, M_vals, 'ro', label='data')
    plt.loglog(L_vals, 10**b*L_vals**a, 'b--', label=r'fit of $M_{SC} \propto L^{%.4f}$' %a)
    plt.xlabel(r"$L$")
    plt.ylabel(r"$M_{SC}$")
    plt.legend()
    plt.show()


def P_sc(produce_data = False):
    pc = 0.59275
    nsamp = 100
    p_vals = np.linspace(pc, 0.7, 10)
    pmpc = abs(p_vals - pc)
    L_vals = [2**k for k in range(6, 10)]
    if produce_data:
        P_vals = np.zeros((len(p_vals), len(L_vals)))

        for i, p in tqdm(enumerate(p_vals)):
            for j, L in enumerate(L_vals):
                M_sc = 0
                for k in range(nsamp):
                    perc = generate_percolating_cluster(L, p)
                    left, right = walk(perc)
                    bonds = np.array(left*right, dtype=bool)
                    M_sc += np.sum(bonds)
                P_vals[i, j] = M_sc / nsamp / L**2

        np.save("data/singly_connected/P_SC.npy", P_vals)
    else:
        P_vals = np.load("data/singly_connected/P_SC.npy")

    for i, L in enumerate(L_vals):
        plt.plot(pmpc, P_vals[:,i], label=f"L={L}")
    plt.xlabel(r"$p-p_c$")
    plt.ylabel(r"$P_{SC}$")
    plt.legend()
    plt.show()

    print(np.log10(P_vals[:,-1]))
    print(pmpc)
    print(np.log10(pmpc))

    a, b = np.polyfit(np.log10(pmpc[1:]), np.log10(P_vals[1:,-1]), deg=1)
    print(f"Exponent x={a}")
    plt.plot(np.log10(pmpc), np.log10(P_vals[:,-1]), 'ro', label='data')
    plt.plot(np.log10(pmpc), np.log10(10**b*pmpc**a), 'b--', label=r'fit of $P_{SC} \propto |p-p_c|^{%.4f}$' %a)
    plt.xlabel(r"$\log_{10}(p-p_c)$")
    plt.ylabel(r"$\log_{10}(P_{SC})$")
    plt.legend()
    plt.show()



P_sc(False)



# estimate_Dsc()







#
