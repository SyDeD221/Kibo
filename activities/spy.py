import pygame


DURACOES = {"APARECER": 350, "ESQUERDA": 900, "OUTRO_LADO": 450, "CENTRO": 700}
PROXIMA_FASE = {"APARECER": "ESQUERDA", "ESQUERDA": "OUTRO_LADO", "OUTRO_LADO": "CENTRO", "CENTRO": "FIM"}


def atualizar(agora, fase, tempo_fase, dados):
    if agora - tempo_fase >= DURACOES.get(fase, 500):
        fase = PROXIMA_FASE[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    x = {"ESQUERDA": -48, "OUTRO_LADO": 48}.get(fase, 0)
    return x, 0, 1, fase, tempo_fase


def desenhar(superficie, agora, fase, inicio_atividade, dados, criar_fonte):
    x = dados.get("objeto_x", 400)
    largura = superficie.get_width()
    pygame.draw.rect(superficie, (255, 255, 255), (0 if x < 400 else largura - 22, 320, 22, 80), 3)
