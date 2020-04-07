import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')



def plotStress(filename, center=33.6/2, nBins=20, dx=1):

    forTimeStep = 1000
    dumpStep = 1000
    nSkipLines = 9

    infile = open(filename, "r")
    contents = infile.readlines()

    nAtoms = int(contents[3])
    boxBound = float(contents[5].split()[1])

    idxBeginRead = 2*nSkipLines + nAtoms
    assert(int(contents[idxBeginRead-nSkipLines+1])==forTimeStep)


    #indices
    ix = 2
    iy = 3
    iz = 4
    isx = 8
    isy = 9
    isz = 10

    yArr = []
    zArr = []
    sArr = []


    j = idxBeginRead
    for i in range(nAtoms):
        line = contents[j].split()
        xpos = float(line[ix])
        if xpos > center - dx and xpos < center + dx:
            yArr.append(float(line[iy]))
            zArr.append(float(line[iz]))
            sx = float(line[isx])
            sy = float(line[isy])
            sz = float(line[isz])
            sMagn = -1*(sx + sy + sz) #pressure is negative of stress on atom
            sArr.append(sMagn)

        j+=1
    #end for

    yArr = np.array(yArr)
    zArr = np.array(zArr)
    sArr = np.array(sArr)

    S, Z, Y = np.histogram2d(zArr, yArr, bins=nBins, weights=sArr, normed=False)
    counts, _, _ = np.histogram2d(zArr, yArr, bins=nBins)
    S /= counts
    S = np.ma.masked_invalid(S)


    plt.pcolormesh(Y, Z, S, edgecolors=None)#, vmin=0, vmax=40)
    cbar = plt.colorbar()
    plt.margins(0.0)
    plt.xlabel(r"$y/\sigma$")
    plt.ylabel(r"$z/\sigma$")
    cbar.set_label(r"average pressure per atom volume $p^*/\sigma^3$")
    plt.savefig(f"./figures/pressure/crossection_center={center}.png")
    # plt.show()
    plt.clf()

def plotTempEvolution():
    filename = "temps.txt"
    infile = open(filename, "r")
    contents = infile.readlines()

    nLines = len(contents)
    steps = np.zeros(nLines)
    temps = np.zeros(nLines)

    for i in range(nLines):
        line = contents[i].split()
        steps[i] = float(line[0])
        temps[i] = float(line[1])

    plt.plot(steps, temps)
    plt.xlabel("Time steps")
    plt.ylabel("Temperature")
    plt.show()
