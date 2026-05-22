import streamlit as st

from services.obras import listar_obras


def renderizar_catalogo():
    st.header("Obras Disponíveis")

    obras = listar_obras()
    if not obras:
        st.info("Nenhuma obra cadastrada ainda.")
        return

    for obra in obras:
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(obra["imagem_url"])

            with col2:
                st.subheader(obra["titulo"])
            st.write(f"**Nota:** {obra['nota']} ⭐")
            st.write(f"**Postado por:** {obra['nome_usuario']}")
            st.write(obra["descricao"])
