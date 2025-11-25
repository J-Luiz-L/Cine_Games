from typing import Optional, Dict, Any
from .jogo import Jogo

class JogoMobile(Jogo):
    def __init__(self, titulo: str, genero: str, sistema_operacional: str, **kwargs):
        super().__init__(titulo=titulo, genero=genero, plataforma=sistema_operacional, **kwargs)
        self._sistema_operacional = sistema_operacional

    @property
    def sistema_operacional(self) -> str:
        return self._sistema_operacional

    @sistema_operacional.setter
    def sistema_operacional(self, novo: str) -> None:
        if not novo:
            raise ValueError("Sistema operacional não pode ser vazio")
        self._sistema_operacional = novo

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({"sistema_operacional": self._sistema_operacional})
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
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
