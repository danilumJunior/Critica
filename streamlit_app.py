import streamlit as st
from supabase import create_client

# -----------------------------------
# CONEXÃO SUPABASE
# -----------------------------------

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(url, key)

# -----------------------------------
# TÍTULO
# -----------------------------------

st.title("Sistema de Login")

# -----------------------------------
# USUÁRIO NÃO LOGADO
# -----------------------------------

if "usuario_id" not in st.session_state:

    modo = st.radio(
        "Escolha uma opção",
        ["Login", "Cadastro"]
    )

    # INPUTS

    if modo == "Cadastro":

        nome = st.text_input("Nome")

    email = st.text_input("E-mail")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    # -----------------------------------
    # CADASTRO
    # -----------------------------------

    if modo == "Cadastro":

        if st.button("Cadastrar"):

            resposta = supabase.auth.sign_up({

                "email": email,

                "password": senha,

                "options": {

                    "data": {

                        "nome": nome

                    }

                }

            })

            st.success("Usuário cadastrado!")

    # -----------------------------------
    # LOGIN
    # -----------------------------------

    if modo == "Login":

        if st.button("Login"):

            resposta = supabase.auth.sign_in_with_password({

                "email": email,

                "password": senha

            })

            usuario_id = resposta.user.id

            usuario_email = resposta.user.email

            # BUSCA PROFILE

            dados_profile = supabase.table("profiles") \
                .select("*") \
                .eq("id", usuario_id) \
                .execute()

            profile = dados_profile.data[0]

            # SALVA DADOS NA SESSÃO

            st.session_state["usuario_id"] = usuario_id

            st.session_state["usuario_email"] = usuario_email

            st.session_state["usuario_nome"] = profile["nome"]

            st.session_state["tipo_usuario"] = profile["tipo"]

            st.rerun()

# -----------------------------------
# USUÁRIO LOGADO
# -----------------------------------

else:

    usuario_nome = st.session_state["usuario_nome"]

    usuario_id = st.session_state["usuario_id"]

    usuario_email = st.session_state["usuario_email"]

    tipo_usuario = st.session_state["tipo_usuario"]

    # MENSAGEM LOGIN

    st.success(
        f"Login realizado! Seja bem-vindo, {usuario_nome}"
    )

    # DADOS

    st.write("ID:", usuario_id)

    st.write("EMAIL:", usuario_email)

    st.write("TIPO DE USUÁRIO:", tipo_usuario)

    # -----------------------------------
    # ADMIN
    # -----------------------------------

    if tipo_usuario == "Admin":

        st.write("Bem-vindo, admin!")

        st.header("Área de Administração")

        st.button("Criar Obra")

        st.button("Editar Obra")

        st.button("Excluir Obra")

    # -----------------------------------
    # USUÁRIO PADRÃO
    # -----------------------------------

    else:

        st.write("Bem-vindo, usuário!")

        st.header("Área do Usuário")

        st.write(
            "Aqui você pode visualizar as obras disponíveis."
        )