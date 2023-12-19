import random
import sys

import pygame.image
from pygame import Surface, SurfaceType
import Constantes
from jogador import Jogador


class Jogo:

    def __init__(self, escala, surface):
        self.escala = escala
        self.surface = surface
        self.mapa = [[0] * Constantes.TAMANHO_MAPA for i in range(0, Constantes.TAMANHO_MAPA)]
        self.dinamites = []
        self.explosoes = []
        self.galinha = Jogador(self.escala)

    def criar_mapa(self) -> None:
        for i in range(0, Constantes.TAMANHO_MAPA):
            for j in range(0, Constantes.TAMANHO_MAPA):
                if i in [0, 14] or j in [0, 14] or (i % 2 == 0 and j % 2 == 0) and i not in [1, 13] and j not in [1, 13]:
                    self.mapa[i][j] = Constantes.GELEIRA

                elif (i == 1 and j == 1) or (i == 2 and j == 1) or (i == 1 and j == 2):
                    continue
                else:
                    self.mapa[i][j] = random.randint(0,1)
                    # self.mapa[i][j] = 0 #  Modo sem obstaculos

        # definindo posição dos ovos
        random.seed()
        posicao_ovos = random.randint(0, 2)
        if posicao_ovos == 0:
            self.mapa[1][13] = Constantes.OVOS
        elif posicao_ovos == 1:
            self.mapa[13][1] = Constantes.OVOS
        else:
            self.mapa[13][13] = Constantes.OVOS

        # mostrando mapa para testes
        # for i in range(0, TAMANHO_MAPA):
        #     for j in range(0, TAMANHO_MAPA):
        #         print(mapa[i][j]," ", end="")
        #     print()

    def carrega_img_mapa(self, escala) -> [Surface | SurfaceType]:
        chao_img = pygame.image.load('imagens/cenario/grama.png')
        chao_img = pygame.transform.scale(chao_img, (escala, escala))

        parede_gelo_img = pygame.image.load('imagens/cenario/parede_gelo.png')
        parede_gelo_img = pygame.transform.scale(parede_gelo_img, (escala, escala))

        geleira_img = pygame.image.load('imagens/cenario/geleira.png')
        geleira_img = pygame.transform.scale(geleira_img, (escala, escala))

        ovos_img = pygame.image.load('imagens/cenario/ovos.png')
        ovos_img = pygame.transform.scale(ovos_img, (escala, escala))

        return [chao_img, parede_gelo_img, geleira_img, ovos_img]

    def carrega_img_dinamites(self, escala) -> [Surface | SurfaceType]:
        dinamite1_img = pygame.image.load('imagens/dinamite/d_1.png')
        dinamite1_img = pygame.transform.scale(dinamite1_img, (escala, escala))

        dinamite2_img = pygame.image.load('imagens/dinamite/d_2.png')
        dinamite2_img = pygame.transform.scale(dinamite2_img, (escala, escala))

        dinamite3_img = pygame.image.load('imagens/dinamite/d_3.png')
        dinamite3_img = pygame.transform.scale(dinamite3_img, (escala, escala))

        return [dinamite1_img, dinamite2_img, dinamite3_img]

    def carrega_img_explosoes(self, escala) -> [Surface | SurfaceType]:
        explosao1_img = pygame.image.load('imagens/explosao/explosao_1.png')
        explosao1_img = pygame.transform.scale(explosao1_img, (escala, escala))

        explosao2_img = pygame.image.load('imagens/explosao/explosao_2.png')
        explosao2_img = pygame.transform.scale(explosao2_img, (escala, escala))

        explosao3_img = pygame.image.load('imagens/explosao/explosao_3.png')
        explosao3_img = pygame.transform.scale(explosao3_img, (escala, escala))

        return [explosao1_img, explosao2_img, explosao3_img]

    def existe_ovo(self):
        return self.mapa[1][13] == Constantes.OVOS or self.mapa[13][1] == Constantes.OVOS or self.mapa[13][13] == Constantes.OVOS

    def desenha_tela(self, surface, escala, terreno_imgs, dinamite_imgs, explosoes_imgs):
        surface.fill(Constantes.COLOR_BACKGROUND)
        for i in range(0, Constantes.TAMANHO_MAPA):
            for j in range(0, Constantes.TAMANHO_MAPA):
                surface.blit(terreno_imgs[self.mapa[i][j]], (i * escala, j * escala))

        for dinamite in self.dinamites:
            surface.blit(dinamite_imgs[dinamite.frame], (dinamite.pos_x * escala, dinamite.pos_y * escala))

        for explosao in self.explosoes:
            for local_afetado in explosao.espacos_afetados:
                surface.blit(explosoes_imgs[explosao.frame], (local_afetado[0] * escala, local_afetado[1] * escala))

        if self.galinha.vivo:
            surface.blit(self.galinha.animacao[self.galinha.direcao][self.galinha.frame],
                         (self.galinha.pos_x * (escala / 4), self.galinha.pos_y * (escala / 4)))

        if self.galinha.venceu:
            tf = pygame.font.SysFont('Bebas', escala).render("Você venceu! Pressione ESC para sair", False, (0, 0, 0))
            surface.blit(tf, (10, 10))

        if not self.existe_ovo() or not self.galinha.vivo:
            tf = pygame.font.SysFont('Bebas', escala).render("Você perdeu! Pressione ESC para sair", False, (0, 0, 0))
            surface.blit(tf, (10, 10))

        pygame.display.update()

    def partida(self) -> None:
        self.carrega_musica()
        self.criar_mapa()
        terreno_imgs = self.carrega_img_mapa(self.escala)
        dinamite_imgs = self.carrega_img_dinamites(self.escala)
        explosoes_imgs = self.carrega_img_explosoes(self.escala)

        self.jogo_em_execucao(self.surface, self.escala, terreno_imgs, dinamite_imgs, explosoes_imgs)

    def carrega_musica(self):
        pygame.mixer.music.load("sons/tchakabum-explosao.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def atualiza_dinamites(self, mapa, tick):
        for dinamite in self.dinamites:
            dinamite.atualiza(tick)
            explosao = dinamite.explode()
            if explosao is not None:
                explosao.explode(mapa, self.dinamites, dinamite)
                self.explosoes.append(explosao)
                explosao.afeta_mapa(mapa)

        self.galinha.verifica_morte(self.explosoes)

        for explosao in self.explosoes:
            explosao.atualiza(tick, self.explosoes)

    def jogo_em_execucao(self, surface, escala, terreno_imgs, dinamite_imgs, explosoes_imgs):
        clock = pygame.time.Clock()

        em_execucao = True

        while em_execucao:
            tick = clock.tick(15)

            if self.galinha.vivo:
                botao = pygame.key.get_pressed()
                alterou_posicao = False
                direcao_movimento = self.galinha.direcao
                if botao[pygame.K_UP]:
                    self.galinha.move(self.mapa, 0, -1)
                    alterou_posicao = True
                elif botao[pygame.K_DOWN]:
                    self.galinha.move(self.mapa, 0, 1)
                    alterou_posicao = True
                elif botao[pygame.K_LEFT]:
                    direcao_movimento = 0
                    self.galinha.move(self.mapa, -1, 0)
                    alterou_posicao = True
                elif botao[pygame.K_RIGHT]:
                    direcao_movimento = 1
                    self.galinha.move(self.mapa, 1, 0)
                    alterou_posicao = True

                if direcao_movimento != self.galinha.direcao:
                    self.galinha.frame = 0
                    self.galinha.direcao = direcao_movimento

                if alterou_posicao:
                    if self.galinha.frame == 2:
                        self.galinha.frame = 0
                    else:
                        self.galinha.frame += 1

            self.desenha_tela(surface, escala, terreno_imgs, dinamite_imgs, explosoes_imgs)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        dinamite = self.galinha.coloca_dinamite(self.mapa, self.dinamites)
                        if dinamite is not None:
                            self.dinamites.append(dinamite)

                    elif event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        em_execucao = False

            self.atualiza_dinamites(self.mapa, tick)
