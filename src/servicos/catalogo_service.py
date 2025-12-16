import json
from collections import Counter
from src.modelos.jogo import Jogo
from src.modelos.colecao import Colecao


class CatalogoService:
    """
    Serviço responsável por gerenciar o catálogo de jogos.
    Contém todas as regras de negócio.
    """

    def __init__(self):
        self.jogos = []
        self.colecoes = {}
        self.config = self._carregar_settings()

    # -----------------------------
    # Configurações
    # -----------------------------
    def _carregar_settings(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "meta_anual_finalizados": 10,
                "limite_jogando": 3
            }

    # -----------------------------
    # Catálogo
    # -----------------------------
    def adicionar_jogo(self, jogo: Jogo):
        # Duplicidade
        for j in self.jogos:
            if j.titulo.lower() == jogo.titulo.lower() and j.plataforma == jogo.plataforma:
                raise ValueError("Já existe um jogo com esse título nessa plataforma.")

        # Limite de jogos jogando
        if jogo.status == "Jogando":
            jogando = [j for j in self.jogos if j.status == "Jogando"]
            if len(jogando) >= self.config["limite_jogando"]:
                raise ValueError("Limite de jogos jogando atingido.")

        # Validação de status finalizado
        if jogo.status == "Finalizado" and jogo.horas_jogadas < 1:
            raise ValueError("Não é possível adicionar um jogo finalizado com menos de 1 hora jogada.")

        # Adiciona o jogo
        self.jogos.append(jogo)

    def remover_jogo(self, jogo_id: str):
        self.jogos = [j for j in self.jogos if j.id != jogo_id]

    def listar_jogos(self):
        return self.jogos

    def buscar_por_titulo(self, termo: str):
        termo = termo.lower()
        return [j for j in self.jogos if termo in j.titulo.lower()]

    def ordenar(self, criterio: str, reverso: bool = True):
        if criterio == "horas":
            return sorted(self.jogos, key=lambda j: j.horas_jogadas, reverse=reverso)
        if criterio == "avaliacao":
            return sorted(self.jogos, key=lambda j: j.avaliacao or 0, reverse=reverso)
        if criterio == "ano":
            return sorted(
                self.jogos,
                key=lambda j: j.data_inicio.year if j.data_inicio else 0,
                reverse=reverso
            )
        return self.jogos

    # -----------------------------
    # Coleções
    # -----------------------------
    def criar_colecao(self, nome: str):
        if nome in self.colecoes:
            raise ValueError("Coleção já existe.")
        self.colecoes[nome] = Colecao(nome)

    def adicionar_em_colecao(self, nome_colecao: str, jogo: Jogo):
        self.colecoes[nome_colecao].adicionar(jogo)

    def listar_colecao(self, nome_colecao: str):
        return self.colecoes[nome_colecao].listar()

    # -----------------------------
    # Estatísticas
    # -----------------------------
    def total_horas(self) -> float:
        return sum(j.horas_jogadas for j in self.jogos)

    def media_avaliacao(self) -> float:
        notas = [j.avaliacao for j in self.jogos if j.status == "Finalizado" and j.avaliacao]
        return round(sum(notas) / len(notas), 2) if notas else 0.0

    def percentual_por_status(self):
        total = len(self.jogos)
        if total == 0:
            return {}

        resultado = {}
        for status in Jogo.STATUS_VALIDOS:
            qtd = len([j for j in self.jogos if j.status == status])
            resultado[status] = round((qtd / total) * 100, 2)

        return resultado

    def top_5_mais_jogados(self):
        return sorted(self.jogos, key=lambda j: j.horas_jogadas, reverse=True)[:5]

    def genero_favorito(self):
        contagem = Counter(j.genero for j in self.jogos)
        return contagem.most_common(1)[0] if contagem else None

    def plataforma_principal(self):
        contagem = Counter(j.plataforma for j in self.jogos)
        return contagem.most_common(1)[0] if contagem else None

    def verificar_meta_finalizados(self):
        finalizados = len([j for j in self.jogos if j.status == "Finalizado"])
        meta = self.config["meta_anual_finalizados"]

        if finalizados < meta:
            return f"⚠️ Você finalizou {finalizados}/{meta} jogos este ano!"
        return "Meta anual atingida!"
