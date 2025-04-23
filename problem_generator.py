'''
GUERRA ADAMES Ariel
Script containing functions with problem generators for the 0/1 knapsack problem.
'''

import numpy as np
from bruteforce import bruteforce
import matplotlib.pyplot as plt
from extract import *

def uniform_dist(size, minw=1, maxw=100, minv=10, maxv=300, capacity=200, seed=42, calc_optimal=False):
    """Problem generator of the 0/1 knapsack problem that draws sample values and weights according
    to a uniform distribution.

    Parameters
    ----------
    size : integer. number of items to be generated.
    minw : integer. (optional) minimum possible weight of an item.
    maxw : integer. (optional) maximum possible weight of an item.
    minv : integer. (optional) minimum possible value of an item.
    maxv : integer.  (optional) maximum possible value of an item.
    capacity : integer.  (optional) maximum weight the knapsack can hold.
    seed : integer.  (optional) seed to be fed to the random number generator.

    Returns
    -------
    values : list of item values.
    weights : list of item weights.
    capacity : maximum weight the knapsack can hold.
    """
    np.random.seed(seed)
    if minw > capacity:
        print('Minimum possible weight exceeds capacity! Adjusting capacity')
        capacity = minw + 1
    values = np.random.uniform(minv, maxv, size).round().astype(int)
    weights = np.random.uniform(minw, maxw, size).round().astype(int)
    if calc_optimal:
        solution, bestweight, optimal = bruteforce(values, weights, capacity)
    else:
        optimal = 1
    return values, weights, capacity, optimal

def normal_dist(size, mean=100, std=50, capacity=300, seed=42, calc_optimal=False):
    """Problem generator of the 0/1 knapsack problem that draws sample values and weights according
    to a gaussian distribution.

    Parameters
    ----------
    size : integer. number of items to be generated.
    mean : integer. (optional) mean of the distribution.
    std : integer. (optional) standard deviation of the distribution.
    capacity : integer.  (optional) maximum weight the knapsack can hold.
    seed : integer.  (optional) seed to be fed to the random number generator.
    Returns
    -------
    values : list of item values.
    weights : list of item weights.
    capacity : maximum weight the knapsack can hold.
    """
    np.random.seed(seed)
    values = np.random.normal(mean, std, size).round().astype(int)
    values = [abs(k) for k in values]
    weights = np.random.normal(mean, std, size).round().astype(int)
    weights = [abs(k) for k in weights]
    if min(weights) > capacity:
        print('Minimum possible weight exceeds capacity! Adjusting capacity')
        capacity = min(weights) + 1
    if calc_optimal:
        solution, bestweight, optimal = bruteforce(values, weights, capacity)
    else:
        optimal = 1
    return values, weights, capacity, optimal

def poisson_dist(size, lam=10, capacity=300, seed=42, calc_optimal=False):
    """Problem generator of the 0/1 knapsack problem that draws sample values and weights according
    to a gaussian distribution.

    Parameters
    ----------
    size : integer. number of items to be generated.
    lam : integer. (optional) lambda value.
    capacity : integer.  (optional) maximum weight the knapsack can hold.
    seed : integer.  (optional) seed to be fed to the random number generator.
    Returns
    -------
    values : list of item values.
    weights : list of item weights.
    capacity : maximum weight the knapsack can hold.
    """
    np.random.seed(seed)
    values = np.random.poisson(lam, size).round().astype(int)
    values = [abs(k) for k in values]
    weights = np.random.poisson(lam, size).round().astype(int)
    weights = [abs(k) for k in weights]
    if min(weights) > capacity:
        print('Minimum possible weight exceeds capacity! Adjusting capacity')
        capacity = min(weights) + 1
    if calc_optimal:
        solution, bestweight, optimal = bruteforce(values, weights, capacity)
    else:
        optimal = 1
    return values, weights, capacity, optimal

def triang_dist(size, minw=1, maxw=100, modew=20, minv=10, maxv=100, modev=75, capacity=300, seed=42, calc_optimal=False):
    """Problem generator of the 0/1 knapsack problem that draws sample values and weights according
    to a triangular distribution over the specified intervals.

    Parameters
    ----------
    size : integer. number of items to be generated.
    minw : integer. (optional) minimum possible weight of an item.
    maxw : integer. (optional) maximum possible weight of an item.
    modew: integer. (optional) value where the peak occurs.
    minv : integer. (optional) minimum possible value of an item.
    maxv : integer.  (optional) maximum possible value of an item.
    modev: integer. (optional) value where the peak occurs.
    capacity : integer.  (optional) maximum weight the knapsack can hold.
    seed : integer.  (optional) seed to be fed to the random number generator.
    Returns
    -------
    values : list of item values.
    weights : list of item weights.
    capacity : maximum weight the knapsack can hold.
    """
    np.random.seed(seed)
    if minw > capacity:
        print('Minimum possible weight exceeds capacity! Adjusting capacity')
        capacity = minw + 1
    values = np.random.triangular(minv, modev, maxv, size).round().astype(int)
    weights = np.random.triangular(minw, modew, maxw, size).round().astype(int)
    if calc_optimal:
        solution, bestweight, optimal = bruteforce(values, weights, capacity)
    else:
        optimal = 1
    return values, weights, capacity, optimal


### Example of usage
# values, weights, capacity, optimal = uniform_dist(1000, maxw=150, calc_optimal=False)
