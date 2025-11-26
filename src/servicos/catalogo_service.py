import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from src.modelos.jogo import Jogo
from src.modelos.jogo_pc import JogoPC
from src.modelos.jogo_console import JogoConsole
from src.modelos.jogo_mobile import JogoMobile
from src.dados.repositorio import RepositorioJogos 

DEFAULT_DB = Path(__file__).parent.parent.parent / "data" / "catalogo.json"

class CatalogoService:
    def __init__(self, caminho: Optional[Path] = None):
        db_path = Path(caminho) if caminho else DEFAULT_DB
        self._repositorio = RepositorioJogos(caminho=db_path)
        self._jogos: List[Jogo] = []

    def carregar(self) -> None:
        self._jogos = self._repositorio.carregar()

    def salvar(self) -> None:
        self._repositorio.salvar(self._jogos)

    def adicionar(self, jogo: Jogo) -> None:
        if not isinstance(jogo, Jogo):
            raise TypeError("Só é possível adicionar instâncias de Jogo")
        if self.buscar_por_titulo(jogo.titulo, plataforma=jogo.plataforma):
            raise ValueError(f"O jogo '{jogo.titulo}' na plataforma '{jogo.plataforma}' já está cadastrado.")
        
        self._jogos.append(jogo)

    def remover(self, jogo: Jogo) -> None:
        self._jogos.remove(jogo)

    def listar(self) -> List[Jogo]:
        return list(self._jogos)

    def buscar_por_titulo(self, texto: str, plataforma: Optional[str] = None) -> List[Jogo]:
        texto = texto.lower()
        
        resultados = [j for j in self._jogos if texto in j.titulo.lower()]
        
        if plataforma:
            resultados = [j for j in resultados if j.plataforma.lower() == plataforma.lower()]

        return resultados
    
    def gerar_relatorio_inicial(self) -> Dict[str, Any]:
        """Gera o relatório inicial: total de jogos e horas jogadas."""
        
        total_jogos = len(self._jogos)
        total_horas = sum(j.horas_jogadas for j in self._jogos)
        
        return {
            "total_jogos": total_jogos,
            "total_horas_jogadas": total_horas,
        }