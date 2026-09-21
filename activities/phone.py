import math

import pygame


DURACOES_TELEMOVEL = {
    "APARECER": 350,
    "OLHAR": 900,
    "INTERAGIR": 2800,
    "GUARDAR": 600,
}

PROXIMA_FASE_TELEMOVEL = {
    "APARECER": "OLHAR",
    "OLHAR": "INTERAGIR",
    "INTERAGIR": "GUARDAR",
    "GUARDAR": "FIM",
}


def atualizar_telemovel(agora, fase, tempo_fase, dados=None):
    duracao = DURACOES_TELEMOVEL.get(fase, 500)
    if agora - tempo_fase >= duracao:
        fase = PROXIMA_FASE_TELEMOVEL[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    progresso = min(1, (agora - tempo_fase) / max(1, DURACOES_TELEMOVEL.get(fase, 500)))
    x = math.sin(agora * 0.012) * 12 if fase == "INTERAGIR" else 0
    return x, 28, 1, fase, tempo_fase


def desenhar_telemovel(superficie, agora, fase, inicio_atividade, dados, criar_fonte):
    x = dados.get("objeto_x", 400)
    y = 365
    pygame.draw.rect(superficie, (255, 255, 255), (x - 22, y - 34, 44, 68), 3)
    pygame.draw.circle(superficie, (255, 255, 255), (x, y + 23), 3)
    if fase == "INTERAGIR":
        pygame.draw.circle(superficie, (255, 255, 255), (x + 9, y - 8), 3)
