from pylab import *
from scipy.sparse import spdiags, dia_matrix, coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.ndimage import measurements
# Written by Marin Soreng 2004
# Calculates the effective flow conductance Ceff of the
# lattice A as well as the potential V in every site .
def FIND_COND (A , X , Y ):
    V_in = 1.
    V_out = 0.
    # Calls MK_EQSYSTEM .
    B,C = MK_EQSYSTEM (A , X , Y )
    # Kirchhoff ’ s equations solve for V
    V = spsolve(B, C)
    # The pressure at the external sites is added
    # ( Boundary conditions )
    V = concatenate((V_in * ones (X), V, V_out * ones (X)))
    # Calculate Ceff
    # second-last X elements of V multiplied with second-last elem. of A
    # these are the second last column of the system
    # gives the conductivity of the system per row?
    Ceff = dot((V[-1-2*X:-1-X] - V_out).T, A[-1-2*X:-1-X, 1]) / ( V_in - V_out )

    return V , Ceff


# Sets up Kirchoff ’ s equations for the 2 D lattice A .
# A has X * Y rows and 2 columns . The rows indicate the site ,
# the first column the bond perpendicular to the flow direction
# and the second column the bond parallel to the flow direction .
# The return values are [B , C ] where B * x = C . This is solved
# for the site pressure by x = B \ C .
def MK_EQSYSTEM (A , X , Y ):
    # Total no of internal lattice sites
    sites = X *( Y - 2)
    # Allocate space for the nonzero upper diagonals
    main_diag = zeros(sites)
    upper_diag1 = zeros(sites - 1)
    upper_diag2 = zeros(sites - X)
    # Calculates the nonzero upper diagonals
    main_diag = A[X:X*(Y-1), 0] + A[X:X*(Y-1), 1] + \
    A[0:X*(Y-2), 1] + A[X-1:X*(Y-1)-1, 0]
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
    # C = dia_matrix ( (sites , 1) )
    C[0:X] = A[0:X, 1]
    C[-1-X+1:-1] = 0*A [-1 -2*X + 1:-1-X, 1]
    return B , C



def sitetobond ( z ):
    # Function to convert the site network z(L,L) into a (L*L,2) bond
    # network
    # g [i,0] gives bond perpendicular to direction of flow
    # g [i,1] gives bond parallel to direction of flow
    # z [ nx , ny ] -> g [ nx * ny , 2]
    nx = size (z ,1 - 1)
    ny = size (z ,2 - 1)
    N = nx * ny
    gg_r = zeros ((nx , ny)) # First , find these
    gg_d = zeros ((nx , ny )) # First , find these
    gg_r [:, 0:ny - 1] = z [:, 0:ny - 1] * z [:, 1:ny]
    gg_r [: , ny - 1] = z [: , ny - 1]
    gg_d [0:nx - 1, :] = z [0:nx - 1, :] * z [1:nx, :]
    gg_d [nx - 1, :] = 0
    # Then , concatenate gg onto g
    g = zeros ((nx *ny ,2))
    g [:, 0] = gg_d.reshape(-1,order='F').T
    g [:, 1] = gg_r.reshape(-1,order='F').T
    return g



def coltomat (z, x, y):
    # Convert z(x*y) into a matrix of z(x,y)
    # Transform this onto a nx x ny lattice
    g = zeros ((x , y))
    for iy in range(1,y):
        i = (iy - 1) * x + 1
        ii = i + x - 1
        g[: , iy - 1] = z[ i - 1 : ii]
    return g
