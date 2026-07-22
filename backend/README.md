# PC-DJANGO-001 Backend

Backend Django para gerenciamento de clientes com PostgreSQL e Storage no Supabase.

## Arquitetura

```text
Browser -> Django -> Supabase
```

O navegador se comunica somente com Django. Banco usa Django ORM; Storage privado e APIs privilegiadas passam por funcoes server-side em `config/supabase.py`. A autenticacao usa sessoes Django seguras. Nao ha cliente Supabase no browser, tokens em `localStorage` ou Realtime.

## Usuarios e Autenticacao

- Identidade: `usuarios.Usuario`, baseado em `AbstractUser`, com UUID.
- Login: e-mail e senha pelo Django; o campo `username` foi removido.
- Cadastro: exclusivamente pelo Django Admin; nao existe signup publico.
- Administrador: conta individual com `is_staff=True` e `is_superuser=True`.
- Usuario comum: edita somente o proprio perfil e nao acessa o Admin.
- Senhas: hash nativo do Django; troca propria exige senha atual e reset de terceiros ocorre no Admin.
- Fora do escopo: Supabase Auth, OAuth, login social, recuperacao por e-mail e MFA.

Rotas:

- `GET|POST /usuarios/entrar/`: login por e-mail.
- `POST /usuarios/sair/`: logout com CSRF.
- `GET /usuarios/perfil/`: perfil autenticado.
- `GET|POST /usuarios/perfil/<uuid>/editar/`: proprio perfil ou acesso administrativo.
- `GET|POST /usuarios/perfil/senha/`: alteracao da propria senha.

Consultas futuras de dominio devem usar `scope_owned_queryset()` em `usuarios/permissions.py`: administradores recebem o queryset completo e usuarios comuns recebem somente registros do proprio owner.

O destino padrao temporario apos login e `clientes:list`. O parametro `next` e
aceito somente quando aponta para uma URL local segura. Usuario ja autenticado nao
permanece na tela de login; logout continua POST-only com CSRF.

## Clientes

Rotas autenticadas:

- `GET /clientes/` (`clientes:list`);
- `GET|POST /clientes/novo/` (`clientes:create`);
- `GET /clientes/<uuid>/` (`clientes:detail`);
- `GET|POST /clientes/<uuid>/editar/` (`clientes:update`);
- `POST /clientes/<uuid>/ativar/` (`clientes:activate`);
- `POST /clientes/<uuid>/inativar/` (`clientes:deactivate`).

`ClienteForm` usa allowlist de campos e nunca aceita ID, situacao, timestamps ou
autoria. O backend define `criado_por` e `atualizado_por`, executa validacao de
dominio e persiste em `transaction.atomic()`. Mascaras locais sao apenas melhoria
progressiva; CPF/CNPJ, telefone e CEP tambem funcionam sem JavaScript.

Consultas de lista e objeto usam `scope_owned_queryset()` antes do lookup. Usuario
comum recebe 404 ao tentar acessar outro owner; administrador possui escopo global.
Documento e unico e bloqueante. Telefone e e-mail repetidos exigem segundo POST com
token assinado vinculado aos valores normalizados, usuario e registro editado.

Paginas internas retornam `Cache-Control: private, no-store` e `Pragma: no-cache`.
Nao existem delete, consulta externa de CEP, busca avancada ou credenciais Supabase
no frontend.

## Autorizacao de Storage

`POST /api/storage/private-url/` recebe:

```json
{"arquivo_id": "<uuid>", "expires_in": 60}
```

O Django busca `ProtectedFile` pelo ORM, valida owner ou administrador e somente depois passa o `storage_path` persistido ao servico Supabase. Caminhos enviados pelo browser sao ignorados. A URL tem TTL limitado pelo backend e a resposta usa `Cache-Control: no-store, private` e `Pragma: no-cache`. A relacao usa `PROTECT` para impedir exclusao acidental do proprietario com arquivos vinculados.

## Variaveis

Obrigatorias:

- `DJANGO_SECRET_KEY`
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_SECRET_KEY`

Opcionais:

- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_SESSION_COOKIE_SECURE`
- `DJANGO_CSRF_COOKIE_SECURE`
- `DJANGO_SECURE_SSL_REDIRECT`
- `DJANGO_TRUST_X_FORWARDED_PROTO`
- `DJANGO_SECURE_HSTS_SECONDS`
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `DJANGO_SECURE_HSTS_PRELOAD`
- `SUPABASE_PUBLISHABLE_KEY` (backend-only e atualmente sem uso)
- `SUPABASE_PRIVATE_STORAGE_BUCKET`
- `SUPABASE_SIGNED_URL_TTL_SECONDS`
- `PRIVATE_STORAGE_REQUEST_MAX_BYTES`

## Ambientes

Para HTTP local, use `DJANGO_DEBUG=True`. Os defaults desativam cookies Secure, redirect SSL e HSTS. Para producao, use `DJANGO_DEBUG=False`; os defaults ativam cookies Secure, redirect HTTPS e HSTS de um ano.

Defina hosts e origens reais em producao. Use `DJANGO_TRUST_X_FORWARDED_PROTO=True` somente quando um proxy reverso controlado sobrescrever `X-Forwarded-Proto`; a confianca fica desativada por default.

## Endpoints

- `GET /api/protected/profile/`: dados basicos do usuario autenticado.
- `POST /api/storage/private-url/`: URL curta de arquivo privado autorizado.

## Verificacao

Execute a partir da pasta pai do backend:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py test usuarios config
```

Os comandos `test` e `makemigrations` usam SQLite em memoria e nao acessam o PostgreSQL Supabase.

O `db.sqlite3` local antigo possui migrations do usuario padrao e nao deve receber
as migrations atuais. Testes e `makemigrations` usam SQLite em memoria; operacoes
normais usam o PostgreSQL configurado.

## Estado das migrations de desenvolvimento

Em 22/07/2026, as migrations `contenttypes`, `auth`, `usuarios`, `admin`, `clientes`,
`config` e `sessions` foram aplicadas com sucesso ao Supabase de desenvolvimento
confirmado como vazio e descartavel. O plano posterior retornou `No planned
migration operations`; tabelas, constraints, indices, ORM e conexao foram
verificados.

Ainda nao existe superusuario nesse banco. Crie-o apenas de forma interativa:

```powershell
.\.venv\Scripts\python.exe backend\manage.py createsuperuser --email EMAIL_DO_ADMINISTRADOR
```

Nunca inclua a senha no comando.
