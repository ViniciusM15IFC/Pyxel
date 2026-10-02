"""
helper.py - funções prontas para a oficina de jogos com Pygame.

Vocês alunos NÃO precisam mexer aqui: só importar e chamar.

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


def frame_por_tempo(frames, ms_por_frame=100):
    """Escolhe o frame atual só pelo relógio (bom para itens simples, como a moeda)."""
    return frames[(pygame.time.get_ticks() // ms_por_frame) % len(frames)]

def desenhar_textura(tela, imagem, retangulo):
    if imagem is None:
        return

    largura = imagem.get_width()
    altura = imagem.get_height()

    for y in range(retangulo.top, retangulo.bottom, altura):
        for x in range(retangulo.left, retangulo.right, largura):
            tela.blit(imagem, (x, y))

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
