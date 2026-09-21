
DURACOES = {"APARECER": 250, "ESQUERDA": 700, "DIREITA": 700, "CIMA": 650, "PARADO": 1100}
PROXIMA_FASE = {"APARECER": "ESQUERDA", "ESQUERDA": "DIREITA", "DIREITA": "CIMA", "CIMA": "PARADO", "PARADO": "FIM"}


def atualizar(agora, fase, tempo_fase, dados):
    if agora - tempo_fase >= DURACOES.get(fase, 500):
        fase = PROXIMA_FASE[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    x = {"ESQUERDA": -45, "DIREITA": 45}.get(fase, 0)
    y = -24 if fase == "CIMA" else 0
    return x, y, 1, fase, tempo_fase
