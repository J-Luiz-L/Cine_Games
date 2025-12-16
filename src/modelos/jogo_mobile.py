from .jogo import Jogo
from typing import Optional, Dict, Any

class JogoMobile(Jogo):
    """
    Representa um jogo para dispositivos móveis (mobile).

    Esta classe herda de `Jogo` e adiciona atributos específicos para jogos mobile,
    como o sistema operacional do dispositivo.

    Atributos:
        _sistema_operacional (str): Sistema operacional em que o jogo pode ser jogado.
    """

    def __init__(self, titulo: str, genero: str, sistema_operacional: str, **kwargs):
        """
        Inicializa um objeto JogoMobile.

        Args:
            titulo (str): Título do jogo.
            genero (str): Gênero do jogo.
            sistema_operacional (str): Sistema operacional compatível com o jogo (ex.: iOS, Android).
            **kwargs: Argumentos adicionais passados para a classe base `Jogo`.
        """
        super().__init__(titulo=titulo, genero=genero, plataforma=sistema_operacional, **kwargs)
        self._sistema_operacional = sistema_operacional

    @property
    def sistema_operacional(self) -> str:
        """
        Obtém o sistema operacional do jogo.

        Returns:
            str: Sistema operacional compatível.
        """
        return self._sistema_operacional

    @sistema_operacional.setter
    def sistema_operacional(self, novo: str) -> None:
        """
        Define o sistema operacional do jogo.

        Args:
            novo (str): Novo sistema operacional a ser definido.

        Raises:
            ValueError: Se o valor fornecido for vazio.
        """
        if not novo:
            raise ValueError("Sistema operacional não pode ser vazio")
        self._sistema_operacional = novo

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto em um dicionário.

        Returns:
            Dict[str, Any]: Representação em dicionário do jogo, incluindo o sistema operacional.
        """
        base = super().to_dict()
        base.update({"sistema_operacional": self._sistema_operacional})
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Cria um objeto JogoMobile a partir de um dicionário.

        Args:
            data (Dict[str, Any]): Dicionário contendo os dados do jogo.

        Returns:
            JogoMobile: Instância criada a partir dos dados fornecidos.
        """
        base = Jogo.from_dict(data)
        return cls(
            titulo=base.titulo,
            genero=base.genero,
            sistema_operacional=data.get("sistema_operacional", "Desconhecido"),
            status=base.status,
            horas_jogadas=base.horas_jogadas,
            avaliacao=base.avaliacao,
            data_inicio=base.data_inicio,
            data_fim=base.data_fim,
        )
