import random

def create_individual_vrp(num_destinos, num_vehicles):

    destinos = list(range(1, num_destinos))
    random.shuffle(destinos)

    routes = [[] for _ in range(num_vehicles)]

    for i, destino in enumerate(destinos):
        routes[i % num_vehicles].append(destino)

    return routes


def create_population_vrp(pop_size, num_destinos, num_vehicles):

    population = []

    for _ in range(pop_size):
        individual = create_individual_vrp(num_destinos, num_vehicles)
        population.append(individual)

    return population

def population_diversity_vrp(population):
    return len(set(tuple(ind) for ind in population)) / len(population)