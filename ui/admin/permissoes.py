import time

import streamlit as st

from config import TIPO_ADMIN, TIPO_PADRAO
from services.perfis import atualizar_tipo, listar_perfis


def renderizar_permissoes(usuario_id, usuario_nome):
    st.header("Permissões de usuário")
    perfis = listar_perfis()
    if not perfis:
        st.info("Nenhum usuário encontrado.")
        return

    opcoes = {p["id"]: f"{p['nome']} ({p['tipo']})" for p in perfis}
    perfil_id = st.selectbox(
        "Selecione o usuário",
        options=list(opcoes.keys()),
        format_func=lambda pid: opcoes[pid],
        key="perm_select_usuario",
    )
    perfil = next(p for p in perfis if p["id"] == perfil_id)

    tipo_atual = perfil["tipo"]
    novo_tipo = st.radio(
        "Tipo de permissão",
        options=[TIPO_ADMIN, TIPO_PADRAO],
        index=0 if tipo_atual == TIPO_ADMIN else 1,
        format_func=lambda t: "Administrador" if t == TIPO_ADMIN else "Padrão",
        key="perm_tipo",
    )

    if perfil_id == usuario_id and novo_tipo != TIPO_ADMIN:
        st.warning(
            "Você está removendo seu próprio acesso de administrador. "
            "Confirme apenas se deseja continuar."
        )

    if st.button("Salvar permissão", key="btn_salvar_perm"):
        try:
            atualizar_tipo(perfil_id, novo_tipo)
            if perfil_id == usuario_id:
                st.session_state["tipo_usuario"] = novo_tipo
            st.success("Permissão atualizada com sucesso!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao atualizar permissão: {e}")
