import math

import pygame


DURACOES = {"APARECER": 400, "JOGAR": 2800, "RESULTADO": 800, "DESAPARECER": 500}
PROXIMA_FASE = {"APARECER": "JOGAR", "JOGAR": "RESULTADO", "RESULTADO": "DESAPARECER", "DESAPARECER": "FIM"}


def atualizar(agora, fase, tempo_fase, dados):
    if agora - tempo_fase >= DURACOES.get(fase, 500):
        fase = PROXIMA_FASE[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    x = math.sin(agora * 0.012) * 12 if fase == "JOGAR" else 0
    return x, 28, 1, fase, tempo_fase


def desenhar(superficie, agora, fase, inicio_atividade, dados, criar_fonte):
    x = dados.get("objeto_x", 400)
    y = 365
    pygame.draw.rect(superficie, (255, 255, 255), (x - 45, y - 14, 90, 28), 3)
    pygame.draw.circle(superficie, (255, 255, 255), (x - 22, y), 6, 2)
    pygame.draw.circle(superficie, (255, 255, 255), (x + 20, y - 4), 3)
    pygame.draw.circle(superficie, (255, 255, 255), (x + 28, y + 5), 3)
