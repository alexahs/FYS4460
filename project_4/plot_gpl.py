from pylab import *
from scipy.ndimage import measurements
from matplotlib.colors import ListedColormap
from flow_in_perc import *
from tqdm import tqdm
import numpy as np
import os
Lvals = [25,50,100,200,400]
# Lvals = [25,50,100]
pVals = logspace(log10(0.58), log10(0.85), 20)

C = zeros((len(pVals),len(Lvals)),float)
P = zeros((len(pVals),len(Lvals)),float)
nSamples = 100
mu = zeros(len(Lvals))
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
run = 2
newdir = dir + f"run_{run}/"
os.mkdir(newdir)

filename_gpl = f"gpl_{nSamples}_samples_dims_pxL.npy"
filename_pvals = f"pvals_{nSamples}_samples.npy"
filename_Lvals = f"Lvals_{nSamples}_samples.npy"
np.save(newdir + filename_gpl, C)
np.save(newdir + filename_pvals, pVals)
np.save(newdir + filename_Lvals, Lvals)

for iL in range(len(Lvals)):
    L = Lvals[iL]
    plot(pVals,C[:,iL],label="L="+str(L))
xlabel(r"$p$")
ylabel(r"$C$")
legend()
show()
