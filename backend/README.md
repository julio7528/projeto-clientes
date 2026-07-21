# PC-DJANGO-001 Backend

Backend Django para gerenciamento de clientes com PostgreSQL e Storage no Supabase.

## Arquitetura

```text
Browser -> Django -> Supabase
```

O navegador se comunica somente com Django. Banco usa Django ORM; Storage privado e APIs privilegiadas passam por funcoes server-side em `config/supabase.py`. A autenticacao usa sessoes Django seguras. Nao ha cliente Supabase no browser, tokens em `localStorage` ou Realtime.

## Autorizacao de Storage

`POST /api/storage/private-url/` recebe:

```json
{"arquivo_id": "<uuid>", "expires_in": 60}
```

O Django busca `ProtectedFile` pelo ORM, compara `owner` com o usuario da sessao e somente depois passa o `storage_path` persistido ao servico Supabase. Caminhos enviados pelo browser sao ignorados. A URL tem TTL limitado pelo backend e a resposta usa `Cache-Control: no-store, private` e `Pragma: no-cache`.

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
python backend/manage.py test config
```

Os comandos `test` e `makemigrations` usam SQLite em memoria e nao acessam o PostgreSQL Supabase.
