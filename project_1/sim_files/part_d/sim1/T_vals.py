import sys
import numpy as np


start, stop, inc = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])

if len(sys.argv) > 4:
    filename = sys.argv[4]
else:
    filename = "T_vals.txt"


outfile = open(filename, 'w')

for T in np.arange(start, stop, inc):
    outfile.write(str(T) + "\n")

outfile.close()
