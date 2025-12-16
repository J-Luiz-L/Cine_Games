import streamlit as st
from src.servicos.catalogo_service import CatalogoService
from src.modelos.jogo import Jogo
from src.modelos.jogo_pc import JogoPC
from src.modelos.jogo_console import JogoConsole
from src.modelos.jogo_mobile import JogoMobile
from src.modelos.colecao import Colecao

# --------------------------
# Configuração da página
# --------------------------
st.set_page_config(page_title="Cine Games", page_icon="🎮", layout="wide")

# --------------------------
# Inicialização do serviço e session_state
# --------------------------
if "service" not in st.session_state:
    st.session_state.service = CatalogoService()

service = st.session_state.service

if "jogos" not in st.session_state:
    st.session_state.jogos = service.jogos.copy()

if "aba_atual" not in st.session_state:
    st.session_state.aba_atual = "➕ Cadastro"

# --------------------------
# Título da aplicação
# --------------------------
st.title("🎮 Cine Games — Catálogo de Jogos")
st.caption("Catalogação de jogos digitais com funcionalidades avançadas!")

# --------------------------
# Controle de abas via radio
# --------------------------
abas = ["📋 Catálogo", "➕ Cadastro", "🗂️ Coleções", "📊 Estatísticas"]
aba_selecionada = st.radio("Escolha a aba", abas, index=abas.index(st.session_state.aba_atual))
st.session_state.aba_atual = aba_selecionada

# ==========================
# ABA CATÁLOGO
# ==========================
if aba_selecionada == "📋 Catálogo":
    st.subheader("📋 Jogos cadastrados")
    jogos_all = st.session_state.jogos

    # Filtros
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        f_genero = st.selectbox("Filtrar por Gênero", [""] + sorted({j.genero for j in jogos_all}))
    with col_f2:
        f_plataforma = st.selectbox("Filtrar por Plataforma", [""] + sorted({j.plataforma for j in jogos_all}))
    with col_f3:
        f_status = st.selectbox("Filtrar por Status", [""] + list(Jogo.STATUS_VALIDOS))
    with col_f4:
        termo = st.text_input("Buscar por Título")

    jogos = jogos_all
    if f_genero:
        jogos = [j for j in jogos if j.genero == f_genero]
    if f_plataforma:
        jogos = [j for j in jogos if j.plataforma == f_plataforma]
    if f_status:
        jogos = [j for j in jogos if j.status == f_status]
    if termo:
        jogos = [j for j in jogos if termo.lower() in j.titulo.lower()]

    # Ordenação
    criterio = st.selectbox("Ordenar por", ["horas", "avaliacao", "ano"])
    jogos = service.ordenar(criterio)

    if not jogos:
        st.info("Nenhum jogo encontrado.")
    else:
        for jogo in jogos:
            with st.expander(f"{jogo.titulo} — {jogo.plataforma} ({jogo.status})"):
                st.write(f"🎮 Gênero: {jogo.genero}")
                st.write(f"⏱️ Horas jogadas: {jogo.horas_jogadas}")
                st.write(f"⭐ Avaliação: {jogo.avaliacao}")
                st.write(f"**ID**: {jogo.id}")

                col1, col2 = st.columns(2)
                with col1:
                    novo_horas = st.number_input(
                        f"Atualizar Horas ({jogo.titulo})",
                        value=jogo.horas_jogadas,
                        min_value=0.0,
                        step=0.5,
                        key=f"horas-{jogo.id}"
                    )
                    if st.button("Atualizar", key=f"upd-{jogo.id}"):
                        service.atualizar_horas(jogo.id, novo_horas)
                        st.success("Horas atualizadas.")
                        st.session_state.jogos = service.jogos.copy()

                with col2:
                    if st.button("Reiniciar", key=f"reiniciar-{jogo.id}"):
                        jogo.reiniciar()
                        st.success(f"Jogo '{jogo.titulo}' reiniciado.")
                        st.session_state.jogos = service.jogos.copy()

                    if st.button("Remover", key=f"rm-{jogo.id}"):
                        service.remover_jogo(jogo.id)
                        st.warning(f"'{jogo.titulo}' removido.")
                        st.session_state.jogos = service.jogos.copy()

# ==========================
# ABA CADASTRO
# ==========================
elif aba_selecionada == "➕ Cadastro":
    st.subheader("➕ Cadastrar Novo Jogo")

    titulo = st.text_input("Título")
    genero = st.text_input("Gênero")
    plataforma = st.selectbox("Plataforma", ["PC", "Console", "Mobile"])
    status = st.selectbox("Status", Jogo.STATUS_VALIDOS)
    horas_jogadas = st.number_input("Horas jogadas", min_value=0.0, step=0.5)
    avaliacao = st.number_input("Avaliação (0-10)", min_value=0, max_value=10)

    requisitos = loja = console = sistema_operacional = ""

    if plataforma == "PC":
        requisitos = st.text_input("Requisitos (OBRIGATÓRIO)")
        loja = st.text_input("Loja (Opcional)")
    elif plataforma == "Console":
        console = st.text_input("Console (OBRIGATÓRIO)")
    else:
        sistema_operacional = st.selectbox("Sistema operacional (OBRIGATÓRIO)", ["Android", "iOS"])

    if st.button("Cadastrar jogo"):
        if not titulo or not genero:
            st.error("Título e Gênero são obrigatórios.")
        else:
            # Criação do objeto do jogo
            if plataforma == "PC":
                jogo = JogoPC(
                    titulo=titulo, genero=genero, requisitos=requisitos,
                    loja=loja, status=status, horas_jogadas=horas_jogadas,
                    avaliacao=avaliacao
                )
            elif plataforma == "Console":
                jogo = JogoConsole(
                    titulo=titulo, genero=genero, console=console,
                    status=status, horas_jogadas=horas_jogadas,
                    avaliacao=avaliacao
                )
            else:
                jogo = JogoMobile(
                    titulo=titulo, genero=genero,
                    sistema_operacional=sistema_operacional,
                    status=status, horas_jogadas=horas_jogadas,
                    avaliacao=avaliacao
                )

            # Adiciona no serviço com captura de exceção
            try:
                service.adicionar_jogo(jogo)
                st.session_state.jogos.append(jogo)
                st.success(f"Jogo '{titulo}' adicionado com sucesso!")
                st.session_state.aba_atual = "📋 Catálogo"
            except ValueError as e:
                st.error(str(e))

# ==========================
# ABA COLEÇÕES
# ==========================
elif aba_selecionada == "🗂️ Coleções":
    st.subheader("🗂️ Gerenciar Coleções")
    nome_colecao = st.text_input("Nome da Coleção")

    if st.button("Criar Coleção"):
        try:
            service.criar_colecao(nome_colecao)
            st.success(f"Coleção '{nome_colecao}' criada!")
        except Exception as e:
            st.error(str(e))

    colecoes_list = list(service.colecoes.keys())
    if colecoes_list:
        colecao_escolhida = st.selectbox("Escolha uma coleção", colecoes_list)
        st.write(f"**Jogos na Coleção '{colecao_escolhida}':**")
        colecao = service.colecoes.get(colecao_escolhida)
        if colecao:
            for jogo in colecao.listar():
                st.write(f"{jogo.titulo} — {jogo.plataforma}")

        jogos_para_adicionar = [j.titulo for j in st.session_state.jogos]
        if jogos_para_adicionar:
            jogo_para_adicionar = st.selectbox("Adicionar jogo à coleção", jogos_para_adicionar)
            if st.button("Adicionar jogo à coleção"):
                jogo = next(j for j in st.session_state.jogos if j.titulo == jogo_para_adicionar)
                service.adicionar_em_colecao(colecao_escolhida, jogo)
                st.success(f"Jogo '{jogo.titulo}' adicionado à coleção!")

# ==========================
# ABA ESTATÍSTICAS
# ==========================
elif aba_selecionada == "📊 Estatísticas":
    st.subheader("📊 Estatísticas do Catálogo")

    jogos = st.session_state.jogos
    col1, col2, col3 = st.columns(3)
    col1.metric("🎮 Total de jogos", len(jogos))
    col2.metric("⏱️ Horas jogadas", sum(j.horas_jogadas for j in jogos))
    col3.metric(
        "⭐ Média avaliação",
        round(sum(j.avaliacao for j in jogos)/len(jogos), 2) if jogos else 0
    )

    dados = service.percentual_por_status()
    if dados:
        st.bar_chart(dados)

    st.subheader("🔥 Top 5 Jogos Mais Jogados")
    top5 = service.top_5_mais_jogados()
    for jogo in top5:
        st.write(f"{jogo.titulo} — {jogo.horas_jogadas} horas")

    st.subheader("🎮 Gênero Favorito")
    genero_favorito = service.genero_favorito()
    if genero_favorito:
        st.write(genero_favorito)

    st.subheader("📱 Plataforma Principal")
    plataforma_principal = service.plataforma_principal()
    if plataforma_principal:
        st.write(plataforma_principal)
