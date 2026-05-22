import streamlit as st

from config import PAGINA_ADMIN_PADRAO
from ui.admin.adicionar import renderizar_adicionar_obra
from ui.admin.excluir import renderizar_excluir_obra
from ui.admin.gerenciar import renderizar_gerenciar_obra
from ui.admin.menu import renderizar_menu_admin
from ui.admin.permissoes import renderizar_permissoes
from ui.admin.ver import renderizar_ver_obras

PAGINAS_ADMIN = {
    "adicionar": renderizar_adicionar_obra,
    "ver": renderizar_ver_obras,
    "gerenciar": renderizar_gerenciar_obra,
    "excluir": renderizar_excluir_obra,
    "permissoes": renderizar_permissoes,
}


def renderizar_area_admin(usuario_id, usuario_nome):
    if "pagina_admin" not in st.session_state:
        st.session_state["pagina_admin"] = PAGINA_ADMIN_PADRAO

    col_menu, col_conteudo = st.columns([1, 4])

    with col_menu:
        renderizar_menu_admin()

    with col_conteudo:
        pagina = st.session_state["pagina_admin"]
        renderizar = PAGINAS_ADMIN.get(pagina, renderizar_adicionar_obra)
        renderizar(usuario_id, usuario_nome)
