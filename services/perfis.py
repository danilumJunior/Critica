from supabase_client import supabase


def listar_perfis():
    return supabase.table("profiles").select("id, nome, tipo").execute().data or []


def atualizar_tipo(perfil_id, tipo):
    supabase.table("profiles").update({"tipo": tipo}).eq("id", perfil_id).execute()
