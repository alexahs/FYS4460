import sys
import numpy as np


start, stop, inc = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])


outfile = open("T_vals.txt", 'w')

for T in np.arange(start, stop, inc):
    outfile.write(str(T) + "\n")

outfile.close()
