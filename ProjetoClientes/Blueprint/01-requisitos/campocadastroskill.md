# Campo Cadastro Skill

## 1. Objetivo

Este documento define os campos do cadastro de clientes do sistema, contemplando clientes Pessoa Física e Pessoa Jurídica.

A estrutura será única para os dois tipos de cliente. A principal diferença será o tipo de documento utilizado:

- Pessoa Física: CPF;
- Pessoa Jurídica: CNPJ.

---

## 2. Estrutura Geral do Cadastro

O cadastro deverá possuir um campo obrigatório para definição do tipo de cliente:

- Pessoa Física — PF;
- Pessoa Jurídica — PJ.

A escolha do tipo de cliente determinará:

- o rótulo exibido para o documento;
- a validação aplicada ao documento;
- o rótulo exibido para o campo de nome;
- o rótulo exibido para o campo de data opcional.

---

## 3. Campos Obrigatórios

### 3.1 Tipo de cliente

Define se o cadastro corresponde a:

- Pessoa Física;
- Pessoa Jurídica.

### 3.2 Nome

O sistema utilizará um único campo interno chamado `nome`.

Na interface, o rótulo deverá mudar conforme o tipo selecionado:

- Pessoa Física: Nome completo;
- Pessoa Jurídica: Nome empresarial.

### 3.3 Documento

O sistema utilizará um único campo interno chamado `documento`.

Na interface e nas validações:

- Pessoa Física: CPF;
- Pessoa Jurídica: CNPJ.

O documento deverá ser obrigatório, válido e único.

### 3.4 CEP

O CEP será obrigatório.

Sempre que possível, o sistema deverá utilizá-lo para preencher automaticamente:

- endereço;
- bairro;
- cidade;
- estado.

### 3.5 Telefone principal

O telefone principal será obrigatório.

Deverá conter:

- DDD;
- número válido;
- formatação padronizada.

---

## 4. Campos Opcionais

### 4.1 Data

O sistema utilizará um único campo interno de data.

Na interface, o rótulo poderá mudar conforme o tipo selecionado:

- Pessoa Física: Data de nascimento;
- Pessoa Jurídica: Data de abertura.

### 4.2 E-mail

O e-mail será opcional, mas deverá ser validado quando preenchido.

### 4.3 Endereço

Campo preenchido manualmente ou automaticamente a partir do CEP.

### 4.4 Número

Número do endereço.

### 4.5 Complemento

Informação adicional do endereço.

### 4.6 Bairro

Bairro do endereço.

### 4.7 Cidade

Cidade do cliente.

### 4.8 Estado

Unidade federativa do cliente.

### 4.9 Observações

Campo livre para informações adicionais relevantes ao cadastro.

---

## 5. Campos Automáticos do Sistema

### 5.1 Situação

O cadastro deverá possuir uma situação:

- ativo;
- inativo.

Todo novo cadastro deverá iniciar como ativo.

### 5.2 Data de criação

Registrada automaticamente no momento da criação do cadastro.

### 5.3 Data da última atualização

Atualizada automaticamente sempre que o cadastro for alterado.

---

## 6. Campos Removidos

O campo telefone secundário não fará parte da primeira versão do cadastro.

---

## 7. Estrutura Conceitual

```text
Tipo de cliente
Nome
Documento
Data
E-mail
Telefone principal
CEP
Endereço
Número
Complemento
Bairro
Cidade
Estado
Observações
Situação
Data de criação
Data da última atualização
```

---

## 8. Comportamento Dinâmico da Interface

Quando o usuário selecionar Pessoa Física:

```text
Nome completo
CPF
Data de nascimento
```

Quando o usuário selecionar Pessoa Jurídica:

```text
Nome empresarial
CNPJ
Data de abertura
```

Os demais campos permanecerão iguais.

---

## 9. Decisão de Modelagem Inicial

Pessoa Física e Pessoa Jurídica serão armazenadas na mesma estrutura de cliente.

Não serão criadas duas tabelas separadas nesta primeira versão.

Essa decisão tem como objetivos:

- simplificar o cadastro;
- reduzir duplicação;
- facilitar pesquisa;
- facilitar relatórios;
- manter a mesma experiência de uso;
- permitir evolução futura sem complexidade desnecessária.
