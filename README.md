# Projeto Clientes

Sistema web para cadastro, organizaÃ§Ã£o, pesquisa e anÃ¡lise de clientes Pessoa FÃ­sica e Pessoa JurÃ­dica.

O projeto serÃ¡ desenvolvido com Django e utilizarÃ¡ PostgreSQL hospedado no Supabase.

---

## VisÃ£o Geral

O sistema serÃ¡ utilizado inicialmente por um Ãºnico usuÃ¡rio e funcionarÃ¡ como base central de consulta dos seus contatos e clientes.

Principais funcionalidades previstas:

- login;
- dashboard;
- cadastro de Pessoa FÃ­sica;
- cadastro de Pessoa JurÃ­dica;
- ediÃ§Ã£o;
- visualizaÃ§Ã£o de detalhes;
- pesquisa;
- filtros;
- ativaÃ§Ã£o e inativaÃ§Ã£o;
- relatÃ³rios;
- exportaÃ§Ã£o CSV, XLSX e PDF;
- proteÃ§Ã£o e privacidade dos dados.

---

## Arquitetura Inicial

```text
UsuÃ¡rio
   |
   v
AplicaÃ§Ã£o Django
   â”œâ”€â”€ Django ORM -> PostgreSQL no Supabase
   â””â”€â”€ serviÃ§o backend-only -> Storage privado no Supabase
```

Responsabilidades:

### Django

- interface web;
- autenticaÃ§Ã£o;
- regras de negÃ³cio;
- validaÃ§Ãµes;
- cadastro;
- pesquisa;
- dashboard;
- relatÃ³rios;
- acesso ao banco.

### Supabase

- hospedagem do PostgreSQL;
- Storage privado acessado exclusivamente pelo backend Django;
- conexÃ£o segura;
- administraÃ§Ã£o do banco;
- recursos de backup conforme o plano utilizado.

O projeto nÃ£o utiliza Supabase Auth ou Realtime. Segredos, caminhos internos e
operaÃ§Ãµes privilegiadas do Storage permanecem no backend; o navegador recebe
somente URLs assinadas de curta duraÃ§Ã£o apÃ³s autenticaÃ§Ã£o e validaÃ§Ã£o de ownership.

---

## Estrutura do RepositÃ³rio

```text
ProjetoClientes/
â”œâ”€â”€ AGENTS.md
â”œâ”€â”€ README.md
â”œâ”€â”€ .gitignore
â”œâ”€â”€ .env.example
â”œâ”€â”€ pyproject.toml
â”œâ”€â”€ Blueprint/
â”‚   â”œâ”€â”€ 00-overview/
â”‚   â”œâ”€â”€ 01-requisitos/
â”‚   â”œâ”€â”€ 02-modelagem/
â”‚   â”œâ”€â”€ 03-ui-ux/
â”‚   â”œâ”€â”€ 04-implementacao/
â”‚   â”œâ”€â”€ 05-testes/
â”‚   â””â”€â”€ 06-deploy/
â”œâ”€â”€ backend/
â”œâ”€â”€ frontend/
â”œâ”€â”€ infrastructure/
â”œâ”€â”€ media/
â”œâ”€â”€ requirements/
â”œâ”€â”€ scripts/
â”œâ”€â”€ static/
â””â”€â”€ tests/
```

A organizaÃ§Ã£o modular atual do backend Ã©:

```text
backend/
â”œâ”€â”€ config/
â”‚   â”œâ”€â”€ settings.py
â”‚   â”œâ”€â”€ urls.py
â”‚   â”œâ”€â”€ supabase.py
â”‚   â”œâ”€â”€ models.py              # ProtectedFile temporariamente
â”‚   â””â”€â”€ migrations/
â”œâ”€â”€ core/
â”‚   â”œâ”€â”€ apps.py
â”‚   â”œâ”€â”€ models.py              # abstraÃ§Ãµes compartilhadas
â”‚   â”œâ”€â”€ normalizers.py
â”‚   â”œâ”€â”€ migrations/            # sem migration concreta
â”‚   â””â”€â”€ tests/
â”œâ”€â”€ usuarios/
â”‚   â”œâ”€â”€ models.py              # usuarios.Usuario
â”‚   â”œâ”€â”€ permissions.py
â”‚   â”œâ”€â”€ urls.py
â”‚   â”œâ”€â”€ templates/
â”‚   â”œâ”€â”€ migrations/
â”‚   â””â”€â”€ tests.py
â””â”€â”€ clientes/
    â”œâ”€â”€ apps.py
    â”œâ”€â”€ models.py              # sem Cliente nesta fase
    â”œâ”€â”€ urls.py                # namespace reservado, nÃ£o incluÃ­do ainda
    â”œâ”€â”€ migrations/            # sem migration concreta
    â””â”€â”€ tests/
```

Responsabilidades atuais:

- `config`: configuraÃ§Ã£o do projeto, composiÃ§Ã£o de URLs e infraestrutura Supabase;
- `core`: abstraÃ§Ãµes e normalizadores realmente compartilhados, sem regras de domÃ­nio;
- `usuarios`: identidade, autenticaÃ§Ã£o por e-mail, perfil, Admin e ownership;
- `clientes`: limite do futuro domÃ­nio PF/PJ, estruturado sem modelo ou rotas concretas.

`ProtectedFile` permanece temporariamente em `config`, com tabela, migrations,
ownership e fluxo de Storage inalterados. A criaÃ§Ã£o de uma app `arquivos` estÃ¡
adiada atÃ© que o vÃ­nculo e o ciclo de vida dos arquivos de clientes sejam definidos.

### DomÃ­nio de clientes â€” Fase 2.3

O backend possui agora uma entidade Ãºnica `clientes.Cliente` para Pessoa FÃ­sica e
Pessoa JurÃ­dica. O modelo herda UUID e timestamps de `core.UUIDTimestampedModel`,
mantÃ©m endereÃ§o e contato principal integrados e registra autoria por
`settings.AUTH_USER_MODEL`.

Regras implementadas no backend:

- choices de tipo (`PF`/`PJ`), situaÃ§Ã£o (`ATIVO`/`INATIVO`) e 27 UFs;
- normalizaÃ§Ã£o idempotente de nome, documento, telefone, CEP, e-mail e endereÃ§o;
- validaÃ§Ã£o de CPF, CNPJ, coerÃªncia entre tipo e documento, telefone, CEP, UF,
  data nÃ£o futura e nome Ãºtil;
- documento globalmente Ãºnico com mensagem genÃ©rica, sem revelar outro cadastro;
- constraints de tipo, situaÃ§Ã£o e comprimentos crÃ­ticos, alÃ©m de Ã­ndices de busca,
  filtro, localidade e auditoria;
- autoria com `criado_por=PROTECT` e `atualizado_por=SET_NULL`;
- alertas nÃ£o bloqueantes de telefone e e-mail repetidos, limitados ao ownership do
  usuÃ¡rio comum e globais somente para administradores;
- Admin com documento mascarado na lista, autoria protegida e aÃ§Ãµes de ativaÃ§Ã£o e
  inativaÃ§Ã£o.

A migration `clientes/0001_initial.py` foi inicialmente validada no banco de teste
isolado e depois aplicada de forma controlada ao Supabase de desenvolvimento,
conforme registrado na etapa seguinte.

### Migrations, autenticaÃ§Ã£o integrada e cadastro â€” Fases 2.4 a 2.6

Em 22/07/2026, as migrations iniciais de Django, `usuarios`, `clientes` e `config`
foram aplicadas ao projeto Supabase explicitamente confirmado como ambiente de
desenvolvimento vazio e descartÃ¡vel. O plano posterior nÃ£o possui operaÃ§Ãµes
pendentes; tabelas, constraints, Ã­ndices e acesso pelo ORM foram verificados sem
persistir dados de smoke test.

O destino temporÃ¡rio apÃ³s login Ã© `clientes:list`. Redirecionamentos por `next`
aceitam somente destinos locais validados; logout continua exclusivamente por POST
com CSRF. PÃ¡ginas internas com dados pessoais retornam `Cache-Control: private,
no-store`.

Rotas do fluxo inicial:

- `GET /clientes/` â€” lista paginada e restrita por ownership;
- `GET|POST /clientes/novo/` â€” cadastro Ãºnico PF/PJ;
- `GET /clientes/<uuid>/` â€” detalhes autorizados;
- `GET|POST /clientes/<uuid>/editar/` â€” ediÃ§Ã£o autorizada;
- `POST /clientes/<uuid>/ativar/` â€” ativaÃ§Ã£o idempotente;
- `POST /clientes/<uuid>/inativar/` â€” inativaÃ§Ã£o idempotente.

UsuÃ¡rios comuns acessam somente clientes em que sÃ£o `criado_por`; administradores
acessam todos. A busca por objeto ocorre sempre no queryset jÃ¡ limitado, portanto
acesso cruzado retorna 404. Documento duplicado bloqueia com mensagem genÃ©rica.
Telefone e e-mail repetidos exigem confirmaÃ§Ã£o explÃ­cita em segundo POST; a
confirmaÃ§Ã£o Ã© assinada, expira e deixa de valer quando os valores mudam.

O primeiro superusuÃ¡rio ainda deve ser criado manualmente, com senha interativa:

```powershell
.\.venv\Scripts\python.exe backend\manage.py createsuperuser --email EMAIL_DO_ADMINISTRADOR
```

NÃ£o coloque a senha no comando, em arquivo ou no histÃ³rico compartilhado.

---

## Blueprint

A pasta `Blueprint/` contÃ©m a documentaÃ§Ã£o funcional e tÃ©cnica do projeto.

Ela deve ser consultada antes da implementaÃ§Ã£o de cada mÃ³dulo.

### Overview

```text
Blueprint/00-overview/
â”œâ”€â”€ overview_roadmap_projeto_clientes.md
â””â”€â”€ relatorio_definicao_projeto_cadastro_clientes.md
```

ContÃ©m:

- visÃ£o geral;
- escopo;
- roadmap;
- arquitetura de alto nÃ­vel;
- riscos;
- critÃ©rios iniciais.

### Requisitos

```text
Blueprint/01-requisitos/
â”œâ”€â”€ campocadastroskill.md
â”œâ”€â”€ comportamento_dinamico_interface_skill.md
â”œâ”€â”€ dashboard_clientes_skill.md
â”œâ”€â”€ pesquisa_clientes_skill.md
â””â”€â”€ relatorios_clientes_skill.md
```

ContÃ©m:

- campos;
- regras;
- comportamento do formulÃ¡rio;
- pesquisa;
- dashboard;
- relatÃ³rios;
- exportaÃ§Ãµes.

### Modelagem

```text
Blueprint/02-modelagem/
â””â”€â”€ modelagem_dados_clientes_skill.md
```

ContÃ©m:

- entidade Cliente;
- UML;
- modelo entidade-relacionamento;
- tipos de dados;
- Ã­ndices;
- constraints;
- esboÃ§o de `models.py`.

### Interface e NavegaÃ§Ã£o

```text
Blueprint/03-ui-ux/
â””â”€â”€ wireframes_navegacao_skill.md
```

ContÃ©m:

- mapa de navegaÃ§Ã£o;
- wireframes;
- layout;
- responsividade;
- acessibilidade;
- fluxos.

---

## Escopo do MVP

O MVP deverÃ¡ incluir:

1. projeto Django configurado;
2. conexÃ£o com PostgreSQL do Supabase;
3. login;
4. proteÃ§Ã£o das pÃ¡ginas internas;
5. cadastro PF;
6. cadastro PJ;
7. validaÃ§Ã£o de CPF e CNPJ;
8. documento Ãºnico;
9. ediÃ§Ã£o;
10. detalhes;
11. pesquisa;
12. ativaÃ§Ã£o e inativaÃ§Ã£o;
13. dashboard;
14. relatÃ³rios;
15. exportaÃ§Ãµes;
16. testes;
17. ambientes separados;
18. publicaÃ§Ã£o.

---

## Regras Principais

### Pessoa FÃ­sica

Campos obrigatÃ³rios:

- nome completo;
- CPF;
- telefone principal;
- CEP.

### Pessoa JurÃ­dica

Campos obrigatÃ³rios:

- nome empresarial;
- CNPJ;
- telefone principal;
- CEP.

### Documento

- CPF ou CNPJ obrigatÃ³rio;
- documento Ãºnico;
- validaÃ§Ã£o dos dÃ­gitos verificadores;
- armazenamento apenas com nÃºmeros;
- mÃ¡scara aplicada apenas na interface.

### SituaÃ§Ã£o

- novos clientes iniciam como ativos;
- clientes podem ser inativados;
- exclusÃ£o definitiva nÃ£o serÃ¡ a operaÃ§Ã£o principal.

### Duplicidades

- CPF ou CNPJ repetido: bloqueio;
- telefone repetido: alerta;
- e-mail repetido: alerta;
- nome semelhante: alerta.

---

## Modelo de Dados

PF e PJ utilizarÃ£o a mesma entidade:

```text
Cliente
```

Campos principais:

```text
id
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
situacao
criado_em
atualizado_em
criado_por
atualizado_por
```

A chave primÃ¡ria prevista Ã© UUID.

---

## Ambientes

O projeto terÃ¡ trÃªs ambientes.

### Desenvolvimento

- execuÃ§Ã£o local;
- dados fictÃ­cios;
- depuraÃ§Ã£o habilitada;
- banco prÃ³prio.

### QA ou HomologaÃ§Ã£o

- configuraÃ§Ã£o semelhante Ã  produÃ§Ã£o;
- dados de teste;
- validaÃ§Ã£o antes da publicaÃ§Ã£o;
- banco separado.

### ProduÃ§Ã£o

- dados reais;
- `DEBUG=False`;
- HTTPS;
- backups;
- logs;
- banco exclusivo;
- credenciais prÃ³prias.

---

## Tecnologias

Tecnologias previstas:

- Python;
- Django;
- PostgreSQL;
- Supabase;
- Django Templates;
- HTML;
- CSS;
- JavaScript;
- Git.

As versÃµes e dependÃªncias serÃ£o definidas durante o setup tÃ©cnico.

---

## Setup

O setup serÃ¡ realizado de forma incremental.

SequÃªncia prevista:

```text
1. Verificar Python
2. Criar ambiente virtual
3. Instalar Django
4. Criar projeto
5. Criar apps
6. Configurar Git
7. Configurar variÃ¡veis de ambiente
8. Configurar Supabase
9. Executar migrations
10. Criar superusuÃ¡rio
11. Validar conexÃ£o
```

Os comandos serÃ£o adicionados a este README quando o setup estiver concluÃ­do.

---

## Comandos

Esta seÃ§Ã£o serÃ¡ atualizada apÃ³s a definiÃ§Ã£o das versÃµes e dependÃªncias.

Exemplos esperados:

```powershell
.\.venv\Scripts\Activate.ps1
python backend\manage.py runserver
python backend\manage.py test
python backend\manage.py makemigrations
python backend\manage.py migrate
```

---

## VariÃ¡veis de Ambiente

O projeto utilizarÃ¡ um arquivo `.env`, que nÃ£o deverÃ¡ ser versionado.

Um arquivo `.env.example` deverÃ¡ documentar as variÃ¡veis necessÃ¡rias.

Exemplo inicial:

```env
DJANGO_SECRET_KEY=
DJANGO_DEBUG=
DJANGO_ALLOWED_HOSTS=
DATABASE_URL=
```

Nunca inclua credenciais reais no repositÃ³rio.

---

## SeguranÃ§a e Privacidade

Diretrizes:

- autenticaÃ§Ã£o obrigatÃ³ria;
- segredos fora do cÃ³digo;
- documentos mascarados em listagens;
- validaÃ§Ã£o no backend;
- conexÃ£o segura com PostgreSQL;
- dados reais separados dos ambientes de teste;
- coleta apenas dos dados necessÃ¡rios;
- proteÃ§Ã£o de informaÃ§Ãµes pessoais;
- preferÃªncia por inativaÃ§Ã£o em vez de exclusÃ£o.

---

## Desenvolvimento com Agentes

O projeto serÃ¡ desenvolvido com apoio do Antigravity e do Codex.

Antes de editar cÃ³digo, o agente deve ler:

```text
AGENTS.md
```

O `AGENTS.md` define:

- regras do projeto;
- fonte de verdade;
- convenÃ§Ãµes;
- validaÃ§Ãµes;
- testes;
- seguranÃ§a;
- comportamento esperado dos agentes.

---

## Roadmap

```text
Planejamento              ConcluÃ­do
Campos e validaÃ§Ãµes       ConcluÃ­do
Pesquisa                  ConcluÃ­do
RelatÃ³rios                ConcluÃ­do
Dashboard                 ConcluÃ­do
Wireframes                ConcluÃ­do
Modelagem de dados        ConcluÃ­do
Setup tÃ©cnico             ConcluÃ­do
AutenticaÃ§Ã£o              ConcluÃ­do
Estrutura modular         ConcluÃ­do
Cadastro                  Pendente
Pesquisa implementada     Pendente
Dashboard implementado    Pendente
RelatÃ³rios implementados  Pendente
Testes                    Pendente
QA                        Pendente
ProduÃ§Ã£o                  Pendente
```

---

## Testes

A estratÃ©gia deverÃ¡ cobrir:

- modelos;
- validadores;
- formulÃ¡rios;
- autenticaÃ§Ã£o;
- permissÃµes;
- cadastro;
- ediÃ§Ã£o;
- pesquisa;
- filtros;
- dashboard;
- relatÃ³rios;
- exportaÃ§Ãµes.

Os comandos e ferramentas serÃ£o definidos no setup.

---

## Status Atual

### Fase final — implementação inicial

Pesquisa, dashboard, relatórios e exports CSV/XLSX/PDF estão implementados no backend. A aplicação possui health checks, WhiteNoise, container e workflow CI; QA e produção continuam condicionados aos recursos e aprovações operacionais descritos em `docs/`.

As migrations iniciais estÃ£o aplicadas no Supabase de desenvolvimento. A
autenticaÃ§Ã£o Django estÃ¡ integrada Ã  lista de clientes e o fluxo inicial de cadastro,
detalhes, ediÃ§Ã£o, ativaÃ§Ã£o e inativaÃ§Ã£o estÃ¡ implementado com ownership e testes.

PrÃ³xima etapa:

```text
Fase 2.7 â€” pesquisa e filtros de clientes
```

