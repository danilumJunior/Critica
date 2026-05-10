import streamlit as st
from supabase import create_client


url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(url, key)

st.title("Sistema de login")

email = st.text_input("Email")
senha = st.text_input("Senha", type="password")

col1, col2 = st.columns(2)

with col1:

    if st.button("Cadastrar"):
        resposta = supabase.auth.sign_up({"email":email, "password":senha})
        st.success("Usuário cadastrado com sucesso!")

with col2:

     if st.button("Login"):

        resposta = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha
        })

        st.success("Login realizado!")