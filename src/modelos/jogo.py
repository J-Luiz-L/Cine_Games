class Jogo:
    def __init__(self, titulo, genero, plataforma):
        self.titulo = titulo
        self.genero = genero
        self.plataforma = plataforma
        self._horas_jogadas = 0
        self._status = "NÃO INICIADO"
        self._avaliacao = None

    def atualizar_progresso(self, horas): pass
    def alterar_status(self, novo_status): pass
    def registrar_avaliacao(self, nota): pass
    def reiniciar(self): pass
    def __str__(self): pass
    def __repr__(self): pass
    def __eq__(self, other): pass
    def __lt__(self, other): pass

class JogoPC(Jogo):
    def __init__(self, titulo, genero):
        super().__init__(titulo, genero, plataforma="PC")

class JogoConsole(Jogo):
    def __init__(self, titulo, genero):
        super().__init__(titulo, genero, plataforma="Console")

class JogoMobile(Jogo):
    def __init__(self, titulo, genero):
        super().__init__(titulo, genero, plataforma="Mobile")
