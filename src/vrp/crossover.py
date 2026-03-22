import random

def crossover_vrp(parent1, parent2):

    cut = random.randint(1, len(parent1)-1)

    child = parent1[:cut] + parent2[cut:]

    return child