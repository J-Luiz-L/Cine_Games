import json
from collections import Counter
from typing import Dict, List

from src.modelos.jogo import Jogo
from src.modelos.colecao import Colecao


class CatalogoService:
    """
    Serviço responsável por gerenciar o catálogo de jogos.

    Centraliza todas as regras de negócio:
    - Cadastro e remoção de jogos
    - Controle de horas e status
    - Gerenciamento de coleções
    - Estatísticas do catálogo
    """

    def __init__(self):
        """Inicializa o serviço, carregando configurações e estruturas."""
        self.jogos: List[Jogo] = []
        self.colecoes: Dict[str, Colecao] = {}
        self.config = self._carregar_settings()

    # -------------------------------------------------
    # Configurações
    # -------------------------------------------------
    def _carregar_settings(self) -> dict:
        """
        Carrega as configurações do arquivo settings.json.

        Returns:
            dict: Configurações da aplicação.
        """
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "meta_anual_finalizados": 10,
                "limite_jogando": 3
            }

    # -------------------------------------------------
    # Jogos
    # -------------------------------------------------
    def adicionar_jogo(self, jogo: Jogo) -> None:
        """
        Adiciona um jogo ao catálogo após validações.

        Raises:
            ValueError: Se regras de negócio forem violadas.
        """
        # Duplicidade
        for j in self.jogos:
            if j.titulo.lower() == jogo.titulo.lower() and j.plataforma == jogo.plataforma:
                raise ValueError("Já existe um jogo com esse título nessa plataforma.")

        # Limite de jogos jogando
        if jogo.status == "Jogando":
            jogando = [j for j in self.jogos if j.status == "Jogando"]
            if len(jogando) >= self.config["limite_jogando"]:
                raise ValueError("Limite de jogos em andamento atingido.")

        self.jogos.append(jogo)

    def remover_jogo(self, jogo_id: str) -> None:
        """Remove um jogo do catálogo pelo ID."""
        self.jogos = [j for j in self.jogos if j.id != jogo_id]

    def atualizar_horas(self, jogo_id: str, novas_horas: float) -> None:
        """
        Atualiza as horas jogadas de forma progressiva.

        Raises:
            ValueError: Se valor for inválido.
        """
        jogo = self._buscar_por_id(jogo_id)
        if novas_horas < jogo.horas_jogadas:
            raise ValueError("Horas não podem ser reduzidas.")
        jogo.registrar_progresso(novas_horas - jogo.horas_jogadas)

    def _buscar_por_id(self, jogo_id: str) -> Jogo:
        """Busca um jogo pelo ID."""
        for jogo in self.jogos:
            if jogo.id == jogo_id:
                return jogo
        raise ValueError("Jogo não encontrado.")

    # -------------------------------------------------
    # Coleções
    # -------------------------------------------------
    def criar_colecao(self, nome: str) -> None:
        """
        Cria uma nova coleção.

        Raises:
            ValueError: Se a coleção já existir.
        """
        if nome in self.colecoes:
            raise ValueError("Coleção já existe.")
        self.colecoes[nome] = Colecao(nome)

    def adicionar_em_colecao(self, nome: str, jogo: Jogo) -> None:
        """Adiciona um jogo a uma coleção existente."""
        self.colecoes[nome].adicionar(jogo)

    def remover_de_colecao(self, nome: str, jogo: Jogo) -> None:
        """Remove um jogo de uma coleção."""
        self.colecoes[nome].remover(jogo)

    # -------------------------------------------------
    # Estatísticas
    # -------------------------------------------------
    def total_horas(self) -> float:
        """Retorna o total de horas jogadas."""
        return sum(j.horas_jogadas for j in self.jogos)

    def media_avaliacao(self) -> float:
        """Calcula a média de avaliações dos jogos finalizados."""
        notas = [j.avaliacao for j in self.jogos if j.avaliacao]
        return round(sum(notas) / len(notas), 2) if notas else 0.0

    def percentual_por_status(self) -> dict:
        """Calcula o percentual de jogos por status."""
        total = len(self.jogos)
        if total == 0:
            return {}

        return {
            status: round(len([j for j in self.jogos if j.status == status]) / total * 100, 2)
            for status in Jogo.STATUS_VALIDOS
        }

    def top_5_mais_jogados(self):
        """Retorna os 5 jogos com mais horas."""
        return sorted(self.jogos, key=lambda j: j.horas_jogadas, reverse=True)[:5]

    def genero_favorito(self):
        """Retorna o gênero mais jogado."""
        contagem = Counter(j.genero for j in self.jogos)
        return contagem.most_common(1)[0] if contagem else None

    def plataforma_principal(self):
        """Retorna a plataforma mais usada."""
        contagem = Counter(j.plataforma for j in self.jogos)
        return contagem.most_common(1)[0] if contagem else None

    def verificar_meta_finalizados(self) -> str:
        """Verifica se a meta anual de jogos finalizados foi atingida."""
        finalizados = len([j for j in self.jogos if j.status == "Finalizado"])
        meta = self.config["meta_anual_finalizados"]

        if finalizados < meta:
            return f"⚠️ Você finalizou {finalizados}/{meta} jogos este ano."
        return "✅ Meta anual de jogos finalizados atingida!"
