import streamlit as st

from config import TIPO_ADMIN
from ui.admin import renderizar_area_admin
from ui.auth import renderizar_cabecalho_logado, renderizar_login_cadastro
from ui.catalogo import renderizar_catalogo


def run():
    st.title("Sistema de Login")

    if "usuario_id" not in st.session_state:
        renderizar_login_cadastro()
        return

    renderizar_cabecalho_logado()

    usuario_id = st.session_state["usuario_id"]
    usuario_nome = st.session_state["usuario_nome"]
    tipo_usuario = st.session_state["tipo_usuario"]

    if tipo_usuario == TIPO_ADMIN:
        renderizar_area_admin(usuario_id, usuario_nome)
    else:
        renderizar_catalogo()
