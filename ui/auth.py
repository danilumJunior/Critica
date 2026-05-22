import streamlit as st

from config import CHAVES_SESSAO_USUARIO
from supabase_client import supabase


def renderizar_login_cadastro():
    modo = st.radio("Escolha uma opção", ["Login", "Cadastro"])

    nome = None
    if modo == "Cadastro":
        nome = st.text_input("Nome")

    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if modo == "Cadastro" and st.button("Cadastrar"):
        supabase.auth.sign_up({
            "email": email,
            "password": senha,
            "options": {"data": {"nome": nome}},
        })
        st.success("Usuário cadastrado!")

    if modo == "Login" and st.button("Login"):
        resposta = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha,
        })

        usuario_id = resposta.user.id
        dados_profile = (
            supabase.table("profiles")
            .select("*")
            .eq("id", usuario_id)
            .execute()
        )
        profile = dados_profile.data[0]

        st.session_state["usuario_id"] = usuario_id
        st.session_state["usuario_email"] = resposta.user.email
        st.session_state["usuario_nome"] = profile["nome"]
        st.session_state["tipo_usuario"] = profile["tipo"]
        st.rerun()


def renderizar_cabecalho_logado():
    usuario_nome = st.session_state["usuario_nome"]
    tipo_usuario = st.session_state["tipo_usuario"]

    st.success(f"Login realizado! Seja bem-vindo, {usuario_nome}")
    st.write("Você tem a permissão de usuário:", tipo_usuario)

    if st.button("Sair da conta", key="logout"):
        fazer_logout()


def fazer_logout():
    supabase.auth.sign_out()
    for chave in CHAVES_SESSAO_USUARIO:
        st.session_state.pop(chave, None)
    st.rerun()
