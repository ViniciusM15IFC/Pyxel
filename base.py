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

# Caminhos da pasta do personagem.
# None = usar o desenho padrão.

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
