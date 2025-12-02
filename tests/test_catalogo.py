# tests/test_catalogo_service.py
import os
import json
from pathlib import Path
from src.servicos.catalogo_service import CatalogoService
from src.modelos.jogo_pc import JogoPC

def test_salvar_carregar_tmp(tmp_path):
    db = tmp_path / "catalogo.json"
    svc = CatalogoService(caminho=db)
    svc.carregar()
    assert svc.listar() == []

    j = JogoPC(titulo="Teste", genero="G", requisitos="R")
    svc.adicionar(j)
    svc.salvar()

    # carregar novo serviço a partir do arquivo
    svc2 = CatalogoService(caminho=db)
    svc2.carregar()
    lista = svc2.listar()
    assert len(lista) == 1
    assert lista[0].titulo == "Teste"
    assert lista[0].requisitos == "R"

def test_remover_e_atualizar(tmp_path):
    db = tmp_path / "catalogo.json"
    svc = CatalogoService(caminho=db)
    j = JogoPC(titulo="A", genero="G", requisitos="R")
    svc.adicionar(j)
    svc.salvar()

    # remover por id
    assert svc.remover_por_id(j.id) is True
    assert len(svc.listar()) == 0

    # adicionar e atualizar
    svc.adicionar(j)
    j.titulo = "B"
    svc.atualizar(j)
    assert svc.get_by_id(j.id).titulo == "B"
