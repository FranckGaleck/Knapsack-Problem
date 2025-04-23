'''
MOUDJAHED Mohamed
Script containing functions necessary to execute the
FPTAS algorithm.
'''

import numpy as np
from extract import read_knapsack, read_optimal
from math import *
from leven import levenshtein
import time

def m(i, j, M, Lw, Lv) :
    if i == 0 or j <= 0 :        
        M[i, j] = 0   
        return 0
    
    #m[i-1, j] n'a pas été calculé, il faut appeler la fonction m          
    if M[i-1, j] == -1 :
        M[i-1, j] = m(i-1, j, M, Lw, Lv)

    #l'article ne peut pas tenir dans le sac
    if Lw[i-1] > j :                            
        M[i, j] = M[i-1, j]   
    else :
    #m[i-1,Lw[i]] n'a pas été calculé, il faut appeler la fonction m
        if M[i-1, j-Lw[i-1]] == -1 :           
            M[i-1, j-Lw[i-1]] = m (i-1 , j-Lw[i-1], M, Lw, Lv)    
        M[i, j] = max(M[i-1, j], M[i-1, j-Lw[i-1]] + Lv[i-1]) 
    return M[i, j]

def taken_items(M, Lw, W):
    taken = []
    n = len(Lw)
    W = int(W)

    for i in range(n, 0, -1): 
        if M[i, W] != M[i-1, W] :
            taken.append(1)
            W -= Lw[i-1]
        else :
            taken.append(0)
    taken.reverse()
    return taken


#La précision de votre algorithme dépendra de sigma !
def Poly(epsilon, Lv, Lw, W, optimal) :
    n = len(Lv)
    W = int(W)

    #La valeur maximale 
    maxVal = max(Lv) 

    #Facteur d'ajustement
    k = (maxVal * epsilon) / n

    #Initialisation de la matrie
    M = np.ones((n+1, W+1)).dot(-1) 

    #On arrondit toutes les valeurs de v sur le multiple de  k juste au dessus
    Lv2 = [ceil(i/k) for i in Lv]

    #On applique l'approche dynamique avec notre nouvelle liste de valeur
    m(n, W, M, Lw, Lv2)

    #On reprends les bonnes valeurs de la liste de valeurs originale qui ont été sélectionnées
    taken = taken_items(M, Lw, W)

    somme=0
    for i in range(len(taken)) :
        if taken[i] == 1 :
            somme += Lv[i]

    precision = somme/optimal*100
    print("The best value is : ", M[n, W],"Value optimal : ", optimal, "précision :", precision, "%")

    return somme, M, precision


################################################
#                    TEST                      #
################################################

# # Declaring item and capacity paths
# filename = 'f10_l-d_kp_20_879'
# items_path = 'low-dimensional/' + str(filename)
# optimal_path = 'low-dimensional-optimum/' + str(filename)
# solution_path = 'low-dimensional-solutions/' + str(filename)
#
# # Reading the values
# values, weights, capacity = read_knapsack(items_path)
# optimal = read_optimal(optimal_path)
# solution = np.loadtxt(solution_path, delimiter=',')
# values = list(map(int, values))
# weights = list(map(int, weights))
#
# # Executing the function
# tic = time.time()
# profit, M, accuracy = Poly(0.5, values, weights, capacity, optimal)
# toc = time.time()-tic
# toc = toc*1000
#
# poly_res = taken_items(M, weights, capacity)
#
# ## Solution quality evaluation
# found_solution = np.array(poly_res)
# found_solution = np.array2string(found_solution, separator='.,', precision=None)
# optimal_solution = np.array2string(solution, separator=',', precision=None)
#
# print(found_solution)
# print(optimal_solution)
#
# edit_distance = levenshtein(optimal_solution, found_solution)-1
#
# print("Execution time: %s miliseconds" % toc)
# print("Solution vector: \n" + str(found_solution))
# print("Value of the objects in the knapsack: %d €" % profit)
# print("Optimal value: %d €" % optimal)
# print("Solution accuracy: " + str(accuracy))
# print("Edit distance of solution: " + str(edit_distance))
# print()