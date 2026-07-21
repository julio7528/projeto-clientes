# Relatorio de Arquitetura de Seguranca

## Resumo

Fluxo permitido: `Browser -> Django -> Supabase`. O endpoint de Storage aceita somente UUID interno, resolve o caminho pelo ORM e valida ownership antes de usar a chave privilegiada.

## Arquivos Alterados

- `.env.example`
- `.gitignore`
- `README.md`
- `config/env.py`
- `config/logging.py`
- `config/models.py`
- `config/migrations/0001_initial.py`
- `config/settings.py`
- `config/supabase.py`
- `config/tests.py`
- `config/urls.py`
- `config/views.py`
- `security_architecture_report.md`

## Controles

- `ProtectedFile` usa UUID, owner, caminho interno, nome e timestamp.
- Browser envia `arquivo_id`; caminhos fornecidos pelo cliente nao participam da assinatura.
- Ownership e validado antes da chamada privilegiada; acesso cruzado retorna 403 e UUID inexistente retorna 404.
- TTL solicitado e limitado por `SUPABASE_SIGNED_URL_TTL_SECONDS`.
- Respostas de Storage usam `no-store, private` e `no-cache`.
- Corpo possui limite; JSON, UUID, metodo e tipos sao validados.
- Erros Supabase e de banco nao sao devolvidos ao cliente.
- Filtro de logging redige segredos, Bearer/apikey, URLs de banco e URLs assinadas; o codigo nao registra body ou headers.
- Chave publishable e opcional, backend-only e atualmente sem uso.
- Cookies, HTTPS e HSTS usam defaults seguros por ambiente.
- `X-Forwarded-Proto` so e confiado por configuracao explicita.
- `.env` continua ignorado e `.env.example` possui somente placeholders.

## Variaveis

Obrigatorias: `DJANGO_SECRET_KEY`, `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_SECRET_KEY`.

Opcionais: `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, `DJANGO_SESSION_COOKIE_SECURE`, `DJANGO_CSRF_COOKIE_SECURE`, `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_TRUST_X_FORWARDED_PROTO`, `DJANGO_SECURE_HSTS_SECONDS`, `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`, `DJANGO_SECURE_HSTS_PRELOAD`, `SUPABASE_PUBLISHABLE_KEY`, `SUPABASE_PRIVATE_STORAGE_BUCKET`, `SUPABASE_SIGNED_URL_TTL_SECONDS`, `PRIVATE_STORAGE_REQUEST_MAX_BYTES`.

## Ambientes

- Local HTTP: `DJANGO_DEBUG=True`; cookies Secure, redirect SSL e HSTS ficam desativados por default.
- Producao HTTPS: `DJANGO_DEBUG=False`; cookies Secure, redirect HTTPS e HSTS ficam ativos por default.
- Proxy: habilitar `DJANGO_TRUST_X_FORWARDED_PROTO=True` apenas se um proxy controlado sobrescrever o header recebido do cliente.

## Migracao

- `config/migrations/0001_initial.py` cria `ProtectedFile`.
- Nao foi aplicada ao PostgreSQL Supabase.
- `test` e `makemigrations` usam SQLite em memoria para nao consultar o banco remoto.

## Riscos Restantes

- `DJANGO_SECRET_KEY` deve ser exclusiva do Django e diferente das chaves Supabase.
- Chaves previamente compartilhadas devem ser rotacionadas.
- A chave secreta ignora RLS; a checagem Django e um controle critico.
- URLs assinadas continuam validas ate expirar e aparecem no Network por necessidade funcional; nao registrar responses em analytics ou proxies.
- O modelo atual autoriza apenas owner. Compartilhamento exige relacao explicita de usuarios autorizados.
- Rate limiting depende da infraestrutura de deploy e ainda nao foi implementado.

## Comandos Executados

- `python backend/manage.py check`: sucesso, 0 issues.
- `python backend/manage.py makemigrations --check --dry-run`: sucesso, nenhuma mudanca detectada.
- `python backend/manage.py test config`: sucesso, 16 testes aprovados.

## Proximos Passos

- Revisar e aplicar a migracao em janela controlada no ambiente correto.
- Configurar hosts, origens, proxy e HTTPS reais de producao.
- Adicionar rate limiting conforme a infraestrutura escolhida.
- Modelar compartilhamento explicito se necessario.
