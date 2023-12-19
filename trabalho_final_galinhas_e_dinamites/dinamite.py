from Explosao import Explosao


class Dinamite:
    frame = 0

    def __init__(self, tamanho, pos_x, pos_y, mapa, galinha):
        self.tamanho = tamanho
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tempo = 3000
        self.galinha = galinha
        self.espacos_afetados = []
        self.define_locais_afetados(mapa)

    def atualiza(self, tempo_transcorrido):
        self.tempo = self.tempo - tempo_transcorrido
        if self.tempo < 1000:
            self.frame = 2
        elif self.tempo < 2000:
            self.frame = 1

    def explode(self):
        if self.tempo < 1:
            self.galinha.qtd_dinamites += 1
            return Explosao(self.pos_x, self.pos_y, self.galinha.tamanho_dinamite)

    def define_locais_afetados(self, mapa):
        self.espacos_afetados.append([self.pos_x, self.pos_y])

        # locais afetados a direita
        for x in range(1, self.tamanho):
            valor_posicao = mapa[self.pos_x + x][self.pos_y]
            if valor_posicao in [0, 3]:  # espaço vazio ou ovos
                self.espacos_afetados.append([self.pos_x + x, self.pos_y])
            elif valor_posicao == 1:  # parede de gelo
                self.espacos_afetados.append([self.pos_x + x, self.pos_y])
                break
            else:  # geleira
                break

        # locais afetados a esquerda
        for x in range(1, self.tamanho):
            valor_posicao = mapa[self.pos_x - x][self.pos_y]
            if valor_posicao in [0, 3]:
                self.espacos_afetados.append([self.pos_x - x, self.pos_y])
            elif valor_posicao == 1:
                self.espacos_afetados.append([self.pos_x - x, self.pos_y])
                break
            else:
                break

        # locais afetados a cima
        for y in range(1, self.tamanho):
            valor_posicao = mapa[self.pos_x][self.pos_y - y]
            if valor_posicao in [0, 3]:
                self.espacos_afetados.append([self.pos_x, self.pos_y - y])
            if valor_posicao == 1:
                self.espacos_afetados.append([self.pos_x, self.pos_y - y])
                break
            else:
                break

        # locais afetados a baixo
        for y in range(1, self.tamanho):
            valor_posicao = mapa[self.pos_x][self.pos_y + y]
            if valor_posicao in [0, 3]:
                self.espacos_afetados.append([self.pos_x, self.pos_y + y])
            if valor_posicao == 1:
                self.espacos_afetados.append([self.pos_x, self.pos_y + y])
                break
            else:
                break
