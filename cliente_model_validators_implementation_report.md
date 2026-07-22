# Relatório de Implementação — Modelo Cliente e Validadores

## Identificação

- Projeto: `PC-DJANGO-001`
- Etapa: Fase 2.3 — modelo definitivo de Cliente e validadores de domínio
- Data: 22/07/2026
- Resultado: implementação local concluída; nenhuma migration aplicada ao Supabase

## 1. Subetapas concluídas

1. Auditoria de `AGENTS.md`, README, Blueprint, especificação aprovada, skill da
   etapa, relatórios anteriores, `core`, `usuarios`, `clientes`, ownership,
   migrations, settings, testes e estado Git.
2. Execução da linha de base isolada: 46 testes, resultado `OK`.
3. Criação das choices de tipo, situação e das 27 UFs oficiais.
4. Implementação dos validadores puros e reutilizáveis de domínio.
5. Implementação da entidade única `clientes.Cliente` para PF e PJ.
6. Implementação de normalização, `clean()`, `full_clean()` seguro para entradas
   formatadas, normalização em `save()`, ativação e inativação.
7. Configuração de autoria, unicidade global, índices e constraints.
8. Implementação dos alertas não bloqueantes de telefone e e-mail com ownership.
9. Registro seguro no Django Admin, com documento mascarado na listagem.
10. Geração e revisão integral da migration inicial de `clientes`.
11. Inclusão de testes de validadores, modelo, banco, ownership, privacidade,
    alertas e Admin, além da execução das regressões existentes.
12. Atualização do README e criação deste relatório.

## 2. Arquivos alterados e criados

Alterados:

- `README.md`;
- `backend/clientes/models.py`;
- `backend/clientes/tests/test_app_structure.py`.

Criados:

- `backend/clientes/choices.py`;
- `backend/clientes/validators.py`;
- `backend/clientes/services.py`;
- `backend/clientes/admin.py`;
- `backend/clientes/migrations/0001_initial.py`;
- `backend/clientes/tests/test_validators.py`;
- `backend/clientes/tests/test_models.py`;
- `backend/clientes/tests/test_duplicate_warnings.py`;
- `backend/clientes/tests/test_admin.py`;
- `cliente_model_validators_implementation_report.md`.

Os arquivos fornecidos em `.skills/` e `.specs/` foram consultados e não alterados.
Nenhum arquivo em `Blueprint/`, `ProtectedFile`, Storage ou configuração de segredos
foi modificado.

## 3. Choices e validadores

Choices:

- `TipoCliente`: `PF` e `PJ`;
- `SituacaoCliente`: `ATIVO` e `INATIVO`;
- `UnidadeFederativa`: as 27 UFs, com sigla persistida e rótulo em português;
- `UF_CHOICES` e `UF_VALUES` para reutilização imutável.

Validadores:

- `validate_cpf`;
- `validate_cnpj`;
- `validate_documento`;
- `validate_telefone`;
- `validate_cep`;
- `validate_uf`;
- `validate_data_nao_futura`;
- `validate_nome`.

CPF e CNPJ aceitam apresentação formatada, rejeitam letras, tamanho incorreto,
dígitos repetidos e dígitos verificadores inválidos. Os validadores reutilizam
`core.normalize_digits` e `core.normalize_whitespace`.

## 4. Modelo e decisões de domínio

`Cliente` herda de `UUIDTimestampedModel` e contém: `tipo`, `nome`, `documento`,
`data_referencia`, `email`, `telefone`, `cep`, `logradouro`, `numero`,
`complemento`, `bairro`, `cidade`, `estado`, `observacoes`, `situacao`,
`criado_por` e `atualizado_por`, além do UUID e timestamps herdados.

Decisões preservadas:

- PF e PJ compartilham uma tabela;
- documento é normalizado e único globalmente;
- novo cliente inicia ativo;
- endereço e contato principal permanecem integrados;
- e-mail textual opcional usa string vazia, não `NULL`;
- `criado_por` aceita nulo para compatibilidade administrativa, usa `PROTECT` e
  `clientes_criados`;
- `atualizado_por` aceita nulo, usa `SET_NULL` e `clientes_atualizados`;
- `save()` normaliza, mas não substitui `full_clean()`; fluxos futuros devem chamar
  `full_clean()` antes de persistir;
- `ativar()` e `inativar()` são idempotentes e não excluem registros.

## 5. Constraints e índices

Constraints explícitas:

- `clientes_tipo_valido_ck`;
- `clientes_situacao_valida_ck`;
- `clientes_documento_tipo_len_ck`;
- `clientes_telefone_len_ck`;
- `clientes_cep_len_ck`.

O documento utiliza a restrição única nativa do campo. Dígitos verificadores
permanecem no domínio Django, não no banco.

Índices simples existem para nome, telefone, e-mail, tipo e situação por
`db_index=True`; documento recebe índice único. Índices explícitos:

- `clientes_estado_cidade_idx`;
- `clientes_tipo_situacao_idx`;
- `clientes_criado_em_idx`;
- `clientes_atualizado_em_idx`.

## 6. Alertas de duplicidade e privacidade

`collect_duplicate_warnings()` retorna objetos imutáveis `DuplicateWarning` com
`code`, `field`, `message` e contagem limitada ao queryset permitido.

- telefone é comparado somente com dígitos;
- e-mail é comparado em minúsculas e sem espaços externos;
- valores vazios são ignorados;
- o registro atual pode ser excluído durante edição;
- usuário comum consulta somente `criado_por=user` por meio do helper existente;
- administrador `is_staff` + `is_superuser` consulta o conjunto global;
- mensagens são genéricas e não incluem nome, documento, UUID ou proprietário;
- os avisos não fazem parte de `clean()` e não bloqueiam o salvamento.

A unicidade global de documento também usa mensagem genérica. Tratamento de
`IntegrityError` concorrente pertence ao futuro fluxo de cadastro.

## 7. Admin

O Admin permite busca por nome, documento, telefone e e-mail; filtros por tipo,
situação, UF e timestamps; exibe documento mascarado na lista; mantém timestamps e
autoria somente leitura; atribui autoria a partir de `request.user`; chama
`full_clean()` antes de salvar; e oferece ações de ativação/inativação que registram
o atualizador e o horário da atualização.

## 8. Estratégia e revisão da migration

`clientes/migrations/0001_initial.py`:

- cria somente `Cliente`;
- possui `initial = True`;
- usa `migrations.swappable_dependency(settings.AUTH_USER_MODEL)`;
- inclui UUID e timestamps herdados sem criar tabela para `core`;
- configura `criado_por` com `PROTECT`;
- configura `atualizado_por` com `SET_NULL`;
- inclui choices, índices e constraints aprovados;
- não contém `RunSQL`, remoção, alteração destrutiva ou operação sobre
  `ProtectedFile`;
- foi aplicada apenas pela criação automática do banco SQLite isolado dos testes;
- não foi aplicada ao Supabase nem a qualquer ambiente remoto.

## 9. Comandos executados e resultados exatos

Linha de base:

```text
.\.venv\Scripts\python.exe backend\manage.py test clientes core usuarios config
Found 46 test(s).
Ran 46 tests in 62.450s
OK
```

Geração da migration:

```text
.\.venv\Scripts\python.exe backend\manage.py check
System check identified no issues (0 silenced).

.\.venv\Scripts\python.exe backend\manage.py makemigrations clientes
Migrations for 'clientes':
  backend\clientes\migrations\0001_initial.py
    + Create model Cliente
```

Teste isolado do domínio após a correção de normalização:

```text
.\.venv\Scripts\python.exe backend\manage.py test clientes
Found 33 test(s).
Ran 33 tests in 5.585s
OK
```

Dry-run e suíte solicitada:

```text
.\.venv\Scripts\python.exe backend\manage.py makemigrations --check --dry-run
No changes detected

.\.venv\Scripts\python.exe backend\manage.py test clientes core usuarios config
Found 72 test(s).
Ran 72 tests in 63.344s
OK
```

Check e suíte Django completa, executados a partir de `backend/` para descoberta:

```text
..\.venv\Scripts\python.exe manage.py check
System check identified no issues (0 silenced).

..\.venv\Scripts\python.exe manage.py test
Found 72 test(s).
Ran 72 tests in 62.660s
OK
```

As mensagens HTTP esperadas emitidas durante testes negativos não representam
falhas. O Python da virtualenv foi usado explicitamente porque o relatório anterior
documenta que o `python` global não possui Django e que a descoberta sem labels na
raiz não encontra a suíte completa.

## 10. Bloqueadores, riscos e limitações

Bloqueadores: nenhum.

Riscos e limitações restantes:

1. a migration ainda precisa ser aplicada separadamente em cada ambiente, com
   backup, revisão do alvo e janela controlada;
2. o futuro CRUD deve sempre executar `full_clean()` e traduzir eventual
   `IntegrityError` de concorrência para a mensagem genérica de documento;
3. ownership precisa ser aplicado em todas as futuras views, pesquisas, dashboards,
   relatórios e exportações;
4. similaridade de nomes permanece deliberadamente fora desta fase;
5. `ProtectedFile` continua em `config` como dívida técnica previamente aceita;
6. testes usam SQLite isolado; a aplicação controlada em QA PostgreSQL continua
   necessária antes de produção.

## 11. Próxima fase recomendada

Fase 2.4 — formulários e fluxo de cadastro de Cliente: `ModelForm`, criação e edição
com autoria derivada de `request.user`, tratamento seguro de concorrência,
apresentação dos alertas não bloqueantes, rotas autenticadas e templates iniciais.

## 12. Veredito

`READY WITH RESERVATIONS`

A implementação e a migration estão consistentes e cobertas pela suíte isolada. A
reserva é operacional: a migration ainda não foi validada em QA PostgreSQL nem
aplicada a qualquer ambiente remoto, conforme exigido pelo escopo.
