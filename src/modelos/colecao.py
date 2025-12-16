from typing import List, Iterable
from .jogo import Jogo

class Colecao:
    """
    Representa uma coleção de jogos.

    Esta classe mantém uma lista interna protegida de jogos e fornece métodos
    para adicionar, remover, listar e buscar jogos de forma segura.

    Atributos:
        _nome (str): Nome da coleção.
        _jogos (List[Jogo]): Lista interna de jogos.
    """

    def __init__(self, nome: str):
        """
        Inicializa uma coleção de jogos.

        Args:
            nome (str): Nome da coleção.
        """
        self._nome = nome
        self._jogos: List[Jogo] = []

    @property
    def nome(self) -> str:
        """
        Obtém o nome da coleção.

        Returns:
            str: Nome da coleção.
        """
        return self._nome

    def adicionar_jogo(self, jogo: Jogo) -> None:
        """
        Adiciona um jogo à coleção.

        Args:
            jogo (Jogo): Instância de Jogo a ser adicionada.

        Raises:
            TypeError: Se o objeto fornecido não for uma instância de Jogo.
        """
        if not isinstance(jogo, Jogo):
            raise TypeError("Só é possível adicionar instâncias de Jogo")
        self._jogos.append(jogo)

    def remover_jogo(self, jogo: Jogo) -> None:
        """
        Remove um jogo da coleção.

        Args:
            jogo (Jogo): Instância de Jogo a ser removida.

        Raises:
            ValueError: Se o jogo não estiver presente na coleção.
        """
        self._jogos.remove(jogo)

    def listar_jogos(self) -> List[Jogo]:
        """
        Retorna todos os jogos da coleção.

        Returns:
            List[Jogo]: Lista com todos os jogos na coleção.
        """
        return list(self._jogos)

    def buscar_por_titulo(self, texto: str) -> List[Jogo]:
        """
        Busca jogos cujo título contenha o texto fornecido (case-insensitive).

        Args:
            texto (str): Texto a ser buscado no título dos jogos.

        Returns:
            List[Jogo]: Lista de jogos cujo título contém o texto.
        """
        texto = texto.lower()
        return [j for j in self._jogos if texto in j.titulo.lower()]

    def __len__(self) -> int:
        """
        Retorna a quantidade de jogos na coleção.

        Returns:
            int: Número de jogos na coleção.
        """
        return len(self._jogos)

    def __iter__(self) -> Iterable[Jogo]:
        """
        Retorna um iterador para percorrer os jogos da coleção.

        Returns:
            Iterable[Jogo]: Iterador dos jogos na coleção.
        """
        return iter(self._jogos)
