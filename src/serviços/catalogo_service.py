import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..modelos.jogo import Jogo
from ..modelos.jogo_pc import JogoPC
from ..modelos.jogo_console import JogoConsole
from ..modelos.jogo_mobile import JogoMobile

DEFAULT_DB = Path(__file__).parent.parent.parent / "data" / "catalogo.json"

class CatalogoService:
    def __init__(self, caminho: Optional[Path] = None):
        self._caminho = Path(caminho) if caminho else DEFAULT_DB
        self._jogos: List[Jogo] = []

    def adicionar(self, jogo: Jogo) -> None:
        if not isinstance(jogo, Jogo):
            raise TypeError("Só é possível adicionar instâncias de Jogo")
        self._jogos.append(jogo)

    def remover(self, jogo: Jogo) -> None:
        self._jogos.remove(jogo)

    def listar(self) -> List[Jogo]:
        return list(self._jogos)

    def buscar_por_titulo(self, texto: str) -> List[Jogo]:
        texto = texto.lower()
        return [j for j in self._jogos if texto in j.titulo.lower()]

    def salvar(self) -> None:
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        raw = [self._serialize_jogo(j) for j in self._jogos]
        with open(self._caminho, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)

    def carregar(self) -> None:
        if not self._caminho.exists():
            self._jogos = []
            return
        with open(self._caminho, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self._jogos = [self._deserialize_jogo(d) for d in raw]

    def _serialize_jogo(self, jogo: Jogo) -> Dict[str, Any]:
        return jogo.to_dict()

    def _deserialize_jogo(self, data: Dict[str, Any]) -> Jogo:
        tipo = data.get("tipo", "Jogo")
        if tipo == "JogoPC":
            return JogoPC.from_dict(data)
        if tipo == "JogoConsole":
            return JogoConsole.from_dict(data)
        if tipo == "JogoMobile":
            return JogoMobile.from_dict(data)
        return Jogo.from_dict(data)
