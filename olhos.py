import pygame
import sys
import random
import math
import json
import os
import threading
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from datetime import datetime
from icons import carregar_icone, obter_icone_clima

pygame.init()

LARGURA = 800
ALTURA = 480

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Olhos do Robô")

relogio = pygame.time.Clock()

# Próxima piscada: intervalo aleatório entre 2 e 5 segundos
proxima_piscada = pygame.time.get_ticks() + random.randint(2000, 5000)

piscando = False
inicio_piscada = 0

# Duração da animação
DURACAO_FECHAR = 180
DURACAO_FECHADO = 80
DURACAO_ABRIR = 180

DURACAO_TOTAL = DURACAO_FECHAR + DURACAO_FECHADO + DURACAO_ABRIR

# Altere esta variável para escolher a expressão inicial.
expressao = "normal"
DURACAO_TRANSICAO_EXPRESSAO = 300

# Altere para "relogio" para testar a apresentação da hora.
modo = "olhos"
DURACAO_PREPARACAO_RELOGIO = 250
DURACAO_TRANSICAO_RELOGIO = 600
DURACAO_RELOGIO_VISIVEL = 5000
# Fonte personalizada escolhida na pasta fonts.
FONTE_PATH = "fonts/EncodeSansSemiExpanded-Medium.ttf"
TAMANHO_FONTE_RELOGIO = 210
TAMANHO_FONTE_CLIMA = 42
TAMANHO_FONTE_LOCAL = 24
TAMANHO_FONTE_DESCRICAO = 22
TESTAR_ICONE = False
ICONE_TESTE = "weather/cloud"
CLIMA_TESTE = None
PROBABILIDADE_REACAO_CLIMA = 0.60
TEMPERATURA_FRIO = 10
TEMPERATURA_CALOR = 28
AMPLITUDE_TREMO_FRIO = 5
DURACAO_REACAO_FRIO = 2500
DURACAO_REACAO_CALOR = 3000
DURACAO_REACAO_CHUVA = 2200
DURACAO_REACAO_TROVOADA = 1800
DURACAO_REACAO_NEVE = 2500
DURACAO_REACAO_NEVEOEIRO = 2500
TESTE_REACAO_CLIMA = None

INTERVALO_IDLE_MIN = 4000
INTERVALO_IDLE_MAX = 12000
PROB_IDLE_OLHAR_LADO = 0.28
PROB_IDLE_OLHAR_CIMA = 0.14
PROB_IDLE_OLHAR_BAIXO = 0.12
PROB_IDLE_OLHAR_RAPIDO = 0.18
PROB_IDLE_PISCAR = 0.12
PROB_IDLE_PENSAR = 0.08
PROB_IDLE_SONOLENTO = 0.04
PROB_IDLE_CURIOSIDADE = 0.04
TESTE_IDLE = None

INTERVALO_ATIVIDADE_MIN = 15000
INTERVALO_ATIVIDADE_MAX = 45000
PROB_TELEMOVEL = 15
PROB_VER_HORAS = 10
PROB_MOEDA = 10
PROB_PENSAR = 15
PROB_CANSADO = 10
PROB_MUSICA = 10
PROB_LER = 10
PROB_JOGAR = 10
PROB_ENTEDIADO = 10
PROB_ESPIAR = 5
TESTE_ATIVIDADE_IDLE = None

atividade_idle_atual = None
fase_atividade = None
tempo_fase = 0
inicio_atividade_idle = 0
atividade_idle_dados = {}
ultima_atividade_idle = None
proxima_atividade_idle = pygame.time.get_ticks() + random.randint(
    INTERVALO_ATIVIDADE_MIN, INTERVALO_ATIVIDADE_MAX
)

modo_idle = False
idle_ativo = False
idle_tipo = None
idle_inicio = 0
idle_duracao = 0
idle_direcao = 1
idle_ultima_animacao = None
idle_proxima_acao = pygame.time.get_ticks() + random.randint(INTERVALO_IDLE_MIN, INTERVALO_IDLE_MAX)


def criar_fonte(tamanho, negrito=False):
    caminho_fonte = os.path.join(os.path.dirname(__file__), FONTE_PATH)
    chave = (caminho_fonte, tamanho, negrito)

    if chave not in fontes_cache:
        try:
            fonte = pygame.font.Font(caminho_fonte, tamanho)
        except (OSError, pygame.error):
            if not fonte_personalizada_indisponivel:
                print(f"Fonte personalizada não encontrada: {caminho_fonte}")
                print("A usar temporariamente a fonte padrão do Pygame.")
                globals()["fonte_personalizada_indisponivel"] = True
            fonte = pygame.font.Font(None, tamanho)
        fonte.set_bold(negrito)
        fontes_cache[chave] = fonte

    return fontes_cache[chave]


fontes_cache = {}
fonte_personalizada_indisponivel = False

# Localização usada pelo Open-Meteo. Altere apenas estes valores para outro local.
LATITUDE = 38.7167
LONGITUDE = -9.1333
NOME_LOCAL = "Lisboa"
DURACAO_CLIMA = 5000
TIMEOUT_CLIMA = 6
DURACAO_TRANSICAO_CLIMA = 600

# Simulação da perceção. Substitua estas variáveis pela saída da câmera no futuro.
pessoa_detectada = False
pessoa_conhecida = False
rosto_x = 0.7
rosto_y = 0.4

PESSOA_CONHECIDA = "pessoa_conhecida"
PESSOA_DESCONHECIDA = "pessoa_desconhecida"
NENHUMA_PESSOA = "nenhuma_pessoa"
DURACAO_OBSERVACAO_DESCONHECIDA = 3000
DURACAO_SEGUIR_ROSTO = 450

EXPRESSOES = {
    "normal": {"largura": 180, "altura": 180, "deslocamento_y": 0, "inclinacao": 0, "arco": 0},
    "feliz": {"largura": 180, "altura": 165, "deslocamento_y": 8, "inclinacao": 0, "arco": 1},
    "sonolento": {"largura": 180, "altura": 58, "deslocamento_y": 62, "inclinacao": 0, "arco": 0},
    "surpreso": {"largura": 195, "altura": 240, "deslocamento_y": -30, "inclinacao": 0, "arco": 0},
    "triste": {"largura": 180, "altura": 145, "deslocamento_y": 15, "inclinacao": 14, "arco": 0},
    "zangado": {"largura": 180, "altura": 165, "deslocamento_y": 8, "inclinacao": -22, "arco": 0},
}
PESSOA_CONHECIDA = "pessoa_conhecida"
PESSOA_DESCONHECIDA = "pessoa_desconhecida"
NENHUMA_PESSOA = "nenhuma_pessoa"
DURACAO_OBSERVACAO_DESCONHECIDA = 3000
DURACAO_SEGUIR_ROSTO = 450

EXPRESSOES = {
    "normal": {"largura": 180, "altura": 180, "deslocamento_y": 0, "inclinacao": 0, "arco": 0},
    "feliz": {"largura": 180, "altura": 165, "deslocamento_y": 8, "inclinacao": 0, "arco": 1},
    "sonolento": {"largura": 180, "altura": 58, "deslocamento_y": 62, "inclinacao": 0, "arco": 0},
    "surpreso": {"largura": 195, "altura": 240, "deslocamento_y": -30, "inclinacao": 0, "arco": 0},
    "triste": {"largura": 180, "altura": 145, "deslocamento_y": 15, "inclinacao": 14, "arco": 0},
    "zangado": {"largura": 180, "altura": 165, "deslocamento_y": 8, "inclinacao": -22, "arco": 0},
}

# Deslocamentos seguros em relação ao centro, partilhados pelos dois olhos.
POSICOES_OLHAR = {
    "centro": (0, 0),
    "esquerda": (-55, 0),
    "direita": (55, 0),
    "cima": (0, -40),
    "baixo": (0, 40),
    "cima-esquerda": (-55, -40),
    "cima-direita": (55, -40),
    "baixo-esquerda": (-55, 40),
    "baixo-direita": (55, 40),
}

# Intervalos, duração do movimento e tendência de cada humor.
COMPORTAMENTOS_HUMOR = {
    "normal": {
        "intervalo": (900, 2200), "espera": (700, 1500),
        "duracao": 520, "voltar_centro": False,
        "pesos": {"centro": 3, "esquerda": 2, "direita": 2, "cima": 1, "baixo": 1,
                   "cima-esquerda": 1, "cima-direita": 1, "baixo-esquerda": 1, "baixo-direita": 1},
    },
    "feliz": {
        "intervalo": (450, 1200), "espera": (450, 1000),
        "duracao": 320, "voltar_centro": False,
        "pesos": {nome: 1 for nome in POSICOES_OLHAR},
    },
    "sonolento": {
        "intervalo": (1800, 3800), "espera": (1800, 3200),
        "duracao": 1100, "voltar_centro": False,
        "pesos": {"centro": 4, "baixo": 3, "baixo-esquerda": 1, "baixo-direita": 1,
                   "esquerda": 1, "direita": 1},
    },
    "surpreso": {
        "intervalo": (1200, 2600), "espera": (250, 600),
        "duracao": 220, "voltar_centro": True,
        "pesos": {"esquerda": 2, "direita": 2, "cima": 2, "cima-esquerda": 1, "cima-direita": 1},
    },
    "triste": {
        "intervalo": (1800, 3600), "espera": (1600, 3000),
        "duracao": 1000, "voltar_centro": False,
        "pesos": {"centro": 3, "baixo": 5, "baixo-esquerda": 2, "baixo-direita": 2,
                   "esquerda": 1, "direita": 1},
    },
    "zangado": {
        "intervalo": (1300, 2800), "espera": (500, 1000),
        "duracao": 280, "voltar_centro": True,
        "pesos": {"esquerda": 4, "direita": 4, "centro": 1},
    },
}


def suavizar(progresso):
    return progresso * progresso * (3 - 2 * progresso)


def interpolar_posicao(inicio, fim, progresso):
    progresso = suavizar(progresso)
    return (
        inicio[0] + (fim[0] - inicio[0]) * progresso,
        inicio[1] + (fim[1] - inicio[1]) * progresso,
    )


def mostrar_relogio():
    """Ativa a apresentação da hora para ser chamada futuramente pela IA."""
    global modo
    modo = "relogio"


def descricao_codigo_meteorologico(codigo):
    descricoes = {
        0: "Céu limpo",
        1: "Parcialmente nublado", 2: "Parcialmente nublado", 3: "Nublado",
        45: "Nevoeiro", 48: "Nevoeiro",
        51: "Chuvisco", 53: "Chuvisco", 55: "Chuvisco",
        56: "Chuvisco congelante", 57: "Chuvisco congelante",
        61: "Chuva", 63: "Chuva", 65: "Chuva",
        66: "Chuva congelante", 67: "Chuva congelante",
        71: "Neve", 73: "Neve", 75: "Neve", 77: "Grãos de neve",
        80: "Aguaceiros", 81: "Aguaceiros", 82: "Aguaceiros",
        85: "Aguaceiros de neve", 86: "Aguaceiros de neve",
        95: "Trovoada", 96: "Trovoada com granizo", 99: "Trovoada com granizo",
    }
    return descricoes.get(codigo, "Clima desconhecido")


def obter_clima():
    parametros = urlencode({
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "timezone": "auto",
    })
    url = "https://api.open-meteo.com/v1/forecast?" + parametros
    pedido = Request(url, headers={"User-Agent": "Kibo-Pygame/1.0"})

    with urlopen(pedido, timeout=TIMEOUT_CLIMA) as resposta:
        dados = json.loads(resposta.read().decode("utf-8"))
    atual = dados["current"]
    codigo = int(atual["weather_code"])
    return {
        "temperatura": round(float(atual["temperature_2m"])),
        "codigo": codigo,
        "descricao": descricao_codigo_meteorologico(codigo),
        "vento": float(atual.get("wind_speed_10m", 0)),
    }


def iniciar_requisicao_clima():
    global clima_dados, clima_erro, clima_requisicao_em_curso
    clima_dados = None
    clima_erro = False
    clima_requisicao_em_curso = True

    def requisitar():
        global clima_dados, clima_erro, clima_requisicao_em_curso
        try:
            clima_dados = obter_clima()
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            clima_erro = True
        finally:
            clima_requisicao_em_curso = False

    threading.Thread(target=requisitar, daemon=True).start()


def mostrar_clima():
    """Ativa a apresentação do clima para ser chamada futuramente pela IA."""
    global modo
    modo = "clima"


def atualizar_modo_clima(agora):
    global modo, estado_modo_clima, inicio_modo_clima, posicao_saida_clima

    if modo == "clima" and estado_modo_clima == "olhos":
        estado_modo_clima = "preparar"
        inicio_modo_clima = agora
        iniciar_requisicao_clima()
    elif modo != "clima" and estado_modo_clima != "olhos":
        posicao_saida_clima = movimento_olhos.posicao_atual
        estado_modo_clima = "sair"
        inicio_modo_clima = agora

    tempo = agora - inicio_modo_clima
    if estado_modo_clima == "preparar" and tempo >= DURACAO_TRANSICAO_CLIMA // 2:
        estado_modo_clima = "visivel"
        inicio_modo_clima = agora
    elif estado_modo_clima == "visivel" and tempo >= DURACAO_CLIMA:
        posicao_saida_clima = movimento_olhos.posicao_atual
        estado_modo_clima = "sair"
        inicio_modo_clima = agora
    elif estado_modo_clima == "sair" and tempo >= DURACAO_TRANSICAO_CLIMA:
        estado_modo_clima = "olhos"
        inicio_modo_clima = agora
        if modo == "clima":
            tipo_reacao = iniciar_reacao_clima()
            modo = "reacao_clima" if tipo_reacao else "olhos"
        return "saida", 1

    # Recomeçar o progresso quando uma nova fase foi iniciada neste frame.
    tempo = agora - inicio_modo_clima

    if estado_modo_clima == "preparar":
        return "entrada", min(1, tempo / (DURACAO_TRANSICAO_CLIMA / 2))
    if estado_modo_clima == "visivel":
        return "visivel", 1
    if estado_modo_clima == "sair":
        return "saida", min(1, tempo / DURACAO_TRANSICAO_CLIMA)
    if modo == "olhos" and estado_modo_clima == "olhos" and tempo >= DURACAO_TRANSICAO_CLIMA:
        return "saida", 1
    return "olhos", 0


def determinar_reacao_clima():
    if TESTE_REACAO_CLIMA is not None:
        return TESTE_REACAO_CLIMA

    if clima_dados is None or random.random() >= PROBABILIDADE_REACAO_CLIMA:
        return None

    codigo = clima_dados.get("codigo")
    temperatura = clima_dados.get("temperatura")
    if codigo in (95, 96, 99):
        return "trovoada"
    if codigo in (71, 73, 75, 77, 85, 86):
        return "neve"
    if codigo in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return "chuva"
    if codigo in (45, 48):
        return "nevoeiro"
    if temperatura is not None and temperatura < TEMPERATURA_FRIO:
        return "frio"
    if temperatura is not None and (temperatura >= TEMPERATURA_CALOR or codigo == 0):
        return "calor"
    return None


def iniciar_reacao_clima():
    global modo, reacao_clima_ativa, tipo_reacao_clima, inicio_reacao_clima
    global fase_reacao_clima, dados_reacao_clima

    tipo_reacao_clima = determinar_reacao_clima()
    reacao_clima_ativa = tipo_reacao_clima is not None
    if reacao_clima_ativa:
        inicio_reacao_clima = pygame.time.get_ticks()
        fase_reacao_clima = "preparar"
        dados_reacao_clima = criar_dados_reacao(tipo_reacao_clima)
        modo = "reacao_clima"
    return tipo_reacao_clima


def criar_dados_reacao(tipo):
    if tipo == "chuva":
        return {
            "gotas": [{"x": random.randint(40, LARGURA - 40), "y": random.randint(70, 280),
                       "velocidade": random.uniform(180, 280), "splash": 0}
                      for _ in range(random.randint(40, 68))],
            "nuvens": [random.randint(60, LARGURA - 60) for _ in range(8)],
        }
    if tipo == "neve":
        return {"flocos": [{"x": random.uniform(0, LARGURA), "y": random.uniform(0, ALTURA),
                             "velocidade": random.uniform(18, 38), "fase": random.random() * 6.28}
                            for _ in range(random.randint(90, 150))]}
    if tipo == "nevoeiro":
        return {"faixas": [random.randint(-220, 100) for _ in range(5)]}
    if tipo == "trovoada":
        return {
            "relampago_em": random.uniform(450, 850), "trovao_em": None,
            "relampago_fim": 0, "vibracao": 0,
            "nuvens": [random.randint(70, LARGURA - 70) for _ in range(6)],
            "raios": [
                {
                    "x": random.randint(80, LARGURA - 80),
                    "y": random.randint(45, 180),
                    "fim_x": random.randint(120, LARGURA - 120),
                    "fim_y": random.randint(260, ALTURA - 30),
                }
                for _ in range(random.randint(5, 9))
            ],
        }
    if tipo == "calor":
        return {"sol_x": LARGURA - 105, "sol_y": 90, "ondas": [0.0, 0.8, 1.6]}
    return {}


def duracao_reacao_clima(tipo):
    return {
        "frio": DURACAO_REACAO_FRIO,
        "calor": DURACAO_REACAO_CALOR,
        "chuva": DURACAO_REACAO_CHUVA,
        "trovoada": DURACAO_REACAO_TROVOADA,
        "neve": DURACAO_REACAO_NEVE,
        "nevoeiro": DURACAO_REACAO_NEVEOEIRO,
    }.get(tipo, 0)


def atualizar_reacao_clima(agora):
    global modo, reacao_clima_ativa, tipo_reacao_clima, fase_reacao_clima

    if not reacao_clima_ativa or tipo_reacao_clima is None:
        modo = "olhos"
        return 0

    duracao = duracao_reacao_clima(tipo_reacao_clima)
    tempo = agora - inicio_reacao_clima
    progresso = min(1, tempo / duracao)

    if tipo_reacao_clima == "trovoada":
        relampago_em = dados_reacao_clima["relampago_em"]
        trovao_em = dados_reacao_clima["trovao_em"]

        if tempo >= relampago_em and trovao_em is None:
            dados_reacao_clima["relampago_fim"] = tempo + random.randint(90, 180)
            dados_reacao_clima["trovao_em"] = tempo + random.randint(400, 850)
            trovao_em = dados_reacao_clima["trovao_em"]

        if trovao_em is not None and tempo >= trovao_em:
            dados_reacao_clima["vibracao"] = 1

        if trovao_em is None:
            fase_reacao_clima = "relampago"
        else:
            fase_reacao_clima = "trovao" if tempo >= trovao_em else "relampago"
    elif tempo < duracao * 0.18:
        fase_reacao_clima = "preparar"
    elif tempo > duracao * 0.78:
        fase_reacao_clima = "recuperar"
    else:
        fase_reacao_clima = "animar"

    if tipo_reacao_clima == "chuva":
        for gota in dados_reacao_clima["gotas"]:
            gota["y"] += gota["velocidade"] / 60
            if gota["y"] >= ALTURA:
                gota["y"] = random.randint(20, 80)
                gota["x"] = random.randint(0, LARGURA)
                gota["splash"] = 1
            else:
                gota["splash"] = max(0, gota["splash"] - 0.08)
    elif tipo_reacao_clima == "neve":
        for floco in dados_reacao_clima["flocos"]:
            floco["y"] += floco["velocidade"] / 60
            floco["x"] += math.sin(tempo * 0.002 + floco["fase"]) * 2.2
            if floco["y"] > ALTURA + 12:
                floco["y"] = -8
            if floco["x"] < -10:
                floco["x"] = LARGURA + 10
            elif floco["x"] > LARGURA + 10:
                floco["x"] = -10
    elif tipo_reacao_clima == "nevoeiro":
        for indice in range(len(dados_reacao_clima["faixas"])):
            dados_reacao_clima["faixas"][indice] += 0.7
            if dados_reacao_clima["faixas"][indice] > 800:
                dados_reacao_clima["faixas"][indice] = -220

    if progresso >= 1:
        reacao_clima_ativa = False
        tipo_reacao_clima = None
        modo = "olhos"
        return 1
    return progresso


def finalizar_reacao_clima():
    global modo, reacao_clima_ativa, tipo_reacao_clima, fase_reacao_clima
    reacao_clima_ativa = False
    tipo_reacao_clima = None
    fase_reacao_clima = "fim"
    modo = "olhos"


def desenhar_reacao_clima(superficie, agora, tipo, progresso):
    tempo = (agora - inicio_reacao_clima) / 1000
    intensidade = math.sin(math.pi * min(1, progresso))
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)

    if tipo == "chuva":
        for x in range(-120, LARGURA + 120, 180):
            desenhar_nuvem(camada, x + 60, 75 + (x % 70), 1.2)
            desenhar_nuvem(camada, x + 130, 120 + (x % 90), 1.0)
        for gota in dados_reacao_clima["gotas"]:
            pygame.draw.line(camada, (255, 255, 255), (int(gota["x"]), int(gota["y"])),
                             (int(gota["x"] - 3), int(gota["y"] + 13)), 2)
            if gota["splash"] > 0:
                raio = int(12 * gota["splash"])
                pygame.draw.arc(camada, (255, 255, 255),
                                (int(gota["x"] - raio), ALTURA - 75 - raio // 3, raio * 2, raio), 0, math.pi, 2)
    elif tipo == "neve":
        for floco in dados_reacao_clima["flocos"]:
            pygame.draw.circle(camada, (255, 255, 255), (int(floco["x"]), int(floco["y"])), 3)
    elif tipo == "nevoeiro":
        for y, x in enumerate(dados_reacao_clima["faixas"]):
            pygame.draw.line(camada, (255, 255, 255, 100), (int(x), 150 + y * 52),
                             (int(x + 260), 150 + y * 52), 5)
    elif tipo == "calor":
        centro = (dados_reacao_clima["sol_x"], dados_reacao_clima["sol_y"])
        pygame.draw.circle(camada, (255, 255, 255), centro, int(26 + 6 * intensidade), 4)
        for indice in range(12):
            inicio = (int(centro[0] - 8), int(centro[1] + 8))
            fim = (int(centro[0] - 40 - indice * 12), int(centro[1] + 18 + indice * 8))
            pygame.draw.line(camada, (255, 255, 255), inicio, fim, 3)
    elif tipo == "frio":
        pass
    elif tipo == "trovoada":
        if dados_reacao_clima["vibracao"]:
            camada.fill((255, 255, 255, 28), special_flags=pygame.BLEND_RGBA_ADD)
        for nuvem_x in dados_reacao_clima.get("nuvens", []):
            desenhar_nuvem(camada, nuvem_x + random.randint(-20, 20), 80 + random.randint(0, 25), 0.9)
        for raio in dados_reacao_clima.get("raios", []):
            if dados_reacao_clima["relampago_fim"] > agora - inicio_reacao_clima:
                pygame.draw.line(camada, (255, 255, 255),
                                 (raio["x"], raio["y"]),
                                 (raio["fim_x"], raio["fim_y"]), 4)

    camada.set_alpha(max(0, min(255, int(255 * intensidade))))
    superficie.blit(camada, (0, 0))


def atualizar_modo_relogio(agora):
    """Atualiza a fase do relógio sem bloquear o ciclo principal."""
    global modo, estado_modo_relogio, inicio_modo_relogio

    if modo == "relogio" and estado_modo_relogio == "olhos":
        estado_modo_relogio = "preparar"
        inicio_modo_relogio = agora
    elif modo == "olhos" and estado_modo_relogio != "olhos":
        estado_modo_relogio = "sair"
        inicio_modo_relogio = agora

    tempo = agora - inicio_modo_relogio

    if estado_modo_relogio == "preparar" and tempo >= DURACAO_PREPARACAO_RELOGIO:
        estado_modo_relogio = "entrar"
        inicio_modo_relogio = agora
    elif estado_modo_relogio == "entrar" and tempo >= DURACAO_TRANSICAO_RELOGIO:
        estado_modo_relogio = "visivel"
        inicio_modo_relogio = agora
    elif estado_modo_relogio == "visivel" and tempo >= DURACAO_RELOGIO_VISIVEL:
        estado_modo_relogio = "sair"
        inicio_modo_relogio = agora
    elif estado_modo_relogio == "sair" and tempo >= DURACAO_TRANSICAO_RELOGIO:
        modo = "olhos"
        estado_modo_relogio = "olhos"
        inicio_modo_relogio = agora

    if estado_modo_relogio == "preparar":
        return "olhos", 0
    if estado_modo_relogio == "entrar":
        return "transicao_entrada", min(1, tempo / DURACAO_TRANSICAO_RELOGIO)
    if estado_modo_relogio == "visivel":
        return "relogio", 1
    if estado_modo_relogio == "sair":
        return "transicao_saida", min(1, tempo / DURACAO_TRANSICAO_RELOGIO)
    return "olhos", 0


class MovimentoOlhos:
    def __init__(self, agora):
        self.posicao_atual = (0, 0)
        self.posicao_desejada = (0, 0)
        self.nome_desejado = "centro"
        self.inicio_movimento = agora
        self.fim_movimento = agora
        self.proxima_decisao = agora + random.randint(1200, 2200)
        self.humor_atual = "normal"

    def escolher_direcao(self, humor):
        pesos = COMPORTAMENTOS_HUMOR[humor]["pesos"]
        nomes = list(pesos)
        valores = [pesos[nome] for nome in nomes]
        return random.choices(nomes, weights=valores, k=1)[0]

    def iniciar_movimento(self, agora, nome_desejado, humor):
        self.posicao_atual = self.posicao_no_tempo(agora)
        self.nome_desejado = nome_desejado
        self.posicao_desejada = POSICOES_OLHAR[nome_desejado]
        self.inicio_movimento = agora
        self.fim_movimento = agora + COMPORTAMENTOS_HUMOR[humor]["duracao"]

    def posicao_no_tempo(self, agora):
        if self.fim_movimento <= self.inicio_movimento:
            return self.posicao_desejada
        progresso = min(1, (agora - self.inicio_movimento) /
                        (self.fim_movimento - self.inicio_movimento))
        return interpolar_posicao(self.posicao_atual, self.posicao_desejada, progresso)

    def atualizar(self, agora, humor):
        if humor not in COMPORTAMENTOS_HUMOR:
            humor = "normal"

        if humor != self.humor_atual:
            self.humor_atual = humor
            self.proxima_decisao = agora + random.randint(500, 1000)

        self.posicao_atual = self.posicao_no_tempo(agora)

        if agora >= self.fim_movimento:
            self.posicao_atual = self.posicao_desejada

        if agora < self.proxima_decisao:
            return self.posicao_atual

        comportamento = COMPORTAMENTOS_HUMOR[humor]
        if (comportamento["voltar_centro"] and
                self.nome_desejado != "centro"):
            proximo_nome = "centro"
        else:
            proximo_nome = self.escolher_direcao(humor)

        self.iniciar_movimento(agora, proximo_nome, humor)
        espera = random.randint(*comportamento["espera"])
        self.proxima_decisao = self.fim_movimento + espera
        return self.posicao_atual

    def acompanhar_rosto(self, agora, alvo, duracao):
        """Segue um alvo que pode mudar continuamente, sem saltos."""
        delta = max(1, agora - getattr(self, "ultima_atualizacao", agora))
        fator = min(1, delta / duracao)
        self.posicao_atual = (
            self.posicao_atual[0] + (alvo[0] - self.posicao_atual[0]) * fator,
            self.posicao_atual[1] + (alvo[1] - self.posicao_atual[1]) * fator,
        )
        self.posicao_desejada = alvo
        self.nome_desejado = "rosto"
        self.ultima_atualizacao = agora
        return self.posicao_atual


def rosto_para_movimento(posicao_x, posicao_y):
    """Converte uma posição relativa do rosto em um deslocamento seguro."""
    posicao_x = max(0.0, min(1.0, posicao_x))
    posicao_y = max(0.0, min(1.0, posicao_y))
    return ((posicao_x - 0.5) * 110, (posicao_y - 0.5) * 80)


def desenhar_olho(
    superficie,
    centro_x,
    centro_y,
    largura,
    altura,
    inclinacao,
    arco,
    fator_abertura,
    escala=1,
    opacidade=255,
    escala_x=None,
    escala_y=None,
):
    if escala_x is None:
        escala_x = escala
    if escala_y is None:
        escala_y = escala

    largura = max(1, int(largura * escala_x))
    altura = max(1, int(altura * escala_y))
    altura_visivel = int(altura * fator_abertura)

    if altura_visivel <= 0:
        return

    olho = pygame.Surface((largura, altura), pygame.SRCALPHA)

    if arco > 0.5:
        # Arco de sorriso: as extremidades ficam mais altas que o centro.
        pontos_superiores = []
        pontos_inferiores = []
        espessura = max(14, int(altura * 0.22))
        for indice in range(25):
            proporcao = indice / 24
            curva = 1 - (2 * proporcao - 1) ** 2
            y = altura * 0.12 + altura * 0.45 * curva
            pontos_superiores.append((int(largura * proporcao), int(y)))
            pontos_inferiores.append((int(largura * proporcao), int(y + espessura)))
        pygame.draw.polygon(olho, (255, 255, 255), pontos_superiores + pontos_inferiores[::-1])
        pygame.draw.circle(olho, (255, 255, 255), (0, int(altura * 0.12 + espessura / 2)), espessura // 2)
        pygame.draw.circle(olho, (255, 255, 255), (largura, int(altura * 0.12 + espessura / 2)), espessura // 2)
    else:
        raio = min(45, largura // 4, altura // 4)
        pygame.draw.rect(olho, (255, 255, 255), (0, 0, largura, altura), border_radius=raio)

    # Recortar a parte superior para a pálpebra descer até à base.
    topo_visivel = altura - altura_visivel
    olho = olho.subsurface((0, topo_visivel, largura, altura_visivel)).copy()
    olho = pygame.transform.rotate(olho, inclinacao)
    olho.set_alpha(max(0, min(255, int(opacidade))))

    base_y = centro_y + altura / 2
    superficie.blit(
        olho,
        (int(centro_x - olho.get_width() / 2), int(base_y - olho.get_height())),
    )


def desenhar_relogio(superficie, opacidade=255, escala=1):
    agora = datetime.now()
    separador = ":" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
    texto = agora.strftime("%H") + separador + agora.strftime("%M")
    tamanho_fonte = max(1, int(TAMANHO_FONTE_RELOGIO * escala))
    fonte = criar_fonte(tamanho_fonte, negrito=True)
    relogio_renderizado = fonte.render(texto, True, (255, 255, 255))
    relogio_renderizado.set_alpha(max(0, min(255, int(opacidade))))
    retangulo = relogio_renderizado.get_rect(center=(LARGURA // 2, ALTURA // 2))
    superficie.blit(relogio_renderizado, retangulo)


def categoria_clima(codigo):
    if codigo == 0:
        return "sol"
    if codigo in (1, 2, 3):
        return "nublado"
    if codigo in (45, 48):
        return "nevoeiro"
    if codigo in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return "chuva"
    if codigo in (71, 73, 75, 77, 85, 86):
        return "neve"
    if codigo in (95, 96, 99):
        return "trovoada"
    return "nublado"


def desenhar_nuvem(superficie, centro_x, centro_y, escala=1):
    cor = (255, 255, 255)
    pygame.draw.circle(superficie, cor, (int(centro_x - 28 * escala), int(centro_y)), int(25 * escala))
    pygame.draw.circle(superficie, cor, (int(centro_x), int(centro_y - 14 * escala)), int(34 * escala))
    pygame.draw.circle(superficie, cor, (int(centro_x + 32 * escala), int(centro_y)), int(23 * escala))
    pygame.draw.rect(
        superficie,
        cor,
        (int(centro_x - 52 * escala), int(centro_y), int(105 * escala), int(27 * escala)),
    )


def desenhar_clima(superficie, agora, dados, opacidade=255):
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    intensidade = agora / 1000
    codigo = dados.get("codigo") if dados else None
    codigos_teste = {
        "sun": 0,
        "rain": 61,
        "thunderstorm": 95,
        "snow": 71,
        "cloud": 2,
        "fog": 45,
    }
    if CLIMA_TESTE in codigos_teste:
        codigo = codigos_teste[CLIMA_TESTE]
    categoria = categoria_clima(codigo) if codigo is not None else "indisponivel"
    nome_icone = ICONE_TESTE if TESTAR_ICONE else obter_icone_clima(codigo)
    icone = carregar_icone(nome_icone, 170) if codigo is not None else None
    deslocamento_nuvem = int((intensidade * 8) % 24) - 12
    centro_icone_x = LARGURA // 2 + deslocamento_nuvem

    if icone is not None:
        camada.blit(icone, icone.get_rect(center=(centro_icone_x, 180)))
    elif categoria == "sol":
        centro = (LARGURA // 2, 155)
        pygame.draw.circle(camada, (255, 255, 255), centro, 48, 5)
    elif categoria in ("nublado", "chuva", "trovoada", "neve"):
        desenhar_nuvem(camada, centro_icone_x, 155, 1.25)

    # Elementos animados continuam separados do ícone principal.
    if categoria == "sol":
        centro = (LARGURA // 2, 155)
        for indice in range(12):
            vetor = pygame.math.Vector2(1, 0).rotate(-indice * 30 + intensidade * 8)
            inicio = (centro[0] + int(vetor.x * 65), centro[1] + int(vetor.y * 65))
            fim = (centro[0] + int(vetor.x * 88), centro[1] + int(vetor.y * 88))
            pygame.draw.line(camada, (255, 255, 255), inicio, fim, 4)
    elif categoria == "chuva":
        for indice in range(9):
            x = 305 + indice * 24
            y = 215 + int((intensidade * 110 + indice * 31) % 115)
            pygame.draw.line(camada, (255, 255, 255), (x, y), (x - 7, y + 18), 3)
    elif categoria == "neve":
        for indice in range(9):
            x = 305 + indice * 24
            y = 215 + int((intensidade * 55 + indice * 37) % 125)
            pygame.draw.circle(camada, (255, 255, 255), (x, y), 4)
    elif categoria == "trovoada":
        pisca = int(agora / 140) % 10 in (0, 1)
        pontos = [(410, 205), (385, 275), (415, 260), (395, 330), (455, 245), (425, 260)]
        pygame.draw.polygon(camada, (255, 255, 255), pontos)
        if pisca:
            camada.fill((255, 255, 255, 35), special_flags=pygame.BLEND_RGBA_ADD)
    elif categoria == "nevoeiro":
        for indice in range(5):
            y = 125 + indice * 38
            x = int((intensidade * 35 + indice * 90) % 150) - 75
            pygame.draw.line(camada, (255, 255, 255), (x, y), (LARGURA + x, y), 5)

    if dados:
        temperatura = f"{dados['temperatura']}°C"
        descricao = dados["descricao"]
    elif clima_erro:
        temperatura = "Clima indisponível"
        descricao = ""
    else:
        temperatura = "A obter clima..."
        descricao = ""

    fonte_temperatura = criar_fonte(TAMANHO_FONTE_CLIMA, negrito=True)
    fonte_local = criar_fonte(TAMANHO_FONTE_LOCAL, negrito=True)
    fonte_descricao = criar_fonte(TAMANHO_FONTE_DESCRICAO)
    superficie_temperatura = fonte_temperatura.render(temperatura, True, (255, 255, 255))
    superficie_local = fonte_local.render(NOME_LOCAL.upper(), True, (255, 255, 255))
    camada.blit(superficie_temperatura, superficie_temperatura.get_rect(center=(LARGURA // 2, 350)))
    camada.blit(superficie_local, superficie_local.get_rect(center=(LARGURA // 2, 395)))
    if descricao:
        superficie_descricao = fonte_descricao.render(descricao, True, (255, 255, 255))
        camada.blit(superficie_descricao, superficie_descricao.get_rect(center=(LARGURA // 2, 310)))

    camada.set_alpha(max(0, min(255, int(opacidade))))
    superficie.blit(camada, (0, 0))


parametros_atuais = EXPRESSOES["normal"].copy()
parametros_inicio = parametros_atuais.copy()
expressao_atual = "normal"
inicio_transicao_expressao = pygame.time.get_ticks()
movimento_olhos = MovimentoOlhos(inicio_transicao_expressao)
estado_modo_relogio = "olhos"
inicio_modo_relogio = inicio_transicao_expressao
estado_comportamento = NENHUMA_PESSOA
inicio_observacao_desconhecida = None
estado_modo_clima = "olhos"
inicio_modo_clima = inicio_transicao_expressao
posicao_saida_clima = (0, 0)
clima_dados = None
clima_erro = False
clima_requisicao_em_curso = False
reacao_clima_ativa = False
tipo_reacao_clima = None
inicio_reacao_clima = 0
fase_reacao_clima = "fim"
dados_reacao_clima = {}


def idle_pode_ativar():
    return (
        modo in ("olhos", "clima")
        and estado_modo_clima == "olhos"
        and estado_modo_relogio == "olhos"
        and not pessoa_detectada
        and not reacao_clima_ativa
        and not clima_requisicao_em_curso
    )


def escolher_idle_tipo():
    if TESTE_IDLE is not None:
        tipo = TESTE_IDLE
        globals()["TESTE_IDLE"] = None
        return tipo

    opcoes = [
        ("olhar_lado", PROB_IDLE_OLHAR_LADO),
        ("olhar_cima", PROB_IDLE_OLHAR_CIMA),
        ("olhar_baixo", PROB_IDLE_OLHAR_BAIXO),
        ("olhar_rapido", PROB_IDLE_OLHAR_RAPIDO),
        ("piscar", PROB_IDLE_PISCAR),
        ("pensar", PROB_IDLE_PENSAR),
        ("sonolento", PROB_IDLE_SONOLENTO),
        ("curiosidade", PROB_IDLE_CURIOSIDADE),
    ]

    if idle_ultima_animacao is not None:
        opcoes = [(nome, peso * 0.35 if nome == idle_ultima_animacao else peso) for nome, peso in opcoes]

    nomes = [nome for nome, _ in opcoes]
    pesos = [max(0.01, peso) for _, peso in opcoes]
    return random.choices(nomes, weights=pesos, k=1)[0]


def cancelar_idle():
    global modo_idle, idle_ativo, idle_tipo, idle_inicio, idle_duracao, idle_direcao
    modo_idle = False
    idle_ativo = False
    idle_tipo = None
    idle_inicio = 0
    idle_duracao = 0
    idle_direcao = 1


def iniciar_idle(agora):
    global modo_idle, idle_ativo, idle_tipo, idle_inicio, idle_duracao, idle_direcao, idle_ultima_animacao
    if not idle_pode_ativar():
        cancelar_idle()
        return

    idle_tipo = escolher_idle_tipo()
    idle_ativa = {
        "olhar_lado": 1200,
        "olhar_cima": 1100,
        "olhar_baixo": 1000,
        "olhar_rapido": 520,
        "piscar": 1200,
        "pensar": 1000,
        "sonolento": 1500,
        "curiosidade": 920,
    }.get(idle_tipo, 1000)

    idle_ativo = True
    modo_idle = True
    idle_inicio = agora
    idle_duracao = idle_ativa
    idle_direcao = random.choice((-1, 1))
    idle_ultima_animacao = idle_tipo


def atualizar_idle(agora):
    global idle_proxima_acao

    if not idle_ativo or idle_tipo is None:
        if idle_pode_ativar() and agora >= idle_proxima_acao:
            iniciar_idle(agora)
        return 0, 0, 1, 1

    if not idle_pode_ativar():
        cancelar_idle()
        return 0, 0, 1, 1

    tempo = agora - idle_inicio
    if tempo >= idle_duracao:
        cancelar_idle()
        idle_proxima_acao = agora + random.randint(INTERVALO_IDLE_MIN, INTERVALO_IDLE_MAX)
        return 0, 0, 1, 1

    progresso = min(1, tempo / max(1, idle_duracao))
    deslocamento_x = 0
    deslocamento_y = 0
    fator_abertura = 1
    escala_idle = 1

    micro_x = math.sin(agora * 0.016) * 1.2
    micro_y = math.cos(agora * 0.018) * 0.8

    if idle_tipo == "olhar_lado":
        alvo = 52 * idle_direcao
        if progresso < 0.34:
            p = suavizar(progresso / 0.34)
            deslocamento_x = (alvo * p)
        elif progresso < 0.72:
            deslocamento_x = alvo
        else:
            p = suavizar((progresso - 0.72) / 0.28)
            deslocamento_x = alvo * (1 - p)
        deslocamento_x += micro_x
        deslocamento_y += micro_y
    elif idle_tipo == "olhar_cima":
        alvo = -28
        if progresso < 0.45:
            p = suavizar(progresso / 0.45)
            deslocamento_y = alvo * p
        elif progresso < 0.8:
            deslocamento_y = alvo
        else:
            p = suavizar((progresso - 0.8) / 0.2)
            deslocamento_y = alvo * (1 - p)
        deslocamento_x += micro_x
    elif idle_tipo == "olhar_baixo":
        alvo = 18
        if progresso < 0.45:
            p = suavizar(progresso / 0.45)
            deslocamento_y = alvo * p
        elif progresso < 0.8:
            deslocamento_y = alvo
        else:
            p = suavizar((progresso - 0.8) / 0.2)
            deslocamento_y = alvo * (1 - p)
        deslocamento_x += micro_x
    elif idle_tipo == "olhar_rapido":
        ciclo = (tempo / idle_duracao) * 2.8
        deslocamento_x = math.sin(ciclo * math.pi) * 18
        deslocamento_y += micro_y
    elif idle_tipo == "piscar":
        if progresso < 0.32:
            fator_abertura = 1 - suavizar(progresso / 0.32)
        elif progresso < 0.62:
            fator_abertura = 0.18
        else:
            p = suavizar((progresso - 0.62) / 0.38)
            fator_abertura = 0.18 + (1 - 0.18) * p
    elif idle_tipo == "pensar":
        alvo = -16
        if progresso < 0.6:
            p = suavizar(progresso / 0.6)
            deslocamento_y = alvo * p
        else:
            p = suavizar((progresso - 0.6) / 0.4)
            deslocamento_y = alvo * (1 - p)
        deslocamento_x += micro_x * 0.7
    elif idle_tipo == "sonolento":
        deslocamento_y = -10 + math.sin(tempo * 0.006) * 4
        escala_idle = 0.96
        deslocamento_x += micro_x * 0.5
    elif idle_tipo == "curiosidade":
        if progresso < 0.3:
            deslocamento_x = -18
        elif progresso < 0.55:
            deslocamento_x = 18
        elif progresso < 0.75:
            deslocamento_x = -10
        else:
            deslocamento_x = 0
        deslocamento_y += micro_y * 0.5

    if idle_tipo not in {"piscar"} and random.random() < 0.18:
        deslocamento_x += random.uniform(-2, 2)
        deslocamento_y += random.uniform(-1.5, 1.5)

    return deslocamento_x, deslocamento_y, fator_abertura, escala_idle


def atividade_idle_pode_ativar():
    return idle_pode_ativar()


def escolher_atividade_idle():
    opcoes = [
        ("telemovel", PROB_TELEMOVEL),
        ("horas", PROB_VER_HORAS),
        ("moeda", PROB_MOEDA),
        ("pensar", PROB_PENSAR),
        ("sono", PROB_CANSADO),
        ("musica", PROB_MUSICA),
        ("ler", PROB_LER),
        ("jogar", PROB_JOGAR),
        ("entediado", PROB_ENTEDIADO),
        ("espiar", PROB_ESPIAR),
    ]
    anterior = ultima_atividade_idle
    opcoes = [(nome, peso) for nome, peso in opcoes if nome != anterior and peso > 0]
    return random.choices(
        [nome for nome, _ in opcoes],
        weights=[peso for _, peso in opcoes],
        k=1,
    )[0]


def iniciar_atividade_idle(agora):
    global atividade_idle_atual, fase_atividade, tempo_fase
    global inicio_atividade_idle, atividade_idle_dados, ultima_atividade_idle

    if not atividade_idle_pode_ativar():
        return False

    atividade = TESTE_ATIVIDADE_IDLE or escolher_atividade_idle()
    atividade_idle_atual = atividade
    ultima_atividade_idle = atividade
    fase_atividade = "APARECER"
    tempo_fase = agora
    inicio_atividade_idle = agora
    atividade_idle_dados = {
        "objeto_x": random.randint(340, 460),
        "repeticoes": random.choice((1, 2)),
        "pagina": 0,
    }
    return True


def finalizar_atividade_idle(agora, cancelar=False):
    global atividade_idle_atual, fase_atividade, tempo_fase
    global atividade_idle_dados, proxima_atividade_idle

    atividade_idle_atual = None
    fase_atividade = None
    tempo_fase = 0
    atividade_idle_dados = {}
    proxima_atividade_idle = agora + random.randint(
        INTERVALO_ATIVIDADE_MIN, INTERVALO_ATIVIDADE_MAX
    )


def _mudar_fase_atividade(nome, agora):
    global fase_atividade, tempo_fase
    fase_atividade = nome
    tempo_fase = agora


def atualizar_atividade_idle(agora):
    global atividade_idle_dados

    if not atividade_idle_pode_ativar():
        if atividade_idle_atual is not None:
            finalizar_atividade_idle(agora, cancelar=True)
        return 0, 0, 1

    if atividade_idle_atual is None:
        if TESTE_ATIVIDADE_IDLE is not None or agora >= proxima_atividade_idle:
            iniciar_atividade_idle(agora)
        return 0, 0, 1

    tempo = agora - tempo_fase
    atividade = atividade_idle_atual
    duracoes = {
        "telemovel": {"APARECER": 350, "OLHAR": 900, "INTERAGIR": 2800, "GUARDAR": 600},
        "horas": {"APARECER": 350, "OLHAR": 700, "VER_HORA": 2200, "REACAO": 650, "GUARDAR": 600},
        "moeda": {"APARECER": 400, "OLHAR": 700, "ATIRAR": 550, "ACOMPANHAR": 850, "APANHAR": 650, "PAUSA": 450, "DESAPARECER": 450},
        "pensar": {"APARECER": 250, "OLHAR": 900, "PAUSA": 1200, "VOLTAR": 850},
        "sono": {"APARECER": 500, "FECHAR": 800, "DORMIR": 1400, "ACORDAR": 1000, "SUSTO": 350, "VOLTAR": 700},
        "musica": {"APARECER": 350, "OUVIR": 3000, "DESAPARECER": 500},
        "ler": {"APARECER": 400, "LER": 3200, "FECHAR": 650},
        "jogar": {"APARECER": 400, "JOGAR": 2800, "RESULTADO": 800, "DESAPARECER": 500},
        "entediado": {"APARECER": 250, "ESQUERDA": 700, "DIREITA": 700, "CIMA": 650, "PARADO": 1100, "FIM": 500},
        "espiar": {"APARECER": 350, "ESQUERDA": 900, "OUTRO_LADO": 450, "CENTRO": 700, "FIM": 450},
    }
    proxima = {
        "telemovel": {"APARECER": "OLHAR", "OLHAR": "INTERAGIR", "INTERAGIR": "GUARDAR", "GUARDAR": "FIM"},
        "horas": {"APARECER": "OLHAR", "OLHAR": "VER_HORA", "VER_HORA": "REACAO", "REACAO": "GUARDAR", "GUARDAR": "FIM"},
        "moeda": {"APARECER": "OLHAR", "OLHAR": "ATIRAR", "ATIRAR": "ACOMPANHAR", "ACOMPANHAR": "APANHAR", "APANHAR": "PAUSA", "PAUSA": "DESAPARECER", "DESAPARECER": "FIM"},
        "pensar": {"APARECER": "OLHAR", "OLHAR": "PAUSA", "PAUSA": "VOLTAR", "VOLTAR": "FIM"},
        "sono": {"APARECER": "FECHAR", "FECHAR": "DORMIR", "DORMIR": "ACORDAR", "ACORDAR": "SUSTO", "SUSTO": "VOLTAR", "VOLTAR": "FIM"},
        "musica": {"APARECER": "OUVIR", "OUVIR": "DESAPARECER", "DESAPARECER": "FIM"},
        "ler": {"APARECER": "LER", "LER": "FECHAR", "FECHAR": "FIM"},
        "jogar": {"APARECER": "JOGAR", "JOGAR": "RESULTADO", "RESULTADO": "DESAPARECER", "DESAPARECER": "FIM"},
        "entediado": {"APARECER": "ESQUERDA", "ESQUERDA": "DIREITA", "DIREITA": "CIMA", "CIMA": "PARADO", "PARADO": "FIM"},
        "espiar": {"APARECER": "ESQUERDA", "ESQUERDA": "OUTRO_LADO", "OUTRO_LADO": "CENTRO", "CENTRO": "FIM"},
    }
    if fase_atividade == "FIM":
        finalizar_atividade_idle(agora)
        return 0, 0, 1
    if tempo >= duracoes[atividade].get(fase_atividade, 500):
        _mudar_fase_atividade(proxima[atividade][fase_atividade], agora)
        if fase_atividade == "FIM":
            finalizar_atividade_idle(agora)
            return 0, 0, 1

    progresso = min(1, (agora - tempo_fase) / max(1, duracoes[atividade].get(fase_atividade, 500)))
    x = y = 0
    abertura = 1
    if atividade in ("telemovel", "horas", "ler", "jogar"):
        y = 28
        if fase_atividade in ("INTERAGIR", "VER_HORA", "LER", "JOGAR"):
            x = math.sin(agora * 0.012) * 12
    elif atividade == "moeda":
        x = (atividade_idle_dados["objeto_x"] - 400) * progresso
        y = -35 * math.sin(math.pi * progresso) if fase_atividade in ("ATIRAR", "ACOMPANHAR") else 18
    elif atividade == "pensar":
        y = -28 if fase_atividade in ("OLHAR", "PAUSA") else -28 * (1 - progresso)
    elif atividade == "sono":
        if fase_atividade in ("FECHAR", "DORMIR"):
            abertura = 1 - min(1, progresso)
        elif fase_atividade == "ACORDAR":
            abertura = progresso
        elif fase_atividade == "SUSTO":
            y = -18 * (1 - progresso)
    elif atividade == "musica":
        y = math.sin(agora * 0.014) * 10
        x = math.sin(agora * 0.009) * 14
    elif atividade == "entediado":
        x = {"ESQUERDA": -45, "DIREITA": 45}.get(fase_atividade, 0)
        y = -24 if fase_atividade == "CIMA" else 0
    elif atividade == "espiar":
        x = {"ESQUERDA": -48, "OUTRO_LADO": 48}.get(fase_atividade, 0)
    return x, y, abertura


def desenhar_atividade_idle(superficie, agora):
    if atividade_idle_atual is None:
        return
    x = atividade_idle_dados.get("objeto_x", 400)
    y = 365
    atividade = atividade_idle_atual
    fase = fase_atividade
    if atividade in ("telemovel", "horas"):
        pygame.draw.rect(superficie, (255, 255, 255), (x - 22, y - 34, 44, 68), 3)
        pygame.draw.circle(superficie, (255, 255, 255), (x, y + 23), 3)
        if atividade == "horas":
            texto = datetime.now().strftime("%H:%M")
            fonte = criar_fonte(24, negrito=True)
            superficie.blit(fonte.render(texto, True, (255, 255, 255)), (x - 31, y - 9))
        elif fase == "INTERAGIR":
            pygame.draw.circle(superficie, (255, 255, 255), (x + 9, y - 8), 3)
    elif atividade == "moeda":
        moeda_y = y - 45 - int(35 * math.sin(math.pi * min(1, (agora - tempo_fase) / 850))) if fase in ("ATIRAR", "ACOMPANHAR") else y
        pygame.draw.circle(superficie, (255, 255, 255), (x, moeda_y), 12, 3)
        pygame.draw.line(superficie, (255, 255, 255), (x - 4, moeda_y - 7), (x + 4, moeda_y + 7), 2)
    elif atividade == "pensar":
        pygame.draw.circle(superficie, (255, 255, 255), (520, 125), 5, 2)
        pygame.draw.circle(superficie, (255, 255, 255), (540, 105), 9, 2)
    elif atividade == "musica":
        pygame.draw.line(superficie, (255, 255, 255), (x, y - 30), (x, y + 8), 4)
        pygame.draw.line(superficie, (255, 255, 255), (x, y - 30), (x + 22, y - 38), 4)
        pygame.draw.circle(superficie, (255, 255, 255), (x - 5, y + 10), 8)
        pygame.draw.circle(superficie, (255, 255, 255), (x + 17, y + 2), 8)
    elif atividade == "ler":
        pygame.draw.polygon(superficie, (255, 255, 255), [(x - 55, y + 20), (x, y + 5), (x + 55, y + 20), (x, y + 35)], 3)
        pygame.draw.line(superficie, (255, 255, 255), (x, y + 5), (x, y + 35), 2)
        pagina = int((agora - inicio_atividade_idle) / 700) % 3
        for indice in range(pagina + 1):
            pygame.draw.line(superficie, (255, 255, 255), (x - 35, y + 17 + indice * 5), (x - 8, y + 13 + indice * 5), 2)
    elif atividade == "jogar":
        pygame.draw.rect(superficie, (255, 255, 255), (x - 45, y - 14, 90, 28), 3)
        pygame.draw.circle(superficie, (255, 255, 255), (x - 22, y), 6, 2)
        pygame.draw.circle(superficie, (255, 255, 255), (x + 20, y - 4), 3)
        pygame.draw.circle(superficie, (255, 255, 255), (x + 28, y + 5), 3)
    elif atividade == "espiar":
        pygame.draw.rect(superficie, (255, 255, 255), (0 if x < 400 else LARGURA - 22, 320, 22, 80), 3)


def atualizar_comportamento(agora):
    """Decide o modo de movimento e o humor que Kibo deve usar."""
    global estado_comportamento, inicio_observacao_desconhecida

    if not pessoa_detectada:
        estado_comportamento = NENHUMA_PESSOA
        inicio_observacao_desconhecida = None
        return "aleatorio", expressao

    if pessoa_conhecida:
        estado_comportamento = PESSOA_CONHECIDA
        inicio_observacao_desconhecida = None
        return "seguir_rosto", expressao

    if inicio_observacao_desconhecida is None:
        inicio_observacao_desconhecida = agora

    estado_comportamento = PESSOA_DESCONHECIDA
    tempo_observacao = agora - inicio_observacao_desconhecida
    if tempo_observacao < DURACAO_OBSERVACAO_DESCONHECIDA:
        return "seguir_rosto", "zangado"

    # Após observar, deixa de reagir à pessoa desconhecida e relaxa.
    return "aleatorio", "normal"


while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    agora = pygame.time.get_ticks()
    if modo == "clima" or estado_modo_clima != "olhos":
        estado_clima, progresso_clima = atualizar_modo_clima(agora)
    else:
        estado_clima, progresso_clima = "olhos", 0

    if modo == "reacao_clima" and not reacao_clima_ativa:
        iniciar_reacao_clima()

    if modo == "reacao_clima":
        progresso_reacao = atualizar_reacao_clima(agora)
    else:
        progresso_reacao = 0

    if modo == "relogio" or estado_modo_relogio != "olhos":
        estado_visual, progresso_relogio = atualizar_modo_relogio(agora)
    else:
        estado_visual, progresso_relogio = "olhos", 0

    deslocamento_x, deslocamento_y = movimento_olhos.posicao_atual
    fator_abertura = 1
    if modo == "olhos" and estado_modo_clima == "olhos":
        # Toda a lógica dos olhos fica bloqueada enquanto o relógio está ativo.
        modo_movimento, expressao_ativa = atualizar_comportamento(agora)

        if expressao_ativa not in EXPRESSOES:
            expressao_ativa = "normal"

        if expressao_ativa != expressao_atual:
            expressao_atual = expressao_ativa
            parametros_inicio = parametros_atuais.copy()
            inicio_transicao_expressao = agora

        progresso_expressao = min(
            1,
            (agora - inicio_transicao_expressao) / DURACAO_TRANSICAO_EXPRESSAO,
        )
        progresso_expressao = suavizar(progresso_expressao)
        parametros_destino = EXPRESSOES[expressao_atual]

        for nome in parametros_atuais:
            parametros_atuais[nome] = (
                parametros_inicio[nome]
                + (parametros_destino[nome] - parametros_inicio[nome]) * progresso_expressao
            )

        if modo_movimento == "seguir_rosto":
            alvo_rosto = rosto_para_movimento(rosto_x, rosto_y)
            deslocamento_x, deslocamento_y = movimento_olhos.acompanhar_rosto(
                agora, alvo_rosto, DURACAO_SEGUIR_ROSTO
            )
        else:
            deslocamento_x, deslocamento_y = movimento_olhos.atualizar(agora, expressao_atual)

        # Começar e terminar a piscada apenas no modo olhos.
        if not piscando and agora >= proxima_piscada:
            piscando = True
            inicio_piscada = agora

        if piscando and agora - inicio_piscada >= DURACAO_TOTAL:
            piscando = False
            proxima_piscada = agora + random.randint(2000, 5000)

        if piscando:
            tempo = agora - inicio_piscada

            if tempo < DURACAO_FECHAR:
                progresso = tempo / DURACAO_FECHAR
                fator_abertura = 1 - suavizar(progresso)
            elif tempo < DURACAO_FECHAR + DURACAO_FECHADO:
                fator_abertura = 0
            else:
                tempo_abrir = tempo - DURACAO_FECHAR - DURACAO_FECHADO
                progresso = tempo_abrir / DURACAO_ABRIR
                fator_abertura = suavizar(progresso)
        else:
            fator_abertura = 1

    atividade_deslocamento_x, atividade_deslocamento_y, atividade_abertura = atualizar_atividade_idle(agora)
    if atividade_idle_atual is not None:
        deslocamento_x += atividade_deslocamento_x
        deslocamento_y += atividade_deslocamento_y
        fator_abertura *= atividade_abertura
    elif (modo == "olhos" and estado_modo_clima == "olhos" and estado_modo_relogio == "olhos" and
            not pessoa_detectada and not reacao_clima_ativa and not clima_requisicao_em_curso):
        idle_desloc_x, idle_desloc_y, idle_fator_abertura, idle_escala = atualizar_idle(agora)
        deslocamento_x += idle_desloc_x
        deslocamento_y += idle_desloc_y
        fator_abertura *= idle_fator_abertura

    janela.fill((0, 0, 0))

    opacidade_relogio = 0
    escala_relogio = 0.35

    if (modo == "olhos" or
            (modo == "relogio" and estado_visual in ("olhos", "preparar", "transicao_entrada", "transicao_saida")) or
            estado_clima in ("entrada", "saida") or
            modo == "reacao_clima"):
        largura = parametros_atuais["largura"]
        altura = parametros_atuais["altura"]
        centro_y = 240 + parametros_atuais["deslocamento_y"]
        inclinacao = parametros_atuais["inclinacao"]
        arco = parametros_atuais["arco"]

        deslocamento_reacao_x = 0
        deslocamento_reacao_y = 0
        fator_abertura_reacao = 1
        if modo == "reacao_clima" and tipo_reacao_clima is not None:
            intensidade_reacao = math.sin(math.pi * progresso_reacao)
            tempo_reacao = progresso_reacao * duracao_reacao_clima(tipo_reacao_clima)

            if tipo_reacao_clima == "frio":
                deslocamento_reacao_x = math.sin(tempo_reacao * 0.045) * AMPLITUDE_TREMO_FRIO * intensidade_reacao
                fator_abertura_reacao = 1.0
            elif tipo_reacao_clima == "calor":
                deslocamento_reacao_x = 35 * math.cos(math.pi * progresso_reacao) * intensidade_reacao
                deslocamento_reacao_y = -25 * intensidade_reacao
                fator_abertura_reacao = 0.78
            elif tipo_reacao_clima == "chuva":
                deslocamento_reacao_y = -22 * intensidade_reacao
                deslocamento_reacao_x = math.sin(tempo_reacao * 0.012) * 6 * intensidade_reacao
                fator_abertura_reacao = 0.9
            elif tipo_reacao_clima == "trovoada":
                deslocamento_reacao_x = math.sin(tempo_reacao * 0.05) * 18 * intensidade_reacao
                parametros_reacao = EXPRESSOES["surpreso"]
                largura = parametros_reacao["largura"]
                altura = parametros_reacao["altura"]
                centro_y = 240 + parametros_reacao["deslocamento_y"]
                inclinacao = parametros_reacao["inclinacao"]
                arco = parametros_reacao["arco"]
            elif tipo_reacao_clima == "neve":
                deslocamento_reacao_y = -24 * intensidade_reacao
                deslocamento_reacao_x = math.sin(tempo_reacao * 0.008) * 10 * intensidade_reacao
            elif tipo_reacao_clima == "nevoeiro":
                deslocamento_reacao_x = math.sin(tempo_reacao * 0.004) * 20 * intensidade_reacao
                fator_abertura_reacao = 0.92

            deslocamento_x += deslocamento_reacao_x
            deslocamento_y += deslocamento_reacao_y
            fator_abertura = fator_abertura_reacao

        escala_olhos = 1
        escala_olhos_x = 1
        escala_olhos_y = 1
        if tipo_reacao_clima == "calor":
            escala_olhos = 0.82
            escala_olhos_x = 0.82
            escala_olhos_y = 0.82
        opacidade_olhos = 255
        if estado_visual == "transicao_entrada":
            transicao = suavizar(progresso_relogio)
            escala_olhos = 1 - 0.65 * transicao
            escala_olhos_x = escala_olhos
            escala_olhos_y = escala_olhos
            opacidade_olhos = 255 * (1 - transicao)
            opacidade_relogio = 255 * transicao
            escala_relogio = 0.35 + 0.65 * transicao
        elif estado_visual == "transicao_saida":
            transicao = suavizar(progresso_relogio)
            escala_olhos = 0.35 + 0.65 * transicao
            escala_olhos_x = escala_olhos
            escala_olhos_y = escala_olhos
            opacidade_olhos = 255 * transicao
            opacidade_relogio = 255 * (1 - transicao)
            escala_relogio = 1 - 0.65 * transicao
        elif modo != "reacao_clima" and estado_clima == "entrada":
            transicao = suavizar(progresso_clima)
            escala_olhos = 1
            escala_olhos_x = 1 - 0.45 * transicao
            opacidade_olhos = 255 * (1 - transicao)
        elif modo != "reacao_clima" and estado_clima == "saida":
            transicao = suavizar(progresso_clima)
            escala_olhos = 1
            escala_olhos_x = 0.55 + 0.45 * transicao
            opacidade_olhos = 255 * transicao

        centro_relogio_x = LARGURA / 2
        centro_relogio_y = ALTURA / 2
        olhos_centro_x = (270 + 530) / 2 + deslocamento_x
        olhos_centro_y = centro_y + deslocamento_y
        centro_x_esquerdo = 270 + deslocamento_x
        centro_x_direito = 530 + deslocamento_x

        if estado_visual == "transicao_entrada":
            centro_x_esquerdo += (centro_relogio_x - olhos_centro_x) * transicao
            centro_x_direito += (centro_relogio_x - olhos_centro_x) * transicao
            olhos_centro_y += (centro_relogio_y - olhos_centro_y) * transicao
        elif estado_visual == "transicao_saida":
            centro_x_esquerdo = centro_relogio_x + (centro_x_esquerdo - centro_relogio_x) * transicao
            centro_x_direito = centro_relogio_x + (centro_x_direito - centro_relogio_x) * transicao
            olhos_centro_y = centro_relogio_y + (olhos_centro_y - centro_relogio_y) * transicao
        elif modo != "reacao_clima" and estado_clima == "entrada":
            # Os olhos caem para baixo e abrem espaço para a meteorologia.
            olhos_centro_y += ALTURA * 0.75 * transicao
        elif modo != "reacao_clima" and estado_clima == "saida":
            # Os olhos entram de cima e caem até à posição original.
            deslocamento_x, deslocamento_y = posicao_saida_clima
            centro_x_esquerdo = 270 + deslocamento_x
            centro_x_direito = 530 + deslocamento_x
            olhos_centro_y = centro_y + deslocamento_y - ALTURA * 0.75 * (1 - transicao)

        desenhar_olho(
            janela,
            centro_x_esquerdo,
            olhos_centro_y,
            largura,
            altura,
            inclinacao,
            arco,
            fator_abertura,
            escala_olhos,
            opacidade_olhos,
            escala_x=escala_olhos_x,
            escala_y=escala_olhos_y,
        )
        desenhar_olho(
            janela,
            centro_x_direito,
            olhos_centro_y,
            largura,
            altura,
            -inclinacao,
            arco,
            fator_abertura,
            escala_olhos,
            opacidade_olhos,
            escala_x=escala_olhos_x,
            escala_y=escala_olhos_y,
        )

    if modo == "reacao_clima" and tipo_reacao_clima is not None:
        desenhar_reacao_clima(janela, agora, tipo_reacao_clima, progresso_reacao)

    if atividade_idle_atual is not None:
        desenhar_atividade_idle(janela, agora)

    if modo == "relogio" and estado_visual == "relogio":
        opacidade_relogio = 255
        escala_relogio = 1
    elif modo == "relogio" and estado_visual == "preparar":
        opacidade_relogio = 0
        escala_relogio = 0.35

    if opacidade_relogio > 0:
        desenhar_relogio(janela, opacidade_relogio, escala_relogio)
    elif modo != "reacao_clima" and estado_clima in ("entrada", "visivel", "saida"):
        if estado_clima == "entrada":
            opacidade_clima = 255 * suavizar(progresso_clima)
        elif estado_clima == "saida":
            opacidade_clima = 255 * (1 - suavizar(progresso_clima))
        else:
            opacidade_clima = 255
        desenhar_clima(janela, agora, clima_dados, opacidade_clima)

    pygame.display.flip()
    relogio.tick(60)