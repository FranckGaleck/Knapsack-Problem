'''
SIRGUEY Franck
Script containing algorithms necessary to perform
bruteforce approach.
'''

import time
import numpy as np
from extract import read_knapsack, read_optimal

def binaire(number):
    """
    Parameters
    ----------
    sorted_one : array-like of shape (n_samples,). The feature which
                will drive the sorting algorithm in the knapsack
                (weights or values).
    other_one : array-like of shape (n_samples,). The other feature.
    Returns
    -------
    sorted_items : array-like. The sorted list of items.
    """
    q = -1
    resul = []
    while q != 0:
        q = number // 2
        r = number % 2
        resul.append(r)
        number = q
    return resul


def val(bestChoice):
    """
    Parameters
    ----------
    sorted_one : array-like of shape (n_samples,). The feature which
                will drive the sorting algorithm in the knapsack
                (weights or values).
    other_one : array-like of shape (n_samples,). The other feature.
    Returns
    -------
    sorted_items : array-like. The sorted list of items.
    """
    sum = 0
    for k in range(capacity):
        if (bestChoice[k] == 1):
            sum = sum + values[k]
    return sum


def bruteforce(values, weight, capacity):
    """Bruteforce implementation of the 0/1 knapsack problem.
    Parameters
    ----------
    values : array-like of shape (n_samples,). List of values of items
                to be put in the knapsack.
    weight : array-like of shape (n_samples,). List of weights of items
                to be put in the knapsack.
    capacity : maximum weight possibly held by the knapsack.
    Returns
    -------
    bestChoice : array-like of shape (n_samples,). One-hot coded list of
                    selected items
    bestweight : int. Total weight of selected items.
    bestval : int. Total value of selected items.
    """
    bestChoice = []
    bestval, bestweight= 0, 0
    a = np.zeros(len(values))

    for i in range(0, pow(2, len(values))):  # for 1 to 2^n
        tab=binaire(i)  # for obtain the binary number of i
        tempval = 0  # will stock the value
        tempweight = 0  # will stock the weight
        while (len(tab)!=len(a)) : # we will have table : 1 the object in the bag 0 not in the bag
            tab.insert(0,0)
        a=tab
        for k in range(len(values)) :
            if(tab[k]==1) : #the object is in bag
                tempval = values[k] + tempval
                tempweight = tempweight + weight[k]
            if(tempweight<=capacity and tempval>bestval):
                bestChoice=a
                bestval=tempval
                bestweight=tempweight

    return bestChoice, bestweight, bestval

###### USAGE EXAMPLE ######
# Declaring item and capacity paths

filename = 'f10_l-d_kp_20_879'
items_path = 'low-dimensional/' + str(filename)
optimal_path = 'low-dimensional-optimum/' + str(filename)

# Reading the values
values, weights, capacity = read_knapsack(items_path)
optimal = read_optimal(optimal_path)

tic = time.time()
solution, bestweight, bestval = bruteforce(values, weights, capacity)
toc = time.time()-tic
toc = toc*1000

print("Execution time: %s miliseconds" % toc)
print("Solution vector: \n" + str(solution))
print("Value of the objects in the knapsack: %d €" % bestval)
print("Optimal value: %d €" % optimal)