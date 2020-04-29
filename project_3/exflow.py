# -*- coding: utf-8 -*-

from pylab import *
from scipy.sparse import spdiags, dia_matrix, coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.ndimage import measurements

#
# Written by Marin Soreng
# ( C ) 2004
#
# Calculates the effective flow conductance Ceff of the
# lattice A as well as the pressure P in every site .
def FIND_COND (A , X , Y ):
    P_in = 1.
    P_out = 0.
    # Calls MK_EQSYSTEM .
    B,C = MK_EQSYSTEM (A , X , Y )
    #print "B"
    #print B.todense()
    #print "C"
    #print C
    # Kirchhoff ’ s equations solve for P
    P = spsolve(B, C)
    # The pressure at the external sites is added
    # ( Boundary conditions )
    P = concatenate((P_in * ones (X), P,  P_out * ones (X)))
    # Calculate Ceff
    Ceff = (P[-1-2*X+1:-1-X] - P_out).T * A[-1-2*X+1:-1-X, 1] / ( P_in - P_out )
    #print "P"
    #print P
    #print "Ceff"
    #print Ceff
    return P , Ceff

#
# Written by Marin S r e n g
# ( C ) 2004
#
# Sets up Kirchoff ’ s equations for the 2 D lattice A .
# A has X * Y rows and 2 columns . The rows indicate the site ,
# the first column the bond perpendicular to the flow direction
# and the second column the bond parallel to the flow direction .
#
# The return values are [B , C ] where B * x = C . This is solved
# for the site pressure by x = B \ C .

def MK_EQSYSTEM (A , X , Y ):
    # Total no of internal lattice sites
    sites = X *( Y - 2)
    #print "sites:", sites
    # Allocate space for the nonzero upper diagonals
    main_diag = zeros(sites)
    upper_diag1 = zeros(sites - 1)
    upper_diag2 = zeros(sites - X)
    # Calculates the nonzero upper diagonals
    #print A
    main_diag = A[X:X*(Y-1), 0] + A[X:X*(Y-1), 1] + A[0:X*(Y-2), 1] + A[X-1:X*(Y-1)-1, 0]
    upper_diag1 = A [X:X*(Y-1)-1, 0]
    upper_diag2 = A [X:X*(Y-2), 1]
    main_diag[where(main_diag == 0)] = 1
    # Constructing B which is symmetric , lower = upper diagonals .
    B = dia_matrix ((sites , sites)) # B *u = t
    B = - spdiags ( upper_diag1 , -1 , sites , sites )
    B = B + - spdiags ( upper_diag2 ,-X , sites , sites )
    B = B + B.T + spdiags ( main_diag , 0 , sites , sites )
    # Constructing C
    C = zeros(sites)
    #    C = dia_matrix ( (sites , 1) )
    C[0:X] = A[0:X, 1]
    C[-1-X+1:-1] = 0*A [-1 -2*X + 1:-1-X, 1]
    return B , C

def sitetobond ( z ):
    #
    # Function to convert the site network z (L , L ) into a ( L *L ,2) bond
    # network
    # g [i,0] gives bond perpendicular to direction of flow
    # g [i,1] gives bond parallel to direction of flow
    # z [ nx , ny ] -> g [ nx * ny , 2]
    #
    nx = size (z ,1 - 1)
    ny = size (z ,2 - 1)
    N = nx * ny
    # g = zeros (N ,2)
    gg_r = zeros ((nx , ny)) # First , find these
    gg_d = zeros ((nx , ny )) # First , find these
    gg_r [:, 0:ny - 1] = z [:, 0:ny - 1] * z [:, 1:ny]
    gg_r [: , ny  - 1] = z [: , ny  - 1]
    gg_d [0:nx - 1, :] = z [0:nx - 1, :] * z [1:nx, :]
    gg_d [nx - 1, :] = 0
    #print "gg_r"
    #print gg_r
    #print "gg_d"
    #print gg_d
    # Then , concatenate gg onto g
    g = zeros ((nx *ny ,2))
    g [:, 0] = gg_d.reshape(-1,order='F').T
    g [:, 1] = gg_r.reshape(-1,order='F').T
    return g

def coltomat (z, x, y):
    # Convert z ( x * y ) into a matrix of z (x , y )
    # Transform this onto a nx x ny lattice
    g = zeros ((x , y))
    #print "For"
    for iy in range(1,y):
        i = (iy - 1) * x + 1
        ii = i + x - 1
        #print iy, i, ii
        g[: , iy - 1] = z[ i - 1 : ii]
    return g

if __name__ == "__main__":
    # First , find the backbone
    # Generate spanning cluster (l - r spanning )
    lx = 100
    ly = 100
    p = 0.59
    ncount = 0
    perc = []

    while (len(perc)==0):
        ncount = ncount + 1
        if (ncount >100):
            #print "Couldn't make percolation cluster..."
            break

        z=rand(lx,ly)<p
#        z = array([[1,1,1,1,1],[1,1,1,0,1],[0,1,1,0,1],[0,1,1,1,0],[1,0,1,0,1]])
        lw,num = measurements.label(z)
        perc_x = intersect1d(lw[0,:],lw[-1,:])
        perc = perc_x[where(perc_x > 0)]
        print "Percolation attempt", ncount

    #print "z="
    #print z*1
    labelList = arange(num + 1)
    clusterareas = measurements.sum(z, lw, index=labelList)
    areaImg = clusterareas[lw]
    maxarea = clusterareas.max()
    zz = asarray((lw == perc[0]))
    # zz now contains the spanning cluster
    # Transpose
    zzz = zz.T
#    # Generate bond lattice from this
    g = sitetobond ( zzz )
#    figure()
#    imshow(g[:,0].reshape(lx,ly), interpolation='nearest')
#    figure()
#    imshow(g[:,1].reshape(lx,ly), interpolation='nearest')
#    figure()
#    imshow(zzz, interpolation='nearest')
#    # Generate conductivity matrix
    p, c_eff = FIND_COND (g, lx, ly)
#    # Transform this onto a nx x ny lattice
    x = coltomat ( p , lx , ly )
    P = x * zzz
    g1 = g[:,0]
    g2 = g[: ,1]
    z1 = coltomat( g1 , lx , ly )
    z2 = coltomat( g2 , lx , ly )
#    # Plotting
    figure()
    ax = subplot(221)
    imshow(zzz, interpolation='nearest')
    title("Spanning cluster")
    grid(color="white")
#    subplot (2 ,2 ,1) , imagesc ( zzz )
#    title ( " Spanning cluster ")
#    axis equal
    subplot(222, sharex=ax, sharey=ax)
    imshow(P, interpolation='nearest')
    title("Pressure")
    colorbar()
    grid(color="white")
#    subplot (2 ,2 ,2) , imagesc ( P )
#    title ( " Pressure " )
#    axis equal

    # Calculate flux from top to down (remember that flux is the negative of the pressure difference)
    f2 = zeros ( (lx , ly ))
    for iy in range(ly -1):
        f2[: , iy ] = ( P [: , iy ] - P [: , iy +1]) * z2 [: , iy ]

    # Calculate flux from left to right (remember that flux is the negative of the pressure difference)
    f1 = zeros ( (lx , ly ))
    for ix in range(lx-1):
        f1[ ix ,:] = ( P [ ix ,:] - P [ ix +1 ,:]) * z1 [ ix ,:]
#
#    # Find the sum of absolute fluxes in and out of each site
    fn = zeros (( lx , ly ))
    fn = fn + abs ( f1 )
    fn = fn + abs ( f2 )
    # Add for each column, except the leftmost one, the up-down flux, but offset
    fn [: ,1: ly ] = fn [: ,1: ly ] + abs ( f2 [: ,0: ly -1])
    # For the left-most one, add the inverse pressure multiplied with the spanning cluster bool information
    fn [: ,0] = fn [: ,0] + abs (( P [: ,0] - 1.0)*( zzz [: ,0]))
    # For each row except the topmost one, add the left-right flux, but offset
    fn [1: lx ,:] = fn [1: lx ,:] + abs ( f1 [0: lx -1 ,:])
    subplot(223, sharex=ax, sharey=ax)
    imshow(fn, interpolation='nearest')
    title ( " Flux " )
    colorbar()
    grid(color="white")

    #print "fn"
    #print fn
#    subplot (2 ,2 ,3) , imagesc ( fn )
    zfn = fn > fn.max() - 1e-6
    zbb = ( zzz + 2* zfn )
    zbb = zbb / zbb.max()
    subplot(224, sharex=ax, sharey=ax)
    imshow(zbb, interpolation='nearest')
#    subplot (2 ,2 ,4) , imagesc ( zbb )
    title ( " BB and DE ")
    grid(color="white")
    show()
