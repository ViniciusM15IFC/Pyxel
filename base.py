import sys
import pygame

from pyxel_helper import (
    criar_janela,
    criar_fonte,
    desenhar_texto,
    carregar_personagem,
    carregar_frames,
    carregar_frames_grade,
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
