'''
SIRGUEY Franck
Script containing algorithms necessary to perform
greedy approaches for the multiple knapsack problem.
'''

import os
import time
import numpy as np
from extract import read_multiknapsack, read_optimal

def b_sort(sorted_one, other_one):
    """Standard implementation of the bubble sort algorithm adapted to
    the 0/1 knapsack problem.
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
    ind = np.array(np.arange(len(sorted_one)))  # Creates registry of indexes
    for i in range(len(sorted_one)):     # Iterator goes through every item of the list
        for j in range(0, len(sorted_one) - i - 1):         # Range of the array is from 0 to len-i-1
            if sorted_one[j] > sorted_one[j + 1]:  # Swap the elements if the element found is greater than the prev.
                sorted_one[j], sorted_one[j + 1] = sorted_one[j + 1], sorted_one[j]
                other_one[j], other_one[j + 1] = other_one[j + 1], other_one[j]
                ind[j], ind[j + 1] = ind[j + 1], ind[j]
    sorted_items = np.stack((sorted_one, other_one, ind), axis=1)
    return sorted_items


def value_greedy(vals, weigh, cap:int, opt:int = 0, opt2:int=0) :
    """Implementation of a value-oriented greedy algorithm to solve
    the 0/1 knapsack problem.
    Parameters
    ----------
    vals : array-like of shape (n_samples,). List of the monetary value
            of the items to be arranged in the knapsack.
    weigh : array-like of shape (n_samples,). list of corresponding weights
            of the items to be arranged in the knapsack.
    cap:    integer. Capacity of the knapsack.
    opt:    integer. Optimal value of the items to be arranged.
    opt2:   integer. optimal value of the items to be arranged

    Returns
    -------
    knap_sol : array-like. The one-hot coded solution of the chosen items.
    """

    ### VALUE-WISE GREEDY ####
    tic = time.time()
    in_sack_w1,in_sack_v1 = 0, 0  # Empty weight and value counters
    in_sack_w2,in_sack_v2 = 0, 0  # Empty weight and value counters
    knap_sol = np.zeros(len(vals))  # Empty solution vector
    knap_sol2 =np.zeros(len(vals))
    sorted_items = np.flipud(b_sort(vals, weigh))  # Sorts the items value-wise, descending order.
    for i in range(len(sorted_items)):  # Iterates through every item
        if in_sack_w1 + sorted_items[i,1] <= capacities[0]:  # Check if the weight limit can be reached in this iter.
            in_sack_w1 += sorted_items[i,1]  # Sums weight
            in_sack_v1 += sorted_items[i,0]  # Sums value
            knap_sol[int(sorted_items[i,2])] = 1  # Found a value for the solution. Added.
        elif in_sack_w2 + sorted_items[i,1] <= capacities[1] :
            in_sack_w2+=sorted_items[i,1]
            in_sack_v2+= sorted_items[i,0]
            knap_sol2[int(sorted_items[i,2])]= 1
        else :
            knap_sol[int(sorted_items[i,2])] = 0  # Weight limit reached. Nothing changed
            knap_sol2[int(sorted_items[i,2])]=0
    exect = (time.time()-tic)*1000
    wasted_value1 = optimal1 - in_sack_v1
    wasted_value2= optimal2- in_sack_v2

    ### PRINTING SOLUTIONS ###
    print("VALUE-ORIENTED GREEDY ALGORITHM RESULTS: ")
    print("Was able to fit %d€ worth of stuff in the 1st bag. "
          "The optimal value was %d€"%(in_sack_v1, optimal1))
    print("Was able to fit %d€ worth of stuff in the 2nd bag. "
          "The optimal value was %d€"%(in_sack_v2, optimal2))
    print("Was able to fit %d kg. The 1st bag had a capacity of "
          "%d kg"%(in_sack_w1, capacities[0]))
    print("Was able to fit %d kg. The 2ng bag had a capacity of  "
          "%d kg" % (in_sack_w2, capacities[1]))
    print("Unprofited value of 1st bag: %d€" % wasted_value1)
    print("Unprofited value of 2nd bag: %d€" % wasted_value2)
    print("One-hot coded solution for the first bag : "+str(knap_sol))
    print("One-hot coded solution for the second bag : " + str(knap_sol2))
    accuracy1 = in_sack_v1/optimal1
    accuracy2 = in_sack_v2/optimal2
    accuracy_mean = (accuracy1+accuracy2)/2
    print("Accuracy: ",accuracy_mean)
    print("Execution time: ", exect, " ms")
    print()
    return knap_sol


def weight_greedy(vals, weigh, cap:int, opt:int = 0, opt2:int=0):
    """Implementation of a weight-oriented greedy algorithm to solve
    the multi knapsack problem.
    Parameters
    ----------
    vals : array-like of shape (n_samples,). List of the monetary value
            of the items to be arranged in the knapsack.
    weigh : array-like of shape (n_samples,). list of corresponding weights
            of the items to be arranged in the knapsack.
    cap:    integer. Capacity of the knapsack.
    opt:    integer. Optimal value of the items to be arranged.
    opt:    integer. Optimal value of the 2nd bag.
    Returns
    -------
    knap_sol : array-like. The one-hot coded solution of the chosen items.
    """
    ### WEIGHT-WISE GREEDY ####
    tic = time.time()
    in_sack_w1, in_sack_v1 = 0, 0 # Empty weight and value counters
    in_sack_w2, in_sack_v2 = 0, 0  # Empty weight and value counters
    knap_sol = np.zeros(len(vals))  # Empty solution vector
    knap_sol2 =np.zeros(len(vals))
    sorted_items = b_sort(weigh, vals)  # Sorts the items weight-wise, ascending order.
    for i in range(len(sorted_items)):  # Iterates through every item
        if in_sack_w1 + sorted_items[i, 0] <= capacities[0]:  # Check if the weight limit can be reached in this iter.
            in_sack_w1 += sorted_items[i, 0]  # Sums weight
            in_sack_v1 += sorted_items[i, 1]  # Sums value
            knap_sol[int(sorted_items[i, 2])] = 1  # Found a value for the solution. Added.
        elif in_sack_w2 + sorted_items[i, 0] <= capacities[1]:
            in_sack_w2 += sorted_items[i, 0]
            in_sack_v2 += sorted_items[i, 1]
            knap_sol2[int(sorted_items[i, 2])] = 1
        else:
            knap_sol[int(sorted_items[i, 2])] = 0  # Weight limit reached. Nothing changed
            knap_sol2[int(sorted_items[i, 2])] = 0
    exect = (time.time()-tic)*1000
    wasted_value1 = optimal1 - in_sack_v1
    wasted_value2 = optimal2 - in_sack_v2
    #### PRINTING SOLUTIONS ###
    print("WEIGHT-ORIENTED GREEDY ALGORITHM RESULTS: ")
    print("Was able to fit %d€ worth of stuff in the 1st bag. "
          "The optimal value was %d€" % (in_sack_v1, optimal1))
    print("Was able to fit %d€ worth of stuff in the 2nd bag. "
          "The optimal value was %d€" % (in_sack_v2, optimal2))
    print("Was able to fit %d kg. The 1st bag had a capacity of "
          "%d kg" % (in_sack_w1, capacities[0]))
    print("Was able to fit %d kg. The 2ng bag had a capacity of  "
          "%d kg" % (in_sack_w2, capacities[1]))
    print("Unprofited value of 1st bag: %d€" % wasted_value1)
    print("Unprofited value of 2nd bag: %d€" % wasted_value2)
    print("One-hot coded solution for the first bag : " + str(knap_sol))
    print("One-hot coded solution for the second bag : " + str(knap_sol2))
    accuracy1 = in_sack_v1/optimal1
    accuracy2 = in_sack_v2/optimal2
    accuracy_mean = (accuracy1+accuracy2)/2
    print("Accuracy: ",accuracy_mean)
    print("Execution time: ",exect," ms")
    print()

    return knap_sol

def fractional_greedy(vals, weigh, cap:int, opt:int = 0,opt2:int=0):
    """Implementation of a weight-oriented greedy algorithm to solve
    the multi knapsack problem.
    Parameters
    ----------
    vals : array-like of shape (n_samples,). List of the monetary value
            of the items to be arranged in the knapsack.
    weigh : array-like of shape (n_samples,). list of corresponding weights
            of the items to be arranged in the knapsack.
    cap:    integer. Capacity of the knapsack.
    opt:    integer. Optimal value of the items to be arranged.
    opt2:   integer. Optimal value of the items to be arranged.
    Returns
    -------
    knap_sol : array-like. The one-hot coded solution of the chosen items.
    """
    ### RATIO-WISE GREEDY ####
    tic = time.time()
    in_sack_w1, in_sack_v1 = 0, 0  # Empty weight and value counters
    in_sack_w2, in_sack_v2= 0,0
    knap_sol = np.zeros(len(vals))  # Empty solution vector
    knap_sol2=np.zeros(len(vals))
    val_wei_ratio = vals/weigh  # Calculates value-weight ratios of each item
    sorted_items = np.flipud(b_sort(val_wei_ratio, weights))  # Sorts the items ratio-wise, descending order.
    for i in range(len(sorted_items)):  # Iterates through every item
        if in_sack_w1 + sorted_items[i, 1] <= capacities[0]:  # Check if the weight limit can be reached in this iter.
            in_sack_w1 += sorted_items[i, 1]  # Sums weight
            index=sorted_items[i,2].astype(int)
            in_sack_v1 += values[index]  # Sums value
            knap_sol[int(sorted_items[i, 2])] = 1  # Found a value for the solution. Added.
        elif in_sack_w2 + sorted_items[i, 1] <= capacities[1]:
            in_sack_w2 += sorted_items[i, 1]
            index=sorted_items[i,2].astype(int)
            in_sack_v2 += values[index]
            knap_sol2[int(sorted_items[i, 2])] = 1
        else:
            knap_sol[int(sorted_items[i, 2])] = 0  # Weight limit reached. Nothing changed
            knap_sol2[int(sorted_items[i, 2])] = 0
    exect = (time.time()-tic)*1000

    #### PRINTING SOLUTIONS ###
    print("FRACTIONAL GREEDY ALGORITHM RESULTS: ")
    print("Was able to fit %d€ worth of stuff in the 1st bag. "
          "The optimal value was %d€" % (in_sack_v1, optimal1))
    print("Was able to fit %d€ worth of stuff in the 2nd bag. "
          "The optimal value was %d€" % (in_sack_v2, optimal2))
    print("Was able to fit %d kg. The 1st bag had a capacity of "
          "%d kg" % (in_sack_w1, capacities[0]))
    print("Was able to fit %d kg. The 2ng bag had a capacity of  "
          "%d kg" % (in_sack_w2, capacities[1]))
    print("One-hot coded solution for the first bag : " + str(knap_sol))
    print("One-hot coded solution for the second bag : " + str(knap_sol2))
    accuracy1 = in_sack_v1/optimal1
    accuracy2 = in_sack_v2/optimal2
    accuracy_mean = (accuracy1+accuracy2)/2
    print("Accuracy: ",accuracy_mean)
    print("Execution time: ",exect, " ms")
    print()
    return knap_sol

# Usage example

# Declaring item and capacity paths
items_path = 'multiple_knapsack/kp6'

# Reading the values
capacities, values, weights, s_sack1, s_sack2, optimal1, optimal2 = read_multiknapsack(items_path)
print(capacities)

# Executing the functions
knap = value_greedy(values, weights, capacities, optimal1,optimal2)
knap2 = weight_greedy(values, weights, capacities, optimal1,optimal2)
ratioknap = fractional_greedy(values, weights, capacities, optimal1,optimal2)