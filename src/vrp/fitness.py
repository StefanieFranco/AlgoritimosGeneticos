import numpy as np

def calcular_distancia_vrp(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def route_cost_vrp(route, df_destinos, veiculo):

    base = (df_destinos.iloc[0]["x"], df_destinos.iloc[0]["y"])

    pos_anterior = base
    distancia = 0
    carga = 0

    for idx in route:

        destino = df_destinos.iloc[idx]

        pos_atual = (destino["x"], destino["y"])

        distancia += calcular_distancia_vrp(pos_anterior, pos_atual)

        carga += destino["demanda_kg"]

        pos_anterior = pos_atual

    distancia += calcular_distancia_vrp(pos_anterior, base)

    penalidade = 0

    if carga > veiculo["capacidade_kg"]:
        penalidade += 10000

    if distancia > veiculo["autonomia_km"]:
        penalidade += 10000

    custo = distancia * veiculo["custo_km"]

    return custo + penalidade


def fitness_function_vrp(individual, df_destinos, vehicles):

    total_cost = 0

    for i, route in enumerate(individual):

        veiculo = vehicles.iloc[i].to_dict()

        total_cost += route_cost_vrp(route, df_destinos, veiculo)

    return total_cost