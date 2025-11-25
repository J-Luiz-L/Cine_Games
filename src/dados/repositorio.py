from pathlib import Path
import json
from typing import Any, Optional

def salvar_json(caminho: Path, dados: Any) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_json(caminho: Path) -> Optional[Any]:
    if not Path(caminho).exists():
        return None
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
