---
name: modelo-cliente-validadores-dominio
description: Implementa e valida a entidade única Cliente, regras PF/PJ, normalização, CPF, CNPJ, constraints, auditoria, índices e alertas de duplicidade do projeto PC-DJANGO-001.
---

# Skill — Modelo Cliente e Validadores de Domínio
## Projeto PC-DJANGO-001

## 1. Finalidade

Esta skill orienta agentes de desenvolvimento na implementação da Fase 2.3 do projeto PC-DJANGO-001:

```text
Modelagem definitiva de Cliente
+
Validadores de domínio
```

O objetivo é criar uma única entidade `clientes.Cliente` para Pessoa Física e Pessoa Jurídica, com validações, normalização, auditoria, índices, constraints e alertas não bloqueantes de telefone e e-mail repetidos.

---

## 2. Quando usar

Use esta skill quando a tarefa envolver:

- criação do modelo `Cliente`;
- implementação de PF e PJ na mesma entidade;
- criação de `TipoCliente`;
- criação de `SituacaoCliente`;
- campos de endereço e contato;
- validação de CPF;
- validação de CNPJ;
- validação cruzada entre tipo e documento;
- normalização de documento, telefone, CEP, e-mail, nome e UF;
- unicidade de documento;
- constraints de banco;
- índices de pesquisa;
- campos de autoria;
- ativação e inativação;
- Django Admin de clientes;
- alertas de telefone repetido;
- alertas de e-mail repetido;
- migrations da app `clientes`;
- testes de modelos, validadores e duplicidade.

---

## 3. Fontes de verdade

Antes de alterar código, leia nesta ordem:

1. `AGENTS.md`;
2. `README.md`;
3. `Blueprint/01-requisitos/campocadastroskill.md`;
4. `Blueprint/02-modelagem/modelagem_dados_clientes_skill.md`;
5. especificação técnica do modelo Cliente e validadores;
6. especificação da estrutura modular das apps;
7. skill da estrutura modular;
8. relatório da etapa anterior;
9. código atual de `core`, `usuarios` e `clientes`;
10. migrations existentes;
11. estado atual do Git.

Em caso de conflito:

```text
Especificação aprovada desta etapa
→ AGENTS.md
→ Blueprint
→ README.md
→ código atual
```

Não invente campos, regras ou comportamentos fora das fontes aprovadas.

---

## 4. Estado atual esperado

Considere como baseline:

- Django configurado em `backend/`;
- app `core` criada;
- `core.UUIDTimestampedModel` existente e abstrato;
- `core.normalize_digits` existente;
- `core.normalize_whitespace` existente;
- app `usuarios` funcional;
- `AUTH_USER_MODEL` configurado;
- login por e-mail funcional;
- ownership por usuário já definido;
- app `clientes` criada, mas sem modelo definitivo;
- `ProtectedFile` ainda em `config`;
- Supabase acessado somente pelo backend;
- migrations remotas não aplicadas automaticamente;
- testes anteriores funcionando.

Se o repositório divergir, documente antes de implementar.

---

## 5. Decisões obrigatórias

A implementação deve respeitar:

1. PF e PJ usarão uma única entidade `Cliente`.
2. O campo `tipo` diferenciará PF e PJ.
3. O campo `nome` servirá para nome completo ou nome empresarial.
4. O campo `documento` servirá para CPF ou CNPJ.
5. O campo `data_referencia` servirá para nascimento ou abertura.
6. Endereço permanecerá dentro de `Cliente`.
7. Haverá apenas um telefone principal no MVP.
8. E-mail será opcional.
9. Documento será obrigatório e único.
10. Documento será armazenado somente com números.
11. Telefone será armazenado somente com números.
12. CEP será armazenado somente com números.
13. UF será armazenada em maiúsculas.
14. E-mail será armazenado em minúsculas.
15. Novo cliente iniciará como ativo.
16. Inativação será preferida à exclusão.
17. Telefone repetido gerará alerta, não bloqueio.
18. E-mail repetido gerará alerta, não bloqueio.
19. Documento repetido bloqueará.
20. O documento único será global.
21. Alertas de telefone e e-mail respeitarão ownership.
22. Não implementar similaridade de nomes nesta fase.
23. Não implementar CRUD completo nesta fase.
24. Não mover `ProtectedFile`.
25. Não criar app `arquivos`.
26. Não aplicar migrations no Supabase automaticamente.
27. Não introduzir frameworks adicionais.
28. Não duplicar normalizadores já existentes em `core`.
29. Não importar `usuarios.Usuario` diretamente.
30. Usar `settings.AUTH_USER_MODEL` em relacionamentos.

---

## 6. Estrutura esperada

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

Não criar arquivos sem responsabilidade concreta.

---

## 7. Choices do domínio

Implementar em:

```text
clientes/choices.py
```

### 7.1 Tipo de cliente

```python
class TipoCliente(models.TextChoices):
    PF = "PF", "Pessoa Física"
    PJ = "PJ", "Pessoa Jurídica"
```

### 7.2 Situação

```python
class SituacaoCliente(models.TextChoices):
    ATIVO = "ATIVO", "Ativo"
    INATIVO = "INATIVO", "Inativo"
```

### 7.3 UF

Criar coleção imutável ou `TextChoices` com as 27 UFs brasileiras.

Regras:

- valor persistido com duas letras;
- validação obrigatória quando preenchido;
- armazenamento em maiúsculas;
- campo opcional.

---

## 8. Modelo `Cliente`

Criar em:

```text
clientes/models.py
```

Nome:

```text
clientes.Cliente
```

Herança:

```python
from core.models import UUIDTimestampedModel

class Cliente(UUIDTimestampedModel):
    ...
```

Não duplicar:

- `id`;
- `criado_em`;
- `atualizado_em`.

---

## 9. Campos obrigatórios do modelo

Implementar:

```text
tipo
nome
documento
telefone
cep
situacao
```

Campos opcionais:

```text
data_referencia
email
logradouro
numero
complemento
bairro
cidade
estado
observacoes
criado_por
atualizado_por
```

---

## 10. Configuração esperada dos campos

### 10.1 Tipo

```python
tipo = models.CharField(
    max_length=2,
    choices=TipoCliente.choices,
    db_index=True,
)
```

### 10.2 Nome

```python
nome = models.CharField(
    max_length=200,
    db_index=True,
)
```

### 10.3 Documento

```python
documento = models.CharField(
    max_length=14,
    unique=True,
)
```

### 10.4 Data de referência

```python
data_referencia = models.DateField(
    null=True,
    blank=True,
)
```

### 10.5 E-mail

Preferir:

```python
email = models.EmailField(
    blank=True,
    default="",
    db_index=True,
)
```

Evitar mistura desnecessária entre `NULL` e string vazia.

### 10.6 Telefone

```python
telefone = models.CharField(
    max_length=11,
    db_index=True,
)
```

### 10.7 CEP

```python
cep = models.CharField(
    max_length=8,
)
```

### 10.8 Endereço

```text
logradouro: 200
numero: 20
complemento: 100
bairro: 100
cidade: 100
estado: 2
```

Todos opcionais.

### 10.9 Observações

```python
observacoes = models.TextField(blank=True)
```

### 10.10 Situação

```python
situacao = models.CharField(
    max_length=7,
    choices=SituacaoCliente.choices,
    default=SituacaoCliente.ATIVO,
    db_index=True,
)
```

---

## 11. Auditoria

### 11.1 Criado por

```python
criado_por = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    related_name="clientes_criados",
)
```

### 11.2 Atualizado por

```python
atualizado_por = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="clientes_atualizados",
)
```

### 11.3 Regras

- nunca aceitar autoria diretamente do navegador;
- formulários comuns não expõem esses campos;
- services ou views preenchem com `request.user`;
- usuário comum não transfere ownership;
- administrador só altera autoria por ação explícita;
- o fluxo comum deve preencher `criado_por`;
- o fluxo de edição deve atualizar `atualizado_por`.

---

## 12. Normalizadores

Reutilizar:

```python
from core.normalizers import normalize_digits, normalize_whitespace
```

Não duplicar essas funções.

Normalizar:

- nome;
- documento;
- telefone;
- CEP;
- e-mail;
- logradouro;
- número;
- complemento;
- bairro;
- cidade;
- estado;
- observações nos espaços externos, quando apropriado.

---

## 13. Validadores obrigatórios

Criar em:

```text
clientes/validators.py
```

Funções esperadas:

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

Regras:

- funções reutilizáveis;
- sem dependência de request;
- usar `ValidationError`;
- cobertas por testes;
- mensagens claras;
- não expor detalhes desnecessários.

---

## 14. CPF

O validador deve:

1. normalizar para dígitos;
2. exigir 11 dígitos;
3. rejeitar sequência repetida;
4. validar os dois dígitos verificadores;
5. rejeitar letras e comprimento inválido;
6. retornar ou aceitar apenas a forma normalizada.

Mensagem sugerida:

```text
Informe um CPF válido.
```

Exemplo válido de teste:

```text
52998224725
```

Não usar dados reais de usuários nos testes.

---

## 15. CNPJ

O validador deve:

1. normalizar para dígitos;
2. exigir 14 dígitos;
3. rejeitar sequência repetida;
4. validar os dois dígitos verificadores;
5. rejeitar letras e comprimento inválido;
6. retornar ou aceitar apenas a forma normalizada.

Mensagem sugerida:

```text
Informe um CNPJ válido.
```

Exemplo válido de teste:

```text
04252011000110
```

---

## 16. Documento por tipo

Implementar regra cruzada:

```text
PF → CPF com 11 dígitos e válido
PJ → CNPJ com 14 dígitos e válido
```

Rejeitar:

- CPF com tipo PJ;
- CNPJ com tipo PF;
- tipo inválido;
- documento ausente;
- documento incompatível.

Aplicar no `clean()` do modelo.

---

## 17. Nome

O campo deve:

- ser obrigatório;
- usar `normalize_whitespace`;
- possuir ao menos 3 caracteres úteis;
- rejeitar somente números;
- rejeitar somente símbolos;
- preservar acentos;
- preservar capitalização informada.

Mensagem sugerida:

```text
Informe um nome válido com pelo menos 3 caracteres.
```

---

## 18. Telefone

O campo deve:

- ser obrigatório;
- usar apenas dígitos;
- possuir 10 ou 11 dígitos;
- incluir DDD;
- não usar máscara no banco.

Mensagem sugerida:

```text
Informe um telefone com DDD e 10 ou 11 dígitos.
```

---

## 19. CEP

O campo deve:

- ser obrigatório;
- usar apenas dígitos;
- possuir exatamente 8 dígitos;
- não depender de serviço externo.

Mensagem sugerida:

```text
Informe um CEP com 8 dígitos.
```

---

## 20. Data

Quando preenchida:

- não pode estar no futuro;
- deve ser data válida;
- PF representa nascimento;
- PJ representa abertura;
- não aplicar idade mínima ou máxima nesta fase.

Mensagem sugerida:

```text
A data não pode estar no futuro.
```

---

## 21. E-mail

Quando preenchido:

- remover espaços;
- converter para minúsculas;
- validar formato;
- não ser único;
- permitir repetição com alerta;
- não bloquear salvamento.

---

## 22. UF

Quando preenchida:

- remover espaços;
- converter para maiúsculas;
- exigir duas letras;
- validar contra lista oficial.

Mensagem sugerida:

```text
Informe uma unidade federativa válida.
```

---

## 23. Normalização no modelo

Implementar método idempotente, por exemplo:

```python
def normalize_fields(self) -> None:
    ...
```

### `clean()`

Deve:

1. chamar `super().clean()`;
2. normalizar;
3. validar nome;
4. validar documento por tipo;
5. validar telefone;
6. validar CEP;
7. validar data;
8. validar UF;
9. validar escolhas;
10. validar e-mail pelo campo.

### `save()`

Pode normalizar antes de salvar.

Não depender de `save()` para validação completa.

Forms, services e admin devem seguir:

```text
normalizar
→ full_clean()
→ save()
```

---

## 24. Unicidade do documento

Documento deve ter:

```python
unique=True
```

A constraint deve ser global.

Mensagem de domínio:

```text
Já existe um cliente cadastrado com este documento.
```

Não revelar:

- nome do cadastro existente;
- proprietário;
- UUID;
- documento adicional;
- qualquer informação de outro usuário.

A validação antecipada não substitui a constraint do banco.

Tratar também `IntegrityError` em fluxos futuros com mensagem genérica.

---

## 25. Constraints de banco

Criar constraints para:

1. `tipo` válido;
2. `situacao` válida;
3. PF com documento de 11 dígitos;
4. PJ com documento de 14 dígitos;
5. CEP com 8 dígitos;
6. telefone com 10 ou 11 dígitos.

Requisitos:

- compatível com PostgreSQL;
- compatível com SQLite de testes;
- nomes explícitos;
- sem lógica de dígito verificador no banco;
- revisar migration gerada.

---

## 26. Índices

Implementar índices para:

- nome;
- telefone;
- e-mail;
- tipo;
- situação;
- criado_em;
- atualizado_em.

Índices compostos:

```text
estado, cidade
tipo, situacao
```

Não duplicar índice do documento, pois `unique=True` já cria índice único.

---

## 27. Meta e representação

Configuração esperada:

```python
class Meta:
    ordering = ("nome",)
    verbose_name = "Cliente"
    verbose_name_plural = "Clientes"
```

Representação:

```python
def __str__(self) -> str:
    return self.nome
```

---

## 28. Ativação e inativação

Criar operações:

```python
ativar()
inativar()
```

Regras:

- idempotentes;
- não excluem;
- alteram apenas situação;
- fluxo externo atualiza `atualizado_por`;
- não criar histórico completo.

---

## 29. Alertas de duplicidade

Implementar em:

```text
clientes/services.py
```

Não usar `ValidationError` para telefone ou e-mail repetidos.

Não colocar em `core`.

Não colocar em `model.clean()`.

Interface conceitual:

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

A estrutura pode conter:

```text
code
field
message
count
```

---

## 30. Regras dos alertas

### Telefone

Mensagem:

```text
Já existe outro cliente com este telefone.
```

### E-mail

Mensagem:

```text
Já existe outro cliente com este e-mail.
```

### Regras gerais

- não bloquear salvamento;
- ignorar valores vazios;
- comparar dados normalizados;
- excluir o próprio registro em edição;
- retornar alertas independentes;
- não identificar o outro registro;
- não fazer merge automático;
- não alterar cadastros existentes.

---

## 31. Escopo de ownership nos alertas

Para usuário comum:

```text
consultar somente clientes visíveis ao próprio usuário
```

Para administrador:

```text
permitir consulta global
```

Reutilizar helper de ownership existente.

Não revelar ao usuário comum dados fora do seu escopo.

O documento único continuará global, mas a mensagem de conflito será genérica.

---

## 32. Similaridade de nome

Não implementar nesta etapa:

- fuzzy search;
- trigram;
- Levenshtein;
- alertas de nome parecido;
- bloqueio de nomes iguais.

Registrar apenas como próxima evolução.

---

## 33. Django Admin

Registrar `Cliente`.

Configurar:

- listagem com nome, tipo, situação, telefone, cidade e estado;
- busca por nome, documento, telefone e e-mail;
- filtros por tipo, situação, estado e datas;
- timestamps somente leitura;
- autoria somente leitura após criação;
- ações de ativar e inativar;
- ordenação por nome;
- documento mascarado em listagem, quando possível;
- documento completo apenas em tela autorizada;
- sem exposição de segredos;
- sem regras paralelas divergentes do domínio.

---

## 34. Privacidade

Preservar:

- autenticação;
- ownership;
- documento mascarado em listagens futuras;
- nenhuma PII em logs;
- nenhuma informação de outro usuário em mensagens;
- dados fictícios em testes;
- observações sem coleta desnecessária;
- nenhum segredo do Supabase no domínio.

Não registrar em logs:

- CPF;
- CNPJ;
- telefone;
- e-mail;
- observações;
- corpo completo de formulários.

---

## 35. Migration inicial

Criar:

```text
clientes/migrations/0001_initial.py
```

A migration deve:

- criar somente `Cliente`;
- depender de `settings.AUTH_USER_MODEL` via `swappable_dependency`;
- incluir índices;
- incluir constraints;
- preservar migrations anteriores;
- não criar tabela de `core.UUIDTimestampedModel`;
- não tocar `ProtectedFile`;
- não executar operação destrutiva;
- não ser aplicada automaticamente ao Supabase.

---

## 36. Regras de migrations

Antes de gerar:

1. revisar migrations atuais;
2. confirmar que `clientes` ainda não possui migration concreta;
3. confirmar que `core` permanece sem tabela;
4. confirmar compatibilidade com usuário customizado.

Depois de gerar:

1. ler a migration inteira;
2. revisar dependências;
3. revisar `on_delete`;
4. revisar índices;
5. revisar constraints;
6. verificar nomes;
7. executar dry-run;
8. executar testes.

Não editar migration gerada de forma irrefletida.

---

## 37. Testes obrigatórios de CPF

Cobrir:

1. válido formatado;
2. válido sem máscara;
3. inválido;
4. curto;
5. longo;
6. repetido;
7. letras.

---

## 38. Testes obrigatórios de CNPJ

Cobrir:

1. válido formatado;
2. válido sem máscara;
3. inválido;
4. curto;
5. longo;
6. repetido;
7. letras.

---

## 39. Testes obrigatórios de outros validadores

Cobrir:

- telefone com 10 dígitos;
- telefone com 11 dígitos;
- telefone inválido;
- CEP válido;
- CEP inválido;
- UF válida;
- UF inválida;
- data passada;
- data futura;
- nome válido;
- nome curto;
- nome numérico;
- nome simbólico.

---

## 40. Testes obrigatórios do modelo

Cobrir:

1. PF válida;
2. PJ válida;
3. UUID automático;
4. situação padrão ativa;
5. timestamps;
6. normalização de nome;
7. normalização de documento;
8. normalização de telefone;
9. normalização de CEP;
10. normalização de e-mail;
11. normalização de UF;
12. CPF com tipo PJ rejeitado;
13. CNPJ com tipo PF rejeitado;
14. documento obrigatório;
15. documento único;
16. telefone obrigatório;
17. CEP obrigatório;
18. e-mail opcional;
19. endereço opcional;
20. autoria;
21. `criado_por` protegido;
22. `atualizado_por` anulável;
23. ativação idempotente;
24. inativação idempotente;
25. ordenação;
26. `__str__`.

---

## 41. Testes obrigatórios dos alertas

Cobrir:

1. telefone repetido gera alerta;
2. e-mail repetido gera alerta;
3. telefone repetido não bloqueia;
4. e-mail repetido não bloqueia;
5. vazio não gera alerta;
6. edição exclui o próprio registro;
7. usuário comum limita escopo;
8. usuário comum não recebe dados de terceiros;
9. administrador detecta globalmente;
10. telefone compara normalizado;
11. e-mail compara normalizado;
12. dois alertas distintos podem ser retornados.

---

## 42. Testes de regressão

Confirmar que continuam funcionando:

- login;
- logout;
- perfil;
- troca de senha;
- Django Admin de usuários;
- `AUTH_USER_MODEL`;
- ownership;
- `ProtectedFile`;
- Storage privado;
- redaction de secrets;
- testes de `config`;
- testes de `usuarios`;
- testes de `core`.

---

## 43. Ordem de implementação

### 43.1 Auditoria

1. ler documentação;
2. revisar `core`;
3. revisar `clientes`;
4. revisar ownership;
5. revisar migrations;
6. executar baseline de testes.

### 43.2 Choices

1. criar tipo;
2. criar situação;
3. criar UF;
4. testar.

### 43.3 Validadores

1. CPF;
2. CNPJ;
3. documento por tipo;
4. telefone;
5. CEP;
6. UF;
7. data;
8. nome;
9. testes.

### 43.4 Modelo

1. herdar base abstrata;
2. criar campos;
3. criar autoria;
4. normalizar;
5. implementar `clean()`;
6. implementar ativação;
7. implementar inativação;
8. criar índices;
9. criar constraints;
10. registrar admin.

### 43.5 Alertas

1. criar estrutura de aviso;
2. implementar telefone;
3. implementar e-mail;
4. aplicar ownership;
5. excluir próprio registro;
6. proteger privacidade;
7. testar.

### 43.6 Migration

1. gerar;
2. revisar;
3. validar dependências;
4. validar constraints;
5. validar índices;
6. não aplicar remotamente.

### 43.7 Validação final

1. executar check;
2. executar dry-run;
3. executar testes específicos;
4. executar regressão;
5. revisar diff;
6. revisar segredos;
7. atualizar documentação;
8. gerar relatório.

---

## 44. Comandos de verificação

Executar da raiz:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py test clientes core usuarios config
python backend/manage.py test
```

A migration inicial deve ser gerada antes do dry-run.

Não executar automaticamente:

```powershell
python backend/manage.py migrate
```

contra o Supabase.

---

## 45. Critérios de aceite

Considere a etapa concluída somente quando:

1. `clientes.Cliente` existir;
2. PF e PJ usarem uma única tabela;
3. UUID estiver ativo;
4. choices estiverem implementadas;
5. campos aprovados estiverem presentes;
6. endereço estiver incorporado;
7. contato estiver incorporado;
8. documento estiver normalizado;
9. documento estiver único;
10. CPF estiver validado;
11. CNPJ estiver validado;
12. tipo e documento forem coerentes;
13. nome estiver normalizado e validado;
14. telefone estiver normalizado e validado;
15. CEP estiver normalizado e validado;
16. e-mail estiver normalizado;
17. UF estiver normalizada e validada;
18. data futura for rejeitada;
19. situação padrão for ativa;
20. autoria estiver correta;
21. índices existirem;
22. constraints existirem;
23. alertas de telefone funcionarem;
24. alertas de e-mail funcionarem;
25. alertas não bloquearem;
26. ownership for preservado;
27. privacidade for preservada;
28. admin estiver configurado;
29. migration estiver revisada;
30. migration remota não tiver sido aplicada;
31. testes passarem;
32. `manage.py check` passar;
33. dry-run estiver estável;
34. documentação estiver atualizada;
35. nenhum segredo ou dado real estiver exposto.

---

## 46. Fora do escopo

Não implementar:

- CRUD completo;
- templates completos;
- JavaScript de máscaras;
- integração automática com CEP;
- pesquisa;
- filtros;
- dashboard;
- relatórios;
- exportações;
- histórico completo;
- similaridade de nomes;
- upload;
- relação de arquivos com Cliente;
- app `arquivos`;
- movimentação de `ProtectedFile`;
- Supabase Auth;
- API pública;
- migrations remotas;
- deploy.

---

## 47. Próxima etapa

A próxima fase será:

```text
Fase 2.4 — Formulários e fluxo de cadastro de Cliente
```

Ela deverá tratar:

- ModelForm;
- PF/PJ dinâmico;
- máscaras de interface;
- mensagens de erro;
- criação com autoria;
- exibição de alertas;
- edição;
- detalhes;
- ativação;
- inativação;
- rotas protegidas;
- templates iniciais.

---

## 48. Restrições do agente

O agente deve:

- trabalhar de forma incremental;
- preservar código existente;
- não expor `.env`;
- não imprimir segredos;
- não registrar PII;
- não fazer commit;
- não fazer push;
- não aplicar migration remota;
- não executar operações destrutivas;
- não alterar Blueprint silenciosamente;
- não ampliar escopo;
- não mover `ProtectedFile`;
- não criar app `arquivos`;
- não implementar CRUD completo;
- registrar bloqueadores com clareza.

---

## 49. Saída esperada

Ao concluir uma implementação baseada nesta skill, apresentar:

1. subetapas concluídas;
2. arquivos alterados;
3. choices criadas;
4. validadores criados;
5. modelo criado;
6. constraints e índices;
7. serviço de alertas;
8. admin configurado;
9. migration criada;
10. testes executados;
11. resultados dos comandos;
12. documentação atualizada;
13. bloqueadores;
14. riscos restantes;
15. próxima fase;
16. veredito:
   - `READY`;
   - `READY WITH RESERVATIONS`;
   - `NOT READY`.
