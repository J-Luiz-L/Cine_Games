import json
import uuid


class CatalogoService:
    """
    Serviço responsável por gerenciar o catálogo de jogos.

    Esta classe concentra todas as regras de negócio do sistema,
    como validações, limites, cadastro, remoção e atualização
    dos jogos cadastrados.
    """

    def __init__(self):
        """
        Inicializa o serviço de catálogo.

        Atributos:
            jogos (list): Lista de jogos cadastrados no catálogo.
            config (dict): Configurações carregadas do arquivo settings.json
                           ou valores padrão.
        """
        self.jogos = []
        self.config = self._carregar_settings()

    # -----------------------------
    #  Carrega configurações
    # -----------------------------
    def _carregar_settings(self):
        """
        Carrega as configurações do sistema a partir do arquivo settings.json.

        Returns:
            dict: Dicionário contendo as configurações do sistema, como:
                  - meta_anual_finalizados
                  - limite_jogando

        Caso o arquivo não exista, retorna valores padrão.
        """
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "meta_anual_finalizados": 10,
                "limite_jogando": 3
            }

    # -----------------------------
    #  Normaliza status
    # -----------------------------
    def _normalize_status(self, raw_status: str) -> str:
        """
        Normaliza o texto do status recebido para um valor padrão do sistema.

        Args:
            raw_status (str): Status informado pelo usuário ou interface.

        Returns:
            str: Status normalizado, podendo ser:
                 - "Jogando"
                 - "Finalizado"
                 - "Pausado"
                 - "Não iniciado"
        """
        if not raw_status:
            return "Não iniciado"

        s = raw_status.strip().lower()

        if "final" in s:
            return "Finalizado"
        if "jog" in s:
            return "Jogando"
        if "paus" in s:
            return "Pausado"
        if "não" in s or "nao" in s or "iniciado" in s:
            return "Não iniciado"

        return "Não iniciado"

    # -----------------------------
    #  Adicionar Jogos
    # -----------------------------
    def adicionar_jogo(self, jogo):
        """
        Adiciona um novo jogo ao catálogo, aplicando todas as regras de negócio.

        Regras aplicadas:
            - Não permite jogos duplicados (título + plataforma)
            - Horas jogadas não podem ser negativas
            - Limita quantidade de jogos com status "Jogando"
            - Avaliação só é permitida para jogos finalizados

        Args:
            jogo (Jogo): Instância de um jogo (PC, Console ou Mobile).

        Raises:
            ValueError: Caso alguma regra de negócio seja violada.
        """

        # Normaliza e aplica o status via método do modelo
        try:
            canonical = self._normalize_status(getattr(jogo, "status", ""))
            jogo.alterar_status(canonical)
        except Exception as e:
            raise ValueError(f"Status inválido: {e}")

        #  Verificar duplicação
        for j in self.jogos:
            if j.titulo.lower() == jogo.titulo.lower() and j.plataforma.lower() == jogo.plataforma.lower():
                raise ValueError("Já existe um jogo com esse título na mesma plataforma.")

        #  Horas jogadas não podem ser negativas
        if jogo.horas_jogadas < 0:
            raise ValueError("Horas jogadas não podem ser negativas.")

        #  Limite de jogos com status "Jogando"
        limite = self.config.get("limite_jogando", 3)
        if jogo.status == "Jogando":
            jogando = [j for j in self.jogos if j.status == "Jogando"]
            if len(jogando) >= limite:
                raise ValueError(f"Você já possui {limite} jogos em andamento.")

        #  Regras para avaliação
        if jogo.status != "Finalizado":
            jogo._avaliacao = None
        else:
            if jogo.avaliacao is None or not (0 <= int(jogo.avaliacao) <= 10):
                raise ValueError("Jogos finalizados devem ter avaliação entre 0 e 10.")

        #  Adiciona ao catálogo
        self.jogos.append(jogo)

    # -----------------------------
    #  Remover Jogo
    # -----------------------------
    def remover_jogo(self, jogo_id):
        """
        Remove um jogo do catálogo pelo seu ID.

        Args:
            jogo_id (str): Identificador único do jogo.
        """
        self.jogos = [j for j in self.jogos if j.id != jogo_id]

    # -----------------------------
    #  Listar os Jogos
    # -----------------------------
    def listar_jogos(self):
        """
        Retorna a lista completa de jogos cadastrados.

        Returns:
            list: Lista de objetos do tipo Jogo.
        """
        return self.jogos

    # -----------------------------
    #  Atualizar as horas jogadas
    # -----------------------------
    def atualizar_horas(self, jogo_id, novas_horas):
        """
        Atualiza a quantidade de horas jogadas de um jogo específico.

        Args:
            jogo_id (str): ID do jogo a ser atualizado.
            novas_horas (float): Novo total de horas jogadas.

        Raises:
            ValueError: Se o jogo não existir ou se as horas diminuírem.
        """
        for j in self.jogos:
            if j.id == jogo_id:
                if novas_horas < j.horas_jogadas:
                    raise ValueError("Horas jogadas não podem diminuir.")
                j.horas_jogadas = novas_horas
                return
        raise ValueError("Jogo não encontrado.")

   # -----------------------------
   # conferir meta anual 
   # -----------------------------
    def verificar_meta_finalizados(self):
        """
        Verifica se a meta anual de jogos finalizados foi atingida.

        Returns:
            str: Mensagem informando o progresso ou confirmação da meta.
        """
        finalizados = len([j for j in self.jogos if j.status == "Finalizado"])
        meta = self.config["meta_anual_finalizados"]

        if finalizados < meta:
            return f"⚠️ Você finalizou {finalizados}/{meta} jogos este ano!"
        return "Meta anual atingida!"
