from flow_in_perc import *
from pylab import *

# Generate spanning cluster (l - r spanning )
lx = 400
ly = 400
p = 0.5927
ncount = 0
perc = []
while (len(perc)==0):
    ncount = ncount + 1
    if (ncount >100):
        break
    z=rand(lx,ly)<p
    lw,num = measurements.label(z)
    perc_x = intersect1d(lw[0,:],lw[-1,:])
    perc = perc_x[where(perc_x > 0)]
    print("Percolation attempt", ncount)
zz = asarray((lw == perc[0]))
# zz now contains the spanning cluster
zzz = zz.T # Transpose
g = sitetobond ( zzz ) # Generate bond lattice
V, c_eff = FIND_COND (g, lx, ly) # Find conductivity
x = coltomat ( V , lx , ly ) # Transform to nx x ny lattice
V = x * zzz
g1 = g[:,0]
g2 = g[: ,1]
z1 = coltomat( g1 , lx , ly )
z2 = coltomat( g2 , lx , ly )

# Plot results
figure(figsize=(16,16))
ax = subplot(221)
imshow(zzz, interpolation='nearest')
title("Spanning cluster")
subplot(222, sharex=ax, sharey=ax)
imshow(V, interpolation='nearest')
title("Potential")

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

# Plot results
subplot(223, sharex=ax, sharey=ax)
imshow(fn, interpolation='nearest')
title (" Current ")
# Singly connected
zsc = fn > (fn.max() - 1e-6)
# Backbone
zbb = fn>1e-6
# Combine visualizations
ztt = ( zzz*1.0 + zsc*2.0 + zbb*3.0 )
zbb = zbb / zbb.max()
subplot(224, sharex=ax, sharey=ax)
imshow(ztt, interpolation='nearest')
title (" SC, BB and DE ")
show()
