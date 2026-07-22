---
name: migrations-autenticacao-cadastro-clientes
description: Aplica migrations de forma controlada no PostgreSQL do Supabase, integra autenticação e proteção das páginas e implementa o fluxo inicial de cadastro, detalhes, edição, ativação e inativação de clientes no projeto PC-DJANGO-001.
---

# Skill — Migrations, Autenticação e Cadastro de Clientes
## Projeto PC-DJANGO-001

## 1. Finalidade

Esta skill orienta agentes de desenvolvimento na execução das fases:

```text
2.4 — Migrations definitivas e banco PostgreSQL no Supabase
2.5 — Autenticação integrada e proteção das páginas
2.6 — Cadastro e gestão inicial de clientes
```

O objetivo é transformar a modelagem já concluída em um fluxo funcional completo:

```text
Usuário autenticado
        ↓
Página interna protegida
        ↓
Cadastro de cliente PF ou PJ
        ↓
Validação e alertas
        ↓
Persistência pelo Django ORM
        ↓
PostgreSQL no Supabase
        ↓
Detalhes, edição, ativação e inativação
```

---

## 2. Quando usar

Use esta skill quando a tarefa envolver:

- revisão e aplicação de migrations;
- validação do plano de migrations;
- conexão real com PostgreSQL no Supabase;
- criação de superusuário;
- integração do login com páginas internas;
- proteção de rotas;
- redirecionamentos após login;
- logout seguro;
- controle de acesso por ownership;
- criação de lista simples de clientes;
- formulário único para PF e PJ;
- cadastro de clientes;
- detalhes de cliente;
- edição de cliente;
- ativação;
- inativação;
- mensagens de sucesso e erro;
- confirmação de telefone ou e-mail repetido;
- templates Django do módulo de clientes;
- testes de autenticação, autorização e fluxo de cadastro.

---

## 3. Fontes de verdade

Antes de alterar código, leia nesta ordem:

1. `AGENTS.md`;
2. `README.md`;
3. `backend/README.md`;
4. `Blueprint/01-requisitos/campocadastroskill.md`;
5. `Blueprint/01-requisitos/comportamento_dinamico_interface_skill.md`;
6. `Blueprint/02-modelagem/modelagem_dados_clientes_skill.md`;
7. `Blueprint/03-ui-ux/wireframes_navegacao_skill.md`;
8. especificação técnica desta etapa;
9. skill do modelo Cliente e validadores;
10. relatórios das etapas anteriores;
11. migrations existentes;
12. código atual de `config`, `core`, `usuarios` e `clientes`;
13. estado atual do Git.

Em caso de conflito:

```text
Especificação aprovada desta etapa
→ AGENTS.md
→ Blueprint
→ README.md
→ código atual
```

Não invente comportamentos não aprovados.

---

## 4. Estado atual esperado

Considere como baseline:

- Django configurado em `backend/`;
- PostgreSQL no Supabase configurado por `DATABASE_URL`;
- app `core` funcional;
- app `usuarios` funcional;
- modelo customizado `usuarios.Usuario`;
- login por e-mail;
- sessões Django;
- app `clientes` funcional;
- modelo `clientes.Cliente`;
- validadores de CPF e CNPJ;
- documento único;
- normalização;
- ownership por usuário;
- Django Admin de usuários e clientes;
- migrations geradas;
- testes anteriores funcionando;
- `ProtectedFile` em `config`;
- Supabase acessado somente pelo backend;
- nenhuma migration remota aplicada automaticamente.

Se o repositório divergir, documente antes de continuar.

---

## 5. Decisões obrigatórias

A implementação deve respeitar:

1. Django continua como única fonte de autenticação.
2. Supabase Auth não será usado.
3. Login continua por e-mail e senha.
4. Não haverá cadastro público de usuários.
5. Somente o administrador cria usuários.
6. Todas as páginas de clientes exigem autenticação.
7. Usuários comuns acessam somente os próprios clientes.
8. Administradores acessam todos os clientes.
9. Acesso cruzado por UUID retorna `404`.
10. O formulário será único para PF e PJ.
11. Documento duplicado bloqueia.
12. Telefone e e-mail repetidos geram alerta.
13. Alertas exigem confirmação explícita para continuar.
14. Novos clientes iniciam ativos.
15. Ativação e inativação usam `POST`.
16. Não haverá exclusão física de clientes.
17. Endereço poderá ser preenchido manualmente.
18. Consulta automática de CEP não será implementada nesta etapa.
19. Pesquisa avançada não será implementada.
20. Dashboard não será implementado.
21. Relatórios não serão implementados.
22. `ProtectedFile` não será movido.
23. App `arquivos` não será criada.
24. Nenhum segredo aparecerá no frontend.
25. Nenhuma senha será colocada em comando.
26. Banco de produção nunca será o primeiro ambiente migrado.
27. Migrations serão aplicadas primeiro em desenvolvimento.
28. Não usar `--fake` sem justificativa formal.
29. Não editar `django_migrations` manualmente.
30. Não executar SQL manual para substituir migrations.

---

# PARTE I — MIGRATIONS E BANCO SUPABASE

## 6. Objetivo das migrations

As migrations deverão criar e manter:

- tabelas nativas do Django;
- `usuarios.Usuario`;
- `clientes.Cliente`;
- `config.ProtectedFile`;
- permissões;
- content types;
- sessões;
- constraints;
- índices;
- relacionamentos;
- histórico de migrations.

O Django ORM será a autoridade estrutural.

Não alterar schema manualmente pelo painel SQL do Supabase.

---

## 7. Classificação do ambiente

Antes de qualquer `migrate`, classifique o projeto Supabase como:

```text
DESENVOLVIMENTO
QA/HOMOLOGAÇÃO
PRODUÇÃO
```

### Regras

- primeiro migrate somente em desenvolvimento;
- desenvolvimento usa dados fictícios;
- QA usa banco separado;
- produção usa banco separado;
- credenciais são distintas;
- ambiente com dados reais não é desenvolvimento;
- interromper quando não for possível confirmar o ambiente.

---

## 8. Pré-condições para migrations

Prosseguir somente quando:

1. branch atual estiver identificada;
2. `git status` estiver revisado;
3. migrations estiverem versionadas;
4. `manage.py check` passar;
5. dry-run indicar `No changes detected`;
6. testes passarem;
7. conexão real com PostgreSQL funcionar;
8. banco esperado estiver selecionado;
9. migrations estiverem revisadas manualmente;
10. banco estiver vazio ou com backup válido;
11. custom user estiver configurado corretamente;
12. nenhuma credencial tiver sido exposta;
13. houver autorização explícita para alterar o banco.

---

## 9. Revisão manual das migrations

Revisar:

```text
backend/usuarios/migrations/
backend/config/migrations/
backend/clientes/migrations/
```

Verificar:

- dependências;
- `swappable_dependency`;
- ordem de criação;
- UUIDs;
- ownership;
- `on_delete`;
- índices;
- constraints;
- unicidade;
- ausência de operações destrutivas;
- ausência de `RunSQL` não justificado;
- ausência de credenciais;
- ausência de tabela concreta para modelo abstrato de `core`.

---

## 10. Banco isolado

Antes do Supabase:

```powershell
python backend/manage.py test
```

Requisitos:

- banco criado automaticamente;
- migrations aplicadas;
- testes executados;
- banco destruído ao final;
- nenhum dado real;
- nenhuma conexão de produção.

SQLite em memória é obrigatório, mas não substitui teste real em PostgreSQL de desenvolvimento.

---

## 11. Comandos de inspeção

Executar:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py showmigrations
python backend/manage.py showmigrations --plan
python backend/manage.py migrate --plan
python backend/manage.py test
```

Não ocultar warnings ou falhas.

---

## 12. Teste de conexão real

Executar:

```powershell
python backend/manage.py shell -c "from django.db import connection; connection.ensure_connection(); print(connection.vendor); print(connection.is_usable())"
```

Resultado esperado:

```text
postgresql
True
```

Não imprimir:

- `DATABASE_URL`;
- senha;
- usuário;
- tokens;
- chaves;
- segredos.

---

## 13. Backup

### Banco vazio

- confirmar que está vazio;
- confirmar que não há dados reais;
- confirmar que pode ser recriado;
- registrar o estado.

### Banco com dados

- criar backup;
- validar conclusão;
- registrar horário;
- manter fora do Git;
- não prosseguir com backup incompleto.

### Falha

- interromper;
- não apagar tabelas manualmente;
- não alterar `django_migrations`;
- não repetir operação destrutiva;
- registrar erro e migration.

---

## 14. Aplicação controlada

Comando:

```powershell
python backend/manage.py migrate
```

Regras:

- executar uma vez;
- não usar `--fake`;
- não usar `--fake-initial` sem justificativa;
- não executar migration de outra branch;
- observar toda saída;
- interromper em erro;
- não ocultar warnings.

---

## 15. Verificação pós-migration

Executar:

```powershell
python backend/manage.py showmigrations
python backend/manage.py showmigrations --plan
python backend/manage.py check
```

Verificar:

- migrations marcadas com `[X]`;
- tabela de usuários;
- tabela de clientes;
- tabela de arquivos;
- tabelas nativas;
- constraints;
- índices;
- ausência de pendências.

Executar smoke test pelo ORM sem persistir dados reais.

---

## 16. Criação do superusuário

Comando:

```powershell
python backend/manage.py createsuperuser --email EMAIL_DO_ADMINISTRADOR
```

Regras:

- senha digitada interativamente;
- senha nunca em comando;
- senha nunca em relatório;
- não compartilhar conta;
- confirmar `is_active`;
- confirmar `is_staff`;
- confirmar `is_superuser`;
- testar login no Admin;
- testar logout;
- não criar duplicado sem necessidade.

---

# PARTE II — AUTENTICAÇÃO E PROTEÇÃO

## 17. Preservação da autenticação

Não reescrever sem necessidade:

- modelo `Usuario`;
- manager;
- autenticação;
- login;
- logout;
- perfil;
- alteração de senha;
- Admin;
- sessões;
- cookies;
- CSRF.

A etapa é de integração, proteção e validação.

---

## 18. Fluxo de login

```text
Usuário acessa página protegida
        ↓
Redirecionamento para login com next
        ↓
Login por e-mail e senha
        ↓
Sessão Django
        ↓
Redirecionamento seguro
```

Destino padrão temporário:

```text
clientes:list
```

Até a criação do dashboard.

---

## 19. Redirecionamento seguro

### Login com sucesso

1. usar `next` somente se interno;
2. sem `next`, ir para `clientes:list`.

### Login inválido

- manter e-mail;
- limpar senha;
- mensagem genérica;
- não revelar se conta existe;
- não revelar inatividade.

Mensagem:

```text
E-mail ou senha inválidos.
```

### Usuário autenticado no login

Redirecionar para:

```text
clientes:list
```

### Logout

- somente `POST`;
- CSRF;
- encerrar sessão;
- redirecionar para login;
- rejeitar `GET`.

---

## 20. Rotas públicas

Somente:

- login;
- arquivos estáticos do login;
- endpoints técnicos aprovados.

Não criar:

- signup;
- recuperação por e-mail;
- OAuth;
- login social;
- Supabase Auth;
- MFA.

---

## 21. Rotas protegidas

Todas as páginas de clientes devem usar:

```python
@login_required
```

ou:

```python
LoginRequiredMixin
```

Rotas esperadas:

```text
GET  /clientes/
GET  /clientes/novo/
POST /clientes/novo/
GET  /clientes/<uuid:pk>/
GET  /clientes/<uuid:pk>/editar/
POST /clientes/<uuid:pk>/editar/
POST /clientes/<uuid:pk>/ativar/
POST /clientes/<uuid:pk>/inativar/
```

Atalhos permitidos:

```text
/clientes/novo/?tipo=PF
/clientes/novo/?tipo=PJ
```

Validar o tipo.

---

## 22. Ownership

### Usuário comum

Pode:

- listar próprios clientes;
- criar próprios clientes;
- ver próprios clientes;
- editar próprios clientes;
- ativar próprios clientes;
- inativar próprios clientes.

### Administrador

Pode acessar todos.

### Consulta segura

Aplicar escopo antes de buscar:

```python
queryset = scope_owned_queryset(
    Cliente.objects.all(),
    request.user,
    owner_field="criado_por",
)
cliente = get_object_or_404(queryset, pk=pk)
```

Não buscar globalmente para depois verificar.

### Acesso cruzado

Retornar:

```text
404
```

Não confirmar existência do registro.

---

## 23. Sessões, CSRF e cache

Preservar:

- `SESSION_COOKIE_HTTPONLY=True`;
- cookies Secure em produção;
- CSRF;
- SameSite;
- HTTPS;
- HSTS;
- nenhum token em `localStorage`;
- nenhum segredo Supabase no navegador.

Páginas com dados pessoais:

```text
Cache-Control: private, no-store
Pragma: no-cache
```

Aplicar especialmente a:

- detalhes;
- edição;
- cadastro;
- alertas;
- perfil.

---

## 24. Layout interno

Elementos mínimos:

- nome do sistema;
- usuário autenticado;
- menu;
- clientes;
- novo cliente;
- perfil;
- logout via POST;
- mensagens;
- breadcrumb;
- conteúdo;
- responsividade;
- acessibilidade.

Não implementar dashboard completo.

---

# PARTE III — CADASTRO DE CLIENTES

## 25. Escopo funcional

Implementar:

1. lista simples;
2. cadastro;
3. detalhes;
4. edição;
5. ativação;
6. inativação;
7. mensagens;
8. validação;
9. confirmação de duplicidade;
10. ownership.

Não implementar pesquisa avançada.

---

## 26. Formulário

Criar:

```text
clientes.forms.ClienteForm
```

Base:

```python
forms.ModelForm
```

Campos:

```text
tipo
nome
documento
data_referencia
email
telefone
cep
logradouro
numero
complemento
bairro
cidade
estado
observacoes
```

Não incluir:

```text
id
situacao
criado_em
atualizado_em
criado_por
atualizado_por
```

Situação será alterada por ações separadas.

---

## 27. Comportamento PF/PJ

### PF

```text
Nome completo
CPF
Data de nascimento
```

Máscara:

```text
000.000.000-00
```

### PJ

```text
Nome empresarial
CNPJ
Data de abertura
```

Máscara:

```text
00.000.000/0000-00
```

### Troca de tipo

- atualizar rótulos;
- alterar máscara;
- avisar;
- limpar documento;
- preservar demais campos;
- validar no backend.

Mensagem:

```text
Ao alterar o tipo de cliente, o documento informado será removido.
```

---

## 28. Máscaras

Aplicar JavaScript simples para:

- CPF;
- CNPJ;
- telefone;
- CEP.

Regras:

- validação real permanece no backend;
- sem dependência obrigatória externa;
- sem envio a terceiros;
- funcionamento progressivo;
- campos numéricos adequados em mobile;
- nenhum segredo.

---

## 29. Endereço

Campos:

- CEP;
- logradouro;
- número;
- complemento;
- bairro;
- cidade;
- estado.

Nesta etapa:

- preenchimento manual;
- sem API externa;
- sem bloqueio por ausência de consulta;
- preservar dados em erro;
- validar CEP e UF.

---

## 30. Situação

Novo cliente:

```text
ATIVO
```

Ações:

```text
Ativar
Inativar
```

Regras:

- somente POST;
- CSRF;
- ownership;
- idempotência;
- atualizar `atualizado_por`;
- mensagem;
- redirect;
- sem exclusão.

---

## 31. Autoria

### Criação

```python
cliente.criado_por = request.user
cliente.atualizado_por = request.user
```

### Edição

```python
cliente.atualizado_por = request.user
```

Não alterar `criado_por`.

Não confiar em dados enviados pelo navegador.

---

## 32. Persistência

Fluxo:

```text
POST
↓
form.is_valid()
↓
form.save(commit=False)
↓
definir autoria
↓
full_clean()
↓
verificar alertas
↓
transaction.atomic()
↓
save()
↓
redirect
```

Tratar `IntegrityError` do documento com mensagem genérica.

---

## 33. Documento duplicado

Bloquear.

Mensagens:

```text
Este CPF já está cadastrado.
Este CNPJ já está cadastrado.
```

Alternativa genérica:

```text
Já existe um cliente cadastrado com este documento.
```

Não revelar dados do registro existente.

---

## 34. Alertas de telefone e e-mail

São não bloqueantes.

Fluxo:

```text
Primeiro POST
↓
Validação
↓
Alertas detectados
↓
Reexibir formulário
↓
Salvar mesmo assim
↓
Segundo POST
↓
Recalcular alertas
↓
Salvar
```

Usar campo não persistente:

```text
confirmar_duplicidade
```

Regras:

- recalcular no segundo POST;
- confirmação antiga não vale se dados mudaram;
- não confiar só em JavaScript;
- não identificar outro cliente;
- usuário comum vê apenas próprio escopo;
- admin pode usar escopo global.

---

## 35. Lista

Rota:

```text
GET /clientes/
```

Exibir:

- nome;
- tipo;
- documento mascarado;
- telefone;
- cidade/UF;
- situação;
- detalhes;
- editar.

Regras:

- ownership;
- admin vê todos;
- ordenar por nome;
- paginação simples recomendada;
- sem pesquisa avançada;
- documento mascarado;
- campos vazios com `—`.

---

## 36. Cadastro

Rota:

```text
GET|POST /clientes/novo/
```

Requisitos:

- login;
- formulário único;
- atalhos PF/PJ;
- erros próximos dos campos;
- manter valores;
- foco no primeiro erro;
- evitar envio duplo;
- mensagem;
- redirect para detalhes.

Mensagem:

```text
Cliente cadastrado com sucesso.
```

---

## 37. Detalhes

Rota:

```text
GET /clientes/<uuid:pk>/
```

Exibir:

- tipo;
- nome;
- documento formatado;
- data com rótulo dinâmico;
- e-mail;
- telefone;
- endereço;
- observações;
- situação;
- timestamps;
- ações.

Regras:

- proprietário ou admin;
- no-store;
- sem botão excluir;
- campos vazios claros;
- documento completo apenas em tela autorizada.

---

## 38. Edição

Rota:

```text
GET|POST /clientes/<uuid:pk>/editar/
```

Requisitos:

- carregar dados;
- mesmo formulário;
- excluir o próprio registro dos alertas;
- revalidar documento;
- manter `criado_por`;
- atualizar `atualizado_por`;
- mensagem;
- redirect para detalhes.

Mensagem:

```text
Cliente atualizado com sucesso.
```

---

## 39. Ativação

Rota:

```text
POST /clientes/<uuid:pk>/ativar/
```

Regras:

- login;
- ownership;
- CSRF;
- POST;
- idempotência;
- autoria;
- mensagem;
- redirect.

Mensagem:

```text
Cliente ativado com sucesso.
```

---

## 40. Inativação

Rota:

```text
POST /clientes/<uuid:pk>/inativar/
```

Regras:

- login;
- ownership;
- CSRF;
- POST;
- idempotência;
- autoria;
- mensagem;
- redirect;
- sem exclusão.

Mensagem:

```text
Cliente inativado com sucesso.
```

---

## 41. Templates

Estrutura recomendada:

```text
backend/clientes/templates/clientes/
├── cliente_list.html
├── cliente_form.html
├── cliente_detail.html
└── partials/
    ├── duplicate_warnings.html
    ├── form_errors.html
    └── status_actions.html
```

Regras:

- herdar layout interno;
- CSRF;
- escaping automático;
- não usar `safe` em dados;
- sem debug de objetos;
- responsivo;
- acessível;
- labels associados;
- erros claros;
- sem segredos.

---

## 42. URLs

Namespace:

```python
app_name = "clientes"
```

Nomes:

```text
clientes:list
clientes:create
clientes:detail
clientes:update
clientes:activate
clientes:deactivate
```

Incluir em:

```text
config/urls.py
```

---

## 43. Views

Podem ser FBV ou CBV.

Regras:

- views pequenas;
- ownership no queryset;
- POST para mutações;
- PRG;
- Django messages;
- sem lógica complexa na view;
- sem PII em logs;
- sem stack trace ao usuário.

Separação:

```text
views.py
→ coordenação HTTP

forms.py
→ entrada e validação

services.py
→ duplicidades e operações

models.py
→ invariantes

permissions.py
→ ownership
```

---

## 44. Mensagens

Sucesso:

```text
Cliente cadastrado com sucesso.
Cliente atualizado com sucesso.
Cliente ativado com sucesso.
Cliente inativado com sucesso.
```

Erro:

```text
Não foi possível concluir a operação. Revise os campos informados.
```

Duplicidade:

```text
Este telefone já está associado a outro cliente. Deseja continuar?
Este e-mail já está associado a outro cliente. Deseja continuar?
```

Não exibir erro técnico de banco.

---

## 45. Privacidade e segurança

Não registrar:

- CPF;
- CNPJ;
- telefone;
- e-mail;
- observações;
- corpo completo do POST;
- senha;
- token;
- URL assinada;
- segredo.

Aplicar:

- documento mascarado na lista;
- no-store;
- ownership;
- autoria backend-only;
- mensagens genéricas;
- dados fictícios em testes.

---

# TESTES

## 46. Testes de migrations

Cobrir:

1. migrations em banco isolado;
2. custom user;
3. Cliente;
4. ProtectedFile;
5. constraints;
6. índices quando verificável;
7. ausência de pendências;
8. plano coerente;
9. conexão PostgreSQL real.

---

## 47. Testes de autenticação

Cobrir:

1. login válido;
2. login inválido;
3. mensagem genérica;
4. usuário inativo;
5. `next` interno;
6. `next` externo rejeitado;
7. usuário autenticado no login;
8. logout POST;
9. logout GET rejeitado;
10. sessão encerrada;
11. clientes exige login;
12. CSRF;
13. usuário comum sem Admin;
14. admin com Admin.

---

## 48. Testes de ownership

Cobrir:

1. usuário vê próprios;
2. usuário não vê de outro;
3. admin vê todos;
4. acesso cruzado retorna 404;
5. edição cruzada retorna 404;
6. ativação cruzada retorna 404;
7. inativação cruzada retorna 404.

---

## 49. Testes de cadastro

Cobrir:

1. PF válida;
2. PJ válida;
3. `?tipo=PF`;
4. `?tipo=PJ`;
5. tipo inválido seguro;
6. autoria backend;
7. situação ativa;
8. documento duplicado;
9. erro mantém dados;
10. sucesso redireciona;
11. campos privilegiados ignorados;
12. acesso sem login.

---

## 50. Testes de duplicidade

Cobrir:

1. telefone repetido alerta;
2. e-mail repetido alerta;
3. sem confirmação não salva;
4. com confirmação salva;
5. segundo POST recalcula;
6. alteração invalida confirmação;
7. edição exclui próprio registro;
8. usuário comum sem dados de terceiros;
9. admin global;
10. dois alertas;
11. valores vazios.

---

## 51. Testes de detalhes e edição

Cobrir:

1. proprietário acessa;
2. outro usuário recebe 404;
3. admin acessa;
4. proprietário edita;
5. outro usuário não edita;
6. `criado_por` preservado;
7. `atualizado_por` atualizado;
8. documento validado;
9. redirect;
10. no-store.

---

## 52. Testes de situação

Cobrir:

1. ativar;
2. inativar;
3. POST-only;
4. CSRF;
5. acesso cruzado;
6. admin;
7. idempotência;
8. autoria;
9. sem exclusão;
10. mensagens.

---

## 53. Testes de regressão

Confirmar:

- login anterior;
- logout;
- perfil;
- troca de senha;
- Admin;
- custom user;
- Cliente;
- validadores;
- ownership;
- ProtectedFile;
- Storage;
- redaction;
- tests de `config`;
- `core`;
- `usuarios`;
- `clientes`.

---

# ORDEM DE EXECUÇÃO

## 54. Auditoria

1. ler documentação;
2. revisar Git;
3. revisar migrations;
4. revisar settings;
5. revisar autenticação;
6. revisar Cliente;
7. executar baseline;
8. confirmar ambiente Supabase.

---

## 55. Migrations

1. `check`;
2. dry-run;
3. revisão manual;
4. testes;
5. plano;
6. conexão;
7. backup;
8. migrate;
9. showmigrations;
10. smoke tests.

---

## 56. Superusuário

1. verificar existente;
2. criar interativamente;
3. testar Admin;
4. testar logout;
5. não registrar senha.

---

## 57. Autenticação

1. revisar login;
2. revisar `next`;
3. bloquear redirect externo;
4. definir destino;
5. proteger rotas;
6. testar ownership;
7. aplicar no-store;
8. testar CSRF.

---

## 58. Cadastro

1. criar form;
2. criar lista;
3. criar cadastro;
4. criar detalhes;
5. criar edição;
6. criar ativação;
7. criar inativação;
8. integrar alertas;
9. criar templates;
10. criar JavaScript mínimo;
11. criar testes.

---

## 59. Validação final

1. `check`;
2. dry-run;
3. testes específicos;
4. suíte completa;
5. revisar diff;
6. verificar segredos;
7. verificar PII;
8. atualizar documentação;
9. gerar relatório.

---

## 60. Comandos

Antes do banco remoto:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py showmigrations --plan
python backend/manage.py migrate --plan
python backend/manage.py test
```

Conexão:

```powershell
python backend/manage.py shell -c "from django.db import connection; connection.ensure_connection(); print(connection.vendor); print(connection.is_usable())"
```

Aplicação:

```powershell
python backend/manage.py migrate
```

Depois:

```powershell
python backend/manage.py showmigrations
python backend/manage.py check
```

Superusuário:

```powershell
python backend/manage.py createsuperuser --email EMAIL_DO_ADMINISTRADOR
```

---

## 61. Documentação

Atualizar:

- `README.md`;
- `backend/README.md`;
- rotas;
- migrations;
- destino pós-login;
- fluxo de cadastro;
- ownership;
- duplicidades;
- limitações.

Criar:

```text
migrations_auth_clientes_implementation_report.md
```

O relatório deve incluir:

- ambiente;
- migrations;
- banco isolado;
- testes;
- conexão;
- migrate;
- superusuário sem senha;
- rotas;
- templates;
- acesso;
- duplicidades;
- arquivos;
- riscos;
- bloqueadores;
- próximos passos.

---

## 62. Critérios de aceite — Banco

A parte de banco estará pronta quando:

1. migrations versionadas;
2. revisão manual registrada;
3. dry-run sem mudanças;
4. testes passando;
5. conexão PostgreSQL utilizável;
6. ambiente confirmado;
7. backup ou banco vazio confirmado;
8. migrate concluído;
9. showmigrations completo;
10. tabelas e constraints disponíveis;
11. sem SQL manual;
12. sem segredo exposto.

---

## 63. Critérios de aceite — Autenticação

A parte de autenticação estará pronta quando:

1. login por e-mail funcionar;
2. logout POST funcionar;
3. usuário inativo bloqueado;
4. `next` seguro funcionar;
5. redirect externo bloqueado;
6. páginas internas protegidas;
7. usuário comum sem Admin;
8. admin com Admin;
9. sessão e CSRF preservados;
10. páginas sensíveis com no-store;
11. rotas de clientes protegidas.

---

## 64. Critérios de aceite — Cadastro

A parte de cadastro estará pronta quando:

1. lista existir;
2. formulário PF/PJ existir;
3. cadastro PF funcionar;
4. cadastro PJ funcionar;
5. rótulos dinâmicos funcionarem;
6. máscaras funcionarem;
7. backend funcionar sem JavaScript;
8. documento duplicado bloquear;
9. telefone repetido alertar;
10. e-mail repetido alertar;
11. confirmação permitir salvar;
12. autoria correta;
13. detalhes protegidos;
14. edição protegida;
15. atualização de autoria;
16. ativação funcionar;
17. inativação funcionar;
18. sem exclusão;
19. ownership correto;
20. admin acessa todos;
21. acesso cruzado retorna 404;
22. mensagens claras;
23. templates acessíveis;
24. testes passam;
25. sem PII em logs.

---

## 65. Fora do escopo

Não implementar:

- signup;
- recuperação por e-mail;
- Supabase Auth;
- OAuth;
- login social;
- MFA;
- pesquisa avançada;
- filtros avançados;
- dashboard;
- relatórios;
- exportações;
- consulta automática de CEP;
- similaridade de nomes;
- exclusão física;
- uploads;
- relação de arquivos com Cliente;
- app `arquivos`;
- movimentação de `ProtectedFile`;
- API pública;
- React;
- Next.js;
- Realtime;
- deploy de produção.

---

## 66. Próxima etapa

A próxima fase será:

```text
Fase 2.7 — Pesquisa e filtros de clientes
```

Ela deverá tratar:

- pesquisa geral;
- nome;
- documento;
- telefone;
- e-mail;
- cidade;
- estado;
- tipo;
- situação;
- paginação;
- preservação de filtros;
- ownership;
- privacidade.

---

## 67. Restrições do agente

O agente deve:

- trabalhar incrementalmente;
- preservar comportamento existente;
- não expor `.env`;
- não imprimir segredos;
- não registrar PII;
- não colocar senha em comando;
- não usar SQL manual;
- não usar fake migrations sem autorização;
- não editar `django_migrations`;
- não fazer commit;
- não fazer push;
- não aplicar em produção sem autorização;
- não alterar Blueprint silenciosamente;
- não ampliar escopo;
- não mover `ProtectedFile`;
- não criar app `arquivos`;
- interromper diante de ambiente ou banco ambíguo.

---

## 68. Saída esperada

Ao concluir uma implementação baseada nesta skill, apresentar:

1. subetapas concluídas;
2. ambiente utilizado;
3. migrations revisadas;
4. migrations aplicadas;
5. resultado da conexão;
6. superusuário criado sem senha exposta;
7. arquivos alterados;
8. rotas implementadas;
9. forms criados;
10. views criadas;
11. templates criados;
12. regras de ownership;
13. fluxo de duplicidade;
14. testes executados;
15. resultados dos comandos;
16. documentação atualizada;
17. relatório;
18. bloqueadores;
19. riscos;
20. próxima fase;
21. veredito:
   - `READY`;
   - `READY WITH RESERVATIONS`;
   - `NOT READY`.
