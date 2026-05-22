import streamlit as st

from services.obras import listar_obras
from ui.components import renderizar_card_obra


def renderizar_excluir_obra(usuario_id, usuario_nome):
    st.header("Excluir obra")
    obras = listar_obras()
    if obras:
        for obra in obras:
            renderizar_card_obra(obra, mostrar_excluir=True, key_prefix="del_")
    else:
        st.info("Nenhuma obra cadastrada ainda.")
