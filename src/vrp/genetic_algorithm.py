import numpy as np
import random
import matplotlib.pyplot as plt

from vrp.population import create_population_vrp
from vrp.crossover import crossover_vrp
from vrp.mutation import mutate_vrp
from vrp.fitness import fitness_function_vrp


def tournament_selection_vrp(population, fitness_scores, k=3):

    selected = random.sample(list(zip(population, fitness_scores)), k)

    selected.sort(key=lambda x: x[1])

    return selected[0][0]


def run_ga_vrp(df_destinos, vehicles,
           pop_size=100,
           generations=200,
           mutation_rate=0.05):

    num_destinos = len(df_destinos)
    num_vehicles = len(vehicles)

    population = create_population_vrp(pop_size, num_destinos, num_vehicles)

    history = []

    for gen in range(generations):

        fitness_scores = [
            fitness_function_vrp(ind, df_destinos, vehicles)
            for ind in population
        ]

        new_population = []

        for _ in range(pop_size):

            p1 = tournament_selection_vrp(population, fitness_scores)
            p2 = tournament_selection_vrp(population, fitness_scores)

            child = crossover_vrp(p1, p2)

            child = mutate_vrp(child, mutation_rate)

            new_population.append(child)

        population = new_population

        best = min(fitness_scores)

        history.append(best)
        
    best_index = np.argmin(fitness_scores)
    print(f"Geração {gen} | Best: {best}")

    return population[best_index], history, population

def plot_routes_vrp(routes, df):

    for route in routes:

        xs = [df.iloc[i]["x"] for i in route]
        ys = [df.iloc[i]["y"] for i in route]

        plt.plot(xs, ys, marker="o")

    plt.scatter(df["x"], df["y"])

    plt.title("Rotas Otimizadas")

    plt.show()