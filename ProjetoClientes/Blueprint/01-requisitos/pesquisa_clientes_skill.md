# Skill — Pesquisa de Clientes

## 1. Objetivo

Este documento define os requisitos funcionais e o comportamento da tela de pesquisa de clientes.

A pesquisa deverá permitir localizar rapidamente clientes Pessoa Física e Pessoa Jurídica, aplicar filtros, ordenar resultados e acessar ações relacionadas ao cadastro.

---

## 2. Escopo da Pesquisa

A tela deverá permitir pesquisar clientes utilizando:

- nome;
- CPF;
- CNPJ;
- telefone;
- e-mail;
- cidade;
- estado;
- tipo de cliente;
- situação do cadastro;
- período de criação;
- período da última atualização.

A pesquisa deverá funcionar sobre a mesma base de clientes utilizada no cadastro.

---

## 3. Campo de Busca Geral

A tela deverá possuir um campo principal chamado:

```text
Buscar cliente
```

Esse campo deverá pesquisar simultaneamente em:

- nome;
- documento;
- telefone;
- e-mail.

Exemplos de entrada:

```text
João da Silva
123.456.789-00
12345678900
12.345.678/0001-99
12345678000199
(65) 99999-9999
cliente@email.com
```

A pesquisa deverá aceitar CPF, CNPJ e telefone com ou sem pontuação.

---

## 4. Filtros

A tela deverá possuir filtros adicionais.

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

Campo de texto ou seleção com cidades já existentes na base.

### 4.4 Estado

Seleção por sigla da unidade federativa.

Opções:

- todos;
- AC;
- AL;
- AP;
- AM;
- BA;
- CE;
- DF;
- ES;
- GO;
- MA;
- MT;
- MS;
- MG;
- PA;
- PB;
- PR;
- PE;
- PI;
- RJ;
- RN;
- RS;
- RO;
- RR;
- SC;
- SP;
- SE;
- TO.

### 4.5 Período de criação

Campos:

- data inicial;
- data final.

### 4.6 Período de atualização

Campos:

- data inicial;
- data final.

---

## 5. Comportamento dos Filtros

Os filtros poderão ser combinados.

Exemplo:

```text
Tipo: Pessoa Jurídica
Estado: MT
Situação: Ativo
```

O resultado deverá conter apenas clientes que atendam a todos os filtros selecionados.

Os filtros não preenchidos não deverão restringir a pesquisa.

---

## 6. Botões da Pesquisa

A tela deverá possuir os seguintes botões:

### 6.1 Pesquisar

Executa a pesquisa com os termos e filtros informados.

### 6.2 Limpar filtros

Remove:

- texto da busca;
- tipo selecionado;
- situação selecionada;
- cidade;
- estado;
- períodos.

Após limpar, a tela poderá voltar a exibir a listagem padrão.

### 6.3 Novo cliente

Abre a tela de cadastro de cliente.

### 6.4 Exportar

A funcionalidade poderá ser incluída na primeira versão ou em evolução posterior.

Formatos possíveis:

- CSV;
- XLSX;
- PDF.

A exportação deverá respeitar os filtros ativos.

---

## 7. Pesquisa Automática ou Manual

A primeira versão deverá utilizar pesquisa manual pelo botão:

```text
Pesquisar
```

Isso evita consultas ao banco a cada caractere digitado.

Como evolução futura, poderá ser aplicada pesquisa automática com atraso controlado.

---

## 8. Normalização da Pesquisa

Antes de executar a busca, o sistema deverá:

- remover espaços no início e no final;
- remover pontuação de CPF, CNPJ e telefone;
- converter e-mail para letras minúsculas;
- ignorar diferenças entre letras maiúsculas e minúsculas;
- tratar espaços duplicados.

Exemplo:

```text
Entrada:   João   da Silva
Pesquisa: João da Silva
```

---

## 9. Correspondência dos Resultados

### 9.1 Nome

A pesquisa deverá aceitar correspondência parcial.

Exemplo:

```text
Busca: João
Resultado: João da Silva
```

### 9.2 Documento

A pesquisa deverá aceitar:

- documento completo;
- documento com pontuação;
- documento sem pontuação.

A busca parcial por documento não deverá ser priorizada por segurança e precisão.

### 9.3 Telefone

A pesquisa deverá aceitar:

- telefone completo;
- com máscara;
- sem máscara.

### 9.4 E-mail

A pesquisa deverá aceitar correspondência completa ou parcial.

---

## 10. Resultado da Pesquisa

Os resultados deverão ser exibidos em tabela.

Colunas iniciais:

| Coluna | Descrição |
|---|---|
| Nome | Nome completo ou nome empresarial |
| Tipo | PF ou PJ |
| Documento | CPF ou CNPJ formatado |
| Telefone | Telefone principal formatado |
| E-mail | E-mail, quando informado |
| Cidade/UF | Cidade e estado |
| Situação | Ativo ou inativo |
| Atualizado em | Data da última atualização |
| Ações | Operações disponíveis |

---

## 11. Exibição de Dados Sensíveis

Na listagem, CPF e CNPJ poderão ser exibidos de forma parcialmente mascarada.

Exemplos:

```text
CPF: ***.456.789-**
CNPJ: **.345.678/0001-**
```

O documento completo poderá ser exibido:

- na tela de detalhes;
- na tela de edição;
- mediante ação explícita do usuário.

Essa regra reforça a privacidade sem impedir o uso do sistema.

---

## 12. Ordenação

A tela deverá permitir ordenar os resultados por:

- nome;
- data de criação;
- última atualização;
- cidade;
- situação.

Ordenação padrão sugerida:

```text
Nome em ordem alfabética crescente
```

Ao clicar novamente na mesma coluna, a ordem deverá alternar entre crescente e decrescente.

---

## 13. Paginação

A listagem deverá ser paginada.

Configuração inicial:

```text
20 registros por página
```

Opções futuras:

- 20;
- 50;
- 100 registros por página.

A paginação deverá preservar:

- texto pesquisado;
- filtros;
- ordenação.

---

## 14. Ações por Cliente

Cada resultado deverá disponibilizar as seguintes ações:

### 14.1 Visualizar

Abre os detalhes completos do cliente.

### 14.2 Editar

Abre o cadastro em modo de edição.

### 14.3 Ativar ou inativar

Altera a situação do cliente.

A ação deverá depender do estado atual:

```text
Cliente ativo: exibir Inativar
Cliente inativo: exibir Ativar
```

### 14.4 Excluir

A exclusão definitiva não deverá ser exibida como ação principal.

Quando necessária, deverá ser restrita e exigir confirmação adicional.

---

## 15. Confirmação de Ativação e Inativação

Antes de alterar a situação, o sistema deverá solicitar confirmação.

Exemplo de inativação:

```text
Deseja realmente inativar este cliente?
```

Exemplo de ativação:

```text
Deseja reativar este cliente?
```

Após a ação:

```text
Cliente inativado com sucesso.
```

ou:

```text
Cliente ativado com sucesso.
```

---

## 16. Estado Inicial da Tela

Ao abrir a tela, o sistema deverá exibir:

- clientes ativos;
- ordenados por nome;
- 20 registros por página.

O usuário poderá alterar essa visualização pelos filtros.

---

## 17. Pesquisa sem Resultados

Quando nenhum cliente for encontrado, a tela deverá exibir:

```text
Nenhum cliente encontrado com os critérios informados.
```

Também deverá oferecer as ações:

- limpar filtros;
- cadastrar novo cliente.

---

## 18. Estado sem Cadastros

Quando a base ainda não possuir clientes:

```text
Nenhum cliente cadastrado.
```

A tela deverá destacar o botão:

```text
Cadastrar primeiro cliente
```

---

## 19. Indicadores da Pesquisa

A tela deverá informar a quantidade de resultados.

Exemplos:

```text
1 cliente encontrado
```

```text
35 clientes encontrados
```

Em listagens paginadas:

```text
Exibindo 1 a 20 de 35 clientes
```

---

## 20. Persistência dos Filtros

Ao abrir um cliente e retornar para a pesquisa, o sistema deverá preservar:

- texto pesquisado;
- filtros;
- página atual;
- ordenação.

Isso evita que o usuário precise repetir a busca.

---

## 21. Desempenho

A pesquisa deverá ser planejada para crescer com a base.

Campos candidatos a indexação:

- documento;
- nome;
- telefone;
- e-mail;
- cidade;
- estado;
- tipo;
- situação;
- data de criação;
- data de atualização.

O campo documento deverá possuir índice único.

---

## 22. Segurança

A pesquisa deverá:

- exigir autenticação;
- respeitar permissões do usuário;
- validar filtros no backend;
- limitar a quantidade de resultados por página;
- evitar exposição desnecessária de documentos;
- impedir consultas diretas não autorizadas.

---

## 23. Acessibilidade

A tela deverá:

- permitir navegação por teclado;
- possuir rótulos associados aos filtros;
- informar a quantidade de resultados;
- permitir leitura adequada por tecnologias assistivas;
- não depender apenas de ícones sem texto ou descrição;
- manter foco visível;
- indicar claramente filtros ativos.

---

## 24. Responsividade

Em telas grandes:

- os filtros poderão ser exibidos em linha ou painel lateral;
- a tabela poderá apresentar todas as colunas.

Em telas pequenas:

- filtros poderão ser recolhidos;
- resultados poderão ser apresentados em cartões;
- ações deverão permanecer acessíveis;
- informações menos prioritárias poderão ser ocultadas ou agrupadas.

---

## 25. Fluxo Resumido

```text
Abrir pesquisa
    |
    v
Exibir clientes ativos
    |
    v
Informar busca e filtros
    |
    v
Normalizar valores
    |
    v
Consultar banco
    |
    v
Exibir resultados
    |
    v
Visualizar, editar ou alterar situação
```

---

## 26. Critérios de Aceitação

A funcionalidade será considerada concluída quando:

- o usuário conseguir pesquisar por nome;
- o usuário conseguir pesquisar por CPF;
- o usuário conseguir pesquisar por CNPJ;
- o usuário conseguir pesquisar por telefone;
- o usuário conseguir pesquisar por e-mail;
- documentos puderem ser pesquisados com ou sem máscara;
- os filtros puderem ser combinados;
- a tabela exibir os dados definidos;
- a ordenação funcionar;
- a paginação preservar os filtros;
- o usuário conseguir visualizar um cliente;
- o usuário conseguir editar um cliente;
- o usuário conseguir ativar ou inativar um cliente;
- a tela informar quando não houver resultados;
- o acesso exigir autenticação;
- documentos forem protegidos conforme a regra de privacidade.

---

## 27. Decisões Aprovadas

- busca geral por nome, documento, telefone e e-mail;
- filtros por tipo, situação, cidade, estado e períodos;
- pesquisa manual por botão;
- resultados em tabela;
- 20 registros por página;
- ordenação padrão por nome;
- ações de visualizar, editar, ativar e inativar;
- exclusão definitiva fora das ações principais;
- filtros preservados ao retornar;
- documentos parcialmente mascarados na listagem;
- pesquisa restrita a usuários autenticados.
