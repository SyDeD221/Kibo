import pygame


DURACOES = {"APARECER": 250, "OLHAR": 900, "PAUSA": 1200, "VOLTAR": 850}
PROXIMA_FASE = {"APARECER": "OLHAR", "OLHAR": "PAUSA", "PAUSA": "VOLTAR", "VOLTAR": "FIM"}


def atualizar(agora, fase, tempo_fase, dados):
    if agora - tempo_fase >= DURACOES.get(fase, 500):
        fase = PROXIMA_FASE[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    progresso = min(1, (agora - tempo_fase) / max(1, DURACOES.get(fase, 500)))
    y = -28 if fase in ("OLHAR", "PAUSA") else -28 * (1 - progresso)
    return 0, y, 1, fase, tempo_fase


def desenhar(superficie, agora, fase, inicio_atividade, dados, criar_fonte):
    pygame.draw.circle(superficie, (255, 255, 255), (520, 125), 5, 2)
    pygame.draw.circle(superficie, (255, 255, 255), (540, 105), 9, 2)
