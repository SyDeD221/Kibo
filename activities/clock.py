from datetime import datetime
import math

import pygame


DURACOES = {"APARECER": 350, "OLHAR": 700, "VER_HORA": 2200, "REACAO": 650, "GUARDAR": 600}
PROXIMA_FASE = {"APARECER": "OLHAR", "OLHAR": "VER_HORA", "VER_HORA": "REACAO", "REACAO": "GUARDAR", "GUARDAR": "FIM"}


def atualizar(agora, fase, tempo_fase, dados):
    if agora - tempo_fase >= DURACOES.get(fase, 500):
        fase = PROXIMA_FASE[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    x = math.sin(agora * 0.012) * 12 if fase == "VER_HORA" else 0
    return x, 28, 1, fase, tempo_fase


def desenhar(superficie, agora, fase, inicio_atividade, dados, criar_fonte):
    x = dados.get("objeto_x", 400)
    y = 365
    pygame.draw.rect(superficie, (255, 255, 255), (x - 22, y - 34, 44, 68), 3)
    pygame.draw.circle(superficie, (255, 255, 255), (x, y + 23), 3)
    texto = datetime.now().strftime("%H:%M")
    fonte = criar_fonte(24, negrito=True)
    superficie.blit(fonte.render(texto, True, (255, 255, 255)), (x - 31, y - 9))
