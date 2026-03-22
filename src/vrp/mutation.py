import random

def mutate_vrp(individual, mutation_rate):

    if random.random() > mutation_rate:
        return individual

    routes = [r.copy() for r in individual]

    v1, v2 = random.sample(range(len(routes)), 2)

    if routes[v1] and routes[v2]:

        i = random.randrange(len(routes[v1]))
        j = random.randrange(len(routes[v2]))

        routes[v1][i], routes[v2][j] = routes[v2][j], routes[v1][i]

    return routes