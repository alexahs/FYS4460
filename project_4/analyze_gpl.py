import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy.ndimage import measurements
from matplotlib.colors import ListedColormap
from flow_in_perc import *
from tqdm import tqdm
import os

def compute_gpl(Lvals, pVals, nSamples, datadir_suffix):
    # Lvals = [25,50,100,200,400]
    # pVals = logspace(log10(0.58), log10(0.85), 20)
    C = zeros((len(pVals),len(Lvals)),float)
    # mu = zeros(len(Lvals))
    for iL in tqdm(range(len(Lvals))):
        L = Lvals[iL]
        lx = L
        ly = L
        for pIndex in tqdm(range(len(pVals))):
            p = pVals[pIndex]
            ncount = 0
            for j in range(nSamples):
                ncount = 0
                perc = []
                while (len(perc)==0):
                    ncount = ncount + 1
                    if (ncount > 1000):
                        print("Couldn’t make percolation cluster...")
                        break
                    z=rand(L,L)<p
                    lw,num = measurements.label(z)
                    perc_x = intersect1d(lw[0,:],lw[-1,:])
                    perc = perc_x[where(perc_x > 0)]
                if len(perc) > 0:
                    zz = asarray((lw == perc[0]))
                    # zz now contains the spanning cluster
                    zzz = zz.T
                    #
                    # Generate bond lattice from this
                    g = sitetobond ( zzz )
                    #
                    # Generate conductivity matrix
                    Pvec, c_eff = FIND_COND(g, lx, ly)
                    C[pIndex,iL] = C[pIndex,iL] + c_eff
            C[pIndex,iL] = C[pIndex,iL]/nSamples

    dir = "data/"
    newdir = dir + f"run_{datadir_suffix}/"
    os.mkdir(newdir)
    filename_gpl = f"gpl_{nSamples}_samples_dims_pxL.npy"
    filename_pvals = f"pvals_{nSamples}_samples.npy"
    filename_Lvals = f"Lvals_{nSamples}_samples.npy"
    np.save(newdir + filename_gpl, C)
    np.save(newdir + filename_pvals, pVals)
    np.save(newdir + filename_Lvals, Lvals)

    return C

pc = 0.59275
nSamples = 100
Lvals = [25,50,100,200,400]
# pVals = logspace(log10(0.58), log10(0.85), 20)
pVals = [pc]
nu_exact = 4/3
mu_approx = 1.258

print("zeta_r=", mu_approx/nu_exact)

# compute_gpl(Lvals, pVals, nSamples, 'gpcl')


def plot_gpl():
    datadir_suffix = 'gpl'
    dir = 'data/' + f'run_{datadir_suffix}/'
    filename_gpl = f"gpl_{nSamples}_samples_dims_pxL.npy"
    filename_pvals = f"pvals_{nSamples}_samples.npy"
    filename_Lvals = f"Lvals_{nSamples}_samples.npy"
    gpl = np.load(dir + filename_gpl)
    pvals = np.load(dir + filename_pvals)
    Lvals = np.load(dir + filename_Lvals)

    for i, L in enumerate(Lvals):
        plt.plot(pvals, gpl[:, i], label=f'L={L}')

    plt.xlabel(r'$p$')
    plt.ylabel(r'$g(p, L)$')
    plt.legend()
    plt.show()

# plot_gpl()

def logplot_gpcl():
    datadir_suffix = 'gpcl'
    dir = 'data/' + f'run_{datadir_suffix}/'
    filename_gpl = f"gpl_{nSamples}_samples_dims_pxL.npy"
    filename_pvals = f"pvals_{nSamples}_samples.npy"
    filename_Lvals = f"Lvals_{nSamples}_samples.npy"
    gpl = np.load(dir + filename_gpl)
    pvals = np.load(dir + filename_pvals)
    Lvals = np.load(dir + filename_Lvals)

    plt.plot(np.log10(Lvals), np.log10(gpl[0,:]), 'b--')
    plt.scatter(np.log10(Lvals), np.log10(gpl[0,:]), c='red')
    plt.xlabel(r"$\log_{10}L$")
    plt.ylabel(r"$\log_{10}g(p_c, L)$")
    plt.show()


# logplot_gpcl()

def logplot_gpl_vs_pmpc():
    datadir_suffix = 'gpl'
    dir = 'data/' + f'run_{datadir_suffix}/'
    filename_gpl = f"gpl_{nSamples}_samples_dims_pxL.npy"
    filename_pvals = f"pvals_{nSamples}_samples.npy"
    filename_Lvals = f"Lvals_{nSamples}_samples.npy"
    gpl = np.load(dir + filename_gpl)
    pvals = np.load(dir + filename_pvals)
    Lvals = np.load(dir + filename_Lvals)
    mu_list = []
    for i, L in enumerate(Lvals):
        log_gpl = np.log10(gpl[2:, i])
        log_pmpc = np.log10(pvals[2:]-pc)
        a, b = np.polyfit(log_pmpc[6:], log_gpl[6:], deg=1)
        mu_list.append(a)
        plt.scatter(log_pmpc, log_gpl, label=rf'$L={L}, \mu=%.2f$' %a)


    plt.xlabel(r'$\log_{10}p$')
    plt.ylabel(r'$\log_{10}g(p, L)$')
    plt.legend()
    plt.show()

    plt.clf()
    mu_exact = 1.3
    # for i, L in enumerate(Lvals):
    plt.plot(Lvals, mu_list, 'b--')
    plt.plot((25, 400), (mu_exact, mu_exact), 'k--', label=rf'Exact value $\mu = {mu_exact}$')
    plt.scatter(Lvals, mu_list, c='red', label=r'Estimated values $\mu$')

    print(f"mu={np.mean(mu_list)}")
    plt.xlabel(r"$L$")
    plt.ylabel(r"$\mu$")
    plt.legend()
    plt.show()



# logplot_gpl_vs_pmpc()

def plot_datacollapse():
    datadir_suffix = 'gpl'
    dir = 'data/' + f'run_{datadir_suffix}/'
    filename_gpl = f"gpl_{nSamples}_samples_dims_pxL.npy"
    filename_pvals = f"pvals_{nSamples}_samples.npy"
    filename_Lvals = f"Lvals_{nSamples}_samples.npy"
    gpl = np.load(dir + filename_gpl)
    pvals = np.load(dir + filename_pvals)
    Lvals = np.load(dir + filename_Lvals)
    for i, L in enumerate(Lvals):
        xvals = (pvals - pc)*L**(1/nu_exact)
        yvals = gpl[:,i]*L**(mu_approx/nu_exact)
        plt.plot(xvals, yvals)


    plt.xlabel(r'$L^{1/\nu}(p-p_c)$')
    plt.ylabel(r'$L^{\mu/\nu}g(p, L)$')
    plt.show()


# plot_datacollapse()














#
