'''
GUERRA ADAMES Ariel
Script containing algorithms necessary to perform
genetic approach.
'''

import numpy as np
import random as rd
from random import randint
from leven import levenshtein
from extract import read_knapsack, read_optimal
import problem_generator as pg
import time

def c_fitness(weights, values, population, threshold):
    """Fitness function of genetic implementation of the 0/1 knapsack problem.
    Parameters
    ----------
    weights : array-like of shape (n_samples,). List of the monetary value
            of the items to be arranged in the knapsack.
    values : array-like of shape (n_samples,). List of weights of items
             to be put in the knapsack.
    population : array-like of shape (n_samples, n_individuals). List of individuals
                to be evaluated.
    threshold :  int. capacity of the knapsack, serving as threshold for this
                fitness function.
    Returns
    -------
    fitness : array-like of shape (n_individuals,). fitness of each individual in the
                population.
    """
    fitness = np.empty(population.shape[0])
    for i in range(population.shape[0]):
        S1 = np.sum(population[i] * values)
        S2 = np.sum(population[i] * weights)
        if S2 <= threshold:
            fitness[i] = S1
        else :
            fitness[i] = 0
    return fitness.astype(int)

def selection(fitness, num_parents, population):
    """Gene selection function of genetic implementation of the 0/1 knapsack problem.
    Parameters
    ----------
    fitness : array-like of shape (n_individuals,). fitness of each individual in the
                population.
    num_parents : int. Number of parents to perform genetic selection.
    population : array-like of shape (n_samples, n_individuals). List of individuals
                to be evaluated.
    Returns
    -------
    parents : array-like of shape (n_samples, n_parents). individuals selected
                for reproduction.
    """
    fitness = list(fitness)
    parents = np.empty((num_parents, population.shape[1]))
    for i in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        parents[i,:] = population[max_fitness_idx[0][0], :]
        fitness[max_fitness_idx[0][0]] = -999999
    return parents

def crossover(parents, num_offsprings):
    """Crossover function of genetic implementation of the 0/1 knapsack problem.
    Parameters
    ----------
    parents : array-like of shape (n_samples,n_parents). individuals selected
                for reproduction.
    num_offsprings : int. Number of offsprings resulting from crossover between
                 parents.
    Returns
    -------
    offsprings : array-like of shape (n_samples, n_offsprings). individuals resulting
                from reproduction.
    """
    offsprings = np.empty((num_offsprings, parents.shape[1]))
    crossover_point = int(parents.shape[1]/2)
    crossover_rate = 0.8
    i=0
    while (parents.shape[0] < num_offsprings):
        parent1_index = i%parents.shape[0]
        parent2_index = (i+1)%parents.shape[0]
        x = rd.random()
        if x > crossover_rate:
            continue
        offsprings[i,0:crossover_point] = parents[parent1_index,0:crossover_point]
        offsprings[i,crossover_point:] = parents[parent2_index,crossover_point:]
        i=+1
    return offsprings

def mutation(offsprings):
    """Mutation function of genetic implementation of the 0/1 knapsack problem.
    Parameters
    ----------
    offsprings : array-like of shape (n_samples, n_offsprings). individuals resulting
                from reproduction.
    Returns
    -------
    mutants : array-like of shape (n_samples, n_offsprings). individuals resulting
                from genetic mutation.
    """
    mutants = np.empty((offsprings.shape))
    mutation_rate = 0.4
    for i in range(mutants.shape[0]):
        random_value = rd.random()
        mutants[i,:] = offsprings[i,:]
        if random_value > mutation_rate:
            continue
        int_random_value = randint(0,offsprings.shape[1]-1)
        if mutants[i,int_random_value] == 0 :
            mutants[i,int_random_value] = 1
        else :
            mutants[i,int_random_value] = 0
    return mutants

def genetic(values, weights, capacity, optimal=1, solution_no=10):
    """Implementation of a genetic approach for the 0/1 knapsack problem.
    Parameters
    ----------
    values : array-like of shape (n_samples,). List of values of items
                to be put in the knapsack.
    weights : array-like of shape (n_samples,). List of weights of items
                to be put in the knapsack.
    capacity : int. capacity of the knapsack.
    Returns
    -------
    solution_vector : array-like of shape (n_samples,). Solution vector provided
                by the algorithm.
    fitness_history : array-like of shape (n_generations,). Fitness obtained
                over generations.
    max_value : int. Value of items put into the knapsack.
    """
    # solution_no = 10
    num_generations = 100
    item_number = np.arange(1, len(values) + 1)
    pop_size = (solution_no, item_number.shape[0])
    print(pop_size)
    print('Population size = {}'.format(pop_size))
    population = np.random.randint(2, size=pop_size)
    population = population.astype(int)
    print('Initial popultaion: \n{}'.format(population))

    solution_vector, fitness_history = [], []
    num_parents = int(pop_size[0] / 2)
    num_offsprings = pop_size[0] - num_parents
    for i in range(num_generations):
        fitness = c_fitness(weights, values, population, capacity)
        fitness_history.append(fitness)
        parents = selection(fitness, num_parents, population)
        offsprings = crossover(parents, num_offsprings)
        mutants = mutation(offsprings)
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = mutants

    print('Last generation: \n' + str(population))
    fitness_last_gen = c_fitness(weights, values, population, capacity)
    print('Fitness of the last generation: \n'+format(fitness_last_gen))
    max_fitness = np.where(fitness_last_gen == np.max(fitness_last_gen))
    solution_vector.append(population[max_fitness[0][0], :])
    max_value = np.max(fitness_last_gen)
    accuracy = (max_value/optimal)*100
    return solution_vector, max_value, accuracy

## Uncomment to test with datasets
#  Declaring item and capacity paths
filename = 'f10_l-d_kp_20_879'
items_path = 'low-dimensional/' + str(filename)
optimal_path = 'low-dimensional-optimum/' + str(filename)
solution_path = 'low-dimensional-solutions/' + str(filename)

# Reading the values
values, weights, capacity = read_knapsack(items_path)
optimal = read_optimal(optimal_path)
solution = np.loadtxt(solution_path, delimiter=',')

# Executing the function
tic = time.time()
genetic_sol, fitness_history, genetic_val = genetic(values, weights, capacity, optimal)
toc = time.time() - tic
toc = toc*1000

##  Evaluating results
found_solution = np.array(genetic_sol[0])
found_solution = np.array2string(found_solution, separator='.,', precision=None)
optimal_solution = np.array2string(solution, separator=',', precision=None)

sol_accuracy = genetic_val / optimal
edit_distance = levenshtein(optimal_solution, found_solution) - 1
print("Selected items: \n " + str(found_solution))
print('Execution time: %s miliseconds'% toc)
print("Value of the objects in the knapsack: %d €" % genetic_val)
print("Optimal value: %d €" % optimal)
print("Solution accuracy: " + str(sol_accuracy * 100))
print("Edit distance of solution: " + str(edit_distance))
