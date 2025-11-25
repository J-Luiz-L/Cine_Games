from typing import Optional, Dict, Any
from .jogo import Jogo

class JogoConsole(Jogo):
    def __init__(self, titulo: str, genero: str, console: str, **kwargs):
        super().__init__(titulo=titulo, genero=genero, plataforma=console, **kwargs)
        self._console = console

    @property
    def console(self) -> str:
        return self._console

    @console.setter
    def console(self, novo: str) -> None:
        if not novo:
            raise ValueError("Console não pode ser vazio")
        self._console = novo

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({"console": self._console})
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
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
