import json
import uuid

class CatalogoService:
    def __init__(self):
        self.jogos = []
        self.config = self._carregar_settings()

    # -----------------------------
    # ⚙️ Carrega configurações
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
    # 🛠️ Normaliza status
    # -----------------------------
    def _normalize_status(self, raw_status: str) -> str:
        if not raw_status:
            return "Não iniciado"

        s = raw_status.strip().lower()

        if "final" in s:
            return "Finalizado"
        if "jog" in s:
            return "Jogando"
        if "paus" in s:
            return "Pausado"
        if "não" in s or "nao" in s:
            return "Não iniciado"
        if "iniciado" in s:
            return "Não iniciado"

        return "Não iniciado"

    # -----------------------------
    # ➕ Adicionar Jogo
    # -----------------------------
    def adicionar_jogo(self, jogo):

        # Normaliza o status e aplica via API do modelo
        try:
            canonical = self._normalize_status(getattr(jogo, "status", ""))
            jogo.alterar_status(canonical)
        except Exception as e:
            raise ValueError(f"Status inválido: {e}")

        # 1 — Verificar duplicação
        for j in self.jogos:
            if j.titulo.lower() == jogo.titulo.lower() and j.plataforma.lower() == jogo.plataforma.lower():
                raise ValueError("Já existe um jogo com esse título na mesma plataforma.")

        # 2 — Horas jogadas não podem ser negativas
        if jogo.horas_jogadas < 0:
            raise ValueError("Horas jogadas não podem ser negativas.")

        # 3 — Limite de jogos com status Jogando
        limite = self.config.get("limite_jogando", 3)
        if jogo.status == "Jogando":
            jogando = [j for j in self.jogos if j.status == "Jogando"]
            if len(jogando) >= limite:
                raise ValueError(f"Você já possui {limite} jogos em andamento.")

        # 4 — Regras para avaliação
        if jogo.status != "Finalizado":
            jogo._avaliacao = None
        else:
            if jogo.avaliacao is None or not (0 <= int(jogo.avaliacao) <= 10):
                raise ValueError("Jogos finalizados devem ter avaliação entre 0 e 10.")

        # 5 — Adicionar ao catálogo
        self.jogos.append(jogo)

    # -----------------------------
    # 🗑️ Remover Jogo
    # -----------------------------
    def remover_jogo(self, jogo_id):
        self.jogos = [j for j in self.jogos if j.id != jogo_id]

    # -----------------------------
    # 📋 Listar Jogos
    # -----------------------------
    def listar_jogos(self):
        return self.jogos

    # -----------------------------
    # ⏫ Atualizar horas jogadas
    # -----------------------------
    def atualizar_horas(self, jogo_id, novas_horas):
        for j in self.jogos:
            if j.id == jogo_id:
                if novas_horas < j.horas_jogadas:
                    raise ValueError("Horas jogadas não podem diminuir.")
                j.horas_jogadas = novas_horas
                return
        raise ValueError("Jogo não encontrado.")

    # -----------------------------
    # 📊 Conferir meta anual
    # -----------------------------
    def verificar_meta_finalizados(self):
        finalizados = len([j for j in self.jogos if j.status == "Finalizado"])
        meta = self.config["meta_anual_finalizados"]

        if finalizados < meta:
            return f"⚠️ Você finalizou {finalizados}/{meta} jogos este ano!"
        return "Meta anual atingida!"
