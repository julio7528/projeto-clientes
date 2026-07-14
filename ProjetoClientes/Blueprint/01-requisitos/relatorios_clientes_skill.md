# Skill — Relatórios de Clientes

## 1. Objetivo

Este documento define os requisitos funcionais da área de relatórios do sistema de cadastro de clientes.

A funcionalidade deverá permitir consolidar, filtrar, visualizar e exportar informações da base de clientes Pessoa Física e Pessoa Jurídica.

Os relatórios deverão apoiar consulta, organização, acompanhamento da base e tomada de decisão.

---

## 2. Escopo da Área de Relatórios

A área de relatórios deverá permitir:

- selecionar um tipo de relatório;
- aplicar filtros;
- visualizar os resultados;
- ordenar os dados;
- consultar totais;
- exportar os resultados;
- preservar a privacidade dos dados;
- restringir o acesso a usuários autenticados.

---

## 3. Relatórios da Primeira Versão

### 3.1 Relatório Geral de Clientes

Apresentará os clientes cadastrados conforme os filtros selecionados.

Colunas sugeridas:

| Coluna | Descrição |
|---|---|
| Nome | Nome completo ou nome empresarial |
| Tipo | PF ou PJ |
| Documento | CPF ou CNPJ |
| Telefone | Telefone principal |
| E-mail | E-mail cadastrado |
| Cidade | Cidade do cliente |
| Estado | Unidade federativa |
| Situação | Ativo ou inativo |
| Criado em | Data de criação |
| Atualizado em | Data da última atualização |

---

### 3.2 Relatório por Tipo de Cliente

Apresentará a distribuição dos cadastros entre:

- Pessoa Física;
- Pessoa Jurídica.

Informações mínimas:

- quantidade de clientes PF;
- quantidade de clientes PJ;
- percentual de cada tipo;
- total geral.

---

### 3.3 Relatório por Situação

Apresentará os clientes classificados por:

- ativos;
- inativos.

Informações mínimas:

- quantidade de clientes ativos;
- quantidade de clientes inativos;
- percentual de cada situação;
- total geral.

---

### 3.4 Relatório por Cidade e Estado

Apresentará a distribuição geográfica da base.

Informações mínimas:

- cidade;
- estado;
- quantidade de clientes;
- percentual sobre o total filtrado.

O relatório poderá ser agrupado por:

- estado;
- cidade;
- cidade e estado.

---

### 3.5 Relatório de Cadastros por Período

Apresentará os clientes criados em um intervalo de datas.

Informações mínimas:

- data de criação;
- nome;
- tipo;
- documento;
- cidade;
- estado;
- situação.

Agrupamentos possíveis:

- por dia;
- por semana;
- por mês;
- por ano.

---

### 3.6 Relatório de Atualizações por Período

Apresentará os clientes modificados em determinado intervalo.

Informações mínimas:

- nome;
- tipo;
- documento;
- data da criação;
- data da última atualização;
- situação.

---

### 3.7 Relatório de Cadastros Incompletos

Apresentará registros que possuam campos opcionais importantes não preenchidos.

Campos considerados para análise inicial:

- e-mail;
- data de nascimento ou abertura;
- endereço;
- número;
- bairro;
- cidade;
- estado.

O relatório deverá indicar quais informações estão ausentes.

Exemplo:

| Cliente | Campos ausentes |
|---|---|
| João da Silva | E-mail, complemento |
| Empresa Exemplo | Data de abertura, número |

CPF, CNPJ, nome, CEP e telefone principal não deverão estar ausentes, pois são obrigatórios.

---

## 4. Filtros Gerais

Os relatórios deverão oferecer filtros conforme o tipo selecionado.

### 4.1 Tipo de cliente

Opções:

- todos;
- Pessoa Física;
- Pessoa Jurídica.

### 4.2 Situação

Opções:

- todos;
- ativos;
- inativos.

### 4.3 Cidade

Permite filtrar por cidade.

### 4.4 Estado

Permite filtrar por unidade federativa.

### 4.5 Período de criação

Campos:

- data inicial;
- data final.

### 4.6 Período de atualização

Campos:

- data inicial;
- data final.

### 4.7 Campo preenchido ou ausente

Disponível principalmente no relatório de cadastros incompletos.

Exemplos:

- com e-mail;
- sem e-mail;
- com endereço;
- sem endereço;
- com data;
- sem data.

---

## 5. Comportamento dos Filtros

Os filtros poderão ser combinados.

Exemplo:

```text
Tipo: Pessoa Jurídica
Estado: MT
Situação: Ativo
Criado entre: 01/01/2026 e 31/12/2026
```

O relatório deverá retornar apenas os registros que atendam a todos os critérios informados.

Filtros não preenchidos não deverão restringir os resultados.

---

## 6. Validação dos Períodos

Quando houver data inicial e data final:

- a data inicial não poderá ser posterior à data final;
- datas futuras poderão ser rejeitadas quando não fizerem sentido;
- campos vazios deverão ser permitidos;
- mensagens de erro deverão ser claras.

Mensagem sugerida:

```text
A data inicial não pode ser posterior à data final.
```

---

## 7. Botões da Área de Relatórios

### 7.1 Gerar relatório

Executa a consulta com base no relatório e filtros selecionados.

### 7.2 Limpar filtros

Remove todos os filtros informados.

### 7.3 Exportar CSV

Exporta os dados em formato CSV.

### 7.4 Exportar XLSX

Exporta os dados em planilha Excel.

### 7.5 Exportar PDF

Exporta uma versão formatada para leitura ou impressão.

### 7.6 Imprimir

Abre uma versão adequada para impressão.

---

## 8. Visualização dos Resultados

Os resultados poderão ser exibidos em:

- tabela;
- resumo numérico;
- gráfico;
- combinação de tabela e gráfico.

O formato dependerá do relatório selecionado.

---

## 9. Tabelas

Relatórios detalhados deverão utilizar tabela.

A tabela deverá:

- possuir cabeçalhos claros;
- permitir ordenação;
- manter os filtros aplicados;
- exibir quantidade total;
- permitir paginação quando necessário;
- ser responsiva.

---

## 10. Gráficos

Relatórios consolidados poderão apresentar gráficos.

Gráficos sugeridos:

- barras para clientes por cidade;
- barras para clientes por estado;
- linha para cadastros por período;
- pizza ou rosca para PF e PJ;
- pizza ou rosca para ativos e inativos.

Os gráficos não deverão substituir os dados tabulares quando a consulta exigir detalhes.

---

## 11. Resumo do Relatório

Todo relatório deverá apresentar um resumo.

Exemplo:

```text
Total de clientes: 250
Pessoa Física: 180
Pessoa Jurídica: 70
Ativos: 230
Inativos: 20
```

O resumo deverá considerar apenas os filtros aplicados.

---

## 12. Ordenação

Relatórios detalhados deverão permitir ordenação por:

- nome;
- tipo;
- cidade;
- estado;
- situação;
- data de criação;
- data da última atualização.

Ordenação padrão sugerida:

```text
Nome em ordem alfabética crescente
```

Para relatórios agrupados, a ordenação padrão poderá ser por quantidade decrescente.

---

## 13. Paginação

Relatórios com muitos registros deverão ser paginados.

Configuração inicial:

```text
50 registros por página
```

A paginação deverá preservar:

- filtros;
- ordenação;
- tipo de relatório.

A exportação deverá incluir todos os registros filtrados, não apenas a página visível.

---

## 14. Exportação CSV

A exportação em CSV deverá:

- respeitar os filtros;
- incluir cabeçalho;
- utilizar codificação UTF-8;
- preservar acentos;
- utilizar separador compatível com planilhas;
- exportar todos os resultados filtrados.

Nome sugerido:

```text
relatorio_clientes_YYYY-MM-DD.csv
```

---

## 15. Exportação XLSX

A exportação em XLSX deverá:

- respeitar os filtros;
- incluir cabeçalhos;
- formatar datas;
- ajustar colunas;
- incluir uma aba com os dados;
- incluir uma aba de resumo quando aplicável;
- exportar todos os resultados filtrados.

Nome sugerido:

```text
relatorio_clientes_YYYY-MM-DD.xlsx
```

---

## 16. Exportação PDF

A exportação em PDF deverá:

- apresentar título;
- apresentar data e hora de geração;
- informar filtros utilizados;
- apresentar resumo;
- apresentar tabela ou gráfico;
- paginar corretamente;
- possuir layout adequado para impressão.

Nome sugerido:

```text
relatorio_clientes_YYYY-MM-DD.pdf
```

---

## 17. Privacidade dos Documentos

Na visualização da tela, CPF e CNPJ deverão aparecer parcialmente mascarados por padrão.

Exemplos:

```text
CPF: ***.456.789-**
CNPJ: **.345.678/0001-**
```

Nas exportações, o comportamento deverá ser configurável.

Sugestão para a primeira versão:

- CSV: documento mascarado;
- XLSX: documento mascarado;
- PDF: documento mascarado.

A exportação de documento completo poderá ser adicionada futuramente para usuários com permissão específica.

---

## 18. Registro da Geração

O sistema poderá registrar futuramente:

- usuário que gerou o relatório;
- tipo do relatório;
- data e hora;
- filtros utilizados;
- formato exportado.

Na primeira versão, esse histórico não será obrigatório.

---

## 19. Segurança

A área de relatórios deverá:

- exigir autenticação;
- respeitar permissões;
- validar filtros no backend;
- impedir exportações não autorizadas;
- limitar consultas excessivas;
- evitar exposição desnecessária de dados;
- registrar erros técnicos em log.

---

## 20. Desempenho

Os relatórios deverão ser executados de forma eficiente.

Boas práticas previstas:

- uso de índices;
- consultas otimizadas;
- paginação;
- agregações no banco;
- limite de resultados na tela;
- exportação controlada;
- prevenção de consultas repetidas desnecessárias.

Caso uma exportação futura possua grande volume, poderá ser processada em tarefa assíncrona.

---

## 21. Estado Inicial da Tela

Ao abrir a área de relatórios:

- nenhum relatório detalhado precisa ser executado automaticamente;
- o sistema deverá exibir os tipos disponíveis;
- o usuário deverá selecionar um relatório;
- filtros padrão poderão ser apresentados;
- o botão Gerar relatório deverá iniciar a consulta.

---

## 22. Relatório sem Resultados

Quando nenhum registro atender aos filtros:

```text
Nenhum registro encontrado para os critérios informados.
```

A tela deverá oferecer:

- limpar filtros;
- alterar período;
- selecionar outro relatório.

---

## 23. Persistência dos Filtros

Durante a navegação dentro da área de relatórios, o sistema deverá preservar:

- relatório selecionado;
- filtros;
- ordenação;
- página atual.

Ao sair da área, essa persistência poderá ser encerrada.

---

## 24. Responsividade

Em computadores:

- filtros poderão ser exibidos em painel lateral ou superior;
- tabelas e gráficos poderão ocupar a área principal.

Em celulares:

- filtros poderão ser recolhidos;
- tabelas poderão ser convertidas em cartões;
- gráficos deverão se ajustar à largura;
- botões de exportação poderão ser agrupados em menu.

---

## 25. Acessibilidade

A área deverá:

- possuir rótulos claros;
- permitir navegação por teclado;
- apresentar tabelas com cabeçalhos adequados;
- não depender apenas de cores;
- oferecer descrição textual dos gráficos;
- manter contraste adequado;
- informar resultados e erros de forma compreensível.

---

## 26. Fluxo Resumido

```text
Abrir relatórios
    |
    v
Selecionar tipo
    |
    v
Informar filtros
    |
    v
Validar filtros
    |
    v
Gerar consulta
    |
    v
Exibir resumo, tabela e/ou gráfico
    |
    v
Ordenar, paginar ou exportar
```

---

## 27. Critérios de Aceitação

A funcionalidade será considerada concluída quando:

- o usuário conseguir selecionar um relatório;
- os filtros puderem ser combinados;
- períodos forem validados;
- o relatório geral funcionar;
- o relatório por tipo funcionar;
- o relatório por situação funcionar;
- o relatório por cidade e estado funcionar;
- o relatório por período funcionar;
- o relatório de cadastros incompletos funcionar;
- o resumo considerar os filtros aplicados;
- a tabela permitir ordenação;
- a paginação preservar os filtros;
- a exportação CSV funcionar;
- a exportação XLSX funcionar;
- a exportação PDF funcionar;
- os documentos estiverem mascarados;
- o acesso exigir autenticação;
- a exportação incluir todos os registros filtrados.

---

## 28. Decisões Aprovadas

- relatórios gerais e consolidados;
- filtros combináveis;
- relatórios por tipo, situação, localidade e período;
- relatório de cadastros incompletos;
- visualização em tabela, resumo e gráficos;
- exportação em CSV, XLSX e PDF;
- 50 registros por página;
- exportação de todos os resultados filtrados;
- CPF e CNPJ mascarados por padrão;
- acesso restrito a usuários autenticados;
- relatórios preparados para crescimento da base.
