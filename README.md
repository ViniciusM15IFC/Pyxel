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
├── pyxel_helper.py
├── base.py
└── sprites/
    ├── personagens/
    │   └── proto/
    ├── inimigos/
    ├── moeda/
    └── cenario/
```

* `pyxel_helper.py` — funções auxiliares fornecidas pela oficina.
* `base.py` — arquivo desenvolvido durante a oficina.

---

# 4. `base.py`

O arquivo auxiliar da oficina é **`pyxel_helper.py`**. As funções e classes necessárias já são importadas no início do `base.py`, então durante a aula o foco fica no código do jogo.

O `base.py` tem quatro seções fixas — **CONFIGURAÇÕES**, **SPRITES**,
**OBJETOS E VARIÁVEIS DO JOGO** e, dentro do loop, **EVENTOS**, **LÓGICA** e
**DESENHO**. As funções e classes da oficina já são importadas no início do
arquivo, então durante a aula o foco fica no código do jogo. Cada etapa do
roteiro indica em qual seção inserir ou ajustar o código. A física é baseada
em tempo (`dt`), não em frames.

```python
import sys
import pygame

from pyxel_helper import (
    criar_janela,
    criar_fonte,
    desenhar_texto,
    carregar_personagem,
    carregar_imagem,
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

# Caminhos da pasta do personagem e dos outros assets.
# None = usar o desenho padrão (retângulo colorido).

SPRITE_PERSONAGEM = None
SPRITE_INIMIGO = "sprites/inimigos/inimigo.png"
SPRITE_MOEDA = "sprites/moeda/moeda.png"
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
    # ...
```

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

### Gravidade

```python
gravidade = 1200
jogador_vel_y = 0
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

## 0:50–1:20 — Sprites e animações

### Objetivo

Substituir os desenhos provisórios por sprites e fazer o personagem se
animação conforme sua ação.

### Personagem

O `Rect` continua representando a hitbox. O sprite representa o visual.

```python
SPRITE_PERSONAGEM = "sprites/personagens/proto/"
```

Usar `carregar_personagem()` para carregar as animações e criar a hitbox a
partir do personagem.

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

## 1:20–1:35 — Moeda e contador

### Objetivo

Adicionar o primeiro objetivo do jogador e introduzir sprites para objetos
do cenário.

### Configuração

```python
SPRITE_MOEDA = "sprites/moeda/moeda.png"
```

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

sprite_moeda = carregar_imagem(
    SPRITE_MOEDA,
    tamanho=(40, 40)
)
```

`carregar_imagem()` retorna `None` se o arquivo não existir. Assim, podemos
manter um desenho provisório enquanto o asset não estiver disponível.

### Coleta

```python
if not moeda_coletada and jogador.colliderect(moeda):
    moeda_coletada = True
    moedas_coletadas += 1
```

### Desenho

```python
if not moeda_coletada:
    if sprite_moeda:
        tela.blit(
            sprite_moeda,
            sprite_moeda.get_rect(center=moeda.center)
        )
    else:
        pygame.draw.rect(tela, AMARELO, moeda)
```

### Trabalhar

* `carregar_imagem()`
* sprite de imagem única
* colisão com a moeda
* variáveis de contagem

### Checkpoint

A moeda aparece como sprite, desaparece ao ser coletada e o contador aumenta.

---

## 1:35–1:50 — Inimigo e trajetória

### Objetivo

Criar um objeto com comportamento próprio e usar um sprite para representá-lo.

### Configuração

```python
SPRITE_INIMIGO = "sprites/inimigos/inimigo.png"
```

### Adicionar em `OBJETOS E VARIÁVEIS DO JOGO`

```python
inimigo = pygame.Rect(
    400,
    300,
    40,
    50
)

inimigo_vel = 3

sprite_inimigo = carregar_imagem(
    SPRITE_INIMIGO,
    tamanho=(60, 60)
)
```

### Movimento e trajetória

```python
inimigo.x += inimigo_vel

if inimigo.left <= 300 or inimigo.right >= 550:
    inimigo_vel *= -1
```

### Colisão

```python
if jogador.colliderect(inimigo):
    estado = DERROTA
```

### Desenho

```python
if sprite_inimigo:
    tela.blit(
        sprite_inimigo,
        sprite_inimigo.get_rect(midbottom=inimigo.midbottom)
    )
else:
    pygame.draw.rect(tela, VERMELHO, inimigo)
```

### Checkpoint

Inimigo aparece com sprite, percorre sua trajetória e pode atingir o jogador.

---

## 1:50–2:05 — Estados e telas: início, derrota e reinício

Agora os estados apresentados anteriormente passam a controlar o fluxo
completo do jogo.

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
moeda_coletada = False
moedas_coletadas = 0
inimigo.x = 400
inimigo_vel = 3
```

### Desenho

Criar as telas de `INICIO` e `DERROTA` com `desenhar_texto()`. A lógica de
gameplay continua protegida por:

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
sala possui sua própria posição de moeda e seu estado de coleta.

```text
┌──────────┐   ↔   ┌──────────┐   ↔   ┌──────────┐
│  SALA 1  │       │  SALA 2  │       │  SALA 3  │
│    🪙    │       │    👾    │       │    🪙    │
└──────────┘       └──────────┘       └──────────┘
```

### Plataformas

As plataformas ficam como extensão opcional caso a turma esteja adiantada.
Elas introduzem caminhos verticais e novas situações de colisão.

```python
plataformas = [
    pygame.Rect(150, 300, 120, 20),
    pygame.Rect(350, 250, 120, 20),
    pygame.Rect(550, 300, 120, 20)
]
```

### Checkpoint

O jogador consegue ir e voltar entre as salas. Uma moeda já coletada não
reaparece ao retornar.

---

## 2:20–2:30 — Vitória + buffer

### Vitória

Ao coletar todas as moedas das salas:

```python
if moedas_coletadas == total_moedas:
    estado = VITORIA
```

Depois, desenhar a tela de vitória.

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
   └── todas as moedas → VITORIA
```

### Buffer

Use os minutos finais para testar, ajustar valores ou corrigir algum ponto
que tenha atrasado. Não corte os checkpoints de funcionamento para ganhar
tempo.

---

# Bônus — Plataformas completas

Se a turma terminar antes, implemente a colisão das plataformas para que o
jogador consiga pousar nelas. Isso fica fora do caminho obrigatório da oficina.

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

### Checkpoint

Jogador consegue pousar nas plataformas e utilizá-las para avançar.

---

# 6. Trocando de personagem (opcional, para quem quiser)

Como a hitbox é calculada automaticamente, trocar de sprite é só:

1. Colocar a pasta nova em `sprites/personagens/<novo_pack>/`
2. Mudar `SPRITE_PERSONAGEM` para apontar para ela
3. Ajustar `frame=` se o pack usar um tamanho de canvas diferente de 128
4. Ajustar os nomes dos arquivos em `animacoes_arquivos` se o pack usar nomes
   diferentes (ex.: `Idle.png` em vez de `Walking.png`)

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
* [ ] Sprite da moeda
* [ ] Moeda e contador
* [ ] Sprite do inimigo
* [ ] Inimigo e trajetória
* [ ] Tela de derrota
* [ ] Reinício com `ENTER`
* [ ] Salas (ida e volta)
* [ ] Vitória
* [ ] (Bônus) Plataformas

**`base.py` → desenvolvimento gradual → jogo completo**

## Créditos dos assets

Os sprites utilizados nesta oficina foram disponibilizados pela CraftPix
e são utilizados de acordo com os termos da licença da plataforma:

https://craftpix.net/file-licenses/

Os assets não são de autoria dos organizadores da oficina.
