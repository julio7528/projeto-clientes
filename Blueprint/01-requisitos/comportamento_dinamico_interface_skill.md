# Skill — Comportamento Dinâmico da Interface

## 1. Objetivo

Este documento define como a interface do cadastro de clientes deverá reagir às escolhas e ações do usuário.

O formulário será único para clientes Pessoa Física e Pessoa Jurídica, alterando dinamicamente os rótulos, máscaras, validações e mensagens conforme o tipo selecionado.

---

## 2. Seleção do Tipo de Cliente

O primeiro campo do formulário será:

```text
Tipo de cliente
```

Opções disponíveis:

- Pessoa Física — PF;
- Pessoa Jurídica — PJ.

Esse campo será obrigatório.

Enquanto o tipo de cliente não for selecionado, os campos dependentes poderão permanecer desabilitados ou sem máscara específica.

---

## 3. Comportamento para Pessoa Física

Quando o usuário selecionar Pessoa Física, a interface deverá exibir:

```text
Nome completo
CPF
Data de nascimento
```

O campo de documento deverá:

- aplicar máscara de CPF;
- aceitar onze dígitos;
- validar os dígitos verificadores;
- rejeitar CPF já cadastrado.

A máscara visual sugerida será:

```text
000.000.000-00
```

---

## 4. Comportamento para Pessoa Jurídica

Quando o usuário selecionar Pessoa Jurídica, a interface deverá exibir:

```text
Nome empresarial
CNPJ
Data de abertura
```

O campo de documento deverá:

- aplicar máscara de CNPJ;
- aceitar quatorze dígitos;
- validar os dígitos verificadores;
- rejeitar CNPJ já cadastrado.

A máscara visual sugerida será:

```text
00.000.000/0000-00
```

---

## 5. Troca do Tipo de Cliente

Caso o usuário altere o tipo de cliente durante o preenchimento:

- os rótulos deverão ser atualizados imediatamente;
- a máscara do documento deverá ser alterada;
- a validação anterior deverá ser removida;
- o documento já digitado deverá ser limpo;
- a data preenchida poderá ser mantida;
- os demais campos deverão permanecer preenchidos.

Antes de limpar o documento, a interface deverá exibir um aviso:

```text
Ao alterar o tipo de cliente, o documento informado será removido.
```

---

## 6. Campo Nome

O sistema utilizará internamente um único campo chamado `nome`.

Na interface:

- PF: Nome completo;
- PJ: Nome empresarial.

Comportamento esperado:

- remover espaços no início e no final;
- substituir espaços duplicados;
- impedir envio com menos de três caracteres;
- destacar o campo quando houver erro;
- manter o valor preenchido após falha de validação.

---

## 7. Campo Documento

O sistema utilizará internamente um único campo chamado `documento`.

Na interface:

- PF: CPF;
- PJ: CNPJ.

Comportamento esperado:

- aplicar máscara enquanto o usuário digita;
- armazenar somente números;
- permitir pesquisa com ou sem pontuação;
- validar antes do envio;
- consultar duplicidade antes de concluir o cadastro;
- exibir mensagem específica em caso de erro.

Mensagens sugeridas:

```text
Informe um CPF válido.
Informe um CNPJ válido.
Este CPF já está cadastrado.
Este CNPJ já está cadastrado.
```

---

## 8. Campo Telefone Principal

O telefone será obrigatório.

Comportamento esperado:

- aceitar telefone fixo ou celular;
- aplicar máscara conforme a quantidade de dígitos;
- exigir DDD;
- armazenar somente números;
- alertar quando o telefone já estiver associado a outro cliente;
- não bloquear o cadastro apenas por telefone repetido.

Máscaras sugeridas:

```text
(00) 0000-0000
(00) 00000-0000
```

Mensagem de alerta sugerida:

```text
Este telefone já está associado a outro cliente. Deseja continuar?
```

---

## 9. Campo CEP

O CEP será obrigatório.

Comportamento esperado:

- aplicar máscara;
- aceitar oito dígitos;
- armazenar somente números;
- consultar automaticamente os dados do endereço;
- preencher endereço, bairro, cidade e estado;
- permitir edição manual;
- não bloquear o cadastro quando o serviço externo estiver indisponível.

Máscara sugerida:

```text
00000-000
```

Durante a consulta, a interface deverá indicar:

```text
Consultando CEP...
```

Em caso de CEP não encontrado:

```text
CEP não encontrado. Preencha o endereço manualmente.
```

Em caso de indisponibilidade:

```text
Não foi possível consultar o CEP agora. Preencha o endereço manualmente.
```

---

## 10. Campos de Endereço

Campos envolvidos:

- endereço;
- número;
- complemento;
- bairro;
- cidade;
- estado.

Comportamento esperado:

- permitir preenchimento automático;
- permitir edição manual;
- manter os dados preenchidos em caso de erro;
- limitar o estado às siglas válidas;
- posicionar o cursor no campo número após preenchimento automático do CEP.

---

## 11. Campo E-mail

O e-mail será opcional.

Quando preenchido:

- remover espaços;
- converter para letras minúsculas;
- validar o formato;
- alertar quando o e-mail já estiver associado a outro cliente;
- não bloquear o cadastro apenas por e-mail repetido.

Mensagem sugerida:

```text
Este e-mail já está associado a outro cliente. Deseja continuar?
```

---

## 12. Campo Data

O sistema utilizará internamente um único campo de data.

Na interface:

- PF: Data de nascimento;
- PJ: Data de abertura.

Comportamento esperado:

- não permitir data futura;
- aceitar campo vazio;
- utilizar seletor de data;
- manter o valor preenchido após falha de validação.

Mensagem sugerida:

```text
A data informada não pode ser futura.
```

---

## 13. Campo Situação

Todo novo cliente deverá iniciar com a situação:

```text
Ativo
```

Na tela de edição, o usuário poderá alterar para:

- ativo;
- inativo.

A interface deverá priorizar inativação em vez de exclusão definitiva.

---

## 14. Botão Salvar

O botão Salvar deverá:

- validar todos os campos obrigatórios;
- impedir envio duplicado;
- exibir indicador de processamento;
- permanecer desabilitado durante o salvamento;
- manter os dados quando houver erro;
- redirecionar ou atualizar a tela após sucesso.

Texto durante processamento:

```text
Salvando...
```

Mensagem de sucesso:

```text
Cliente cadastrado com sucesso.
```

Na edição:

```text
Cliente atualizado com sucesso.
```

---

## 15. Tratamento de Erros

Os erros deverão ser exibidos próximos aos campos correspondentes.

A interface deverá:

- destacar visualmente o campo;
- explicar o problema de forma objetiva;
- manter os demais dados preenchidos;
- posicionar o foco no primeiro campo com erro;
- evitar mensagens técnicas para o usuário.

Exemplos:

```text
O nome é obrigatório.
Informe um telefone com DDD.
Informe um CEP válido.
```

---

## 16. Alertas de Possível Duplicidade

O sistema deverá bloquear:

- CPF duplicado;
- CNPJ duplicado.

O sistema deverá apenas alertar:

- telefone repetido;
- e-mail repetido;
- nome semelhante.

O usuário poderá continuar quando a duplicidade não envolver CPF ou CNPJ.

---

## 17. Comportamento na Edição

Na edição, a interface deverá:

- carregar todos os dados atuais;
- permitir alteração dos campos;
- validar novamente CPF ou CNPJ;
- alertar ao trocar PF por PJ ou PJ por PF;
- limpar o documento quando o tipo for alterado;
- atualizar automaticamente a data de modificação;
- permitir ativar ou inativar o cadastro.

---

## 18. Responsividade

A interface deverá funcionar em:

- computadores;
- notebooks;
- tablets;
- celulares.

Em telas menores:

- os campos deverão ser organizados em uma coluna;
- os botões deverão permanecer acessíveis;
- mensagens não poderão ficar cortadas;
- máscaras e teclados numéricos deverão ser adequados aos campos.

---

## 19. Acessibilidade

A interface deverá:

- possuir rótulos associados aos campos;
- permitir navegação por teclado;
- indicar campos obrigatórios;
- não depender apenas de cor para indicar erros;
- utilizar mensagens claras;
- manter contraste adequado;
- posicionar corretamente o foco após erros.

---

## 20. Fluxo Resumido

```text
Abrir cadastro
    |
    v
Selecionar PF ou PJ
    |
    v
Atualizar rótulos e máscaras
    |
    v
Preencher dados
    |
    v
Consultar CEP
    |
    v
Validar campos
    |
    v
Verificar duplicidades
    |
    v
Salvar
    |
    v
Exibir confirmação
```

---

## 21. Decisões Aprovadas

- um único formulário para PF e PJ;
- um único campo interno para nome;
- um único campo interno para documento;
- CPF ou CNPJ obrigatório e único;
- telefone e CEP obrigatórios;
- telefone secundário removido;
- endereço preenchido automaticamente quando possível;
- telefone e e-mail repetidos geram alerta, não bloqueio;
- novos clientes iniciam como ativos;
- exclusão definitiva não será priorizada;
- interface responsiva e acessível.
