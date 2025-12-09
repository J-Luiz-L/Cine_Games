# src/modelos/jogo.py
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

class Jogo:
    """Classe base para jogos com encapsulamento forte.
       Agora com identificador único (id) para operações de edição/remoção.
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

    # id é somente leitura
    @property
    def id(self) -> str:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, novo: str) -> None:
        if not novo:
            raise ValueError("Título não pode ser vazio")
        self._titulo = novo

    @property
    def genero(self) -> str:
        return self._genero

    @genero.setter
    def genero(self, novo: str) -> None:
        if not novo:
            raise ValueError("Gênero não pode ser vazio")
        self._genero = novo

    @property
    def plataforma(self) -> str:
        return self._plataforma

    @plataforma.setter
    def plataforma(self, novo: str) -> None:
        if not novo:
            raise ValueError("Plataforma não pode ser vazia")
        self._plataforma = novo

    @property
    def status(self) -> str:
        return self._status

    def alterar_status(self, novo_status: str) -> None:
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: {novo_status}")
        self._status = novo_status

    @property
    def horas_jogadas(self) -> float:
        return self._horas_jogadas

    def registrar_progresso(self, horas: float) -> None:
        horas = float(horas)
        if horas < 0:
            raise ValueError("Horas não podem ser negativas")
        self._horas_jogadas += horas

    @property
    def avaliacao(self) -> Optional[int]:
        return self._avaliacao

    @avaliacao.setter
    def avaliacao(self, nota: Optional[int]) -> None:
    # Se o jogo NÃO está finalizado → avaliação deve ser None ou 0
        if self._status != "Finalizado":
            if nota not in (None, 0):
                raise ValueError("Somente jogos finalizados podem receber avaliação.")
            self._avaliacao = None
            return

    # Se está finalizado → nota obrigatória entre 1 e 10
        if nota is None:
         raise ValueError("Avaliação deve ser informada para jogos finalizados.")

        if not (1 <= int(nota) <= 10):
             raise ValueError("Avaliação deve ser um inteiro entre 1 e 10 para jogos finalizados.")

        self._avaliacao = int(nota)

    @property
    def data_inicio(self) -> Optional[datetime]:
        return self._data_inicio

    @data_inicio.setter
    def data_inicio(self, d: Optional[datetime]) -> None:
        self._data_inicio = d

    @property
    def data_fim(self) -> Optional[datetime]:
        return self._data_fim

    @data_fim.setter
    def data_fim(self, d: Optional[datetime]) -> None:
        self._data_fim = d

    # serialização
    def to_dict(self) -> Dict[str, Any]:
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
        return (
            f"<{self.__class__.__name__} id={self._id} titulo={self._titulo!r} genero={self._genero!r} "
            f"plataforma={self._plataforma!r} horas={self._horas_jogadas} status={self._status!r}>"
        )
