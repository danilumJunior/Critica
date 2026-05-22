import re

from supabase_client import supabase


def extrair_caminho_storage(imagem_url):
    marcador = "/object/public/obras/"
    if marcador in imagem_url:
        return imagem_url.split(marcador, 1)[1]
    return None


def upload_capa(imagem):
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

    return supabase.storage.from_("obras").get_public_url(caminho_final)


def listar_obras():
    return supabase.table("obras").select("*").execute().data or []


def criar_obra(titulo, descricao, nota, usuario_id, nome_usuario, imagem_url):
    supabase.table("obras").insert({
        "titulo": titulo,
        "descricao": descricao,
        "nota": nota,
        "usuario_id": usuario_id,
        "nome_usuario": nome_usuario,
        "imagem_url": imagem_url,
    }).execute()


def atualizar_obra(obra_id, dados):
    supabase.table("obras").update(dados).eq("id", obra_id).execute()


def remover_arquivo_storage(caminho):
    if caminho:
        supabase.storage.from_("obras").remove([caminho])


def remover_obra(obra):
    caminho = extrair_caminho_storage(obra.get("imagem_url", ""))
    remover_arquivo_storage(caminho)
    supabase.table("obras").delete().eq("id", obra["id"]).execute()
