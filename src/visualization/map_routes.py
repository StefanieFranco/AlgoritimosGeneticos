import pygame
import numpy as np
import matplotlib.pyplot as plt

def atualizar_tela_evolucao(tela, df_destinos, melhor_rota, geracao, fitness):
    BRANCO, PRETO, VERDE, VERMELHO, AZUL, CINZA = (255,255,255), (0,0,0), (0,200,0), (255,0,0), (0,0,255), (200,200,200)
    tela.fill(BRANCO)
    fonte = pygame.font.SysFont("Arial", 18)

    pos_base = (int(df_destinos.iloc[0]['x']), int(df_destinos.iloc[0]['y']))
    pos_ant = pos_base
    
    if melhor_rota:
        for idx in melhor_rota:
            dest = df_destinos.iloc[idx]
            pos_at = (int(dest['x']), int(dest['y']))
            pygame.draw.line(tela, AZUL, pos_ant, pos_at, 1)
            pos_ant = pos_at
        pygame.draw.line(tela, AZUL, pos_ant, pos_base, 1)

    for i, row in df_destinos.iterrows():
        pos = (int(row['x']), int(row['y']))
        cor = VERDE if i == 0 else (VERMELHO if row['prioridade'] == 2 else CINZA)
        pygame.draw.circle(tela, cor, pos, 4)

    txt = fonte.render(f"Geracao: {geracao} | Melhor Fitness: {fitness:.2f}", True, PRETO)
    tela.blit(txt, (10, 10))
    pygame.display.flip()

def plotar_mapa_inline(df_destinos, melhor_rota, titulo="Resultado Final"):
    """Renderiza a rota final e exibe diretamente no corpo do Jupyter"""
    
    # 1. Configurar um Pygame "oculto" (Surface em memória)
    LARGURA, ALTURA = 800, 600
    surface = pygame.Surface((LARGURA, ALTURA))
    
    # Cores
    BRANCO, PRETO, VERDE, VERMELHO, AZUL, CINZA = (255,255,255), (0,0,0), (0,200,0), (255,0,0), (0,0,255), (200,200,200)
    surface.fill(BRANCO)
    
    # 2. Desenhar a Rota na Surface
    pos_base = (int(df_destinos.iloc[0]['x']), int(df_destinos.iloc[0]['y']))
    pos_ant = pos_base
    
    for idx in melhor_rota:
        dest = df_destinos.iloc[idx]
        pos_at = (int(dest['x']), int(dest['y']))
        pygame.draw.line(surface, AZUL, pos_ant, pos_at, 2)
        pos_ant = pos_at
    pygame.draw.line(surface, AZUL, pos_ant, pos_base, 2)

    # 3. Desenhar os Pontos
    for i, row in df_destinos.iterrows():
        pos = (int(row['x']), int(row['y']))
        cor = VERDE if i == 0 else (VERMELHO if row['prioridade'] == 2 else CINZA)
        pygame.draw.circle(surface, cor, pos, 6)

    # 4. Converter a Surface do Pygame para Array do Matplotlib
    # Precisamos rotacionar e transpor porque o Pygame usa (x,y) e o Array (y,x)
    view = pygame.surfarray.array3d(surface)
    view = view.transpose([1, 0, 2])

    # 5. Plotar usando Matplotlib (para aparecer no Jupyter)
    plt.figure(figsize=(12, 8))
    plt.imshow(view)
    plt.title(titulo)
    plt.axis('off') # Esconde as coordenadas dos eixos
    plt.show()