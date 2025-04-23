'''
MOUDJAHED Mohamed
Script containing functions necessary to execute the
multiple knapsack version of the bruteforce algorithm.
'''

from itertools import combinations
from extract import read_multiknapsack, read_optimal
import time

# retourne une liste de toutes sommes des combinaisons
def sumcomb(a):
    combinaison = sum([list(map(list, combinations(a, i))) for i in range(len(a) + 1)], [])
    sumvalues = []
    for i in combinaison:
        sumvalues.append(sum(i))

    return sumvalues


# retourne seulement une liste de toutes les combinaisons possible
def comb(a):
    combinaison = sum([list(map(list, combinations(a, i))) for i in range(len(a) + 1)], [])

    return combinaison


# retourne 1 si les listes a et b ont une valeur commune sinon 0
def same(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return 1
    else:
        return 0


def BrutForce_MKP(Lv, Lw, W1, W2, opt1, opt2):
    # Liste des indices des objets
    O = []
    for i in range(len(Lv)):
        O.append(i)

    # calcule des poids et des valeurs
    sumweight = sumcomb(Lw)
    sumvalues = sumcomb(Lv)

    # combinaison des indices
    combobjet = comb(O)

    # On récupère toutes les combinaisons possiblent
    # ((sumweight1, sumweight2),(sumvalues1, sumvalues2))
    # En prenant bien en compte qu'on ne peut pas mettre un objet dans deux sacs
    # Puis on prend la meilleur combinaison possible

    Valmax = 0
    for sw1, sv1, co1 in zip(sumweight, sumvalues, combobjet):
        for sw2, sv2, co2 in zip(sumweight, sumvalues, combobjet):
            if (same(co1, co2) == 0) and sw1 <= W1 and sw2 <= W2 and sv1 + sv2 > Valmax:
                Valmax = sv1 + sv2
                indices1 = co1
                indice2 = co2
                in_sack_v1 = sv1
                in_sack_v2 = sv2
                in_sack_w1 = sw1
                in_sack_w2 = sw2

    def indices(comb):
        taken = []
        for i in range(len(Lv)):
            if i in comb:
                taken.append(1)
            else:
                taken.append(0)
        return taken

    taken1 = indices(co1)
    taken2 = indices(co2)

    #### PRINTING SOLUTIONS ###
    print("WEIGHT-ORIENTED BRUTFORCE ALGORITHM RESULTS: ")
    print("Was able to fit %d€ worth of stuff in the 1st bag. "
          "The optimal value was %d€" % (in_sack_v1, optimal1))
    print("Was able to fit %d€ worth of stuff in the 2nd bag. "
          "The optimal value was %d€" % (in_sack_v2, optimal2))
    print("Was able to fit %d kg. The 1st bag had a capacity of "
          "%d kg" % (in_sack_w1, W1))
    print("Was able to fit %d kg. The 2ng bag had a capacity of  "
          "%d kg" % (in_sack_w2, W2))
    print("One-hot coded solution for the first bag : " + str(taken1))
    print("One-hot coded solution for the second bag : " + str(taken2))
    print("Best value for 2 bags :" + Valmax)
    print()

    return Valmax


# Declaring item and capacity paths
items_path = 'multiple_knapsack/kp1'
# Reading the values
capacities, values, weights, s_sack1, s_sack2, optimal1, optimal2 = read_multiknapsack(items_path)

# Calling the value greedy
values = list(map(int, values))
weights = list(map(int, weights))

tic = time.time()
knap = BrutForce_MKP(values, weights, s_sack1, s_sack2, optimal1, optimal2)
toc = time.time() - tic
print("Execution time: ", toc)