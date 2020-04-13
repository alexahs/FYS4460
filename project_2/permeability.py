import numpy as np
import matplotlib.pyplot as plt
import lammps_logfile
import os

b = 5.72
sigma = 3.405
b_sig = b/sigma
mu = 0.48
Fx = 0.1
n = 2/b_sig**3
# n = 2


data_dir = "./sim_files/spheres_porous/data/"
data_files = os.listdir(data_dir)
log_files = []
for file in data_files:
    if "log.spheres" in file:
        log_files.append(file)

n_files = len(log_files)

perm_measured = lambda u: u*mu/(n*Fx)
perm_spheres = lambda r, phi: r**2/45*phi**3/(1-phi)**2

r_vec = np.zeros(n_files)
phi_vec = np.zeros(n_files)
vcm_vec = np.zeros(n_files)

for i, filename in enumerate(log_files):
    idx_k = filename.index("_r")
    idx_phi = filename.index("phi")

    r = filename[idx_k + 2:idx_k + 5]
    phi = filename[idx_phi + 3: idx_phi + 7]

    r_vec[i] = r
    phi_vec[i] = phi

    log = lammps_logfile.File(data_dir + filename)
    vcm = log.get("v_velocity_cm", run_num=0)
    if type(vcm) is np.ndarray:
        avg_vcm = np.mean(vcm)
        vcm_vec[i] = avg_vcm
    else:
        print(f"no vcm data in file {filename}")
        # exit()


sorted_idx = np.argsort(r_vec)
r_vec = r_vec[sorted_idx]
phi_vec = phi_vec[sorted_idx]
vcm_vec = vcm_vec[sorted_idx]
# print(r_vec)
# print(phi_vec)
print(vcm_vec)

# plt.plot(phi_vec, vcm_vec)
plt.scatter(phi_vec, perm_measured(vcm_vec), c="r", label="Measured permeability")
plt.plot(phi_vec, perm_spheres(r_vec, phi_vec), label="Theoretical")
plt.xlabel(r"$\phi$")
plt.ylabel(r"$k/\sigma^3$")
plt.legend()
plt.show()
