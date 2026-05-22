import streamlit as st

from services.obras import listar_obras
from ui.components import renderizar_card_obra


def renderizar_ver_obras(usuario_id, usuario_nome):
    st.header("Obras cadastradas")
    obras = listar_obras()
    if obras:
        for obra in obras:
            renderizar_card_obra(obra, key_prefix="ver_")
    else:
        st.info("Nenhuma obra cadastrada ainda.")
