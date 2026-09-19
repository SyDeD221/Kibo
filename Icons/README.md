# Icones do Kibo

Os icones devem ser obtidos do repositorio oficial da Google:

https://github.com/google/material-design-icons

Prefira Material Symbols ou Material Symbols Rounded. Mantenha os SVGs originais
como fonte e use PNGs locais de alta resolucao para o Kibo.

## Estrutura

Coloque os icones meteorologicos em `icons/weather/`, por exemplo:

```text
icons/png/weather/clear_day.png
icons/png/weather/cloud.png
icons/png/weather/foggy.png
icons/png/weather/rainy.png
icons/png/weather/weather_snowy.png
icons/png/weather/thunderstorm.png
```

Os PNGs podem ter `96x96`, `128x128`, `256x256` ou `512x512`. O sistema mantém
o PNG original em memoria e aplica `smoothscale` apenas para criar o tamanho
necessario no ecrã.

Os ficheiros devem acompanhar a licenca do repositorio de origem. Os Material
Design Icons sao distribuidos sob Apache License 2.0; mantenha a informacao de
licenca ao redistribuir os ficheiros.

## Utilizacao

```python
from icons import carregar_icone, desenhar_icone

icone = carregar_icone("weather/cloud", 48)
if icone is not None:
    tela.blit(icone, (100, 100))

desenhar_icone(tela, "weather/cloud", 100, 100, tamanho=48)
```

O modulo carrega cada combinacao de nome, tamanho e cor uma vez. Um ficheiro
ausente gera um aviso no terminal e devolve `None`, sem interromper o Kibo.

## PNGs convertidos

O Kibo nao converte SVGs nem instala conversores. Coloque manualmente os PNGs
de alta resolucao em `icons/png/weather/`. Os SVGs originais podem continuar
guardados em `icons/weather/` como fonte. O programa usa apenas `pygame.image.load()`
para carregar os PNGs e nao depende de CairoSVG ou de runtimes nativos.