import numpy as np

def calcular_distancia(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def fitness_function(rota, df_destinos, veiculo):
    # --- AJUSTE PARA DATAFRAME/SERIES ---
    # Se o 'veiculo' for um DataFrame ou Series, extraímos os valores puros
    # Isso evita o erro "The truth value of a Series is ambiguous"
    is_pandas = hasattr(veiculo, 'iloc') or hasattr(veiculo, 'item')
    
    v_tipo = veiculo["tipo"].iloc[0] if hasattr(veiculo["tipo"], 'iloc') else veiculo["tipo"]
    v_velocidade = veiculo["velocidade_media"].iloc[0] if hasattr(veiculo["velocidade_media"], 'iloc') else veiculo["velocidade_media"]
    v_capacidade = veiculo["capacidade_kg"].iloc[0] if hasattr(veiculo["capacidade_kg"], 'iloc') else veiculo["capacidade_kg"]
    v_autonomia = veiculo["autonomia_km"].iloc[0] if hasattr(veiculo["autonomia_km"], 'iloc') else veiculo["autonomia_km"]
    v_custo_km = veiculo["custo_km"].iloc[0] if hasattr(veiculo["custo_km"], 'iloc') else veiculo["custo_km"]
    # ------------------------------------

    # Ponto de partida: Coordenadas da Base (ID 0)
    base = (df_destinos.iloc[0]["x"], df_destinos.iloc[0]["y"])

    pos_anterior = base
    distancia_total = 0
    carga_total = 0
    penalidade = 0
    tempo_acumulado_minutos = 0

    for ordem, idx in enumerate(rota):
        destino = df_destinos.iloc[idx]
        pos_atual = (destino["x"], destino["y"])

        # 1. Cálculos de Deslocamento (Usando a variável v_velocidade extraída)
        dist = calcular_distancia(pos_anterior, pos_atual)
        distancia_total += dist
        
        tempo_trecho = (dist / v_velocidade) * 60
        tempo_acumulado_minutos += tempo_trecho

        # 2. Carga Real e Validação de Valor
        carga_total += destino["peso_kg"]
        
        # Penalidade de Segurança (Usando v_tipo extraído)
        if destino["valor_declarado"] > 3000 and v_tipo == "moto":
            penalidade += 5000

        # 3. Prioridades
        if destino["prioridade"] == 1:
            penalidade += ordem * 200

        if destino["tipo"] == "hospital":
            penalidade += ordem * 150 

        # 4. Janela de Horário
        if destino["horario"] == "comercial" and tempo_acumulado_minutos > 480:
            penalidade += 10000 

        # Bonificação para eficiência com Moto
        # Se é prioridade, valor seguro, cabe na moto e não excedeu a capacidade ainda:
        if (destino["prioridade"] == 1 and 
            destino["valor_declarado"] <= 3000 and 
            veiculo["tipo"] == "moto" and 
            carga_total <= veiculo["capacidade_kg"]):
            
                penalidade -= 1000  # "Ganho" de fitness ao reduzir o custo total

        pos_anterior = pos_atual

    # Retorno à base
    dist_retorno = calcular_distancia(pos_anterior, base)
    distancia_total += dist_retorno
    tempo_acumulado_minutos += (dist_retorno / v_velocidade) * 60

    # 5. Penalidades de Capacidade e Autonomia (Usando v_capacidade e v_autonomia)
    if carga_total > v_capacidade:
        penalidade += 50000 

    if distancia_total > v_autonomia:
        penalidade += 50000

    # 6. Cálculo do Custo Financeiro (Usando v_custo_km)
    custo_operacional = distancia_total * v_custo_km

    return custo_operacional + penalidade