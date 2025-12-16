from .jogo import Jogo
from typing import Optional, Dict, Any

class JogoConsole(Jogo):
    """
    Representa um jogo para consoles.

    Esta classe herda de `Jogo` e adiciona atributos específicos para jogos de console,
    como o nome do console em que o jogo pode ser jogado.

    Atributos:
        _console (str): Console compatível com o jogo (ex.: PlayStation, Xbox, Nintendo Switch).
    """

    def __init__(self, titulo: str, genero: str, console: str, **kwargs):
        """
        Inicializa um objeto JogoConsole.

        Args:
            titulo (str): Título do jogo.
            genero (str): Gênero do jogo.
            console (str): Console compatível com o jogo.
            **kwargs: Argumentos adicionais passados para a classe base `Jogo`.
        """
        super().__init__(titulo=titulo, genero=genero, plataforma=console, **kwargs)
        self._console = console

    @property
    def console(self) -> str:
        """
        Obtém o console do jogo.

        Returns:
            str: Nome do console compatível com o jogo.
        """
        return self._console

    @console.setter
    def console(self, novo: str) -> None:
        """
        Define o console do jogo.

        Args:
            novo (str): Novo console a ser definido.

        Raises:
            ValueError: Se o valor fornecido for vazio.
        """
        if not novo:
            raise ValueError("Console não pode ser vazio")
        self._console = novo

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto em um dicionário.

        Returns:
            Dict[str, Any]: Representação em dicionário do jogo, incluindo o console.
        """
        base = super().to_dict()
        base.update({"console": self._console})
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Cria um objeto JogoConsole a partir de um dicionário.

        Args:
            data (Dict[str, Any]): Dicionário contendo os dados do jogo.

        Returns:
            JogoConsole: Instância criada a partir dos dados fornecidos.
        """
        base = Jogo.from_dict(data)
        return cls(
            titulo=base.titulo,
            genero=base.genero,
            console=data.get("console", "Console Desconhecido"),
            status=base.status,
            horas_jogadas=base.horas_jogadas,
            avaliacao=base.avaliacao,
            data_inicio=base.data_inicio,
            data_fim=base.data_fim,
        )
