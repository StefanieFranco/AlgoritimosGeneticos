import random

def create_individual(num_destinos):
    """
    Cria uma rota aleatória.
    """
    rota = list(range(1, num_destinos))  # ignorando a base (0)
    random.shuffle(rota)
    return rota


def create_population(pop_size, num_destinos):
    """
    Gera a população inicial.
    """
    population = []

    for _ in range(pop_size):
        individual = create_individual(num_destinos)
        population.append(individual)

    return population

def population_diversity(population):
    unique_individuals = len(set(tuple(ind) for ind in population))
    return unique_individuals / len(population)