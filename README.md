# Critica

Aplicacao web em Streamlit para autenticacao e avaliacao de obras audiovisuais, inspirada na experiencia do Letterboxd. O projeto usa Python no frontend/backend da aplicacao, Supabase para autenticacao e persistencia de dados, e Streamlit para entregar a interface.

> Estado atual: o app implementa cadastro, login, leitura do perfil do usuario no Supabase e exibicao de areas diferentes para usuarios comuns e administradores. As funcionalidades de catalogo, criacao de obras e avaliacoes ainda aparecem como proximos passos ou botoes sem acao implementada.

## Stack

- Python
- Streamlit
- Supabase
- Supabase Auth
- Supabase Database

## Estrutura do projeto

```text
Critica/
+-- .streamlit/
|   +-- secrets.toml
+-- README.md
+-- requirements.txt
+-- streamlit_app.py
```

## Funcionalidades atuais

- Cadastro de usuario com e-mail, senha e nome.
- Login com e-mail e senha usando Supabase Auth.
- Persistencia dos dados do usuario logado em `st.session_state`.
- Busca do perfil do usuario na tabela `profiles`.
- Controle simples de permissao por tipo de usuario:
  - `Admin`: visualiza a area de administracao e botoes para criar, editar e excluir obras.
  - Usuario comum: visualiza a area do usuario.

## Fluxo da aplicacao

1. O app carrega as credenciais do Supabase a partir de `st.secrets`.
2. Um cliente Supabase e criado com `create_client`.
3. Se nao houver `usuario_id` em `st.session_state`, o usuario pode escolher entre login e cadastro.
4. No cadastro, o app chama `supabase.auth.sign_up` e salva o nome nos metadados do usuario.
5. No login, o app chama `supabase.auth.sign_in_with_password`.
6. Depois do login, o app consulta a tabela `profiles` usando o `id` do usuario autenticado.
7. Os dados principais do usuario sao salvos na sessao:
   - `usuario_id`
   - `usuario_email`
   - `usuario_nome`
   - `tipo_usuario`
8. A interface renderiza a area correta de acordo com `tipo_usuario`.

## Configuracao do ambiente

### 1. Criar e ativar ambiente virtual

```bash
python -m venv venv
```

No Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar secrets do Streamlit

Crie ou edite o arquivo `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://seu-projeto.supabase.co"
SUPABASE_ANON_KEY = "sua-chave-anon"
```

Nao publique esse arquivo com credenciais reais. Em ambientes de deploy, configure esses valores nos secrets da plataforma.

### 4. Executar o app

```bash
streamlit run streamlit_app.py
```

## Configuracao esperada no Supabase

O app espera que exista uma tabela `profiles` relacionada aos usuarios autenticados.

Modelo minimo esperado:

| Campo | Tipo sugerido | Descricao |
| --- | --- | --- |
| `id` | `uuid` | Mesmo ID do usuario em `auth.users` |
| `nome` | `text` | Nome exibido na aplicacao |
| `tipo` | `text` | Tipo do usuario, por exemplo `Admin` ou `Usuario` |

Exemplo de SQL para uma estrutura inicial:

```sql
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  nome text not null,
  tipo text not null default 'Usuario',
  created_at timestamp with time zone default now()
);
```

Para que o perfil seja criado automaticamente apos o cadastro, recomenda-se criar uma trigger em `auth.users` que copie o nome enviado nos metadados do usuario.

Exemplo:

```sql
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
as $$
begin
  insert into public.profiles (id, nome, tipo)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'nome', 'Usuario'),
    'Usuario'
  );

  return new;
end;
$$;

create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();
```

## Arquivo principal

### `streamlit_app.py`

Contem toda a aplicacao Streamlit:

- conexao com Supabase;
- formulario de login;
- formulario de cadastro;
- consulta de perfil;
- gerenciamento de sessao;
- renderizacao condicional para admin e usuario comum.

## Variaveis de sessao

O app usa `st.session_state` para manter o usuario autenticado durante a sessao atual do Streamlit.

| Chave | Finalidade |
| --- | --- |
| `usuario_id` | Identificador do usuario autenticado |
| `usuario_email` | E-mail do usuario |
| `usuario_nome` | Nome vindo da tabela `profiles` |
| `tipo_usuario` | Perfil de permissao do usuario |

## Melhorias recomendadas

- Adicionar botao de logout.
- Tratar erros de login, cadastro e consulta de perfil.
- Validar campos vazios antes de enviar dados ao Supabase.
- Implementar CRUD real de obras para administradores.
- Criar tabelas para obras, avaliacoes, comentarios e listas.
- Adicionar politicas de Row Level Security no Supabase.
- Separar o app em modulos conforme crescer:
  - `auth.py`
  - `database.py`
  - `pages/admin.py`
  - `pages/user.py`
- Corrigir a codificacao dos textos em `streamlit_app.py`, que atualmente parecem ter sido salvos com caracteres quebrados.

## Ideia de evolucao para o modelo de dados

Para aproximar o projeto de uma plataforma de avaliacoes estilo Letterboxd, uma evolucao natural seria:

- `profiles`: dados publicos do usuario.
- `works`: filmes, series ou obras cadastradas.
- `reviews`: avaliacoes textuais e notas.
- `watchlist`: obras que o usuario quer assistir.
- `likes`: curtidas em avaliacoes.
- `comments`: comentarios em avaliacoes.

## Licenca

Defina uma licenca antes de publicar o projeto.
