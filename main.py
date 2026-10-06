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

SPRITE_PERSONAGEM = "sprites/personagens/proto/"      # etapa 0:50
SPRITE_INIMIGO = "sprites/inimigos/orc.png"           # etapa 1:35
SPRITE_MOEDA = "sprites/moeda/moeda_sheet.png"        # etapa 1:20


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    clock = pygame.time.Clock()


    # ========================================================
    # OBJETOS E VARIÁVEIS DO JOGO
    # ========================================================

    # --- 0:20 Estados (1:50: o jogo passa a começar em INICIO) ---
    INICIO = "INICIO"
    JOGANDO = "JOGANDO"
    DERROTA = "DERROTA"
    VITORIA = "VITORIA"

    estado = INICIO

    # --- 0:25 Chão e gravidade ---
    chao = pygame.Rect(
        0,
        350,
        LARGURA,
        50
    )

    gravidade = 1200
    jogador_vel_y = 0
    pulando = False

    # --- 2:05 Plataformas (usadas na colisão do Bônus) ---
    plataformas = [
        pygame.Rect(150, 300, 120, 20),
        pygame.Rect(350, 250, 120, 20),
        pygame.Rect(550, 300, 120, 20)
    ]

    # --- 0:50 Jogador com sprite (substitui o Rect fixo do 0:05) ---
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

    # --- 1:20 Frames da moeda ---
    frames_moeda = carregar_frames_auto(
        SPRITE_MOEDA,
        (40, 40),
        remover_fundo_branco=True,
        ignorar_rodape=0.15
    )

    # --- 1:35 Frames do inimigo ---
    frames_orc = carregar_frames_grade(
        SPRITE_INIMIGO,
        100,
        100,
        (60, 60)
    )

    # --- 2:05 Salas (substituem moeda, moeda_coletada, inimigo, inimigo_vel) ---
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
            if evento.type == pygame.KEYDOWN:

                # --- 1:50 / 2:20 ENTER em INICIO, DERROTA e VITORIA ---
                if estado == INICIO or estado == DERROTA or estado == VITORIA:
                    if evento.key == pygame.K_RETURN:
                        estado = JOGANDO

                        # Reset
                        jogador.x = 100
                        jogador.bottom = chao.top
                        jogador_vel_y = 0
                        pulando = False
                        animador.olhando_direita = True
                        salas = criar_salas()
                        sala_atual = 0
                        moedas_coletadas = 0

                # --- 0:25 Pulo ---
                if evento.key == pygame.K_SPACE and not pulando:
                    jogador_vel_y = -500
                    pulando = True


        # ====================================================
        # LÓGICA
        # ====================================================

        if estado == JOGANDO:

            dt = dt_ms / 1000

            # --- 0:05 / 0:50 Entrada contínua (A / D) ---
            teclas = pygame.key.get_pressed()

            andando = False

            if teclas[pygame.K_a]:
                jogador.x -= 5
                animador.olhando_direita = False
                andando = True

            if teclas[pygame.K_d]:
                jogador.x += 5
                animador.olhando_direita = True
                andando = True

            # --- 0:25 Gravidade ---
            jogador_vel_y += gravidade * dt
            jogador.y += jogador_vel_y * dt

            # --- 0:25 Colisão com o chão ---
            if jogador.colliderect(chao):
                jogador.bottom = chao.top
                jogador_vel_y = 0
                pulando = False

            # --- Bônus: colisão com as plataformas ---
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

            # --- 2:05 Passo 2: passar de sala nas bordas (ida e volta) ---
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

            # --- 2:05 Passo 1: tudo abaixo olha para a sala atual ---
            sala = salas[sala_atual]

            # Moeda (1:20 + 2:20 vitória)
            moeda = sala["moeda"]

            if (
                moeda is not None
                and not sala["coletada"]
                and jogador.colliderect(moeda)
            ):
                sala["coletada"] = True
                moedas_coletadas += 1

                if moedas_coletadas == total_moedas:
                    estado = VITORIA

            # Inimigo (1:35)
            inimigo = sala["inimigo"]

            if inimigo is not None:
                inimigo.x += sala["inimigo_vel"]

                if inimigo.left <= 300 or inimigo.right >= 550:
                    sala["inimigo_vel"] *= -1

                if jogador.colliderect(inimigo):
                    estado = DERROTA

            # --- 0:50 Estado de animação do jogador ---
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


        # ====================================================
        # DESENHO
        # ====================================================

        if estado == INICIO:
            desenhar_texto(tela, "Coleta da Moeda", fonte_titulo, PRETO, LARGURA // 2, 140)
            desenhar_texto(tela, "Pressione ENTER para jogar", fonte_texto, AZUL, LARGURA // 2, 230)

        elif estado == JOGANDO:

            sala = salas[sala_atual]

            # Chão (0:25)
            pygame.draw.rect(tela, VERDE, chao)

            # Plataformas (Bônus)
            for plataforma in plataformas:
                pygame.draw.rect(tela, AZUL, plataforma)

            # Moeda (1:20 / 2:05)
            if sala["moeda"] is not None and not sala["coletada"]:
                img = frame_por_tempo(frames_moeda, 100)
                tela.blit(img, img.get_rect(center=sala["moeda"].center))

            # Inimigo (1:35 / 2:05)
            if sala["inimigo"] is not None:
                img = frame_por_tempo(frames_orc, 120)

                if sala["inimigo_vel"] < 0:
                    img = pygame.transform.flip(img, True, False)

                tela.blit(img, img.get_rect(midbottom=sala["inimigo"].midbottom))

            # Jogador (0:50)
            img = animador.imagem_atual()
            tela.blit(img, img.get_rect(midbottom=jogador.midbottom))

            # HUD (2:05 passo 3)
            desenhar_texto(
                tela,
                f"Moedas: {moedas_coletadas}/{total_moedas}   Sala {sala_atual + 1}/{len(salas)}",
                fonte_texto,
                PRETO,
                LARGURA // 2,
                30
            )

        elif estado == DERROTA:
            desenhar_texto(tela, "Você perdeu!", fonte_titulo, VERMELHO, LARGURA // 2, 140)
            desenhar_texto(tela, "Pressione ENTER para reiniciar", fonte_texto, PRETO, LARGURA // 2, 230)

        elif estado == VITORIA:
            desenhar_texto(tela, "Você venceu!", fonte_titulo, AMARELO, LARGURA // 2, 140)
            desenhar_texto(tela, "Pressione ENTER para jogar de novo", fonte_texto, PRETO, LARGURA // 2, 230)


        pygame.display.flip()


if __name__ == "__main__":
    main()