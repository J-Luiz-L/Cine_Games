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



    def adicionar_jogo(self, jogo: Jogo) -> None:

        if not isinstance(jogo, Jogo):

            raise TypeError("Só é possível adicionar instâncias de Jogo")

        self._jogos.append(jogo)



    def remover_jogo(self, jogo: Jogo) -> None:

        self._jogos.remove(jogo)



    def listar_jogos(self) -> List[Jogo]:


        return list(self._jogos)



    def buscar_por_titulo(self, texto: str) -> List[Jogo]:

        texto = texto.lower()

        return [j for j in self._jogos if texto in j.titulo.lower()]



    def __len__(self) -> int:

        return len(self._jogos)



    def __iter__(self) -> Iterable[Jogo]:

        return iter(self._jogos)

