from scipy.stats import binned_statistic
import numpy as np
import matplotlib.pyplot as plt

sigma = 3.405
a = 20 / sigma
b = 5.72 / sigma
L = 20 * b

num_bins = 50
bin_edges = np.sqrt(np.linspace(0, a**2, num_bins + 1))
bin_mids = np.sqrt(0.5 * (bin_edges[1:]**2 + bin_edges[:-1]**2))

vx_dists = []
timesteps = []
num_values = 0

start_frame = 0  # From looking at graph

with open("sim_files/cylindrical/dump.lammpstrj", "r") as infile:
    for line in infile:
        if "TIMESTEP" in line:
            current_timestep = int(infile.readline())
            timesteps.append(current_timestep)
            print("Reading timestep %8d" % current_timestep)
        elif "NUMBER OF ATOMS" in line:
            number_of_atoms = int(infile.readline())
        elif "ITEM: ATOMS" in line:
            if current_timestep >= start_frame:
                headers = line.split()[2:]
                vxindex = headers.index("vx")
                yindex = headers.index("y")
                zindex = headers.index("z")
                values = np.zeros((number_of_atoms, len(headers)))
                for i in range(number_of_atoms):
                    line = infile.readline()
                    values[i] = line.split()
                vx = values[:, vxindex]
                y = values[:, yindex] - L / 2
                z = values[:, zindex] - L / 2
                r = np.sqrt(y**2 + z**2)

                vxs, binstuff1, binstuff2 = binned_statistic(
                    r, vx, "mean", bins=bin_edges)
                vx_dists.append(vxs)
            else:
                for i in range(number_of_atoms):
                    infile.readline()

equilibrium_vxs = np.asarray(vx_dists)
mean_result = np.nanmean(equilibrium_vxs, axis=0)

n = 2 / b**3
Fx = 0.1
m, b = np.polyfit(
    n * Fx / 4 * (a**2 - bin_edges[:-1]**2), mean_result, deg=1)
mu = 1 / m
print("b:", b)

approximation = n * Fx / (4 * mu) * (a**2 - bin_edges**2)


plt.plot(bin_edges[:-1], mean_result)
plt.plot(bin_edges, approximation)
plt.show()

print(mu)
