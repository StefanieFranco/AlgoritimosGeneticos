import random

def order_crossover(parent1, parent2):

    size = len(parent1)

    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size

    # copia parte do parent1
    child[start:end] = parent1[start:end]

    # preenche com genes do parent2
    p2_index = 0

    for i in range(size):

        if child[i] is None:

            while parent2[p2_index] in child:
                p2_index += 1

            child[i] = parent2[p2_index]

    return child