import math

import pygame


DURACOES = {"APARECER": 400, "LER": 3200, "FECHAR": 650}
PROXIMA_FASE = {"APARECER": "LER", "LER": "FECHAR", "FECHAR": "FIM"}


def atualizar(agora, fase, tempo_fase, dados):
    if agora - tempo_fase >= DURACOES.get(fase, 500):
        fase = PROXIMA_FASE[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    x = 0
    if fase == "LER":
        x = math.sin(agora * 0.012) * 12
    return x, 28, 1, fase, tempo_fase


def desenhar(superficie, agora, fase, inicio_atividade, dados, criar_fonte):
    x = dados.get("objeto_x", 400)
    y = 365
    pygame.draw.polygon(superficie, (255, 255, 255), [(x - 55, y + 20), (x, y + 5), (x + 55, y + 20), (x, y + 35)], 3)
    pygame.draw.line(superficie, (255, 255, 255), (x, y + 5), (x, y + 35), 2)
    pagina = int((agora - inicio_atividade) / 700) % 3
    for indice in range(pagina + 1):
        pygame.draw.line(superficie, (255, 255, 255), (x - 35, y + 17 + indice * 5), (x - 8, y + 13 + indice * 5), 2)
