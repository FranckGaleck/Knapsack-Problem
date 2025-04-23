'''
MOUDJAHED Mohamed
Script containing functions necessary to execute the
dynamic algorithm.
'''

import sys
import numpy as np
from extract import read_knapsack, read_optimal
import time
from leven import levenshtein
sys.setrecursionlimit(10**8)

'''
Programmation dynamique

Explication brève :
- Les valeurs de la matrice sont initialisées à 0
- Pour remplir une valeur dans la matrice il y'a deux situations :
  i) Le poid Lw[i] > w : On ne peut rien ajouter de plus, la valeur du dessus est reprise (M[i-1, w])
  ii) Sinon : La valeur sera le maximum entre celle du dessus (M[i-1, w]) et M[i-1, w - Lw[i]] + Lv[i]
      Pourquoi "M[i-1, w - Lw[i]] + Lv[i]" ? 
        -> Il s'agit de la valeur à la capacité maximale déjà calculée + la valeur à ajouter
 '''

def Dynamic(Lv, Lw, W, optimal):
    n = len(Lv)
    W = int(W)
    M = np.zeros((n+1, W+1))
    for i in range(1, n+1) :
        for w in range(1, W+1):
            if Lw[i-1] > w :
                M[i, w] = M[i-1, w]
            else :
                M[i, w] = max(M[i-1, w], Lv[i-1] + M[i-1, w-Lw[i-1]])
    accuracy = M[n,W]/optimal*100
    print("The best value is : ",M[n, W],"Value optimal : ",optimal, "précision :",M[n,W]/optimal*100,"%")
    return M[n, W], M, accuracy

'''
Version Top Down plus optimisée réduisant le nombre d'appels, en calculant les poids 
seulement si nécessaire.
'''
def m(i, j, M, Lw, Lv):
    if i == 0 or j <= 0 :        
        M[i, j] = 0   
        return 0

    if M[i-1, j] == -1 :#m[i-1, j] n'a pas été calculé, il faut appeler la fonction m
        M[i-1, j] = m(i-1, j, M, Lw, Lv)

    if Lw[i-1] > j :   #l'article ne peut pas tenir dans le sac
        M[i, j] = M[i-1, j]   
    else :
        if M[i-1, j-Lw[i-1]] == -1 : #m[i-1,Lw[i]] n'a pas été calculé, il faut appeler la fonction m
            M[i-1, j-Lw[i-1]] = m(i-1 , j-Lw[i-1], M, Lw, Lv)
        M[i, j] = max(M[i-1, j], M[i-1, j-Lw[i-1]] + Lv[i-1])
    return M[i, j]

def TopDown(Lv, Lw, W, optimal):
    n = len(Lv)
    W = int(W)
    M = np.ones((n+1, W+1)).dot(-1)
    m(n, W, M, Lw, Lv)
    print("The best value is : ",M[n, W],"Value optimal : ",optimal, "précision :",M[n,W]/optimal*100,"%")
    accuracy = M[n,W]/optimal*100
    return M[n, W],M, accuracy

def taken_items(M, Lw, W):
    taken = []
    n = len(Lw)
    W = int(W)

    for i in range(n, 0, -1): 
        if M[i, W] != M[i-1, W] :
            # print(M[i-1,W])
            taken.append(1)
            W -= Lw[i-1]
        else :
            taken.append(0)
    taken.reverse()
    return taken

# Declaring item and capacity paths
filename = 'f10_l-d_kp_20_879'
items_path = 'low-dimensional/'+ str(filename)
optimal_path = 'low-dimensional-optimum/' + str(filename)
solution_path = 'low-dimensional-solutions/' + str(filename)

# Reading the values
values, weights, capacity = read_knapsack(items_path)
optimal = read_optimal(optimal_path)
solution = np.loadtxt(solution_path, delimiter=',')
values = list(map(int, values))
weights = list(map(int, weights))

#  Executing functions, measuring time
ticd = time.time()
best_value_D, M = Dynamic(values, weights, capacity, optimal)
tocd = time.time()-ticd
tocd = tocd*1000

tict = time.time()
best_value_TD, M = TopDown(values, weights, capacity, optimal)
toct = time.time()-tict
toct = toct*1000

## Solution quality evaluation for the normal dynamic method
dynamic_sol = taken_items(M, weights, capacity)
found_solution = np.array(dynamic_sol)
found_solution = np.array2string(found_solution, separator='.,', precision=None)
optimal_solution = np.array2string(solution, separator=',', precision=None)

print(found_solution)
print(optimal_solution)

edit_distance = levenshtein(optimal_solution, found_solution)-1

print("Results for the normal dynamic approach")
print("Execution time: %s miliseconds" % tocd)
print("Solution vector: \n" + str(found_solution))
print("Value of the objects in the knapsack: %d €" % best_value_D)
print("Optimal value: %d €" % optimal)
print("Solution accuracy: " + str(best_value_D/optimal * 100))
print("Edit distance of solution: " + str(edit_distance))
print()


## Solution quality evaluation for the top down method
topd_sol = taken_items(M, weights, capacity)
found_solution = np.array(topd_sol)
found_solution = np.array2string(found_solution, separator='.,', precision=None)
optimal_solution = np.array2string(solution, separator=',', precision=None)

print(found_solution)
print(optimal_solution)

edit_distance = levenshtein(optimal_solution, found_solution)-1

print("Results for the top down method approach")
print("Execution time: %s miliseconds" % toct)
print("Solution vector: \n" + str(found_solution))
print("Value of the objects in the knapsack: %d €" % best_value_TD)
print("Optimal value: %d €" % optimal)
print("Solution accuracy: " + str(best_value_TD / optimal * 100))
print("Edit distance of solution: " + str(edit_distance))
print()
