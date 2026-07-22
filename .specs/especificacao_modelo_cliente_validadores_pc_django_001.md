# Especificação Técnica — Modelo Cliente e Validadores de Domínio
## Projeto PC-DJANGO-001

## 1. Identificação da etapa

**Fase principal:** Fase 2 — Estruturação do domínio  
**Subetapa:** 2.3 — Modelagem definitiva de Cliente e validadores de domínio  
**Status:** Especificação aprovada para implementação futura  
**Escopo deste documento:** definir a entidade única `Cliente`, suas escolhas, campos, auditoria, normalização, validações, constraints, índices, alertas de possível duplicidade, administração e testes.

---

## 2. Objetivo

Implementar a base persistente do domínio de clientes Pessoa Física e Pessoa Jurídica utilizando uma única entidade Django:

```text
clientes.Cliente
```

A entidade deverá:

- usar UUID;
- representar PF e PJ;
- armazenar CPF ou CNPJ em um único campo;
- manter endereço e contato principal na própria tabela;
- registrar situação;
- registrar timestamps;
- registrar autoria;
- validar e normalizar os dados no backend;
- impedir documento duplicado;
- alertar, sem bloquear, telefone ou e-mail repetidos;
- respeitar o isolamento de dados por usuário;
- ser compatível com PostgreSQL no Supabase;
- utilizar Django ORM e migrations.

---

## 3. Estado atual considerado

Esta especificação considera que o projeto já possui:

1. backend Django em `backend/`;
2. app `config` responsável por configuração e infraestrutura;
3. app `core` responsável por elementos compartilhados;
4. `core.UUIDTimestampedModel`, abstrato, com UUID e timestamps;
5. `core.normalize_digits`;
6. `core.normalize_whitespace`;
7. app `usuarios` com modelo customizado;
8. login por e-mail e sessões Django;
9. isolamento de dados por usuário;
10. helpers de ownership existentes;
11. app `clientes` criada e registrada;
12. `clientes/models.py` ainda sem o modelo definitivo;
13. integração backend-only com Supabase;
14. `ProtectedFile` ainda localizado em `config`;
15. migrations remotas ainda não aplicadas automaticamente.

A implementação deverá preservar integralmente autenticação, segurança, Storage privado e migrations existentes.

---

## 4. Decisões de modelagem aprovadas

1. PF e PJ serão armazenadas na mesma entidade `Cliente`.
2. A diferenciação será feita pelo campo `tipo`.
3. O campo interno de nome será `nome`.
4. O campo interno de CPF ou CNPJ será `documento`.
5. O campo interno de nascimento ou abertura será `data_referencia`.
6. O endereço permanecerá dentro de `Cliente`.
7. Haverá apenas um telefone principal no MVP.
8. O e-mail será opcional.
9. Não haverá tabela separada de endereço.
10. Não haverá tabela separada de contato.
11. Não haverá apps separadas para PF e PJ.
12. O documento será armazenado somente com números.
13. O telefone será armazenado somente com números.
14. O CEP será armazenado somente com números.
15. A UF será armazenada em letras maiúsculas.
16. O e-mail será armazenado em letras minúsculas.
17. O documento será único em todo o sistema.
18. Documento duplicado será bloqueado.
19. Telefone duplicado não será bloqueado.
20. E-mail duplicado não será bloqueado.
21. Telefone ou e-mail repetidos gerarão alertas.
22. Novos clientes iniciarão como ativos.
23. Inativação será preferida à exclusão física.
24. A auditoria inicial registrará criação, atualização, criador e último atualizador.
25. Não será criado histórico completo de alterações nesta fase.
26. `ProtectedFile` não será movido nesta fase.
27. Não será criada a app `arquivos` nesta fase.
28. Não será implementado o CRUD completo nesta fase.
29. Não será implementada integração externa de CEP nesta fase.
30. Nenhuma migration será aplicada automaticamente ao Supabase.

---

## 5. Arquivos da implementação

Estrutura esperada:

```text
backend/clientes/
├── __init__.py
├── admin.py
├── apps.py
├── choices.py
├── models.py
├── services.py
├── validators.py
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_validators.py
    ├── test_duplicate_warnings.py
    └── test_admin.py
```

Não criar arquivos adicionais sem responsabilidade concreta.

---

## 6. Escolhas do domínio

As escolhas deverão ficar em:

```text
clientes/choices.py
```

### 6.1 Tipo de cliente

```python
class TipoCliente(models.TextChoices):
    PF = "PF", "Pessoa Física"
    PJ = "PJ", "Pessoa Jurídica"
```

Regras:

- obrigatório;
- aceitar somente `PF` ou `PJ`;
- usar rótulos em português;
- ser utilizado pelo modelo, formulários e filtros futuros.

### 6.2 Situação do cliente

```python
class SituacaoCliente(models.TextChoices):
    ATIVO = "ATIVO", "Ativo"
    INATIVO = "INATIVO", "Inativo"
```

Regras:

- obrigatório;
- padrão `ATIVO`;
- aceitar somente `ATIVO` ou `INATIVO`;
- não utilizar exclusão física como operação principal.

### 6.3 Unidades federativas

Deverá existir uma coleção imutável de UFs válidas, contendo as 27 unidades federativas brasileiras.

Ela poderá ser representada por:

```python
UF_CHOICES
```

ou por uma `TextChoices`, desde que:

- o valor persistido tenha duas letras;
- o banco armazene a sigla;
- a validação rejeite siglas inexistentes;
- o campo continue opcional.

---

## 7. Modelo `Cliente`

O modelo deverá ser criado em:

```text
clientes/models.py
```

Nome completo:

```text
clientes.Cliente
```

Herança recomendada:

```python
from core.models import UUIDTimestampedModel

class Cliente(UUIDTimestampedModel):
    ...
```

A classe abstrata de `core` fornecerá:

- `id`;
- `criado_em`;
- `atualizado_em`.

Não duplicar esses campos no modelo concreto.

---

## 8. Dicionário de campos

| Campo | Tipo Django | Tamanho | Obrigatório | Regra principal |
|---|---|---:|---:|---|
| `id` | UUIDField herdado | — | Sim | Chave primária |
| `tipo` | CharField + choices | 2 | Sim | `PF` ou `PJ` |
| `nome` | CharField | 200 | Sim | Nome completo ou empresarial |
| `documento` | CharField | 14 | Sim | CPF ou CNPJ, somente números e único |
| `data_referencia` | DateField | — | Não | Nascimento ou abertura; não futura |
| `email` | EmailField | 254 | Não | Minúsculo e validado quando informado |
| `telefone` | CharField | 11 | Sim | 10 ou 11 dígitos |
| `cep` | CharField | 8 | Sim | Exatamente 8 dígitos |
| `logradouro` | CharField | 200 | Não | Texto normalizado |
| `numero` | CharField | 20 | Não | Aceita número ou `S/N` |
| `complemento` | CharField | 100 | Não | Texto normalizado |
| `bairro` | CharField | 100 | Não | Texto normalizado |
| `cidade` | CharField | 100 | Não | Texto normalizado |
| `estado` | CharField + choices | 2 | Não | UF válida e maiúscula |
| `observacoes` | TextField | — | Não | Texto livre, sem dados desnecessários |
| `situacao` | CharField + choices | 7 | Sim | Padrão `ATIVO` |
| `criado_em` | DateTimeField herdado | — | Sim | Automático |
| `atualizado_em` | DateTimeField herdado | — | Sim | Automático |
| `criado_por` | ForeignKey | — | Não no banco | Usuário criador |
| `atualizado_por` | ForeignKey | — | Não no banco | Último usuário que atualizou |

---

## 9. Campos de auditoria

### 9.1 `criado_por`

Configuração aprovada:

```python
criado_por = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    related_name="clientes_criados",
)
```

Justificativa:

- preserva a autoria;
- impede exclusão acidental do usuário quando existem clientes atribuídos;
- aceita nulo para importações, migrations e registros administrativos;
- o fluxo normal da aplicação deverá sempre preencher o campo.

### 9.2 `atualizado_por`

Configuração aprovada:

```python
atualizado_por = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="clientes_atualizados",
)
```

Justificativa:

- registra o último atualizador;
- não bloqueia permanentemente a remoção excepcional de um usuário apenas por ter atualizado registros;
- preserva o cliente;
- o fluxo normal deverá preencher o campo em cada alteração.

### 9.3 Regras de segurança

- os campos de autoria não serão fornecidos pelo navegador;
- formulários comuns não incluirão esses campos;
- views ou services preencherão os campos usando `request.user`;
- usuários comuns não poderão transferir ownership;
- administrador poderá corrigir autoria apenas por ação administrativa explícita;
- consultas comuns continuarão restritas ao proprietário definido pela regra do projeto.

---

## 10. Unicidade do documento

O campo deverá utilizar:

```python
documento = models.CharField(
    max_length=14,
    unique=True,
)
```

A unicidade será global no banco.

Consequências:

- o mesmo CPF ou CNPJ não poderá existir em dois registros;
- a restrição valerá mesmo para registros de usuários diferentes;
- erros para usuários comuns deverão ser genéricos;
- não revelar o proprietário, nome ou identificador do registro existente;
- concorrência deverá ser protegida pela constraint do banco;
- validação antecipada na aplicação melhora a mensagem, mas não substitui a constraint.

Mensagem conceitual:

```text
Já existe um cliente cadastrado com este documento.
```

---

## 11. Validadores de domínio

Os validadores deverão ficar em:

```text
clientes/validators.py
```

Eles deverão ser:

- funções puras sempre que possível;
- reutilizáveis;
- independentes de request;
- cobertos por testes unitários;
- compatíveis com valores normalizados;
- responsáveis por lançar `ValidationError`.

Validadores obrigatórios:

```text
validate_cpf
validate_cnpj
validate_documento
validate_telefone
validate_cep
validate_uf
validate_data_nao_futura
validate_nome
```

---

## 12. Normalização genérica

Reutilizar de `core.normalizers`:

```python
normalize_digits
normalize_whitespace
```

Não duplicar essas funções em `clientes`.

Normalizações específicas de domínio poderão permanecer em `clientes`, como:

- e-mail para minúsculas;
- UF para maiúsculas;
- documento conforme tipo;
- campos de endereço.

---

## 13. Validação de CPF

### 13.1 Entrada

O validador deverá aceitar valor textual e trabalhar com os dígitos normalizados.

Exemplos aceitos para normalização:

```text
529.982.247-25
52998224725
```

Resultado persistido:

```text
52998224725
```

### 13.2 Regras

Um CPF será válido quando:

1. possuir exatamente 11 dígitos;
2. não possuir todos os dígitos iguais;
3. o primeiro dígito verificador estiver correto;
4. o segundo dígito verificador estiver correto.

### 13.3 Rejeições obrigatórias

Rejeitar:

- vazio quando o tipo exigir documento;
- menos de 11 dígitos;
- mais de 11 dígitos;
- letras;
- sequências repetidas como `00000000000`;
- dígitos verificadores inválidos.

### 13.4 Mensagem

Mensagem sugerida:

```text
Informe um CPF válido.
```

Não retornar detalhes desnecessários do algoritmo.

---

## 14. Validação de CNPJ

### 14.1 Entrada

O validador deverá aceitar valor textual e trabalhar com dígitos normalizados.

Exemplos aceitos para normalização:

```text
04.252.011/0001-10
04252011000110
```

Resultado persistido:

```text
04252011000110
```

### 14.2 Regras

Um CNPJ será válido quando:

1. possuir exatamente 14 dígitos;
2. não possuir todos os dígitos iguais;
3. o primeiro dígito verificador estiver correto;
4. o segundo dígito verificador estiver correto.

### 14.3 Rejeições obrigatórias

Rejeitar:

- vazio quando o tipo exigir documento;
- menos de 14 dígitos;
- mais de 14 dígitos;
- letras;
- sequências repetidas;
- dígitos verificadores inválidos.

### 14.4 Mensagem

Mensagem sugerida:

```text
Informe um CNPJ válido.
```

---

## 15. Validação cruzada de tipo e documento

A função:

```python
validate_documento(tipo, documento)
```

ou regra equivalente deverá aplicar:

```text
tipo = PF → documento deve ser CPF válido com 11 dígitos
tipo = PJ → documento deve ser CNPJ válido com 14 dígitos
```

Rejeitar:

- CPF com tipo PJ;
- CNPJ com tipo PF;
- tipo ausente;
- tipo inválido;
- documento ausente;
- documento de tamanho incompatível.

Essa regra depende de mais de um campo e deverá ser aplicada no `clean()` do modelo.

---

## 16. Validação de telefone

Regras:

1. obrigatório;
2. normalizar para somente números;
3. possuir 10 ou 11 dígitos;
4. conter DDD;
5. não aplicar máscara no banco.

Exemplos:

```text
(65) 3333-4444 → 6533334444
(65) 99999-8888 → 65999998888
```

Mensagem sugerida:

```text
Informe um telefone com DDD e 10 ou 11 dígitos.
```

Não validar existência real da linha telefônica.

---

## 17. Validação de CEP

Regras:

1. obrigatório;
2. normalizar para somente números;
3. possuir exatamente 8 dígitos;
4. não depender de serviço externo.

Exemplo:

```text
78890-000 → 78890000
```

Mensagem sugerida:

```text
Informe um CEP com 8 dígitos.
```

---

## 18. Validação de nome

O campo `nome` deverá:

1. ser obrigatório;
2. ser normalizado com `normalize_whitespace`;
3. possuir pelo menos 3 caracteres úteis;
4. não aceitar apenas números;
5. não aceitar apenas símbolos;
6. preservar acentos;
7. preservar capitalização informada, sem converter automaticamente tudo para maiúsculo.

Exemplo:

```text
"  João   da Silva  " → "João da Silva"
```

Para PJ, a mesma regra se aplica ao nome empresarial.

Mensagem sugerida:

```text
Informe um nome válido com pelo menos 3 caracteres.
```

---

## 19. Validação de data de referência

Quando informada:

- deverá ser uma data válida;
- não poderá estar no futuro;
- PF interpretará como data de nascimento;
- PJ interpretará como data de abertura;
- não haverá idade mínima ou máxima nesta fase;
- não haverá consulta externa de CNPJ.

Mensagem sugerida:

```text
A data não pode estar no futuro.
```

---

## 20. Validação de e-mail

Quando informado:

1. remover espaços externos;
2. converter para minúsculas;
3. validar com `EmailField`;
4. não exigir unicidade;
5. permitir repetição com alerta;
6. armazenar vazio de forma consistente.

Representação aprovada:

```python
email = models.EmailField(
    blank=True,
    default="",
    db_index=True,
)
```

Evitar mistura desnecessária entre `NULL` e string vazia para campo textual opcional.

Exemplo:

```text
"  CLIENTE@EMAIL.COM " → "cliente@email.com"
```

---

## 21. Validação de UF

Quando informada:

1. remover espaços;
2. converter para maiúsculas;
3. possuir exatamente duas letras;
4. pertencer à lista oficial de UFs.

Exemplo:

```text
" mt " → "MT"
```

Mensagem sugerida:

```text
Informe uma unidade federativa válida.
```

---

## 22. Normalização do modelo

O modelo deverá possuir método interno idempotente, como:

```python
def normalize_fields(self) -> None:
    ...
```

Normalizar:

- `nome`;
- `documento`;
- `email`;
- `telefone`;
- `cep`;
- `logradouro`;
- `numero`;
- `complemento`;
- `bairro`;
- `cidade`;
- `estado`;
- opcionalmente `observacoes` apenas nos espaços externos.

### 22.1 `clean()`

O método `clean()` deverá:

1. chamar `super().clean()`;
2. normalizar os campos;
3. validar tipo e documento;
4. validar nome;
5. validar telefone;
6. validar CEP;
7. validar data;
8. validar UF;
9. validar e-mail pelo mecanismo do campo;
10. validar escolhas e regras cruzadas.

### 22.2 `save()`

O método `save()` poderá normalizar de forma idempotente antes da persistência.

Não depender exclusivamente de `save()` para validação, pois Django não chama `full_clean()` automaticamente.

### 22.3 Fluxo de persistência

Forms, services e operações administrativas deverão:

```text
normalizar
→ full_clean()
→ save()
```

A constraint do banco continuará sendo a defesa final para unicidade e integridade.

---

## 23. Constraints de banco

A migration deverá garantir, no mínimo:

1. chave primária UUID;
2. documento único;
3. tipo válido;
4. situação válida;
5. tamanho do documento coerente com o tipo;
6. CEP com 8 dígitos;
7. telefone com 10 ou 11 dígitos;
8. integridade das chaves estrangeiras.

Constraints sugeridas:

```text
tipo PF + documento com 11 dígitos
OU
tipo PJ + documento com 14 dígitos
```

As constraints deverão ser compatíveis com:

- PostgreSQL;
- SQLite utilizado nos testes;
- migrations do Django.

A validação dos dígitos verificadores permanecerá na aplicação Django.

---

## 24. Índices

O modelo deverá possuir índices adequados para pesquisa, filtros e relatórios.

### 24.1 Índices simples

- `nome`;
- `telefone`;
- `email`;
- `tipo`;
- `situacao`;
- `criado_em`;
- `atualizado_em`.

O documento já possuirá índice único por `unique=True`.

### 24.2 Índices compostos

Criar:

```text
estado, cidade
tipo, situacao
```

Nomes devem ser explícitos e respeitar o limite do banco.

### 24.3 Relações

Foreign keys já recebem índice por padrão no Django.

Não criar índices duplicados sem benefício.

---

## 25. Ordenação e representação

Ordenação padrão:

```python
ordering = ("nome",)
```

Representação textual:

```python
def __str__(self) -> str:
    return self.nome
```

Nomes administrativos:

```text
Cliente
Clientes
```

---

## 26. Ativação e inativação

O modelo ou service deverá disponibilizar operações explícitas:

```python
ativar()
inativar()
```

Regras:

- `ativar()` define situação `ATIVO`;
- `inativar()` define situação `INATIVO`;
- as operações devem ser idempotentes;
- não excluir o registro;
- atualização deverá registrar `atualizado_por` no fluxo de aplicação;
- não implementar histórico completo nesta fase.

---

## 27. Alertas de telefone e e-mail repetidos

### 27.1 Natureza

Telefone e e-mail repetidos serão alertas, não erros.

Portanto:

- não usar `unique=True`;
- não criar `UniqueConstraint`;
- não lançar `ValidationError` apenas pela repetição;
- não impedir o salvamento;
- não executar merge automático;
- não alterar outro cadastro.

### 27.2 Localização da regra

A detecção deverá ficar em:

```text
clientes/services.py
```

ou módulo de domínio equivalente.

Não colocar essa regra em `core`.

Não colocar a regra diretamente em `model.clean()`, pois:

- é contextual;
- depende do usuário;
- gera aviso, não erro;
- precisa excluir o próprio registro durante edição.

### 27.3 Interface sugerida

Exemplo conceitual:

```python
def collect_duplicate_warnings(
    *,
    user,
    telefone: str = "",
    email: str = "",
    exclude_cliente_id=None,
) -> list[DuplicateWarning]:
    ...
```

A estrutura de retorno poderá conter:

```text
code
field
message
count
```

### 27.4 Escopo de privacidade

Para usuário comum:

```text
buscar duplicidades apenas entre clientes visíveis para o próprio usuário
```

Para administrador:

```text
permitir busca global
```

Deverá reutilizar o helper de ownership já existente ou equivalente aprovado.

Não revelar ao usuário comum:

- nome do cliente de outro usuário;
- documento;
- proprietário;
- UUID;
- contagem global;
- qualquer dado que confirme registros fora do seu escopo.

### 27.5 Normalização

Antes da comparação:

- telefone somente com números;
- e-mail minúsculo;
- espaços removidos;
- valores vazios ignorados.

### 27.6 Edição

Ao editar:

- excluir o próprio cliente da consulta;
- não alertar sobre o valor do próprio registro;
- alertar caso outro registro visível tenha o mesmo valor.

### 27.7 Mensagens sugeridas

Telefone:

```text
Já existe outro cliente com este telefone.
```

E-mail:

```text
Já existe outro cliente com este e-mail.
```

As mensagens não deverão identificar o outro cadastro nesta fase.

---

## 28. Similaridade de nome

O Blueprint prevê alerta de nome semelhante.

Nesta etapa:

- não implementar algoritmo de similaridade;
- não utilizar busca fuzzy;
- não bloquear nomes iguais;
- registrar como requisito da futura etapa de cadastro e pesquisa.

A implementação atual de alertas será limitada a:

```text
telefone repetido
e-mail repetido
```

---

## 29. Isolamento por usuário

O modelo deverá ser compatível com a regra:

```text
usuário comum acessa somente os próprios clientes
administrador acessa todos
```

As consultas futuras deverão utilizar o helper de ownership existente.

Regras:

- não confiar em `criado_por` enviado pelo cliente HTTP;
- não permitir alteração de ownership por usuário comum;
- o documento único continuará global;
- mensagens de documento duplicado serão genéricas;
- alertas de telefone e e-mail serão limitados ao escopo visível;
- relatórios e dashboards futuros herdarão o mesmo escopo.

---

## 30. Django Admin

Registrar `Cliente` em:

```text
clientes/admin.py
```

Configuração mínima:

- lista por nome, tipo, situação, telefone, cidade e estado;
- busca por nome, documento, telefone e e-mail;
- filtros por tipo, situação, estado e data;
- ordenação por nome;
- timestamps somente leitura;
- autoria somente leitura após criação;
- ações administrativas de ativar e inativar;
- documento mascarado na listagem quando possível;
- documento completo apenas na tela administrativa autorizada;
- não permitir alteração silenciosa de ownership;
- não expor segredos ou dados do Supabase.

O admin não deverá implementar regras paralelas diferentes do domínio.

---

## 31. Privacidade

1. CPF e CNPJ serão armazenados completos por necessidade de identificação.
2. Listagens futuras deverão mascarar documentos.
3. Relatórios futuros deverão mascarar documentos quando não houver necessidade do valor completo.
4. O documento completo será exibido apenas em telas autorizadas.
5. Observações não deverão armazenar dados sensíveis sem necessidade.
6. Logs não deverão registrar documentos completos, telefones, e-mails ou observações de clientes.
7. Mensagens de erro não deverão incluir dados de outro cadastro.
8. Testes deverão usar somente dados fictícios.

---

## 32. Migration inicial

A implementação deverá criar:

```text
clientes/migrations/0001_initial.py
```

A migration deverá:

- criar somente a tabela `Cliente`;
- depender do usuário customizado por `swappable_dependency`;
- preservar migrations existentes;
- não mover `ProtectedFile`;
- não criar tabela para `core.UUIDTimestampedModel`;
- criar constraints e índices revisados;
- não conter operação destrutiva;
- não ser aplicada automaticamente ao Supabase.

Antes de considerar pronta:

1. ler a migration inteira;
2. verificar dependências;
3. verificar nomes dos índices e constraints;
4. verificar `on_delete`;
5. executar dry-run;
6. executar testes em SQLite isolado.

---

## 33. Testes de validadores

Cobrir no mínimo:

### CPF

1. CPF válido formatado;
2. CPF válido sem máscara;
3. CPF inválido;
4. CPF curto;
5. CPF longo;
6. CPF com dígitos repetidos;
7. CPF com letras.

### CNPJ

8. CNPJ válido formatado;
9. CNPJ válido sem máscara;
10. CNPJ inválido;
11. CNPJ curto;
12. CNPJ longo;
13. CNPJ com dígitos repetidos;
14. CNPJ com letras.

### Outros

15. telefone de 10 dígitos;
16. telefone de 11 dígitos;
17. telefone inválido;
18. CEP válido;
19. CEP inválido;
20. UF válida em minúsculas após normalização;
21. UF inválida;
22. data atual ou passada;
23. data futura;
24. nome válido;
25. nome somente numérico;
26. nome somente com símbolos;
27. nome curto.

---

## 34. Testes do modelo

Cobrir no mínimo:

1. criação de PF válida;
2. criação de PJ válida;
3. UUID automático;
4. situação padrão ativa;
5. timestamps automáticos;
6. normalização de nome;
7. normalização de documento;
8. normalização de telefone;
9. normalização de CEP;
10. normalização de e-mail;
11. normalização de UF;
12. rejeição de CPF para tipo PJ;
13. rejeição de CNPJ para tipo PF;
14. documento obrigatório;
15. documento único;
16. telefone obrigatório;
17. CEP obrigatório;
18. e-mail opcional;
19. endereço opcional;
20. autoria correta;
21. `criado_por` protegido;
22. `atualizado_por` anulável;
23. ativação idempotente;
24. inativação idempotente;
25. ordenação por nome;
26. representação textual.

---

## 35. Testes de alertas

Cobrir no mínimo:

1. telefone repetido gera alerta;
2. e-mail repetido gera alerta;
3. telefone repetido não bloqueia;
4. e-mail repetido não bloqueia;
5. valores vazios não geram alerta;
6. edição exclui o próprio registro;
7. usuário comum vê duplicidades apenas no próprio escopo;
8. usuário comum não recebe informações de outro usuário;
9. administrador pode detectar duplicidade global;
10. telefone é comparado normalizado;
11. e-mail é comparado normalizado;
12. dois campos repetidos geram dois alertas distintos.

---

## 36. Testes de regressão

A implementação não poderá quebrar:

- login;
- logout;
- perfil;
- alteração de senha;
- Django Admin de usuários;
- `AUTH_USER_MODEL`;
- ownership;
- `ProtectedFile`;
- Storage privado;
- segurança de secrets;
- testes de `config`;
- testes de `usuarios`;
- testes de `core`.

---

## 37. Comandos de validação

Executar a partir da raiz do repositório:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py test clientes core usuarios config
```

Depois, quando necessário:

```powershell
python backend/manage.py test
```

A geração inicial da migration deverá ocorrer antes do comando de dry-run.

Não executar automaticamente:

```powershell
python backend/manage.py migrate
```

contra o Supabase.

---

## 38. Subetapas numeradas da implementação

### 38.1 Auditoria inicial

1. ler `AGENTS.md`;
2. ler o Blueprint de campos;
3. ler o Blueprint de modelagem;
4. ler a especificação modular;
5. revisar `core`;
6. revisar `clientes`;
7. revisar `usuarios.permissions`;
8. revisar migrations;
9. executar testes baseline.

### 38.2 Escolhas

1. criar `TipoCliente`;
2. criar `SituacaoCliente`;
3. criar choices de UF;
4. testar choices.

### 38.3 Validadores

1. implementar CPF;
2. implementar CNPJ;
3. implementar documento por tipo;
4. implementar telefone;
5. implementar CEP;
6. implementar UF;
7. implementar data;
8. implementar nome;
9. testar cada validador.

### 38.4 Modelo

1. herdar de `UUIDTimestampedModel`;
2. adicionar campos;
3. adicionar autoria;
4. adicionar normalização;
5. implementar `clean()`;
6. implementar ativação e inativação;
7. adicionar Meta, índices e constraints;
8. registrar admin.

### 38.5 Alertas

1. criar estrutura de aviso;
2. implementar telefone repetido;
3. implementar e-mail repetido;
4. aplicar ownership;
5. excluir o próprio registro em edição;
6. proteger privacidade;
7. testar alertas.

### 38.6 Migration

1. gerar migration;
2. ler migration;
3. revisar dependências;
4. revisar constraints;
5. revisar índices;
6. não aplicar remotamente.

### 38.7 Validação final

1. executar `check`;
2. executar dry-run;
3. executar testes específicos;
4. executar regressão;
5. revisar diff;
6. verificar segredos;
7. atualizar documentação;
8. criar relatório.

---

## 39. Critérios de aceite

A etapa será considerada concluída quando:

1. `clientes.Cliente` existir;
2. PF e PJ compartilharem a mesma tabela;
3. UUID for utilizado;
4. `TipoCliente` estiver implementado;
5. `SituacaoCliente` estiver implementado;
6. os campos aprovados estiverem presentes;
7. endereço estiver incorporado;
8. contato principal estiver incorporado;
9. documento estiver normalizado;
10. documento for único;
11. CPF for validado;
12. CNPJ for validado;
13. tipo e documento forem coerentes;
14. nome for normalizado e validado;
15. telefone for normalizado e validado;
16. CEP for normalizado e validado;
17. e-mail for normalizado;
18. UF for normalizada e validada;
19. data futura for rejeitada;
20. novos clientes iniciarem ativos;
21. autoria estiver configurada;
22. índices estiverem presentes;
23. constraints estiverem presentes;
24. alertas de telefone funcionarem;
25. alertas de e-mail funcionarem;
26. alertas não bloquearem salvamento;
27. ownership e privacidade forem preservados;
28. migration inicial estiver revisada;
29. nenhuma migration remota tiver sido aplicada automaticamente;
30. testes passarem;
31. `manage.py check` passar;
32. nenhuma alteração pendente de modelagem for detectada;
33. documentação estiver atualizada;
34. nenhum segredo ou dado real tiver sido exposto.

---

## 40. Próxima etapa

Depois desta etapa, a próxima fase recomendada será:

```text
Fase 2.4 — Formulários e fluxo de cadastro de Cliente
```

Ela deverá incluir:

- ModelForm;
- comportamento dinâmico PF/PJ;
- máscaras apenas na interface;
- mensagens de validação;
- criação com autoria;
- exibição dos alertas de telefone e e-mail;
- edição;
- detalhes;
- ativação e inativação;
- proteção das rotas;
- templates iniciais.

---

## 41. Itens fora do escopo

Não implementar nesta etapa:

- CRUD completo;
- templates completos;
- JavaScript de máscaras;
- consulta automática de CEP;
- pesquisa;
- filtros;
- dashboard;
- relatórios;
- exportações;
- histórico completo;
- similaridade de nomes;
- upload;
- vínculo de arquivos com Cliente;
- app `arquivos`;
- movimentação de `ProtectedFile`;
- Supabase Auth;
- API pública;
- migrations remotas;
- deploy.

---

## 42. Conclusão

A decisão aprovada é implementar uma única entidade:

```text
clientes.Cliente
```

com:

- UUID;
- tipo PF/PJ;
- nome;
- CPF ou CNPJ;
- data de referência;
- e-mail;
- telefone;
- endereço;
- situação;
- observações;
- timestamps;
- autoria;
- constraints;
- índices;
- normalização;
- validadores de CPF e CNPJ;
- alertas não bloqueantes de telefone e e-mail repetidos.

O modelo utilizará as abstrações já criadas em `core`, preservará o usuário customizado e manterá a arquitetura backend-only com Supabase.
