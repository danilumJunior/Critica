import time

import streamlit as st

from services.obras import criar_obra, upload_capa


def renderizar_adicionar_obra(usuario_id, usuario_nome):
    st.header("Adicionar obra")
    titulo = st.text_input("Título", key="add_titulo")
    descricao = st.text_area("Descrição", key="add_descricao")
    imagem = st.file_uploader(
        "Imagem da obra",
        type=["jpg", "jpeg", "png"],
        key="add_imagem",
    )
    nota = st.number_input(
        "Nota",
        min_value=0.0,
        max_value=5.0,
        value=5.0,
        step=0.5,
        key="add_nota",
    )

    if st.button("Criar obra", key="btn_criar_obra"):
        if not titulo.strip():
            st.warning("Informe o título da obra.")
            return
        if imagem is None:
            st.warning("Selecione uma imagem para a obra.")
            return
        try:
            url_publica = upload_capa(imagem)
            criar_obra(
                titulo, descricao, nota, usuario_id, usuario_nome, url_publica
            )
            st.success("Obra criada com sucesso!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao criar obra: {e}")
