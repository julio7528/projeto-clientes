# Relatório de Implementação — Migrations, Autenticação e Clientes

## 1. Ambiente e autorização

- Projeto: `PC-DJANGO-001`.
- Data: 22/07/2026.
- Branch: `main`.
- Ambiente Supabase: `DESENVOLVIMENTO`.
- Estado confirmado pelo operador: sem dados reais, vazio, descartável, correto
  para o primeiro migrate e explicitamente autorizado para mudanças de schema.
- Arquivos fornecidos em `.skills/` e `.specs/`: consultados e não alterados.
- Nenhuma credencial, host, usuário ou senha foi registrada neste relatório.

## 2. Migrations revisadas

Revisão manual integral:

- `usuarios/0001_initial.py`: cria `usuarios.Usuario` com UUID, e-mail único,
  grupos, permissões e constraint case-insensitive; depende de `auth.0012`.
- `config/0001_initial.py`: cria `ProtectedFile`, usa UUID e
  `swappable_dependency(settings.AUTH_USER_MODEL)`.
- `config/0002_alter_protectedfile_owner.py`: altera somente `owner` para `PROTECT`.
- `clientes/0001_initial.py`: cria `Cliente`, usa UUID, timestamps, documento único,
  choices, constraints, índices e dependência swappable; `criado_por=PROTECT` e
  `atualizado_por=SET_NULL`.
- `core`: somente pacote de migrations; `UUIDTimestampedModel` permanece abstrato
  e não possui tabela.

Não foram encontrados `RunSQL`, SQL manual, fake migration, remoção de tabela ou
campo, alteração destrutiva, credencial ou operação inesperada. As operações Python
do plano pertencem exclusivamente às migrations nativas do Django.

## 3. Aplicação e verificação do banco

O plano inicial mostrou todas as 22 migrations esperadas como não aplicadas. Depois
dos gates de segurança, `migrate` foi executado uma única vez, sem `--fake` ou
`--fake-initial`. Foram aplicadas com `OK`:

- `contenttypes.0001` e `0002`;
- `auth.0001` até `0012`;
- `usuarios.0001`;
- `admin.0001` até `0003`;
- `clientes.0001`;
- `config.0001` e `0002`;
- `sessions.0001`.

Verificação posterior:

- todas as migrations aparecem com `[X]`;
- `migrate --plan`: `No planned migration operations`;
- tabelas esperadas: `True`;
- constraints de Cliente: `True`;
- índices explícitos de Cliente: `True`;
- ORM utilizável para usuários, clientes, arquivos e content types: `True`;
- conexão utilizável: `True`;
- nenhum dado de smoke test foi persistido.

## 4. Superusuário

A consulta sanitizada retornou `superuser_exists False`. Nenhuma conta foi criada,
pois não foi fornecido e-mail administrativo e a execução exige entrada interativa
segura de senha.

Ação manual necessária:

```powershell
.\.venv\Scripts\python.exe backend\manage.py createsuperuser --email EMAIL_DO_ADMINISTRADOR
```

A senha deve ser digitada somente no prompt interativo e não deve aparecer em
comandos, arquivos, logs ou relatórios.

## 5. Autenticação integrada

- Django permanece como única fonte de identidade e sessão.
- Login continua por e-mail e senha.
- Destino padrão temporário: `clientes:list`.
- `next` local validado é respeitado; destino externo é rejeitado.
- Usuário autenticado é redirecionado para a lista ao acessar login.
- Usuário inativo continua rejeitado com mensagem genérica.
- Logout permanece exclusivamente por POST com CSRF.
- Cookies, sessão, HTTPS e proteções existentes não foram removidos.
- Perfil, edição, alteração de senha e páginas de clientes usam headers privados
  `no-store` quando contêm dados pessoais.

## 6. Formulário e fluxo de clientes

`ClienteForm` é um único `ModelForm` PF/PJ com allowlist:

```text
tipo, nome, documento, data_referencia, email, telefone, cep,
logradouro, numero, complemento, bairro, cidade, estado, observacoes
```

Não expõe ID, situação, timestamps ou autoria. Rótulos alternam entre nome
completo/empresarial, CPF/CNPJ e nascimento/abertura. Máscaras locais de documento,
telefone e CEP são progressivas; toda validação continua no backend e o endereço é
manual, sem API externa.

Criação e edição usam `transaction.atomic()`, `full_clean()`, autoria controlada
pelo backend, Post/Redirect/Get e mensagem genérica para conflito de documento.
Criação força situação ativa; edição preserva `criado_por` e atualiza
`atualizado_por`.

## 7. Ownership e rotas

Rotas:

- `clientes:list` — `GET /clientes/`;
- `clientes:create` — `GET|POST /clientes/novo/`;
- `clientes:detail` — `GET /clientes/<uuid>/`;
- `clientes:update` — `GET|POST /clientes/<uuid>/editar/`;
- `clientes:activate` — `POST /clientes/<uuid>/ativar/`;
- `clientes:deactivate` — `POST /clientes/<uuid>/inativar/`.

Usuários comuns recebem queryset limitado por `criado_por`; administradores
`is_staff + is_superuser` recebem o queryset global. Todo lookup de objeto ocorre
depois do escopo. Acesso cruzado a detalhes, edição ou situação retorna 404.
Ativar/inativar é POST-only, protegido por CSRF, idempotente, não exclui registros e
atualiza autoria e timestamp.

## 8. Confirmação de duplicidades

Documento repetido é bloqueante e global, com mensagem genérica. Telefone e e-mail
repetidos são avisos não bloqueantes:

1. o primeiro POST é validado e os avisos são recalculados no escopo permitido;
2. o formulário é reexibido sem salvar;
3. o backend emite token assinado contendo somente hash, sem telefone ou e-mail;
4. o segundo POST precisa enviar confirmação explícita e token válido;
5. os avisos são recalculados novamente;
6. mudança de telefone, e-mail, usuário ou registro invalida a confirmação antiga;
7. edição exclui o próprio registro;
8. nenhuma mensagem identifica outro cliente.

## 9. Layout e templates

Foi criado layout interno sem dependências externas, com navegação para clientes,
novo cliente, perfil e logout POST, mensagens, breadcrumb, foco visível, HTML
semântico e comportamento responsivo. A lista usa tabela no desktop e apresentação
empilhada no mobile; documento é mascarado. Detalhes autorizados exibem rótulos
PF/PJ e não oferecem exclusão.

Templates e assets:

- `core/templates/base.html`;
- `core/static/core/app.css`;
- `clientes/templates/clientes/cliente_list.html`;
- `clientes/templates/clientes/cliente_form.html`;
- `clientes/templates/clientes/cliente_detail.html`;
- partials de campo, avisos e situação;
- `clientes/static/clientes/cliente_form.js`.

A direção do `frontend-skill` resultou em interface operacional sóbria, sem cards
decorativos ou dependências externas, com um único destaque visual e movimento
restrito a feedback de interação.

## 10. Testes e resultados exatos

Antes do migrate:

```text
manage.py check
System check identified no issues (0 silenced).

manage.py makemigrations --check --dry-run
No changes detected

manage.py test (SQLite isolado)
Found 72 test(s).
Ran 72 tests in 63.326s
OK

showmigrations --plan
22 migrations não aplicadas

migrate --plan
plano coerente para as 22 migrations

teste de conexão sanitizado
postgresql
True
```

O primeiro acesso de rede no sandbox foi bloqueado pela política local; os comandos
read-only foram repetidos com autorização explícita e concluíram. Duas invocações
preliminares de `check`/dry-run usaram caminho relativo incompatível com o diretório
de trabalho e falharam antes de iniciar Django; foram imediatamente reexecutadas da
raiz com sucesso.

Aplicação:

```text
manage.py migrate
22 migrations aplicadas com OK em 30.9s
```

Depois da implementação:

```text
manage.py test clientes usuarios
Found 74 test(s).
Ran 74 tests in 64.527s
OK

manage.py test (suíte completa, SQLite isolado)
Found 95 test(s).
Ran 95 tests in 88.732s
OK

manage.py check
System check identified no issues (0 silenced).

manage.py makemigrations --check --dry-run
No changes detected

manage.py migrate --plan
No planned migration operations.

teste final de conexão
postgresql
True
```

As mensagens 404, 405 e 403 vistas na suíte são respostas deliberadamente testadas
para ownership, método HTTP e CSRF.

## 11. Arquivos alterados e criados

Alterados:

- `README.md`;
- `backend/README.md`;
- `backend/clientes/services.py`;
- `backend/clientes/urls.py`;
- `backend/clientes/tests/test_app_structure.py`;
- `backend/config/settings.py`;
- `backend/config/urls.py`;
- `backend/usuarios/views.py`;
- `backend/usuarios/tests.py`;
- `backend/usuarios/templates/usuarios/base.html`;
- `backend/usuarios/templates/usuarios/perfil.html`.

Criados:

- `backend/core/http.py`;
- `backend/core/templates/base.html`;
- `backend/core/static/core/app.css`;
- `backend/clientes/forms.py`;
- `backend/clientes/views.py`;
- templates e partials de clientes;
- `backend/clientes/static/clientes/cliente_form.js`;
- `backend/clientes/tests/test_forms.py`;
- `backend/clientes/tests/test_views.py`;
- `migrations_auth_clientes_implementation_report.md`.

Nenhum Blueprint, migration existente, `ProtectedFile`, integração de Storage ou
segredo foi alterado. Nenhum commit ou push foi realizado.

## 12. Bloqueadores, riscos e próximos passos

Bloqueador operacional:

- criação manual do primeiro superusuário com e-mail administrativo e senha
  interativa.

Riscos restantes:

- validar o fluxo visual em navegador real após criar uma conta administrativa;
- manter bancos e credenciais separados ao criar QA e produção;
- executar backup e plano de rollback antes de migrations futuras;
- rate limiting de login continua dependente da infraestrutura;
- pesquisa e filtros ainda não existem por decisão de escopo.

Próxima fase recomendada: Fase 2.7 — pesquisa e filtros de clientes, sempre
preservando ownership, mascaramento e paginação.

## 13. Veredito

`READY WITH RESERVATIONS`

Banco de desenvolvimento, autenticação integrada e fluxo inicial estão funcionais e
testados. A reserva é a criação interativa do primeiro superusuário e a validação
visual manual autenticada.
