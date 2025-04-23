'''
SIRGUEY Franck
Script containing algorithms necessary to perform
randomized approach.
'''

import random
import numpy as np
import time
from leven import levenshtein
from extract import read_knapsack, read_optimal

#param : nombre d'itération, faire deux listes, une autre listes avec n random par exemple le premier ->4 k[4]->1
# boucle n -> qui va faire le truc random

def randomize(values,weight,capacity,optimal,iter=1000) :
    """Naïve random implementation of the 0/1 knapsack problem.
    Parameters
    ----------
    values : array-like of shape (n_samples,). List of values of items
                to be put in the knapsack.
    weight : array-like of shape (n_samples,). List of weights of items
                to be put in the knapsack.
    capacity : maximum weight possibly held by the knapsack.
    iter : int. number of random iterations to test.
    Returns
    -------
    bestChoice : array-like of shape (n_samples,). One-hot coded list of
                    selected items
    bestweight : int. Total weight of selected items.
    bestval : int. Total value of selected items.
    """
    # creation de la variable qui renverra le meilleur choix
    bestChoice = []
    bestValue, bestweight = 0, 0

    for tour in range(iter):
        ran = random.sample(range(len(values)), len(values))  # liste de nombre aléatoire de taille n,corresponds a indice du tableau
        tempweight, tempvalue = 0, 0  # creation des variables temporaire de poids,valeur
        a = np.zeros(len(values))  # initialisation de notre liste a, servira de liste temporaire qui conservera la meilleur chemin

        for i in range(0,len(values)-1):  #boucle qui va parcourir tout les elem de ma liste ran
            j = ran[i]  #j sera égale a l'indice renvoyer dans la liste de random
            tempweight = tempweight + weight[j]
            if(tempweight<capacity) :
                a[j] = 1  #on le met dans le sac
                tempvalue = tempvalue+values[j]  #on ajoute la valeur de j
            elif bestValue < tempvalue:
                bestWeight = tempweight - weight[j]  #on soustrait le poids mis en trop et on l'attribue a notre poids final
                bestValue = tempvalue  #on attribue la valeur finale
                bestChoice = a  #bestChoice deviens a

    print(bestValue, bestChoice, bestWeight, optimal)
    accuracy = bestValue/optimal
    print("Accuracy : ", accuracy)
    return bestChoice, bestWeight, accuracy


### Usage exmaple

#  Declaring item and capacity paths
filename = 'f10_l-d_kp_20_879'
items_path = 'low-dimensional/'+ str(filename)
optimal_path = 'low-dimensional-optimum/' + str(filename)
solution_path = 'low-dimensional-solutions/' + str(filename)

# Reading the values
values, weights, capacity = read_knapsack(items_path)
optimal = read_optimal(optimal_path)
solution = np.loadtxt(solution_path, delimiter=',')

tic = time.time()
rand_res, bestweight, profit = randomize(values, weights, capacity, 10000)
toc = time.time()-tic
toc = toc*1000

## Evaluating results
found_solution = np.array(rand_res)
found_solution = np.array2string(found_solution, separator=',', precision=None)
optimal_solution = np.array2string(solution, separator=',', precision=None)

sol_accuracy = profit/optimal
edit_distance = levenshtein(optimal_solution, found_solution)

print("Execution time: %s miliseconds" % toc)
print("Solution vector: \n" + str(rand_res))
print("Value of the objects in the knapsack: %d €" % profit)
print("Optimal value: %d €" % optimal)
print("Solution accuracy: " + str(sol_accuracy*100))
print("Edit distance of solution: " + str(edit_distance))
print()