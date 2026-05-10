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
# SE USUÁRIO NÃO ESTIVER LOGADO
# -----------------------------------

if "usuario_id" not in st.session_state:

    email = st.text_input("E-mail")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    col1, col2 = st.columns(2)

    # CADASTRO
    with col1:

        if st.button("Cadastrar"):

            resposta = supabase.auth.sign_up({
                "email": email,
                "password": senha
            })

            st.success("Usuário cadastrado!")

    # LOGIN
    with col2:

        if st.button("Login"):

            resposta = supabase.auth.sign_in_with_password({
                "email": email,
                "password": senha
            })

            st.session_state["usuario_id"] = resposta.user.id

            st.session_state["usuario_email"] = resposta.user.email

            st.rerun()

# -----------------------------------
# SE USUÁRIO ESTIVER LOGADO
# -----------------------------------

else:

    usuario_id = st.session_state["usuario_id"]

    usuario_email = st.session_state["usuario_email"]

    st.success("Login realizado!")

    st.write("ID:", usuario_id)

    st.write("EMAIL:", usuario_email)

    # BUSCA PROFILE
    dados_profile = supabase.table("profiles") \
        .select("*") \
        .eq("id", usuario_id) \
        .execute()

    st.write(dados_profile.data)

    profile = dados_profile.data[0]

    tipo_usuario = profile["tipo"]

    st.write("TIPO DE USUÁRIO:", tipo_usuario)

    # ADMIN
    if tipo_usuario == "Admin":

        st.write("Bem-vindo, admin!")

        st.header("Área de Administração")

        st.button("Criar Obra")
        st.button("Editar Obra")
        st.button("Excluir Obra")

    # PADRÃO
    else:

        st.write("Bem-vindo, usuário!")

        st.header("Área do Usuário")

        st.write("Aqui você pode visualizar as obras disponíveis.")