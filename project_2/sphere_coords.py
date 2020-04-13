import numpy as np
import matplotlib.pyplot as plt


# L = 33.5
L = 20
L4 = L/4
L8 = L/14
N = 27
# rMax = 3
# rMin = 2
rMin = L/10
rMax = L/6


xvals = np.zeros(N)
yvals = np.zeros(N)
zvals = np.zeros(N)
rvals = np.linspace(rMin, rMax, 10)


start=1
stop=4
step=1

c = 0
for i in range(start, stop, step):
    for j in range(start, stop, step):
        for k in range(start, stop, step):
            xvals[c] = L4*(i)
            yvals[c] = L4*(j)
            zvals[c] = L4*(k)
            if i == 1:
                xvals[c] -= L8
            elif i == 3:
                xvals[c] += L8
            if j == 1:
                yvals[c] -= L8
            elif j == 3:
                yvals[c] += L8
            if k == 1:
                zvals[c] -= L8
            elif k == 3:
                zvals[c] += L8


            c+=1

np.set_printoptions(precision=2)
print(xvals)
print(yvals)
print(zvals)
print(rvals)
