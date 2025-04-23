'''
TRIVEDI Josh
Script containing algorithms necessary to perform the backtracking approach.
'''

import sys
import math
import extract
import time
from leven import levenshtein
import numpy as np
import problem_generator as pg

sys.setrecursionlimit(10**8)

c = 0
def knapsack(mW, weights, values, n):
    global c
    c += 1
    if(n == 0 or mW == 0):
        return [0, []]
    
    if(weights[n-1] > mW):
        return knapsack(mW, weights, values, n-1)
    
    set1 = knapsack(mW-weights[n-1], weights, values, n-1)
    set2 = knapsack(mW, weights, values, n-1)

    if(set1[0] + values[n-1] > set2[0]):
        set1[1].append(n-1)
        set1[0] += values[n-1]
        return set1
    else:
        return set2
    
def accuracy(sol):
    optimal = extract.read_optimal("low-dimensional-optimum/f2_l-d_kp_20_878")
    acc = sol[0]/optimal * 100
    return acc

def onehot(sol, val, wt, W):
    n = len(val)
    onehot = [0]*n
    for i in range(len(sol[1])):
        onehot[sol[1][i]] = 1
    return onehot

def main():
    #  Declaring item and capacity paths
    filename = 'f10_l-d_kp_20_879'
    items_path = 'low-dimensional/' + str(filename)
    optimal_path = 'low-dimensional-optimum/' + str(filename)
    solution_path = 'low-dimensional-solutions/' + str(filename)

    # Reading the values of the dataset
    val, wt, W = extract.read_knapsack(items_path)
    print(val, wt, W)
    optimal = extract.read_optimal(optimal_path)
    solution = np.loadtxt(solution_path, delimiter=',')
    n = len(val)

    # Using the problem generator
    # i = 6
    # val, wt, W, optimal = pg.uniform_dist(i, capacity=i * 10, maxw=50, maxv=50, calc_optimal=False)  # Uniform distribution
    # print(val, wt, W, optimal)
    # n = len(val)

    #Executing function and evaluating time performance
    tic = time.time()
    sol = knapsack(W, wt, val, n)
    toc = time.time() - tic

    ## Evaluating results
    backtrack_res = onehot(sol, val, wt, W)
    found_solution = np.array(backtrack_res)
    found_solution = np.array2string(found_solution, separator='.,', precision=None)
    optimal_solution = np.array2string(solution, separator=',', precision=None)

    sol_accuracy = sol[0] / optimal
    edit_distance = levenshtein(optimal_solution, found_solution)-1

    print("Execution time: %s seconds" % toc)
    print("Solution vector: " + str(backtrack_res))
    print("Value of the objects in the knapsack: %d €" % sol[0])
    print("Optimal value: %d €" % optimal)
    print("Solution accuracy: " + str(sol_accuracy * 100))
    print("Edit distance of solution: " + str(edit_distance))
    print("Total recursive steps: ", c)

if __name__ == "__main__":
    main()
