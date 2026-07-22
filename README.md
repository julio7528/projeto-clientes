# Projeto Clientes

Sistema web para cadastro, organização, pesquisa e análise de clientes Pessoa Física e Pessoa Jurídica.

O projeto será desenvolvido com Django e utilizará PostgreSQL hospedado no Supabase.

---

## Visão Geral

O sistema será utilizado inicialmente por um único usuário e funcionará como base central de consulta dos seus contatos e clientes.

Principais funcionalidades previstas:

- login;
- dashboard;
- cadastro de Pessoa Física;
- cadastro de Pessoa Jurídica;
- edição;
- visualização de detalhes;
- pesquisa;
- filtros;
- ativação e inativação;
- relatórios;
- exportação CSV, XLSX e PDF;
- proteção e privacidade dos dados.

---

## Arquitetura Inicial

```text
Usuário
   |
   v
Aplicação Django
   ├── Django ORM -> PostgreSQL no Supabase
   └── serviço backend-only -> Storage privado no Supabase
```

Responsabilidades:

### Django

- interface web;
- autenticação;
- regras de negócio;
- validações;
- cadastro;
- pesquisa;
- dashboard;
- relatórios;
- acesso ao banco.

### Supabase

- hospedagem do PostgreSQL;
- Storage privado acessado exclusivamente pelo backend Django;
- conexão segura;
- administração do banco;
- recursos de backup conforme o plano utilizado.

O projeto não utiliza Supabase Auth ou Realtime. Segredos, caminhos internos e
operações privilegiadas do Storage permanecem no backend; o navegador recebe
somente URLs assinadas de curta duração após autenticação e validação de ownership.

---

## Estrutura do Repositório

```text
ProjetoClientes/
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── pyproject.toml
├── Blueprint/
│   ├── 00-overview/
│   ├── 01-requisitos/
│   ├── 02-modelagem/
│   ├── 03-ui-ux/
│   ├── 04-implementacao/
│   ├── 05-testes/
│   └── 06-deploy/
├── backend/
├── frontend/
├── infrastructure/
├── media/
├── requirements/
├── scripts/
├── static/
└── tests/
```

A organização modular atual do backend é:

```text
backend/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── supabase.py
│   ├── models.py              # ProtectedFile temporariamente
│   └── migrations/
├── core/
│   ├── apps.py
│   ├── models.py              # abstrações compartilhadas
│   ├── normalizers.py
│   ├── migrations/            # sem migration concreta
│   └── tests/
├── usuarios/
│   ├── models.py              # usuarios.Usuario
│   ├── permissions.py
│   ├── urls.py
│   ├── templates/
│   ├── migrations/
│   └── tests.py
└── clientes/
    ├── apps.py
    ├── models.py              # sem Cliente nesta fase
    ├── urls.py                # namespace reservado, não incluído ainda
    ├── migrations/            # sem migration concreta
    └── tests/
```

Responsabilidades atuais:

- `config`: configuração do projeto, composição de URLs e infraestrutura Supabase;
- `core`: abstrações e normalizadores realmente compartilhados, sem regras de domínio;
- `usuarios`: identidade, autenticação por e-mail, perfil, Admin e ownership;
- `clientes`: limite do futuro domínio PF/PJ, estruturado sem modelo ou rotas concretas.

`ProtectedFile` permanece temporariamente em `config`, com tabela, migrations,
ownership e fluxo de Storage inalterados. A criação de uma app `arquivos` está
adiada até que o vínculo e o ciclo de vida dos arquivos de clientes sejam definidos.

### Domínio de clientes — Fase 2.3

O backend possui agora uma entidade única `clientes.Cliente` para Pessoa Física e
Pessoa Jurídica. O modelo herda UUID e timestamps de `core.UUIDTimestampedModel`,
mantém endereço e contato principal integrados e registra autoria por
`settings.AUTH_USER_MODEL`.

Regras implementadas no backend:

- choices de tipo (`PF`/`PJ`), situação (`ATIVO`/`INATIVO`) e 27 UFs;
- normalização idempotente de nome, documento, telefone, CEP, e-mail e endereço;
- validação de CPF, CNPJ, coerência entre tipo e documento, telefone, CEP, UF,
  data não futura e nome útil;
- documento globalmente único com mensagem genérica, sem revelar outro cadastro;
- constraints de tipo, situação e comprimentos críticos, além de índices de busca,
  filtro, localidade e auditoria;
- autoria com `criado_por=PROTECT` e `atualizado_por=SET_NULL`;
- alertas não bloqueantes de telefone e e-mail repetidos, limitados ao ownership do
  usuário comum e globais somente para administradores;
- Admin com documento mascarado na lista, autoria protegida e ações de ativação e
  inativação.

A migration `clientes/0001_initial.py` foi inicialmente validada no banco de teste
isolado e depois aplicada de forma controlada ao Supabase de desenvolvimento,
conforme registrado na etapa seguinte.

### Migrations, autenticação integrada e cadastro — Fases 2.4 a 2.6

Em 22/07/2026, as migrations iniciais de Django, `usuarios`, `clientes` e `config`
foram aplicadas ao projeto Supabase explicitamente confirmado como ambiente de
desenvolvimento vazio e descartável. O plano posterior não possui operações
pendentes; tabelas, constraints, índices e acesso pelo ORM foram verificados sem
persistir dados de smoke test.

O destino temporário após login é `clientes:list`. Redirecionamentos por `next`
aceitam somente destinos locais validados; logout continua exclusivamente por POST
com CSRF. Páginas internas com dados pessoais retornam `Cache-Control: private,
no-store`.

Rotas do fluxo inicial:

- `GET /clientes/` — lista paginada e restrita por ownership;
- `GET|POST /clientes/novo/` — cadastro único PF/PJ;
- `GET /clientes/<uuid>/` — detalhes autorizados;
- `GET|POST /clientes/<uuid>/editar/` — edição autorizada;
- `POST /clientes/<uuid>/ativar/` — ativação idempotente;
- `POST /clientes/<uuid>/inativar/` — inativação idempotente.

Usuários comuns acessam somente clientes em que são `criado_por`; administradores
acessam todos. A busca por objeto ocorre sempre no queryset já limitado, portanto
acesso cruzado retorna 404. Documento duplicado bloqueia com mensagem genérica.
Telefone e e-mail repetidos exigem confirmação explícita em segundo POST; a
confirmação é assinada, expira e deixa de valer quando os valores mudam.

O primeiro superusuário ainda deve ser criado manualmente, com senha interativa:

```powershell
.\.venv\Scripts\python.exe backend\manage.py createsuperuser --email EMAIL_DO_ADMINISTRADOR
```

Não coloque a senha no comando, em arquivo ou no histórico compartilhado.

---

## Blueprint

A pasta `Blueprint/` contém a documentação funcional e técnica do projeto.

Ela deve ser consultada antes da implementação de cada módulo.

### Overview

```text
Blueprint/00-overview/
├── overview_roadmap_projeto_clientes.md
└── relatorio_definicao_projeto_cadastro_clientes.md
```

Contém:

- visão geral;
- escopo;
- roadmap;
- arquitetura de alto nível;
- riscos;
- critérios iniciais.

### Requisitos

```text
Blueprint/01-requisitos/
├── campocadastroskill.md
├── comportamento_dinamico_interface_skill.md
├── dashboard_clientes_skill.md
├── pesquisa_clientes_skill.md
└── relatorios_clientes_skill.md
```

Contém:

- campos;
- regras;
- comportamento do formulário;
- pesquisa;
- dashboard;
- relatórios;
- exportações.

### Modelagem

```text
Blueprint/02-modelagem/
└── modelagem_dados_clientes_skill.md
```

Contém:

- entidade Cliente;
- UML;
- modelo entidade-relacionamento;
- tipos de dados;
- índices;
- constraints;
- esboço de `models.py`.

### Interface e Navegação

```text
Blueprint/03-ui-ux/
└── wireframes_navegacao_skill.md
```

Contém:

- mapa de navegação;
- wireframes;
- layout;
- responsividade;
- acessibilidade;
- fluxos.

---

## Escopo do MVP

O MVP deverá incluir:

1. projeto Django configurado;
2. conexão com PostgreSQL do Supabase;
3. login;
4. proteção das páginas internas;
5. cadastro PF;
6. cadastro PJ;
7. validação de CPF e CNPJ;
8. documento único;
9. edição;
10. detalhes;
11. pesquisa;
12. ativação e inativação;
13. dashboard;
14. relatórios;
15. exportações;
16. testes;
17. ambientes separados;
18. publicação.

---

## Regras Principais

### Pessoa Física

Campos obrigatórios:

- nome completo;
- CPF;
- telefone principal;
- CEP.

### Pessoa Jurídica

Campos obrigatórios:

- nome empresarial;
- CNPJ;
- telefone principal;
- CEP.

### Documento

- CPF ou CNPJ obrigatório;
- documento único;
- validação dos dígitos verificadores;
- armazenamento apenas com números;
- máscara aplicada apenas na interface.

### Situação

- novos clientes iniciam como ativos;
- clientes podem ser inativados;
- exclusão definitiva não será a operação principal.

### Duplicidades

- CPF ou CNPJ repetido: bloqueio;
- telefone repetido: alerta;
- e-mail repetido: alerta;
- nome semelhante: alerta.

---

## Modelo de Dados

PF e PJ utilizarão a mesma entidade:

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

A chave primária prevista é UUID.

---

## Ambientes

O projeto terá três ambientes.

### Desenvolvimento

- execução local;
- dados fictícios;
- depuração habilitada;
- banco próprio.

### QA ou Homologação

- configuração semelhante à produção;
- dados de teste;
- validação antes da publicação;
- banco separado.

### Produção

- dados reais;
- `DEBUG=False`;
- HTTPS;
- backups;
- logs;
- banco exclusivo;
- credenciais próprias.

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

As versões e dependências serão definidas durante o setup técnico.

---

## Setup

O setup será realizado de forma incremental.

Sequência prevista:

```text
1. Verificar Python
2. Criar ambiente virtual
3. Instalar Django
4. Criar projeto
5. Criar apps
6. Configurar Git
7. Configurar variáveis de ambiente
8. Configurar Supabase
9. Executar migrations
10. Criar superusuário
11. Validar conexão
```

Os comandos serão adicionados a este README quando o setup estiver concluído.

---

## Comandos

Esta seção será atualizada após a definição das versões e dependências.

Exemplos esperados:

```powershell
.\.venv\Scripts\Activate.ps1
python backend\manage.py runserver
python backend\manage.py test
python backend\manage.py makemigrations
python backend\manage.py migrate
```

---

## Variáveis de Ambiente

O projeto utilizará um arquivo `.env`, que não deverá ser versionado.

Um arquivo `.env.example` deverá documentar as variáveis necessárias.

Exemplo inicial:

```env
DJANGO_SECRET_KEY=
DJANGO_DEBUG=
DJANGO_ALLOWED_HOSTS=
DATABASE_URL=
```

Nunca inclua credenciais reais no repositório.

---

## Segurança e Privacidade

Diretrizes:

- autenticação obrigatória;
- segredos fora do código;
- documentos mascarados em listagens;
- validação no backend;
- conexão segura com PostgreSQL;
- dados reais separados dos ambientes de teste;
- coleta apenas dos dados necessários;
- proteção de informações pessoais;
- preferência por inativação em vez de exclusão.

---

## Desenvolvimento com Agentes

O projeto será desenvolvido com apoio do Antigravity e do Codex.

Antes de editar código, o agente deve ler:

```text
AGENTS.md
```

O `AGENTS.md` define:

- regras do projeto;
- fonte de verdade;
- convenções;
- validações;
- testes;
- segurança;
- comportamento esperado dos agentes.

---

## Roadmap

```text
Planejamento              Concluído
Campos e validações       Concluído
Pesquisa                  Concluído
Relatórios                Concluído
Dashboard                 Concluído
Wireframes                Concluído
Modelagem de dados        Concluído
Setup técnico             Concluído
Autenticação              Concluído
Estrutura modular         Concluído
Cadastro                  Pendente
Pesquisa implementada     Pendente
Dashboard implementado    Pendente
Relatórios implementados  Pendente
Testes                    Pendente
QA                        Pendente
Produção                  Pendente
```

---

## Testes

A estratégia deverá cobrir:

- modelos;
- validadores;
- formulários;
- autenticação;
- permissões;
- cadastro;
- edição;
- pesquisa;
- filtros;
- dashboard;
- relatórios;
- exportações.

Os comandos e ferramentas serão definidos no setup.

---

## Status Atual

As migrations iniciais estão aplicadas no Supabase de desenvolvimento. A
autenticação Django está integrada à lista de clientes e o fluxo inicial de cadastro,
detalhes, edição, ativação e inativação está implementado com ownership e testes.

Próxima etapa:

```text
Fase 2.7 — pesquisa e filtros de clientes
```
