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


data_dir = './data/percolation_threshold/'




def perc_prob(n_samples = None, save_data = False):
    L_vals = [25,50,100,200,400,800]
    p_vals = np.linspace(0.5, 0.7, 50)

    prob = np.zeros((len(L_vals), len(p_vals)))

    for i, L in tqdm(enumerate(L_vals)):
        if n_samples is None:
            n_samples = int(500*25/L)
        for j, p in tqdm(enumerate(p_vals)):
            for k in range(n_samples):
                m = np.random.random((L, L)) < p
                density = spanning_cluster_density(m, single_perc = True)
                if density > 0:
                    prob[i, j] += 1
        prob[i,:] /= n_samples

    if save_data:
        np.save(data_dir + 'perc_prob_nsamples' + str(n_samples) + '.npy', prob)
        np.save(data_dir + 'p_vals.npy', p_vals)
        np.save(data_dir + 'L_vals.npy', L_vals)
    return prob


def plot_Pi():
    n_samples = 500
    L_vals = np.load(data_dir + 'L_vals.npy')
    p_vals = np.load(data_dir + 'p_vals.npy')
    filename = data_dir + 'perc_prob_nsamples' + str(n_samples) + '.npy'
    data = np.load(filename)
    for i, L in enumerate(L_vals):
        Pi_vals = data[i]
        plt.plot(p_vals, Pi_vals, label=f"L={L}")

    plt.xlabel(r"$p$")
    plt.ylabel(r"$\Pi(p,L)$")
    plt.plot((0.5,0.7), (0.3,0.3), 'k--')
    plt.plot((0.5,0.7), (0.8,0.8), 'k--')
    plt.legend()
    plt.show()





def Pi_inverse(plotting = False):
    n_samples = 500
    L_vals = np.load(data_dir + 'L_vals.npy')
    p = np.load(data_dir + 'p_vals.npy')
    filename = data_dir + 'perc_prob_nsamples' + str(n_samples) + '.npy'
    data = np.load(filename)
    x_vals = [0.3, 0.8]
    p_pi_vals = np.zeros((len(x_vals), len(L_vals)))

    for j, x in enumerate(x_vals):
        for i, L in enumerate(L_vals):
            Pi = data[i,:]
            idx = np.argmax(Pi > x)
            pc = p[idx-1] + (x-Pi[idx-1])*(p[idx] - p[idx-1])/(Pi[idx] - Pi[idx-1])
            p_pi_vals[j,i] = pc

        if plotting:
            plt.plot(L_vals, p_pi_vals[j,:], 'o-', label=rf"$x={x}$")

    if plotting:
        plt.xlabel(r"$L$")
        plt.ylabel(r"$p_{\Pi_x}(L)$")
        plt.legend()
        plt.show()

    a, b = np.polyfit(np.log10(L_vals), np.log10(p_pi_vals[1,:] - p_pi_vals[0,:]), deg=1)
    nu = -1/a
    print(f"Nu = {nu}")
    return p_pi_vals


# prob = perc_prob(save_data = True)
# plot_Pi()
# Pi_inverse()

def compute_pc():
    nu = 4/3
    n_samples = 500
    L_vals = np.load(data_dir + 'L_vals.npy')
    p = np.load(data_dir + 'p_vals.npy')
    filename = data_dir + 'perc_prob_nsamples' + str(n_samples) + '.npy'
    data = np.load(filename)
    x_vals = [0.3, 0.8]
    p_pi_vals = Pi_inverse()
    coeffs = np.zeros((len(x_vals), 2))

    colors = ['blue', 'red']

    for i, x in enumerate(x_vals):
        L_nu = L_vals**(-1/nu)
        Cx, pc = np.polyfit(L_nu, p_pi_vals[i, :], deg=1) #[nx, nL]
        plt.plot(L_nu, p_pi_vals[i, :], marker='o', color=colors[i], label=rf'$x={x}$, estimated $p_c={pc:.4f}$')
        # coeffs[i, :] = Cx, pc
        plt.plot(L_nu, pc + Cx*L_nu, ls='--', color='dimgray')



    plt.xlabel(r"$L^{-1/\nu}$")
    plt.ylabel(r"$p_{\Pi_x}$")
    plt.legend()
    plt.show()

compute_pc()













#
