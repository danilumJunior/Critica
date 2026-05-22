import time

import streamlit as st

from services.obras import remover_obra


def renderizar_card_obra(obra, mostrar_excluir=False, key_prefix=""):
    with st.container(border=True):
        col_img, col_info, col_acao = st.columns([1, 2, 1])

        with col_img:
            st.image(obra["imagem_url"])

        with col_info:
            st.subheader(obra["titulo"])
            st.write(f"**Nota:** {obra['nota']} ⭐")
            st.write(f"**Postado por:** {obra['nome_usuario']}")
            st.write(obra["descricao"])

        if mostrar_excluir:
            with col_acao:
                if st.button(
                    "Excluir",
                    key=f"{key_prefix}excluir_obra_{obra['id']}",
                ):
                    try:
                        remover_obra(obra)
                        st.success("Obra removida com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao remover: {e}")
