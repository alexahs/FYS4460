import numpy as np
import matplotlib.pyplot as plt
import sys, os
from lib.analyze_velocity_distribution import *
from lib.analyze_dt import *
from lib.measure_temp import *




def main():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    dir_part_a = main_dir + "/sim_files/part_a/sim1/"
    dir_part_b = main_dir + "/sim_files/part_b/sim1/"
    dir_part_c = main_dir + "/sim_files/part_c/sim1/"


    analyze_velocity_distribution(dir_part_a)
    # analyze_dt(dir_part_b)
    # measure_temp(dir_part_c)





    exit(1)









if __name__ == '__main__':
    main()
