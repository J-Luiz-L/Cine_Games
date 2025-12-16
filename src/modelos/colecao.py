class Colecao:
    """
    Representa uma coleção nomeada de jogos.
    Ex: Favoritos, Co-op, Zerados 2025
    """

    def __init__(self, nome: str):
        self._nome = nome
        self._jogos = []

    @property
    def nome(self):
        return self._nome

    def adicionar(self, jogo):
        if jogo not in self._jogos:
            self._jogos.append(jogo)

    def remover(self, jogo):
        self._jogos = [j for j in self._jogos if j.id != jogo.id]

    def listar(self):
        return self._jogos
