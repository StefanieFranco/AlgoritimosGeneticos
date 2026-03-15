import random

def swap_mutation(individual, mutation_rate=0.05):
    new_ind = individual[:]
    for i in range(len(new_ind)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(new_ind) - 1)
            new_ind[i], new_ind[j] = new_ind[j], new_ind[i]
    return new_ind