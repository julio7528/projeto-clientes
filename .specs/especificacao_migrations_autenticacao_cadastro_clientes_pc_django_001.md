# Especificação Técnica — Migrations, Proteção das Páginas e Cadastro de Clientes
## Projeto PC-DJANGO-001

## 1. Identificação da etapa

**Fase principal:** Fase 2 — Banco definitivo e funcionalidades centrais do MVP  
**Subetapas abrangidas:**

```text
2.4 — Migrations definitivas e banco PostgreSQL no Supabase
2.5 — Autenticação integrada e proteção das páginas
2.6 — Cadastro e gestão inicial de clientes
```

**Status:** Especificação aprovada para implementação futura  
**Escopo deste documento:** definir a aplicação controlada das migrations no PostgreSQL do Supabase, a validação do fluxo de autenticação existente e a implementação das páginas iniciais de cadastro e gestão de clientes.

---

## 2. Objetivo

Concluir a fundação operacional do sistema e disponibilizar o primeiro fluxo funcional completo do MVP:

```text
Usuário autenticado
        ↓
Página interna protegida
        ↓
Cadastro de Cliente PF ou PJ
        ↓
Validação e alerta de duplicidade
        ↓
Persistência pelo Django ORM
        ↓
PostgreSQL no Supabase
        ↓
Detalhes, edição, ativação e inativação
```

A etapa deverá transformar a modelagem já concluída em uma aplicação utilizável, mantendo:

- Django como única camada de autenticação;
- sessões seguras;
- isolamento dos dados por usuário;
- acesso total apenas para administrador;
- Supabase acessado somente pelo backend;
- PostgreSQL gerenciado por migrations do Django;
- ausência de credenciais privilegiadas no navegador;
- preferência por inativação em vez de exclusão.

---

## 3. Estado atual considerado

Esta especificação considera que o repositório já possui:

1. projeto Django em `backend/`;
2. conexão com PostgreSQL no Supabase por `DATABASE_URL`;
3. configuração de SSL;
4. app `core`;
5. app `usuarios`;
6. modelo customizado `usuarios.Usuario`;
7. autenticação por e-mail e senha;
8. login, logout, perfil e troca de senha;
9. app `clientes`;
10. modelo definitivo `clientes.Cliente`;
11. choices de tipo, situação e UF;
12. validadores de CPF, CNPJ, telefone, CEP, UF, data e nome;
13. normalização de dados;
14. documento globalmente único;
15. alertas de telefone e e-mail repetidos;
16. ownership por usuário;
17. Django Admin de usuários e clientes;
18. migrations geradas para `usuarios`, `config` e `clientes`;
19. testes automatizados das etapas anteriores;
20. integração backend-only com Supabase;
21. `ProtectedFile` ainda localizado em `config`;
22. nenhuma migration remota aplicada automaticamente pelo agente.

Antes de implementar, o agente deverá confirmar o estado real do repositório e não apenas assumir que todos os itens existem.

---

## 4. Observação sobre a quantidade de fases

Embora o planejamento tenha sido apresentado como “duas fases”, o escopo contém três blocos técnicos distintos:

1. banco e migrations;
2. autenticação e proteção;
3. cadastro e gestão inicial de clientes.

Eles serão executados na mesma etapa de trabalho, mas em ordem obrigatória. O cadastro não poderá ser validado no Supabase antes da conclusão segura das migrations.

---

## 5. Decisões obrigatórias

1. Django continuará sendo a única fonte de identidade e sessão.
2. Supabase Auth não será utilizado.
3. Login continuará sendo realizado por e-mail e senha.
4. Não haverá cadastro público de usuários.
5. Apenas o administrador criará usuários.
6. Todas as páginas de clientes exigirão autenticação.
7. Usuários comuns acessarão somente os próprios clientes.
8. Administradores poderão acessar todos os clientes.
9. Tentativas de acesso a cliente de outro usuário retornarão `404`.
10. O formulário será único para PF e PJ.
11. A interface alterará rótulos e máscaras de acordo com o tipo.
12. O mesmo modelo `Cliente` será utilizado para PF e PJ.
13. Documento duplicado bloqueará o salvamento.
14. Telefone e e-mail repetidos gerarão confirmação, sem bloqueio definitivo.
15. O usuário deverá confirmar explicitamente que deseja continuar quando houver alertas.
16. Novos clientes iniciarão ativos.
17. Ativação e inativação serão ações explícitas.
18. Não haverá exclusão física de clientes nesta etapa.
19. Endereço poderá ser preenchido manualmente.
20. Consulta externa de CEP ficará fora desta etapa.
21. Pesquisa avançada e filtros ficarão fora desta etapa.
22. Dashboard e relatórios ficarão fora desta etapa.
23. `ProtectedFile` não será movido.
24. Não será criada a app `arquivos`.
25. Nenhuma credencial será colocada em templates, JavaScript, logs ou respostas.
26. Nenhuma migration será editada silenciosamente depois de aplicada.
27. Migrations deverão ser aplicadas primeiro em ambiente de desenvolvimento isolado.
28. O banco de produção nunca deverá ser o primeiro ambiente de aplicação.
29. A criação do superusuário ocorrerá somente depois das migrations.
30. Senhas não poderão aparecer no comando, histórico do terminal, relatório ou Git.

---

# PARTE I — MIGRATIONS DEFINITIVAS E BANCO SUPABASE

## 6. Objetivo das migrations

Criar no PostgreSQL do Supabase todas as tabelas, constraints, índices e relações aprovadas no projeto, incluindo:

- autenticação e sessões nativas do Django;
- modelo customizado `usuarios.Usuario`;
- modelo `config.ProtectedFile`;
- modelo `clientes.Cliente`;
- tabelas administrativas do Django;
- permissões;
- grupos;
- content types;
- migrations;
- sessões.

O Django ORM será a única autoridade para mudanças estruturais.

Não criar ou alterar tabelas manualmente pelo painel SQL do Supabase.

---

## 7. Classificação obrigatória do ambiente Supabase

Antes de executar `migrate`, o projeto Supabase deverá ser classificado explicitamente como:

```text
DESENVOLVIMENTO
QA/HOMOLOGAÇÃO
PRODUÇÃO
```

### 7.1 Regras

- o primeiro `migrate` deverá ocorrer em desenvolvimento;
- desenvolvimento deverá usar somente dados fictícios;
- QA deverá possuir banco separado;
- produção deverá possuir banco separado;
- credenciais deverão ser distintas;
- um projeto com dados reais não poderá ser tratado como desenvolvimento;
- o relatório deverá registrar apenas a classificação, nunca credenciais.

### 7.2 Ambiente atual

Se existir apenas um projeto Supabase:

- confirmar que ele é de desenvolvimento;
- confirmar que não possui dados reais;
- confirmar que pode ser recriado em caso de falha;
- interromper se houver dúvida sobre dados existentes.

---

## 8. Pré-condições para aplicar migrations

A aplicação somente poderá continuar quando:

1. `git status` tiver sido revisado;
2. o branch atual estiver identificado;
3. migrations estiverem versionadas;
4. `python backend/manage.py check` passar;
5. `makemigrations --check --dry-run` retornar `No changes detected`;
6. todos os testes passarem;
7. a conexão real com o Supabase funcionar;
8. o host corresponder ao projeto esperado;
9. o banco esperado estiver selecionado;
10. o plano de migrations estiver revisado;
11. o banco estiver vazio ou possuir backup adequado;
12. não houver migration conflitante com o usuário customizado;
13. `AUTH_USER_MODEL` estiver configurado antes da primeira migration de autenticação;
14. nenhuma credencial tiver sido exposta;
15. o operador tiver autorização explícita para alterar o banco.

---

## 9. Auditoria manual das migrations

Revisar integralmente:

```text
backend/usuarios/migrations/
backend/config/migrations/
backend/clientes/migrations/
```

E também as dependências das apps nativas do Django.

### 9.1 Verificações obrigatórias

- ordem das dependências;
- `swappable_dependency(settings.AUTH_USER_MODEL)`;
- criação de `usuarios.Usuario` antes de relações dependentes;
- criação de `ProtectedFile`;
- alteração de ownership para `PROTECT`, quando prevista;
- criação de `Cliente`;
- UUIDs;
- `on_delete`;
- índices;
- constraints;
- unicidade de documento;
- ausência de operações destrutivas;
- ausência de `RunSQL` não justificado;
- ausência de credenciais;
- ausência de nomes de tabelas inesperados;
- ausência de migration concreta para modelos abstratos de `core`.

---

## 10. Banco isolado para testes

Antes do Supabase, executar a suíte usando banco de teste isolado.

### 10.1 Teste obrigatório

```powershell
python backend/manage.py test
```

O banco de teste deverá:

- ser criado automaticamente;
- receber todas as migrations;
- executar todos os testes;
- ser destruído ao final;
- não reutilizar dados reais;
- não acessar o banco de produção.

### 10.2 Compatibilidade PostgreSQL

Como constraints podem se comportar de forma diferente entre SQLite e PostgreSQL, a validação ideal deverá ocorrer também em um PostgreSQL de desenvolvimento descartável ou em um projeto Supabase exclusivo de desenvolvimento.

O teste SQLite em memória continua obrigatório, mas não substitui a validação real no PostgreSQL antes de produção.

---

## 11. Comandos de inspeção antes da aplicação

Executar:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py showmigrations
python backend/manage.py showmigrations --plan
python backend/manage.py migrate --plan
python backend/manage.py test
```

A saída deverá ser revisada e resumida no relatório sem dados sensíveis.

---

## 12. Conexão real antes das migrations

Executar teste sanitizado:

```powershell
python backend/manage.py shell -c "from django.db import connection; connection.ensure_connection(); print(connection.vendor); print(connection.is_usable())"
```

Resultado esperado:

```text
postgresql
True
```

Não imprimir:

- host completo quando contiver informação sensível;
- usuário;
- senha;
- `DATABASE_URL`;
- tokens;
- chaves Supabase.

---

## 13. Backup e ponto de restauração

### 13.1 Banco vazio de desenvolvimento

Quando o banco estiver comprovadamente vazio:

- registrar o plano de migrations;
- registrar o estado anterior;
- confirmar que não existem dados reais;
- confirmar que o projeto pode ser recriado.

### 13.2 Banco com tabelas ou dados

Antes de `migrate`:

- criar backup adequado;
- registrar horário do backup;
- validar que o backup terminou;
- não prosseguir com backup incompleto;
- não armazenar o backup no repositório Git.

### 13.3 Falha

Em caso de falha:

- interromper imediatamente;
- não apagar tabelas manualmente;
- não editar `django_migrations` diretamente;
- não repetir comandos destrutivos;
- registrar migration, erro e estado;
- restaurar somente por procedimento controlado.

---

## 14. Aplicação controlada no Supabase

A aplicação deverá ocorrer somente depois da aprovação das pré-condições.

Comando:

```powershell
python backend/manage.py migrate
```

### 14.1 Regras de execução

- executar uma única vez;
- não usar `--fake`;
- não usar `--fake-initial` sem justificativa formal;
- não usar SQL manual para simular migration;
- monitorar a saída completa;
- interromper se houver erro;
- não ocultar warnings;
- não aplicar migration de outra branch.

---

## 15. Verificação após `migrate`

Executar:

```powershell
python backend/manage.py showmigrations
python backend/manage.py showmigrations --plan
python backend/manage.py check
```

Verificar:

- todas as migrations esperadas marcadas com `[X]`;
- tabela de usuários criada;
- tabela de clientes criada;
- tabela de arquivos protegidos preservada;
- tabelas nativas do Django;
- índices esperados;
- constraints esperadas;
- conexão utilizável;
- ausência de migrations pendentes.

Executar smoke test pelo ORM:

```text
contar usuários
contar clientes
consultar content types
validar uma transação simples sem persistir dado real
```

---

## 16. Criação do primeiro superusuário

A criação ocorrerá após o banco estar migrado.

Comando recomendado:

```powershell
python backend/manage.py createsuperuser --email EMAIL_DO_ADMINISTRADOR
```

### 16.1 Regras

- usar e-mail administrativo real somente no ambiente correto;
- digitar a senha de forma interativa;
- não colocar senha no comando;
- não usar senha em arquivo versionado;
- não registrar senha no relatório;
- não compartilhar a conta;
- manter `is_active=True`;
- manter `is_staff=True`;
- manter `is_superuser=True`;
- completar os dados de perfil pelo Django Admin quando necessário;
- confirmar login no Admin;
- confirmar logout.

### 16.2 Duplicidade

Antes de criar:

- verificar se já existe superusuário;
- não criar contas administrativas duplicadas sem necessidade;
- não alterar senha de conta existente sem autorização.

---

# PARTE II — AUTENTICAÇÃO E PROTEÇÃO DAS PÁGINAS

## 17. Estado da autenticação

A autenticação já existente deverá ser preservada e integrada ao fluxo de clientes.

Não reescrever desnecessariamente:

- modelo `Usuario`;
- manager;
- backend de autenticação;
- login;
- logout;
- perfil;
- alteração de senha;
- Django Admin;
- sessões;
- cookies;
- CSRF.

A tarefa desta fase é validar, proteger e integrar.

---

## 18. Fluxo de autenticação

```text
Usuário acessa página interna
        ↓
Não autenticado?
        ↓ sim
Redirecionar para login com parâmetro next
        ↓
Login por e-mail e senha
        ↓
Criar/renovar sessão Django
        ↓
Redirecionar para next seguro
        ↓
Sem next: redirecionar para lista de clientes
```

Enquanto o dashboard não estiver implementado, o destino padrão após login será:

```text
clientes:list
```

Essa decisão será temporária até a criação do dashboard.

---

## 19. Redirecionamentos

### 19.1 Login bem-sucedido

Prioridade:

1. parâmetro `next` válido e interno;
2. lista de clientes.

Não permitir redirecionamento para domínio externo.

### 19.2 Login inválido

- manter e-mail preenchido;
- não manter senha;
- mensagem genérica;
- não revelar se o e-mail existe;
- não revelar se a conta está inativa.

Mensagem sugerida:

```text
E-mail ou senha inválidos.
```

### 19.3 Usuário já autenticado

Ao abrir a tela de login:

```text
redirecionar para clientes:list
```

### 19.4 Logout

- somente `POST`;
- protegido por CSRF;
- encerrar sessão;
- redirecionar para login;
- não aceitar logout por `GET`.

---

## 20. Rotas públicas

Somente estas rotas poderão ser públicas:

- login;
- arquivos estáticos necessários ao login;
- endpoints técnicos explicitamente aprovados.

Não haverá:

- signup público;
- recuperação por e-mail;
- reset público;
- login social;
- OAuth;
- Supabase Auth.

---

## 21. Rotas internas protegidas

Todas as rotas de clientes deverão usar:

```python
@login_required
```

ou:

```python
LoginRequiredMixin
```

Rotas previstas:

```text
GET  /clientes/
GET  /clientes/novo/
POST /clientes/novo/
GET  /clientes/<uuid:pk>/
GET  /clientes/<uuid:pk>/editar/
POST /clientes/<uuid:pk>/editar/
POST /clientes/<uuid:pk>/ativar/
POST /clientes/<uuid:pk>/inativar/
```

Atalhos opcionais para pré-seleção:

```text
/clientes/novo/?tipo=PF
/clientes/novo/?tipo=PJ
```

O parâmetro deverá ser validado contra `TipoCliente`.

---

## 22. Controle de acesso por objeto

### 22.1 Usuário comum

Poderá:

- listar os próprios clientes;
- criar clientes próprios;
- visualizar clientes próprios;
- editar clientes próprios;
- ativar clientes próprios;
- inativar clientes próprios.

### 22.2 Administrador

Poderá:

- listar todos;
- criar;
- visualizar todos;
- editar todos;
- ativar;
- inativar;
- acessar Django Admin.

### 22.3 Consulta segura

Objetos deverão ser obtidos a partir de queryset já limitado:

```python
queryset = scope_owned_queryset(
    Cliente.objects.all(),
    request.user,
    owner_field="criado_por",
)

cliente = get_object_or_404(queryset, pk=pk)
```

Não buscar o objeto globalmente para depois testar ownership.

### 22.4 Resposta para acesso cruzado

Retornar:

```text
404 Not Found
```

Não retornar `403` que confirme a existência do cliente.

Não revelar:

- nome;
- documento;
- proprietário;
- UUID;
- situação;
- qualquer detalhe do registro.

---

## 23. Sessões e cookies

Preservar:

- `SESSION_COOKIE_HTTPONLY=True`;
- `SESSION_COOKIE_SECURE=True` em produção;
- `CSRF_COOKIE_SECURE=True` em produção;
- `SESSION_COOKIE_SAMESITE="Lax"` ou equivalente;
- CSRF ativo;
- HTTPS em produção;
- HSTS conforme configuração aprovada;
- nenhum token em `localStorage`;
- nenhuma credencial Supabase no navegador.

Páginas com dados pessoais deverão retornar:

```text
Cache-Control: private, no-store
Pragma: no-cache
```

Aplicar especialmente a:

- detalhes;
- criação;
- edição;
- perfil;
- respostas com alertas de duplicidade.

---

## 24. Layout interno

Criar ou reutilizar um layout autenticado compartilhado.

Elementos mínimos:

- nome do sistema;
- usuário autenticado;
- menu principal;
- link para clientes;
- link para novo cliente;
- link para perfil;
- botão de logout em formulário `POST`;
- área de mensagens;
- breadcrumb;
- conteúdo principal;
- suporte responsivo;
- HTML semântico;
- navegação por teclado.

Não implementar dashboard ou relatórios completos nesta etapa.

---

# PARTE III — CADASTRO E GESTÃO INICIAL DE CLIENTES

## 25. Escopo funcional

Implementar:

1. lista simples de clientes;
2. cadastro;
3. detalhes;
4. edição;
5. ativação;
6. inativação;
7. validação;
8. mensagens;
9. confirmação de duplicidade não bloqueante;
10. isolamento por usuário.

A lista simples é necessária para completar o fluxo, mas não deverá incluir pesquisa avançada ou filtros nesta etapa.

---

## 26. Formulário único PF/PJ

Criar:

```text
clientes.forms.ClienteForm
```

Base:

```python
forms.ModelForm
```

Modelo:

```text
clientes.Cliente
```

Campos editáveis:

```text
tipo
nome
documento
data_referencia
email
telefone
cep
logradouro
numero
complemento
bairro
cidade
estado
observacoes
```

Não incluir:

```text
id
situacao
criado_em
atualizado_em
criado_por
atualizado_por
```

A situação será administrada por ações explícitas.

---

## 27. Comportamento PF/PJ

### 27.1 PF

Rótulos:

```text
Nome completo
CPF
Data de nascimento
```

Máscara:

```text
000.000.000-00
```

### 27.2 PJ

Rótulos:

```text
Nome empresarial
CNPJ
Data de abertura
```

Máscara:

```text
00.000.000/0000-00
```

### 27.3 Alteração do tipo

Quando o tipo mudar:

- atualizar rótulos;
- atualizar máscara;
- avisar que o documento será limpo;
- limpar documento;
- preservar os demais campos;
- executar validação também no backend.

Mensagem sugerida:

```text
Ao alterar o tipo de cliente, o documento informado será removido.
```

---

## 28. Máscaras de interface

Aplicar com JavaScript simples e local:

- CPF;
- CNPJ;
- telefone;
- CEP.

Regras:

- JavaScript não substitui validação backend;
- o backend recebe e normaliza valores;
- nenhuma biblioteca externa é obrigatória;
- não enviar dados a terceiros;
- não expor credenciais;
- funcionar progressivamente sem JavaScript;
- usar teclado numérico apropriado em dispositivos móveis.

---

## 29. Endereço

Campos:

- CEP;
- logradouro;
- número;
- complemento;
- bairro;
- cidade;
- estado.

Nesta etapa:

- preenchimento manual obrigatório como alternativa;
- não depender de API externa;
- não bloquear por ausência de consulta automática;
- preservar valores em falhas;
- validar CEP e UF no backend.

Consulta automática de CEP será implementada em etapa posterior.

---

## 30. Situação

Novo cliente:

```text
ATIVO
```

O campo não será controlado diretamente pelo formulário comum.

Ações disponíveis:

```text
Ativar
Inativar
```

Regras:

- somente `POST`;
- CSRF obrigatório;
- idempotentes;
- exigir ownership;
- registrar `atualizado_por`;
- exibir mensagem de sucesso;
- redirecionar para detalhes;
- não excluir fisicamente.

---

## 31. Autoria

### 31.1 Criação

No backend:

```python
cliente.criado_por = request.user
cliente.atualizado_por = request.user
```

Não confiar em campos enviados pelo navegador.

### 31.2 Edição

No backend:

```python
cliente.atualizado_por = request.user
```

Não alterar `criado_por`.

### 31.3 Administrador

O administrador poderá editar registros, mas a mudança de autoria não será feita pelo formulário comum.

---

## 32. Persistência segura

Fluxo recomendado:

```text
POST
↓
ClienteForm.is_valid()
↓
form.save(commit=False)
↓
definir autoria
↓
full_clean()
↓
verificar alertas
↓
salvar em transação
↓
redirect
```

Usar:

```python
transaction.atomic()
```

nas operações de criação e edição.

Tratar `IntegrityError` de documento duplicado com mensagem genérica.

Não retornar exceção técnica ao usuário.

---

## 33. Documento duplicado

Documento duplicado deverá bloquear.

Mensagens:

```text
Este CPF já está cadastrado.
Este CNPJ já está cadastrado.
```

Quando não for seguro diferenciar:

```text
Já existe um cliente cadastrado com este documento.
```

Não revelar:

- nome do cliente existente;
- usuário proprietário;
- UUID;
- link;
- situação;
- qualquer dado fora do escopo do usuário.

A constraint global do banco será a defesa final.

---

## 34. Telefone e e-mail repetidos

### 34.1 Natureza

São alertas não bloqueantes.

### 34.2 Fluxo em duas etapas

```text
Usuário envia formulário
        ↓
Formulário válido
        ↓
Detectar telefone/e-mail repetidos
        ↓
Há alertas e não houve confirmação?
        ↓ sim
Reexibir o formulário com alertas
        ↓
Botão "Salvar mesmo assim"
        ↓
Novo POST com confirmação
        ↓
Revalidar tudo
        ↓
Salvar
```

### 34.3 Confirmação

Utilizar campo interno não persistente, como:

```text
confirmar_duplicidade=1
```

O backend deverá:

- não confiar apenas no JavaScript;
- recalcular alertas no segundo POST;
- exigir confirmação explícita;
- ignorar confirmação antiga se os dados mudaram;
- não armazenar o campo no modelo.

### 34.4 Mensagens

```text
Este telefone já está associado a outro cliente. Deseja continuar?
Este e-mail já está associado a outro cliente. Deseja continuar?
```

### 34.5 Privacidade

Usuários comuns verão alertas apenas dentro do próprio escopo.

Administradores poderão receber alertas globais.

Não identificar o outro registro.

---

## 35. Página de lista

Rota:

```text
GET /clientes/
```

Exibir:

- nome;
- tipo;
- documento mascarado;
- telefone formatado;
- cidade/UF;
- situação;
- ações de detalhes e edição.

Regras:

- usuário comum vê somente os próprios;
- administrador vê todos;
- ordenação por nome;
- paginação simples recomendada;
- sem pesquisa avançada;
- sem filtros avançados;
- sem exportação;
- documento sempre mascarado;
- estado vazio tratado com `—`.

---

## 36. Página de cadastro

Rota:

```text
GET|POST /clientes/novo/
```

Requisitos:

- autenticação;
- formulário único;
- tipo obrigatório;
- atalhos PF e PJ por query string validada;
- erros próximos aos campos;
- manter valores após erro;
- foco no primeiro erro;
- impedir duplo clique visualmente;
- backend protegido contra duplicação;
- mensagem de sucesso;
- redirecionar para detalhes.

Mensagem:

```text
Cliente cadastrado com sucesso.
```

---

## 37. Página de detalhes

Rota:

```text
GET /clientes/<uuid:pk>/
```

Exibir:

- tipo;
- nome;
- documento formatado;
- data de referência com rótulo dinâmico;
- e-mail;
- telefone;
- endereço;
- observações;
- situação;
- criação;
- atualização;
- ações permitidas.

Regras:

- somente proprietário ou administrador;
- sem dados de outro usuário;
- `Cache-Control: private, no-store`;
- campos vazios representados de forma clara;
- documento completo apenas por ser tela autenticada e autorizada;
- botão editar;
- botão ativar ou inativar;
- sem botão excluir.

---

## 38. Página de edição

Rota:

```text
GET|POST /clientes/<uuid:pk>/editar/
```

Requisitos:

- carregar dados atuais;
- utilizar o mesmo `ClienteForm`;
- excluir o próprio registro dos alertas;
- revalidar documento;
- atualizar `atualizado_por`;
- preservar `criado_por`;
- exibir situação atual;
- oferecer ação separada de ativar/inativar;
- mensagem de sucesso;
- redirecionar para detalhes.

Mensagem:

```text
Cliente atualizado com sucesso.
```

---

## 39. Ativação

Rota:

```text
POST /clientes/<uuid:pk>/ativar/
```

Regras:

- autenticação;
- ownership;
- CSRF;
- método `POST`;
- idempotência;
- atualizar `atualizado_por`;
- mensagem;
- redirect para detalhes.

Mensagem:

```text
Cliente ativado com sucesso.
```

---

## 40. Inativação

Rota:

```text
POST /clientes/<uuid:pk>/inativar/
```

Regras:

- autenticação;
- ownership;
- CSRF;
- método `POST`;
- idempotência;
- atualizar `atualizado_por`;
- mensagem;
- redirect para detalhes;
- não excluir.

Mensagem:

```text
Cliente inativado com sucesso.
```

---

## 41. Templates

Estrutura esperada:

```text
backend/clientes/templates/clientes/
├── cliente_list.html
├── cliente_form.html
├── cliente_detail.html
└── partials/
    ├── duplicate_warnings.html
    ├── form_errors.html
    └── status_actions.html
```

Poderão existir nomes equivalentes desde que claros.

Os templates deverão:

- herdar do layout interno;
- usar `{% csrf_token %}`;
- escapar conteúdo automaticamente;
- não usar `safe` em dados de clientes;
- não incluir segredos;
- não imprimir objetos completos para debug;
- ser responsivos;
- ser acessíveis;
- não depender apenas de cor;
- associar labels e inputs;
- exibir erros de forma objetiva.

---

## 42. URLs e namespaces

Criar namespace:

```python
app_name = "clientes"
```

Nomes recomendados:

```text
clientes:list
clientes:create
clientes:detail
clientes:update
clientes:activate
clientes:deactivate
```

Incluir em `config/urls.py`:

```text
path("clientes/", include("clientes.urls"))
```

Evitar nomes ambíguos.

---

## 43. Views

Podem ser implementadas com function-based views ou class-based views.

Critérios:

- manter código pequeno;
- reutilizar helpers;
- não colocar validação complexa diretamente na view;
- aplicar ownership no queryset;
- usar POST para mutações;
- usar PRG: Post/Redirect/Get;
- utilizar Django messages;
- não retornar stack traces;
- não registrar PII.

Estrutura recomendada:

```text
views.py
→ coordenação HTTP

forms.py
→ validação de entrada

services.py
→ duplicidade e operações coordenadas

models.py
→ invariantes persistentes

permissions.py
→ escopo por usuário
```

---

## 44. Mensagens do sistema

Sucesso:

```text
Cliente cadastrado com sucesso.
Cliente atualizado com sucesso.
Cliente ativado com sucesso.
Cliente inativado com sucesso.
```

Erro genérico:

```text
Não foi possível concluir a operação. Revise os campos informados.
```

Documento:

```text
Este CPF já está cadastrado.
Este CNPJ já está cadastrado.
```

Duplicidade não bloqueante:

```text
Este telefone já está associado a outro cliente. Deseja continuar?
Este e-mail já está associado a outro cliente. Deseja continuar?
```

Não exibir mensagens técnicas de banco.

---

## 45. Segurança dos dados pessoais

1. não registrar CPF ou CNPJ completos em logs;
2. não registrar telefone;
3. não registrar e-mail;
4. não registrar observações;
5. não registrar corpo completo de POST;
6. mascarar documento na lista;
7. usar no-store em páginas sensíveis;
8. impedir acesso cruzado;
9. não aceitar ownership do navegador;
10. não retornar dados de outro usuário em alertas;
11. não expor URLs internas do Supabase;
12. não expor chaves;
13. usar dados fictícios em testes.

---

## 46. Testes das migrations

Cobrir:

1. todas as migrations carregam em banco isolado;
2. banco de teste é criado;
3. `usuarios.Usuario` existe;
4. `clientes.Cliente` existe;
5. `ProtectedFile` existe;
6. constraints de Cliente funcionam;
7. índices esperados existem quando verificável;
8. migrations não possuem alterações pendentes;
9. `showmigrations --plan` é coerente;
10. conexão PostgreSQL real funciona antes da aplicação.

A aplicação remota será comprovada por comandos e smoke tests, não pela suíte local.

---

## 47. Testes de autenticação

Cobrir:

1. login válido por e-mail;
2. login inválido;
3. mensagem genérica;
4. usuário inativo bloqueado;
5. `next` interno respeitado;
6. `next` externo rejeitado;
7. login autenticado redireciona;
8. logout por POST;
9. logout por GET rejeitado;
10. sessão encerrada;
11. página de clientes exige login;
12. cookie e CSRF preservados;
13. usuário comum sem acesso ao Admin;
14. administrador com acesso.

---

## 48. Testes de listagem e ownership

Cobrir:

1. usuário vê próprios clientes;
2. usuário não vê clientes de outro;
3. administrador vê todos;
4. documento aparece mascarado;
5. lista exige login;
6. ordenação por nome;
7. cliente inativo continua listado com situação;
8. acesso cruzado por UUID retorna 404.

---

## 49. Testes de cadastro

Cobrir:

1. cadastro PF válido;
2. cadastro PJ válido;
3. atalho `?tipo=PF`;
4. atalho `?tipo=PJ`;
5. tipo inválido ignorado ou rejeitado com segurança;
6. autoria definida pelo backend;
7. situação inicial ativa;
8. documento duplicado bloqueado;
9. erro preserva dados;
10. sucesso redireciona;
11. usuário não envia `criado_por`;
12. campos privilegiados ignorados;
13. tentativa sem login redirecionada.

---

## 50. Testes de alertas

Cobrir:

1. telefone repetido exibe alerta;
2. e-mail repetido exibe alerta;
3. sem confirmação não salva;
4. com confirmação salva;
5. segundo POST recalcula alertas;
6. alteração dos dados invalida confirmação anterior;
7. edição exclui o próprio registro;
8. usuário comum não recebe dados de terceiros;
9. administrador usa escopo global;
10. dois alertas aparecem simultaneamente;
11. valores vazios não alertam.

---

## 51. Testes de detalhes e edição

Cobrir:

1. proprietário acessa detalhes;
2. outro usuário recebe 404;
3. administrador acessa;
4. proprietário edita;
5. outro usuário não edita;
6. `criado_por` permanece;
7. `atualizado_por` muda;
8. documento continua validado;
9. atualização redireciona;
10. resposta sensível usa `no-store`.

---

## 52. Testes de ativação e inativação

Cobrir:

1. proprietário inativa;
2. proprietário ativa;
3. ações são POST-only;
4. CSRF é exigido;
5. outro usuário recebe 404;
6. administrador pode executar;
7. operações são idempotentes;
8. `atualizado_por` é registrado;
9. nenhuma exclusão ocorre;
10. mensagens são exibidas.

---

## 53. Testes de regressão

A implementação não poderá quebrar:

- modelo customizado;
- login existente;
- logout existente;
- perfil;
- troca de senha;
- Admin de usuários;
- Admin de clientes;
- `ProtectedFile`;
- Storage privado;
- segurança de secrets;
- normalizadores;
- validadores;
- constraints;
- testes de `config`;
- testes de `core`;
- testes de `usuarios`;
- testes anteriores de `clientes`.

---

## 54. Ordem obrigatória de implementação

### 54.1 Auditoria

1. ler documentação;
2. revisar repositório;
3. revisar migrations;
4. revisar settings;
5. revisar autenticação;
6. revisar modelo Cliente;
7. executar baseline de testes;
8. confirmar ambiente Supabase.

### 54.2 Validação de migrations

1. executar check;
2. executar dry-run;
3. revisar migration por migration;
4. executar testes;
5. revisar plano;
6. validar conexão PostgreSQL.

### 54.3 Aplicação no Supabase

1. confirmar backup ou banco vazio;
2. executar `migrate --plan`;
3. executar `migrate`;
4. verificar migrations;
5. executar smoke tests;
6. registrar resultados.

### 54.4 Superusuário

1. verificar contas existentes;
2. criar superusuário interativamente;
3. testar Admin;
4. testar logout;
5. não registrar senha.

### 54.5 Integração da autenticação

1. revisar redirecionamentos;
2. definir destino temporário;
3. proteger rotas;
4. validar ownership;
5. aplicar headers de cache;
6. testar sessão e CSRF.

### 54.6 Cadastro de clientes

1. criar form;
2. criar lista;
3. criar cadastro;
4. criar detalhes;
5. criar edição;
6. criar ativação;
7. criar inativação;
8. integrar alertas;
9. criar templates;
10. criar JavaScript mínimo;
11. criar testes.

### 54.7 Validação final

1. executar `check`;
2. executar dry-run;
3. executar suíte específica;
4. executar suíte completa;
5. revisar diff;
6. verificar segredos;
7. verificar PII;
8. atualizar README;
9. criar relatório.

---

## 55. Comandos de validação

Antes do banco remoto:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py showmigrations --plan
python backend/manage.py migrate --plan
python backend/manage.py test
```

Conexão:

```powershell
python backend/manage.py shell -c "from django.db import connection; connection.ensure_connection(); print(connection.vendor); print(connection.is_usable())"
```

Aplicação controlada:

```powershell
python backend/manage.py migrate
```

Depois:

```powershell
python backend/manage.py showmigrations
python backend/manage.py check
```

Superusuário:

```powershell
python backend/manage.py createsuperuser --email EMAIL_DO_ADMINISTRADOR
```

Nenhum comando deverá conter senha.

---

## 56. Documentação e relatório

Atualizar:

- `README.md`;
- `backend/README.md`;
- árvore de rotas;
- estado das migrations;
- destino temporário após login;
- fluxo de cadastro;
- regras de ownership;
- regras de duplicidade;
- limitações da etapa.

Criar:

```text
migrations_auth_clientes_implementation_report.md
```

O relatório deverá ser escrito em português e conter:

1. ambiente utilizado;
2. migrations revisadas;
3. banco isolado;
4. resultado dos testes;
5. resultado da conexão;
6. resultado do `migrate`;
7. migrations aplicadas;
8. superusuário criado, sem e-mail completo quando não necessário e sem senha;
9. rotas implementadas;
10. templates;
11. regras de acesso;
12. fluxo de duplicidade;
13. arquivos alterados;
14. riscos;
15. bloqueadores;
16. próximos passos.

---

## 57. Critérios de aceite — Migrations

A parte de banco será concluída quando:

1. migrations estiverem versionadas;
2. revisão manual estiver registrada;
3. dry-run não indicar mudanças;
4. suíte completa passar;
5. conexão PostgreSQL retornar utilizável;
6. ambiente for confirmado como desenvolvimento;
7. backup ou estado vazio for confirmado;
8. `migrate` concluir sem erro;
9. `showmigrations` marcar todas as esperadas;
10. tabelas e constraints estiverem disponíveis;
11. nenhum SQL manual tiver sido necessário;
12. nenhum segredo tiver sido exposto.

---

## 58. Critérios de aceite — Autenticação

A parte de autenticação será concluída quando:

1. login por e-mail funcionar;
2. logout por POST funcionar;
3. usuário inativo não autenticar;
4. `next` seguro funcionar;
5. redirect externo for bloqueado;
6. página interna exigir login;
7. usuário comum não acessar Admin;
8. administrador acessar Admin;
9. sessões e CSRF permanecerem ativos;
10. páginas sensíveis usarem `no-store`;
11. todas as rotas de clientes estiverem protegidas.

---

## 59. Critérios de aceite — Cadastro

A parte de cadastro será concluída quando:

1. lista simples existir;
2. formulário único PF/PJ existir;
3. cadastro PF funcionar;
4. cadastro PJ funcionar;
5. rótulos dinâmicos funcionarem;
6. máscaras de interface funcionarem;
7. backend funcionar sem JavaScript;
8. documento duplicado bloquear;
9. telefone repetido alertar;
10. e-mail repetido alertar;
11. confirmação explícita permitir continuar;
12. criação registrar autoria;
13. detalhes respeitarem ownership;
14. edição respeitar ownership;
15. atualização registrar autoria;
16. ativação funcionar;
17. inativação funcionar;
18. nenhuma exclusão existir;
19. usuário comum acessar somente próprios dados;
20. administrador acessar todos;
21. acesso cruzado retornar 404;
22. mensagens forem claras;
23. templates forem responsivos e acessíveis;
24. testes passarem;
25. nenhum dado pessoal for registrado em logs.

---

## 60. Itens fora do escopo

Não implementar nesta etapa:

- cadastro público de usuários;
- recuperação de senha por e-mail;
- Supabase Auth;
- OAuth;
- login social;
- MFA;
- pesquisa avançada;
- filtros avançados;
- dashboard;
- relatórios;
- exportações;
- integração automática de CEP;
- similaridade de nomes;
- exclusão física de clientes;
- upload de arquivos;
- vínculo de arquivos com Cliente;
- app `arquivos`;
- movimentação de `ProtectedFile`;
- API pública;
- React;
- Next.js;
- Realtime;
- deploy de produção.

---

## 61. Próxima etapa

Após a conclusão, a próxima fase recomendada será:

```text
Fase 2.7 — Pesquisa e filtros de clientes
```

Ela deverá incluir:

- pesquisa geral;
- nome;
- CPF/CNPJ;
- telefone;
- e-mail;
- cidade;
- estado;
- tipo;
- situação;
- paginação integrada;
- preservação de filtros;
- escopo por usuário;
- privacidade dos resultados.

---

## 62. Conclusão

A etapa será executada em três blocos sequenciais:

```text
Migrations e Supabase
        ↓
Autenticação integrada e páginas protegidas
        ↓
Cadastro e gestão inicial de clientes
```

Ao final, o projeto deverá possuir banco PostgreSQL migrado de forma controlada, primeiro administrador criado, autenticação integrada ao domínio e fluxo funcional de cadastro PF/PJ, detalhes, edição, ativação e inativação, sempre com isolamento por usuário e proteção dos dados pessoais.
