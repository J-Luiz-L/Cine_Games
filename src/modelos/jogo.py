from datetime import datetime
from typing import Optional, Dict, Any
import uuid


class Jogo:
    """
    Classe base que representa um jogo genérico no catálogo.

    Esta classe define os atributos e comportamentos comuns
    a todos os tipos de jogos (PC, Console e Mobile),
    utilizando encapsulamento forte e validações básicas.

    Cada jogo possui um identificador único (id) que é gerado
    automaticamente e não pode ser alterado.
    """

    STATUS_VALIDOS = ("Não iniciado", "Jogando", "Pausado", "Finalizado")

    def __init__(
        self,
        titulo: str,
        genero: str,
        plataforma: str = "Genérica",
        status: str = "Não iniciado",
        horas_jogadas: float = 0.0,
        avaliacao: Optional[int] = None,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None,
        id: Optional[str] = None,
    ):
        """
        Inicializa um objeto Jogo.

        Args:
            titulo (str): Título do jogo.
            genero (str): Gênero do jogo.
            plataforma (str): Plataforma do jogo (PC, Console, Mobile).
            status (str): Status atual do jogo.
            horas_jogadas (float): Total de horas jogadas.
            avaliacao (int | None): Avaliação do jogo (1 a 10).
            data_inicio (datetime | None): Data de início do jogo.
            data_fim (datetime | None): Data de finalização do jogo.
            id (str | None): Identificador único do jogo.
        """
        self._id = id or str(uuid.uuid4())
        self._titulo = titulo
        self._genero = genero
        self._plataforma = plataforma
        self._status = status
        self._horas_jogadas = float(horas_jogadas)
        self._avaliacao = None
        self._data_inicio = data_inicio
        self._data_fim = data_fim

        if avaliacao is not None:
            self.avaliacao = avaliacao

    # -----------------------------
    # Propriedades
    # -----------------------------
    @property
    def id(self) -> str:
        """
        Retorna o identificador único do jogo.

        O ID é somente leitura e não pode ser alterado.
        """
        return self._id

    @property
    def titulo(self) -> str:
        """Retorna o título do jogo."""
        return self._titulo

    @titulo.setter
    def titulo(self, novo: str) -> None:
        """
        Define um novo título para o jogo.

        Raises:
            ValueError: Se o título for vazio.
        """
        if not novo:
            raise ValueError("Título não pode ser vazio")
        self._titulo = novo

    @property
    def genero(self) -> str:
        """Retorna o gênero do jogo."""
        return self._genero

    @genero.setter
    def genero(self, novo: str) -> None:
        """
        Define um novo gênero para o jogo.

        Raises:
            ValueError: Se o gênero for vazio.
        """
        if not novo:
            raise ValueError("Gênero não pode ser vazio")
        self._genero = novo

    @property
    def plataforma(self) -> str:
        """Retorna a plataforma do jogo."""
        return self._plataforma

    @plataforma.setter
    def plataforma(self, novo: str) -> None:
        """
        Define a plataforma do jogo.

        Raises:
            ValueError: Se a plataforma for vazia.
        """
        if not novo:
            raise ValueError("Plataforma não pode ser vazia")
        self._plataforma = novo

    @property
    def status(self) -> str:
        """Retorna o status atual do jogo."""
        return self._status

    def alterar_status(self, novo_status: str) -> None:
        """
        Altera o status do jogo.

        Args:
            novo_status (str): Novo status do jogo.

        Raises:
            ValueError: Se o status não estiver entre os valores permitidos.
        """
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: {novo_status}")
        self._status = novo_status

    @property
    def horas_jogadas(self) -> float:
        """Retorna o total de horas jogadas."""
        return self._horas_jogadas

    def registrar_progresso(self, horas: float) -> None:
        """
        Registra novas horas jogadas no jogo.

        As horas são acumuladas progressivamente.

        Args:
            horas (float): Quantidade de horas a adicionar.

        Raises:
            ValueError: Se o valor for negativo.
        """
        horas = float(horas)
        if horas < 0:
            raise ValueError("Horas não podem ser negativas")
        self._horas_jogadas += horas

    @property
    def avaliacao(self) -> Optional[int]:
        """Retorna a avaliação do jogo."""
        return self._avaliacao

    @avaliacao.setter
    def avaliacao(self, nota: Optional[int]) -> None:
        """
        Define a avaliação do jogo.

        Args:
            nota (int | None): Nota entre 1 e 10 ou None.

        Raises:
            ValueError: Se a nota não estiver entre 1 e 10.
        """
        if nota is None:
            self._avaliacao = None
            return
        if not (1 <= int(nota) <= 10):
            raise ValueError("Avaliação deve ser inteiro entre 1 e 10")
        self._avaliacao = int(nota)

    @property
    def data_inicio(self) -> Optional[datetime]:
        """Retorna a data de início do jogo."""
        return self._data_inicio

    @data_inicio.setter
    def data_inicio(self, d: Optional[datetime]) -> None:
        """Define a data de início do jogo."""
        self._data_inicio = d

    @property
    def data_fim(self) -> Optional[datetime]:
        """Retorna a data de finalização do jogo."""
        return self._data_fim

    @data_fim.setter
    def data_fim(self, d: Optional[datetime]) -> None:
        """Define a data de finalização do jogo."""
        self._data_fim = d

    # -----------------------------
    # Serialização
    # -----------------------------
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto Jogo para um dicionário.

        Returns:
            dict: Representação serializável do jogo.
        """
        return {
            "id": self._id,
            "titulo": self._titulo,
            "genero": self._genero,
            "plataforma": self._plataforma,
            "status": self._status,
            "horas_jogadas": self._horas_jogadas,
            "avaliacao": self._avaliacao,
            "data_inicio": self._data_inicio.isoformat() if self._data_inicio else None,
            "data_fim": self._data_fim.isoformat() if self._data_fim else None,
            "tipo": self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Cria um objeto Jogo a partir de um dicionário.

        Args:
            data (dict): Dicionário com os dados do jogo.

        Returns:
            Jogo: Instância da classe Jogo.
        """
        di = data.get("data_inicio")
        df = data.get("data_fim")
        data_inicio = datetime.fromisoformat(di) if di else None
        data_fim = datetime.fromisoformat(df) if df else None

        return cls(
            titulo=data["titulo"],
            genero=data["genero"],
            plataforma=data.get("plataforma", "Genérica"),
            status=data.get("status", "Não iniciado"),
            horas_jogadas=data.get("horas_jogadas", 0.0),
            avaliacao=data.get("avaliacao"),
            data_inicio=data_inicio,
            data_fim=data_fim,
            id=data.get("id"),
        )

    def __repr__(self) -> str:
        """
        Retorna a representação textual do objeto para depuração.
        """
        return (
            f"<{self.__class__.__name__} id={self._id} titulo={self._titulo!r} "
            f"genero={self._genero!r} plataforma={self._plataforma!r} "
            f"horas={self._horas_jogadas} status={self._status!r}>"
        )
    
    def alterar_status(self, novo_status: str) -> None:
        """
        Altera o status do jogo respeitando regras de negócio.
        """
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: {novo_status}")

        if novo_status == "Finalizado" and self._horas_jogadas < 1:
            raise ValueError("Não é possível finalizar um jogo com menos de 1h jogada.")

        self._status = novo_status

    def reiniciar(self) -> None:
        """
        Reinicia o jogo, voltando para 'Jogando' e zerando horas.
        """
        self._status = "Jogando"
        self._horas_jogadas = 0.0
        self._avaliacao = None
        self._data_inicio = None
        self._data_fim = None

