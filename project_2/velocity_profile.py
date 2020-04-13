import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def main():


    dir = "./sim_files/cylindrical/"
    # filename = "flow_final.lammpstrj"
    filename = "dump.lammpstrj"

    # pos, vel = readFinalState(dir + filename)
    # bins, vel = averageVelBins(pos, vel, 10)
    # # center = np.mean(binPos)
    # binPos = binPos - center

    # avgVel = np.mean(vel)
    nBins = 50

    velocity_profile(dir + filename, nBins)





def velocity_profile(filename, nBins):
    # timeStep = 999
    sigma = 3.405
    b = 5.72/sigma
    a = 20/sigma
    L = 20*b
    Fx = 0.1
    n = 2/b**3


    infile = open(filename, "r")

    bins = np.linspace(0, a, nBins)
    counts = np.zeros(nBins)
    cumulative_vx = np.zeros(nBins)

    for line in infile:
        if "NUMBER OF ATOMS" in line:
            nAtoms = int(infile.readline())
        elif "ITEM: ATOMS" in line:
            keywords = line.split()[2:]
            yIdx = keywords.index("y")
            zIdx = keywords.index("z")
            vxIdx = keywords.index("vx")
            # r = np.zeros(nAtoms)
            # vx = np.zeros(nAtoms)
            for i in range(nAtoms):
                line = infile.readline().split()
                # vals = line.split()
                y = float(line[yIdx]) - L/2
                z = float(line[zIdx]) - L/2
                r = np.sqrt(y**2 + z**2)
                vx = float(line[vxIdx])

                idx = np.where(bins < r)[0]
                if len(idx) == 0:
                    idx = 0
                else:
                    idx = idx[-1]

                cumulative_vx[idx] += vx
                counts[idx] += 1

    infile.close()
    velocities = cumulative_vx/counts

    rPrime = n*Fx*(a**2 - bins**2)/4

    m, b = np.polyfit(rPrime, velocities, deg=1)
    print(m, b)
    mu = 1/m
    print(f"mu = {mu}")

    approx = n*Fx/(4*mu)*(a**2 - bins**2)

    plt.plot(bins, approx, "r", label="continuum result $u(r)$")
    plt.plot(bins, approx + b, "r--", label="$u(r) + b$, $b=%.3f$" %b)
    plt.scatter(bins, velocities, c="b", label="data")
    plt.xlabel(r"$r/\sigma$")
    plt.ylabel(r"$v_x \tau/\sigma$")
    plt.legend()
    plt.show()





if __name__ == '__main__':
    main()
