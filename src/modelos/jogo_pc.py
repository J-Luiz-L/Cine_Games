from .jogo import Jogo

from typing import Optional, Dict, Any



class JogoPC(Jogo):

    """Jogo específico para PC.



    Atributos adicionais (protegidos):

      - _requisitos

      - _loja

    """



    def __init__(self, titulo: str, genero: str, requisitos: str, loja: Optional[str] = None, **kwargs):

        super().__init__(titulo=titulo, genero=genero, plataforma="PC", **kwargs)

        self._requisitos = requisitos

        self._loja = loja



    @property

    def requisitos(self) -> str:

        return self._requisitos



    @requisitos.setter

    def requisitos(self, novo: str) -> None:

        if not novo:

            raise ValueError("Requisitos não pode ser vazio")

        self._requisitos = novo



    @property

    def loja(self) -> Optional[str]:

        return self._loja



    @loja.setter

    def loja(self, novo: Optional[str]) -> None:

        self._loja = novo



    def to_dict(self) -> Dict[str, Any]:

        base = super().to_dict()

        base.update({"requisitos": self._requisitos, "loja": self._loja})

        return base



    @classmethod

    def from_dict(cls, data: Dict[str, Any]):

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