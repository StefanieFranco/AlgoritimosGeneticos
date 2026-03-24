import numpy as np

def calcular_distancia_vrp(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def route_cost_vrp(route, df_destinos, veiculo):
    base = (df_destinos.iloc[0]["x"], df_destinos.iloc[0]["y"])
    
    pos_anterior = base
    distancia_total = 0
    carga_atual_no_veiculo = 0 # Carga da "viagem" atual
    carga_total_entregue = 0    # Carga total do dia
    penalidade = 0
    tempo_acumulado_minutos = 0
    
    velocidade = veiculo.get("velocidade_media", 40)
    capacidade_max = veiculo["capacidade_kg"]

    for ordem, idx in enumerate(route):
        # Localiza o destino no DataFrame (que já deve estar com o merge dos pesos)
        destino = df_destinos.iloc[idx]
        pos_atual = (destino["x"], destino["y"])
        peso_pedido = destino["peso_kg"]

        # --- LÓGICA DE REABASTECIMENTO (FRAGMENTAÇÃO) ---
        # Se o peso do próximo hospital estourar a capacidade, 
        # o veículo PRECISA voltar na base antes de ir até ele.
        if carga_atual_no_veiculo + peso_pedido > capacidade_max:
            # 1. Distância: atual -> base -> atual (Simulando ida ao CD e volta ao ponto)
            dist_ate_base = calcular_distancia_vrp(pos_anterior, base)
            dist_da_base_ao_destino = calcular_distancia_vrp(base, pos_atual)
            
            distancia_total += (dist_ate_base + dist_da_base_ao_destino)
            # Zeramos a carga porque ele reabasteceu na base
            carga_atual_no_veiculo = peso_pedido 
            
            # Penalidade de tempo: Adiciona o tempo de deslocamento + 15 min de carga
            tempo_extra = ((dist_ate_base + dist_da_base_ao_destino) / velocidade) * 60 + 15
            tempo_acumulado_minutos += tempo_extra
        else:
            # Viagem normal entre pontos
            dist = calcular_distancia_vrp(pos_anterior, pos_atual)
            distancia_total += dist
            tempo_acumulado_minutos += (dist / velocidade) * 60
            carga_atual_no_veiculo += peso_pedido

        # --- 2. Acumuladores e Regras de Negócio ---
        carga_total_entregue += peso_pedido
                        
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

        carga_total_entregue += peso_pedido
        pos_anterior = pos_atual

    # Retorno à base
    dist_retorno = calcular_distancia_vrp(pos_anterior, base)
    distancia_total += dist_retorno
    tempo_acumulado_minutos += (dist_retorno / velocidade) * 60
    
    if distancia_total > veiculo["autonomia_km"]:
        penalidade += 50000
   
    if destino["horario"] == "comercial" and veiculo["tipo"] == "caminhao":
        penalidade += 50000
    
    # Bonificação para eficiência com Moto
    # Se é prioridade, valor seguro, cabe na moto e não excedeu a capacidade ainda:
    if (destino["prioridade"] == 1 and 
        destino["valor_declarado"] <= 3000 and 
        veiculo["tipo"] == "moto"):    
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