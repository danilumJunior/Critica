import streamlit as st
from supabase import create_client
import re
import time


# -----------------------------------
# CONEXÃO SUPABASE
# -----------------------------------

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(url, key)


def extrair_caminho_storage(imagem_url):
    marcador = "/object/public/obras/"
    if marcador in imagem_url:
        return imagem_url.split(marcador, 1)[1]
    return None


def remover_obra(obra):
    caminho = extrair_caminho_storage(obra.get("imagem_url", ""))
    if caminho:
        supabase.storage.from_("obras").remove([caminho])
    supabase.table("obras").delete().eq("id", obra["id"]).execute()


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

    st.write("TIPO DE USUÁRIO:", tipo_usuario)

    if st.button("Sair da conta", key="logout"):
        supabase.auth.sign_out()
        for chave in (
            "usuario_id",
            "usuario_email",
            "usuario_nome",
            "tipo_usuario",
            "pagina_admin",
        ):
            st.session_state.pop(chave, None)
        st.rerun()

    if "pagina_admin" not in st.session_state:
        st.session_state["pagina_admin"] = "principal"

    # -----------------------------------
    # ADMIN
    # -----------------------------------

    if tipo_usuario == "Admin":

        if st.session_state["pagina_admin"] == "principal":

            st.header("Área de Administração")
            titulo = st.text_input("Título")
            descricao = st.text_area("Descrição")
            imagem = st.file_uploader(
                "Imagem da obra",
                type=["jpg", "jpeg", "png"],
            )
            nota = st.number_input(
                "Nota",
                min_value=0.0,
                max_value=5.0,
                value=5.0,
                step=0.5,
            )

            if st.button("Criar Obra"):
                if imagem is not None:
                    try:
                        nome_arquivo = imagem.name
                        nome_limpo = re.sub(r"[^a-zA-Z0-9.-]", "_", nome_arquivo)
                        caminho_final = f"capas/{nome_limpo}"

                        supabase.storage.from_("obras").upload(
                            path=caminho_final,
                            file=imagem.getvalue(),
                            file_options={
                                "content-type": imagem.type,
                                "upsert": "true",
                            },
                        )

                        url_publica = supabase.storage.from_("obras").get_public_url(
                            caminho_final
                        )

                        supabase.table("obras").insert({
                            "titulo": titulo,
                            "descricao": descricao,
                            "nota": nota,
                            "usuario_id": usuario_id,
                            "nome_usuario": usuario_nome,
                            "imagem_url": url_publica,
                        }).execute()

                        st.success("Obra criada com sucesso!")
                        time.sleep(1)
                        st.rerun()

                    except Exception as e:
                        st.error(f"Erro no upload: {e}")

            if st.button("Remover obras", type="primary"):
                st.session_state["pagina_admin"] = "remover"
                st.rerun()

        else:

            st.header("Remover obras")

            if st.button("← Voltar"):
                st.session_state["pagina_admin"] = "principal"
                st.rerun()

            obras_admin = supabase.table("obras").select("*").execute()

            if obras_admin.data:
                for obra in obras_admin.data:
                    with st.container(border=True):
                        col_img, col_info, col_acao = st.columns([1, 2, 1])

                        with col_img:
                            st.image(obra["imagem_url"])

                        with col_info:
                            st.subheader(obra["titulo"])
                            st.write(f"**Nota:** {obra['nota']} ⭐")
                            st.write(f"**Postado por:** {obra['nome_usuario']}")
                            st.write(obra["descricao"])

                        with col_acao:
                            if st.button(
                                "Excluir",
                                key=f"excluir_obra_{obra['id']}",
                            ):
                                try:
                                    remover_obra(obra)
                                    st.success("Obra removida com sucesso!")
                                    time.sleep(1)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao remover: {e}")
            else:
                st.info("Nenhuma obra cadastrada ainda.")

    # -----------------------------------
    # USUÁRIO PADRÃO
    # -----------------------------------

    else:

        st.header("Obras Disponíveis")

        obras = supabase.table("obras").select("*").execute()

        if obras.data:
            for obra in obras.data:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.image(obra["imagem_url"])
                    
                    with col2:
                        st.subheader(obra["titulo"])
                    st.write(f"**Nota:** {obra['nota']} ⭐")
                    st.write(f"**Postado por:** {obra['nome_usuario']}")
                    st.write(obra["descricao"])
        else:
            st.info("Nenhuma obra cadastrada ainda.")
        