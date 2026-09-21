
DURACOES = {"APARECER": 500, "FECHAR": 800, "DORMIR": 1400, "ACORDAR": 1000, "SUSTO": 350, "VOLTAR": 700}
PROXIMA_FASE = {"APARECER": "FECHAR", "FECHAR": "DORMIR", "DORMIR": "ACORDAR", "ACORDAR": "SUSTO", "SUSTO": "VOLTAR", "VOLTAR": "FIM"}


def atualizar(agora, fase, tempo_fase, dados):
    if agora - tempo_fase >= DURACOES.get(fase, 500):
        fase = PROXIMA_FASE[fase]
        tempo_fase = agora
        if fase == "FIM":
            return 0, 0, 1, fase, tempo_fase

    progresso = min(1, (agora - tempo_fase) / max(1, DURACOES.get(fase, 500)))
    abertura = 1
    y = 0
    if fase in ("FECHAR", "DORMIR"):
        abertura = 1 - min(1, progresso)
    elif fase == "ACORDAR":
        abertura = progresso
    elif fase == "SUSTO":
        y = -18 * (1 - progresso)
    return 0, y, abertura, fase, tempo_fase
