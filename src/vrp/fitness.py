import numpy as np

def calcular_distancia_vrp(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def route_cost_vrp(route, df_destinos, veiculo):
    # Ponto de partida: Coordenadas da Base (Sempre ID 0 no seu CSV)
    base = (df_destinos.iloc[0]["x"], df_destinos.iloc[0]["y"])
    
    pos_anterior = base
    distancia_total = 0
    carga_total = 0
    penalidade = 0
    tempo_acumulado_minutos = 0
    
    # Extrai a velocidade do veículo (certifique-se que existe no CSV/DataFrame)
    velocidade = veiculo.get("velocidade_media", 40) # Default 40 se não houver

    for ordem, idx in enumerate(route):
        # Localiza o destino no DataFrame (que já deve estar com o merge dos pesos)
        destino = df_destinos.iloc[idx]
        pos_atual = (destino["x"], destino["y"])

        # 1. Cálculos de Deslocamento e Tempo
        dist = calcular_distancia_vrp(pos_anterior, pos_atual)
        distancia_total += dist
        
        # Tempo = (Distância / Velocidade) * 60
        tempo_trecho = (dist / velocidade) * 60
        tempo_acumulado_minutos += tempo_trecho

        # 2. Carga e Valor Declarado
        carga_total += destino["peso_kg"]
        
        # Penalidade de Segurança: Carga valiosa em moto
        if destino["valor_declarado"] > 3000 and veiculo["tipo"] == "moto":
            penalidade += 5000

        # 3. Prioridades e Tipos de Destino
        # Penaliza deixar hospitais ou urgências para o final da rota individual
        if destino["prioridade"] == 1:
            penalidade += ordem * 200
        
        if destino["tipo"] == "hospital":
            penalidade += ordem * 150

        # 4. Janela de Horário Realista (480 min = 8h de turno)
        if destino["horario"] == "comercial" and tempo_acumulado_minutos > 480:
            penalidade += 10000 

        pos_anterior = pos_atual

    # Retorno à base
    dist_retorno = calcular_distancia_vrp(pos_anterior, base)
    distancia_total += dist_retorno
    tempo_acumulado_minutos += (dist_retorno / velocidade) * 60

    # 5. Penalidades de Capacidade e Autonomia (Hard Constraints)
    if carga_total > veiculo["capacidade_kg"]:
        penalidade += 50000 

    if distancia_total > veiculo["autonomia_km"]:
        penalidade += 50000
   
    if destino["horario"] == "comercial" and veiculo["tipo"] == "caminhao":
        penalidade += 50000
    
    # Bonificação para eficiência com Moto
    # Se é prioridade, valor seguro, cabe na moto e não excedeu a capacidade ainda:
    if (destino["prioridade"] == 1 and 
        destino["valor_declarado"] <= 3000 and 
        veiculo["tipo"] == "moto" and 
        carga_total <= veiculo["capacidade_kg"]):
    
            penalidade -= 1000  # "Ganho" de fitness ao reduzir o custo total

     # 6. Custo Operacional da Rota
    custo_rota = (distancia_total * veiculo["custo_km"]) + penalidade
    
    return custo_rota

def fitness_function_vrp(individual, df_destinos, vehicles):
    """
    individual: Lista de listas, onde cada sublista é a rota de um veículo.
    Ex: [[1, 4, 3], [2, 5], []] -> Veículo 0 faz hospitais 1,4,3; Veículo 1 faz 2,5...
    """
    total_cost = 0

    for i, route in enumerate(individual):
        # Evita processar veículos sem rota
        if not route:
            continue
            
        # Pega as specs do veículo correspondente à rota i
        veiculo = vehicles.iloc[i].to_dict()

        # Soma o custo desta rota específica ao custo total do indivíduo
        total_cost += route_cost_vrp(route, df_destinos, veiculo)

    return total_cost