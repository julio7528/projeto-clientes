# AGENTS.md

## 1. Finalidade

Este arquivo orienta agentes de desenvolvimento, incluindo Codex e agentes executados no Antigravity, sobre como trabalhar neste repositÃ³rio.

O projeto deve ser desenvolvido de forma incremental, seguindo a documentaÃ§Ã£o existente em `Blueprint/`.

Os agentes devem tratar o Blueprint como a principal fonte de requisitos, arquitetura funcional, comportamento da interface e modelagem de dados.

---

## 2. VisÃ£o Geral do Projeto

O projeto consiste em um sistema web de cadastro e gestÃ£o de clientes Pessoa FÃ­sica e Pessoa JurÃ­dica.

O sistema serÃ¡ utilizado inicialmente por um Ãºnico usuÃ¡rio e deverÃ¡ oferecer:

- autenticaÃ§Ã£o;
- dashboard;
- cadastro de clientes;
- ediÃ§Ã£o;
- visualizaÃ§Ã£o de detalhes;
- pesquisa;
- filtros;
- ativaÃ§Ã£o e inativaÃ§Ã£o;
- relatÃ³rios;
- exportaÃ§Ãµes;
- proteÃ§Ã£o e privacidade dos dados.

Arquitetura inicial:

```text
Django
â”œâ”€â”€ interface web
â”œâ”€â”€ autenticaÃ§Ã£o
â”œâ”€â”€ regras de negÃ³cio
â”œâ”€â”€ validaÃ§Ãµes
â”œâ”€â”€ pesquisa
â”œâ”€â”€ dashboard
â”œâ”€â”€ relatÃ³rios
â””â”€â”€ acesso ao banco pelo Django ORM

Supabase
â””â”€â”€ banco de dados PostgreSQL
```

---

## 3. Tecnologias Previstas

- Python;
- Django;
- PostgreSQL;
- Supabase;
- Django Templates;
- HTML;
- CSS;
- JavaScript;
- Git;
- testes automatizados com as ferramentas do ecossistema Django.

As versÃµes exatas serÃ£o definidas durante o setup tÃ©cnico.

NÃ£o introduza frameworks adicionais sem necessidade ou sem decisÃ£o explÃ­cita.

---

## 4. Fonte de Verdade do Projeto

Antes de implementar ou alterar uma funcionalidade, leia:

1. `Blueprint/00-overview/overview_roadmap_projeto_clientes.md`;
2. o arquivo especializado relacionado Ã  tarefa;
3. `Blueprint/02-modelagem/modelagem_dados_clientes_skill.md`, quando houver impacto em dados;
4. `Blueprint/03-ui-ux/wireframes_navegacao_skill.md`, quando houver impacto visual ou de navegaÃ§Ã£o.

Arquivos especializados:

```text
Blueprint/
â”œâ”€â”€ 00-overview/
â”‚   â”œâ”€â”€ overview_roadmap_projeto_clientes.md
â”‚   â””â”€â”€ relatorio_definicao_projeto_cadastro_clientes.md
â”œâ”€â”€ 01-requisitos/
â”‚   â”œâ”€â”€ campocadastroskill.md
â”‚   â”œâ”€â”€ comportamento_dinamico_interface_skill.md
â”‚   â”œâ”€â”€ dashboard_clientes_skill.md
â”‚   â”œâ”€â”€ pesquisa_clientes_skill.md
â”‚   â””â”€â”€ relatorios_clientes_skill.md
â”œâ”€â”€ 02-modelagem/
â”‚   â””â”€â”€ modelagem_dados_clientes_skill.md
â””â”€â”€ 03-ui-ux/
    â””â”€â”€ wireframes_navegacao_skill.md
```

Em caso de conflito:

1. nÃ£o invente uma decisÃ£o;
2. identifique o conflito;
3. preserve a implementaÃ§Ã£o atual;
4. solicite decisÃ£o explÃ­cita antes de alterar comportamento relevante.

---

## 5. Regras Fundamentais

### 5.1 Trabalhar de forma incremental

- implemente uma funcionalidade por vez;
- evite alteraÃ§Ãµes amplas e nÃ£o relacionadas;
- mantenha commits pequenos e objetivos;
- nÃ£o reestruture todo o projeto sem necessidade.

### 5.2 NÃ£o ampliar o escopo

NÃ£o implemente funcionalidades fora do MVP sem solicitaÃ§Ã£o explÃ­cita.

Exemplos atualmente fora do escopo:

- aplicativo mobile nativo;
- integraÃ§Ã£o com WhatsApp;
- emissÃ£o fiscal;
- mÃ³dulo financeiro;
- CRM completo;
- automaÃ§Ãµes de marketing;
- API pÃºblica;
- mÃºltiplos perfis avanÃ§ados;
- Supabase Auth;
- frontend separado em React ou Next.js.

### 5.3 NÃ£o expor segredos

Nunca inclua no cÃ³digo, documentaÃ§Ã£o, logs ou commits:

- senhas;
- `DJANGO_SECRET_KEY`;
- URLs privadas com credenciais;
- chaves do Supabase;
- tokens;
- dados reais de clientes.

Use variÃ¡veis de ambiente.

O arquivo `.env` nÃ£o deve ser versionado.

### 5.4 NÃ£o editar o Blueprint silenciosamente

A documentaÃ§Ã£o em `Blueprint/` representa decisÃµes aprovadas.

NÃ£o altere esses arquivos durante uma implementaÃ§Ã£o comum.

Quando uma mudanÃ§a funcional exigir atualizaÃ§Ã£o documental:

- informe a necessidade;
- proponha o arquivo afetado;
- altere apenas quando solicitado.

---

## 6. Estrutura Esperada do RepositÃ³rio

```text
ProjetoClientes/
â”œâ”€â”€ AGENTS.md
â”œâ”€â”€ README.md
â”œâ”€â”€ .gitignore
â”œâ”€â”€ .env.example
â”œâ”€â”€ pyproject.toml
â”œâ”€â”€ Blueprint/
â”œâ”€â”€ backend/
â”œâ”€â”€ infrastructure/
â”œâ”€â”€ requirements/
â”œâ”€â”€ scripts/
â”œâ”€â”€ staticfiles/
â””â”€â”€ tests/
```

Estrutura prevista para o Django:

```text
backend/
â”œâ”€â”€ manage.py
â”œâ”€â”€ config/
â”œâ”€â”€ apps/
â”‚   â”œâ”€â”€ clientes/
â”‚   â”œâ”€â”€ dashboard/
â”‚   â””â”€â”€ relatorios/
â”œâ”€â”€ templates/
â”œâ”€â”€ static/
â””â”€â”€ media/
```

A estrutura final poderÃ¡ ser ajustada durante o setup, desde que permaneÃ§a simples e coerente.

---

## 7. ConvenÃ§Ãµes de CÃ³digo

### 7.1 Python

- siga PEP 8;
- use nomes claros;
- evite abreviaÃ§Ãµes obscuras;
- mantenha funÃ§Ãµes pequenas;
- adicione type hints quando aumentarem a clareza;
- nÃ£o duplique regras de negÃ³cio;
- prefira cÃ³digo explÃ­cito a soluÃ§Ãµes excessivamente abstratas.

### 7.2 Django

- use Django ORM para acesso ao banco;
- use migrations para alteraÃ§Ãµes estruturais;
- nÃ£o crie ou altere tabelas manualmente no Supabase;
- mantenha regras reutilizÃ¡veis em validadores ou serviÃ§os;
- use formulÃ¡rios Django para validaÃ§Ã£o de entrada;
- proteja pÃ¡ginas internas com autenticaÃ§Ã£o;
- use `settings.AUTH_USER_MODEL` em relacionamentos;
- evite lÃ³gica complexa diretamente nos templates;
- evite views excessivamente grandes.

### 7.3 Templates

- reutilize `base.html`;
- use partials para cabeÃ§alho, menu, mensagens, paginaÃ§Ã£o e modais;
- preserve acessibilidade;
- use HTML semÃ¢ntico;
- nÃ£o dependa apenas de cor;
- mantenha responsividade;
- evite JavaScript desnecessÃ¡rio.

### 7.4 Banco de Dados

- CPF e CNPJ devem ser armazenados somente com nÃºmeros;
- telefone deve ser armazenado somente com nÃºmeros;
- CEP deve ser armazenado somente com nÃºmeros;
- documento deve ser Ãºnico;
- PF e PJ devem utilizar a mesma entidade `Cliente`;
- inativaÃ§Ã£o deve ser preferida Ã  exclusÃ£o;
- toda alteraÃ§Ã£o estrutural deve possuir migration;
- Ã­ndices devem seguir a modelagem aprovada.

---

## 8. Regras de NegÃ³cio Essenciais

### Cliente

Campos obrigatÃ³rios:

- tipo;
- nome;
- documento;
- telefone principal;
- CEP.

Tipo:

- `PF`;
- `PJ`.

Documento:

- CPF para PF;
- CNPJ para PJ;
- obrigatÃ³rio;
- vÃ¡lido;
- Ãºnico.

SituaÃ§Ã£o:

- `ATIVO`;
- `INATIVO`;
- novos clientes iniciam como ativos.

Duplicidade:

- CPF ou CNPJ duplicado: bloquear;
- telefone repetido: alertar;
- e-mail repetido: alertar;
- nome semelhante: alertar, sem bloquear.

Privacidade:

- documentos mascarados em listagens e relatÃ³rios;
- documento completo apenas em telas autorizadas;
- nÃ£o expor dados desnecessÃ¡rios no dashboard.

---

## 9. ValidaÃ§Ã£o e NormalizaÃ§Ã£o

Antes de salvar:

- remover espaÃ§os laterais;
- reduzir espaÃ§os duplicados;
- converter e-mail para minÃºsculas;
- remover pontuaÃ§Ã£o de documento;
- remover pontuaÃ§Ã£o de telefone;
- remover pontuaÃ§Ã£o de CEP;
- converter UF para letras maiÃºsculas.

ValidaÃ§Ãµes obrigatÃ³rias:

- CPF;
- CNPJ;
- telefone com 10 ou 11 dÃ­gitos;
- CEP com 8 dÃ­gitos;
- data nÃ£o futura;
- UF vÃ¡lida;
- nome com conteÃºdo Ãºtil.

A validaÃ§Ã£o deve existir no backend mesmo que tambÃ©m exista na interface.

---

## 10. Interface e NavegaÃ§Ã£o

A interface seguirÃ¡ arquitetura hÃ­brida:

- dashboard separado;
- pesquisa em tela prÃ³pria;
- cadastro em tela prÃ³pria;
- ediÃ§Ã£o reutiliza o formulÃ¡rio;
- detalhes em tela prÃ³pria;
- relatÃ³rios em mÃ³dulo prÃ³prio;
- menu lateral no desktop;
- menu recolhÃ­vel no mobile;
- breadcrumb;
- tabelas no desktop;
- cartÃµes no mobile.

Consulte:

```text
Blueprint/03-ui-ux/wireframes_navegacao_skill.md
```

NÃ£o altere fluxos aprovados sem solicitaÃ§Ã£o.

---

## 11. Testes

Toda funcionalidade relevante deve possuir testes adequados.

Prioridades:

1. modelos;
2. validadores;
3. formulÃ¡rios;
4. autenticaÃ§Ã£o;
5. permissÃµes;
6. views;
7. filtros;
8. relatÃ³rios;
9. exportaÃ§Ãµes;
10. fluxos crÃ­ticos.

Casos mÃ­nimos:

- cadastrar PF vÃ¡lido;
- cadastrar PJ vÃ¡lido;
- rejeitar CPF invÃ¡lido;
- rejeitar CNPJ invÃ¡lido;
- rejeitar documento duplicado;
- validar telefone;
- validar CEP;
- impedir acesso sem login;
- editar cliente;
- ativar e inativar;
- pesquisar por nome e documento;
- aplicar filtros;
- mascarar documento.

NÃ£o considere uma tarefa concluÃ­da quando os testes relacionados estiverem falhando.

---

## 12. Qualidade Antes de Concluir uma Tarefa

Antes de informar conclusÃ£o:

1. revise o diff;
2. confirme que a alteraÃ§Ã£o atende ao Blueprint;
3. execute testes relevantes;
4. execute lint e formataÃ§Ã£o quando configurados;
5. confira migrations;
6. verifique se nÃ£o hÃ¡ segredos;
7. valide comportamento em caso de erro;
8. confira acessibilidade bÃ¡sica;
9. verifique se a alteraÃ§Ã£o nÃ£o quebrou funcionalidades existentes.

---

## 13. Comandos

Os comandos definitivos serÃ£o atualizados apÃ³s o setup.

Exemplos previstos:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements\development.txt
python backend\manage.py migrate
python backend\manage.py runserver
python backend\manage.py test
```

NÃ£o invente comandos de ferramentas ainda nÃ£o configuradas.

---

## 14. Migrations

Ao modificar models:

1. revise o impacto;
2. crie migration;
3. leia a migration gerada;
4. aplique no ambiente de desenvolvimento;
5. execute testes;
6. nÃ£o altere migrations jÃ¡ aplicadas em QA ou produÃ§Ã£o;
7. crie uma nova migration para correÃ§Ãµes.

NÃ£o execute migrations destrutivas sem confirmaÃ§Ã£o explÃ­cita.

---

## 15. Ambientes

O projeto terÃ¡:

- desenvolvimento;
- QA ou homologaÃ§Ã£o;
- produÃ§Ã£o.

Cada ambiente deverÃ¡ possuir:

- banco separado;
- credenciais prÃ³prias;
- variÃ¡veis prÃ³prias;
- configuraÃ§Ãµes apropriadas;
- dados independentes.

Nunca use dados reais de produÃ§Ã£o em desenvolvimento.

---

## 16. Git

- nÃ£o versionar `.env`;
- nÃ£o versionar `.venv`;
- nÃ£o versionar caches;
- nÃ£o versionar arquivos gerados;
- nÃ£o versionar dados reais;
- manter commits focados;
- descrever claramente alteraÃ§Ãµes;
- revisar arquivos antes de commit;
- nÃ£o fazer force push sem solicitaÃ§Ã£o explÃ­cita.

---

## 17. SeguranÃ§a

- autenticaÃ§Ã£o obrigatÃ³ria para pÃ¡ginas internas;
- proteÃ§Ã£o CSRF;
- validaÃ§Ã£o no backend;
- `DEBUG=False` em produÃ§Ã£o;
- `ALLOWED_HOSTS` configurado;
- HTTPS em produÃ§Ã£o;
- cookies seguros em produÃ§Ã£o;
- queries pelo ORM;
- princÃ­pio de menor privilÃ©gio;
- logs sem dados sensÃ­veis.

---

## 18. Comportamento Esperado do Agente

Ao receber uma tarefa:

1. identificar o mÃ³dulo envolvido;
2. ler a documentaÃ§Ã£o relevante;
3. inspecionar a implementaÃ§Ã£o atual;
4. propor ou executar a menor alteraÃ§Ã£o necessÃ¡ria;
5. implementar;
6. testar;
7. informar arquivos alterados;
8. informar testes executados;
9. registrar limitaÃ§Ãµes ou decisÃµes pendentes.

O agente nÃ£o deve:

- assumir requisitos nÃ£o documentados;
- alterar arquitetura sem necessidade;
- apagar cÃ³digo funcional sem justificativa;
- introduzir dependÃªncias sem explicar;
- esconder testes falhando;
- afirmar que algo funciona sem verificar.

---

## 19. DefiniÃ§Ã£o de Pronto

Uma tarefa estÃ¡ pronta quando:

- atende ao requisito;
- segue a arquitetura;
- possui validaÃ§Ã£o;
- possui tratamento de erro;
- possui testes relevantes;
- nÃ£o expÃµe segredos;
- migrations estÃ£o corretas;
- interface estÃ¡ consistente;
- documentaÃ§Ã£o afetada foi identificada;
- o diff estÃ¡ limitado Ã  tarefa.

---

## 20. Prioridade de ImplementaÃ§Ã£o

Ordem prevista:

```text
1. Setup do projeto
2. ConfiguraÃ§Ã£o dos ambientes
3. AutenticaÃ§Ã£o
4. Modelo Cliente
5. Validadores
6. Django Admin
7. Cadastro
8. Detalhes
9. EdiÃ§Ã£o
10. Pesquisa
11. Dashboard
12. RelatÃ³rios
13. ExportaÃ§Ãµes
14. Testes integrados
15. QA
16. ProduÃ§Ã£o
```

Trabalhe respeitando essa sequÃªncia, salvo decisÃ£o explÃ­cita em contrÃ¡rio.

