'''
GUERRA ADAMES Ariel
Script containing functions used to obtain experimental results.
'''

import time
import numpy as np
import matplotlib.pyplot as plt
import problem_generator as pg
from bruteforce import bruteforce
from greedy import *
from dynamic import *
from poly import *
from randomize import *
from genetic import *
from middle import *
from backtracking import *

def time_test_brute(noitems):
    times, knapsize = [], []
    for i in range(3, noitems, 3):
        print("Testing for %d items"%i)
        data = pg.uniform_dist(i, capacity=i*10, maxw=50, maxv=50)
        print(data[0], data[1], data[2])
        init = time.time()
        values, weights, solution = bruteforce(data[0], data[1], data[2])
        print(values)
        exec_t = time.time()-init
        print("Execution time: "+str(exec_t)+" seconds")
        knapsize.append(i)
        times.append(exec_t*1000)
    return times, knapsize

# times, knapsize = time_test_brute(9)  # Usage example

def time_test(noitems, algorithm):
    times, knapsize, accuracies = [], [], []
    for i in range(3, noitems, 33):
        print("Testing for %d items"%i)
        data = pg.uniform_dist(i, capacity=i*10, maxw=50, maxv=50, calc_optimal=False)   # Uniform distribution
        # data = pg.normal_dist(i, mean=100, std=50, capacity=i*10, seed=42, calc_optimal=False)  # Normal distribution
        # data = pg.triang_dist(i, minw=1, maxw=100, modew=5, minv=10, maxv=100, modev=90, capacity=200, seed=42, calc_optimal=False)  # Triangular distribution
        print(data)
        init = time.time()
        solution, values, accuracy = algorithm(data[0], data[1], data[2], data[3])
        exec_t = (time.time()-init)
        print("Execution time: "+str(exec_t)+" seconds")
        knapsize.append(i)
        times.append(exec_t)
        accuracies.append(accuracy)
    return times, knapsize, accuracies

def time_genetic(population_size):
    times, knapsize, accuracies = [], [], []
    for i in range(10, population_size, 100):
        print("Testing for %d individuals"%i)
        data = pg.uniform_dist(100, capacity=i*10, maxw=50, maxv=50, calc_optimal=False)   # Uniform distribution
        # data = pg.normal_dist(i, mean=100, std=50, capacity=i*10, seed=42, calc_optimal=False)  # Normal distribution
        # data = pg.triang_dist(i, minw=1, maxw=100, modew=5, minv=10, maxv=100, modev=90, capacity=200, seed=42, calc_optimal=False)  # Triangular distribution
        print(data)
        init = time.time()
        solution, values, accuracy = genetic(data[0], data[1], data[2], data[3], solution_no=i)
        exec_t = (time.time()-init)
        print("Execution time: "+str(exec_t)+" seconds")
        knapsize.append(i)
        times.append(exec_t)
        accuracies.append(accuracy)
    return times, knapsize, accuracies

# times, knapsize, accuracies = time_genetic(2100)  # Usage example
# print(knapsize)
# print(times)
# print(np.mean(accuracies))
