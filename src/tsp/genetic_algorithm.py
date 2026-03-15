import random
import pygame
from .fitness import fitness_function
from .crossover import ordered_crossover
from .mutation import swap_mutation
from src.visualization.map_routes import atualizar_tela_evolucao

def run_genetic_algorithm(df_destinos, veiculo_obj, pop_size=50, generations=100):
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    
    destinos_ids = list(df_destinos['id'].values)
    destinos_ids.remove(0)
    
    population = [random.sample(destinos_ids, len(destinos_ids)) for _ in range(pop_size)]
    best_individual = population[0]
    best_fitness = float('inf')
    historico_fitness = []

    for gen in range(generations):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return best_individual, best_fitness, historico_fitness

        # Avaliação e Elitismo
        fits = [(ind, fitness_function(ind, df_destinos, veiculo_obj)) for ind in population]
        fits.sort(key=lambda x: x[1])
        
        if fits[0][1] < best_fitness:
            best_fitness = fits[0][1]
            best_individual = fits[0][0]
        
        historico_fitness.append(best_fitness)
        atualizar_tela_evolucao(tela, df_destinos, best_individual, gen, best_fitness)

        # Evolução
        new_pop = [f[0] for f in fits[:2]]
        while len(new_pop) < pop_size:
            p1, p2 = random.sample([f[0] for f in fits[:10]], 2)
            child = ordered_crossover(p1, p2)
            new_pop.append(swap_mutation(child))
        population = new_pop

    pygame.time.delay(2000)
    pygame.quit()
    return best_individual, best_fitness, historico_fitness