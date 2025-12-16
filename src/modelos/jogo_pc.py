from .jogo import Jogo
from typing import Optional, Dict, Any

class JogoPC(Jogo):
    """
    Representa um jogo específico para PC.

    Esta classe herda de `Jogo` e adiciona atributos específicos para jogos de PC,
    como requisitos de sistema e loja de aquisição.

    Atributos:
        _requisitos (str): Requisitos mínimos ou recomendados do PC para rodar o jogo.
        _loja (Optional[str]): Loja ou plataforma digital onde o jogo pode ser adquirido.
    """

    def __init__(self, titulo: str, genero: str, requisitos: str, loja: Optional[str] = None, **kwargs):
        """
        Inicializa um objeto JogoPC.

        Args:
            titulo (str): Título do jogo.
            genero (str): Gênero do jogo.
            requisitos (str): Requisitos mínimos ou recomendados do PC.
            loja (Optional[str], opcional): Loja ou plataforma onde o jogo está disponível. Padrão é None.
            **kwargs: Argumentos adicionais passados para a classe base `Jogo`.
        """
        super().__init__(titulo=titulo, genero=genero, plataforma="PC", **kwargs)
        self._requisitos = requisitos
        self._loja = loja

    @property
    def requisitos(self) -> str:
        """
        Obtém os requisitos do jogo para PC.

        Returns:
            str: Requisitos mínimos ou recomendados do PC.
        """
        return self._requisitos

    @requisitos.setter
    def requisitos(self, novo: str) -> None:
        """
        Define os requisitos do jogo para PC.

        Args:
            novo (str): Novos requisitos a serem definidos.

        Raises:
            ValueError: Se o valor fornecido for vazio.
        """
        if not novo:
            raise ValueError("Requisitos não pode ser vazio")
        self._requisitos = novo

    @property
    def loja(self) -> Optional[str]:
        """
        Obtém a loja do jogo.

        Returns:
            Optional[str]: Nome da loja ou None se não especificado.
        """
        return self._loja

    @loja.setter
    def loja(self, novo: Optional[str]) -> None:
        """
        Define a loja do jogo.

        Args:
            novo (Optional[str]): Nova loja a ser definida.
        """
        self._loja = novo

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto em um dicionário.

        Returns:
            Dict[str, Any]: Representação em dicionário do jogo, incluindo atributos específicos de PC.
        """
        base = super().to_dict()
        base.update({"requisitos": self._requisitos, "loja": self._loja})
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Cria um objeto JogoPC a partir de um dicionário.

        Args:
            data (Dict[str, Any]): Dicionário contendo os dados do jogo.

        Returns:
            JogoPC: Instância criada a partir dos dados fornecidos.
        """
        base = Jogo.from_dict(data)
        return cls(
            titulo=base.titulo,
            genero=base.genero,
            requisitos=data.get("requisitos", ""),
            loja=data.get("loja"),
            status=base.status,
            horas_jogadas=base.horas_jogadas,
            avaliacao=base.avaliacao,
            data_inicio=base.data_inicio,
            data_fim=base.data_fim,
        )
