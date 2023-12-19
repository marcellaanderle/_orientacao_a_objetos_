class Explosao:
    def __init__(self, pos_x, pos_y, tamanho):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tamanho = tamanho
        self.tempo = 300
        self.frame = 0
        self.espacos_afetados = []

    def explode(self, mapa, dinamites, dinamite):
        self.espacos_afetados.extend(dinamite.espacos_afetados)
        dinamites.remove(dinamite)
        self.bombas_afetadas(mapa, dinamites)

    def bombas_afetadas(self, mapa, dinamites):
        for espaco in self.espacos_afetados:
            for dinamite in dinamites:
                if dinamite.pos_x == espaco[0] and dinamite.pos_y == espaco[1]:
                    mapa[dinamite.pos_x][dinamite.pos_y] = 0
                    dinamite.galinha.qtd_dinamites += 1
                    self.explode(mapa, dinamites, dinamite)

    def atualiza(self, tempo_transcorrido, explosoes):
        self.tempo = self.tempo - tempo_transcorrido
        if self.tempo < 100:
            self.frame = 2
        elif self.tempo < 200:
            self.frame = 1

        if self.tempo < 1:
            explosoes.remove(self)

    def afeta_mapa(self, mapa):
        for posicao in self.espacos_afetados:
            mapa[posicao[0]][posicao[1]] = 0
