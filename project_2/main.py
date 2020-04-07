import numpy as np
import matplotlib.pyplot as plt
import os
import lammps_logfile
from pressDist import *
plt.style.use('ggplot')






def main():

    dirSpheres = "./sim_files/spheres_porous/"
    logFilename = "log.lammps"
    dumpFilename = "dump.lammpstrj"

    diffusion(dirSpheres, logFilename)
    # plotTemp(dirSpheres, logFilename)

def plotTemp(dir, filename):

    log = lammps_logfile.File(dir + filename)
    time = log.get("v_time", run_num=2)
    temp = log.get("c_moving_temp", run_num=2)

    plt.plot(time, temp)
    plt.xlabel(r"$t/\tau$")
    plt.ylabel(r"$T/T_0$")
    plt.show()


def radial_distribution(dir, filename, nBins = 50, nSteps=5000, stepWindow=100):
    # [bin number][bin coord][g(r)]

    nSkipLines = 3
    nWindows = int(nSteps/stepWindow + 1)
    ifile = open(dir + filename, "r")
    contents = ifile.readlines()

    distances = np.zeros((nBins, nWindows))
    bins = np.zeros(nBins)

    for b in range(nBins):
        idx = nSkipLines + b + 1
        line = contents[idx].split()
        bins[b] = line[1]

    i = nSkipLines + 1
    for w in range(nWindows):
        for b in range(nBins):
            line = contents[i].split()
            distances[b, w] = line[2]
            i += 1
        i += 1

    avg_distance = np.mean(distances, axis=1)
    avg_distance /= np.sqrt(np.sum(avg_distance**2))

    return bins, avg_distance


def plotRadial(dir, filename):
    dirSpheres = "./sim_files/spheres_porous/"
    fRadial1 = "radialDist_phiEqual1.tmp"
    fRadial2 = "radialDist_porous.tmp"
    bins, dist1 = radial_distribution(dirSpheres, fRadial1, nSteps=1000)
    bins, dist2 = radial_distribution(dirSpheres, fRadial2, nSteps=5000)

    plt.plot(bins, dist1, label=r"$\phi=1.0$")
    plt.plot(bins, dist2, label=r"$\phi=0.48$")
    plt.xlabel(r"Radial distance $[\sigma]$")
    plt.ylabel(r"$g(r)$")
    plt.legend()
    plt.show()


def diffusion(dir, filename):
    log = lammps_logfile.File(dir + filename)
    dt = 0.005
    time = np.array(log.get("v_time", run_num=2))
    msd = np.array(log.get("c_my_msd[4]", run_num=2))
    timeFinal = time[-1]

    coeff = np.polyfit(time, msd, deg=1)[0]
    D = coeff/(6*timeFinal)
    print(f"Estimated diffusion coefficient: D={D:.3f}")


    plt.plot(time, msd)
    plt.xlabel(r"$t/\tau$")
    plt.ylabel(r"$\langle r^2(t) \rangle / \sigma^2}$")
    plt.show()






if __name__ == '__main__':
    main()
