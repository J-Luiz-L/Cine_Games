from datetime import datetime



class Jogo:
    
    """Classe Base que representa um Jogo no catálogo.
    
    Responsável por definir a estrutura fundamental (titulo, status, horas jogadas)
    e implementar o encapsulamento (@property) e os métodos especiais (__str__, __eq__, etc.) 
    que são comuns a todos os tipos de jogos (PC, Console, Mobile)."""
    
    
    def __init__(self, titulo: str, genero: str, plataforma: str):
        
        """Inicializa um objeto Jogo.
        
        Atributos:
            titulo (str): Título do jogo (Requisito: não vazio).
            genero (str): Gênero do jogo.
            plataforma (str): Plataforma (PC, Console, Mobile).
            horas_jogadas (float): Tempo total jogado (Inicial: 0.0).
            status (str): Status atual do jogo (Inicial: "NÃO INICIADO").
            avaliacao (int | None): Nota de 0 a 10 (Inicial: None).
            data_inicio (datetime | None): Data de início da jogatina.
            data_termino (datetime | None): Data de término da jogatina."""
        
       
        self._titulo = titulo
        self._genero = genero
        self._plataforma = plataforma
        self._horas_jogadas = 0.0
        self._status = "NÃO INICIADO"
        self._avaliacao = None
        self._data_inicio = None
        self._data_termino = None
        
    def atualizar_progresso(self, horas_adicionais: float):
        
        """Método placeholder para registrar progresso na Semana 2."""
        
        pass
        
    
    
    
class JogoPC(Jogo):
    
    """Representa um jogo específico para a plataforma PC.
    
    Esta classe herda de Jogo e pode incluir atributos/métodos exclusivos 
    da plataforma PC (ex: 'requisitos minimos', 'exige launcher')."""
    
    
    def __init__(self, titulo: str, genero: str):
        
        """Inicializa um JogoPC, fixando a plataforma como 'PC'."""
        
       
        super().__init__(titulo=titulo, genero=genero, plataforma="PC")

        
class JogoConsole(Jogo):
    
    """Representa um jogo específico para Consoles (PS, Xbox, Switch).
    
    Herda de Jogo."""
    
    
    def __init__(self, titulo: str, genero: str, console: str):
        
        """Inicializa um JogoConsole, onde 'console' é a plataforma específica."""
        
        
        super().__init__(titulo=titulo, genero=genero, plataforma="Console")
        
        self.console_especifico = console 
        
        
class Colecao:
    
    """Representa uma lista personalizada de jogos (ex: "Favoritos", "Zerados 2025").
    
    Responsável por agrupar objetos Jogo e gerenciar essa relação de 
    agregação/composição."""
    
    
    def __init__(self, nome: str):
        """Inicializa uma Coleção nomeada."""
        
        
        self.nome = nome
        self.jogos = [] 
        
    def adicionar_jogo(self, jogo: Jogo):
        pass