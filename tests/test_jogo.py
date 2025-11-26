from src.modelos.jogo import Jogo

from src.modelos.jogo_pc import JogoPC



def test_jogo_basico():

    j = Jogo(titulo="X", genero="Aventura")

    assert j.titulo == "X"

    j.registrar_progresso(2.5)

    assert j.horas_jogadas == 2.5



def test_jogo_pc_to_dict_from_dict():

    j = JogoPC(titulo="Portal", genero="Puzzle", requisitos="Minimo 4GB")

    d = j.to_dict()

    novo = JogoPC.from_dict(d)

    assert novo.titulo == j.titulo

    assert novo.requisitos == j.requisitos