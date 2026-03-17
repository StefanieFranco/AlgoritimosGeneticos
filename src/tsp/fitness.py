import numpy as np


def calcular_distancia(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def fitness_function(rota, df_destinos, veiculo):

    base = (df_destinos.iloc[0]["x"], df_destinos.iloc[0]["y"])

    pos_anterior = base
    distancia_total = 0
    carga_total = 0
    penalidade = 0

    for ordem, idx in enumerate(rota):

        destino = df_destinos.iloc[idx]

        pos_atual = (destino["x"], destino["y"])

        dist = calcular_distancia(pos_anterior, pos_atual)
        distancia_total += dist

        carga_total += destino["demanda_kg"]

        # prioridade
        if destino["prioridade"] == 1:
            penalidade += ordem * 50

        pos_anterior = pos_atual

    distancia_total += calcular_distancia(pos_anterior, base)

    # penalidade capacidade
    if carga_total > veiculo.capacidade_kg:
        penalidade += 10000

    # penalidade autonomia
    if distancia_total > veiculo.autonomia_km:
        penalidade += 10000

    custo_total = distancia_total * veiculo.custo_km

    return custo_total + penalidade