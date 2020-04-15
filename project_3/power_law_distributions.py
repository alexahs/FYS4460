import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')



N = 1e5
np.random.seed(12)
z = np.sort(np.random.random(int(N))**(-3 + 1))

def cumulative_distribution_v1(z):
    n = len(z)
    cumulative = np.zeros(n)
    cumulative[0] = z[0]
    for i in range(1, n):
        cumulative[i] = cumulative[i-1] + z[i]

    return cumulative/np.max(cumulative)

def compute_distribution_function(z):
    n = len(z)
    P = np.linspace(1, n + 1, n)/n
    f = np.diff(P) / np.diff(z)
    alpha, _ = np.polyfit(np.log(z[1:]), np.log(f), deg=1)
    return P, f, alpha


    plt.loglog(z[1:], f, label='$f(z)$')
    plt.loglog(z, P, label='P(Z > z)')
    plt.loglog(z, z**alpha, label=r'Fit to $f(z) = z^\alpha$')
    plt.xlabel('$z$')
    plt.legend()
    # plt.axis([0, 10, 0, 1])
    plt.show()


def plot_distribution(z):
    P, f, alpha = compute_distribution_function(z)
    plt.loglog(z[1:], f, label='$f(z)$')
    plt.loglog(z, P, label='P(Z > z)')
    plt.loglog(z, z**alpha, label=r'Fit to $f(z) = z^\alpha$')
    plt.xlabel('$z$')
    plt.legend()
    print(f'Fitted exponent alpha={alpha}$')
    plt.show()


def log_bin(z, n_bins=20, base=10):
    log_max = np.ceil(np.max(np.log(z))/np.log(base))
    log_bins = np.logspace(0, log_max, n_bins)
    log_hist, _ = np.histogram(z, bins=log_bins)
    dz = np.diff(log_bins)
    log_bins = 0.5*(log_bins[1:] + log_bins[:-1])
    log_hist_normed = log_hist / dz

    return log_bins, log_hist



def plot_log_bins(z):
    bins, fz = log_bin(z)
    plt.loglog(bins, fz, "ro")
    plt.show()


plot_distribution(z)


# plot_log_bins(z)

# plot_dist_function(z)
