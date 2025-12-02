class CatalogoService:
    def __init__(self):
        from pathlib import Path
        from src.dados.repositorio import RepositorioJogos
        self.repositorio = RepositorioJogos(Path("data/jogos.json"))

    def listar_jogos(self):
        return self.repositorio.carregar()

    def adicionar_jogo(self, jogo):
        jogos = self.repositorio.carregar()
        jogos.append(jogo)
        self.repositorio.salvar(jogos)

    def remover_jogo(self, jogo_id: str):
        jogos = self.repositorio.carregar()
        jogos = [j for j in jogos if j.id != jogo_id]
        self.repositorio.salvar(jogos)

    # -----------------------------
    # 🔍 FILTROS
    # -----------------------------
    def filtrar(self, genero=None, status=None, plataforma=None):
        jogos = self.repositorio.carregar()

        if genero:
            jogos = [j for j in jogos if j.genero.lower() == genero.lower()]

        if status:
            jogos = [j for j in jogos if j.status == status]

        if plataforma:
            jogos = [j for j in jogos if j.plataforma == plataforma]

        return jogos
