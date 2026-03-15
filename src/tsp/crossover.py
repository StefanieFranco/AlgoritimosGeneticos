import random

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size
    start, end = sorted(random.sample(range(size), 2))
    child[start:end+1] = parent1[start:end+1]
    
    p2_pointer = 0
    for i in range(size):
        if child[i] == -1:
            while parent2[p2_pointer] in child:
                p2_pointer += 1
            child[i] = parent2[p2_pointer]
    return child