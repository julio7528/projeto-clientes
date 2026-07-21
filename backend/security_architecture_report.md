# Relatorio de Arquitetura de Seguranca

## Resumo

A integracao Supabase foi isolada no backend. O navegador usa apenas endpoints Django autenticados, enquanto o Django atua como gateway de aplicacao e camada de autorizacao.

Fluxo permitido:

```text
Browser -> Django -> Supabase
```

## Arquivos Alterados

- `.gitignore`
- `.env.example`
- `README.md`
- `config/env.py`
- `config/logging.py`
- `config/settings.py`
- `config/supabase.py`
- `config/tests.py`
- `config/urls.py`
- `config/views.py`
- `security_architecture_report.md`

## Controles Implementados

- Carregamento centralizado de variaveis em `config/env.py`.
- Validacao de variaveis obrigatorias sem imprimir valores secretos.
- `.env.example` com placeholders, sem credenciais reais.
- `.gitignore` garantindo que `.env` fique fora do Git.
- `SUPABASE_SECRET_KEY` isolada em configuracao e camada de servico backend-only.
- Operacoes normais de banco mantidas no Django ORM via `DATABASE_URL`.
- Cliente administrativo minimo de Supabase Storage em `config/supabase.py`.
- Endpoint autenticado para perfil protegido em `config/views.py`.
- Endpoint autenticado para URL assinada curta de Storage privado.
- Cookies HTTP-only, SameSite, Secure configuravel, HSTS, X-Frame-Options e content-type nosniff.
- Filtro de logging para redigir valores sensiveis antes de escrita em handlers.
- Testes cobrindo rejeicao de acesso anonimo e ausencia de segredos em respostas.
- Teste para impedir referencias a chaves Supabase em templates e arquivos frontend.

## Variaveis Obrigatorias

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_PUBLISHABLE_KEY`
- `SUPABASE_SECRET_KEY`

## Variaveis Opcionais

- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_SESSION_COOKIE_SECURE`
- `DJANGO_CSRF_COOKIE_SECURE`
- `DJANGO_SECURE_SSL_REDIRECT`
- `DJANGO_SECURE_HSTS_SECONDS`
- `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `DJANGO_SECURE_HSTS_PRELOAD`
- `SUPABASE_PRIVATE_STORAGE_BUCKET`
- `SUPABASE_SIGNED_URL_TTL_SECONDS`

## Riscos Restantes

- O `.env` atual deve usar uma `DJANGO_SECRET_KEY` propria do Django, diferente de qualquer chave Supabase.
- As chaves e credenciais ja vistas no ambiente local devem ser rotacionadas se foram compartilhadas fora da maquina.
- `DJANGO_ALLOWED_HOSTS` e `DJANGO_CSRF_TRUSTED_ORIGINS` precisam ser definidos com os dominios reais antes de producao.
- O bucket privado do Supabase precisa existir e suas politicas devem refletir o modelo de autorizacao do Django.
- URLs assinadas continuam validas ate expirar; manter TTL baixo e evitar cache em clientes.

## Testes Executados

- `python manage.py check`
- `python manage.py test config`

## Proximos Passos

- Rotacionar segredos se houve exposicao.
- Configurar dominios reais em `DJANGO_ALLOWED_HOSTS` e `DJANGO_CSRF_TRUSTED_ORIGINS`.
- Criar modelos Django reais para clientes e manter CRUD via ORM.
- Mapear autorizacao por usuario antes de liberar arquivos privados do Storage.
