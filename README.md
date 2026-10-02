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

* `helper.py` — funções auxiliares fornecidas pela oficina.
* `base.py` — arquivo desenvolvido durante a oficina.

---

# 3. `helper.py`

Arquivo fornecido pela oficina.

<details>
<summary>📄 Código do helper.py</summary>

```python
# colocar aqui o helper.py completo
```

</details>

---

# 4. `base.py`

O `base.py` deve começar com **marcadores indicando onde cada etapa será adicionada**.

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


    # ========================================================
    # [1] OBJETOS E VARIÁVEIS DO JOGO
    # ========================================================

    # Jogador
    # Chão
    # Gravidade
    # Velocidade vertical
    # Estado do pulo


    while True:

        # ====================================================
        # [2] TEMPO
        # ====================================================

        dt_ms = clock.tick(60)
        tela.fill(BRANCO)


        # ====================================================
        # [3] EVENTOS
        # ====================================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Teclas pressionadas uma vez
            # Ex.: pulo


        # ====================================================
        # [4] ENTRADA CONTÍNUA
        # ====================================================

        # A / D


        # ====================================================
        # [5] FÍSICA E MOVIMENTO
        # ====================================================

        # dt
        # Gravidade
        # Movimento vertical
        # Colisão com o chão


        # ====================================================
        # [6] MOEDA
        # ====================================================

        # Criar moeda
        # Detectar coleta
        # Contador


        # ====================================================
        # [7] INIMIGO
        # ====================================================

        # Movimento
        # Limites
        # Colisão com jogador


        # ====================================================
        # [8] ESTADOS DO JOGO
        # ====================================================

        # INICIO
        # JOGANDO
        # DERROTA
        # VITORIA


        # ====================================================
        # [9] SALAS
        # ====================================================

        # Sala atual
        # Configuração da sala
        # Transição


        # ====================================================
        # [10] PLATAFORMAS
        # ====================================================

        # Criar
        # Desenhar
        # Colisão


        # ====================================================
        # [11] SPRITES E ANIMAÇÕES
        # ====================================================

        # Carregar personagem
        # Animador
        # Atualizar animação
        # Desenhar sprite


        # ====================================================
        # [12] DESENHO
        # ====================================================

        # Jogador
        # Chão
        # Moeda
        # Inimigo
        # Plataformas
        # HUD


        pygame.display.flip()


if __name__ == "__main__":
    main()
```

---

# 5. Roteiro de execução

## 0:00–0:10 — Janela e loop

### Objetivo

Garantir que todos tenham a janela funcionando.

### Trabalhar

* `pygame.init()`
* `while`
* eventos
* `Clock`
* `60 FPS`
* atualização da tela

### Base

Nenhuma alteração estrutural necessária.

### Checkpoint

Janela abre, permanece funcionando e fecha pelo `X`.

---

## 0:10–0:20 — Jogador

### Adicionar em `[1] OBJETOS E VARIÁVEIS`

```python
jogador = pygame.Rect(
    100,
    300,
    40,
    50
)
```

### Adicionar em `[12] DESENHO`

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

## 0:20–0:35 — Movimentação

### Adicionar em `[4] ENTRADA CONTÍNUA`

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

## 0:35–0:40 — Chão

### Adicionar em `[1] OBJETOS E VARIÁVEIS`

```python
chao = pygame.Rect(
    0,
    350,
    LARGURA,
    50
)
```

### Adicionar em `[12] DESENHO`

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

## 0:40–0:50 — Gravidade

### Adicionar em `[1] OBJETOS E VARIÁVEIS`

```python
gravidade = 1200
jogador_vel_y = 0
```

### Adicionar em `[5] FÍSICA E MOVIMENTO`

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

### Checkpoint

Jogador cai.

---

## 0:50–1:05 — Colisão e pulo

### Adicionar em `[1] OBJETOS E VARIÁVEIS`

```python
pulando = False
```

### Adicionar em `[5] FÍSICA E MOVIMENTO`

```python
if jogador.colliderect(chao):
    jogador.bottom = chao.top
    jogador_vel_y = 0
    pulando = False
```

### Adicionar em `[3] EVENTOS`

```python
if evento.type == pygame.KEYDOWN:
    if evento.key == pygame.K_SPACE and not pulando:
        jogador_vel_y = -500
        pulando = True
```

### Checkpoint

Jogador cai, para no chão e consegue pular.

### ⚠️ Atenção

`jogador_vel_y` é uma **variável separada do `jogador`**. Não usar `jogador.vel_y`.

---

## 1:05–1:15 — Sprite

Substituir o retângulo do jogador pelo sprite.

### Alterar

* `[1]` → carregamento/configuração
* `[12]` → `blit`

### Checkpoint

O personagem aparece no lugar do retângulo.

---

## 1:15–1:25 — Animações

### Adicionar em `[11] SPRITES E ANIMAÇÕES`

* Criar `Animador`
* Carregar animações
* Definir estado
* Atualizar animação
* Virar sprite conforme direção

Estados:

```python
"parado"
"correndo"
"pulando"
"caindo"
```

### Checkpoint

Personagem troca de animação conforme o movimento.

---

## 1:25–1:40 — Moeda

### Adicionar em `[1] OBJETOS E VARIÁVEIS`

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

### Adicionar em `[6] MOEDA`

```python
if not moeda_coletada:
    if jogador.colliderect(moeda):
        moeda_coletada = True
        moedas_coletadas += 1
```

### Adicionar em `[12] DESENHO`

Desenhar somente enquanto não estiver coletada.

### Checkpoint

Moeda desaparece ao ser coletada e contador aumenta.

---

## 1:40–1:55 — Inimigo

### Adicionar em `[1] OBJETOS E VARIÁVEIS`

```python
inimigo = pygame.Rect(
    400,
    300,
    40,
    50
)

inimigo_vel = 3
```

### Adicionar em `[7] INIMIGO`

```python
inimigo.x += inimigo_vel

if inimigo.left <= 300 or inimigo.right >= 550:
    inimigo_vel *= -1
```

Colisão:

```python
if jogador.colliderect(inimigo):
    # derrota
```

### Checkpoint

Inimigo patrulha e pode atingir o jogador.

---

## 1:55–2:00 — Estados

### Adicionar em `[8] ESTADOS DO JOGO`

```python
INICIO = "INICIO"
JOGANDO = "JOGANDO"
DERROTA = "DERROTA"
VITORIA = "VITORIA"

estado = INICIO
```

Separar a lógica/desenho conforme o estado.

### Checkpoint

Jogo possui início, gameplay, derrota e vitória.

---

## 2:00–2:10 — Salas

### Adicionar em `[9] SALAS`

Criar:

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

sala_atual = 0
```

Adicionar transição pela borda direita:

```python
if jogador.right >= LARGURA:
    if sala_atual < len(salas) - 1:
        sala_atual += 1
        jogador.left = 20
```

### Checkpoint

Jogador consegue passar de uma sala para outra.

---

## 2:10–2:20 — Plataformas

### Adicionar em `[10] PLATAFORMAS`

```python
plataformas = [
    pygame.Rect(150, 300, 120, 20),
    pygame.Rect(350, 250, 120, 20),
    pygame.Rect(550, 300, 120, 20)
]
```

Desenhar:

```python
for plataforma in plataformas:
    pygame.draw.rect(
        tela,
        VERDE,
        plataforma
    )
```

Adicionar colisão vertical.

### Checkpoint

Jogador consegue pousar nas plataformas e utilizá-las para avançar.

---

## 2:20–2:25 — Vitória

### Adicionar em `[6] MOEDA` / `[8] ESTADOS`

```python
if moedas_coletadas == total_moedas:
    estado = VITORIA
```

Na tela de vitória:

```python
desenhar_texto(
    tela,
    "VOCÊ VENCEU!",
    fonte_grande,
    PRETO,
    LARGURA // 2,
    ALTURA // 2
)
```

### Checkpoint

Coletar todas as moedas leva à vitória.

---

## 2:25–2:30 — Teste e ajustes

Testar rapidamente:

```python
gravidade = 800
```

```python
jogador_vel_y = -600
```

```python
inimigo_vel = 5
```

Verificar:

* Movimento
* Pulo
* Colisões
* Moedas
* Inimigos
* Salas
* Plataformas
* Vitória
* Derrota

---

# 6. Resultado esperado

* [] Janela e loop
* [] Movimentação
* [] Gravidade
* [] Pulo
* [] Colisões
* [] Sprite
* [] Animações
* [] Moedas
* [] Contador
* [] Inimigo
* [] Estados
* [] Salas
* [] Transições
* [] Plataformas
* [] Vitória
* [] Derrota

**`base.py` → desenvolvimento gradual → jogo completo**
