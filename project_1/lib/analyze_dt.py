import numpy as np
import matplotlib.pyplot as plt
import sys, os



def read_log(filename, n_read_lines, n_types):



    #temp, PotEng, KinEng, TotEng
    measurements = np.zeros((n_read_lines, 4))


    with open(filename, 'r') as infile:
        for line in infile:
            if line[:4] == "Temp":
                for i in range(n_read_lines):
                    measurements[i] = np.fromstring(infile.readline(), dtype='float', count=4, sep=' ')

    return measurements




def analyze_dt(data_dir):


    items = os.listdir(data_dir)


    filenames = []
    for name in items:
        if name[:6] == "log.dt":
            filenames.append(name)

    filenames = sorted(filenames)
    n_files = len(filenames)
    n_read_lines = 101
    n_types = 4


    measurements = np.zeros((n_read_lines, n_types, n_files))
    for i in range(n_files):
        measurements[:,:,i] = read_log(data_dir + filenames[i], n_read_lines, n_types)


    for i in range(n_files):
        label = "%s" %filenames[i][3:]
        # plt.plot(list(range(measurements.shape[0])), measurements[:,1, i], label='PotEng')
        # plt.plot(list(range(measurements.shape[0])), measurements[:,2, i], label='KinEng')
        plt.plot(list(range(measurements.shape[0])), measurements[:,3, i], label=label) #totEng

    plt.legend()
    plt.show()
