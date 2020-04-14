import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')





# z = np.sort(z)

def cumulative_distribution(z):
    n = len(z)
    cumulative = np.zeros(n)
    cumulative[0] = z[0]
    for i in range(1, n):
        cumulative[i] = cumulative[i-1] + z[i]

    return cumulative/np.max(cumulative)



def log_bin(z, n_bins=20, base=10):
    log_max = np.ceil(np.max(np.log(z))/np.log(base))
    log_bins = np.logspace(0, log_max, n_bins)
    log_hist, _ = np.histogram(z, bins=log_bins)
    dz = np.diff(log_bins)
    log_bins = 0.5*(log_bins[1:] + log_bins[:-1])
    log_hist_normed = log_hist / dz

    return log_bins, log_hist


def plot_dist_function(z):
    z = np.sort(np.random.random(int(N))**(-2))
    Pz = cumulative_distribution(z)
    fz = np.gradient(Pz)
    plt.loglog(z, Pz, "b.", label=r'$P(Z > z)$')
    plt.loglog(z, fz, "r.", label=r'$f(z)=dP/dz$')
    plt.xlabel(r'z')


    alpha, b = np.polyfit(np.log(z), np.log(fz), deg=1)
    print(alpha)
    plt.legend()
    plt.show()


def plot_log_bins(z):
    bins, fz = log_bin(z)
    plt.loglog(bins, fz, "ro")
    plt.show()

N = 1e6
np.random.seed(12)
z = np.random.random(int(N))**(-3 + 1)

plot_log_bins(z)
