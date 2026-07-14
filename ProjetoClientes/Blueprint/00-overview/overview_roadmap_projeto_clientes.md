# Overview e Roadmap do Projeto de Cadastro de Clientes

## 1. Objetivo deste Documento

Este arquivo funciona como o documento centralizador do projeto.

Ele apresenta:

- a visão geral do sistema;
- o objetivo do projeto;
- a sequência das etapas;
- a função de cada arquivo Markdown criado;
- a relação entre os documentos;
- o ponto atual do projeto;
- os próximos passos.

Este documento não substitui os arquivos detalhados. Quando for necessário consultar regras, campos, comportamentos ou critérios específicos, deverá ser utilizado o arquivo correspondente.

---

## 2. Visão Geral do Projeto

O projeto consiste no desenvolvimento de um sistema web para cadastro, consulta, edição, pesquisa, análise e geração de relatórios de clientes.

O sistema atenderá:

- clientes Pessoa Física;
- clientes Pessoa Jurídica;
- uso inicialmente individual;
- autenticação por login;
- cadastro e edição;
- pesquisa;
- dashboard;
- relatórios;
- proteção e privacidade dos dados;
- banco de dados PostgreSQL hospedado no Supabase;
- aplicação desenvolvida em Django.

A divisão principal será:

```text
Django
├── interface
├── autenticação
├── regras de negócio
├── validações
├── cadastro
├── pesquisa
├── dashboard
├── relatórios
└── acesso ao banco

Supabase
└── banco de dados PostgreSQL
```

---

## 3. Objetivo do Sistema

O sistema deverá ser a base central de consulta e gestão de contatos e clientes.

Ele deverá permitir:

- cadastrar clientes;
- diferenciar PF e PJ;
- validar CPF e CNPJ;
- localizar clientes rapidamente;
- atualizar dados;
- ativar e inativar registros;
- acompanhar indicadores;
- gerar relatórios;
- proteger os dados conforme boas práticas de privacidade;
- evoluir futuramente para novos módulos e usuários.

---

## 4. Escopo da Primeira Versão

A primeira versão contempla:

1. tela de login;
2. dashboard;
3. cadastro de clientes;
4. edição;
5. visualização de detalhes;
6. pesquisa;
7. filtros;
8. ativação e inativação;
9. relatórios;
10. exportações;
11. validação de CPF e CNPJ;
12. integração com Supabase;
13. separação de ambientes;
14. testes;
15. publicação.

---

## 5. Roadmap Geral

```text
1. Definição do projeto
2. Definição dos campos
3. Regras de validação
4. Comportamento dinâmico da interface
5. Pesquisa de clientes
6. Relatórios
7. Dashboard
8. Wireframes e navegação
9. Modelagem de dados
10. Setup técnico
11. Arquitetura de ambientes
12. Implementação
13. Testes
14. QA e homologação
15. Produção
16. Monitoramento e evolução
```

---

# 6. Índice dos Arquivos do Projeto

## 6.1 `relatorio_definicao_projeto_cadastro_clientes.md`

### Finalidade

Documento inicial de visão e escopo do projeto.

### Assuntos tratados

1. identificação do projeto;
2. visão geral;
3. objetivo do sistema;
4. problema a ser resolvido;
5. usuários;
6. escopo funcional;
7. regras de negócio;
8. privacidade e LGPD;
9. requisitos não funcionais;
10. arquitetura inicial;
11. ambientes;
12. escopo do MVP;
13. itens fora do escopo;
14. premissas;
15. riscos;
16. critérios de aceitação;
17. estratégia de desenvolvimento;
18. próximas etapas.

### Quando consultar

Consultar quando for necessário entender:

- o propósito do sistema;
- o escopo geral;
- o que faz ou não parte da primeira versão;
- os princípios do projeto;
- a arquitetura de alto nível.

---

## 6.2 `campocadastroskill.md`

### Finalidade

Define os campos do cadastro de clientes.

### Assuntos tratados

1. estrutura geral;
2. campos obrigatórios;
3. campos opcionais;
4. campos automáticos;
5. campos removidos;
6. diferença entre PF e PJ;
7. uso de campos únicos para nome, documento e data;
8. decisão de usar uma única estrutura de cliente.

### Quando consultar

Consultar quando for necessário saber:

- quais campos existem;
- quais são obrigatórios;
- quais são opcionais;
- como PF e PJ são representadas;
- quais campos aparecem no formulário.

---

## 6.3 `comportamento_dinamico_interface_skill.md`

### Finalidade

Define como o formulário reage às ações do usuário.

### Assuntos tratados

1. seleção entre PF e PJ;
2. alteração de rótulos;
3. máscaras de CPF e CNPJ;
4. troca de tipo de cliente;
5. comportamento do nome;
6. comportamento do documento;
7. telefone;
8. CEP;
9. preenchimento de endereço;
10. e-mail;
11. data;
12. situação;
13. botão salvar;
14. tratamento de erros;
15. alertas de duplicidade;
16. edição;
17. responsividade;
18. acessibilidade;
19. fluxo do formulário.

### Quando consultar

Consultar quando for necessário definir:

- interação do formulário;
- máscaras;
- mensagens;
- comportamento ao trocar PF por PJ;
- validações visuais;
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
7. ordenação;
8. paginação;
9. visualização dos resultados;
10. ações por cliente;
11. documentos mascarados;
12. ativação e inativação;
13. estados sem resultados;
14. responsividade;
15. segurança;
16. critérios de aceitação.

### Quando consultar

Consultar quando for necessário implementar:

- tela de clientes;
- filtros;
- listagem;
- paginação;
- ordenação;
- ações rápidas;
- retorno de pesquisa.

---

## 6.5 `relatorios_clientes_skill.md`

### Finalidade

Define a área de relatórios.

### Assuntos tratados

1. relatório geral;
2. relatório por tipo;
3. relatório por situação;
4. relatório por cidade e estado;
5. relatório por período;
6. relatório de atualizações;
7. relatório de cadastros incompletos;
8. filtros;
9. tabelas;
10. gráficos;
11. resumos;
12. ordenação;
13. paginação;
14. exportação CSV;
15. exportação XLSX;
16. exportação PDF;
17. impressão;
18. privacidade;
19. segurança;
20. desempenho;
21. critérios de aceitação.

### Quando consultar

Consultar quando for necessário implementar:

- relatórios;
- exportações;
- filtros analíticos;
- gráficos;
- resumos;
- impressão.

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
9. gráficos;
10. rankings;
11. clientes recentes;
12. atalhos;
13. interação com indicadores;
14. carregamento;
15. estados vazios;
16. privacidade;
17. segurança;
18. desempenho;
19. responsividade;
20. critérios de aceitação.

### Quando consultar

Consultar quando for necessário implementar:

- página inicial;
- indicadores;
- gráficos;
- filtros do dashboard;
- atalhos;
- resumos gerenciais.

---

## 6.7 `wireframes_navegacao_skill.md`

### Finalidade

Define a organização visual, navegação e estrutura das telas.

### Assuntos tratados

1. arquitetura híbrida da interface;
2. mapa de navegação;
3. menu;
4. cabeçalho;
5. breadcrumb;
6. login;
7. dashboard;
8. pesquisa;
9. cadastro;
10. edição;
11. detalhes;
12. relatórios;
13. perfil;
14. logout;
15. componentes compartilhados;
16. mensagens;
17. modais;
18. estados de carregamento;
19. estados vazios;
20. responsividade;
21. acessibilidade;
22. padrão visual;
23. fluxos principais;
24. organização sugerida de templates;
25. critérios de aceitação.

### Quando consultar

Consultar quando for necessário definir:

- estrutura das páginas;
- fluxo de navegação;
- disposição dos elementos;
- comportamento em desktop e mobile;
- organização dos templates.

---

## 6.8 `modelagem_dados_clientes_skill.md`

### Finalidade

Define a estrutura de dados do sistema.

### Assuntos tratados

1. decisões de modelagem;
2. entidade Cliente;
3. entidade Usuário;
4. UML de classes;
5. diagrama entidade-relacionamento;
6. dicionário de dados;
7. chave primária;
8. enumerações;
9. regras de integridade;
10. constraints;
11. índices;
12. relacionamentos;
13. auditoria;
14. estrutura lógica da tabela;
15. esboço de `models.py`;
16. validações;
17. normalização;
18. privacidade;
19. suporte ao dashboard;
20. suporte aos relatórios;
21. pesquisa;
22. duplicidades;
23. exclusão e integridade;
24. migrations;
25. compatibilidade com ambientes;
26. critérios de aceitação.

### Quando consultar

Consultar quando for necessário implementar:

- banco de dados;
- models do Django;
- migrations;
- constraints;
- índices;
- relacionamentos;
- validações de integridade.

---

# 7. Relação entre os Arquivos

Os documentos seguem uma sequência lógica.

```text
Definição do projeto
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
Relatórios
    |
    v
Dashboard
    |
    v
Wireframes e navegação
    |
    v
Modelagem de dados
    |
    v
Setup técnico e implementação
```

Cada arquivo detalha uma parte específica.

O arquivo centralizador apresenta o caminho geral, mas as decisões técnicas e funcionais devem ser consultadas nos arquivos especializados.

---

# 8. Matriz de Consulta Rápida

| Necessidade | Arquivo |
|---|---|
| Entender o projeto | `relatorio_definicao_projeto_cadastro_clientes.md` |
| Consultar campos | `campocadastroskill.md` |
| Implementar comportamento do formulário | `comportamento_dinamico_interface_skill.md` |
| Implementar pesquisa | `pesquisa_clientes_skill.md` |
| Implementar relatórios | `relatorios_clientes_skill.md` |
| Implementar dashboard | `dashboard_clientes_skill.md` |
| Criar telas e navegação | `wireframes_navegacao_skill.md` |
| Criar banco e models | `modelagem_dados_clientes_skill.md` |
| Entender a sequência geral | `overview_roadmap_projeto_clientes.md` |

---

# 9. Dependências entre Etapas

## 9.1 Cadastro

Depende de:

- definição de campos;
- comportamento dinâmico;
- modelagem de dados;
- wireframe do formulário.

## 9.2 Pesquisa

Depende de:

- modelagem de dados;
- campos indexados;
- regras de privacidade;
- wireframe da listagem.

## 9.3 Relatórios

Depende de:

- modelagem;
- pesquisa;
- filtros;
- regras de exportação;
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

- configuração do Django;
- autenticação;
- templates;
- controle de sessão.

---

# 10. Estado Atual do Projeto

As seguintes etapas estão concluídas em nível de planejamento:

- definição do projeto;
- definição dos campos;
- comportamento dinâmico;
- regras de validação;
- pesquisa;
- relatórios;
- dashboard;
- wireframes;
- navegação;
- modelagem de dados.

O projeto está pronto para iniciar:

```text
Setup Técnico e Arquitetura de Ambientes
```

---

# 11. Próxima Fase

A próxima fase será conduzida manualmente e de forma interativa.

Ela incluirá:

1. verificar o ambiente local;
2. escolher a versão do Python;
3. criar a pasta do projeto;
4. criar o ambiente virtual;
5. instalar Django;
6. criar o projeto;
7. criar os aplicativos;
8. iniciar o repositório Git;
9. definir dependências;
10. configurar variáveis de ambiente;
11. configurar Supabase;
12. separar desenvolvimento, QA e produção;
13. executar a primeira migration;
14. criar o primeiro usuário;
15. validar a conexão.

Essa etapa não precisará ser documentada em um novo arquivo Markdown a cada passo. O trabalho será realizado em conversa, seguindo uma ação por vez.

---

# 12. Etapas Futuras de Implementação

Após o setup:

```text
1. Estrutura base do Django
2. Autenticação
3. Modelo Cliente
4. Validadores
5. Migrations
6. Django Admin
7. Cadastro
8. Edição
9. Detalhes
10. Pesquisa
11. Dashboard
12. Relatórios
13. Exportações
14. Testes
15. QA
16. Produção
```

---

# 13. Critério para Alterações no Projeto

Sempre que uma decisão relevante mudar, deverá ser atualizado o arquivo específico.

Exemplos:

- novo campo → `campocadastroskill.md`;
- nova validação → `comportamento_dinamico_interface_skill.md`;
- novo filtro → arquivo da funcionalidade correspondente;
- nova entidade → `modelagem_dados_clientes_skill.md`;
- nova tela → `wireframes_navegacao_skill.md`;
- mudança de escopo → `relatorio_definicao_projeto_cadastro_clientes.md`.

Este arquivo centralizador deverá ser atualizado apenas quando:

- um novo documento for criado;
- uma etapa for concluída;
- o roadmap mudar;
- a estrutura geral do projeto for alterada.

---

# 14. Organização Sugerida dos Documentos

```text
documentacao/
├── overview_roadmap_projeto_clientes.md
├── relatorio_definicao_projeto_cadastro_clientes.md
├── campocadastroskill.md
├── comportamento_dinamico_interface_skill.md
├── pesquisa_clientes_skill.md
├── relatorios_clientes_skill.md
├── dashboard_clientes_skill.md
├── wireframes_navegacao_skill.md
└── modelagem_dados_clientes_skill.md
```

---

# 15. Conclusão

O projeto já possui uma base funcional, visual e técnica suficientemente detalhada para iniciar a implementação.

Os documentos especializados definem o comportamento de cada módulo. Este arquivo funciona como o mapa principal para localizar as decisões e acompanhar a evolução do projeto.

O próximo passo será iniciar o setup técnico do Django e dos ambientes, conduzido manualmente e de forma incremental.
