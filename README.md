# Oficina Pyxel — Coleta da Moeda

Oficina prática de programação em Python na qual os alunos são guiados na construção conjunta de um jogo, partindo dos conceitos mais básicos e avançando gradualmente para movimentação, gravidade, colisões, uso de sprites com animações e lógica de jogo.

## Duração

**2h30min**

## Objetivos

Durante a oficina, os alunos irão trabalhar com:

* Loop principal de um jogo
* Eventos e entrada do teclado
* `Clock` e controle do tempo
* `Rect` e coordenadas
* Movimentação
* Gravidade e pulo
* Colisões
* Sprites e animações
* Listas e múltiplos objetos
* Estados do jogo
* Salas e transições
* Condições de vitória e derrota

---

# 1. Preparação

## Requisitos

* Python 3
* Editor de código
* Terminal

## Instalação

Instale o Pygame:

```bash
python -m pip install pygame
```

Teste a instalação:

```bash
python -c "import pygame; print(pygame.version.ver)"
```

Se a versão do Pygame aparecer no terminal, o ambiente está pronto.

---

# 2. Estrutura do projeto

No início da oficina, o projeto terá esta estrutura:

```text
coleta-da-moeda/
│
├── helper.py
├── base.py
└── sprites/
    ├── personagens/
    │   └── proto/
    ├── inimigos/
    └── cenario/
```

O arquivo `helper.py` contém funções auxiliares para esconder detalhes técnicos do Pygame.

O arquivo `base.py` será usado como ponto de partida para a construção do jogo.

---

# 3. `helper.py`

O `helper.py` já vem pronto e será utilizado durante toda a oficina.

Ele contém ferramentas para:

* Criar a janela
* Criar fontes
* Desenhar textos
* Localizar arquivos
* Carregar imagens
* Carregar spritesheets
* Criar animações
* Reproduzir animações
* Repetir texturas

> Os alunos não precisam implementar essas funções durante a oficina. O objetivo é utilizar essas ferramentas para construir a lógica do jogo.

```python
import os
import pygame


PASTA_BASE = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# CORES
# ============================================================

BRANCO = (245, 245, 245)
PRETO = (30, 30, 30)
AZUL = (90, 100, 255)
VERDE = (40, 200, 90)
VERMELHO = (255, 70, 70)
AMARELO = (255, 215, 0)


# ============================================================
# JANELA E TEXTO
# ============================================================

def criar_janela(largura, altura, titulo="Jogo"):
    pygame.init()

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption(titulo)

    return tela


def criar_fonte(tamanho, negrito=False, nome="poppins"):
    return pygame.font.SysFont(
        nome,
        tamanho,
        bold=negrito
    )


def desenhar_texto(tela, texto, fonte, cor, x, y):
    imagem = fonte.render(texto, True, cor)

    retangulo = imagem.get_rect(
        center=(x, y)
    )

    tela.blit(imagem, retangulo)


# ============================================================
# CAMINHOS
# ============================================================

def caminho(*partes):
    return os.path.join(
        PASTA_BASE,
        *partes
    )


def _exigir_janela():
    if not pygame.display.get_surface():
        raise RuntimeError(
            "Crie a janela antes de carregar imagens."
        )


# ============================================================
# IMAGENS
# ============================================================

def carregar_imagem(arquivo, tamanho=None):

    _exigir_janela()

    caminho_arquivo = caminho(arquivo)

    if not os.path.exists(caminho_arquivo):
        return None

    imagem = pygame.image.load(
        caminho_arquivo
    ).convert_alpha()

    if tamanho:
        imagem = pygame.transform.scale(
            imagem,
            tamanho
        )

    return imagem


def carregar_frames(
    arquivo,
    frame_w,
    frame_h=None,
    tamanho=None
):

    _exigir_janela()

    imagem = pygame.image.load(
        caminho(arquivo)
    ).convert_alpha()

    largura = imagem.get_width()
    altura = imagem.get_height()

    if frame_h is None:
        frame_h = altura

    frames = []

    for x in range(0, largura, frame_w):

        frame = imagem.subsurface(
            pygame.Rect(
                x,
                0,
                frame_w,
                frame_h
            )
        ).copy()

        if tamanho:
            frame = pygame.transform.scale(
                frame,
                tamanho
            )

        frames.append(frame)

    return frames


def carregar_frames_auto(
    arquivo,
    tamanho,
    remover_fundo_branco=False,
    ignorar_rodape=0.0,
    limiar_branco=235
):

    _exigir_janela()

    imagem = pygame.image.load(
        caminho(arquivo)
    ).convert_alpha()

    largura = imagem.get_width()
    altura = imagem.get_height()

    limite_y = int(
        altura * (1 - ignorar_rodape)
    )

    colunas_visiveis = []

    for x in range(largura):

        encontrou = False

        for y in range(limite_y):

            r, g, b, a = imagem.get_at((x, y))

            if a > 0:

                if not remover_fundo_branco:
                    encontrou = True
                    break

                if (
                    r < limiar_branco
                    or g < limiar_branco
                    or b < limiar_branco
                ):
                    encontrou = True
                    break

        colunas_visiveis.append(encontrou)

    grupos = []
    inicio = None

    for x, visivel in enumerate(colunas_visiveis):

        if visivel and inicio is None:
            inicio = x

        elif not visivel and inicio is not None:
            grupos.append((inicio, x))
            inicio = None

    if inicio is not None:
        grupos.append((inicio, largura))

    frames = []

    for esquerda, direita in grupos:

        frame = imagem.subsurface(
            pygame.Rect(
                esquerda,
                0,
                direita - esquerda,
                limite_y
            )
        ).copy()

        frame = pygame.transform.scale(
            frame,
            tamanho
        )

        frames.append(frame)

    return frames


# ============================================================
# ANIMAÇÃO
# ============================================================

def frame_por_tempo(frames, ms_por_frame=100):

    if not frames:
        return None

    tempo = pygame.time.get_ticks()

    indice = (
        tempo // ms_por_frame
    ) % len(frames)

    return frames[indice]


class Animador:

    def __init__(
        self,
        animacoes,
        ms_por_frame=100
    ):

        self.animacoes = animacoes
        self.estado = next(iter(animacoes))

        self.ms_por_frame = ms_por_frame

        self.indice = 0
        self.tempo = 0

        self.olhando_direita = True

    def definir_estado(self, estado):

        if estado != self.estado:

            self.estado = estado
            self.indice = 0
            self.tempo = 0

    def atualizar(self, dt_ms):

        frames = self.animacoes.get(
            self.estado,
            []
        )

        if not frames:
            return

        self.tempo += dt_ms

        while self.tempo >= self.ms_por_frame:

            self.tempo -= self.ms_por_frame
            self.indice += 1

            if self.indice >= len(frames):
                self.indice = 0

    def imagem_atual(self):

        frames = self.animacoes.get(
            self.estado,
            []
        )

        if not frames:
            return None

        imagem = frames[self.indice]

        if self.olhando_direita:
            return imagem

        return pygame.transform.flip(
            imagem,
            True,
            False
        )


# ============================================================
# TEXTURAS
# ============================================================

def desenhar_textura(
    tela,
    imagem,
    retangulo
):

    if imagem is None:
        return

    largura = imagem.get_width()
    altura = imagem.get_height()

    for y in range(
        retangulo.top,
        retangulo.bottom,
        altura
    ):

        for x in range(
            retangulo.left,
            retangulo.right,
            largura
        ):

            tela.blit(
                imagem,
                (x, y)
            )
```

---

# 4. `base.py`

O `base.py` começa com apenas a estrutura básica do jogo.

```python
import sys
import pygame

from helper import (
    criar_janela,
    criar_fonte,
    desenhar_texto,
    BRANCO,
    PRETO,
    AZUL,
    VERDE,
    VERMELHO,
    AMARELO
)


# ============================================================
# CONFIGURAÇÕES
# ============================================================

LARGURA = 800
ALTURA = 400

tela = criar_janela(
    LARGURA,
    ALTURA,
    "Coleta da Moeda"
)


# ============================================================
# SPRITES
# ============================================================

SPRITE_PERSONAGEM = "sprites/personagens/proto/"

SPRITE_INIMIGO = None

SPRITE_CHAO = None

SPRITE_PLATAFORMA = None


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    clock = pygame.time.Clock()

    # TODO:
    # Criar estado do jogo

    # TODO:
    # Criar jogador

    # TODO:
    # Criar chão

    # TODO:
    # Criar moeda

    # TODO:
    # Criar inimigo


    while True:

        dt_ms = clock.tick(60)

        tela.fill(BRANCO)


        # ====================================================
        # EVENTOS
        # ====================================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            # TODO:
            # Eventos de teclado


        # ====================================================
        # LÓGICA
        # ====================================================

        # TODO:
        # Movimento

        # TODO:
        # Gravidade

        # TODO:
        # Pulo

        # TODO:
        # Colisões

        # TODO:
        # Moeda

        # TODO:
        # Inimigo


        # ====================================================
        # DESENHO
        # ====================================================

        # TODO:
        # Desenhar jogador

        # TODO:
        # Desenhar chão

        # TODO:
        # Desenhar moeda

        # TODO:
        # Desenhar inimigo


        pygame.display.flip()


if __name__ == "__main__":
    main()
```

---

# 5. Roteiro da oficina

## 0:00–0:10 — Janela e loop

Começamos entendendo:

* `while True`
* eventos
* `Clock`
* FPS
* atualização da tela

O objetivo é ter uma janela funcionando.

---

## 0:10–0:20 — Jogador

Criar o jogador usando `pygame.Rect`:

```python
jogador = pygame.Rect(
    100,
    300,
    40,
    50
)
```

Desenhar:

```python
pygame.draw.rect(
    tela,
    AZUL,
    jogador
)
```

---

## 0:20–0:35 — Movimentação

Ler o teclado:

```python
teclas = pygame.key.get_pressed()

if teclas[pygame.K_a]:
    jogador.x -= 5

if teclas[pygame.K_d]:
    jogador.x += 5
```

Conceitos:

* entrada do usuário
* coordenadas
* alteração da posição

---

## 0:35–0:40 — Chão

Criar:

```python
chao = pygame.Rect(
    0,
    350,
    LARGURA,
    50
)
```

Desenhar:

```python
pygame.draw.rect(
    tela,
    VERDE,
    chao
)
```

---

## 0:40–0:50 — Gravidade

Criar:

```python
gravidade = 1200
jogador_vel_y = 0
```

Converter o tempo:

```python
dt = dt_ms / 1000
```

Aplicar a gravidade:

```python
jogador_vel_y += gravidade * dt
jogador.y += jogador_vel_y * dt
```

A ideia:

```text
velocidade += gravidade × tempo
posição += velocidade × tempo
```

---

## 0:50–1:05 — Colisão e pulo

Colisão com o chão:

```python
if jogador.colliderect(chao):
    jogador.bottom = chao.top
    jogador_vel_y = 0
```

Pulo:

```python
pulando = False
```

No evento:

```python
if evento.type == pygame.KEYDOWN:

    if evento.key == pygame.K_SPACE and not pulando:
        jogador_vel_y = -500
        pulando = True
```

Ao tocar o chão:

```python
pulando = False
```

### Checkpoint

Neste momento o jogo já possui:

* movimento
* gravidade
* pulo
* chão
* colisão

---

## 1:05–1:15 — Sprite do personagem

Substituir o retângulo pelo personagem.

O carregamento das imagens é feito pelo `helper.py`, permitindo que os alunos se concentrem na utilização do sprite.

---

## 1:15–1:25 — Animações

Definir a animação de acordo com o estado do jogador:

```python
if jogador_vel_y < 0:
    animador.definir_estado("pulando")

elif jogador_vel_y > 0:
    animador.definir_estado("caindo")

elif teclas[pygame.K_a] or teclas[pygame.K_d]:
    animador.definir_estado("correndo")

else:
    animador.definir_estado("parado")
```

Atualizar:

```python
animador.atualizar(dt_ms)

imagem = animador.imagem_atual()

tela.blit(
    imagem,
    jogador
)
```

---

## 1:25–1:40 — Moeda

Criar:

```python
moeda = pygame.Rect(
    650,
    300,
    30,
    30
)

moeda_coletada = False
```

Detectar a coleta:

```python
if not moeda_coletada:
    
    if jogador.colliderect(moeda):
        moeda_coletada = True
```

Adicionar contador:

```python
moedas_coletadas = 0
```

E:

```python
if not moeda_coletada and jogador.colliderect(moeda):
    moeda_coletada = True
    moedas_coletadas += 1
```

Mostrar:

```python
desenhar_texto(
    tela,
    f"Moedas: {moedas_coletadas}/1",
    fonte,
    PRETO,
    100,
    30
)
```

---

## 1:40–1:55 — Inimigo

Criar:

```python
inimigo = pygame.Rect(
    400,
    300,
    40,
    50
)

inimigo_vel = 3
```

Movimentar:

```python
inimigo.x += inimigo_vel
```

Fazer o inimigo voltar:

```python
if inimigo.left <= 300 or inimigo.right >= 550:
    inimigo_vel *= -1
```

Colisão:

```python
if jogador.colliderect(inimigo):
    estado = "DERROTA"
```

---

## 1:55–2:00 — Estados do jogo

Criar:

```python
INICIO = "INICIO"
JOGANDO = "JOGANDO"
DERROTA = "DERROTA"
VITORIA = "VITORIA"

estado = INICIO
```

Organizar:

```python
if estado == INICIO:
    # tela inicial

elif estado == JOGANDO:
    # jogo

elif estado == DERROTA:
    # derrota

elif estado == VITORIA:
    # vitória
```

---

## 2:00–2:10 — Salas

Criar uma lista de salas:

```python
salas = [
    {
        "moeda": (650, 300),
        "inimigos": []
    },
    {
        "moeda": (250, 250),
        "inimigos": []
    },
    {
        "moeda": (650, 250),
        "inimigos": []
    }
]
```

Sala atual:

```python
sala_atual = 0
```

Transição pela borda direita:

```python
if jogador.right >= LARGURA:

    if sala_atual < len(salas) - 1:

        sala_atual += 1

        jogador.left = 20
```

---

## 2:10–2:20 — Plataformas

Criar:

```python
plataformas = [
    pygame.Rect(150, 300, 120, 20),
    pygame.Rect(350, 250, 120, 20),
    pygame.Rect(550, 300, 120, 20)
]
```

Desenhar todas:

```python
for plataforma in plataformas:
    pygame.draw.rect(
        tela,
        VERDE,
        plataforma
    )
```

Colisão:

```python
for plataforma in plataformas:

    if (
        jogador.colliderect(plataforma)
        and jogador_vel_y >= 0
        and jogador.bottom - jogador_vel_y
            <= plataforma.top + 5
    ):
        jogador.bottom = plataforma.top
        jogador_vel_y = 0
        pulando = False
```

---

## 2:20–2:25 — Vitória

Verificar se todas as moedas foram coletadas:

```python
if moedas_coletadas == total_moedas:
    estado = VITORIA
```

Mostrar:

```python
if estado == VITORIA:

    desenhar_texto(
        tela,
        "VOCÊ VENCEU!",
        fonte_grande,
        PRETO,
        LARGURA // 2,
        ALTURA // 2
    )
```

---

## 2:25–2:30 — Teste e exploração

Nos minutos finais, os alunos podem modificar os valores do jogo.

### Gravidade

```python
gravidade = 800
```

### Força do pulo

```python
jogador_vel_y = -600
```

### Velocidade do inimigo

```python
inimigo_vel = 5
```

A ideia é experimentar e observar como pequenas mudanças no código alteram o comportamento do jogo.

---

# 6. Resultado esperado

Ao final da oficina, o jogo terá:

* [x] Janela e loop principal
* [x] Movimentação do jogador
* [x] Gravidade
* [x] Pulo
* [x] Colisões
* [x] Sprite do personagem
* [x] Animações
* [x] Moedas
* [x] Contador de moedas
* [x] Inimigo
* [x] Condição de derrota
* [x] Múltiplas salas
* [x] Transição entre salas
* [x] Plataformas
* [x] Condição de vitória

A construção começa em `base.py` e, ao longo da oficina, evolui para o jogo completo.
::
