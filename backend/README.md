# PC-DJANGO-001 Backend

Backend Django para gerenciamento de clientes usando PostgreSQL hospedado no Supabase.

## Arquitetura

Fluxo permitido:

```text
Browser -> Django -> Supabase
```

O navegador deve se comunicar somente com o Django. Chamadas diretas do browser para Supabase, Supabase Storage, Data API, Auth API ou Realtime ficam fora da arquitetura atual.

## Regras de Segurança

- `DATABASE_URL`, credenciais de banco e `SUPABASE_SECRET_KEY` ficam apenas no backend.
- `SUPABASE_SECRET_KEY` nunca deve aparecer em templates, bundles frontend, respostas JSON, logs ou requests do navegador.
- `SUPABASE_PUBLISHABLE_KEY` também permanece server-side neste projeto, mesmo sendo uma chave publicavel.
- Operações normais de banco devem usar Django ORM via `DATABASE_URL`.
- APIs administrativas do Supabase e Storage privado devem passar por funcoes server-side em `config/supabase.py`.
- Autenticacao do navegador usa sessoes seguras do Django.
- Tokens nao devem ser armazenados em `localStorage`.
- Realtime esta fora de escopo.
- URLs assinadas de Storage devem usar TTL curto. O padrao atual e 60 segundos.

## Variaveis de Ambiente

Use `.env` local e mantenha esse arquivo fora do Git. O modelo seguro esta em `.env.example`.

Variaveis obrigatorias:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_PUBLISHABLE_KEY`
- `SUPABASE_SECRET_KEY`

Variaveis opcionais:

- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_SESSION_COOKIE_SECURE`
- `DJANGO_CSRF_COOKIE_SECURE`
- `DJANGO_SECURE_SSL_REDIRECT`
- `DJANGO_SECURE_HSTS_SECONDS`
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `DJANGO_SECURE_HSTS_PRELOAD`
- `SUPABASE_PRIVATE_STORAGE_BUCKET`
- `SUPABASE_SIGNED_URL_TTL_SECONDS`

## Endpoints de Exemplo

- `GET /api/protected/profile/`: endpoint autenticado que retorna dados basicos do usuario Django.
- `POST /api/storage/private-url/`: endpoint autenticado que cria URL assinada curta para objeto privado no Supabase Storage.

Esses endpoints nao retornam chaves Supabase nem credenciais de banco.

## Verificacao

```powershell
python manage.py check
python manage.py test config
```
