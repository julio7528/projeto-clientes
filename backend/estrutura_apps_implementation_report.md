# Relatório de Implementação da Estrutura Modular das Apps

## Identificação

- Projeto: `PC-DJANGO-001`
- Etapa: Fase 2.2 — organização modular de `config`, `core`, `usuarios` e `clientes`
- Data: 22/07/2026
- Resultado: implementação concluída sem alteração de schema remoto

## 1. Subetapas concluídas

1. Auditoria de `AGENTS.md`, README, Blueprint relacionado, especificação aprovada,
   skill modular, relatórios anteriores, migrations, Git, settings, URLs, imports,
   testes e código de `config` e `usuarios`.
2. Criação de `core` como app Django independente de domínio.
3. Criação de `clientes` com estrutura mínima para a próxima fase.
4. Registro explícito de `CoreConfig` e `ClientesConfig` em `INSTALLED_APPS`.
5. Preservação de `usuarios`, `AUTH_USER_MODEL`, rotas, Admin e permissões.
6. Preservação de `ProtectedFile`, tabela, migrations, ownership e Storage privado.
7. Revisão automatizada dos limites de imports entre as apps.
8. Inclusão de testes estruturais, de migrations, URLs e isolamento de segredos.
9. Atualização do README com a arquitetura modular final desta etapa.
10. Execução dos checks e das suítes segmentada e completa.

## 2. Estado auditado e baseline

O estado inicial correspondia à especificação: `usuarios.Usuario` já era o modelo
customizado, `AUTH_USER_MODEL` estava configurado, `ProtectedFile` permanecia em
`config`, e havia 35 testes de autenticação e infraestrutura.

O Git já continha, antes desta implementação, dois arquivos não rastreados:

- `.skills/skill_estrutura_modular_apps_django_pc_django_001.md`;
- `.specs/especificacao_estrutura_apps_pc_django_001.md`.

Eles foram usados como fonte e não foram alterados. Nenhum arquivo de `Blueprint/`
foi modificado.

Baseline executado:

- `python backend/manage.py test`: falhou antes do Django com
  `ModuleNotFoundError: No module named 'django'`, pois o Python global não usa a
  virtualenv;
- `.\.venv\Scripts\python.exe backend\manage.py test`: encontrou 0 testes quando
  executado sem labels a partir da raiz;
- `.\.venv\Scripts\python.exe backend\manage.py test usuarios config`: 35 testes,
  resultado `OK`.

## 3. Apps criadas

### `core`

Responsabilidade: componentes compartilhados e independentes de domínio.

Conteúdo implementado:

- `CoreConfig`;
- `UUIDTimestampedModel`, abstrato, com UUID, `criado_em` e `atualizado_em`;
- `normalize_digits()` para valores textuais opcionais;
- `normalize_whitespace()` para remoção e redução genérica de whitespace;
- testes próprios;
- pacote de migrations sem migration concreta.

O normalizador de dígitos passou a ser reutilizado por `usuarios.validators`, sem
alterar a API do módulo, a validação de CPF ou a migration existente.

### `clientes`

Responsabilidade: limite do futuro domínio de clientes PF/PJ.

Conteúdo implementado:

- `ClientesConfig`;
- módulo `models` sem modelo concreto;
- URLconf com `app_name = "clientes"` e sem rotas;
- testes estruturais e arquiteturais;
- pacote de migrations sem migration concreta.

Não foram criados `Cliente`, CRUD, choices, validações de CPF/CNPJ, pesquisa,
dashboard, relatórios, exportações, CEP, uploads ou vínculos com arquivos. O URLconf
não foi incluído em `config.urls`, porque ainda não existe rota real.

## 4. Decisões arquiteturais

- `core` não depende de `config`, `usuarios` ou `clientes`.
- `usuarios` depende somente do normalizador genérico de `core` e não depende de
  `clientes`.
- O código de produção de `clientes` não depende de `config` nem importa
  `usuarios.Usuario` diretamente.
- Relações futuras com usuários deverão usar `settings.AUTH_USER_MODEL`; obtenção em
  runtime deverá usar `get_user_model()`.
- Helpers de ownership permanecem em `usuarios.permissions`, pois movê-los não é
  necessário nesta etapa.
- `ProtectedFile` permanece como dívida técnica controlada em `config`.
- A decisão sobre uma futura app `arquivos` permanece adiada.
- Nenhum framework ou dependência foi adicionado.

## 5. Preservação de autenticação e Supabase

Permaneceram inalterados:

- `AUTH_USER_MODEL = "usuarios.Usuario"`;
- login por e-mail, logout POST, perfil e troca de senha;
- restrições do Django Admin;
- permissões e bypass administrativo explícito;
- classe e tabela `config.ProtectedFile`;
- migrations `config/0001`, `config/0002` e `usuarios/0001`;
- `ForeignKey` de owner com `PROTECT`;
- endpoint de URL privada e validação de ownership;
- integração backend-only e redaction de segredos.

Não houve consulta SQL, alteração de schema, chamada de Storage real ou aplicação
de migration no Supabase. As mudanças recentes do Data API do Supabase não afetam
esta etapa, pois nenhuma tabela foi criada e o acesso ORM continua por conexão
PostgreSQL direta.

## 6. Arquivos alterados e criados

Alterados:

- `README.md`;
- `backend/config/settings.py`;
- `backend/usuarios/validators.py`.

Criados:

- `backend/core/__init__.py`;
- `backend/core/apps.py`;
- `backend/core/models.py`;
- `backend/core/normalizers.py`;
- `backend/core/migrations/__init__.py`;
- `backend/core/tests/__init__.py`;
- `backend/core/tests/test_models.py`;
- `backend/clientes/__init__.py`;
- `backend/clientes/apps.py`;
- `backend/clientes/models.py`;
- `backend/clientes/urls.py`;
- `backend/clientes/migrations/__init__.py`;
- `backend/clientes/tests/__init__.py`;
- `backend/clientes/tests/test_app_structure.py`;
- `backend/estrutura_apps_implementation_report.md`.

## 7. Migrations

- `core`: nenhuma migration concreta e nenhuma tabela.
- `clientes`: nenhuma migration concreta e nenhuma tabela.
- `usuarios`: migrations existentes não alteradas.
- `config`: migrations existentes e tabela de `ProtectedFile` não alteradas.
- Banco remoto: nenhuma migration aplicada.

Resultado de `.\.venv\Scripts\python.exe backend\manage.py makemigrations --check --dry-run`:

```text
No changes detected
```

## 8. Testes e comandos finais

### Check do Django

Comando:

```powershell
.\.venv\Scripts\python.exe backend\manage.py check
```

Resultado:

```text
System check identified no issues (0 silenced).
```

### Testes novos isolados

Comando:

```powershell
.\.venv\Scripts\python.exe backend\manage.py test core clientes
```

Resultado: 11 testes, `OK`.

### Suíte solicitada

Comando:

```powershell
.\.venv\Scripts\python.exe backend\manage.py test usuarios config core clientes
```

Resultado: 46 testes em 67,120 segundos, `OK`.

### Suíte Django completa

Comando executado a partir de `backend/` para garantir descoberta sem labels:

```powershell
..\.venv\Scripts\python.exe manage.py test
```

Resultado: 46 testes em 60,488 segundos, `OK`.

### Revisão final

- `git diff --check`: sucesso, sem erro de whitespace;
- `makemigrations --check --dry-run`: nenhuma mudança;
- nenhuma app `arquivos` encontrada;
- somente `__init__.py` nos novos pacotes de migrations;
- nenhum Blueprint alterado;
- nenhum segredo adicionado ao diff;
- nenhum commit ou push realizado.

## 9. Riscos, limitações e bloqueadores

Bloqueadores da etapa: nenhum.

Riscos e limitações restantes:

1. o comando `python` global não aponta para a virtualenv; os comandos devem ser
   executados após ativá-la ou com o executável explícito;
2. a descoberta sem labels a partir da raiz retorna 0 testes; a suíte completa deve
   ser executada a partir de `backend/` ou com labels explícitos;
3. `ProtectedFile` permanece em `config` como dívida técnica deliberada;
4. as migrations existentes ainda exigem aplicação remota futura, em janela
   controlada e ambiente explicitamente escolhido;
5. rate limiting e a decisão definitiva sobre o ciclo de vida de arquivos continuam
   fora desta etapa.

## 10. Próxima fase recomendada

Fase 2.3 — implementar o modelo definitivo `Cliente` conforme o Blueprint, incluindo
choices, UUID, campos PF/PJ, normalização, validações, autoria com
`settings.AUTH_USER_MODEL`, índices, constraints, Admin, migration revisada e testes.

## 11. Veredito

`READY WITH RESERVATIONS`

A estrutura modular está pronta. As reservas são operacionais e documentadas: uso
obrigatório da virtualenv, descoberta de testes dependente do diretório e aplicação
remota de migrations ainda pendente em etapa separada.
