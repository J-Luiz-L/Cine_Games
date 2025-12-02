# src/dados/repositorio.py

from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from src.modelos.jogo import Jogo
from src.modelos.jogo_pc import JogoPC
from src.modelos.jogo_console import JogoConsole
from src.modelos.jogo_mobile import JogoMobile


# --- Funções utilitárias JSON ---
def salvar_json(caminho: Path, dados: Any) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_json(caminho: Path) -> Optional[Any]:
    if not Path(caminho).exists():
        return None
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


class RepositorioJogos:
    """Gerencia persistência de objetos Jogo em JSON."""

    def __init__(self, caminho: Path):
        self._caminho = caminho

    # ----------------------------
    # CARREGAR
    # ----------------------------
    def carregar(self) -> List[Jogo]:
        dados_raw = carregar_json(self._caminho)
        if dados_raw is None:
            return []
        return [self._deserialize_jogo(d) for d in dados_raw]

    # ----------------------------
    # SALVAR
    # ----------------------------
    def salvar(self, jogos: List[Jogo]) -> None:
        dados_raw = [j.to_dict() for j in jogos]
        salvar_json(self._caminho, dados_raw)

    # ----------------------------
    # REMOVER POR ID
    # ----------------------------
    def remover(self, jogo_id: str) -> None:
        jogos = self.carregar()
        jogos = [j for j in jogos if j.id != jogo_id]
        self.salvar(jogos)

    # ----------------------------
    # DESERIALIZAÇÃO DINÂMICA
    # ----------------------------
    def _deserialize_jogo(self, data: Dict[str, Any]) -> Jogo:
        tipo = data.get("tipo", "Jogo")
        if tipo == "JogoPC":
            return JogoPC.from_dict(data)
        if tipo == "JogoConsole":
            return JogoConsole.from_dict(data)
        if tipo == "JogoMobile":
            return JogoMobile.from_dict(data)
        return Jogo.from_dict(data)
