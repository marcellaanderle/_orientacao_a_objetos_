import math

import pygame.image

from dinamite import Dinamite

TAMANHO_FRAME = 4


class Jogador:
    pos_x = 4
    pos_y = 4
    frame = 0
    qtd_dinamites = 3
    tamanho_dinamite = 3
    animacao = []
    direcao = 0  # referencia de qual img vai ser utilizada (0 = esquerda, 1 = direita)
    vivo = True
    venceu = False

    def __init__(self, escala):
        self.carrega_imgs(escala)

    def move(self, mapa, mov_x, mov_y):
        atual_x = int(self.pos_x / TAMANHO_FRAME)
        atual_y = int(self.pos_y / TAMANHO_FRAME)

        copia_mapa = []

        for i in range(len(mapa)):
            copia_mapa.append([])
            for j in range(len(mapa[i])):
                copia_mapa[i].append(mapa[i][j])

        if self.pos_x % TAMANHO_FRAME != 0 and mov_x == 0:
            if self.pos_x % TAMANHO_FRAME == 1:
                self.pos_x -= 1
            if self.pos_x % TAMANHO_FRAME == 3:
                self.pos_x += 1

        if self.pos_y % TAMANHO_FRAME != 0 and mov_y == 0:
            if self.pos_y % TAMANHO_FRAME == 1:
                self.pos_y -= 1
            elif self.pos_y % TAMANHO_FRAME == 3:
                self.pos_y += 1

        # direita
        if mov_x == 1:
            if copia_mapa[atual_x + 1][atual_y] in [0,3]:
                self.pos_x += 1
        # esquerda
        if mov_x == -1:
            atual_x = math.ceil(self.pos_x / TAMANHO_FRAME)
            if copia_mapa[atual_x - 1][atual_y] in [0,3]:
                self.pos_x -= 1
        # baixo
        if mov_y == 1:
            if copia_mapa[atual_x][atual_y + 1] in [0,3]:
                self.pos_y += 1
        # cima
        if mov_y == -1:
            atual_y = math.ceil(self.pos_y / TAMANHO_FRAME)
            if copia_mapa[atual_x][atual_y - 1] in [0,3]:
                self.pos_y -= 1

        if copia_mapa[int(self.pos_x / TAMANHO_FRAME)][int(self.pos_y / TAMANHO_FRAME)] == 3:
            self.venceu = True

    def coloca_dinamite(self, mapa, dinamites):
        existe_dinamite_posicao_atual = False
        for dinamite in dinamites:
            if dinamite.pos_x == int(self.pos_x / TAMANHO_FRAME) and dinamite.pos_y == int(self.pos_y / TAMANHO_FRAME):
                existe_dinamite_posicao_atual = True

        if self.qtd_dinamites > 0 and not existe_dinamite_posicao_atual:
            self.qtd_dinamites -= 1
            return Dinamite(self.tamanho_dinamite,
                            round(self.pos_x / TAMANHO_FRAME),
                            round(self.pos_y / TAMANHO_FRAME),
                            mapa,
                            self)
        else:
            return None

    def verifica_morte(self, explosoes):
        for explosao in explosoes:
            for local in explosao.espacos_afetados:
                if int(self.pos_x / TAMANHO_FRAME) == local[0] and int(self.pos_y / TAMANHO_FRAME) == local[1]:
                    self.vivo = False

    def carrega_imgs(self, escala):
        # Nesse momento só terá animações de esquerda e direita

        l1 = pygame.image.load('imagens/galinha/gl_1.png')
        l1 = pygame.transform.scale(l1, (escala, escala))

        l2 = pygame.image.load('imagens/galinha/gl_2.png')
        l2 = pygame.transform.scale(l2, (escala, escala))

        l3 = pygame.image.load('imagens/galinha/gl_3.png')
        l3 = pygame.transform.scale(l3, (escala, escala))

        r1 = pygame.image.load('imagens/galinha/gr_1.png')
        r1 = pygame.transform.scale(r1, (escala, escala))

        r2 = pygame.image.load('imagens/galinha/gr_2.png')
        r2 = pygame.transform.scale(r2, (escala, escala))

        r3 = pygame.image.load('imagens/galinha/gr_3.png')
        r3 = pygame.transform.scale(r3, (escala, escala))

        esquerda = [r1, r2, r3] # TODO corrigir referencias
        direita = [l1, l2, l3]

        self.animacao.append(esquerda)
        self.animacao.append(direita)
