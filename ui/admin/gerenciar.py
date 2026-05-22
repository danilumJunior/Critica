import time

import streamlit as st

from services.obras import (
    atualizar_obra,
    extrair_caminho_storage,
    listar_obras,
    remover_arquivo_storage,
    upload_capa,
)


def renderizar_gerenciar_obra(usuario_id, usuario_nome):
    st.header("Gerenciar obra")
    obras = listar_obras()
    if not obras:
        st.info("Nenhuma obra cadastrada para editar.")
        return

    opcoes = {obra["id"]: obra["titulo"] for obra in obras}
    obra_id = st.selectbox(
        "Selecione a obra",
        options=list(opcoes.keys()),
        format_func=lambda oid: opcoes[oid],
        key="gerenciar_select_obra",
    )
    obra = next(o for o in obras if o["id"] == obra_id)

    col_img, col_form = st.columns([1, 2])
    with col_img:
        st.image(obra["imagem_url"], caption="Capa atual")

    with col_form:
        titulo = st.text_input("Título", value=obra["titulo"], key="edit_titulo")
        descricao = st.text_area(
            "Descrição",
            value=obra["descricao"] or "",
            key="edit_descricao",
        )
        nota = st.number_input(
            "Nota",
            min_value=0.0,
            max_value=5.0,
            value=float(obra["nota"]),
            step=0.5,
            key="edit_nota",
        )
        nova_imagem = st.file_uploader(
            "Nova capa (opcional)",
            type=["jpg", "jpeg", "png"],
            key="edit_imagem",
        )

    if st.button("Salvar alterações", key="btn_salvar_obra"):
        try:
            dados = {
                "titulo": titulo,
                "descricao": descricao,
                "nota": nota,
            }
            if nova_imagem is not None:
                caminho_antigo = extrair_caminho_storage(obra.get("imagem_url", ""))
                dados["imagem_url"] = upload_capa(nova_imagem)
                remover_arquivo_storage(caminho_antigo)

            atualizar_obra(obra_id, dados)
            st.success("Obra atualizada com sucesso!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")
