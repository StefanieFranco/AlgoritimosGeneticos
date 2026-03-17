import random
import numpy as np

from tsp.population import create_population
from tsp.crossover import order_crossover
from tsp.mutation import swap_mutation
from tsp.fitness import fitness_function


def tournament_selection(population, fitness_scores, k=3):

    selected = random.sample(list(zip(population, fitness_scores)), k)

    selected.sort(key=lambda x: x[1])

    return selected[0][0]


def run_ga(df_destinos, veiculo,
           pop_size=100,
           generations=200,
           mutation_rate=0.05):

    num_destinos = len(df_destinos)

    population = create_population(pop_size, num_destinos)

    best_fitness_history = []

    for gen in range(generations):

        fitness_scores = [
            fitness_function(ind, df_destinos, veiculo)
            for ind in population
        ]

        new_population = []

        for _ in range(pop_size):

            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)

            child = order_crossover(parent1, parent2)

            child = swap_mutation(child, mutation_rate)

            new_population.append(child)

        population = new_population

        best_fitness = min(fitness_scores)
        best_fitness_history.append(best_fitness)

        

    best_index = np.argmin(fitness_scores)

    best_solution = population[best_index]
    print(f"Geração {gen} | Melhor fitness: {best_fitness}")

    return best_solution, best_fitness_history, population