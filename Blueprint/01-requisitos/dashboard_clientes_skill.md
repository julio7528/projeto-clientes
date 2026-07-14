# Skill — Dashboard de Clientes

## 1. Objetivo

Este documento define os requisitos funcionais e o comportamento do dashboard do sistema de cadastro de clientes.

O dashboard deverá apresentar uma visão rápida e consolidada da base de clientes, permitindo acompanhar volume, distribuição, situação dos cadastros e evolução ao longo do tempo.

---

## 2. Escopo do Dashboard

O dashboard deverá permitir:

- visualizar indicadores principais;
- acompanhar a quantidade de clientes;
- comparar Pessoa Física e Pessoa Jurídica;
- acompanhar clientes ativos e inativos;
- analisar cadastros por período;
- visualizar distribuição por cidade e estado;
- identificar cadastros incompletos;
- aplicar filtros;
- acessar rapidamente outras áreas do sistema.

---

## 3. Indicadores Principais

O dashboard deverá apresentar cartões de resumo.

### 3.1 Total de clientes

Exibe a quantidade total de clientes cadastrados.

```text
Total de clientes
250
```

### 3.2 Pessoas Físicas

Exibe a quantidade de clientes do tipo PF.

```text
Pessoas Físicas
180
```

### 3.3 Pessoas Jurídicas

Exibe a quantidade de clientes do tipo PJ.

```text
Pessoas Jurídicas
70
```

### 3.4 Clientes ativos

Exibe a quantidade de clientes com situação ativa.

```text
Clientes ativos
230
```

### 3.5 Clientes inativos

Exibe a quantidade de clientes com situação inativa.

```text
Clientes inativos
20
```

### 3.6 Novos clientes no período

Exibe a quantidade de clientes cadastrados dentro do período selecionado.

```text
Novos clientes no período
15
```

### 3.7 Cadastros incompletos

Exibe a quantidade de clientes com campos opcionais relevantes não preenchidos.

```text
Cadastros incompletos
32
```

---

## 4. Filtros do Dashboard

O dashboard deverá permitir aplicar filtros aos indicadores e gráficos.

### 4.1 Período

Opções sugeridas:

- hoje;
- últimos 7 dias;
- últimos 30 dias;
- mês atual;
- ano atual;
- período personalizado;
- todos os períodos.

### 4.2 Tipo de cliente

Opções:

- todos;
- Pessoa Física;
- Pessoa Jurídica.

### 4.3 Situação

Opções:

- todos;
- ativos;
- inativos.

### 4.4 Estado

Permite selecionar uma unidade federativa.

### 4.5 Cidade

Permite filtrar por cidade.

---

## 5. Comportamento dos Filtros

Os filtros deverão afetar:

- cartões de indicadores;
- gráficos;
- tabelas resumidas;
- rankings;
- atalhos contextuais.

Os filtros poderão ser combinados.

Exemplo:

```text
Período: Ano atual
Tipo: Pessoa Jurídica
Estado: MT
Situação: Ativo
```

Os resultados deverão considerar apenas os clientes que atendam a todos os critérios selecionados.

---

## 6. Período Padrão

Ao abrir o dashboard, o filtro padrão deverá ser:

```text
Todos os períodos
```

Como alternativa futura, o sistema poderá lembrar o último período utilizado pelo usuário.

---

## 7. Gráficos da Primeira Versão

### 7.1 Distribuição por tipo de cliente

Apresenta a proporção entre:

- Pessoa Física;
- Pessoa Jurídica.

Formato sugerido:

- gráfico de rosca;
- gráfico de pizza;
- gráfico de barras.

### 7.2 Distribuição por situação

Apresenta a proporção entre:

- clientes ativos;
- clientes inativos.

Formato sugerido:

- gráfico de rosca;
- gráfico de barras.

### 7.3 Novos clientes por período

Apresenta a evolução dos novos cadastros.

Agrupamento automático:

- por dia para períodos curtos;
- por semana para períodos intermediários;
- por mês para períodos longos;
- por ano para visão histórica.

Formato sugerido:

- gráfico de linha;
- gráfico de barras.

### 7.4 Clientes por estado

Apresenta os estados com maior quantidade de clientes.

Formato sugerido:

- gráfico de barras horizontais.

Quantidade inicial:

```text
10 estados com mais clientes
```

### 7.5 Clientes por cidade

Apresenta as cidades com maior quantidade de clientes.

Formato sugerido:

- gráfico de barras horizontais.

Quantidade inicial:

```text
10 cidades com mais clientes
```

### 7.6 Cadastros incompletos

Apresenta os campos opcionais que mais estão ausentes.

Exemplos:

- sem e-mail;
- sem data de nascimento ou abertura;
- sem endereço;
- sem número;
- sem bairro;
- sem cidade;
- sem estado.

Formato sugerido:

- gráfico de barras.

---

## 8. Tabelas Resumidas

O dashboard poderá incluir pequenas tabelas de apoio.

### 8.1 Clientes cadastrados recentemente

Colunas sugeridas:

| Coluna | Descrição |
|---|---|
| Nome | Nome completo ou empresarial |
| Tipo | PF ou PJ |
| Cidade/UF | Localização |
| Criado em | Data de criação |
| Ação | Visualizar cadastro |

Quantidade inicial:

```text
5 clientes mais recentes
```

### 8.2 Clientes atualizados recentemente

Colunas sugeridas:

| Coluna | Descrição |
|---|---|
| Nome | Nome completo ou empresarial |
| Tipo | PF ou PJ |
| Atualizado em | Data da última atualização |
| Ação | Visualizar cadastro |

Quantidade inicial:

```text
5 clientes atualizados recentemente
```

### 8.3 Cadastros incompletos prioritários

Apresenta clientes com maior quantidade de campos ausentes.

Colunas sugeridas:

| Coluna | Descrição |
|---|---|
| Nome | Cliente |
| Tipo | PF ou PJ |
| Campos ausentes | Resumo |
| Ação | Editar cadastro |

---

## 9. Atalhos Rápidos

O dashboard deverá apresentar atalhos para:

- cadastrar novo cliente;
- pesquisar clientes;
- abrir relatórios;
- visualizar cadastros incompletos;
- visualizar clientes inativos.

---

## 10. Interação com Indicadores

Os cartões e gráficos poderão funcionar como atalhos.

Exemplos:

- clicar em Pessoas Físicas abre a pesquisa filtrada por PF;
- clicar em Clientes inativos abre a pesquisa filtrada por inativos;
- clicar em Cadastros incompletos abre o relatório correspondente;
- clicar em uma cidade abre a pesquisa filtrada pela cidade;
- clicar em um estado abre a pesquisa filtrada pelo estado.

Essa interação deverá preservar o contexto do filtro aplicado.

---

## 11. Atualização dos Dados

O dashboard deverá carregar dados atuais a partir do banco.

Na primeira versão:

- os dados serão atualizados ao abrir a página;
- os dados serão atualizados ao alterar filtros;
- poderá existir um botão Atualizar.

Texto sugerido:

```text
Atualizar dados
```

Atualização automática em tempo real não será obrigatória na primeira versão.

---

## 12. Informação de Última Atualização

O dashboard deverá informar quando os dados foram carregados.

Exemplo:

```text
Atualizado em 13/07/2026 às 21:30
```

---

## 13. Estado de Carregamento

Enquanto os dados estiverem sendo consultados, a interface deverá exibir:

- indicadores de carregamento;
- esqueletos de cartões;
- mensagens curtas;
- bloqueio apenas das áreas em atualização.

Mensagem sugerida:

```text
Carregando indicadores...
```

---

## 14. Estado sem Dados

Quando a base estiver vazia:

```text
Ainda não há clientes cadastrados.
```

O dashboard deverá destacar o botão:

```text
Cadastrar primeiro cliente
```

Os gráficos não deverão apresentar erros ou valores indefinidos.

---

## 15. Estado sem Resultados para o Filtro

Quando existirem clientes, mas nenhum atender aos filtros:

```text
Nenhum dado encontrado para os filtros selecionados.
```

A tela deverá oferecer:

- limpar filtros;
- selecionar outro período;
- retornar à visão geral.

---

## 16. Privacidade

O dashboard deverá apresentar apenas dados consolidados e informações mínimas de identificação.

Não deverá exibir diretamente:

- CPF completo;
- CNPJ completo;
- endereço completo;
- observações;
- dados desnecessários para a visão gerencial.

As tabelas resumidas poderão exibir apenas:

- nome;
- tipo;
- cidade;
- estado;
- datas;
- situação.

---

## 17. Segurança

O dashboard deverá:

- exigir autenticação;
- respeitar permissões;
- validar filtros no backend;
- impedir acesso direto não autorizado;
- evitar exposição de dados pessoais;
- registrar erros técnicos em log;
- limitar consultas excessivas.

---

## 18. Desempenho

O dashboard deverá utilizar consultas agregadas e otimizadas.

Boas práticas previstas:

- contagens realizadas no banco;
- agrupamentos realizados no banco;
- uso de índices;
- limitação de rankings;
- carregamento eficiente;
- evitar buscar registros completos quando apenas totais forem necessários;
- cache futuro para indicadores de maior custo.

---

## 19. Responsividade

Em computadores:

- cartões poderão ser exibidos em várias colunas;
- gráficos poderão ser organizados lado a lado;
- tabelas resumidas poderão ocupar a largura disponível.

Em celulares:

- cartões deverão ser empilhados;
- gráficos deverão se ajustar à largura;
- filtros poderão ser recolhidos;
- tabelas poderão ser exibidas como cartões;
- atalhos deverão permanecer acessíveis.

---

## 20. Acessibilidade

O dashboard deverá:

- possuir títulos claros;
- permitir navegação por teclado;
- apresentar valores em texto além dos gráficos;
- não depender apenas de cor;
- possuir contraste adequado;
- oferecer descrição dos gráficos;
- informar mudanças de filtro;
- manter foco visível.

---

## 21. Fluxo Resumido

```text
Abrir dashboard
    |
    v
Carregar indicadores
    |
    v
Carregar gráficos e resumos
    |
    v
Aplicar filtros
    |
    v
Atualizar dados
    |
    v
Acessar pesquisa, relatório ou cadastro
```

---

## 22. Critérios de Aceitação

A funcionalidade será considerada concluída quando:

- o total de clientes for exibido;
- a quantidade de PF for exibida;
- a quantidade de PJ for exibida;
- a quantidade de ativos for exibida;
- a quantidade de inativos for exibida;
- novos clientes no período forem calculados;
- cadastros incompletos forem contabilizados;
- os filtros puderem ser combinados;
- os cartões responderem aos filtros;
- os gráficos responderem aos filtros;
- a distribuição por tipo funcionar;
- a distribuição por situação funcionar;
- a evolução por período funcionar;
- os rankings por cidade e estado funcionarem;
- clientes recentes forem exibidos;
- atalhos rápidos funcionarem;
- o acesso exigir autenticação;
- o dashboard funcionar sem dados;
- o dashboard funcionar sem resultados para filtros;
- nenhuma informação sensível for exposta desnecessariamente.

---

## 23. Decisões Aprovadas

- dashboard com visão consolidada da base;
- cartões com indicadores principais;
- filtros por período, tipo, situação, cidade e estado;
- gráficos por tipo, situação, período, cidade e estado;
- acompanhamento de cadastros incompletos;
- tabelas resumidas de clientes recentes;
- atalhos para cadastro, pesquisa e relatórios;
- interação entre indicadores e telas filtradas;
- dados atualizados ao carregar e alterar filtros;
- privacidade e segurança aplicadas desde a primeira versão;
- estrutura responsiva e acessível.
