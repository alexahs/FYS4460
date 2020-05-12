from pylab import *
from scipy.ndimage import measurements
from flow_in_perc import *
from tqdm import tqdm
Lvals = [400]
# pVals = logspace(log10(0.58), log10(0.85), 20)
pVals = logspace(log10(0.58), log10(0.85), 10)
C = zeros((len(pVals),len(Lvals)),float)
P = zeros((len(pVals),len(Lvals)),float)
# nSamples = 600
nSamples = 100
G = zeros(len(Lvals))
for iL in range(len(Lvals)):
    L = Lvals[iL]
    lx = L
    ly = L
    for pIndex in tqdm(range(len(pVals))):
        p = pVals[pIndex]
        ncount = 0
        for j in tqdm(range(nSamples)):
            ncount = 0
            perc = []
            while (len(perc)==0):
                ncount = ncount + 1
                if (ncount > 1000):
                    print("Couldn’t make percolation cluster...")
                    break
                z=rand(lx,ly)<p
                lw,num = measurements.label(z)
                perc_x = intersect1d(lw[0,:],lw[-1,:])
                perc = perc_x[where(perc_x > 0)]
            if len(perc) > 0: # Found spanning cluster
                area = measurements.sum(z, lw, perc[0])
                P[pIndex,iL] = P[pIndex,iL] + area # Find P(p,L)
                zz = asarray((lw == perc[0])) # zz=spanning cluster
                zzz = zz.T
                g = sitetobond (zzz) # Generate bond lattice
                Pvec, c_eff = FIND_COND(g, lx, ly) # Find conducance
                C[pIndex,iL] = C[pIndex,iL] + c_eff
        C[pIndex,iL] = C[pIndex,iL]/nSamples
        P[pIndex,iL] = P[pIndex,iL]/(nSamples*L*L)

plot(pVals,C[:,-1],'-ob',label='$G$')
plot(pVals,P[:,-1],'-or',label='$P$')
legend()
xlabel(r"$p$")
ylabel(r"$G,P$")
show()
