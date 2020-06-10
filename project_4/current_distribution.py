import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy.ndimage import measurements
from matplotlib.colors import ListedColormap
from flow_in_perc import *
from tqdm import tqdm
import os

pc = 0.59275

def generate_percolating(L, p, verbose=False):
    ncount = 0
    perc = []
    while (len(perc)==0):
        ncount = ncount + 1
        if (ncount >100):
            break
        z=rand(L,L)<p
        lw,num = measurements.label(z)
        perc_x = intersect1d(lw[0,:],lw[-1,:])
        perc = perc_x[where(perc_x > 0)]
        if verbose:
            print("Percolation attempt", ncount)
    z = asarray((lw == perc[0]))

    return z


def calculate_currents(z):
    lx, ly = z.shape
    zzz = z.T # Transpose
    g = sitetobond ( zzz ) # Generate bond lattice
    V, c_eff = FIND_COND (g, lx, ly) # Find conductivity
    x = coltomat ( V , lx , ly ) # Transform to nx x ny lattice
    V = x * zzz
    g1 = g[:,0]
    g2 = g[: ,1]
    z1 = coltomat( g1 , lx , ly )
    z2 = coltomat( g2 , lx , ly )


    # Calculate current from top to down from the potential
    f2 = zeros ( (lx , ly ))
    for iy in range(ly -1):
        f2[: , iy ] = ( V [: , iy ] - V [: , iy +1]) * z2 [: , iy ]
    # Calculate current from left to right from the potential
    f1 = zeros ( (lx , ly ))
    for ix in range(lx-1):
        f1[ ix ,:] = ( V [ ix ,:] - V [ ix +1 ,:]) * z1 [ ix ,:]


    # Find the sum of (absolute) currents in and out of each site
    fn = zeros (( lx , ly ))
    fn = fn + abs ( f1 )
    fn = fn + abs ( f2 )
    # Add for each column (except leftmost) the up-down current, but offset
    fn [: ,1: ly ] = fn [: ,1: ly ] + abs ( f2 [: ,0: ly -1])
    # For the left-most one, add the inverse potential
    # multiplied with the spanning cluster bool information
    fn [: ,0] = fn [: ,0] + abs (( V [: ,0] - 1.0)*( zzz [: ,0]))
    # For each row (except topmost) add the left-right current, but offset
    fn [1: lx ,:] = fn [1: lx ,:] + abs ( f1 [0: lx -1 ,:])


    # Backbone
    zbb = fn>1e-14

    return fn, zbb, c_eff


def create_hist(z, edges, log = True, n_bins=10, base=10):
    if log:
        bins = np.logspace(edges[0], edges[1], num=n_bins, base=base)
    else:
        bins = np.linspace(edges[0], edges[1], num=n_bins)
    hist, bins = np.histogram(z, bins=bins)
    bins = 0.5*(bins[1:] + bins[:-1])

    return hist, bins




def calculate_distribution(L, p, nSamples=100, nBins=20):


    mass_bb = 0
    currents = []
    for i in tqdm(range(nSamples)):

        z = generate_percolating(L, p)
        zCurrents, zbb, totalCurrent = calculate_currents(z)
        Mbb = sum(zbb)
        mass_bb += Mbb
        fractional_currents = (np.ravel(zCurrents)/totalCurrent)
        currents.append(fractional_currents)

    mass_bb /= nSamples

    currents /= nSamples*mass_bb

    currents = np.ravel(currents)
    hist, bins = create_hist(currents, edges=(-15, 0), log=True, n_bins=nBins)
    return hist, bins


def calculate_moments_of_distribution(L, p, q, nSamples=100, nBins=20):
    mass_bb = 0
    currents = []
    for i in tqdm(range(nSamples)):

        z = generate_percolating(L, p)
        zCurrents, zbb, totalCurrent = calculate_currents(z)
        Mbb = sum(zbb)
        mass_bb += Mbb
        currents_ravel = np.ravel(zCurrents)
        fractional_currents = (currents_ravel/totalCurrent)
        currents.append(fractional_currents)


    currents = np.ravel(currents)
    currents /= nSamples
    hist, bins = create_hist(currents, edges=(-3, 0), log=True, n_bins=nBins)
    # hist, bins = create_hist(currents, edges=(0, 1), log=False, n_bins=nBins)
    hist = hist*bins**(2*q)
    return hist, bins


def plot_normalized_distributions():
    p = pc
    nBins = 80
    nSamples = 100
    L = 400
    # Lvals = [50, 100, 200, 400]
    # for L in tqdm(Lvals):
    for p in tqdm([0.585, pc, 0.6]):
        hist, bins = calculate_distribution(L, p, nSamples, nBins)
        # plt.semilogx(bins, hist, label=f'L={L}')
        plt.semilogx(bins, hist, label=f'p={p}')

    plt.xlabel(f"Fractional current $i_b$")
    plt.ylabel("Distribution $P(i)$")
    plt.legend()
    plt.show()

# plot_normalized_distributions()

def plot_distribution_moments():
    p = pc
    nBins = 80
    nSamples = 100
    L = 200
    moments = [5, 10, 15]
    for q in tqdm(moments):
        hist, bins = calculate_moments_of_distribution(L, p, q, nSamples, nBins)
        plt.semilogx(bins, hist/hist.max(), label=f'q={q}')
        # plt.plot(bins, hist/hist.max(), label=f'q={q}')

    plt.xlabel(f"Fractional current $i_b$")
    plt.ylabel("Distribution $n(i)i^{2q}$")
    plt.legend()
    plt.show()

# plot_distribution_moments()


def moments_of_current():

    p = pc
    nSamples = 600
    Lvals = [25, 50, 100, 200, 400]
    moments = [0, 1, 2, 3]
    currents = np.zeros((len(Lvals), len(moments)))

    for s in tqdm(range(nSamples)):
        for i, L in enumerate(Lvals):
            for j, q in enumerate(moments):
                z = generate_percolating(L, p)
                zCurrents, zbb, totalCurrent = calculate_currents(z)
                currents[i, j] = np.sum((zCurrents/totalCurrent)**(2*q))


    currents /= nSamples
    dir = "data/internal_flux/"
    np.save(dir + f"moments_of_current_{nSamples}_samples.npy", currents)
    np.save(dir + f"Lvals_{nSamples}_samples.npy", Lvals)
    np.save(dir + f"qVals_{nSamples}_samples.npy", moments)
    for j, q in enumerate(moments):
        log_L = np.log10(Lvals)
        log_i = np.log10(currents[:,j])
        y, b = np.polyfit(log_L, log_i, deg=1)
        plt.plot(log_L, log_i, 'o', label=f"$q={q}, y(q)={y:.2f}$")

    plt.xlabel(r"$\log_{10} L$")
    plt.ylabel(r"$\log_{10} \langle i^{2q} \rangle$")
    plt.legend()
    plt.show()

moments_of_current()








# L = 400
# p = 0.6


















#
