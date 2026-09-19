import os

import pygame


ICONS_DIR = os.path.join(os.path.dirname(__file__), "icons")
_originais = {}
_cache = {}
_avisos = set()


def _caminhos_icone(nome):
    partes = nome.replace("\\", "/").split("/")
    nome_ficheiro = partes[-1]
    subpastas = partes[:-1]
    pastas = [
        os.path.join(ICONS_DIR, "png", *subpastas),
        os.path.join(ICONS_DIR, *subpastas),
    ]
    caminhos = [os.path.join(pasta, nome_ficheiro + ".png") for pasta in pastas]

    for pasta in pastas:
        if os.path.isdir(pasta):
            variantes = sorted(
                ficheiro for ficheiro in os.listdir(pasta)
                if ficheiro.startswith(nome_ficheiro + "_")
                and ficheiro.lower().endswith(".png")
            )
            caminhos.extend(os.path.join(pasta, ficheiro) for ficheiro in variantes)
    return caminhos


def carregar_icone(nome, tamanho, cor=None):
    """Carrega o PNG original e cria versões suavemente redimensionadas em cache."""
    tamanho = int(tamanho)
    caminhos = _caminhos_icone(nome)
    caminho = next((item for item in caminhos if os.path.isfile(item)), None)

    chave = (caminho or nome, tamanho, cor)
    if chave in _cache:
        return _cache[chave]

    if caminho is None:
        if nome not in _avisos:
            print(f"[ICON] Ícone não encontrado: {nome}")
            _avisos.add(nome)
        return None

    try:
        if caminho not in _originais:
            _originais[caminho] = pygame.image.load(caminho).convert_alpha()
        original = _originais[caminho]
        icone = pygame.transform.smoothscale(original, (tamanho, tamanho))
    except (OSError, RuntimeError, pygame.error) as erro:
        print(f"[ICON] Não foi possível carregar {nome}: {erro}")
        return None

    if cor is not None:
        icone = icone.copy()
        icone.fill(cor, special_flags=pygame.BLEND_RGBA_MULT)

    _cache[chave] = icone
    return icone


def desenhar_icone(superficie, nome, x, y, tamanho=48, cor=None):
    icone = carregar_icone(nome, tamanho, cor)
    if icone is not None:
        superficie.blit(icone, (int(x), int(y)))
    return icone


def obter_icone_clima(codigo):
    if codigo == 0:
        return "weather/clear_day"
    if codigo in (1, 2, 3):
        return "weather/cloud"
    if codigo in (45, 48):
        return "weather/foggy"
    if codigo in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return "weather/rainy"
    if codigo in (71, 73, 75, 77, 85, 86):
        return "weather/weather_snowy"
    if codigo in (95, 96, 99):
        return "weather/thunderstorm"
    return "weather/cloud"