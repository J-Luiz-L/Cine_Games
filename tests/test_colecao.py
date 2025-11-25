from src.modelos.colecao import Colecao
from src.modelos.jogo import Jogo

def test_colecao_add():
    c = Colecao("Favoritos")
    j = Jogo(titulo="X", genero="Ação")
    c.adicionar_jogo(j)
    assert len(c) == 1
    assert c.buscar_por_titulo("x")
