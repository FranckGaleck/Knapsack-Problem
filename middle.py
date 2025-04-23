'''
MOUDJAHED Mohamed
Script containing functions necessary to execute the
meet in the middle algorithm.
'''

from itertools import combinations
from extract import read_knapsack, read_optimal
import numpy as np
import time
from leven import levenshtein

def comb(a) :
    combinaison = sum([list(map(list, combinations(a, i))) for i in range(len(a) + 1)], [])
    sumvalues = []
    for i in combinaison :
        sumvalues.append(sum(i))

    #retourne une liste de toutes les combinaisons possibles
    #et une liste de la somme de chaque combinaison
    return combinaison, sumvalues

def Middle(Lv, Lw, W, optimal) :
    indices = []
    #On récupère les indices
    for i in range(len(Lw)):
        indices.append(i)

    #On divise notre ensemble d'éléments en deux ensembles d'éléments A et B
    ALw,ALv = [Lw[:2], Lv[:2]]
    BLw,BLv = [Lw[2:], Lv[2:]]
    #On divise nos indices en deux
    indices1 = indices[:2]
    indices2 = indices[2:]
    
    #calcule des poids et des valeurs de tous les sous-ensembles de chaque ensemble
    Acomweight,Asumweight = comb(ALw)
    Acombvalues,Asumvalues = comb(ALv)

    Bcomweight,Bsumweight = comb(BLw)
    Bcombvalues,Bsumvalues = comb(BLv)

    #On récupère la combinaisons de nos indices
    indicesA,s1 = comb(indices1)
    indicesB,s2 = comb(indices2)
    
  
    #On cherche à trouver le sous-ensemble de B de plus grande valeur 
    #de sorte que le poids combiné est inférieur à W
    max = 0
    SacV = []
    SacD = []
    for Aw,Av,Ai in zip(Asumweight, Asumvalues, indicesA) :
        for Bw,Bv,Bi in zip(Bsumweight, Bsumvalues, indicesB) :
            if (Bv+Av) > max and (Bw+Aw) <= W :
                max = Bv+Av
                maxindices = Ai + Bi

    taken = []
    for i in range(len(Lv)):
        if i in maxindices:
            taken.append(1)
        else :
            taken.append(0)
    accuracy = (max/optimal)*100
    print("The best value is : ",max,"Value optimal : ",optimal, "précision :",max/optimal*100,"%")
    print(taken)

    return max, taken, accuracy

# Declaring item and capacity paths
filename = 'f10_l-d_kp_20_879'
items_path = 'low-dimensional/' + str(filename)
optimal_path = 'low-dimensional-optimum/' + str(filename)
solution_path = 'low-dimensional-solutions/' + str(filename)

# Reading the values
values, weights, capacity = read_knapsack(items_path)
optimal = read_optimal(optimal_path)
solution = np.loadtxt(solution_path, delimiter=',')
values = list(map(int, values))
weights = list(map(int, weights))

#  Executing functions, measuring time
tic = time.time()
profit, middle_sol = Middle(values, weights, capacity, optimal)
toc = time.time()-tic
toc = toc*1000

## Solution quality evaluation for the normal dynamic method
found_solution = np.array(middle_sol)
found_solution = np.array2string(found_solution, separator='.,', precision=None)
optimal_solution = np.array2string(solution, separator=',', precision=None)

print(found_solution)
print(optimal_solution)

edit_distance = levenshtein(optimal_solution, found_solution)-1

print("Results for the normal dynamic approach")
print("Execution time: %s miliseconds" % toc)
print("Solution vector: \n" + str(found_solution))
print("Value of the objects in the knapsack: %d €" % profit)
print("Optimal value: %d €" % optimal)
print("Solution accuracy: " + str(profit/optimal * 100))
print("Edit distance of solution: " + str(edit_distance))
print()
