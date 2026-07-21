# Auditoria tecnica - PC-DJANGO-001

## Resumo executivo

Fato verificado: o bootstrap Django existe em `backend/`, usa `python-decouple`, `dj-database-url`, `psycopg` e carrega `DATABASE_URL` para PostgreSQL. O comando `python backend/manage.py check` concluiu sem problemas.

Fato verificado: a conexao sanitizada via `connection.ensure_connection()` alcancou o host do Supabase Session Pooler, mas falhou por autenticacao do usuario do banco. Portanto, a configuracao ainda nao comprova uma conexao PostgreSQL funcional.

Conclusao executiva: **NAO PRONTO**.

## Escopo

Auditoria read-only do repositorio local, incluindo estrutura, Git, arquivos ignorados, ambiente Python, dependencias, bootstrap Django, carregamento de ambiente, seguranca de `.env`, configuracao PostgreSQL/Supabase, SSL, porta 5432, host de Session Pooler, documentacao e consistencia com README, AGENTS e Blueprint.

Restricoes respeitadas: nao foram feitas alteracoes em codigo, instalacao de pacotes, migrations, criacao de apps, commits, push ou alteracao de banco. Foi criado somente este `report.md`.

## Estrutura encontrada

Fatos verificados:

- Raiz Git: `H:\Dev Front End\CadastroDjango`.
- Diretório Django: `backend/`.
- Encontrados: `.git/`, `.venv/`, `backend/`, `Blueprint/`, `frontend/`, `infrastructure/`, `media/`, `requirements/`, `scripts/`, `static/`, `tests/`, `.gitignore`, `AGENTS.md`, `README.md`.
- Em `backend/`: `manage.py`, `config/`, `.env`, `db.sqlite3`.
- Em `backend/config/`: `settings.py`, `urls.py`, `asgi.py`, `wsgi.py`, `__init__.py`.
- Blueprint encontrado com arquivos de overview, requisitos, modelagem e UI/UX, alem de pastas adicionais `04-implementacao`, `05-testes` e `06-deploy`.

Lacunas verificadas:

- `.env.example` nao existe na raiz nem em `backend/`.
- `pyproject.toml` nao existe.
- `backend/apps/`, `backend/templates/`, `backend/static/` e `backend/media/` ainda nao existem.
- Existe `frontend/`, enquanto AGENTS indica que frontend separado em React/Next esta fora do escopo sem decisao explicita. Nao foi verificado conteudo relevante nessa pasta.

## Verificações executadas

Fatos verificados:

- `git status --short --branch`.
- `git status --ignored --short`.
- `git ls-files`.
- Listagem de estrutura ate profundidade limitada.
- Leitura de `README.md`, `AGENTS.md`, `.gitignore`, `requirements/base.txt`, `backend/manage.py` e `backend/config/settings.py`.
- Leitura dos nomes das variaveis presentes em `backend/.env`, sem exibir valores.
- `H:\Dev Front End\CadastroDjango\.venv\Scripts\python.exe --version`.
- `python -m pip freeze` dentro da `.venv`.
- `python backend/manage.py check`.
- Inspecao sanitizada de `settings.DATABASES["default"]`.
- Teste de conexao sanitizado com `connection.ensure_connection()`.

## Git e segurança

Fatos verificados:

- Branch atual: `main`, acompanhando `origin/main`.
- Worktree nao esta limpo:
  - `backend/config/settings.py` modificado.
  - `requirements/` nao rastreado.
- Ignorados corretamente:
  - `.venv/`.
  - `backend/.env`.
  - `backend/config/__pycache__/`.
  - `backend/db.sqlite3`.
- Arquivos rastreados nao incluem `.env`.
- `.gitignore` contem regras para `.env`, `.env.*`, `.venv/`, caches Python, `db.sqlite3`, logs e artefatos comuns.
- `backend/.env` contem as chaves `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` e `DATABASE_URL`. Valores nao foram exibidos.

Recomendacao: antes da proxima fase, revisar e versionar apenas arquivos intencionais, mantendo `backend/.env` fora do Git.

## Ambiente Python e dependências

Fatos verificados:

- Python da `.venv`: `Python 3.14.2`.
- Pacotes instalados:
  - `Django==6.0.7`
  - `dj-database-url==3.1.2`
  - `psycopg==3.3.4`
  - `psycopg-binary==3.3.4`
  - `python-decouple==3.8`
  - `asgiref==3.11.1`
  - `sqlparse==0.5.5`
  - `tzdata==2026.3`
- `requirements/base.txt` existe e corresponde ao `pip freeze` observado.

Lacunas verificadas:

- `requirements/` esta nao rastreado no Git.
- Nao existem `requirements/development.txt` ou outros arquivos por ambiente.
- Nao existe `pyproject.toml`, embora README e AGENTS o prevejam na estrutura esperada.

## Configuração Django

Fatos verificados:

- `manage.py` define `DJANGO_SETTINGS_MODULE` como `config.settings`.
- `settings.py` importa `dj_database_url` e `config` de `decouple`.
- `SECRET_KEY` e carregado de `DJANGO_SECRET_KEY`.
- `DEBUG` e carregado de `DJANGO_DEBUG` com `cast=bool`.
- Valor efetivo verificado: `DEBUG=True`.
- `ALLOWED_HOSTS=[]` esta fixo no codigo.
- `INSTALLED_APPS` contem somente apps padrao do Django.
- `python backend/manage.py check` retornou: `System check identified no issues (0 silenced).`

Recomendacao: tornar `ALLOWED_HOSTS` configuravel por ambiente antes de ambientes QA/producao.

## Conexão PostgreSQL/Supabase

Fatos verificados, sanitizados:

- Engine Django efetiva: `django.db.backends.postgresql`.
- `DATABASE_URL` e carregada pelo `dj_database_url.config`.
- `conn_max_age=60`.
- `conn_health_checks=True`.
- `ssl_require=True`.
- SSL efetivo: `sslmode=require`.
- Host efetivo: `aws-0-ca-central-1.pooler.supabase.com`.
- Porta efetiva: `5432`.
- Nome do banco e usuario estao presentes, mas foram sanitizados.
- O host contem `pooler.supabase.com`, consistente com uso do Session Pooler.
- `connection.ensure_connection()` alcancou o servidor, mas falhou com `OperationalError` por autenticacao: mensagem sanitizada indica `password authentication failed for user "postgres"`.

Interpretacao: a rede e o host do pooler parecem alcancaveis, mas as credenciais ou o usuario configurado em `DATABASE_URL` nao estao validos para abrir conexao.

## Documentação e Blueprint

Fatos verificados:

- README define o projeto como Django com PostgreSQL no Supabase.
- AGENTS define Blueprint como fonte de verdade e exige uso de variaveis de ambiente.
- Blueprint possui documentos de planejamento, requisitos, modelagem e UI/UX.
- README afirma que setup tecnico e a proxima etapa.
- A implementacao atual esta coerente com inicio de setup tecnico, mas ainda incompleta para passar para autenticacao/modelo Cliente.

Inconsistencias verificadas:

- README e AGENTS preveem `.env.example`; arquivo ausente.
- README e AGENTS preveem `pyproject.toml`; arquivo ausente.
- AGENTS preve `staticfiles/`, mas a raiz contem `static/`.
- README lista `frontend/`, enquanto AGENTS alerta que frontend separado esta fora do escopo sem decisao explicita.
- README e AGENTS aparecem com caracteres acentuados corrompidos na leitura do terminal, sugerindo possivel problema de encoding ou renderizacao do console.

## Problemas encontrados

### Bloqueadores

1. Conexao PostgreSQL/Supabase nao validada: `connection.ensure_connection()` falhou por autenticacao do banco, apesar de host, SSL e porta estarem configurados.
2. `.env.example` ausente: nao ha template versionavel para documentar `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` e `DATABASE_URL` com placeholders seguros.

### Importantes

1. `ALLOWED_HOSTS` esta fixo como lista vazia e nao usa variavel de ambiente, apesar de README/AGENTS preverem `DJANGO_ALLOWED_HOSTS`.
2. `requirements/` esta nao rastreado no Git, incluindo `requirements/base.txt`.
3. Worktree possui alteracao nao commitada em `backend/config/settings.py`; a auditoria confirma o estado local, mas ainda nao ha baseline limpo.
4. `pyproject.toml` ausente, embora esteja previsto na estrutura documentada.
5. `backend/db.sqlite3` existe no projeto local, ainda que ignorado; isso pode confundir a verificacao do uso exclusivo de PostgreSQL durante o setup.

### Melhorias recomendadas

1. Adicionar `.env.example` com placeholders sem segredos.
2. Ler `DJANGO_ALLOWED_HOSTS` por ambiente, mantendo padrao seguro.
3. Criar arquivos de requirements por ambiente quando a estrategia for definida.
4. Remover ou arquivar o `db.sqlite3` local somente quando confirmado que nao contem dado necessario.
5. Corrigir ou padronizar encoding dos arquivos Markdown caso a corrupcao de acentos tambem ocorra fora do terminal.
6. Decidir se `frontend/` faz parte do escopo ou se deve permanecer vazio/fora da implementacao.
7. Validar credenciais do Supabase Session Pooler no `.env` local, sem registrar valores em Git ou logs.

## Checklist de prontidão

- Estrutura base Django presente: OK.
- `.venv` local presente: OK.
- Dependencias principais instaladas: OK.
- `requirements/base.txt` presente: OK, mas nao rastreado.
- `manage.py check`: OK.
- `SECRET_KEY` fora do codigo: OK.
- `.env` ignorado pelo Git: OK.
- `.env.example` versionavel: FALHA.
- `DEBUG` via ambiente: OK; valor atual e desenvolvimento.
- `ALLOWED_HOSTS` via ambiente: FALHA.
- Banco configurado como PostgreSQL: OK.
- Uso de Supabase Session Pooler: OK pelo host efetivo.
- Porta 5432: OK.
- SSL requerido: OK.
- Conexao real com PostgreSQL: FALHA.
- Git limpo: FALHA.
- Documentacao consistente com implementacao: PARCIAL.

## Conclusão

NAO PRONTO

## Próxima etapa recomendada

Corrigir a configuracao local de `DATABASE_URL` para autenticar no Supabase Session Pooler e criar `.env.example` seguro. Depois, repetir `python backend/manage.py check` e `connection.ensure_connection()` antes de avancar para configuracao de ambientes/autenticacao.
