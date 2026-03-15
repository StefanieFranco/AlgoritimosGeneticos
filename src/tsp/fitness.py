import numpy as np

def calcular_distancia(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def fitness_function(rota, df_destinos, veiculo_obj):
    distancia_total = 0
    distancia_viagem_atual = 0
    carga_atual = 0
    penalidade = 0
    
    pos_base = (df_destinos.iloc[0]['x'], df_destinos.iloc[0]['y'])
    pos_anterior = pos_base
    
    for i, idx_destino in enumerate(rota):
        destino = df_destinos.iloc[idx_destino]
        pos_atual = (destino['x'], destino['y'])
        
        dist_trecho = calcular_distancia(pos_anterior, pos_atual)
        dist_retorno = calcular_distancia(pos_atual, pos_base)
        
        # Regra de Autonomia: volta à base se necessário
        if (distancia_viagem_atual + dist_trecho + dist_retorno) > veiculo_obj.autonomia_km:
            distancia_total += calcular_distancia(pos_anterior, pos_base)
            distancia_viagem_atual = 0
            carga_atual = 0
            pos_anterior = pos_base
            dist_trecho = calcular_distancia(pos_base, pos_atual)

        carga_atual += destino['demanda_kg']
        if carga_atual > veiculo_obj.capacidade_kg:
            penalidade += 10000
            
        if destino['prioridade'] == 2:
            penalidade += (i * 50)
            
        distancia_total += dist_trecho
        distancia_viagem_atual += dist_trecho
        pos_anterior = pos_atual
        
    distancia_total += calcular_distancia(pos_anterior, pos_base)
    return distancia_total + penalidade