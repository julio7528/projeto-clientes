# Overview e Roadmap do Projeto de Cadastro de Clientes

## 1. Objetivo deste Documento

Este arquivo funciona como o documento centralizador do projeto.

Ele apresenta:

- a visÃ£o geral do sistema;
- o objetivo do projeto;
- a sequÃªncia das etapas;
- a funÃ§Ã£o de cada arquivo Markdown criado;
- a relaÃ§Ã£o entre os documentos;
- o ponto atual do projeto;
- os prÃ³ximos passos.

Este documento nÃ£o substitui os arquivos detalhados. Quando for necessÃ¡rio consultar regras, campos, comportamentos ou critÃ©rios especÃ­ficos, deverÃ¡ ser utilizado o arquivo correspondente.

---

## 2. VisÃ£o Geral do Projeto

O projeto consiste no desenvolvimento de um sistema web para cadastro, consulta, ediÃ§Ã£o, pesquisa, anÃ¡lise e geraÃ§Ã£o de relatÃ³rios de clientes.

O sistema atenderÃ¡:

- clientes Pessoa FÃ­sica;
- clientes Pessoa JurÃ­dica;
- uso inicialmente individual;
- autenticaÃ§Ã£o por login;
- cadastro e ediÃ§Ã£o;
- pesquisa;
- dashboard;
- relatÃ³rios;
- proteÃ§Ã£o e privacidade dos dados;
- banco de dados PostgreSQL hospedado no Supabase;
- aplicaÃ§Ã£o desenvolvida em Django.

A divisÃ£o principal serÃ¡:

```text
Django
â”œâ”€â”€ interface
â”œâ”€â”€ autenticaÃ§Ã£o
â”œâ”€â”€ regras de negÃ³cio
â”œâ”€â”€ validaÃ§Ãµes
â”œâ”€â”€ cadastro
â”œâ”€â”€ pesquisa
â”œâ”€â”€ dashboard
â”œâ”€â”€ relatÃ³rios
â””â”€â”€ acesso ao banco

Supabase
â””â”€â”€ banco de dados PostgreSQL
```

---

## 3. Objetivo do Sistema

O sistema deverÃ¡ ser a base central de consulta e gestÃ£o de contatos e clientes.

Ele deverÃ¡ permitir:

- cadastrar clientes;
- diferenciar PF e PJ;
- validar CPF e CNPJ;
- localizar clientes rapidamente;
- atualizar dados;
- ativar e inativar registros;
- acompanhar indicadores;
- gerar relatÃ³rios;
- proteger os dados conforme boas prÃ¡ticas de privacidade;
- evoluir futuramente para novos mÃ³dulos e usuÃ¡rios.

---

## 4. Escopo da Primeira VersÃ£o

A primeira versÃ£o contempla:

1. tela de login;
2. dashboard;
3. cadastro de clientes;
4. ediÃ§Ã£o;
5. visualizaÃ§Ã£o de detalhes;
6. pesquisa;
7. filtros;
8. ativaÃ§Ã£o e inativaÃ§Ã£o;
9. relatÃ³rios;
10. exportaÃ§Ãµes;
11. validaÃ§Ã£o de CPF e CNPJ;
12. integraÃ§Ã£o com Supabase;
13. separaÃ§Ã£o de ambientes;
14. testes;
15. publicaÃ§Ã£o.

---

## 5. Roadmap Geral

```text
1. DefiniÃ§Ã£o do projeto
2. DefiniÃ§Ã£o dos campos
3. Regras de validaÃ§Ã£o
4. Comportamento dinÃ¢mico da interface
5. Pesquisa de clientes
6. RelatÃ³rios
7. Dashboard
8. Wireframes e navegaÃ§Ã£o
9. Modelagem de dados
10. Setup tÃ©cnico
11. Arquitetura de ambientes
12. ImplementaÃ§Ã£o
13. Testes
14. QA e homologaÃ§Ã£o
15. ProduÃ§Ã£o
16. Monitoramento e evoluÃ§Ã£o
```

---

# 6. Ãndice dos Arquivos do Projeto

## 6.1 `relatorio_definicao_projeto_cadastro_clientes.md`

### Finalidade

Documento inicial de visÃ£o e escopo do projeto.

### Assuntos tratados

1. identificaÃ§Ã£o do projeto;
2. visÃ£o geral;
3. objetivo do sistema;
4. problema a ser resolvido;
5. usuÃ¡rios;
6. escopo funcional;
7. regras de negÃ³cio;
8. privacidade e LGPD;
9. requisitos nÃ£o funcionais;
10. arquitetura inicial;
11. ambientes;
12. escopo do MVP;
13. itens fora do escopo;
14. premissas;
15. riscos;
16. critÃ©rios de aceitaÃ§Ã£o;
17. estratÃ©gia de desenvolvimento;
18. prÃ³ximas etapas.

### Quando consultar

Consultar quando for necessÃ¡rio entender:

- o propÃ³sito do sistema;
- o escopo geral;
- o que faz ou nÃ£o parte da primeira versÃ£o;
- os princÃ­pios do projeto;
- a arquitetura de alto nÃ­vel.

---

## 6.2 `campocadastroskill.md`

### Finalidade

Define os campos do cadastro de clientes.

### Assuntos tratados

1. estrutura geral;
2. campos obrigatÃ³rios;
3. campos opcionais;
4. campos automÃ¡ticos;
5. campos removidos;
6. diferenÃ§a entre PF e PJ;
7. uso de campos Ãºnicos para nome, documento e data;
8. decisÃ£o de usar uma Ãºnica estrutura de cliente.

### Quando consultar

Consultar quando for necessÃ¡rio saber:

- quais campos existem;
- quais sÃ£o obrigatÃ³rios;
- quais sÃ£o opcionais;
- como PF e PJ sÃ£o representadas;
- quais campos aparecem no formulÃ¡rio.

---

## 6.3 `comportamento_dinamico_interface_skill.md`

### Finalidade

Define como o formulÃ¡rio reage Ã s aÃ§Ãµes do usuÃ¡rio.

### Assuntos tratados

1. seleÃ§Ã£o entre PF e PJ;
2. alteraÃ§Ã£o de rÃ³tulos;
3. mÃ¡scaras de CPF e CNPJ;
4. troca de tipo de cliente;
5. comportamento do nome;
6. comportamento do documento;
7. telefone;
8. CEP;
9. preenchimento de endereÃ§o;
10. e-mail;
11. data;
12. situaÃ§Ã£o;
13. botÃ£o salvar;
14. tratamento de erros;
15. alertas de duplicidade;
16. ediÃ§Ã£o;
17. responsividade;
18. acessibilidade;
19. fluxo do formulÃ¡rio.

### Quando consultar

Consultar quando for necessÃ¡rio definir:

- interaÃ§Ã£o do formulÃ¡rio;
- mÃ¡scaras;
- mensagens;
- comportamento ao trocar PF por PJ;
- validaÃ§Ãµes visuais;
- estados da interface.

---

## 6.4 `pesquisa_clientes_skill.md`

### Finalidade

Define a pesquisa e listagem de clientes.

### Assuntos tratados

1. busca geral;
2. pesquisa por nome;
3. pesquisa por documento;
4. pesquisa por telefone;
5. pesquisa por e-mail;
6. filtros;
7. ordenaÃ§Ã£o;
8. paginaÃ§Ã£o;
9. visualizaÃ§Ã£o dos resultados;
10. aÃ§Ãµes por cliente;
11. documentos mascarados;
12. ativaÃ§Ã£o e inativaÃ§Ã£o;
13. estados sem resultados;
14. responsividade;
15. seguranÃ§a;
16. critÃ©rios de aceitaÃ§Ã£o.

### Quando consultar

Consultar quando for necessÃ¡rio implementar:

- tela de clientes;
- filtros;
- listagem;
- paginaÃ§Ã£o;
- ordenaÃ§Ã£o;
- aÃ§Ãµes rÃ¡pidas;
- retorno de pesquisa.

---

## 6.5 `relatorios_clientes_skill.md`

### Finalidade

Define a Ã¡rea de relatÃ³rios.

### Assuntos tratados

1. relatÃ³rio geral;
2. relatÃ³rio por tipo;
3. relatÃ³rio por situaÃ§Ã£o;
4. relatÃ³rio por cidade e estado;
5. relatÃ³rio por perÃ­odo;
6. relatÃ³rio de atualizaÃ§Ãµes;
7. relatÃ³rio de cadastros incompletos;
8. filtros;
9. tabelas;
10. grÃ¡ficos;
11. resumos;
12. ordenaÃ§Ã£o;
13. paginaÃ§Ã£o;
14. exportaÃ§Ã£o CSV;
15. exportaÃ§Ã£o XLSX;
16. exportaÃ§Ã£o PDF;
17. impressÃ£o;
18. privacidade;
19. seguranÃ§a;
20. desempenho;
21. critÃ©rios de aceitaÃ§Ã£o.

### Quando consultar

Consultar quando for necessÃ¡rio implementar:

- relatÃ³rios;
- exportaÃ§Ãµes;
- filtros analÃ­ticos;
- grÃ¡ficos;
- resumos;
- impressÃ£o.

---

## 6.6 `dashboard_clientes_skill.md`

### Finalidade

Define o dashboard e seus indicadores.

### Assuntos tratados

1. total de clientes;
2. total de PF;
3. total de PJ;
4. ativos;
5. inativos;
6. novos clientes;
7. cadastros incompletos;
8. filtros;
9. grÃ¡ficos;
10. rankings;
11. clientes recentes;
12. atalhos;
13. interaÃ§Ã£o com indicadores;
14. carregamento;
15. estados vazios;
16. privacidade;
17. seguranÃ§a;
18. desempenho;
19. responsividade;
20. critÃ©rios de aceitaÃ§Ã£o.

### Quando consultar

Consultar quando for necessÃ¡rio implementar:

- pÃ¡gina inicial;
- indicadores;
- grÃ¡ficos;
- filtros do dashboard;
- atalhos;
- resumos gerenciais.

---

## 6.7 `wireframes_navegacao_skill.md`

### Finalidade

Define a organizaÃ§Ã£o visual, navegaÃ§Ã£o e estrutura das telas.

### Assuntos tratados

1. arquitetura hÃ­brida da interface;
2. mapa de navegaÃ§Ã£o;
3. menu;
4. cabeÃ§alho;
5. breadcrumb;
6. login;
7. dashboard;
8. pesquisa;
9. cadastro;
10. ediÃ§Ã£o;
11. detalhes;
12. relatÃ³rios;
13. perfil;
14. logout;
15. componentes compartilhados;
16. mensagens;
17. modais;
18. estados de carregamento;
19. estados vazios;
20. responsividade;
21. acessibilidade;
22. padrÃ£o visual;
23. fluxos principais;
24. organizaÃ§Ã£o sugerida de templates;
25. critÃ©rios de aceitaÃ§Ã£o.

### Quando consultar

Consultar quando for necessÃ¡rio definir:

- estrutura das pÃ¡ginas;
- fluxo de navegaÃ§Ã£o;
- disposiÃ§Ã£o dos elementos;
- comportamento em desktop e mobile;
- organizaÃ§Ã£o dos templates.

---

## 6.8 `modelagem_dados_clientes_skill.md`

### Finalidade

Define a estrutura de dados do sistema.

### Assuntos tratados

1. decisÃµes de modelagem;
2. entidade Cliente;
3. entidade UsuÃ¡rio;
4. UML de classes;
5. diagrama entidade-relacionamento;
6. dicionÃ¡rio de dados;
7. chave primÃ¡ria;
8. enumeraÃ§Ãµes;
9. regras de integridade;
10. constraints;
11. Ã­ndices;
12. relacionamentos;
13. auditoria;
14. estrutura lÃ³gica da tabela;
15. esboÃ§o de `models.py`;
16. validaÃ§Ãµes;
17. normalizaÃ§Ã£o;
18. privacidade;
19. suporte ao dashboard;
20. suporte aos relatÃ³rios;
21. pesquisa;
22. duplicidades;
23. exclusÃ£o e integridade;
24. migrations;
25. compatibilidade com ambientes;
26. critÃ©rios de aceitaÃ§Ã£o.

### Quando consultar

Consultar quando for necessÃ¡rio implementar:

- banco de dados;
- models do Django;
- migrations;
- constraints;
- Ã­ndices;
- relacionamentos;
- validaÃ§Ãµes de integridade.

---

# 7. RelaÃ§Ã£o entre os Arquivos

Os documentos seguem uma sequÃªncia lÃ³gica.

```text
DefiniÃ§Ã£o do projeto
    |
    v
Campos do cadastro
    |
    v
Comportamento da interface
    |
    v
Pesquisa
    |
    v
RelatÃ³rios
    |
    v
Dashboard
    |
    v
Wireframes e navegaÃ§Ã£o
    |
    v
Modelagem de dados
    |
    v
Setup tÃ©cnico e implementaÃ§Ã£o
```

Cada arquivo detalha uma parte especÃ­fica.

O arquivo centralizador apresenta o caminho geral, mas as decisÃµes tÃ©cnicas e funcionais devem ser consultadas nos arquivos especializados.

---

# 8. Matriz de Consulta RÃ¡pida

| Necessidade | Arquivo |
|---|---|
| Entender o projeto | `relatorio_definicao_projeto_cadastro_clientes.md` |
| Consultar campos | `campocadastroskill.md` |
| Implementar comportamento do formulÃ¡rio | `comportamento_dinamico_interface_skill.md` |
| Implementar pesquisa | `pesquisa_clientes_skill.md` |
| Implementar relatÃ³rios | `relatorios_clientes_skill.md` |
| Implementar dashboard | `dashboard_clientes_skill.md` |
| Criar telas e navegaÃ§Ã£o | `wireframes_navegacao_skill.md` |
| Criar banco e models | `modelagem_dados_clientes_skill.md` |
| Entender a sequÃªncia geral | `overview_roadmap_projeto_clientes.md` |

---

# 9. DependÃªncias entre Etapas

## 9.1 Cadastro

Depende de:

- definiÃ§Ã£o de campos;
- comportamento dinÃ¢mico;
- modelagem de dados;
- wireframe do formulÃ¡rio.

## 9.2 Pesquisa

Depende de:

- modelagem de dados;
- campos indexados;
- regras de privacidade;
- wireframe da listagem.

## 9.3 RelatÃ³rios

Depende de:

- modelagem;
- pesquisa;
- filtros;
- regras de exportaÃ§Ã£o;
- privacidade.

## 9.4 Dashboard

Depende de:

- modelagem;
- consultas agregadas;
- indicadores definidos;
- filtros;
- wireframes.

## 9.5 Login

Depende de:

- configuraÃ§Ã£o do Django;
- autenticaÃ§Ã£o;
- templates;
- controle de sessÃ£o.

---

# 10. Estado Atual do Projeto

As seguintes etapas estÃ£o concluÃ­das em nÃ­vel de planejamento:

- definiÃ§Ã£o do projeto;
- definiÃ§Ã£o dos campos;
- comportamento dinÃ¢mico;
- regras de validaÃ§Ã£o;
- pesquisa;
- relatÃ³rios;
- dashboard;
- wireframes;
- navegaÃ§Ã£o;
- modelagem de dados.

O projeto estÃ¡ pronto para iniciar:

```text
Setup TÃ©cnico e Arquitetura de Ambientes
```

---

# 11. PrÃ³xima Fase

A prÃ³xima fase serÃ¡ conduzida manualmente e de forma interativa.

Ela incluirÃ¡:

1. verificar o ambiente local;
2. escolher a versÃ£o do Python;
3. criar a pasta do projeto;
4. criar o ambiente virtual;
5. instalar Django;
6. criar o projeto;
7. criar os aplicativos;
8. iniciar o repositÃ³rio Git;
9. definir dependÃªncias;
10. configurar variÃ¡veis de ambiente;
11. configurar Supabase;
12. separar desenvolvimento, QA e produÃ§Ã£o;
13. executar a primeira migration;
14. criar o primeiro usuÃ¡rio;
15. validar a conexÃ£o.

Essa etapa nÃ£o precisarÃ¡ ser documentada em um novo arquivo Markdown a cada passo. O trabalho serÃ¡ realizado em conversa, seguindo uma aÃ§Ã£o por vez.

---

# 12. Etapas Futuras de ImplementaÃ§Ã£o

ApÃ³s o setup:

```text
1. Estrutura base do Django
2. AutenticaÃ§Ã£o
3. Modelo Cliente
4. Validadores
5. Migrations
6. Django Admin
7. Cadastro
8. EdiÃ§Ã£o
9. Detalhes
10. Pesquisa
11. Dashboard
12. RelatÃ³rios
13. ExportaÃ§Ãµes
14. Testes
15. QA
16. ProduÃ§Ã£o
```

---

# 13. CritÃ©rio para AlteraÃ§Ãµes no Projeto

Sempre que uma decisÃ£o relevante mudar, deverÃ¡ ser atualizado o arquivo especÃ­fico.

Exemplos:

- novo campo â†’ `campocadastroskill.md`;
- nova validaÃ§Ã£o â†’ `comportamento_dinamico_interface_skill.md`;
- novo filtro â†’ arquivo da funcionalidade correspondente;
- nova entidade â†’ `modelagem_dados_clientes_skill.md`;
- nova tela â†’ `wireframes_navegacao_skill.md`;
- mudanÃ§a de escopo â†’ `relatorio_definicao_projeto_cadastro_clientes.md`.

Este arquivo centralizador deverÃ¡ ser atualizado apenas quando:

- um novo documento for criado;
- uma etapa for concluÃ­da;
- o roadmap mudar;
- a estrutura geral do projeto for alterada.

---

# 14. OrganizaÃ§Ã£o Sugerida dos Documentos

```text
documentacao/
â”œâ”€â”€ overview_roadmap_projeto_clientes.md
â”œâ”€â”€ relatorio_definicao_projeto_cadastro_clientes.md
â”œâ”€â”€ campocadastroskill.md
â”œâ”€â”€ comportamento_dinamico_interface_skill.md
â”œâ”€â”€ pesquisa_clientes_skill.md
â”œâ”€â”€ relatorios_clientes_skill.md
â”œâ”€â”€ dashboard_clientes_skill.md
â”œâ”€â”€ wireframes_navegacao_skill.md
â””â”€â”€ modelagem_dados_clientes_skill.md
```

---

# 15. ConclusÃ£o

O projeto jÃ¡ possui uma base funcional, visual e tÃ©cnica suficientemente detalhada para iniciar a implementaÃ§Ã£o.

Os documentos especializados definem o comportamento de cada mÃ³dulo. Este arquivo funciona como o mapa principal para localizar as decisÃµes e acompanhar a evoluÃ§Ã£o do projeto.

O prÃ³ximo passo serÃ¡ iniciar o setup tÃ©cnico do Django e dos ambientes, conduzido manualmente e de forma incremental.

