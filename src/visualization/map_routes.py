import matplotlib.pyplot as plt
import numpy as np

def visualizar_rotas_vrp_pro(df_destinos, individuo_campeao, df_veiculos):
    plt.figure(figsize=(14, 9))
    
    # 1. Plotar a Base (Centro de Distribuição)
    base = df_destinos.iloc[0]
    plt.scatter(base['x'], base['y'], c='black', marker='s', s=300, label='Centro de Distribuição (Base)', zorder=5)
    
    # 2. Plotar os Destinos com ícones diferentes baseados no 'tipo'
    # Filtramos para não plotar a base novamente como ponto comum
    df_hospitais = df_destinos[(df_destinos['tipo'] == 'hospital') & (df_destinos['id'] != 0)]
    df_casas = df_destinos[(df_destinos['tipo'] == 'casa') & (df_destinos['id'] != 0)]
    
    plt.scatter(df_hospitais['x'], df_hospitais['y'], c='white', edgecolors='red', 
                marker='H', s=150, label='Hospital (Prioritário)', zorder=4, linewidth=2)
    
    plt.scatter(df_casas['x'], df_casas['y'], c='white', edgecolors='blue', 
                marker='p', s=120, label='Casa (Entrega Domiciliar)', zorder=4, linewidth=1.5)

    # 3. Definição de estilo por tipo de veículo
    estilos_veiculo = {
        'moto': {'cor': '#e74c3c', 'estilo': '--', 'espessura': 1.5},      # Vermelho tracejado
        'mini_caminhao': {'cor': '#3498db', 'estilo': '-', 'espessura': 2.5}, # Azul contínuo
        'caminhao': {'cor': '#27ae60', 'estilo': '-', 'espessura': 4.0}      # Verde grosso
    }

    # 4. Desenhar as Rotas do Indivíduo Campeão
    for i, rota in enumerate(individuo_campeao):
        if not rota: 
            continue  # Ignora veículos que o AG decidiu não usar
            
        veiculo = df_veiculos.iloc[i]
        config = estilos_veiculo.get(veiculo['tipo'], {'cor': 'gray', 'estilo': ':', 'espessura': 1})
        
        # Sequência de coordenadas: Base -> Pontos da Rota -> Base
        x_coords = [base['x']] + [df_destinos.iloc[idx]['x'] for idx in rota] + [base['x']]
        y_coords = [base['y']] + [df_destinos.iloc[idx]['y'] for idx in rota] + [base['y']]
        
        # Desenhar a linha da trajetória
        plt.plot(x_coords, y_coords, color=config['cor'], linestyle=config['estilo'], 
                 linewidth=config['espessura'], alpha=0.8, 
                 label=f"Rota {veiculo['id']} [{veiculo['tipo']}]")
        
        # Pequenas setas para indicar a direção do fluxo (Opcional, mas muito 'pro')
        for j in range(len(x_coords)-1):
            plt.annotate('', xy=(x_coords[j+1], y_coords[j+1]), xytext=(x_coords[j], y_coords[j]),
                         arrowprops=dict(arrowstyle='->', color=config['cor'], lw=1, alpha=0.5))

    # 5. Estética do Gráfico
    plt.title('Logística Hospitalar: Otimização de Rotas Multi-Veículo (VRP)', fontsize=16, fontweight='bold')
    plt.xlabel('Coordenada X (km)', fontsize=12)
    plt.ylabel('Coordenada Y (km)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Legenda Logística")
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Adicionar anotações de ID nos pontos para conferência
    for i, row in df_destinos.iterrows():
        if i == 0: continue
        plt.annotate(str(row['id']), (row['x'], row['y']), textcoords="offset points", 
                     xytext=(0,10), ha='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    return plt

def visualizar_no_subplot(ax, df_destinos, individuo, df_veiculos, titulo="Mapa de Rotas"):
    """
    ax: O eixo do matplotlib onde o desenho será feito.
    individuo: Pode ser uma lista de listas (VRP) ou lista simples (TSP).
    """
    # 1. Configurações de estilo e ícones
    base = df_destinos.iloc[0]
    ax.scatter(base['x'], base['y'], c='black', marker='s', s=200, label='Base', zorder=5)
    
    # Diferenciar Hospitais e Casas
    hospitais = df_destinos[df_destinos['tipo'] == 'hospital']
    casas = df_destinos[df_destinos['tipo'] == 'casa']
    
    ax.scatter(hospitais['x'], hospitais['y'], c='white', edgecolors='red', marker='H', s=100, label='Hospital', zorder=4)
    ax.scatter(casas['x'], casas['y'], c='white', edgecolors='blue', marker='p', s=80, label='Casa', zorder=4)

    # Cores e estilos para os veículos
    estilos = {
        'moto': {'c': '#e74c3c', 'ls': '--', 'lw': 1.5},
        'mini_caminhao': {'c': '#3498db', 'ls': '-', 'lw': 2.5},
        'caminhao': {'c': '#27ae60', 'ls': '-', 'lw': 4.0}
    }

    # 2. Lógica para tratar TSP ou VRP
    # Se for uma lista simples [1, 2, 3], transformamos em [[1, 2, 3]] para o loop funcionar
    if isinstance(individuo[0], (int, np.integer)):
        rotas_para_processar = [individuo]
    else:
        rotas_para_processar = individuo

    # 3. Desenhar as Rotas
    for i, rota in enumerate(rotas_para_processar):
        if not rota: continue
        
        # Pega estilo do veículo (se houver mais rotas que veículos, usa default)
        v_tipo = df_veiculos.iloc[i]['tipo'] if i < len(df_veiculos) else 'moto'
        cfg = estilos.get(v_tipo, {'c': 'gray', 'ls': '-', 'lw': 1})
        
        x_coords = [base['x']] + [df_destinos.iloc[idx]['x'] for idx in rota] + [base['x']]
        y_coords = [base['y']] + [df_destinos.iloc[idx]['y'] for idx in rota] + [base['y']]
        
        ax.plot(x_coords, y_coords, color=cfg['c'], linestyle=cfg['ls'], linewidth=cfg['lw'], alpha=0.7)
        
        # Setas de direção
        for j in range(len(x_coords)-1):
            ax.annotate('', xy=(x_coords[j+1], y_coords[j+1]), xytext=(x_coords[j], y_coords[j]),
                         arrowprops=dict(arrowstyle='->', color=cfg['c'], lw=1, alpha=0.4))

    # 4. Ajustes de layout do Eixo
    ax.set_title(titulo)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_aspect('equal') # Mantém a proporção real das distâncias