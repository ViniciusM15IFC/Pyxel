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
* Sprites e animações (jogador, inimigo e moeda)
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
├── pyxel_helper.py
├── base.py
└── sprites/
    ├── personagens/
    │   └── proto/          (e os outros packs opcionais)
    ├── inimigos/
    │   └── orc.png
    └── moeda/
        └── moeda_sheet.png
```

* `pyxel_helper.py` — funções auxiliares fornecidas pela oficina.
* `base.py` — arquivo desenvolvido durante a oficina.

> ⚠️ O arquivo precisa se chamar **`pyxel_helper.py`** (com underscore).
> Com hífen (`pyxel-helper.py`) o Python não consegue importá-lo e o
> `base.py` falha logo na primeira linha com `ModuleNotFoundError`.

---

# 3. O que tem no `pyxel_helper.py`

Os alunos não precisam abrir esse arquivo. Esta tabela é para o instrutor
saber o que é usado no roteiro e o que é recurso extra.

| Função / classe | Usada no roteiro? | Para quê |
| --- | --- | --- |
| `criar_janela`, `criar_fonte`, `desenhar_texto` | Sim | Janela, fontes e textos centralizados |
| `carregar_personagem` | Sim (0:50) | Carrega as animações do jogador e mede a hitbox sozinha |
| `Animador` | Sim (0:50) | Escolhe o frame do jogador conforme o estado de animação |
| `carregar_frames_grade` | Sim (1:35) | Corta o `orc.png` (grade de 8 células de 100×100) |
| `carregar_frames_auto` | Sim (1:20) | Corta o `moeda_sheet.png` (frames de larguras diferentes, fundo branco) |
| `frame_por_tempo` | Sim (1:20 e 1:35) | Escolhe o frame de moeda e Orc pelo relógio |
| `carregar_imagem` | Não | Imagem única (útil para cenário e itens sem animação) |
| `carregar_frames` | Não (usada internamente) | Sheet horizontal com frames de tamanho igual |
| `desenhar_textura` | Não | Repete uma imagem para preencher um `Rect` (chão com textura) |
| `medir_hitbox` | Não | Diagnóstico: imprime a proporção que um sprite ocupa no canvas |

As funções marcadas "Não" ficam disponíveis como **recurso extra** para quem
terminar antes (por exemplo, usar `carregar_imagem` e `desenhar_textura` para
dar textura ao chão). Chão e plataformas, no caminho principal, são retângulos
coloridos.

---

# 4. `base.py`

O arquivo auxiliar da oficina é **`pyxel_helper.py`**. As funções e classes necessárias já são importadas no início do `base.py`, então durante a aula o foco fica no código do jogo.

O `base.py` tem quatro seções fixas — **CONFIGURAÇÕES**, **SPRITES**,
**OBJETOS E VARIÁVEIS DO JOGO** e, dentro do loop, **EVENTOS**, **LÓGICA** e
**DESENHO**. Cada etapa do roteiro indica em qual seção inserir ou ajustar o
código. A física é baseada em tempo (`dt`), não em frames.

```python
import sys
import pygame

from pyxel_helper import (
    criar_janela,
    criar_fonte,
    desenhar_texto,
    carregar_personagem,
    carregar_frames_grade,
    carregar_frames_auto,
    frame_por_tempo,
    Animador,
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

# Caminhos dos assets. Cada um é preenchido na etapa em que passa
# a ser usado (None = ainda não usado, o jogo usa um retângulo colorido).
# Chão e plataformas são sempre retângulos coloridos (sem sprite).

SPRITE_PERSONAGEM = None
SPRITE_INIMIGO = None
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

Cronograma com os 150 minutos redistribuídos para uma oficina em que o código
é construído junto com os alunos no VS Code. As etapas que mais costumam
travar (física, sprites/animações e estados) recebem mais tempo.

> **Regra principal da oficina:** cada etapa deve terminar com o jogo
> funcionando exatamente como descrito no `Checkpoint`. Não avance se a etapa
> atual estiver quebrada.
>
> **Regra de segurança:** quando uma etapa altera uma parte que já existia,
> primeiro preserve o comportamento anterior e depois acrescente a nova lógica.
> Não substituir um bloco inteiro por outro sem conferir o que já estava ali.
>
> **Regra para eventos e estados:** sempre que surgir uma nova ação do jogador
> ou um novo `estado`, confira os três lugares do programa:
>
> 1. `EVENTOS` — o que o teclado/comando faz;
> 2. `LÓGICA` — o que muda no jogo;
> 3. `DESENHO` — o que aparece na tela.
>
> Um estado não está completo enquanto essas três partes não estiverem
> coerentes entre si.

> **Gabarito:** o arquivo `jogo_completo.py` é o `base.py` com todas as
> etapas feitas. Use-o para conferir o resultado final (não entregue aos
> alunos).

---

## 0:00–0:05 — Clock, loop e janela em branco

### Objetivo

Apresentar rapidamente o ciclo do jogo e mostrar o ponto de partida. A
estrutura básica já vem pronta no `base.py`.

### Trabalhar

* `while`
* eventos
* `Clock`
* `60 FPS`
* atualização da tela
* `dt_ms = clock.tick(60)`

### Explicação rápida do `Clock`

O `Clock` controla o ritmo do loop e informa quanto tempo passou desde o
último ciclo. O `tick(60)` limita o loop a aproximadamente 60 ciclos por
segundo e retorna esse tempo em milissegundos.

```text
EVENTOS → LÓGICA → DESENHO → repete
```

A janela em branco é o ponto de partida: a partir dela, vamos construir o
jogo junto com a turma.

### Checkpoint

Janela abre, permanece funcionando e fecha pelo `X`.

---

## 0:05–0:20 — Jogador e movimentação

### Objetivo

Criar o primeiro objeto do jogo e fazê-lo responder ao teclado.

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
jogador = pygame.Rect(
    100,
    300,
    40,
    50
)
```

### Adicionar em `LÓGICA`

```python
teclas = pygame.key.get_pressed()

if teclas[pygame.K_a]:
    jogador.x -= 5

if teclas[pygame.K_d]:
    jogador.x += 5
```

### Adicionar em `DESENHO`

Por enquanto o jogador é só um **quadrado azul temporário** — o próprio
`Rect` desenhado na tela. Ele será trocado pelo sprite na etapa de 0:50.

```python
pygame.draw.rect(tela, AZUL, jogador)
```

Sem essa linha o `Rect` existe, mas é invisível: a tela fica em branco.

### Trabalhar

* `Rect`
* posição (`x`, `y`)
* largura e altura
* alteração de coordenadas
* entrada contínua com `get_pressed()`

### Checkpoint

Jogador aparece na tela e anda para esquerda e direita.

### ⚠️ Atenção

`pygame.key.get_pressed()` é usado para ações contínuas, como andar. O
`KEYDOWN` será usado depois para ações que acontecem uma vez quando uma tecla
é pressionada, como o pulo e o `ENTER`.

---

## 0:20–0:25 — Estados e telas: introdução

Nesta etapa apresentamos a ideia de que o jogo pode estar em diferentes
estados, sem implementar ainda todas as telas.

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
INICIO = "INICIO"
JOGANDO = "JOGANDO"
DERROTA = "DERROTA"
VITORIA = "VITORIA"

estado = JOGANDO
```

Neste momento o jogo continua começando diretamente em `JOGANDO`. A estrutura
das telas será completada mais adiante.

### Adicionar em `LÓGICA` e `DESENHO`

A lógica e o desenho do jogo passam a ser executados apenas quando:

```python
if estado == JOGANDO:
    # LÓGICA: movimento do jogador (A / D)
```

```python
if estado == JOGANDO:
    # DESENHO: o quadrado temporário do jogador
    pygame.draw.rect(tela, AZUL, jogador)
```

Cada novo elemento do jogo entra nesses dois blocos (`LÓGICA` e `DESENHO`).

### Checkpoint

O jogo continua funcionando exatamente como antes.

---

## 0:25–0:50 — Chão, gravidade, colisão e pulo

### Objetivo

Transformar o movimento em uma física simples de plataforma.

### Chão

```python
chao = pygame.Rect(
    0,
    350,
    LARGURA,
    50
)
```

No `DESENHO`:

```python
pygame.draw.rect(tela, VERDE, chao)
```

### Gravidade

```python
gravidade = 1200
jogador_vel_y = 0
pulando = False
```

```python
dt = dt_ms / 1000

jogador_vel_y += gravidade * dt
jogador.y += jogador_vel_y * dt
```

A física é baseada em tempo (`dt`), não em frames.

### Colisão com o chão

```python
if jogador.colliderect(chao):
    jogador.bottom = chao.top
    jogador_vel_y = 0
    pulando = False
```

### Pulo

```python
if evento.type == pygame.KEYDOWN:
    if evento.key == pygame.K_SPACE and not pulando:
        jogador_vel_y = -500
        pulando = True
```

### Trabalhar

* `dt`
* velocidade vertical
* gravidade
* `colliderect()`
* pulo
* diferença entre `KEYDOWN` e `get_pressed()`

### Checkpoint

Jogador cai, para no chão e consegue pular.

---

## 0:50–1:20 — Sprites e animações do jogador

### Objetivo

Substituir o retângulo azul por sprites e fazer o personagem se animar
conforme sua ação.

### Personagem

O `Rect` continua representando a hitbox. O sprite representa o visual.

Em `SPRITES`:

```python
SPRITE_PERSONAGEM = "sprites/personagens/proto/"
```

`carregar_personagem()` carrega as animações **e** devolve a largura e a
altura da hitbox, medidas automaticamente a partir do personagem.

Em `OBJETOS E VARIÁVEIS DO JOGO` (isto **substitui** o `jogador = pygame.Rect(...)`
fixo de antes — o `chao` precisa já existir acima):

```python
animacoes, hit_w, hit_h = carregar_personagem(
    SPRITE_PERSONAGEM,
    128,    # tamanho do frame no PNG
    96,     # tamanho do sprite na tela
    {
        "parado":   ("Walking.png", 1),
        "correndo": ("Running.png", None),
        "pulando":  ("Jumping.png", None),
        "caindo":   ("Falling.png", None),
    },
)

jogador = pygame.Rect(100, 0, hit_w, hit_h)
jogador.bottom = chao.top

animador = Animador(animacoes, "parado")
```

### Direção e estado de animação

Em `LÓGICA`, a entrada contínua passa a guardar se o jogador está andando e
para que lado olha:

```python
andando = False

if teclas[pygame.K_a]:
    jogador.x -= 5
    animador.olhando_direita = False
    andando = True

if teclas[pygame.K_d]:
    jogador.x += 5
    animador.olhando_direita = True
    andando = True
```

No fim da `LÓGICA` (ainda dentro de `if estado == JOGANDO`), escolha a animação:

```python
if pulando or jogador_vel_y > 200:
    if jogador_vel_y < 0:
        animador.definir_estado("pulando")
    else:
        animador.definir_estado("caindo")
elif andando:
    animador.definir_estado("correndo")
else:
    animador.definir_estado("parado")

animador.atualizar(dt_ms)
```

> Por que `jogador_vel_y > 200` e não `> 0`? Com o jogador parado no chão, a
> gravidade acumula um pouquinho de velocidade a cada frame até o `Rect`
> andar 1 pixel e a colisão zerar tudo. Com `> 0` a animação de "caindo"
> ficaria piscando no chão. O limite de 200 só é atingido numa queda de
> verdade (e também serve para quem andar para fora de uma plataforma).

### Desenho

Em `DESENHO`, no lugar do `pygame.draw.rect(tela, AZUL, jogador)`:

```python
img = animador.imagem_atual()
tela.blit(img, img.get_rect(midbottom=jogador.midbottom))
```

### Trabalhar

* transparência e `convert_alpha()`
* spritesheets
* `blit()`
* hitbox x visual
* `midbottom`
* `Animador`
* estados de animação

Estados do personagem:

```text
PARADO → CORRENDO → PULANDO → CAINDO
```

### Checkpoint

O personagem aparece com sprite, anda, vira de direção e troca de animação
ao correr, pular e cair.

### ⚠️ Atenção

Não desenhar o sprite esticado dentro do `Rect` da hitbox. Use:

```python
sprite.get_rect(midbottom=jogador.midbottom)
```

---

## 1:20–1:35 — Moeda e contador (retângulo → sprite animado)

### Objetivo

Adicionar o primeiro objetivo do jogador. Primeiro a moeda aparece como um
**quadrado amarelo temporário**; depois trocamos por uma moeda que gira.

### Parte 1 — Moeda temporária

Em `OBJETOS E VARIÁVEIS DO JOGO`:

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

Em `LÓGICA` (coleta):

```python
if not moeda_coletada and jogador.colliderect(moeda):
    moeda_coletada = True
    moedas_coletadas += 1
```

Em `DESENHO` (quadrado amarelo + contador na tela):

```python
if not moeda_coletada:
    pygame.draw.rect(tela, AMARELO, moeda)

desenhar_texto(
    tela,
    f"Moedas: {moedas_coletadas}",
    fonte_texto,
    PRETO,
    LARGURA // 2,
    30
)
```

**Checkpoint da parte 1:** o quadrado amarelo aparece, some ao ser coletado e
o contador no topo aumenta.

### Parte 2 — Trocar pelo sprite animado

Em `SPRITES`:

```python
SPRITE_MOEDA = "sprites/moeda/moeda_sheet.png"
```

Em `OBJETOS E VARIÁVEIS DO JOGO`, acrescente:

```python
frames_moeda = carregar_frames_auto(
    SPRITE_MOEDA,
    (40, 40),
    remover_fundo_branco=True,
    ignorar_rodape=0.15
)
```

O `moeda_sheet.png` tem fundo branco opaco, frames de larguras diferentes e
uma faixa de texto na base. Por isso usamos `carregar_frames_auto`: ele acha
cada moeda sozinho, apaga o fundo branco e ignora os 15% de baixo da imagem.
Ele é um pouco lento (varre os pixels), então os frames são carregados **uma
vez**, antes do loop — nunca dentro dele.

Em `DESENHO`, **no lugar** do `pygame.draw.rect(tela, AMARELO, moeda)`:

```python
if not moeda_coletada:
    img = frame_por_tempo(frames_moeda, 100)
    tela.blit(img, img.get_rect(center=moeda.center))
```

`frame_por_tempo(frames, 100)` troca de frame a cada 100 ms, usando só o
relógio — por isso a moeda gira sem precisar de um `Animador`. A coleta
continua usando o `Rect` `moeda` como hitbox.

### Trabalhar

* hitbox (`Rect`) x visual (sprite)
* spritesheet com frames irregulares
* animação pelo tempo (`frame_por_tempo`)
* colisão com a moeda
* variáveis de contagem e HUD

### Checkpoint

A moeda aparece girando, desaparece ao ser coletada e o contador aumenta.

---

## 1:35–1:50 — Inimigo e trajetória (retângulo → Orc animado)

### Objetivo

Criar um objeto com comportamento próprio. Primeiro como um **quadrado
vermelho temporário**; depois trocamos por um Orc animado.

### Parte 1 — Inimigo temporário

Em `OBJETOS E VARIÁVEIS DO JOGO`:

```python
inimigo = pygame.Rect(
    400,
    310,
    50,
    40
)

inimigo_vel = 3
```

Em `LÓGICA` (movimento e trajetória):

```python
inimigo.x += inimigo_vel

if inimigo.left <= 300 or inimigo.right >= 550:
    inimigo_vel *= -1
```

Em `LÓGICA` (colisão):

```python
if jogador.colliderect(inimigo):
    estado = DERROTA
```

Em `DESENHO`:

```python
pygame.draw.rect(tela, VERMELHO, inimigo)
```

> Até a etapa de 1:50 ainda não existe tela de derrota: ao encostar no
> inimigo o jogo vai para `DERROTA` e a tela fica em branco (o desenho e a
> lógica só rodam em `JOGANDO`). É esperado — feche a janela e abra de novo
> para testar outra vez.

**Checkpoint da parte 1:** o quadrado vermelho percorre a trajetória entre
x = 300 e x = 550 e, ao encostar nele, o jogo para.

### Parte 2 — Trocar pelo Orc animado

Em `SPRITES`:

```python
SPRITE_INIMIGO = "sprites/inimigos/orc.png"
```

Em `OBJETOS E VARIÁVEIS DO JOGO`, acrescente:

```python
frames_orc = carregar_frames_grade(
    SPRITE_INIMIGO,
    100,
    100,
    (60, 60)
)
```

O `orc.png` é uma grade de 8 células de 100×100, com um Orc pequeno no meio
de cada uma. `carregar_frames_grade` corta cada célula, remove a margem
transparente, alinha os pés e mantém a proporção (o Orc cabe em 60×60 sem
ficar esticado). A hitbox (50×40) tem o tamanho aproximado do Orc na tela.

Em `DESENHO`, **no lugar** do `pygame.draw.rect(tela, VERMELHO, inimigo)`.
O sprite do Orc olha para a direita; quando ele anda para a esquerda,
espelhamos a imagem:

```python
img = frame_por_tempo(frames_orc, 120)

if inimigo_vel < 0:
    img = pygame.transform.flip(img, True, False)

tela.blit(img, img.get_rect(midbottom=inimigo.midbottom))
```

### Checkpoint

O Orc aparece animado, percorre sua trajetória (virando para o lado em que
anda) e pode atingir o jogador.

---

## 1:50–2:05 — Estados e telas: início, derrota e reinício

Agora os estados apresentados anteriormente passam a controlar o fluxo
completo do jogo.

### Estado inicial

Agora o jogo passa a começar na tela de início:

```python
estado = INICIO
```

### Entrada

Em `EVENTOS`, `ENTER` deve funcionar tanto em `INICIO` quanto em `DERROTA`.

```python
if estado == INICIO or estado == DERROTA:
    if evento.key == pygame.K_RETURN:
        estado = JOGANDO
        # resetar jogador, física, moeda e inimigo
```

### Reset

Ao reiniciar, devolver o jogo a um estado inicial conhecido:

```python
jogador.x = 100
jogador.bottom = chao.top
jogador_vel_y = 0
pulando = False
animador.olhando_direita = True
moeda_coletada = False
moedas_coletadas = 0
inimigo.x = 400
inimigo_vel = 3
```

### Desenho

Em `DESENHO`, o que é desenhado passa a depender do `estado`. O que já
existia (chão, moeda, inimigo, jogador, contador) vai dentro do `elif estado == JOGANDO`:

```python
if estado == INICIO:
    desenhar_texto(tela, "Coleta da Moeda", fonte_titulo, PRETO, LARGURA // 2, 140)
    desenhar_texto(tela, "Pressione ENTER para jogar", fonte_texto, AZUL, LARGURA // 2, 230)

elif estado == JOGANDO:
    # chão, moeda, inimigo, jogador e contador (tudo que já existia)
    ...

elif estado == DERROTA:
    desenhar_texto(tela, "Você perdeu!", fonte_titulo, VERMELHO, LARGURA // 2, 140)
    desenhar_texto(tela, "Pressione ENTER para reiniciar", fonte_texto, PRETO, LARGURA // 2, 230)
```

A lógica de gameplay continua protegida por:

```python
if estado == JOGANDO:
    # gameplay
```

### Checkpoint obrigatório

1. Pressione `ENTER`.
2. Jogue normalmente.
3. Encoste no inimigo.
4. A tela de derrota aparece.
5. Pressione `ENTER`.
6. O jogo reinicia.
7. A moeda está disponível novamente.
8. Jogador e inimigo voltam às posições iniciais.

Se qualquer passo falhar, não avance para Salas.

---

## 2:05–2:20 — Salas e plataformas

### Objetivo

Aumentar o espaço do jogo e preparar diferentes desafios.

### Salas

Criar três salas e permitir passagem pelas bordas nos dois sentidos. Cada
sala possui sua própria moeda, o seu próprio estado de coleta e o seu próprio
inimigo.

```text
┌──────────┐   ↔   ┌──────────┐   ↔   ┌──────────┐
│  SALA 1  │       │  SALA 2  │       │  SALA 3  │
│    🪙    │       │    👾    │       │    🪙    │
└──────────┘       └──────────┘       └──────────┘
```

A ideia central: **o estado de cada sala mora na própria sala** (um
dicionário), e o jogo só guarda *em qual sala o jogador está*. É isso que
faz a moeda coletada continuar coletada quando o jogador volta.

Faça em três passos curtos, conferindo o jogo funcionando entre eles.

### Passo 1 — Mover moeda e inimigo para dentro das salas

Em `OBJETOS E VARIÁVEIS DO JOGO`, **apague** as variáveis soltas `moeda`,
`moeda_coletada`, `inimigo` e `inimigo_vel` e crie no lugar:

```python
def criar_salas():
    return [
        {   # Sala 1: moeda
            "moeda": pygame.Rect(650, 300, 30, 30),
            "coletada": False,
            "inimigo": None,
            "inimigo_vel": 0,
        },
        {   # Sala 2: inimigo
            "moeda": None,
            "coletada": False,
            "inimigo": pygame.Rect(400, 310, 50, 40),
            "inimigo_vel": 3,
        },
        {   # Sala 3: moeda
            "moeda": pygame.Rect(650, 300, 30, 30),
            "coletada": False,
            "inimigo": None,
            "inimigo_vel": 0,
        },
    ]


salas = criar_salas()
sala_atual = 0

moedas_coletadas = 0
total_moedas = sum(1 for s in salas if s["moeda"] is not None)
```

`total_moedas` é calculado a partir da lista: se você mudar as salas, o total
acompanha sozinho. `moedas_coletadas` continua sendo um contador único do jogo.

Agora a `LÓGICA` e o `DESENHO` passam a olhar para a **sala atual**. No começo
do bloco de moeda/inimigo da `LÓGICA`:

```python
sala = salas[sala_atual]
```

**Moeda** (`LÓGICA`):

```python
moeda = sala["moeda"]

if (
    moeda is not None
    and not sala["coletada"]
    and jogador.colliderect(moeda)
):
    sala["coletada"] = True
    moedas_coletadas += 1
```

**Inimigo** (`LÓGICA`):

```python
inimigo = sala["inimigo"]

if inimigo is not None:
    inimigo.x += sala["inimigo_vel"]

    if inimigo.left <= 300 or inimigo.right >= 550:
        sala["inimigo_vel"] *= -1

    if jogador.colliderect(inimigo):
        estado = DERROTA
```

**Desenho** (`DESENHO`, também começando com `sala = salas[sala_atual]`):

```python
if sala["moeda"] is not None and not sala["coletada"]:
    img = frame_por_tempo(frames_moeda, 100)
    tela.blit(img, img.get_rect(center=sala["moeda"].center))

if sala["inimigo"] is not None:
    img = frame_por_tempo(frames_orc, 120)

    if sala["inimigo_vel"] < 0:
        img = pygame.transform.flip(img, True, False)

    tela.blit(img, img.get_rect(midbottom=sala["inimigo"].midbottom))
```

**Reset** (no bloco de `ENTER` do `EVENTOS`): troque as linhas que resetavam
moeda e inimigo por:

```python
salas = criar_salas()
sala_atual = 0
moedas_coletadas = 0
```

**Checkpoint do passo 1:** o jogo se comporta como antes, mas ainda com uma
única sala (a sala 1, com a moeda). Se o Orc ainda precisar aparecer para
testar a derrota, troque temporariamente `sala_atual = 1`.

### Passo 2 — Passar de sala nas bordas (ida e volta)

Em `LÓGICA`, logo depois da colisão com o chão e **antes** de
`sala = salas[sala_atual]`:

```python
if jogador.right > LARGURA:
    if sala_atual < len(salas) - 1:
        sala_atual += 1
        jogador.left = 0
    else:
        jogador.right = LARGURA

if jogador.left < 0:
    if sala_atual > 0:
        sala_atual -= 1
        jogador.right = LARGURA
    else:
        jogador.left = 0
```

* Saiu pela direita → próxima sala, entrando pela esquerda.
* Saiu pela esquerda → sala anterior, entrando pela direita.
* Nas bordas do mundo (sala 1 à esquerda, sala 3 à direita) o jogador é
  segurado, sem sair da tela.

Se o jogador passar direto pela moeda da sala 1, ele pode **voltar**; e como
o estado de coleta mora na sala, a moeda não "trava": ela continua lá até ser
pega, e não reaparece depois de coletada.

### Passo 3 — HUD com a sala

Em `DESENHO`, **no lugar** do contador `Moedas: ...` da etapa de 1:20:

```python
desenhar_texto(
    tela,
    f"Moedas: {moedas_coletadas}/{total_moedas}   Sala {sala_atual + 1}/{len(salas)}",
    fonte_texto,
    PRETO,
    LARGURA // 2,
    30
)
```

### Checkpoint

O jogador consegue ir e voltar entre as salas. Uma moeda já coletada não
reaparece ao retornar. Uma moeda **não coletada** continua esperando quando o
jogador volta. O Orc só existe (e só machuca) na sala 2.

### Plataformas

As plataformas ficam como extensão opcional caso a turma esteja adiantada.
Elas introduzem caminhos verticais e novas situações de colisão. Veja o
Bônus ao final.

```python
plataformas = [
    pygame.Rect(150, 300, 120, 20),
    pygame.Rect(350, 250, 120, 20),
    pygame.Rect(550, 300, 120, 20)
]
```

---

## 2:20–2:30 — Vitória + buffer

### Vitória

A vitória é verificada **no momento em que uma moeda é coletada** (dentro do
`if` da coleta, no passo 1 das Salas):

```python
sala["coletada"] = True
moedas_coletadas += 1

if moedas_coletadas == total_moedas:
    estado = VITORIA
```

Depois, em `EVENTOS`, deixe o `ENTER` também funcionar em `VITORIA`
(`if estado == INICIO or estado == DERROTA or estado == VITORIA:`) e, em
`DESENHO`, acrescente a tela de vitória:

```python
elif estado == VITORIA:
    desenhar_texto(tela, "Você venceu!", fonte_titulo, AMARELO, LARGURA // 2, 140)
    desenhar_texto(tela, "Pressione ENTER para jogar de novo", fonte_texto, PRETO, LARGURA // 2, 230)
```

### Fluxo final

```text
INICIO
   │
 ENTER
   ↓
JOGANDO
   │
   ├── inimigo → DERROTA ── ENTER ──→ JOGANDO
   │
   └── todas as moedas → VITORIA ── ENTER ──→ JOGANDO
```

### Buffer

Use os minutos finais para testar, ajustar valores ou corrigir algum ponto
que tenha atrasado. Não corte os checkpoints de funcionamento para ganhar
tempo.

---

# Bônus — Plataformas completas

Se a turma terminar antes, implemente a colisão das plataformas para que o
jogador consiga pousar nelas. Isso fica fora do caminho obrigatório da oficina.

Em `LÓGICA`, logo depois da colisão com o chão:

```python
for plataforma in plataformas:
    if (
        jogador.colliderect(plataforma)
        and jogador_vel_y >= 0
        and jogador.bottom - jogador_vel_y * dt
            <= plataforma.top + 5
    ):
        jogador.bottom = plataforma.top
        jogador_vel_y = 0
        pulando = False
```

Em `DESENHO`:

```python
for plataforma in plataformas:
    pygame.draw.rect(tela, AZUL, plataforma)
```

### Checkpoint

Jogador consegue pousar nas plataformas e utilizá-las para avançar.

---

# 6. Trocando de personagem (opcional, para quem quiser)

Como a hitbox é calculada automaticamente, trocar de sprite é só:

1. Colocar a pasta nova em `sprites/personagens/<novo_pack>/`
2. Mudar `SPRITE_PERSONAGEM` para apontar para ela
3. Ajustar o `128` (tamanho do frame) na chamada de `carregar_personagem` se o
   pack usar um tamanho de canvas diferente
4. Ajustar os nomes dos arquivos no dicionário de animações se o pack usar
   nomes diferentes (ex.: `Idle.png` em vez de `Walking.png`)

Nada mais muda — `carregar_personagem` mede a hitbox de novo sozinha a partir
do frame 0 da pose `"parado"` do pack.

---

# 7. Resultado esperado

* [ ] Clock, loop e janela
* [ ] Jogador e movimentação
* [ ] Estados básicos introduzidos
* [ ] Chão e gravidade
* [ ] Pulo e colisões
* [ ] Sprite e hitbox do jogador
* [ ] Animações do jogador
* [ ] Moeda animada e contador
* [ ] Inimigo (Orc animado) e trajetória
* [ ] Tela de derrota
* [ ] Reinício com `ENTER`
* [ ] Salas (ida e volta, estado de coleta por sala)
* [ ] Vitória
* [ ] (Bônus) Plataformas

**`base.py` → desenvolvimento gradual → jogo completo (`jogo_completo.py`)**

## Créditos dos assets

Os sprites utilizados nesta oficina foram disponibilizados pela CraftPix
e são utilizados de acordo com os termos da licença da plataforma:

https://craftpix.net/file-licenses/

Os assets não são de autoria dos organizadores da oficina.