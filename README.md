# Oficina Pyxel — Coleta da Moeda

## Descrição

Oficina prática de programação em Python na qual os alunos são guiados na construção conjunta de um jogo, partindo dos conceitos mais básicos e avançando gradualmente para movimentação, gravidade, colisões, uso de sprites com animações e lógica de jogo.

## Duração

**2h30min**

---

# Objetivos

Ao final da oficina, os alunos deverão compreender e aplicar:

* Estrutura básica de um jogo com Pygame.
* Game loop.
* Eventos e entrada pelo teclado.
* Uso de `Clock` e controle de tempo.
* Coordenadas e `Rect`.
* Movimentação de personagem.
* Gravidade e pulo.
* Colisões.
* Sprites e animações.
* Listas para trabalhar com múltiplos objetos.
* Estados de jogo.
* Salas e transições entre áreas.
* Condições de vitória e derrota.

---

# Estrutura

O jogo será desenvolvido gradualmente, seguindo esta sequência:

1. Janela e game loop
2. Jogador
3. Movimentação
4. Estados do jogo
5. Chão
6. Gravidade
7. Colisão e pulo
8. Sprites
9. Animações
10. Moeda
11. Inimigo
12. Salas
13. Vitória e telas finais
14. Buffer / melhorias opcionais

A ideia é que cada etapa aproveite diretamente o que foi construído na anterior.

---

# `helper.py`

O arquivo `helper.py` já será fornecido.

Os alunos **não precisam editar esse arquivo**. Ele funciona como uma caixa de ferramentas para evitar que a oficina perca tempo com código de infraestrutura.

Entre as funções disponíveis estão:

* `criar_janela()`
* `criar_fonte()`
* `desenhar_texto()`
* `carregar_imagem()`
* `carregar_frames()`
* `carregar_frames_auto()`
* `desenhar_textura()`
* `carregar_personagem()`
* `medir_hitbox()`
* `frame_por_tempo()`
* `Animador`

### Ordem importante

A janela deve ser criada antes do carregamento dos sprites:

```python
tela = criar_janela(...)
```

e somente depois:

```python
carregar_imagem(...)
carregar_frames(...)
carregar_personagem(...)
```

Isso acontece porque o carregamento das imagens utiliza a janela do Pygame para preparar os sprites.

---

# `base.py`

O arquivo `base.py` será desenvolvido durante a oficina.

A estrutura principal será mantida organizada em:

```text
CONFIGURAÇÕES
SPRITES
OBJETOS E VARIÁVEIS DO JOGO

LOOP PRINCIPAL
    EVENTOS
    LÓGICA
    DESENHO
```

A física vertical utilizará `dt`, permitindo que o movimento seja baseado no tempo em vez de depender diretamente da quantidade de quadros por segundo.

---

# Roteiro da oficina

## 0:00–0:05 — Janela e loop

### Objetivo

Criar a janela e compreender o funcionamento básico do game loop.

### Conteúdo

* Importar `pygame`.
* Criar a janela.
* Criar o `Clock`.
* Criar o loop principal.
* Processar o evento de fechar a janela.
* Atualizar a tela.

### Conceito principal

O jogo funciona repetindo continuamente:

```text
eventos
↓
lógica
↓
desenho
↓
próximo quadro
```

### Estrutura inicial

```python
clock = pygame.time.Clock()

while True:

    # EVENTOS

    # LÓGICA

    # DESENHO

    pygame.display.flip()

    dt_ms = clock.tick(60)
```

---

# 0:05–0:15 — Jogador

### Objetivo

Criar o personagem utilizando um `pygame.Rect`.

### Conteúdo

* Criar o `Rect` do jogador.
* Definir posição inicial.
* Definir tamanho.
* Desenhar o jogador como um retângulo.

Inicialmente não é necessário utilizar sprites.

### Exemplo conceitual

```python
jogador = pygame.Rect(
    100,
    200,
    40,
    60
)
```

E no desenho:

```python
pygame.draw.rect(
    tela,
    AZUL,
    jogador
)
```

### Resultado

O jogo já possui:

* janela;
* loop;
* jogador visível.

---

# 0:15–0:25 — Movimentação

### Objetivo

Fazer o jogador responder ao teclado.

### Conteúdo

* `pygame.key.get_pressed()`.
* Teclas A e D.
* Movimento horizontal.
* Velocidade.
* Limites da tela.

### Exemplo

```python
teclas = pygame.key.get_pressed()

if teclas[pygame.K_a]:
    jogador.x -= velocidade

if teclas[pygame.K_d]:
    jogador.x += velocidade
```

### Conceito importante

O jogador não "anda sozinho".

A cada quadro, o programa verifica:

```text
A pressionado?
    ↓
move para esquerda

D pressionado?
    ↓
move para direita
```

Neste momento, o jogo ainda funciona de forma simples, sem estados.

---

# 0:25–0:30 — Introdução aos estados do jogo

### Objetivo

Introduzir os estados somente quando eles passam a ser necessários para organizar o comportamento do jogo.

Até aqui, toda a lógica criada roda diretamente no loop.

Agora o jogo terá diferentes situações:

```text
INICIO
JOGANDO
DERROTA
VITORIA
```

### Primeiro passo

Criar os estados:

```python
INICIO = "INICIO"
JOGANDO = "JOGANDO"
DERROTA = "DERROTA"
VITORIA = "VITORIA"

estado = JOGANDO
```

Neste momento, o objetivo **não é ainda criar todas as telas**.

A ideia é apresentar o conceito:

> O estado informa em qual situação o jogo está e permite decidir qual lógica deve ser executada.

### Reorganização da lógica

Tudo que já foi criado até agora passa a ficar dentro de:

```python
if estado == JOGANDO:

    # MOVIMENTAÇÃO

    ...
```

Por enquanto, o jogo continuará começando diretamente em `JOGANDO`.

### Por que fazer isso agora?

Porque, a partir da próxima etapa, teremos elementos que precisam reagir ao estado do jogo.

Por exemplo:

```text
Jogador encosta no inimigo
        ↓
estado = DERROTA
        ↓
jogador não deve continuar jogando
```

Ou:

```text
Última moeda coletada
        ↓
estado = VITORIA
        ↓
mostrar tela de vitória
```

Assim, o conceito de estado é introduzido **antes de a complexidade aparecer**, mas sem complicar as primeiras etapas.

---

# 0:30–0:35 — Chão

### Objetivo

Criar uma superfície para o jogador ficar apoiado.

### Conteúdo

* Criar `Rect` do chão.
* Desenhar o chão.
* Posicionar o jogador acima dele.

### Exemplo

```python
chao = pygame.Rect(
    0,
    ALTURA - 50,
    LARGURA,
    50
)
```

A lógica continua dentro de:

```python
if estado == JOGANDO:
```

O desenho do chão também ficará dentro do bloco de desenho do estado `JOGANDO`.

### Resultado

O jogo passa a ter:

```text
jogador
──────────────
    chão
```

---

# 0:35–0:45 — Gravidade

### Objetivo

Fazer o jogador cair naturalmente.

### Conceitos

* Velocidade vertical.
* Gravidade.
* `dt`.
* Movimento baseado em tempo.

### Variáveis

```python
gravidade = 1200
jogador_vel_y = 0
```

### Conversão do tempo

```python
dt = dt_ms / 1000
```

O `dt` transforma milissegundos em segundos.

### Aplicação da gravidade

```python
jogador_vel_y += gravidade * dt
jogador.y += jogador_vel_y * dt
```

### Conceito

A gravidade altera a velocidade:

```text
gravidade
    ↓
velocidade vertical
    ↓
posição vertical
```

---

# 0:45–1:00 — Colisão e pulo

### Objetivo

Permitir que o jogador fique sobre o chão e possa pular.

### Colisão com o chão

```python
if jogador.colliderect(chao):

    jogador.bottom = chao.top
    jogador_vel_y = 0
    pulando = False
```

### Pulo

Criar:

```python
forca_pulo = -500
pulando = False
```

No evento de teclado:

```python
if evento.key == pygame.K_SPACE and not pulando:

    jogador_vel_y = forca_pulo
    pulando = True
```

### Conceito importante

O valor negativo faz o jogador subir porque, no Pygame:

```text
y menor → sobe
y maior → desce
```

---

# 1:00–1:15 — Sprites

### Objetivo

Substituir o retângulo do jogador por um personagem visual.

### Conteúdo

* Carregamento de sprites.
* Uso do `helper.py`.
* Separação entre aparência e hitbox.
* Posicionamento do sprite utilizando os pés do personagem.

### Configuração

```python
SPRITE_PERSONAGEM = "sprites/personagens/proto/"
```

### Carregamento

Utilizar:

```python
carregar_personagem(...)
```

O `Rect` continua representando a área de colisão.

O sprite representa apenas a aparência.

### Conceito importante

```text
SPRITE
   ↓
aparência

RECT
   ↓
colisão
```

Isso evita que as áreas transparentes do sprite interfiram na física.

### Desenho

O personagem é desenhado utilizando:

```python
sprite.get_rect(
    midbottom=jogador.midbottom
)
```

Assim, os pés do personagem permanecem alinhados com o `Rect`.

---

# 1:15–1:30 — Animações

### Objetivo

Fazer o personagem trocar de animação de acordo com o que está acontecendo.

### Estados da animação

```text
parado
correndo
pulando
caindo
```

O `Animador` já estará disponível no `helper.py`.

Os alunos não precisam implementar o sistema de troca de frames.

### O jogo decide qual animação utilizar

```python
if jogador_vel_y < 0:
    animador.definir_estado("pulando")

elif jogador_vel_y > 0:
    animador.definir_estado("caindo")

elif movendo:
    animador.definir_estado("correndo")

else:
    animador.definir_estado("parado")
```

Depois:

```python
animador.atualizar(dt_ms)
```

### Conceito importante

O `helper.py` sabe **como** trocar os frames.

O `main.py` decide **qual animação deve estar ativa**.

---

# 1:30–1:45 — Moeda

### Objetivo

Adicionar o primeiro objeto que interage diretamente com o jogador.

### Criar a moeda

Inicialmente, pode ser utilizado um `Rect`.

Depois, substituir sua aparência pelo sprite da moeda.

### Colisão

```python
if jogador.colliderect(moeda):

    moedas_coletadas += 1
```

### Controle da moeda

A moeda precisa deixar de ser coletável depois de ser pega.

```python
moeda_coletada = True
```

### Relação com os estados

Agora fica evidente por que introduzimos `JOGANDO` anteriormente.

A coleta deve acontecer somente enquanto o jogo está efetivamente sendo jogado:

```python
elif estado == JOGANDO:

    # movimento
    # física
    # colisões
    # moeda
```

### Vitória

Quando todas as moedas forem coletadas:

```python
estado = VITORIA
```

A partir desse momento, a lógica normal de gameplay deixa de ser executada.

---

# 1:45–2:00 — Inimigo

### Objetivo

Adicionar um obstáculo que pode causar derrota.

### Estrutura

Cada inimigo pode possuir:

```python
{
    "rect": ...,
    "vel_x": ...,
    "limite_esq": ...,
    "limite_dir": ...
}
```

### Movimento

```python
inimigo["rect"].x += inimigo["vel_x"]
```

Quando chegar ao limite:

```python
inimigo["vel_x"] *= -1
```

### Colisão

```python
if jogador.colliderect(inimigo["rect"]):

    estado = DERROTA
```

### Ponto importante

A partir de agora, fica clara a utilidade do estado:

```text
JOGANDO
    ↓
colisão com inimigo
    ↓
DERROTA
    ↓
para de executar a lógica de gameplay
```

O jogador não deve continuar andando, pulando ou coletando moedas enquanto estiver em `DERROTA`.

---

# 2:00–2:15 — Salas e transições

### Objetivo

Transformar o jogo em uma sequência de salas com desafios diferentes.

### Estrutura

Cada sala poderá possuir:

* posição da moeda;
* plataformas;
* inimigos;
* limites específicos.

Exemplo conceitual:

```python
salas = [
    {
        "moeda": (...),
        "plataformas": [...],
        "inimigos": [...]
    },
    ...
]
```

### Sala atual

```python
sala_atual = 0
```

### Transição para a direita

Quando o jogador chegar ao lado direito:

```python
if jogador.right >= LARGURA:
    ...
```

Se houver outra sala:

```python
sala_atual += 1
```

O jogador é reposicionado no lado esquerdo.

### Retorno para a sala anterior

Também será permitido retornar:

```python
if jogador.left <= 0:
    ...
```

Se existir uma sala anterior:

```python
sala_atual -= 1
```

O jogador é reposicionado no lado direito.

### Por que permitir retorno?

Como as moedas podem ser coletadas em salas diferentes, o jogador precisa poder voltar caso tenha deixado alguma para trás.

### Resultado

O jogo passa a ter:

```text
SALA 1 ←→ SALA 2 ←→ SALA 3
```

---

# 2:15–2:25 — Telas de início, derrota e vitória

Agora que os estados já estão sendo utilizados pela lógica do jogo, serão criadas as telas correspondentes.

## Início

```python
if estado == INICIO:
```

Mostrar:

```text
COLETA DA MOEDA

Pressione ENTER para começar
```

O jogo começa quando o jogador pressiona `ENTER`.

---

## JOGANDO

```python
elif estado == JOGANDO:
```

Executar:

* movimentação;
* gravidade;
* pulo;
* colisões;
* animações;
* inimigos;
* moedas;
* transições entre salas.

E desenhar:

* chão;
* plataformas;
* moedas;
* inimigos;
* jogador;
* HUD.

---

## Derrota

```python
elif estado == DERROTA:
```

Mostrar:

```text
GAME OVER!

Pressione ENTER para tentar de novo
```

A lógica normal do jogo não deve mais ser executada.

---

## Vitória

```python
elif estado == VITORIA:
```

Mostrar:

```text
MISSÃO CUMPRIDA!

Você coletou todas as moedas!
```

A lógica normal do jogo também não deve mais ser executada.

---

# Fluxo final dos estados

Ao final da etapa, o jogo terá o seguinte fluxo:

```text
                 ENTER
                   ↓
                INICIO
                   ↓
                JOGANDO
                ↙       ↘
          inimigo       moedas
             ↓             ↓
          DERROTA       VITORIA
             ↓             ↓
           ENTER         ENTER
             └──────┬──────┘
                    ↓
                 JOGANDO
```

---

# 2:25–2:30 — Vitória + buffer

Últimos minutos destinados a:

* testar o jogo completo;
* corrigir pequenos erros;
* testar as transições entre salas;
* verificar colisões;
* verificar vitória e derrota;
* testar diferentes configurações de sprites.

Caso tudo esteja funcionando, podem ser adicionadas melhorias opcionais.

---

# Bônus — Plataformas

As plataformas podem ser utilizadas para aumentar a dificuldade das salas.

### Colisão

A colisão deve considerar principalmente quando o jogador está caindo:

```python
if (
    jogador.colliderect(plataforma)
    and jogador_vel_y >= 0
):
    ...
```

A plataforma passa a funcionar como uma superfície adicional para o jogador.

### Possibilidades

* plataformas estáticas;
* diferentes alturas;
* obstáculos;
* parkour;
* salas com desafios diferentes.

As plataformas não são necessárias para completar a oficina.

---

# Resultado esperado

Ao final da oficina, o jogo deverá possuir:

* [ ] Janela funcionando.
* [ ] Game loop.
* [ ] Jogador.
* [ ] Movimento horizontal.
* [ ] Pulo.
* [ ] Gravidade.
* [ ] Colisões.
* [ ] Sprite do personagem.
* [ ] Animações.
* [ ] Moedas.
* [ ] Inimigos.
* [ ] Derrota.
* [ ] Vitória.
* [ ] Tela inicial.
* [ ] Múltiplas salas.
* [ ] Transição para a próxima sala.
* [ ] Retorno para salas anteriores.
* [ ] Contador de moedas.
* [ ] Diferentes desafios por sala.
* [ ] Possibilidade de substituir sprites sem alterar a lógica principal.
* [ ] Código organizado em `helper.py` e `base.py`.
