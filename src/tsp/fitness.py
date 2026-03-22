import numpy as np

def calcular_distancia(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def fitness_function(rota, df_destinos, veiculo):
    # Ponto de partida: Coordenadas da Base (ID 0)
    base = (df_destinos.iloc[0]["x"], df_destinos.iloc[0]["y"])

    pos_anterior = base
    distancia_total = 0
    carga_total = 0
    penalidade = 0
    tempo_acumulado_minutos = 0
    
    # Velocidade vinda do CSV (km/h)
    velocidade = veiculo["velocidade_media"]

    for ordem, idx in enumerate(rota):
        # Localiza o destino no DataFrame processado
        destino = df_destinos.iloc[idx]
        pos_atual = (destino["x"], destino["y"])

        # 1. Cálculos de Deslocamento
        dist = calcular_distancia(pos_anterior, pos_atual)
        distancia_total += dist
        
        # Tempo = (Distância / Velocidade) * 60 para converter para minutos
        tempo_trecho = (dist / velocidade) * 60
        tempo_acumulado_minutos += tempo_trecho

        # 2. Carga Real e Validação de Valor
        carga_total += destino["peso_kg"]
        
        # Penalidade de Segurança: Carga valiosa em moto é risco de roubo/dano
        if destino["valor_declarado"] > 3000 and veiculo["tipo"] == "moto":
            penalidade += 5000

        # 3. Prioridades (Hospitais e Nível de Urgência)
        # Quanto mais tarde (ordem maior) um hospital crítico é visitado, maior a penalidade
        if destino["prioridade"] == 1:
            penalidade += ordem * 200

        if destino["tipo"] == "hospital":
            penalidade += ordem * 150 # Aumentei um pouco o peso para hospitais

        # 4. Janela de Horário Realista
        # Se o destino for "comercial" e o tempo acumulado passar de 8h (480 min)
        if destino["horario"] == "comercial" and tempo_acumulado_minutos > 480:
            penalidade += 10000 # Penalidade pesada por encontrar local fechado

        pos_anterior = pos_atual

    # Retorno à base (essencial para o problema do Caixeiro Viajante)
    dist_retorno = calcular_distancia(pos_anterior, base)
    distancia_total += dist_retorno
    tempo_acumulado_minutos += (dist_retorno / velocidade) * 60

    # 5. Penalidades de Capacidade e Autonomia (Restrições Físicas)
    if carga_total > veiculo["capacidade_kg"]:
        penalidade += 50000 # Valor altíssimo para descartar essa rota

    if distancia_total > veiculo["autonomia_km"]:
        penalidade += 50000

    # 6. Cálculo do Custo Financeiro
    custo_operacional = distancia_total * veiculo["custo_km"]

    # O objetivo do Algoritmo Genético será MINIMIZAR este retorno
    return custo_operacional + penalidade