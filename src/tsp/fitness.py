import numpy as np

def calcular_distancia(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def fitness_function(rota, df_destinos, veiculo):
    # --- 1. EXTRAÇÃO DE PARÂMETROS DO VEÍCULO (PROTEÇÃO PANDAS) ---
    v_tipo = veiculo["tipo"].iloc[0] if hasattr(veiculo["tipo"], 'iloc') else veiculo["tipo"]
    v_velocidade = veiculo["velocidade_media"].iloc[0] if hasattr(veiculo["velocidade_media"], 'iloc') else veiculo["velocidade_media"]
    v_capacidade = veiculo["capacidade_kg"].iloc[0] if hasattr(veiculo["capacidade_kg"], 'iloc') else veiculo["capacidade_kg"]
    v_autonomia = veiculo["autonomia_km"].iloc[0] if hasattr(veiculo["autonomia_km"], 'iloc') else veiculo["autonomia_km"]
    v_custo_km = veiculo["custo_km"].iloc[0] if hasattr(veiculo["custo_km"], 'iloc') else veiculo["custo_km"]

    # Ponto de partida: Coordenadas da Base (ID 0)
    base = (df_destinos.iloc[0]["x"], df_destinos.iloc[0]["y"])

    pos_anterior = base
    distancia_total = 0
    carga_atual_no_veiculo = 0  # Carga da "viagem" atual
    carga_total_entregue = 0     # Acumulado total da rota
    penalidade = 0
    tempo_acumulado_minutos = 0

    # --- 2. LOOP DE ENTREGA COM LÓGICA DE REABASTECIMENTO ---
    for ordem, idx in enumerate(rota):
        destino = df_destinos.iloc[idx]
        pos_atual = (destino["x"], destino["y"])
        peso_pedido = destino["peso_kg"]

        # LÓGICA DE FRAGMENTAÇÃO: Se estourar a carga, volta na base e retorna ao ponto
        if carga_atual_no_veiculo + peso_pedido > v_capacidade:
            dist_ate_base = calcular_distancia(pos_anterior, base)
            dist_da_base_ao_destino = calcular_distancia(base, pos_atual)
            
            distancia_total += (dist_ate_base + dist_da_base_ao_destino)
            # Tempo: Deslocamento + 15 min de carregamento no CD
            tempo_acumulado_minutos += ((dist_ate_base + dist_da_base_ao_destino) / v_velocidade) * 60 + 15
            
            carga_atual_no_veiculo = peso_pedido # Reset da carga para nova "perna"
        else:
            # Viagem normal entre pontos
            dist = calcular_distancia(pos_anterior, pos_atual)
            distancia_total += dist
            tempo_acumulado_minutos += (dist / v_velocidade) * 60
            carga_atual_no_veiculo += peso_pedido

        carga_total_entregue += peso_pedido

        # --- 3. REGRAS DE NEGÓCIO E PENALIDADES ---
        
        # Penalidade de Segurança: Carga valiosa em moto
        if destino["valor_declarado"] > 3000 and v_tipo == "moto":
            penalidade += 5000

        # Prioridades (Hospitais e Urgências)
        if destino["prioridade"] == 1:
            penalidade += ordem * 200
        if destino["tipo"] == "hospital":
            penalidade += ordem * 150 

        # Janela de Horário (Comercial fecha após 8h de turno)
        if destino["horario"] == "comercial" and tempo_acumulado_minutos > 480:
            penalidade += 10000 

        # BONIFICAÇÃO DE EFICIÊNCIA: Se for prioridade e coube na moto
        if (destino["prioridade"] == 1 and 
            destino["valor_declarado"] <= 3000 and 
            v_tipo == "moto"):
            penalidade -= 1000 

        pos_anterior = pos_atual

    # --- 4. RETORNO FINAL E PENALIDADES DE RESTRIÇÃO ---
    dist_retorno = calcular_distancia(pos_anterior, base)
    distancia_total += dist_retorno
    tempo_acumulado_minutos += (dist_retorno / v_velocidade) * 60

    # Penalidade de Autonomia (Km total do dia)
    if distancia_total > v_autonomia:
        penalidade += 500000 

    # Penalidade Caminhão em Comercial (Baseado no último destino processado)
    if destino["horario"] == "comercial" and v_tipo == "caminhao":
        penalidade += 50000

    # --- 5. RESULTADO FINAL ---
    custo_operacional = distancia_total * v_custo_km
    return custo_operacional + penalidade