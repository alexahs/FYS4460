import numpy as np
import matplotlib.pyplot as plt
import sys, os



def read_log(filename):


    n_read_lines = 51 #

    #temp, PotEng, KinEng, TotEng
    measurements = np.zeros((n_read_lines, 4))


    with open(filename, 'r') as infile:
        for line in infile:
            if line[:4] == "Temp":
                for i in range(n_read_lines):
                    measurements[i] = np.fromstring(infile.readline(), dtype='float', count=4, sep=' ')

    return measurements






def main():


    filenames = os.listdir()

    print(filenames)

    # filename = "log.dt_0.05"

    # measurements = read_log(filename)


    # print(measurements.shape)

    # plt.plot(list(range(measurements.shape[0])), measurements[:,1], label='PotEng')
    # plt.plot(list(range(measurements.shape[0])), measurements[:,2], label='KinEng')
    # plt.plot(list(range(measurements.shape[0])), measurements[:,3], label='TotEng')
    # plt.legend()
    # plt.show()



if __name__ == '__main__':
    main()
