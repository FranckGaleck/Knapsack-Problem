'''
GUERRA ADAMES Ariel
Script containing extraction algorithms used to
execute experiments based on external datasets
'''

import numpy as np
import fnmatch
import os
from scipy import stats

def read_knapsack(filepath):
    """Function to extract the values of the 0/1 knapsack problem found in
    http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/ .

    Parameters
    ----------
    filepath : path of the directory containing the problem instances.

    Returns
    -------
    values : list of item values.
    weights : list of item weights.
    capacity : maximum weight the knapsack can hold.
    """
    items = np.loadtxt(filepath, delimiter=' ')
    values = items[1:, 0].astype(int)
    weights = items[1:, 1].astype(int)
    capacity = items[0, 1].astype(int)
    return values, weights, capacity

def read_optimal(filepath):
    """Function to extract the optimal profit of the 0/1 knapsack problem found in
    http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/ .

    Parameters
    ----------
    filepath : path of the directory containing the problem solutions.

    Returns
    -------
    optimal: optimal profit of the selected instance.
    """
    optimal = np.loadtxt(filepath)
    return optimal


def read_multiknapsack(directory):
    """Function to extract instances of the 0/1 multiple knapsack problem
    found in https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_multiple/knapsack_multiple.html .

    Parameters
    ----------
    filepath : path of the directory containing the problem instances.

    Returns
    -------
    capacities : maximum weights that each of the knapsacks can hold.
    values : list of item values.
    weights : list of item weights.
    s_sack1 : (optional) one-hot coded solution vector for the first knapsack. Only provided
                for 2-knapsack problems.
    s_sack2 : (optional) one-hot coded solution vector for the second knapsack. Only provided
                for 2-knapsack problems.
    optimal_v2 : (optional) maximum profit attainable according to the solution vector. Only
                    provided for 2-knapsack problems.
    optimal_v2 : (optional) maximum profit attainable according to the solution vector. Only
                    provided for 2-knapsack problems.
    """
    s_sack1, s_sack2, optimal_v1, optimal_v2 = [], [], 0, 0
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(directory+'/'+filename, '*c.txt'):
            capacities = np.loadtxt(directory+'/'+filename)
        if fnmatch.fnmatch(directory+'/'+filename, '*p.txt'):
            values = np.loadtxt(directory+'/'+filename, unpack=True).astype(int)
        if fnmatch.fnmatch(directory+'/'+filename, '*w.txt'):
            weights = np.loadtxt(directory+'/'+filename, unpack=True).astype(int)

    for filename in os.listdir(directory):
        if fnmatch.fnmatch(directory+'/'+filename, '*s.txt'):
            solutions = np.loadtxt(directory+'/'+filename)
            s_sack1 = solutions[:, 0]
            s_sack2 = solutions[:, 1]
            optimal_v1 = sum(np.prod([values, s_sack1], axis=0))
            optimal_v2 = sum(np.prod([values, s_sack2], axis=0))

    return capacities, values, weights, s_sack1, s_sack2, optimal_v1, optimal_v2

### Example of use of the above function
# capacities, values, weights, s_sack1, s_sack2, optimal1, optimal2 = read_multiknapsack('multiple_knapsack/kp1')
