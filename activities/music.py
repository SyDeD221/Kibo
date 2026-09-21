import math

import pygame


DURACOES = {"APARECER": 350, "OUVIR": 3000, "DESAPARECER": 500}
PROXIMA_FASE = {"APARECER": "OUVIR", "OUVIR": "DESAPARECER", "DESAPARECER": "FIM"}


def atualizar(agora, fase, tempo_fase, dados):
    if agora - tempo_fase >= DURACOES.get(fase, 500):
        fase = PROXIMA_FASE[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    y = math.sin(agora * 0.014) * 10
    x = math.sin(agora * 0.009) * 14
    return x, y, 1, fase, tempo_fase


def desenhar(superficie, agora, fase, inicio_atividade, dados, criar_fonte):
    x = dados.get("objeto_x", 400)
    y = 365
    pygame.draw.line(superficie, (255, 255, 255), (x, y - 30), (x, y + 8), 4)
    pygame.draw.line(superficie, (255, 255, 255), (x, y - 30), (x + 22, y - 38), 4)
    pygame.draw.circle(superficie, (255, 255, 255), (x - 5, y + 10), 8)
    pygame.draw.circle(superficie, (255, 255, 255), (x + 17, y + 2), 8)
