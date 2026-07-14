# Relatório de Definição do Projeto

## 1. Identificação do Projeto

**Nome provisório:** Sistema de Cadastro e Gestão de Clientes  
**Tipo de sistema:** Aplicação web  
**Responsável e usuário inicial:** Proprietário do sistema  
**Tecnologias previstas:** Django e banco de dados PostgreSQL hospedado no Supabase

---

## 2. Visão Geral

O projeto consiste no desenvolvimento de um sistema web para cadastro, organização, consulta e acompanhamento de clientes e contatos.

O sistema deverá permitir o registro de clientes dos tipos:

- Pessoa Física — PF;
- Pessoa Jurídica — PJ.

A aplicação será utilizada inicialmente por um único usuário, que será o proprietário e administrador do sistema.

O objetivo é centralizar os dados de contatos e clientes em uma base estruturada, segura e de fácil consulta, substituindo controles dispersos ou informais.

---

## 3. Objetivo do Sistema

O objetivo principal do sistema é disponibilizar uma base centralizada para consulta, cadastro, atualização e análise dos dados de clientes e contatos.

O sistema deverá permitir que o usuário:

- registre clientes Pessoa Física e Pessoa Jurídica;
- consulte rapidamente os dados cadastrados;
- pesquise clientes por diferentes critérios;
- atualize informações existentes;
- visualize indicadores e informações consolidadas;
- gere relatórios;
- mantenha os dados organizados e protegidos;
- administre os dados em conformidade com princípios de privacidade e proteção de dados.

---

## 4. Problema a Ser Resolvido

Atualmente, contatos e informações de clientes podem estar distribuídos em diferentes locais, formatos ou ferramentas, dificultando:

- a localização rápida de informações;
- a atualização dos dados;
- a identificação de registros duplicados;
- a distinção entre Pessoa Física e Pessoa Jurídica;
- a geração de relatórios;
- a análise da base de clientes;
- o controle de acesso;
- a aplicação de boas práticas de privacidade.

O sistema será a fonte principal de consulta dos contatos e clientes cadastrados.

---

## 5. Usuários do Sistema

### 5.1 Usuário inicial

Na primeira versão, o sistema será utilizado apenas pelo proprietário.

Esse usuário terá permissão administrativa para:

- acessar o sistema;
- cadastrar clientes;
- editar clientes;
- pesquisar registros;
- consultar relatórios;
- visualizar o dashboard;
- administrar os dados da aplicação.

### 5.2 Evolução futura

A arquitetura deverá permitir a inclusão futura de outros usuários e perfis de acesso, como:

- administrador;
- atendente;
- comercial;
- consultor;
- usuário somente para consulta.

A gestão avançada de perfis e permissões não faz parte obrigatoriamente da primeira versão, mas não deverá ser impedida pela arquitetura inicial.

---

## 6. Escopo Funcional Inicial

A primeira versão do sistema deverá contemplar os seguintes módulos.

### 6.1 Autenticação

Tela de login para acesso ao sistema.

Funcionalidades previstas:

- autenticação por usuário e senha;
- encerramento de sessão;
- bloqueio de acesso para usuários não autenticados;
- proteção das páginas internas;
- possibilidade futura de recuperação de senha.

### 6.2 Cadastro de clientes

Tela ou área destinada ao cadastro de clientes Pessoa Física e Pessoa Jurídica.

O usuário deverá selecionar o tipo de cliente antes de concluir o cadastro:

- Pessoa Física;
- Pessoa Jurídica.

Os campos apresentados poderão mudar conforme o tipo selecionado.

### 6.3 Edição de clientes

O sistema deverá permitir:

- localizar um cliente;
- abrir o registro;
- alterar as informações;
- validar novamente os campos obrigatórios;
- registrar a data da última atualização;
- salvar as alterações.

### 6.4 Pesquisa de clientes

O sistema deverá oferecer uma tela ou área de pesquisa.

Critérios iniciais de pesquisa:

- nome;
- razão social;
- nome fantasia;
- CPF;
- CNPJ;
- telefone;
- e-mail;
- cidade;
- estado;
- tipo de cliente;
- situação do cadastro.

### 6.5 Relatórios

O sistema deverá possuir uma área de relatórios para consulta consolidada dos dados.

Relatórios iniciais possíveis:

- clientes cadastrados;
- clientes por tipo;
- clientes ativos e inativos;
- clientes por cidade;
- clientes por estado;
- cadastros realizados por período;
- clientes com dados incompletos.

A definição final dos relatórios ocorrerá durante a etapa de detalhamento dos requisitos.

### 6.6 Dashboard

O sistema deverá apresentar um painel com indicadores resumidos.

Indicadores iniciais possíveis:

- total de clientes;
- quantidade de pessoas físicas;
- quantidade de pessoas jurídicas;
- clientes ativos;
- clientes inativos;
- novos cadastros no período;
- distribuição por cidade ou estado;
- registros incompletos.

### 6.7 Organização das telas

As funcionalidades poderão ser distribuídas em várias telas ou reunidas em uma interface única.

Essa decisão será tomada posteriormente, durante a definição dos wireframes e da experiência de uso.

As possibilidades incluem:

- telas separadas por módulo;
- painel único com abas;
- tela principal com pesquisa, cadastro e edição;
- dashboard com atalhos para as demais funcionalidades.

---

## 7. Regras de Negócio Iniciais

### 7.1 Tipo de cliente obrigatório

Todo cliente deverá ser classificado como:

- Pessoa Física; ou
- Pessoa Jurídica.

O tipo escolhido determinará quais dados e validações serão aplicados.

### 7.2 Documento obrigatório

Todo cliente deverá possuir um documento principal obrigatório:

- CPF para Pessoa Física;
- CNPJ para Pessoa Jurídica.

Não será permitido concluir o cadastro sem o documento correspondente ao tipo selecionado.

### 7.3 Documento único

O sistema não deverá permitir dois clientes com o mesmo CPF ou CNPJ.

Antes de salvar um novo registro, o sistema deverá verificar se o documento já está cadastrado.

### 7.4 Validação do documento

O CPF ou CNPJ deverá:

- possuir formato válido;
- passar pela validação dos dígitos verificadores;
- ser armazenado de forma padronizada;
- ser pesquisável com ou sem pontuação.

### 7.5 Campos condicionais

Para Pessoa Física, poderão ser utilizados campos como:

- nome completo;
- CPF;
- data de nascimento;
- telefone;
- e-mail;
- endereço.

Para Pessoa Jurídica, poderão ser utilizados campos como:

- razão social;
- nome fantasia;
- CNPJ;
- inscrição estadual;
- responsável pelo contato;
- telefone;
- e-mail;
- endereço.

A lista definitiva dos campos será definida na etapa de requisitos detalhados e modelagem de dados.

### 7.6 Situação do cadastro

Todo cliente deverá possuir uma situação, inicialmente:

- ativo;
- inativo.

A preferência será pela inativação em vez da exclusão definitiva de registros que já tenham histórico de uso.

### 7.7 Datas de controle

O sistema deverá registrar automaticamente:

- data de criação;
- data da última atualização.

### 7.8 Padronização dos dados

Os dados deverão seguir padrões de preenchimento sempre que possível.

Exemplos:

- CPF e CNPJ com formatação consistente;
- telefones com DDD;
- estado por sigla;
- e-mail em letras minúsculas;
- remoção de espaços indevidos;
- nomes sem espaços duplicados;
- CEP em formato padronizado.

### 7.9 Prevenção de duplicidades

Além da unicidade do CPF e do CNPJ, o sistema poderá alertar sobre possíveis duplicidades com base em:

- nome semelhante;
- mesmo telefone;
- mesmo e-mail;
- mesma razão social.

Esses alertas poderão ser implementados em uma etapa posterior.

---

## 8. Privacidade e Proteção de Dados

O sistema deverá ser planejado com base nos princípios de privacidade e proteção de dados pessoais.

### 8.1 Coleta necessária

Deverão ser coletados apenas os dados necessários para a finalidade do cadastro e relacionamento com o cliente.

Campos sem finalidade definida deverão ser evitados.

### 8.2 Finalidade

Os dados deverão ser utilizados para:

- identificação do cliente;
- manutenção do contato;
- consulta interna;
- organização da base;
- geração de relatórios gerenciais;
- execução das atividades relacionadas ao relacionamento com o cliente.

### 8.3 Controle de acesso

Somente usuários autenticados e autorizados deverão acessar os dados.

Na primeira versão, o acesso será restrito ao proprietário do sistema.

### 8.4 Segurança das credenciais

Senhas, chaves de acesso e dados de conexão com o banco não deverão ser armazenados diretamente no código-fonte.

Essas informações deverão ser mantidas em variáveis de ambiente.

### 8.5 Registro de alterações

O sistema deverá registrar, no mínimo:

- quando o cliente foi criado;
- quando foi atualizado.

Em uma evolução futura, poderá registrar:

- quem realizou a alteração;
- quais campos foram modificados;
- histórico das alterações.

### 8.6 Exclusão e anonimização

O sistema deverá prever procedimentos para:

- inativação de cadastro;
- correção de dados;
- exclusão quando aplicável;
- anonimização quando houver necessidade de preservar informações estatísticas ou históricas.

A regra definitiva dependerá da finalidade do tratamento e das obrigações aplicáveis ao negócio.

### 8.7 Exportação dos dados

Poderá ser incluída futuramente uma funcionalidade para exportar os dados de um cliente, apoiando solicitações de acesso e portabilidade quando aplicável.

### 8.8 Dados sensíveis

O sistema não deverá coletar dados pessoais sensíveis sem necessidade claramente justificada.

Caso essa necessidade surja, deverão ser definidas regras adicionais de segurança, acesso e tratamento.

---

## 9. Requisitos Não Funcionais Iniciais

### 9.1 Segurança

O sistema deverá:

- exigir autenticação;
- proteger rotas internas;
- utilizar conexões seguras;
- manter segredos fora do código;
- aplicar validação no backend;
- impedir acesso indevido aos registros;
- utilizar proteção contra vulnerabilidades comuns de aplicações web.

### 9.2 Usabilidade

A interface deverá ser:

- clara;
- objetiva;
- responsiva;
- adequada para uso em computador;
- organizada para facilitar pesquisa e atualização;
- consistente entre as telas.

### 9.3 Desempenho

Pesquisas comuns deverão retornar resultados rapidamente, mesmo com o crescimento da base.

Campos frequentemente pesquisados deverão ser considerados na estratégia de indexação do banco.

### 9.4 Manutenibilidade

O código deverá ser organizado por módulos e seguir boas práticas do Django.

As regras de negócio não deverão ficar espalhadas de forma desorganizada entre telas, modelos e banco de dados.

### 9.5 Rastreabilidade

As mudanças no código deverão ser versionadas em Git.

As alterações no banco deverão ser controladas por migrations do Django.

### 9.6 Disponibilidade

O sistema deverá ser acessível pela internet após a publicação em produção.

Durante o desenvolvimento, será executado inicialmente em ambiente local.

### 9.7 Backup

O ambiente de produção deverá possuir estratégia de backup e recuperação do banco de dados.

---

## 10. Arquitetura Inicial Proposta

A divisão inicial de responsabilidades será:

### 10.1 Django

O Django será responsável por:

- interface web;
- autenticação;
- regras de negócio;
- validação dos dados;
- cadastro e edição;
- pesquisa;
- relatórios;
- dashboard;
- administração da aplicação;
- acesso ao banco por meio do Django ORM.

### 10.2 Supabase

O Supabase será utilizado inicialmente como serviço de banco de dados PostgreSQL.

Será responsável por:

- armazenamento dos dados;
- disponibilidade do PostgreSQL;
- conexão segura com a aplicação;
- recursos de administração e backup conforme o plano utilizado.

### 10.3 Fluxo principal

```text
Usuário
   |
   v
Aplicação Django
   |
   v
Django ORM
   |
   v
PostgreSQL no Supabase
```

Na primeira versão, a autenticação poderá ser gerenciada pelo próprio Django.

O uso de Supabase Auth, Storage, Realtime ou outras funcionalidades não faz parte obrigatoriamente do escopo inicial.

---

## 11. Ambientes do Projeto

O projeto deverá possuir três ambientes separados.

### 11.1 Desenvolvimento

Utilizado para programação e testes locais.

Características:

- execução no computador do desenvolvedor;
- dados fictícios;
- liberdade para alterações;
- banco exclusivo de desenvolvimento;
- ferramentas de depuração habilitadas.

### 11.2 QA ou Homologação

Utilizado para validar o sistema antes da publicação.

Características:

- configuração semelhante à produção;
- dados de teste;
- banco separado;
- validação funcional;
- testes de interface;
- testes de permissões;
- verificação das migrations;
- aprovação antes da liberação.

### 11.3 Produção

Utilizado com dados reais.

Características:

- banco exclusivo;
- configurações seguras;
- depuração desabilitada;
- HTTPS;
- backups;
- logs;
- controle de acesso;
- processo controlado de publicação.

---

## 12. Escopo da Primeira Versão

A primeira versão funcional, ou MVP, deverá incluir:

1. projeto Django configurado;
2. conexão com um banco PostgreSQL no Supabase;
3. tela de login;
4. proteção das páginas internas;
5. cadastro de Pessoa Física;
6. cadastro de Pessoa Jurídica;
7. validação de CPF e CNPJ;
8. prevenção de documentos duplicados;
9. edição de clientes;
10. pesquisa e listagem;
11. ativação e inativação;
12. dashboard básico;
13. relatório inicial;
14. registro das datas de criação e atualização;
15. configuração separada para desenvolvimento, QA e produção;
16. testes das regras principais.

---

## 13. Itens Fora do Escopo Inicial

Os seguintes itens não fazem parte obrigatoriamente da primeira versão:

- aplicativo mobile nativo;
- integração com WhatsApp;
- envio automático de e-mails;
- emissão de notas fiscais;
- controle financeiro;
- vendas e contratos;
- integração com serviços externos de consulta de CPF ou CNPJ;
- múltiplos perfis avançados de usuários;
- assinatura eletrônica;
- importação em massa;
- automações de marketing;
- portal de autoatendimento para clientes;
- API pública;
- histórico completo de auditoria.

Esses itens poderão ser avaliados como evoluções futuras.

---

## 14. Premissas

O planejamento considera inicialmente que:

- o sistema será uma aplicação web;
- o proprietário será o único usuário da primeira versão;
- os dados serão armazenados no PostgreSQL do Supabase;
- o Django será responsável pelas regras de negócio e autenticação;
- o sistema trabalhará com clientes PF e PJ;
- CPF ou CNPJ será obrigatório e único;
- os ambientes terão bancos separados;
- os primeiros dados utilizados em desenvolvimento e QA serão fictícios;
- a estrutura poderá evoluir para múltiplos usuários.

---

## 15. Riscos Iniciais

### 15.1 Escopo crescer durante o desenvolvimento

O cadastro de clientes poderá evoluir rapidamente para CRM, financeiro, agenda ou vendas.

**Tratamento:** manter uma lista de funcionalidades futuras e proteger o escopo do MVP.

### 15.2 Dados duplicados ou inconsistentes

Cadastros manuais podem produzir registros repetidos ou mal formatados.

**Tratamento:** validações, campos únicos, padronização e alertas.

### 15.3 Uso inadequado de dados pessoais

A coleta excessiva ou o acesso indevido pode gerar riscos de privacidade.

**Tratamento:** minimização de dados, autenticação, controle de acesso e documentação da finalidade.

### 15.4 Mistura entre ambientes

A utilização do mesmo banco em desenvolvimento, QA e produção pode causar perda ou exposição de dados.

**Tratamento:** projetos, bancos, credenciais e variáveis separados.

### 15.5 Alterações não controladas no banco

Mudanças manuais podem gerar divergência entre o código e o banco.

**Tratamento:** utilizar migrations do Django e um processo definido de publicação.

---

## 16. Critérios Iniciais de Aceitação

A primeira versão poderá ser considerada funcional quando:

- o usuário conseguir realizar login;
- páginas internas não forem acessíveis sem autenticação;
- for possível cadastrar uma Pessoa Física com CPF válido;
- for possível cadastrar uma Pessoa Jurídica com CNPJ válido;
- CPF e CNPJ duplicados forem rejeitados;
- o usuário conseguir editar um cliente;
- o usuário conseguir pesquisar um cliente;
- o usuário conseguir ativar ou inativar um cadastro;
- o dashboard apresentar indicadores básicos;
- existir pelo menos um relatório funcional;
- os dados forem armazenados no banco correto;
- desenvolvimento, QA e produção utilizarem configurações separadas;
- as principais regras possuírem testes;
- nenhuma senha de banco estiver versionada no repositório.

---

## 17. Estratégia de Desenvolvimento

O desenvolvimento será incremental.

Cada funcionalidade seguirá o ciclo:

```text
Definir
   |
   v
Modelar
   |
   v
Implementar
   |
   v
Testar localmente
   |
   v
Revisar
   |
   v
Publicar em QA
   |
   v
Homologar
   |
   v
Publicar em produção
```

Ordem inicial sugerida:

1. setup do projeto;
2. configuração dos ambientes;
3. autenticação;
4. modelagem de clientes;
5. cadastro;
6. edição;
7. pesquisa;
8. dashboard;
9. relatórios;
10. preparação de QA;
11. preparação de produção;
12. monitoramento e evolução.

---

## 18. Próximas Etapas do Projeto

Após a aprovação deste documento, as próximas etapas serão:

### Etapa 2 — Detalhamento dos requisitos

Definir:

- todos os campos de Pessoa Física;
- todos os campos de Pessoa Jurídica;
- campos obrigatórios e opcionais;
- regras de endereço e contato;
- regras de ativação e inativação;
- filtros de pesquisa;
- indicadores do dashboard;
- relatórios da primeira versão.

### Etapa 3 — Setup e ambientes

Preparar:

- Python;
- ambiente virtual;
- Django;
- Git;
- repositório;
- estrutura de configurações;
- variáveis de ambiente;
- Supabase de desenvolvimento;
- Supabase de QA;
- Supabase de produção;
- estratégia de deploy.

### Etapa 4 — Wireframes

Definir se o sistema utilizará:

- telas separadas;
- painel único;
- navegação por abas;
- combinação entre dashboard e telas de operação.

### Etapa 5 — Modelo de dados

Criar:

- entidades;
- campos;
- relacionamentos;
- restrições;
- índices;
- regras de integridade;
- estratégia de auditoria.

### Etapa 6 — Planejamento do MVP

Transformar o escopo em funcionalidades menores, com critérios de aceitação e ordem de implementação.

---

## 19. Conclusão

O escopo inicial está suficientemente definido para avançar para o detalhamento dos requisitos e, posteriormente, para o setup técnico.

O sistema será uma aplicação web de uso inicialmente individual, voltada ao cadastro e consulta de clientes Pessoa Física e Pessoa Jurídica. O Django concentrará a aplicação, a autenticação e as regras de negócio, enquanto o Supabase fornecerá o banco PostgreSQL.

A primeira versão priorizará segurança, organização, pesquisa, validação de CPF e CNPJ, privacidade, dashboard e relatórios básicos. A arquitetura deverá permitir a evolução futura para novos usuários, integrações e módulos, sem ampliar prematuramente o escopo do MVP.
