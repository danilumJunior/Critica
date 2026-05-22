import streamlit as st


def renderizar_menu_admin():
    st.markdown("### Menu Admin")
    opcoes = {
        "adicionar": "Adicionar obras",
        "ver": "Ver obras",
        "gerenciar": "Gerenciar obra",
        "excluir": "Excluir obra",
        "permissoes": "Permissões",
    }
    for pagina, rotulo in opcoes.items():
        if st.button(
            rotulo,
            key=f"menu_admin_{pagina}",
            use_container_width=True,
            type="primary"
            if st.session_state["pagina_admin"] == pagina
            else "secondary",
        ):
            st.session_state["pagina_admin"] = pagina
            st.rerun()
