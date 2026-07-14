# Skill — Wireframes e Navegação do Sistema

## 1. Objetivo

Este documento define a estrutura visual, os wireframes textuais e a navegação do sistema de cadastro de clientes.

O objetivo é estabelecer como o usuário acessará e utilizará:

- login;
- dashboard;
- cadastro de clientes;
- edição de clientes;
- pesquisa;
- visualização de detalhes;
- relatórios;
- filtros;
- ações rápidas;
- mensagens e estados da interface.

Este documento deverá orientar:

- design da interface;
- desenvolvimento frontend;
- organização das URLs;
- definição dos templates Django;
- testes de usabilidade;
- testes responsivos;
- critérios de aceitação das telas.

---

## 2. Decisão de Arquitetura da Interface

A interface utilizará uma estrutura híbrida.

A aplicação terá:

- dashboard como página inicial;
- cadastro e edição em telas próprias;
- pesquisa e listagem em uma área própria;
- detalhes do cliente em tela própria;
- relatórios em uma área própria;
- navegação principal persistente;
- atalhos entre módulos.

A estrutura híbrida foi escolhida porque:

- organiza melhor as funcionalidades;
- reduz excesso de informações em uma única tela;
- facilita manutenção;
- melhora a navegação;
- permite evolução futura;
- funciona melhor em computador e celular;
- evita uma tela única excessivamente complexa.

---

## 3. Estrutura Geral da Aplicação

```text
Login
   |
   v
Dashboard
   |
   +--> Novo cliente
   |
   +--> Pesquisar clientes
   |
   +--> Relatórios
   |
   +--> Clientes recentes
   |
   +--> Cadastros incompletos
```

A aplicação interna possuirá um layout principal compartilhado.

```text
+------------------------------------------------------------+
| Cabeçalho                                                  |
+----------------------+-------------------------------------+
| Menu lateral         | Conteúdo da página                  |
|                      |                                     |
| Dashboard            | Título                              |
| Clientes             | Breadcrumb                          |
| Novo cliente         | Conteúdo específico                 |
| Relatórios           |                                     |
|                      |                                     |
| Sair                 |                                     |
+----------------------+-------------------------------------+
```

---

## 4. Mapa de Navegação

```text
/login
   |
   v
/dashboard
   |
   +--> /clientes
   |       |
   |       +--> /clientes/novo
   |       |
   |       +--> /clientes/{id}
   |       |
   |       +--> /clientes/{id}/editar
   |       |
   |       +--> /clientes/{id}/ativar
   |       |
   |       +--> /clientes/{id}/inativar
   |
   +--> /relatorios
   |       |
   |       +--> /relatorios/clientes
   |       |
   |       +--> /relatorios/tipos
   |       |
   |       +--> /relatorios/situacoes
   |       |
   |       +--> /relatorios/localidades
   |       |
   |       +--> /relatorios/periodos
   |       |
   |       +--> /relatorios/incompletos
   |
   +--> /perfil
   |
   +--> /logout
```

As URLs são conceituais e poderão ser ajustadas durante o setup técnico.

---

## 5. Navegação Principal

A navegação principal deverá estar disponível após o login.

Itens:

- Dashboard;
- Clientes;
- Novo cliente;
- Relatórios;
- Perfil;
- Sair.

### 5.1 Dashboard

Leva para a visão geral.

### 5.2 Clientes

Leva para a pesquisa e listagem.

### 5.3 Novo cliente

Leva diretamente ao formulário de cadastro.

### 5.4 Relatórios

Leva para a área de relatórios.

### 5.5 Perfil

Leva para configurações básicas da conta.

### 5.6 Sair

Encerra a sessão.

---

## 6. Comportamento do Menu

Em telas grandes:

- menu lateral fixo;
- ícone e texto;
- item atual destacado;
- possibilidade futura de recolher o menu;
- botão Sair na parte inferior.

Em telas pequenas:

- menu oculto;
- botão de abertura no cabeçalho;
- menu exibido como painel lateral;
- fechamento ao selecionar um item;
- fechamento ao tocar fora do painel.

---

## 7. Cabeçalho

O cabeçalho interno deverá conter:

- botão de menu em telas pequenas;
- nome do sistema;
- título opcional da seção;
- usuário autenticado;
- acesso ao perfil;
- opção de sair.

Wireframe:

```text
+------------------------------------------------------------+
| ☰  Sistema de Clientes                    Júlio ▼           |
+------------------------------------------------------------+
```

---

## 8. Breadcrumb

As telas internas deverão exibir breadcrumb.

Exemplos:

```text
Dashboard
```

```text
Clientes > Pesquisa
```

```text
Clientes > João da Silva
```

```text
Clientes > João da Silva > Editar
```

```text
Relatórios > Clientes por estado
```

O breadcrumb deverá ajudar o usuário a entender sua posição e retornar a níveis anteriores.

---

# PARTE I — TELA DE LOGIN

## 9. Objetivo da Tela de Login

Permitir acesso seguro ao sistema.

---

## 10. Wireframe da Tela de Login — Desktop

```text
+------------------------------------------------------------+
|                                                            |
|                  SISTEMA DE CLIENTES                       |
|                                                            |
|              +----------------------------+                |
|              | Entrar no sistema          |                |
|              |                            |                |
|              | Usuário ou e-mail          |                |
|              | [________________________] |                |
|              |                            |                |
|              | Senha                      |                |
|              | [____________________] 👁  |                |
|              |                            |                |
|              | [ ] Lembrar acesso         |                |
|              |                            |                |
|              | [        ENTRAR         ]  |                |
|              |                            |                |
|              | Esqueci minha senha        |                |
|              +----------------------------+                |
|                                                            |
+------------------------------------------------------------+
```

---

## 11. Wireframe da Tela de Login — Mobile

```text
+------------------------------+
|                              |
|     SISTEMA DE CLIENTES      |
|                              |
| Entrar no sistema            |
|                              |
| Usuário ou e-mail            |
| [________________________]   |
|                              |
| Senha                        |
| [____________________] 👁    |
|                              |
| [ ] Lembrar acesso           |
|                              |
| [         ENTRAR          ]  |
|                              |
| Esqueci minha senha          |
|                              |
+------------------------------+
```

---

## 12. Comportamento do Login

- usuário e senha obrigatórios;
- botão Entrar desabilitado durante autenticação;
- senha oculta por padrão;
- opção de exibir ou ocultar senha;
- mensagem clara em caso de erro;
- redirecionamento ao dashboard após sucesso;
- redirecionamento ao login quando a sessão expirar.

Mensagens:

```text
Informe seu usuário ou e-mail.
```

```text
Informe sua senha.
```

```text
Usuário ou senha inválidos.
```

```text
Sua sessão expirou. Entre novamente.
```

---

# PARTE II — DASHBOARD

## 13. Wireframe do Dashboard — Desktop

```text
+------------------------------------------------------------+
| Cabeçalho                                                  |
+----------------------+-------------------------------------+
| Menu                 | Dashboard                           |
|                      | Visão geral da base de clientes     |
| Dashboard            |                                     |
| Clientes             | [Período ▼] [Tipo ▼] [Situação ▼]  |
| Novo cliente         | [Estado ▼] [Cidade ▼] [Atualizar]   |
| Relatórios           |                                     |
|                      | +----------+ +----------+ +--------+ |
|                      | | Total    | | PF       | | PJ     | |
|                      | | 250      | | 180      | | 70     | |
|                      | +----------+ +----------+ +--------+ |
|                      |                                     |
|                      | +----------+ +----------+ +--------+ |
|                      | | Ativos   | | Inativos | | Novos  | |
|                      | | 230      | | 20       | | 15     | |
|                      | +----------+ +----------+ +--------+ |
|                      |                                     |
|                      | +----------------+ +---------------+ |
|                      | | Tipo cliente   | | Situação      | |
|                      | | gráfico        | | gráfico       | |
|                      | +----------------+ +---------------+ |
|                      |                                     |
|                      | +----------------------------------+ |
|                      | | Novos clientes por período       | |
|                      | | gráfico                          | |
|                      | +----------------------------------+ |
|                      |                                     |
|                      | +----------------+ +---------------+ |
|                      | | Estados        | | Cidades       | |
|                      | | ranking        | | ranking       | |
|                      | +----------------+ +---------------+ |
|                      |                                     |
|                      | Clientes recentes                   |
|                      | [tabela resumida]                   |
+----------------------+-------------------------------------+
```

---

## 14. Wireframe do Dashboard — Mobile

```text
+------------------------------+
| ☰ Sistema de Clientes  Júlio |
+------------------------------+
| Dashboard                    |
| Visão geral                  |
|                              |
| [ Filtros ]   [ Atualizar ]  |
|                              |
| +--------------------------+ |
| | Total de clientes   250  | |
| +--------------------------+ |
| | Pessoas Físicas     180  | |
| +--------------------------+ |
| | Pessoas Jurídicas    70  | |
| +--------------------------+ |
| | Ativos              230  | |
| +--------------------------+ |
| | Inativos             20  | |
| +--------------------------+ |
|                              |
| Distribuição por tipo        |
| [ gráfico responsivo ]       |
|                              |
| Novos clientes               |
| [ gráfico responsivo ]       |
|                              |
| Clientes recentes            |
| [ cartões ]                  |
+------------------------------+
```

---

## 15. Navegação a Partir do Dashboard

Interações:

- Total de clientes → lista completa;
- Pessoas Físicas → clientes filtrados por PF;
- Pessoas Jurídicas → clientes filtrados por PJ;
- Ativos → clientes ativos;
- Inativos → clientes inativos;
- Cadastros incompletos → relatório de incompletos;
- cidade do ranking → pesquisa filtrada;
- estado do ranking → pesquisa filtrada;
- cliente recente → detalhes do cliente.

---

# PARTE III — PESQUISA E LISTAGEM

## 16. Wireframe da Pesquisa — Desktop

```text
+------------------------------------------------------------+
| Clientes                                                   |
| Pesquise e gerencie os cadastros                           |
|                                                            |
| [ Buscar cliente____________________________ ] [Pesquisar] |
|                                                            |
| [Tipo ▼] [Situação ▼] [Estado ▼] [Cidade____]              |
| [Criação inicial] [Criação final] [Mais filtros]           |
|                                                            |
| [Limpar filtros]                         [+ Novo cliente]   |
|                                                            |
| 35 clientes encontrados                                    |
|                                                            |
| +--------------------------------------------------------+ |
| | Nome | Tipo | Documento | Telefone | Cidade | Situação | |
| |--------------------------------------------------------| |
| | João | PF   | ***...**  | (65)...  | Sorriso| Ativo   | |
| | Empresa X|PJ| **...**   | (65)...  | Cuiabá | Ativo   | |
| +--------------------------------------------------------+ |
|                                                            |
| [< Anterior] Página 1 de 2 [Próxima >]                    |
+------------------------------------------------------------+
```

---

## 17. Wireframe da Pesquisa — Mobile

```text
+------------------------------+
| ☰ Clientes                   |
+------------------------------+
| [ Buscar cliente__________ ] |
| [ Pesquisar ]                |
|                              |
| [ Filtros ▼ ]                |
|                              |
| 35 clientes encontrados      |
|                              |
| +--------------------------+ |
| | João da Silva            | |
| | PF • Ativo               | |
| | ***.456.789-**           | |
| | Sorriso/MT               | |
| | [Ver] [Editar] [⋮]       | |
| +--------------------------+ |
|                              |
| +--------------------------+ |
| | Empresa Exemplo          | |
| | PJ • Ativo               | |
| | **.345.678/0001-**       | |
| | Cuiabá/MT                | |
| | [Ver] [Editar] [⋮]       | |
| +--------------------------+ |
|                              |
| [<] Página 1 de 2 [>]       |
+------------------------------+
```

---

## 18. Comportamento da Pesquisa

- pesquisa executada pelo botão;
- filtros combináveis;
- resultados preservados ao retornar;
- filtros ativos visíveis;
- paginação mantém pesquisa;
- ordenação mantém filtros;
- busca aceita documento com ou sem máscara;
- busca aceita nome parcial;
- telefone e e-mail podem ser pesquisados;
- documentos mascarados na listagem.

---

## 19. Ações da Listagem

Ações diretas:

- visualizar;
- editar;
- ativar;
- inativar.

No desktop:

```text
[Visualizar] [Editar] [Inativar]
```

No mobile:

```text
[Ver] [Editar] [⋮]
```

O menu adicional poderá conter:

- ativar;
- inativar;
- copiar telefone;
- copiar e-mail.

---

# PARTE IV — CADASTRO DE CLIENTE

## 20. Estrutura do Formulário

O formulário será dividido em seções:

1. Tipo e identificação;
2. Contato;
3. Endereço;
4. Informações complementares;
5. Situação;
6. Ações.

---

## 21. Wireframe de Cadastro — Desktop

```text
+------------------------------------------------------------+
| Clientes > Novo cliente                                    |
|                                                            |
| Novo cliente                                               |
| Cadastre uma Pessoa Física ou Jurídica                     |
|                                                            |
| IDENTIFICAÇÃO                                              |
| Tipo de cliente *                                          |
| ( ) Pessoa Física   ( ) Pessoa Jurídica                    |
|                                                            |
| Nome completo *              CPF *                         |
| [____________________]       [___.___.___-__]              |
|                                                            |
| Data de nascimento                                         |
| [__/__/____]                                               |
|                                                            |
| CONTATO                                                    |
| Telefone principal *         E-mail                        |
| [(65) 99999-9999____]        [________________________]    |
|                                                            |
| ENDEREÇO                                                   |
| CEP *                        [Buscar CEP]                   |
| [_____-___]                                                |
|                                                            |
| Endereço                     Número                        |
| [____________________]       [________]                    |
|                                                            |
| Complemento                  Bairro                        |
| [____________________]       [________________]            |
|                                                            |
| Cidade                       Estado                        |
| [____________________]       [MT ▼]                        |
|                                                            |
| INFORMAÇÕES COMPLEMENTARES                                 |
| Observações                                                |
| [______________________________________________________]   |
| [______________________________________________________]   |
|                                                            |
| Situação: Ativo                                            |
|                                                            |
| [Cancelar]                              [Salvar cliente]   |
+------------------------------------------------------------+
```

---

## 22. Wireframe de Cadastro PJ — Desktop

```text
+------------------------------------------------------------+
| Tipo de cliente *                                          |
| ( ) Pessoa Física   (●) Pessoa Jurídica                    |
|                                                            |
| Nome empresarial *          CNPJ *                         |
| [____________________]       [__.___.___/____-__]           |
|                                                            |
| Data de abertura                                           |
| [__/__/____]                                               |
|                                                            |
| Demais campos iguais ao cadastro PF                        |
+------------------------------------------------------------+
```

---

## 23. Wireframe de Cadastro — Mobile

```text
+------------------------------+
| ☰ Novo cliente               |
+------------------------------+
| Tipo de cliente *            |
| [ PF ] [ PJ ]                |
|                              |
| Nome completo *              |
| [________________________]   |
|                              |
| CPF *                        |
| [___.___.___-__]             |
|                              |
| Data de nascimento           |
| [__/__/____]                 |
|                              |
| Telefone principal *         |
| [________________________]   |
|                              |
| E-mail                       |
| [________________________]   |
|                              |
| CEP *                        |
| [_________] [Buscar]         |
|                              |
| Endereço                     |
| [________________________]   |
|                              |
| Número                       |
| [________________________]   |
|                              |
| Complemento                  |
| [________________________]   |
|                              |
| Bairro                       |
| [________________________]   |
|                              |
| Cidade                       |
| [________________________]   |
|                              |
| Estado                       |
| [ MT ▼ ]                     |
|                              |
| Observações                  |
| [________________________]   |
| [________________________]   |
|                              |
| [Cancelar]                   |
| [Salvar cliente]             |
+------------------------------+
```

---

## 24. Comportamento do Cadastro

- tipo obrigatório;
- rótulos mudam conforme PF ou PJ;
- documento limpo ao trocar tipo;
- CEP consulta endereço;
- campos preenchidos permanecem após erro;
- primeiro erro recebe foco;
- botão Salvar fica desabilitado durante processamento;
- mensagens de erro próximas aos campos;
- sucesso redireciona para detalhes ou lista.

Decisão sugerida:

Após cadastrar, redirecionar para a tela de detalhes do cliente.

---

## 25. Ações do Cadastro

### Salvar cliente

Valida e salva.

### Cancelar

Retorna à pesquisa ou página anterior.

Quando houver dados não salvos:

```text
Existem alterações não salvas. Deseja sair?
```

Opções:

- permanecer;
- sair sem salvar.

---

# PARTE V — DETALHES DO CLIENTE

## 26. Objetivo

Apresentar o cadastro completo sem entrar diretamente em modo de edição.

---

## 27. Wireframe de Detalhes — Desktop

```text
+------------------------------------------------------------+
| Clientes > João da Silva                                   |
|                                                            |
| João da Silva                              [Ativo]          |
| Pessoa Física                                             |
|                                                            |
| [Editar] [Inativar] [Voltar]                               |
|                                                            |
| IDENTIFICAÇÃO                                              |
| CPF: 123.456.789-00                                        |
| Data de nascimento: 10/05/1985                             |
|                                                            |
| CONTATO                                                    |
| Telefone: (65) 99999-9999                                  |
| E-mail: joao@email.com                                     |
|                                                            |
| ENDEREÇO                                                   |
| CEP: 78890-000                                             |
| Rua Exemplo, 123                                           |
| Centro                                                     |
| Sorriso/MT                                                 |
|                                                            |
| OBSERVAÇÕES                                                |
| Cliente cadastrado para acompanhamento comercial.          |
|                                                            |
| CONTROLE                                                   |
| Criado em: 13/07/2026 21:30                                |
| Atualizado em: 13/07/2026 21:30                            |
+------------------------------------------------------------+
```

---

## 28. Wireframe de Detalhes — Mobile

```text
+------------------------------+
| ☰ Cliente                    |
+------------------------------+
| João da Silva                |
| Pessoa Física • Ativo        |
|                              |
| [Editar] [⋮]                 |
|                              |
| Identificação                |
| CPF                          |
| 123.456.789-00               |
|                              |
| Data de nascimento           |
| 10/05/1985                   |
|                              |
| Contato                      |
| (65) 99999-9999              |
| joao@email.com               |
|                              |
| Endereço                     |
| Rua Exemplo, 123             |
| Centro                       |
| Sorriso/MT                   |
|                              |
| Observações                  |
| Texto...                     |
|                              |
| Criado em 13/07/2026         |
| Atualizado em 13/07/2026     |
+------------------------------+
```

---

## 29. Ações nos Detalhes

- editar;
- ativar;
- inativar;
- voltar à pesquisa;
- copiar telefone;
- copiar e-mail;
- visualizar documento completo.

Ações futuras:

- imprimir ficha;
- exportar ficha;
- histórico de alterações.

---

# PARTE VI — EDIÇÃO

## 30. Estrutura da Tela de Edição

A tela de edição reutilizará o formulário de cadastro.

Diferenças:

- campos preenchidos;
- título Editar cliente;
- situação editável;
- botão Atualizar cliente;
- dados de controle exibidos;
- alerta ao alterar tipo.

---

## 31. Wireframe de Edição

```text
+------------------------------------------------------------+
| Clientes > João da Silva > Editar                          |
|                                                            |
| Editar cliente                                             |
|                                                            |
| [formulário preenchido]                                    |
|                                                            |
| Situação                                                   |
| (●) Ativo   ( ) Inativo                                    |
|                                                            |
| Criado em: 13/07/2026                                      |
| Última atualização: 13/07/2026                             |
|                                                            |
| [Cancelar]                            [Atualizar cliente]   |
+------------------------------------------------------------+
```

---

## 32. Comportamento da Edição

- validar novamente todos os campos;
- impedir documento duplicado;
- permitir alterar documento;
- alertar ao trocar PF/PJ;
- registrar atualização automática;
- preservar dados em caso de erro;
- redirecionar para detalhes após sucesso.

Mensagem:

```text
Cliente atualizado com sucesso.
```

---

# PARTE VII — RELATÓRIOS

## 33. Tela Inicial de Relatórios

A tela poderá apresentar cards de tipos de relatório.

Wireframe:

```text
+------------------------------------------------------------+
| Relatórios                                                 |
| Selecione o relatório desejado                             |
|                                                            |
| +------------------+ +------------------+                  |
| | Geral de clientes| | Por tipo         |                  |
| | [Abrir]          | | [Abrir]          |                  |
| +------------------+ +------------------+                  |
|                                                            |
| +------------------+ +------------------+                  |
| | Por situação     | | Por localidade   |                  |
| | [Abrir]          | | [Abrir]          |                  |
| +------------------+ +------------------+                  |
|                                                            |
| +------------------+ +------------------+                  |
| | Por período      | | Incompletos      |                  |
| | [Abrir]          | | [Abrir]          |                  |
| +------------------+ +------------------+                  |
+------------------------------------------------------------+
```

---

## 34. Tela de Relatório

```text
+------------------------------------------------------------+
| Relatórios > Geral de clientes                             |
|                                                            |
| Tipo [Todos ▼]  Situação [Todos ▼]                         |
| Estado [Todos ▼] Cidade [____________]                     |
| Período [__/__/____] até [__/__/____]                      |
|                                                            |
| [Limpar] [Gerar relatório]                                 |
|                                                            |
| Total de clientes: 250                                     |
| PF: 180 | PJ: 70 | Ativos: 230 | Inativos: 20             |
|                                                            |
| [Exportar CSV] [Exportar XLSX] [Exportar PDF] [Imprimir]  |
|                                                            |
| [gráfico, quando aplicável]                                |
|                                                            |
| [tabela de resultados]                                     |
|                                                            |
| [paginação]                                                |
+------------------------------------------------------------+
```

---

## 35. Tela de Relatórios — Mobile

```text
+------------------------------+
| ☰ Relatórios                 |
+------------------------------+
| Geral de clientes            |
|                              |
| [ Filtros ▼ ]                |
| [ Gerar relatório ]          |
|                              |
| Total: 250                   |
| PF: 180                      |
| PJ: 70                       |
|                              |
| [ Exportar ▼ ]               |
|                              |
| [ gráfico responsivo ]       |
|                              |
| [ cartões de resultados ]    |
+------------------------------+
```

---

# PARTE VIII — PERFIL E SESSÃO

## 36. Tela de Perfil

Itens iniciais:

- nome do usuário;
- e-mail;
- alteração de senha;
- encerrar outras sessões, futuramente.

Wireframe:

```text
+------------------------------------------------------------+
| Perfil                                                     |
|                                                            |
| Nome                                                       |
| [Júlio________________________________]                    |
|                                                            |
| E-mail                                                     |
| [email@exemplo.com____________________]                    |
|                                                            |
| [Salvar alterações]                                        |
|                                                            |
| Segurança                                                  |
| [Alterar senha]                                            |
+------------------------------------------------------------+
```

---

## 37. Logout

Ao selecionar Sair:

- sessão encerrada;
- redirecionamento para login;
- páginas internas deixam de ser acessíveis;
- botão Voltar do navegador não deverá reabrir conteúdo protegido.

---

# PARTE IX — COMPONENTES COMPARTILHADOS

## 38. Botões

Tipos:

- primário;
- secundário;
- perigo;
- link;
- ícone.

Exemplos:

```text
Primário: Salvar cliente
Secundário: Cancelar
Perigo: Inativar
Link: Voltar
Ícone: Editar
```

---

## 39. Campos de Formulário

Todos os campos deverão possuir:

- rótulo;
- indicação de obrigatório;
- ajuda opcional;
- mensagem de erro;
- estado normal;
- estado em foco;
- estado desabilitado;
- estado carregando, quando aplicável.

---

## 40. Mensagens Globais

Tipos:

- sucesso;
- erro;
- aviso;
- informação.

Exemplos:

```text
Cliente cadastrado com sucesso.
```

```text
Não foi possível salvar o cliente.
```

```text
Este telefone já está associado a outro cliente.
```

```text
Consultando CEP...
```

---

## 41. Modal de Confirmação

Usado para:

- inativação;
- ativação;
- saída com dados não salvos;
- alteração de tipo PF/PJ;
- exclusão futura.

Wireframe:

```text
+--------------------------------------+
| Confirmar ação                       |
|                                      |
| Deseja realmente inativar este       |
| cliente?                             |
|                                      |
| [Cancelar]          [Inativar]       |
+--------------------------------------+
```

---

## 42. Estado de Carregamento

Componentes:

- spinner;
- texto de carregamento;
- skeleton;
- botão desabilitado.

Exemplos:

```text
Carregando clientes...
```

```text
Salvando...
```

```text
Gerando relatório...
```

---

## 43. Estado Vazio

Cada módulo deverá possuir um estado vazio útil.

Clientes:

```text
Nenhum cliente cadastrado.
[Cadastrar primeiro cliente]
```

Pesquisa:

```text
Nenhum cliente encontrado.
[Limpar filtros]
```

Relatórios:

```text
Nenhum dado encontrado para os filtros selecionados.
```

Dashboard:

```text
Ainda não há clientes cadastrados.
[Cadastrar primeiro cliente]
```

---

# PARTE X — RESPONSIVIDADE

## 44. Breakpoints Conceituais

### Desktop

```text
Largura maior ou igual a 1024 px
```

### Tablet

```text
Largura entre 768 px e 1023 px
```

### Mobile

```text
Largura menor que 768 px
```

Os valores finais poderão ser ajustados conforme o framework CSS escolhido.

---

## 45. Regras para Desktop

- menu lateral visível;
- formulários em duas colunas;
- tabelas completas;
- gráficos lado a lado;
- filtros em linha;
- ações visíveis.

---

## 46. Regras para Tablet

- menu recolhível;
- formulários em uma ou duas colunas;
- tabelas com rolagem horizontal;
- gráficos ajustáveis;
- filtros agrupados.

---

## 47. Regras para Mobile

- menu em painel;
- formulários em uma coluna;
- tabelas convertidas em cartões quando necessário;
- botões em largura total quando apropriado;
- filtros recolhíveis;
- ações secundárias em menu;
- áreas clicáveis maiores;
- teclado adequado para CPF, CNPJ, CEP e telefone.

---

# PARTE XI — ACESSIBILIDADE

## 48. Requisitos

- navegação completa por teclado;
- foco visível;
- rótulos associados aos campos;
- títulos hierárquicos;
- contraste adequado;
- mensagens de erro em texto;
- descrição para ícones;
- gráficos com alternativa textual;
- modais com foco controlado;
- links e botões semanticamente corretos;
- campos obrigatórios identificados.

---

# PARTE XII — PADRÃO VISUAL

## 49. Hierarquia Visual

A interface deverá seguir:

```text
Título da página
Subtítulo ou descrição
Ações principais
Filtros ou formulário
Conteúdo
Ações secundárias
```

---

## 50. Uso de Cores

As cores deverão indicar função.

- cor principal: ações principais;
- verde: sucesso e ativo;
- vermelho: erro e ação destrutiva;
- amarelo: aviso;
- cinza: conteúdo secundário;
- azul ou cor principal: links e navegação.

A cor nunca deverá ser o único indicador.

---

## 51. Espaçamento

Deverá existir espaçamento consistente entre:

- seções;
- campos;
- botões;
- cards;
- tabelas;
- gráficos;
- títulos.

---

## 52. Tipografia

A tipografia deverá priorizar legibilidade.

Sugestão:

- títulos destacados;
- corpo entre 14 e 16 px;
- rótulos claros;
- números de indicadores em destaque;
- evitar excesso de estilos.

---

# PARTE XIII — FLUXOS PRINCIPAIS

## 53. Fluxo de Login

```text
Abrir sistema
    |
    v
Informar credenciais
    |
    v
Validar
    |
    +--> Erro: exibir mensagem
    |
    v
Dashboard
```

---

## 54. Fluxo de Cadastro

```text
Dashboard ou pesquisa
    |
    v
Novo cliente
    |
    v
Selecionar PF ou PJ
    |
    v
Preencher dados
    |
    v
Consultar CEP
    |
    v
Validar
    |
    +--> Erro: permanecer no formulário
    |
    v
Salvar
    |
    v
Detalhes do cliente
```

---

## 55. Fluxo de Pesquisa e Edição

```text
Clientes
    |
    v
Pesquisar
    |
    v
Selecionar cliente
    |
    v
Detalhes
    |
    v
Editar
    |
    v
Salvar alterações
    |
    v
Detalhes atualizados
```

---

## 56. Fluxo de Inativação

```text
Pesquisa ou detalhes
    |
    v
Selecionar Inativar
    |
    v
Confirmar
    |
    +--> Cancelar
    |
    v
Atualizar situação
    |
    v
Exibir sucesso
```

---

## 57. Fluxo de Relatório

```text
Relatórios
    |
    v
Selecionar tipo
    |
    v
Aplicar filtros
    |
    v
Gerar
    |
    v
Visualizar resultados
    |
    +--> Exportar
    |
    +--> Imprimir
```

---

# PARTE XIV — ORGANIZAÇÃO SUGERIDA DE TEMPLATES

## 58. Templates Compartilhados

```text
templates/
├── base.html
├── partials/
│   ├── header.html
│   ├── sidebar.html
│   ├── breadcrumb.html
│   ├── messages.html
│   ├── pagination.html
│   └── modal.html
```

---

## 59. Templates de Autenticação

```text
templates/
└── registration/
    ├── login.html
    ├── password_change_form.html
    └── password_change_done.html
```

---

## 60. Templates de Clientes

```text
templates/
└── clientes/
    ├── lista.html
    ├── formulario.html
    ├── detalhe.html
    ├── confirmar_ativacao.html
    └── confirmar_inativacao.html
```

---

## 61. Templates de Dashboard

```text
templates/
└── dashboard/
    └── index.html
```

---

## 62. Templates de Relatórios

```text
templates/
└── relatorios/
    ├── index.html
    ├── geral.html
    ├── por_tipo.html
    ├── por_situacao.html
    ├── por_localidade.html
    ├── por_periodo.html
    └── incompletos.html
```

---

# PARTE XV — CRITÉRIOS DE ACEITAÇÃO

## 63. Navegação Geral

- menu disponível após login;
- item atual destacado;
- breadcrumb correto;
- navegação funcional;
- logout encerra sessão;
- páginas protegidas exigem autenticação.

---

## 64. Login

- usuário consegue entrar;
- credenciais inválidas geram mensagem;
- senha pode ser exibida ou ocultada;
- sessão expirada redireciona ao login;
- layout funciona em desktop e mobile.

---

## 65. Dashboard

- indicadores carregam;
- filtros atualizam dados;
- cartões direcionam para telas filtradas;
- gráficos funcionam;
- estados vazio e carregando funcionam;
- layout responsivo.

---

## 66. Pesquisa

- busca geral funciona;
- filtros funcionam;
- paginação preserva filtros;
- resultados aparecem em tabela ou cartões;
- ações funcionam;
- documentos aparecem mascarados.

---

## 67. Cadastro

- tipo PF/PJ altera rótulos;
- documento muda de máscara;
- CEP preenche endereço;
- erros aparecem próximos aos campos;
- dados permanecem após erro;
- sucesso redireciona para detalhes;
- aviso de dados não salvos funciona.

---

## 68. Detalhes

- dados completos são exibidos;
- ações de editar e inativar funcionam;
- layout é legível;
- informações de controle aparecem;
- documentos podem ser exibidos conforme permissão.

---

## 69. Edição

- formulário carrega preenchido;
- alterações são salvas;
- duplicidade é validada;
- troca de tipo gera alerta;
- data de atualização é modificada.

---

## 70. Relatórios

- tipos de relatório podem ser selecionados;
- filtros funcionam;
- resultados aparecem;
- exportações funcionam;
- gráficos e tabelas são responsivos;
- documentos permanecem protegidos.

---

# PARTE XVI — DECISÕES APROVADAS

## 71. Decisões de Interface

- arquitetura híbrida;
- dashboard separado;
- pesquisa em tela própria;
- cadastro em tela própria;
- edição reutiliza o formulário;
- detalhes em tela própria;
- relatórios em módulo próprio;
- menu lateral em desktop;
- menu recolhível em mobile;
- breadcrumb;
- formulários divididos por seções;
- tabelas no desktop;
- cartões no mobile;
- mensagens claras;
- estados de carregamento e vazio;
- acessibilidade;
- responsividade.

---

# PARTE XVII — PRÓXIMA ETAPA

## 72. Próxima Etapa do Projeto

Após a definição dos wireframes e da navegação, a próxima etapa será:

```text
Modelagem de Dados
```

Nessa etapa deverão ser definidos:

- entidade Cliente;
- campos;
- tipos de dados;
- tamanhos;
- obrigatoriedade;
- valores padrão;
- restrições;
- índices;
- unicidade;
- regras de integridade;
- auditoria;
- relacionamento com usuário;
- preparação para migrations do Django;
- compatibilidade com PostgreSQL do Supabase.

A modelagem deverá transformar as definições funcionais deste projeto em uma estrutura de banco de dados pronta para implementação.
