import numpy as np
import random
import matplotlib.pyplot as plt
import uuid # Para gerar IDs únicos para cada gráfico
from IPython.display import clear_output, display, update_display
from vrp.population import create_population_vrp
from vrp.crossover import crossover_vrp
from vrp.mutation import mutate_vrp
from vrp.fitness import fitness_function_vrp
from visualization.map_routes import visualizar_no_subplot


def tournament_selection_vrp(population, fitness_scores, k=3):

    selected = random.sample(list(zip(population, fitness_scores)), k)

    selected.sort(key=lambda x: x[1])

    return selected[0][0]


def run_ga_vrp(df_destinos, vehicles, pop_size=100, generations=200, mutation_rate=0.05, patience=20, display_id=None, visualize=True):
    num_destinos = len(df_destinos)
    num_vehicles = len(vehicles)
    
    # 1. População inicial
    population = create_population_vrp(pop_size, num_destinos, num_vehicles)
    history = []
    history_v = []
    best_fitness_global = float('inf')
    generations_without_improvement = 0

    for gen in range(generations):
        # 2. Cálculo do Fitness de toda a população atual
        fitness_scores = [
            fitness_function_vrp(ind, df_destinos, vehicles) 
            for ind in population
        ]

        new_population = []

        # ELITISMO: Salva o melhor indivíduo da geração anterior direto na nova
        best_idx = np.argmin(fitness_scores)
        best_individual = population[best_idx]
        history_v.append(fitness_scores[best_idx])
        new_population.append(population[best_idx])
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
            visualizar_no_subplot(ax2, df_destinos, best_individual, vehicles, titulo=f"Mapa de Rotas - Gen {gen}")
            
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

        # 3. Loop para criar os novos filhos até encher a nova população
        while len(new_population) < pop_size:
            p1 = tournament_selection_vrp(population, fitness_scores)
            p2 = tournament_selection_vrp(population, fitness_scores)

            child = crossover_vrp(p1, p2)
            child = mutate_vrp(child, mutation_rate)

            # --- AQUI ENTRA A VALIDAÇÃO ---
            # Verificamos se o filho gerado é válido (não repete hospitais e não esquece nenhum)
            e_valido, motivo = validar_individuo_vrp(child, num_destinos - 1)
            
            if e_valido:
                new_population.append(child)
            else:
                # Se for inválido, podemos tentar gerar outro ou aplicar uma penalidade
                # No VRP, o ideal é que o crossover já gere filhos válidos, 
                # mas essa trava garante que o erro não passe.
                continue 
        
        population = new_population
        best_fitness = min(fitness_scores)
        history.append(best_fitness)

        if gen % 10 == 0:
            print(f"Geração {gen} | Melhor Fitness: {best_fitness:.2f}")

    best_index = np.argmin(fitness_scores)
    return population[best_index], history, population


def validar_individuo_vrp(individual, total_esperado_hospitais):
    # 'individual' é [[rota_moto1], [rota_moto2], [rota_caminhao]]
    
    # Transforma todas as rotas em uma lista única (flatten)
    todos_destinos = [dest for rota in individual for dest in rota]
    
    # 1. Verificar Duplicados
    if len(todos_destinos) != len(set(todos_destinos)):
        return False, "Hospital visitado por mais de um veículo!"
        
    # 2. Verificar se algum hospital ficou de fora
    # (Excluímos o ID 0 pois ele é a Base e não entra na lista de visitas)
    if len(todos_destinos) != total_esperado_hospitais:
        return False, "Algum hospital não recebeu entrega!"
        
    return True, "OK"

def plot_routes_vrp(routes, df):

    for route in routes:

        xs = [df.iloc[i]["x"] for i in route]
        ys = [df.iloc[i]["y"] for i in route]

        plt.plot(xs, ys, marker="o")

    plt.scatter(df["x"], df["y"])

    plt.title("Rotas Otimizadas")

    plt.show()