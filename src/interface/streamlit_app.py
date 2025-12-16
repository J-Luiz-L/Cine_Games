import streamlit as st
from datetime import date, datetime
from collections import Counter
import json
import os
import uuid

from src.modelos.jogo import Jogo
from src.modelos.colecao import Colecao
from src.servicos.catalogo_service import CatalogoService

# -------------------------------------------------
# FUNÇÕES DE PERSISTÊNCIA
# -------------------------------------------------
def salvar_json(service: CatalogoService):
    os.makedirs("data", exist_ok=True)
    # Jogos
    with open("data/jogos.json", "w", encoding="utf-8") as f:
        json.dump([j.to_dict() for j in service.jogos], f, ensure_ascii=False, indent=4)
    # Coleções
    colecoes_dict = {nome: col.to_dict() for nome, col in service.colecoes.items()}
    with open("data/colecoes.json", "w", encoding="utf-8") as f:
        json.dump(colecoes_dict, f, ensure_ascii=False, indent=4)

def carregar_json(service: CatalogoService):
    # Jogos
    if os.path.exists("data/jogos.json"):
        with open("data/jogos.json", "r", encoding="utf-8") as f:
            jogos_data = json.load(f)
            service.jogos = [Jogo.from_dict(j) for j in jogos_data]
    # Coleções
    if os.path.exists("data/colecoes.json"):
        with open("data/colecoes.json", "r", encoding="utf-8") as f:
            col_data = json.load(f)
            service.colecoes = {nome: Colecao.from_dict(d) for nome, d in col_data.items()}
        # Restaurar objetos jogo nas coleções pelo ID
        for colecao in service.colecoes.values():
            if hasattr(colecao, "_jogos_ids"):
                colecao._jogos = [j for j in service.jogos if j.id in colecao._jogos_ids]
                del colecao._jogos_ids

# -------------------------------------------------
# CONFIGURAÇÃO INICIAL
# -------------------------------------------------
st.set_page_config(page_title="Cine Games", page_icon="🎮", layout="wide")

if "service" not in st.session_state:
    st.session_state.service = CatalogoService()

service: CatalogoService = st.session_state.service

# Carregar dados salvos
carregar_json(service)

st.title("🎮 Cine Games — Catálogo de Jogos Digitais")
st.caption("Gerencie seu catálogo, coleções e estatísticas de jogos")

abas = st.tabs(["📚 Catálogo", "➕ Cadastro", "🗂️ Coleções", "📊 Estatísticas"])

# =================================================
# ABA CATÁLOGO
# =================================================
with abas[0]:
    st.subheader("📚 Jogos cadastrados")

    if not service.jogos:
        st.info("Nenhum jogo cadastrado.")
    else:
        for jogo in service.jogos:
            with st.expander(f"{jogo.titulo} — {jogo.plataforma} ({jogo.status})"):
                st.write(f"🎮 Gênero: {jogo.genero}")
                st.write(f"⏱️ Horas jogadas: {jogo.horas_jogadas}")
                st.write(f"⭐ Avaliação: {jogo.avaliacao}")
                st.write(f"📅 Início: {jogo.data_inicio}")
                st.write(f"🏁 Fim: {jogo.data_fim}")

                col1, col2, col3, col4, col5 = st.columns(5)

                # -------- Atualizar horas --------
                with col1:
                    novas_horas = st.number_input(
                        "Atualizar horas",
                        min_value=jogo.horas_jogadas,
                        step=0.5,
                        key=f"horas-{jogo.id}"
                    )
                    if st.button("Salvar horas", key=f"btn-horas-{jogo.id}"):
                        try:
                            service.atualizar_horas(jogo.id, novas_horas)
                            salvar_json(service)
                            st.success("Horas atualizadas com sucesso.")
                        except ValueError as e:
                            st.error(str(e))

                # -------- Reiniciar jogo --------
                with col2:
                    if st.button("🔄 Reiniciar jogo", key=f"reset-{jogo.id}"):
                        jogo._status = "Backlog"
                        jogo._avaliacao = None
                        jogo._horas_jogadas = 0.0
                        jogo.data_inicio = None
                        jogo.data_fim = None
                        salvar_json(service)
                        st.warning("Jogo reiniciado para Backlog.")

                # -------- Remover jogo --------
                with col3:
                    if st.button("🗑️ Remover", key=f"remover-{jogo.id}"):
                        service.jogos.remove(jogo)
                        salvar_json(service)
                        st.error("Jogo removido do catálogo.")
                        st.rerun()

                # -------- Alterar avaliação --------
                with col4:
                    nova_avaliacao = st.number_input(
                        "Alterar avaliação",
                        min_value=0,
                        max_value=10,
                        value=jogo.avaliacao or 0,
                        key=f"aval-{jogo.id}"
                    )
                    if st.button("Salvar avaliação", key=f"btn-aval-{jogo.id}"):
                        jogo._avaliacao = nova_avaliacao
                        salvar_json(service)
                        st.success("Avaliação atualizada.")

                # -------- Alterar status --------
                with col5:
                    status_novo = st.selectbox(
                        "Alterar status",
                        options=Jogo.STATUS_VALIDOS,
                        index=Jogo.STATUS_VALIDOS.index(jogo.status),
                        key=f"status-{jogo.id}"
                    )
                    if status_novo != jogo.status:
                        jogo._status = status_novo
                        salvar_json(service)
                        st.success(f"Status atualizado para {status_novo}.")

                # -------- Atualizar datas --------
                jogo.data_inicio = st.date_input(
                    "Data de início",
                    value=jogo.data_inicio or date.today(),
                    key=f"start-{jogo.id}"
                )

                t_fim_disabled = jogo.status.lower() == "jogando"
                jogo.data_fim = st.date_input(
                    "Data de término",
                    value=jogo.data_fim or date.today(),
                    key=f"end-{jogo.id}",
                    disabled=t_fim_disabled
                )
                salvar_json(service)

# =================================================
# ABA CADASTRO
# =================================================
with abas[1]:
    st.subheader("➕ Cadastrar novo jogo")

    titulo = st.text_input("Título")
    genero = st.text_input("Gênero")
    plataforma = st.selectbox("Plataforma", ["PC", "PlayStation", "Xbox", "Switch"])
    status = st.selectbox("Status", Jogo.STATUS_VALIDOS)
    horas = st.number_input("Horas jogadas", min_value=0.0, step=0.5)
    avaliacao = st.number_input("Avaliação (0–10)", min_value=0, max_value=10)
    data_inicio = st.date_input("Data de início", value=date.today())
    data_fim = st.date_input("Data de término", value=date.today(), disabled=status.lower() == "jogando")

    if st.button("Cadastrar jogo"):
        try:
            jogo = Jogo(
                titulo=titulo,
                genero=genero,
                plataforma=plataforma,
                status=status,
                horas_jogadas=horas,
                avaliacao=avaliacao if avaliacao > 0 else None
            )
            jogo.data_inicio = data_inicio
            jogo.data_fim = data_fim
            service.adicionar_jogo(jogo)
            salvar_json(service)
            st.success("Jogo cadastrado com sucesso!")
        except ValueError as e:
            st.error(str(e))

# =================================================
# ABA COLEÇÕES
# =================================================
with abas[2]:
    st.subheader("🗂️ Gerenciar coleções")

    nome_colecao = st.text_input("Nome da coleção")

    if st.button("Criar coleção"):
        try:
            service.colecoes[nome_colecao] = Colecao(nome_colecao)
            salvar_json(service)
            st.success(f"Coleção '{nome_colecao}' criada.")
        except ValueError as e:
            st.error(str(e))

    if service.colecoes:
        colecao_nome = st.selectbox("Escolha uma coleção", list(service.colecoes.keys()))
        colecao = service.colecoes[colecao_nome]

        st.write("🎮 Jogos na coleção:")
        for jogo in colecao.listar():
            if st.button(f"Remover {jogo.titulo}", key=f"rm-col-{jogo.id}"):
                colecao.remover(jogo)
                salvar_json(service)
                st.warning("Jogo removido da coleção.")
                st.rerun()

        jogo_para_add = st.selectbox(
            "Adicionar jogo à coleção",
            [j.titulo for j in service.jogos]
        )

        if st.button("Adicionar à coleção"):
            jogo = next(j for j in service.jogos if j.titulo == jogo_para_add)
            colecao.adicionar(jogo)
            salvar_json(service)
            st.success("Jogo adicionado à coleção.")

# =================================================
# ABA ESTATÍSTICAS
# =================================================
with abas[3]:
    st.subheader("📊 Estatísticas do catálogo")

    st.metric("🎮 Total de jogos", len(service.jogos))
    st.metric("⏱️ Horas jogadas", service.total_horas())
    st.metric("⭐ Média de avaliação", service.media_avaliacao())

    # Top 5 jogos mais jogados
    top5 = sorted(service.jogos, key=lambda j: j.horas_jogadas, reverse=True)[:5]
    st.write("🏆 Top 5 jogos mais jogados:")
    for i, j in enumerate(top5, start=1):
        st.write(f"{i}. {j.titulo} — {j.horas_jogadas} horas")

    # Gênero mais jogado
    generos = [j.genero for j in service.jogos]
    if generos:
        genero_mais = Counter(generos).most_common(1)[0][0]
        st.write(f"🎨 Gênero mais jogado: {genero_mais}")

    # Plataforma mais jogada
    plataformas = [j.plataforma for j in service.jogos]
    if plataformas:
        plataforma_mais = Counter(plataformas).most_common(1)[0][0]
        st.write(f"🖥️ Plataforma mais jogada: {plataforma_mais}")

    aviso = service.verificar_meta_finalizados()
    if "⚠️" in aviso:
        st.warning(aviso)
    else:
        st.success(aviso)
