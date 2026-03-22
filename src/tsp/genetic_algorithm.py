import random
import numpy as np
import matplotlib.pyplot as plt
import uuid # Para gerar IDs únicos para cada gráfico
from IPython.display import clear_output, display, update_display
from tsp.population import create_population
from tsp.crossover import order_crossover
from tsp.mutation import swap_mutation
from tsp.fitness import fitness_function
from visualization.map_routes import visualizar_no_subplot


def tournament_selection(population, fitness_scores, k=3):

    selected = random.sample(list(zip(population, fitness_scores)), k)

    selected.sort(key=lambda x: x[1])

    return selected[0][0]


def run_ga(df_destinos, veiculo,
           pop_size=100,
           generations=200,
           mutation_rate=0.05,
           patience=20,
           display_id=None,           
           visualize=True):

    num_destinos = len(df_destinos)

    population = create_population(pop_size, num_destinos)

    best_fitness_history = []
    history_v = []
    best_fitness_global = float('inf')
    generations_without_improvement = 0

    for gen in range(generations):

        fitness_scores = [
            fitness_function(ind, df_destinos, veiculo)
            for ind in population
        ]

        new_population = []
        # ELITISMO: Salva o melhor indivíduo da geração anterior direto na nova
        best_idx = np.argmin(fitness_scores)
        best_individual = population[best_idx]
        history_v.append(fitness_scores[best_idx])
        current_best_fitness = fitness_scores[best_idx]

        if current_best_fitness < best_fitness_global:
            best_fitness_global = current_best_fitness
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1

        # INTERATIVIDADE: Atualiza o gráfico a cada 10 gerações
        if visualize and gen % 1 == 0:
            #clear_output(wait=True) # Limpa a saída anterior sem "piscar" a tela
            
            # Criamos uma figura com dois subplots (Lado a lado)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
            
            # 1. Plotar o Gráfico de Evolução (Histórico) no ax1
            ax1.plot(history_v, color='green')
            ax1.set_title(f"Geração {gen} - Evolução do Custo")
            ax1.set_xlabel("Geração")
            ax1.set_ylabel("Custo Total")
            ax1.grid(True, linestyle=':', alpha=0.6)

            # 2. Plotar o Mapa no ax2 (Chamando sua função pro que criamos)
            # Nota: vamos passar o 'ax' para a função desenhar dentro do subplot
            visualizar_no_subplot(ax2, df_destinos, best_individual, veiculo, titulo=f"Mapa de Rotas - Gen {gen}")
            
            if display_id:
                update_display(fig, display_id=display_id)
            else:
                clear_output(wait=True)
                display(fig)
            
            plt.close(fig) # Exibe o quadro atual
        
        # 4. Verificação da Parada Precoce
        if generations_without_improvement >= patience:
            print(f"\n🛑 Estagnação detectada! Parando na geração {gen}.")
            print(f"O resultado não melhora há {patience} gerações.")
            break

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