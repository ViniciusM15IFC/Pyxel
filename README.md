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
* Salas e transições (nos dois sentidos)
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
    ├── moeda/
    └── cenario/
```

* `helper.py` — funções auxiliares fornecidas pela oficina.
* `base.py` — arquivo desenvolvido durante a oficina.

---

# 3. `helper.py`

Arquivo fornecido pela oficina. Os alunos não precisam mexer aqui.

<details>
<summary>📄 Código do helper.py</summary>

```python
"""
helper.py - funções prontas para a oficina de jogos com Pygame.

Os alunos NÃO precisam mexer aqui: só importar e chamar.

Ordem obrigatória: criar_janela(...) primeiro, depois carregar_* (os sprites
usam convert_alpha(), que exige uma janela já criada).
"""
import os
import pygame

PASTA_BASE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------
# CORES
# --------------------------------------------------------------------
BRANCO = (245, 245, 245)
PRETO = (30, 30, 30)
AZUL = (90, 100, 255)
VERDE = (40, 200, 90)
VERMELHO = (255, 70, 70)
AMARELO = (255, 215, 0)


# --------------------------------------------------------------------
# JANELA, FONTES E TEXTO
# --------------------------------------------------------------------
def criar_janela(largura, altura, titulo="Jogo"):
    """Inicializa o Pygame, cria a janela e devolve a tela (Surface)."""
    pygame.init()
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption(titulo)
    return tela


def criar_fonte(tamanho, negrito=False, nome="poppins"):
    """Cria uma fonte do sistema (se 'nome' não existir, o Pygame usa a padrão)."""
    return pygame.font.SysFont(nome, tamanho, bold=negrito)


def desenhar_texto(tela, texto, fonte, cor, x, y):
    """Desenha o texto CENTRALIZADO na posição (x, y)."""
    img = fonte.render(texto, True, cor)
    tela.blit(img, img.get_rect(center=(x, y)))


# --------------------------------------------------------------------
# SPRITES
# --------------------------------------------------------------------
def caminho(*partes):
    """Monta o caminho de um arquivo a partir da pasta do projeto.
    Funciona não importa de onde o jogo seja executado."""
    return os.path.join(PASTA_BASE, *partes)


def _exigir_janela():
    if pygame.display.get_surface() is None:
        raise RuntimeError(
            "Crie a janela antes de carregar sprites: chame criar_janela(...) primeiro."
        )


def carregar_imagem(arquivo, tamanho=None):
    """Carrega uma imagem única.

    Se o arquivo não existir, retorna None.
    tamanho -> (largura, altura) opcional.
    """
    _exigir_janela()

    caminho_arquivo = caminho(arquivo)

    if not os.path.exists(caminho_arquivo):
        return None

    imagem = pygame.image.load(caminho_arquivo).convert_alpha()

    if tamanho:
        imagem = pygame.transform.scale(imagem, tamanho)

    return imagem


def carregar_frames(arquivo, frame_w, frame_h=None, tamanho=None):
    """Corta uma spritesheet HORIZONTAL com frames do mesmo tamanho.

    arquivo  -> caminho relativo à pasta do projeto
    frame_w  -> largura de cada frame no PNG
    frame_h  -> altura de cada frame (padrão: altura do PNG)
    tamanho  -> (largura, altura) final na tela (padrão: tamanho original)
    Devolve uma lista de imagens (pygame.Surface).
    """
    _exigir_janela()
    sheet = pygame.image.load(caminho(arquivo)).convert_alpha()
    frame_h = frame_h or sheet.get_height()
    frames = []
    for i in range(sheet.get_width() // frame_w):
        frame = sheet.subsurface((i * frame_w, 0, frame_w, frame_h)).copy()
        if tamanho:
            frame = pygame.transform.scale(frame, tamanho)  # scale = pixel art nítida
        frames.append(frame)
    return frames


def carregar_frames_auto(arquivo, tamanho, remover_fundo_branco=False,
                         ignorar_rodape=0.0, limiar_branco=235):
    """Para sheets em que os frames NÃO são igualmente espaçados.

    Acha cada sprite sozinho (trechos de colunas com pixels visíveis),
    recorta cada um e centraliza todos num canvas comum, para a animação
    não "tremer".

    remover_fundo_branco -> apaga pixels quase brancos (fundo opaco)
    ignorar_rodape       -> fração da base da imagem a apagar (ex.: 0.15 para
                            eliminar uma faixa de texto/marca d'água)
    """
    _exigir_janela()
    sheet = pygame.image.load(caminho(arquivo)).convert_alpha()
    w, h = sheet.get_size()

    # 1) limpeza opcional do fundo
    if remover_fundo_branco or ignorar_rodape:
        corte_y = int(h * (1 - ignorar_rodape))
        for x in range(w):
            for y in range(h):
                r, g, b, _ = sheet.get_at((x, y))
                branco = r > limiar_branco and g > limiar_branco and b > limiar_branco
                if y >= corte_y or (remover_fundo_branco and branco):
                    sheet.set_at((x, y), (0, 0, 0, 0))

    # 2) acha as faixas de colunas que têm algum pixel visível
    ocupada = [any(sheet.get_at((x, y))[3] > 0 for y in range(h)) for x in range(w)]
    faixas, inicio = [], None
    for x, tem_pixel in enumerate(ocupada + [False]):
        if tem_pixel and inicio is None:
            inicio = x
        elif not tem_pixel and inicio is not None:
            faixas.append((inicio, x))
            inicio = None

    if not faixas:
        raise ValueError(f"Nenhum sprite visível encontrado em {arquivo}")

    # 3) recorta cada sprite na sua própria caixa
    sprites = []
    for x0, x1 in faixas:
        faixa = sheet.subsurface((x0, 0, x1 - x0, h))
        sprites.append(faixa.subsurface(faixa.get_bounding_rect()).copy())

    # 4) centraliza todos num canvas comum e escala
    larg = max(s.get_width() for s in sprites)
    alt = max(s.get_height() for s in sprites)
    frames = []
    for s in sprites:
        canvas = pygame.Surface((larg, alt), pygame.SRCALPHA)
        canvas.blit(s, s.get_rect(center=(larg // 2, alt // 2)))
        frames.append(pygame.transform.scale(canvas, tamanho))
    return frames


def desenhar_textura(tela, imagem, retangulo):
    """Repete 'imagem' lado a lado até preencher 'retangulo'."""
    if imagem is None:
        return

    largura = imagem.get_width()
    altura = imagem.get_height()

    for y in range(retangulo.top, retangulo.bottom, altura):
        for x in range(retangulo.left, retangulo.right, largura):
            tela.blit(imagem, (x, y))


def carregar_personagem(pasta, frame, tamanho_visual, animacoes_arquivos):
    """Carrega as animações de um personagem E calcula a hitbox automaticamente,
    medindo a margem transparente no 1º frame da pose "parado".

    pasta              -> ex.: "sprites/personagens/proto/"
    frame              -> tamanho do frame no PNG (frames quadrados, ex.: 128)
    tamanho_visual     -> tamanho final do sprite na tela (int)
    animacoes_arquivos -> dict {"estado": ("arquivo.png", quantidade_de_frames)}
                          quantidade_de_frames=None usa todos os frames do arquivo.
                          Precisa ter a chave "parado" (é nela que a hitbox é medida).

    Devolve (animacoes, hitbox_largura, hitbox_altura) — já prontos pra criar
    o Rect do jogador e o Animador. Troca de personagem é só trocar 'pasta'
    e 'frame': a hitbox se ajusta sozinha, sem precisar medir nada à mão.
    """
    _exigir_janela()

    # mede a hitbox no frame 0 da pose "parado"
    arquivo_parado, _ = animacoes_arquivos["parado"]
    sheet_parado = pygame.image.load(caminho(f"{pasta}{arquivo_parado}")).convert_alpha()
    frame0 = sheet_parado.subsurface((0, 0, frame, frame))
    caixa = frame0.get_bounding_rect()
    hitbox_largura = max(1, int(tamanho_visual * caixa.width / frame))
    hitbox_altura = max(1, int(tamanho_visual * caixa.height / frame))

    # carrega cada animação
    animacoes = {}
    for estado, (arquivo, n_frames) in animacoes_arquivos.items():
        todos = carregar_frames(f"{pasta}{arquivo}", frame, frame,
                                (tamanho_visual, tamanho_visual))
        animacoes[estado] = todos[:n_frames] if n_frames else todos

    return animacoes, hitbox_largura, hitbox_altura


def medir_hitbox(arquivo, frame_w, frame_h=None, quadro=0):
    """Ferramenta de diagnóstico: mostra no terminal a proporção que um
    personagem ocupa dentro do canvas. Não é necessária no dia a dia —
    carregar_personagem() já mede isso sozinha — mas ajuda a entender
    o número ou a investigar um sprite com margem incomum.

    arquivo  -> caminho relativo à pasta do projeto
    frame_w, frame_h -> tamanho de cada frame no PNG (frame_h padrão: altura do PNG)
    quadro   -> índice do frame a medir (0 = primeiro); use a pose "parada"

    Imprime hitbox_largura e hitbox_altura (já na forma "numerador/denominador")
    e também devolve os dois valores, caso queira usar direto no código.
    """
    _exigir_janela()
    sheet = pygame.image.load(caminho(arquivo)).convert_alpha()
    frame_h = frame_h or sheet.get_height()
    frame = sheet.subsurface((quadro * frame_w, 0, frame_w, frame_h))
    caixa = frame.get_bounding_rect()  # menor retângulo com pixels visíveis

    print(f"{arquivo} [frame {quadro}] de {frame_w}x{frame_h}:")
    print(f"  hitbox_largura = {caixa.width}/{frame_w}  ({caixa.width / frame_w:.3f})")
    print(f"  hitbox_altura  = {caixa.height}/{frame_h}  ({caixa.height / frame_h:.3f})")

    return caixa.width / frame_w, caixa.height / frame_h


def frame_por_tempo(frames, ms_por_frame=100):
    """Escolhe o frame atual só pelo relógio (bom para itens simples, como a moeda)."""
    return frames[(pygame.time.get_ticks() // ms_por_frame) % len(frames)]


class Animador:
    """Controla qual frame mostrar (para personagens com vários estados).

    animacoes -> dict {"estado": [frames...]}
    """

    def __init__(self, animacoes, estado_inicial, ms_por_frame=80):
        self.animacoes = animacoes
        self.estado = estado_inicial
        self.ms_por_frame = ms_por_frame
        self.indice = 0
        self.tempo = 0
        self.olhando_direita = True

    def definir_estado(self, novo_estado):
        if novo_estado != self.estado:
            self.estado = novo_estado
            self.indice = 0
            self.tempo = 0

    def atualizar(self, dt_ms):
        frames = self.animacoes[self.estado]
        self.tempo += dt_ms
        if self.tempo >= self.ms_por_frame:
            self.tempo = 0
            self.indice = (self.indice + 1) % len(frames)

    def imagem_atual(self):
        frames = self.animacoes[self.estado]
        img = frames[self.indice % len(frames)]
        if not self.olhando_direita:
            img = pygame.transform.flip(img, True, False)
        return img
```

</details>

---

# 4. `base.py`

O `base.py` tem só quatro seções fixas — **CONFIGURAÇÕES**, **SPRITES**,
**OBJETOS E VARIÁVEIS DO JOGO** e, dentro do loop, **EVENTOS**, **LÓGICA** e
**DESENHO**. Cada etapa do roteiro diz em qual dessas seções colar o código
novo. A física é baseada em tempo (`dt`), não em frames, então o jogo roda
igual em qualquer taxa de quadros.

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

fonte_titulo = criar_fonte(48, negrito=True)
fonte_texto = criar_fonte(32)


# ============================================================
# SPRITES
# ============================================================

# Caminhos da pasta do personagem e dos outros assets.
# None = usar o desenho padrão (retângulo colorido).

SPRITE_PERSONAGEM = None
SPRITE_INIMIGO = None
SPRITE_CHAO = None
SPRITE_PLATAFORMA = None
SPRITE_MOEDA = None


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    clock = pygame.time.Clock()


    # ========================================================
    # OBJETOS E VARIÁVEIS DO JOGO
    # ========================================================

    # Jogador, chão, gravidade, velocidade vertical,
    # estado do pulo, moeda, inimigo, estado do jogo, salas...


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

            # Teclas pressionadas uma vez (ex.: pulo)


        # ====================================================
        # LÓGICA
        # ====================================================

        # dt = dt_ms / 1000
        # Entrada contínua (A / D)
        # Gravidade e movimento vertical
        # Colisão com o chão / plataformas
        # Moeda, inimigo, salas
        # Estado do jogo (INICIO / JOGANDO / DERROTA / VITORIA)
        # Animação (qual estado o Animador deve mostrar)


        # ====================================================
        # DESENHO
        # ====================================================

        # Chão, plataformas, moeda, inimigo
        # Jogador (sprite ancorado pelos pés, NÃO esticado no Rect)
        # HUD
        # Textos de cada tela (início, derrota, vitória)


        pygame.display.flip()


if __name__ == "__main__":
    main()
```

---

# 5. Roteiro de execução

Cronograma com os 150 minutos redistribuídos: as etapas que mais costumam travar (Sprite, Animações, Estados) ganharam mais tempo, tirado de etapas mais simples e das Plataformas, que viraram bônus opcional.

## 0:00–0:05 — Janela e loop

### Objetivo

Garantir que todos tenham a janela funcionando.

### Trabalhar

* `pygame.init()` (dentro de `criar_janela`)
* `while`
* eventos
* `Clock`
* `60 FPS`
* atualização da tela

### Checkpoint

Janela abre, permanece funcionando e fecha pelo `X`.

---

## 0:05–0:15 — Jogador

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
jogador = pygame.Rect(
    100,
    300,
    40,
    50
)
```

### Adicionar em `DESENHO`

```python
pygame.draw.rect(
    tela,
    AZUL,
    jogador
)
```

### Trabalhar

* `Rect`
* `x`, `y`
* largura e altura
* desenho

### Checkpoint

Um retângulo aparece na tela.

---

## 0:15–0:25 — Movimentação

### Adicionar em `LÓGICA`

```python
teclas = pygame.key.get_pressed()

if teclas[pygame.K_a]:
    jogador.x -= 5

if teclas[pygame.K_d]:
    jogador.x += 5
```

### Trabalhar

* teclado
* coordenadas
* alteração de posição

### Checkpoint

Jogador anda para esquerda e direita.

---

## 0:25–0:30 — Chão

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
chao = pygame.Rect(
    0,
    350,
    LARGURA,
    50
)
```

### Adicionar em `DESENHO`

```python
pygame.draw.rect(
    tela,
    VERDE,
    chao
)
```

### Checkpoint

Chão aparece na parte inferior da tela.

---

## 0:30–0:40 — Gravidade

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
gravidade = 1200       # pixels por segundo²
jogador_vel_y = 0
```

### Adicionar em `LÓGICA` (no início, antes de mexer no jogador)

```python
dt = dt_ms / 1000

jogador_vel_y += gravidade * dt
jogador.y += jogador_vel_y * dt
```

### Trabalhar

* `dt`
* velocidade
* aceleração
* posição

### ⚠️ Atenção

A física é baseada em **tempo** (`dt`), não em frames. Isso garante que o jogo
tenha a mesma velocidade em qualquer computador, independente do FPS real.

### Checkpoint

Jogador cai.

---

## 0:40–0:55 — Colisão e pulo

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
forca_pulo = -500      # pixels por segundo
pulando = False
```

### Adicionar em `LÓGICA`

```python
if jogador.colliderect(chao):
    jogador.bottom = chao.top
    jogador_vel_y = 0
    pulando = False
```

### Adicionar em `EVENTOS`

```python
if evento.type == pygame.KEYDOWN:
    if evento.key == pygame.K_SPACE and not pulando:
        jogador_vel_y = forca_pulo
        pulando = True
```

### Checkpoint

Jogador cai, para no chão e consegue pular.

### ⚠️ Atenção

`jogador_vel_y` é uma **variável separada do `jogador`**. Não usar `jogador.vel_y`.

---

## 0:55–1:10 — Sprite

Substituir o retângulo do jogador pelo sprite. A hitbox (colisão) e o
sprite (visual) usam tamanhos diferentes — o PNG tem margem transparente ao
redor do personagem — mas a proporção entre os dois é **calculada
automaticamente** pelo `carregar_personagem`, no momento em que o jogo
carrega. Não precisa medir nada à mão.

### Adicionar em `SPRITES`

```python
SPRITE_PERSONAGEM = "sprites/personagens/proto/"
```

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
from helper import carregar_personagem

TAMANHO_VISUAL = 150

animacoes, HITBOX_LARGURA, HITBOX_ALTURA = carregar_personagem(
    SPRITE_PERSONAGEM,
    frame=128,
    tamanho_visual=TAMANHO_VISUAL,
    animacoes_arquivos={
        "parado": ("Walking.png", 1),   # o pack não tem "idle"
        "correndo": ("Running.png", None),
        "pulando": ("Jumping.png", None),
        "caindo": ("Falling.png", None),
    }
)

jogador = pygame.Rect(100, 350 - HITBOX_ALTURA, HITBOX_LARGURA, HITBOX_ALTURA)
sprite_parado = animacoes["parado"][0]
```

### Adicionar em `DESENHO` (no lugar do `draw.rect` do jogador)

```python
tela.blit(sprite_parado, sprite_parado.get_rect(midbottom=jogador.midbottom))
```

### Trabalhar

* `convert_alpha` / transparência
* recorte de spritesheet
* `blit`
* por que a hitbox é medida (`get_bounding_rect`), não chutada

### ⚠️ Atenção — a pegadinha mais comum da oficina

O PNG do sprite tem uma margem transparente ao redor do personagem (espaço
para os braços e pernas se moverem na animação). Se você desenhar o sprite
**esticado dentro do `Rect` da hitbox**, o personagem aparece pequeno demais.

A correção é usar **dois tamanhos diferentes**: a hitbox (colisão, pequena)
e o sprite (visual, maior), ancorando o desenho pelos **pés**
(`midbottom`) em vez de preencher o `Rect` inteiro — é o que o código acima
já faz. `carregar_personagem` mede essa proporção sozinha no 1º frame da
pose "parado", então trocar de personagem é só trocar `SPRITE_PERSONAGEM`
(e `frame`, se o pack novo usar outro tamanho de canvas) — a hitbox se
ajusta sem precisar medir nada de novo.

Se algum pack der uma hitbox estranha (a pose "parada" tem um braço muito
esticado, por exemplo), `medir_hitbox` no `helper.py` serve pra investigar
o número manualmente.

### Checkpoint

O personagem aparece no lugar do retângulo, parado em cima do chão.

---

## 1:10–1:25 — Animações

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
from helper import Animador

animador = Animador(animacoes, "parado")
```

### Adicionar em `LÓGICA` (junto da entrada contínua)

```python
movendo = False

if teclas[pygame.K_a]:
    jogador.x -= 5
    animador.olhando_direita = False
    movendo = True

if teclas[pygame.K_d]:
    jogador.x += 5
    animador.olhando_direita = True
    movendo = True
```

### Adicionar em `LÓGICA` (depois da física, já sabendo se `pulando` e `movendo`)

```python
if pulando and jogador_vel_y < 0:
    animador.definir_estado("pulando")
elif pulando and jogador_vel_y >= 0:
    animador.definir_estado("caindo")
elif movendo:
    animador.definir_estado("correndo")
else:
    animador.definir_estado("parado")

animador.atualizar(dt_ms)
```

### Adicionar em `DESENHO` (substitui o `sprite_parado` fixo)

```python
sprite_atual = animador.imagem_atual()
tela.blit(sprite_atual, sprite_atual.get_rect(midbottom=jogador.midbottom))
```

### Checkpoint

Personagem troca de animação conforme o movimento, e vira de lado ao mudar de direção.

---

## 1:25–1:40 — Moeda

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
moeda = pygame.Rect(
    650,
    300,
    30,
    30
)

moeda_coletada = False
moedas_coletadas = 0
```

### Adicionar em `LÓGICA`

```python
if not moeda_coletada:
    if jogador.colliderect(moeda):
        moeda_coletada = True
        moedas_coletadas += 1
```

### Adicionar em `DESENHO`

```python
if not moeda_coletada:
    pygame.draw.rect(tela, AMARELO, moeda)
```

### Checkpoint

Moeda desaparece ao ser coletada e contador aumenta.

---

## 1:40–1:55 — Inimigo

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
inimigo = pygame.Rect(
    400,
    300,
    40,
    50
)

inimigo_vel = 3
```

### Adicionar em `LÓGICA`

```python
inimigo.x += inimigo_vel

if inimigo.left <= 300 or inimigo.right >= 550:
    inimigo_vel *= -1
```

Colisão:

```python
if jogador.colliderect(inimigo):
    estado = DERROTA
```

### Adicionar em `DESENHO`

```python
pygame.draw.rect(tela, VERMELHO, inimigo)
```

### Checkpoint

Inimigo patrulha e pode atingir o jogador.

---

## 1:55–2:10 — Estados

Essa etapa reorganiza tudo que já foi escrito dentro de blocos por estado —
reserve o tempo todo, é mais trabalhosa do que parece.

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
INICIO = "INICIO"
JOGANDO = "JOGANDO"
DERROTA = "DERROTA"
VITORIA = "VITORIA"

estado = INICIO
```

### Trabalhar

* Separar a **lógica** (física, colisões, moeda, inimigo) dentro de
  `if estado == JOGANDO: ...`, em `LÓGICA`
* Separar o **desenho** de cada tela (`INICIO`, `DERROTA`, `VITORIA`) usando
  `desenhar_texto`, em `DESENHO`
* `ENTER` reinicia o jogo a partir de `INICIO`, `DERROTA` ou `VITORIA`, em `EVENTOS`

### Checkpoint

Jogo possui início, gameplay, derrota e vitória, e dá pra reiniciar com ENTER.

---

## 2:10–2:20 — Salas (com volta)

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
salas = [
    {"moeda": (650, 300), "inimigos": []},
    {"moeda": (250, 250), "inimigos": []},
    {"moeda": (650, 250), "inimigos": []},
]

sala_atual = 0
total_moedas = len(salas)
coletada_na_sala = [False] * len(salas)   # lembra o que já foi pego em cada sala

moeda.x, moeda.y = salas[sala_atual]["moeda"]
```

### Adicionar em `LÓGICA` — transição nos dois sentidos

```python
if jogador.right >= LARGURA and sala_atual < len(salas) - 1:
    sala_atual += 1
    jogador.left = 20
    moeda.x, moeda.y = salas[sala_atual]["moeda"]

elif jogador.left <= 0 and sala_atual > 0:
    sala_atual -= 1
    jogador.right = LARGURA - 20
    moeda.x, moeda.y = salas[sala_atual]["moeda"]
```

### Ajustar em `LÓGICA` (etapa da Moeda)

```python
if not coletada_na_sala[sala_atual] and jogador.colliderect(moeda):
    coletada_na_sala[sala_atual] = True
    moedas_coletadas += 1

    if moedas_coletadas == total_moedas:
        estado = VITORIA
```

### Ajustar em `DESENHO`

```python
if not coletada_na_sala[sala_atual]:
    pygame.draw.rect(tela, AMARELO, moeda)
```

### ⚠️ Por que voltar é importante

Sem poder voltar, o jogador pode atravessar a borda direita sem pegar a
moeda da sala — e como não existe volta, ela fica impossível de pegar pra
sempre, e o jogo nunca chega à vitória. Permitir `jogador.left <= 0` também
disparar a troca de sala resolve isso, desde que `coletada_na_sala` lembre o
que já foi pego (senão a moeda reaparece ao voltar).

### Checkpoint

Jogador consegue ir e voltar entre as salas, e nenhuma moeda fica impossível de coletar.

---

## 2:20–2:30 — Vitória + buffer de ajustes

### Em `DESENHO`, na tela de vitória

```python
if estado == VITORIA:
    desenhar_texto(
        tela,
        "VOCÊ VENCEU!",
        fonte_titulo,
        PRETO,
        LARGURA // 2,
        ALTURA // 2
    )
```

### Buffer

Esses minutos finais são de propósito flexíveis:

* Se a turma está no horário, use pra testar e ajustar valores:

  ```python
  gravidade = 800
  forca_pulo = -600
  inimigo_vel = 5
  ```

* Se algum passo anterior atrasou, é daqui que se tira o tempo — sem
  cortar nada essencial, porque o jogo já tem início, fim e vitória
  desde a etapa de Estados.

### Checkpoint

Coletar todas as moedas leva à vitória. Jogo completo, do início ao fim.

---

## Bônus — Plataformas (opcional, pra quem terminar antes)

Fica fora do cronograma principal: o jogo já funciona sem isso. Oferecer como desafio pra quem acabar cedo.

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
plataformas = [
    pygame.Rect(150, 300, 120, 20),
    pygame.Rect(350, 250, 120, 20),
    pygame.Rect(550, 300, 120, 20)
]
```

### Adicionar em `DESENHO`

```python
for plataforma in plataformas:
    pygame.draw.rect(tela, VERDE, plataforma)
```

### Adicionar em `LÓGICA` (colisão só enquanto o jogador está caindo, pra não grudar nela por baixo)

```python
for plataforma in plataformas:
    if (
        jogador.colliderect(plataforma)
        and jogador_vel_y >= 0
        and jogador.bottom - jogador_vel_y * dt <= plataforma.top + 5
    ):
        jogador.bottom = plataforma.top
        jogador_vel_y = 0
        pulando = False
```

### Checkpoint

Jogador consegue pousar nas plataformas e utilizá-las para avançar.

---

# 6. Trocando de personagem (opcional, pra quem quiser)

Como a hitbox é calculada automaticamente, trocar de sprite é só:

1. Colocar a pasta nova em `sprites/personagens/<novo_pack>/`
2. Mudar `SPRITE_PERSONAGEM` pra apontar pra ela
3. Ajustar `frame=` se o pack usar um tamanho de canvas diferente de 128
4. Ajustar os nomes dos arquivos em `animacoes_arquivos` se o pack usar nomes diferentes (ex.: `Idle.png` em vez de `Walking.png`)

Nada mais muda — `carregar_personagem` mede a hitbox de novo sozinha a
partir do frame 0 da pose "parado" do pack novo.

---

# 7. Resultado esperado

* [ ] Janela e loop
* [ ] Movimentação
* [ ] Gravidade
* [ ] Pulo
* [ ] Colisões
* [ ] Sprite
* [ ] Animações
* [ ] Moedas
* [ ] Contador
* [ ] Inimigo
* [ ] Estados
* [ ] Salas (ida e volta)
* [ ] Vitória
* [ ] Derrota
* [ ] (Bônus) Plataformas

**`base.py` → desenvolvimento gradual → jogo completo**
