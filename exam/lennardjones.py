import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')



def lj(r):
    return 4*((1/r)**12 - (1/r)**6)

#
# r_min = 2**(1/6)
# r = np.linspace(0.9, 3, 100)
# plt.scatter(r_min, lj(r_min))
# plt.plot(r, lj(r))
# plt.xlabel(r"$r/\sigma$")
# plt.ylabel(r"$U(r)/\epsilon$")
# plt.show()


tau = 2.1569e-12 #s
sigma = 3.405e-10 #m
eps = 1e-2*1.6e-19 #J

ljMu = eps*tau/sigma**3 #Js/m^3

print(0.98*ljMu*1e6)
