# Critica

Aplicação web em Streamlit para autenticação e catálogo de obras audiovisuais, inspirada na experiência do Letterboxd. O projeto usa **Streamlit** na interface, **Supabase Auth** para login e cadastro, **Supabase Database** para perfis e obras, e **Supabase Storage** para capas das obras.

## Stack

- Python
- [Streamlit](https://streamlit.io/)
- [Supabase](https://supabase.com/) (Auth, Database, Storage)

## Funcionalidades

### Visitante (não logado)

- Cadastro com e-mail, senha e nome
- Login com e-mail e senha

### Usuário logado (todos)

- Exibição dos dados da sessão (nome, e-mail, tipo)
- Botão **Sair da conta** (encerra sessão no Supabase e limpa o `session_state`)

### Administrador (`tipo` = `Admin`)

- Criar obra com título, descrição, nota (0–5) e imagem de capa (JPG/PNG)
- Upload da capa para o bucket `obras` em `capas/`
- Navegação para a tela **Remover obras**, com listagem e exclusão (banco + storage)

### Usuário padrão

- Visualizar o catálogo de obras com capa, nota, autor e descrição

## Estrutura do projeto

```text
Critica/
├── .streamlit/
│   └── secrets.toml      # credenciais (não versionar)
├── .gitignore
├── README.md
├── requirements.txt
└── streamlit_app.py      # aplicação principal
```

## Como executar

### 1. Ambiente virtual

```bash
python -m venv venv
```

No Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Dependências

```bash
pip install -r requirements.txt
```

### 3. Secrets do Streamlit

Crie `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://seu-projeto.supabase.co"
SUPABASE_ANON_KEY = "sua-chave-anon"
```

Não commite credenciais reais. Em deploy, use os secrets da plataforma (Streamlit Cloud, etc.).

### 4. Rodar o app

```bash
streamlit run streamlit_app.py
```

## Configuração no Supabase

### Tabela `profiles`

Vinculada ao usuário autenticado (`auth.users`).

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `id` | `uuid` | Mesmo ID de `auth.users` |
| `nome` | `text` | Nome exibido no app |
| `tipo` | `text` | `Admin` ou outro valor para usuário comum |

Exemplo de criação e trigger para perfil automático no cadastro:

```sql
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  nome text not null,
  tipo text not null default 'Usuario',
  created_at timestamptz default now()
);

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

Para ter um administrador, atualize manualmente o campo `tipo` na tabela `profiles` para `Admin`.

### Tabela `obras`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `id` | `uuid` | Chave primária (default `gen_random_uuid()`) |
| `titulo` | `text` | Título da obra |
| `descricao` | `text` | Sinopse ou descrição |
| `nota` | `numeric` | Nota de 0 a 5 |
| `imagem_url` | `text` | URL pública da capa no Storage |
| `usuario_id` | `uuid` | ID do admin que publicou |
| `nome_usuario` | `text` | Nome do autor da publicação |

Exemplo:

```sql
create table public.obras (
  id uuid primary key default gen_random_uuid(),
  titulo text not null,
  descricao text,
  nota numeric not null check (nota >= 0 and nota <= 5),
  imagem_url text,
  usuario_id uuid references auth.users(id),
  nome_usuario text,
  created_at timestamptz default now()
);
```

### Storage

- Crie um bucket público chamado **`obras`**
- As capas são salvas em `capas/<nome-do-arquivo>`
- Configure políticas de leitura/escrita conforme o nível de segurança desejado (RLS no Storage e permissões para usuários autenticados)

A exclusão de obras no app remove o arquivo em `capas/` quando a `imagem_url` segue o padrão `.../object/public/obras/capas/...`.

## Fluxo da aplicação

1. Carrega `SUPABASE_URL` e `SUPABASE_ANON_KEY` de `st.secrets`
2. Se não houver `usuario_id` na sessão → tela de login ou cadastro
3. Após login → consulta `profiles` e preenche a sessão
4. Renderiza a área conforme `tipo_usuario`:
   - **Admin**: formulário de criação na página principal; botão **Remover obras** abre a tela de exclusão
   - **Demais usuários**: listagem do catálogo em `obras`

## Variáveis de sessão (`st.session_state`)

| Chave | Finalidade |
| --- | --- |
| `usuario_id` | ID do usuário autenticado |
| `usuario_email` | E-mail |
| `usuario_nome` | Nome em `profiles` |
| `tipo_usuario` | Perfil (`Admin`, etc.) |
| `pagina_admin` | Navegação interna do admin: `principal` ou `remover` |

## Dependências

```text
streamlit
supabase
```

## Próximos passos

- Edição de obras existentes
- Avaliações e comentários por usuário (estilo Letterboxd)
- Row Level Security (RLS) em `profiles` e `obras`
- Validação de formulários e mensagens de erro mais claras
- Separar o código em módulos (`auth.py`, `obras.py`, páginas Streamlit)
