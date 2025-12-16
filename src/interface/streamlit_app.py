import streamlit as st
from src.servicos.catalogo_service import CatalogoService
from src.modelos.jogo import Jogo
from src.modelos.jogo_pc import JogoPC
from src.modelos.jogo_console import JogoConsole
from src.modelos.jogo_mobile import JogoMobile

if "service" not in st.session_state:
    st.session_state.service = CatalogoService()

service = st.session_state.service

st.set_page_config(page_title="Cine Games", page_icon="🎮", layout="wide")
st.title("🎮 Cine Games — Catálogo de Jogos")


meta_msg = service.verificar_meta_finalizados() if hasattr(service, "verificar_meta_finalizados") else None
if meta_msg:
    st.warning(meta_msg)


col1, col2 = st.columns([2, 3])

with col1:
    st.header("➕ Cadastrar novo jogo")

    titulo = st.text_input("Título")
    genero = st.text_input("Gênero")
    plataforma = st.selectbox("Plataforma", ["PC", "Console", "Mobile"])
    status = st.selectbox("Status", Jogo.STATUS_VALIDOS)
    horas_jogadas = st.number_input("Horas jogadas", min_value=0.0, step=0.5, value=0.0)
    avaliacao = st.number_input("Avaliação (0–10)", min_value=0, max_value=10, value=0)

    requisitos = ""
    loja = ""
    console = ""
    sistema_operacional = ""

    if plataforma == "PC":
        requisitos = st.text_input("Requisitos (OBRIGATÓRIO)", help="Ex.: i5, 8GB RAM, GTX 1050")
        loja = st.text_input("Loja (Opcional) ex: Steam")

    elif plataforma == "Console":
        console = st.text_input("Console (OBRIGATÓRIO) ex: PS5, Xbox Series S")

    else:  
        sistema_operacional = st.selectbox("Sistema operacional (OBRIGATÓRIO)", ["Android", "iOS"])

    if st.button("Salvar jogo"):
        try:
            
            if not titulo or not genero:
                st.error("Título e gênero são obrigatórios.")
            else:
                if plataforma == "PC":
                    
                    jogo = JogoPC(
                        titulo=titulo,
                        genero=genero,
                        requisitos=requisitos,
                        loja=loja or None,
                        status=status,
                        horas_jogadas=horas_jogadas,
                        avaliacao=avaliacao
                    )
                elif plataforma == "Console":
                    jogo = JogoConsole(
                        titulo=titulo,
                        genero=genero,
                        console=console,
                        status=status,
                        horas_jogadas=horas_jogadas,
                        avaliacao=avaliacao
                    )
                else:  
                    jogo = JogoMobile(
                        titulo=titulo,
                        genero=genero,
                        sistema_operacional=sistema_operacional,
                        status=status,
                        horas_jogadas=horas_jogadas,
                        avaliacao=avaliacao
                    )

                service.adicionar_jogo(jogo)
                st.success(f"Jogo '{titulo}' cadastrado com sucesso!")
                st.rerun()
        except Exception as e:
            st.error(f"Erro ao cadastrar jogo: {e}")

with col2:
    st.header("🔎 Buscar / Filtrar")
    jogos_all = service.listar_jogos()

    generos = sorted({j.genero for j in jogos_all})
    plataformas = sorted({j.plataforma for j in jogos_all})
    status_lista = list(Jogo.STATUS_VALIDOS)

    f_genero = st.selectbox("Filtrar por gênero", [""] + generos)
    f_plataforma = st.selectbox("Filtrar por plataforma", [""] + plataformas)
    f_status = st.selectbox("Filtrar por status", [""] + status_lista)
    texto_busca = st.text_input("Buscar por título (contém)")

    jogos = jogos_all
    if f_genero:
        jogos = [j for j in jogos if j.genero == f_genero]
    if f_plataforma:
        jogos = [j for j in jogos if j.plataforma == f_plataforma]
    if f_status:
        jogos = [j for j in jogos if j.status == f_status]
    if texto_busca:
        jogos = [j for j in jogos if texto_busca.lower() in j.titulo.lower()]

st.markdown("---")


st.header("📚 Jogos cadastrados")
if not jogos:
    st.info("Nenhum jogo para exibir com os filtros atuais.")
else:
    for jogo in jogos:
        with st.expander(f"{jogo.titulo} — {jogo.plataforma} ({jogo.status})"):
            cols = st.columns([3, 1, 1])
            with cols[0]:
                st.markdown(f"**Gênero:** {jogo.genero}")
                st.markdown(f"**Horas jogadas:** {jogo.horas_jogadas}")
                st.markdown(f"**Avaliação:** {jogo.avaliacao}")
                st.markdown(f"**ID:** `{jogo.id}`")

                if hasattr(jogo, "requisitos"):
                    st.markdown(f"**Requisitos:** {jogo.requisitos}")
                if hasattr(jogo, "loja") and jogo.loja:
                    st.markdown(f"**Loja:** {jogo.loja}")
                if hasattr(jogo, "console"):
                    st.markdown(f"**Console:** {jogo.console}")
                if hasattr(jogo, "sistema_operacional"):
                    st.markdown(f"**Sistema operacional:** {jogo.sistema_operacional}")

            with cols[1]:
                novo_horas = st.number_input(f"Horas ({jogo.titulo})", value=float(jogo.horas_jogadas), min_value=0.0, step=0.5, key=f"horas-{jogo.id}")
                if st.button("Atualizar horas", key=f"upd-{jogo.id}"):
                    try:
                        if hasattr(service, "atualizar_horas"):
                            service.atualizar_horas(jogo.id, novo_horas)
                        else:
                            jogo._horas_jogadas = novo_horas
                        st.success("Horas atualizadas.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar horas: {e}")

            with cols[2]:
                if st.button("Remover", key=f"rm-{jogo.id}"):
                    try:
                        service.remover_jogo(jogo.id)
                        st.warning(f"'{jogo.titulo}' removido.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao remover: {e}")
