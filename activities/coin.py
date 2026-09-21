import math

import pygame


DURACOES = {"APARECER": 400, "OLHAR": 700, "ATIRAR": 550, "ACOMPANHAR": 850, "APANHAR": 650, "PAUSA": 450, "DESAPARECER": 450}
PROXIMA_FASE = {"APARECER": "OLHAR", "OLHAR": "ATIRAR", "ATIRAR": "ACOMPANHAR", "ACOMPANHAR": "APANHAR", "APANHAR": "PAUSA", "PAUSA": "DESAPARECER", "DESAPARECER": "FIM"}


def atualizar(agora, fase, tempo_fase, dados):
    if agora - tempo_fase >= DURACOES.get(fase, 500):
        fase = PROXIMA_FASE[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    progresso = min(1, (agora - tempo_fase) / max(1, DURACOES.get(fase, 500)))
    x = (dados["objeto_x"] - 400) * progresso
    y = -35 * math.sin(math.pi * progresso) if fase in ("ATIRAR", "ACOMPANHAR") else 18
    return x, y, 1, fase, tempo_fase


def desenhar(superficie, agora, fase, tempo_fase, dados, criar_fonte):
    x = dados.get("objeto_x", 400)
    y = 365
    moeda_y = y - 45 - int(35 * math.sin(math.pi * min(1, (agora - tempo_fase) / 850))) if fase in ("ATIRAR", "ACOMPANHAR") else y
    pygame.draw.circle(superficie, (255, 255, 255), (x, moeda_y), 12, 3)
    pygame.draw.line(superficie, (255, 255, 255), (x - 4, moeda_y - 7), (x + 4, moeda_y + 7), 2)
