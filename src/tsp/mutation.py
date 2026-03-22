import random


def swap_mutation(individual, mutation_rate):

    individual = individual.copy()

    if random.random() < mutation_rate:

        i, j = random.sample(range(len(individual)), 2)

        individual[i], individual[j] = individual[j], individual[i]

    return individual