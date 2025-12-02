import streamlit as st
from src.servicos.catalogo_service import CatalogoService
from src.modelos.jogo import Jogo
from src.modelos.jogo_pc import JogoPC
from src.modelos.jogo_console import JogoConsole
from src.modelos.jogo_mobile import JogoMobile

# Serviço
service = CatalogoService()

st.title("🎮 Catálogo de Jogos - Cine Games")


# ----------------------------------------------------
# 📝 Formulário de Cadastro
# ----------------------------------------------------
st.header("Cadastrar novo jogo")

titulo = st.text_input("Título do jogo")
genero = st.text_input("Gênero")
plataforma = st.selectbox("Plataforma", ["PC", "Console", "Mobile"])
status = st.selectbox("Status", Jogo.STATUS_VALIDOS)
horas = st.number_input("Horas jogadas", min_value=0.0, step=0.5)
avaliacao = st.number_input("Avaliação 0–10", min_value=0, max_value=10)

# Campos adicionais conforme a subclasse
requisitos = None
loja = None
console = None
sistema_operacional = None

if plataforma == "PC":
    requisitos = st.text_input("Requisitos do sistema (OBRIGATÓRIO)")
    loja = st.text_input("Loja (Opcional)")

elif plataforma == "Console":
    console = st.text_input("Console (Ex: PS5, Xbox Series S) (OBRIGATÓRIO)")

elif plataforma == "Mobile":
    sistema_operacional = st.selectbox("Sistema Operacional", ["Android", "iOS"])


# Botão cadastrar
if st.button("Cadastrar jogo"):
    try:
        if plataforma == "PC":
            jogo = JogoPC(
                titulo=titulo,
                genero=genero,
                requisitos=requisitos,
                loja=loja,
                status=status,
                horas_jogadas=horas,
                avaliacao=avaliacao
            )

        elif plataforma == "Console":
            jogo = JogoConsole(
                titulo=titulo,
                genero=genero,
                console=console,
                status=status,
                horas_jogadas=horas,
                avaliacao=avaliacao
            )

        else:  # MOBILE
            jogo = JogoMobile(
                titulo=titulo,
                genero=genero,
                sistema_operacional=sistema_operacional,
                status=status,
                horas_jogadas=horas,
                avaliacao=avaliacao
            )

        service.adicionar_jogo(jogo)
        st.success(f"Jogo '{titulo}' adicionado!")
    except Exception as e:
        st.error(f"Erro ao cadastrar jogo: {e}")


st.divider()


# ----------------------------------------------------
# 🔍 FILTRAGEM
# ----------------------------------------------------
st.header("Filtrar jogos")

todos = service.listar_jogos()
generos = sorted({j.genero for j in todos})
plataformas = sorted({j.plataforma for j in todos})
status_lista = Jogo.STATUS_VALIDOS

f_genero = st.selectbox("Filtrar por gênero", [""] + generos)
f_status = st.selectbox("Filtrar por status", [""] + list(status_lista))
f_plataforma = st.selectbox("Filtrar por plataforma", [""] + plataformas)

if st.button("Aplicar filtros"):
    jogos = service.filtrar(
        genero=f_genero or None,
        status=f_status or None,
        plataforma=f_plataforma or None
    )
else:
    jogos = service.listar_jogos()

st.divider()


# ----------------------------------------------------
# 📄 LISTA DE JOGOS
# ----------------------------------------------------
st.header("Jogos cadastrados")

for j in jogos:
    with st.expander(f"{j.titulo} ({j.plataforma})"):
        st.write(f"**Gênero:** {j.genero}")
        st.write(f"**Status:** {j.status}")
        st.write(f"**Horas:** {j.horas_jogadas}")
        st.write(f"**Avaliação:** {j.avaliacao}")

        # Campos específicos
        if hasattr(j, "requisitos"):
            st.write(f"**Requisitos:** {j.requisitos}")
        if hasattr(j, "loja") and j.loja:
            st.write(f"**Loja:** {j.loja}")
        if hasattr(j, "console"):
            st.write(f"**Console:** {j.console}")
        if hasattr(j, "sistema_operacional"):
            st.write(f"**Sistema Operacional:** {j.sistema_operacional}")

        if st.button(f"Remover {j.titulo}", key=j.id):
            service.remover_jogo(j.id)
            st.warning(f"{j.titulo} removido.")
            st.experimental_rerun()
