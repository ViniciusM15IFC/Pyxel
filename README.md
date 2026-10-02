# Oficina Pyxel — Coleta da Moeda

Oficina prática de programação em Python na qual os alunos constroem um jogo, avançando de conceitos básicos para movimentação, gravidade, colisões, sprites, animações e lógica de jogo.

## Duração

**2h30min**

## Objetivos

* Loop principal
* Eventos e teclado
* `Clock` e tempo
* `Rect` e coordenadas
* Movimentação
* Gravidade e pulo
* Colisões
* Sprites e animações
* Listas e múltiplos objetos
* Estados do jogo
* Salas e transições
* Vitória e derrota

---

# 1. Preparação

## Requisitos

* Python 3
* Editor de código
* Terminal

## Instalação

```bash
python -m pip install pygame
```

Teste:

```bash
python -c "import pygame; print(pygame.version.ver)"
```

---

# 2. Estrutura

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

* `helper.py` — funções auxiliares.
* `base.py` — ponto de partida do jogo.

---

# 3. `helper.py`

Arquivo fornecido pela oficina.

<details>
<summary>📄 Clique para visualizar e copiar</summary>

```python
import os
import pygame


PASTA_BASE = os.path.dirname(os.path.abspath(__file__))


# =========================
# CORES
# =========================

BRANCO = (245, 245, 245)
PRETO = (30, 30, 30)
AZUL = (90, 100, 255)
VERDE = (40, 200, 90)
VERMELHO = (255, 70, 70)
AMARELO = (255, 215, 0)


# =========================
# JANELA E TEXTO
# =========================

def criar_janela(largura, altura, titulo="Jogo"):
    pygame.init()

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption(titulo)

    return tela


def criar_fonte(tamanho, negrito=False, nome="poppins"):
    pygame.font.init()

    try:
        return pygame.font.SysFont(nome, tamanho, bold=negrito)
    except:
        return pygame.font.Font(None, tamanho)


def desenhar_texto(tela, texto, fonte, cor, x, y):
    imagem = fonte.render(texto, True, cor)

    retangulo = imagem.get_rect(
        center=(x, y)
    )

    tela.blit(imagem, retangulo)


# =========================
# CAMINHOS
# =========================

def caminho(*partes):
    return os.path.join(PASTA_BASE, *partes)


def _exigir_janela():
    if not pygame.display.get_surface():
        raise RuntimeError(
            "A janela do pygame precisa ser criada antes."
        )


# =========================
# IMAGENS
# =========================

def carregar_imagem(arquivo, tamanho=None):
    """
    Carrega uma imagem.

    Se o arquivo não existir, retorna None.
    tamanho -> (largura, altura) opcional.
    """
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


def desenhar_textura(tela, imagem, retangulo):
    """
    Repete uma imagem para preencher um retângulo.
    """
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
            tela.blit(imagem, (x, y))


# =========================
# SPRITES
# =========================

def carregar_frames(
    arquivo,
    frame_w,
    frame_h=None,
    tamanho=None
):
    _exigir_janela()

    caminho_arquivo = caminho(arquivo)

    if not os.path.exists(caminho_arquivo):
        return []

    imagem = pygame.image.load(
        caminho_arquivo
    ).convert_alpha()

    if frame_h is None:
        frame_h = imagem.get_height()

    quantidade = imagem.get_width() // frame_w

    frames = []

    for i in range(quantidade):
        frame = imagem.subsurface(
            pygame.Rect(
                i * frame_w,
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
    """
    Carrega spritesheet automaticamente.
    """
    _exigir_janela()

    caminho_arquivo = caminho(arquivo)

    if not os.path.exists(caminho_arquivo):
        return []

    imagem = pygame.image.load(
        caminho_arquivo
    ).convert_alpha()

    largura, altura = imagem.get_size()

    limite_altura = int(
        altura * (1 - ignorar_rodape)
    )

    colunas = []

    for x in range(largura):
        tem_conteudo = False

        for y in range(limite_altura):
            r, g, b, a = imagem.get_at((x, y))

            if a > 0:
                if not remover_fundo_branco:
                    tem_conteudo = True
                    break

                if (
                    r < limiar_branco
                    or g < limiar_branco
                    or b < limiar_branco
                ):
                    tem_conteudo = True
                    break

        colunas.append(tem_conteudo)

    grupos = []
    inicio = None

    for x, tem_conteudo in enumerate(colunas):
        if tem_conteudo and inicio is None:
            inicio = x

        elif not tem_conteudo and inicio is not None:
            grupos.append((inicio, x))
            inicio = None

    if inicio is not None:
        grupos.append((inicio, largura))

    frames = []

    for esquerda, direita in grupos:
        largura_frame = direita - esquerda

        if largura_frame <= 0:
            continue

        frame = imagem.subsurface(
            pygame.Rect(
                esquerda,
                0,
                largura_frame,
                limite_altura
            )
        ).copy()

        if remover_fundo_branco:
            pixels = pygame.PixelArray(frame)

            for x in range(frame.get_width()):
                for y in range(frame.get_height()):
                    cor = frame.unmap_rgb(
                        pixels[x, y]
                    )

                    if (
                        cor.r >= limiar_branco
                        and cor.g >= limiar_branco
                        and cor.b >= limiar_branco
                    ):
                        pixels[x, y] = (
                            0, 0, 0, 0
                        )

            del pixels

        retangulo = frame.get_bounding_rect()

        if retangulo.width > 0 and retangulo.height > 0:
            frame = frame.subsurface(
                retangulo
            ).copy()

        frame = pygame.transform.scale(
            frame,
            tamanho
        )

        frames.append(frame)

    return frames


def frame_por_tempo(frames, ms_por_frame=100):
    if not frames:
        return None

    tempo = pygame.time.get_ticks()

    indice = (
        tempo // ms_por_frame
    ) % len(frames)

    return frames[indice]


# =========================
# ANIMAÇÃO
# =========================

class Animador:

    def __init__(
        self,
        animacoes,
        ms_por_frame=100
    ):
        self.animacoes = animacoes
        self.ms_por_frame = ms_por_frame

        self.estado = None
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

        if self.tempo >= self.ms_por_frame:
            self.tempo = 0
            self.indice = (
                self.indice + 1
            ) % len(frames)

    def imagem_atual(self):
        frames = self.animacoes.get(
            self.estado,
            []
        )

        if not frames:
            return None

        imagem = frames[self.indice]

        if not self.olhando_direita:
            imagem = pygame.transform.flip(
                imagem,
                True,
                False
            )

        return imagem
```

</details>

---

# 4. `base.py`

Ponto de partida:

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

SPRITE_PERSONAGEM = None

SPRITE_INIMIGO = None

SPRITE_CHAO = None

SPRITE_PLATAFORMA = None


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    clock = pygame.time.Clock()

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


        # ====================================================
        # LÓGICA
        # ====================================================


        # ====================================================
        # DESENHO
        # ====================================================


        pygame.display.flip()


if __name__ == "__main__":
    main()
```

---

# 5. Roteiro da oficina

## 0:00–0:10 — Janela e loop

* `while`
* Eventos
* `Clock`
* FPS
* Atualização da tela

---

## 0:10–0:20 — Jogador

```python
jogador = pygame.Rect(
    100,
    300,
    40,
    50
)
```

```python
pygame.draw.rect(
    tela,
    AZUL,
    jogador
)
```

* `Rect`
* Coordenadas
* Desenho

---

## 0:20–0:35 — Movimentação

```python
teclas = pygame.key.get_pressed()

if teclas[pygame.K_a]:
    jogador.x -= 5

if teclas[pygame.K_d]:
    jogador.x += 5
```

* Teclado
* Coordenadas
* Posição

---

## 0:35–0:40 — Chão

```python
chao = pygame.Rect(
    0,
    350,
    LARGURA,
    50
)
```

```python
pygame.draw.rect(
    tela,
    VERDE,
    chao
)
```

---

## 0:40–0:50 — Gravidade

```python
gravidade = 1200
jogador_vel_y = 0
```

```python
dt = dt_ms / 1000
```

```python
jogador_vel_y += gravidade * dt
jogador.y += jogador_vel_y * dt
```

```text
velocidade += gravidade × tempo
posição += velocidade × tempo
```

---

## 0:50–1:05 — Colisão e pulo

```python
if jogador.colliderect(chao):
    jogador.bottom = chao.top
    jogador_vel_y = 0
```

```python
pulando = False
```

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

* Movimento
* Gravidade
* Pulo
* Chão
* Colisão

---

## 1:05–1:15 — Sprite

Substituir o retângulo pelo personagem.

---

## 1:15–1:25 — Animações

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

```python
moeda = pygame.Rect(
    650,
    300,
    30,
    30
)

moeda_coletada = False
```

```python
if not moeda_coletada:

    if jogador.colliderect(moeda):
        moeda_coletada = True
```

Contador:

```python
moedas_coletadas = 0
```

```python
if not moeda_coletada and jogador.colliderect(moeda):
    moeda_coletada = True
    moedas_coletadas += 1
```

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

```python
inimigo = pygame.Rect(
    400,
    300,
    40,
    50
)

inimigo_vel = 3
```

```python
inimigo.x += inimigo_vel
```

```python
if inimigo.left <= 300 or inimigo.right >= 550:
    inimigo_vel *= -1
```

```python
if jogador.colliderect(inimigo):
    estado = "DERROTA"
```

---

## 1:55–2:00 — Estados

```python
INICIO = "INICIO"
JOGANDO = "JOGANDO"
DERROTA = "DERROTA"
VITORIA = "VITORIA"

estado = INICIO
```

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

```python
sala_atual = 0
```

Transição:

```python
if jogador.right >= LARGURA:

    if sala_atual < len(salas) - 1:

        sala_atual += 1

        jogador.left = 20
```

---

## 2:10–2:20 — Plataformas

```python
plataformas = [
    pygame.Rect(150, 300, 120, 20),
    pygame.Rect(350, 250, 120, 20),
    pygame.Rect(550, 300, 120, 20)
]
```

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

```python
if moedas_coletadas == total_moedas:
    estado = VITORIA
```

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

## 2:25–2:30 — Teste

### Gravidade

```python
gravidade = 800
```

### Pulo

```python
jogador_vel_y = -600
```

### Inimigo

```python
inimigo_vel = 5
```

---

# 6. Resultado

* [x] Janela e loop
* [x] Movimentação
* [x] Gravidade
* [x] Pulo
* [x] Colisões
* [x] Sprite
* [x] Animações
* [x] Moedas
* [x] Contador
* [x] Inimigo
* [x] Derrota
* [x] Salas
* [x] Transições
* [x] Plataformas
* [x] Vitória

**`base.py` → desenvolvimento gradual → jogo completo**
