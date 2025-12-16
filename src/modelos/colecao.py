from typing import List, Iterable
from .jogo import Jogo

class Colecao:
    """Coleção de jogos. Mantém a lista interna protegida e expõe métodos seguros."""

    def __init__(self, nome: str):
        self._nome = nome
        self._jogos: List[Jogo] = []

    @property
    def nome(self) -> str:
        return self._nome

    def adicionar(self, jogo: Jogo):
        if jogo not in self._jogos:
            self._jogos.append(jogo)

    def remover(self, jogo: Jogo):
        if jogo in self._jogos:
            self._jogos.remove(jogo)

    def listar(self) -> List[Jogo]:
        return list(self._jogos)

    # ----------------- MÉTODOS DE PERSISTÊNCIA -----------------
    def to_dict(self):
        """Converte a coleção em um dicionário JSON-serializável"""
        return {
            "nome": self.nome,
            "jogos_ids": [j.id for j in self._jogos]
        }

    @classmethod
    def from_dict(cls, d):
        """Cria uma coleção a partir de um dicionário JSON"""
        colecao = cls(d["nome"])
        # Armazenamos os IDs dos jogos para depois ligar aos objetos reais
        colecao._jogos_ids = d.get("jogos_ids", [])
        return colecao
