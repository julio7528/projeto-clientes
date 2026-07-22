# Especificação Técnica — Modelo de Usuário e Autenticação
## Projeto PC-DJANGO-001

## 1. Identificação da etapa

**Etapa principal:** Fase 2 — Usuários, autenticação e autorização  
**Subetapa:** 2.1 — Definição do modelo de usuário customizado  
**Status:** Especificação aprovada para implementação futura  
**Escopo deste documento:** definir o comportamento, os campos, as regras de acesso e os critérios técnicos do modelo de usuário antes da criação das migrations definitivas do domínio.

---

## 2. Objetivo

Definir uma arquitetura de autenticação baseada no Django, com login por e-mail e senha, contas individuais, administração centralizada e isolamento de dados por usuário.

O Supabase continuará sendo utilizado como infraestrutura de PostgreSQL e Storage, mas não será utilizado como provedor principal de autenticação nesta etapa.

Fluxo definido:

```text
Navegador
   ↓
Sessão segura do Django
   ↓
Modelo de usuário customizado
   ↓
Permissões e isolamento de dados
   ↓
Django ORM
   ↓
PostgreSQL no Supabase
```

---

## 3. Decisões arquiteturais aprovadas

1. A autenticação principal será feita pelo Django.
2. O login utilizará exclusivamente e-mail e senha.
3. O e-mail será obrigatório e único.
4. O campo `username` padrão do Django será removido.
5. Cada pessoa terá sua própria conta.
6. Não será permitido compartilhamento de contas.
7. Não haverá cadastro público de usuários.
8. Apenas o administrador poderá criar usuários.
9. Não haverá login social no MVP.
10. Não haverá Supabase Auth no MVP.
11. Não haverá recuperação automática de senha por e-mail.
12. O administrador poderá redefinir senhas pelo Django Admin.
13. Não haverá autenticação de dois fatores nesta fase.
14. Usuários poderão editar o próprio perfil.
15. Usuários comuns não poderão criar outros usuários.
16. Usuários comuns verão apenas os próprios dados.
17. O administrador terá acesso total ao sistema.
18. Usuários poderão ser desativados sem exclusão física.
19. A exclusão física será excepcional e restrita ao administrador.
20. Arquivos privados permanecerão vinculados ao usuário proprietário.

---

## 4. Tipos de usuário

### 4.1 Administrador

O administrador será uma conta individual e intransferível.

Configuração esperada:

```text
is_superuser = True
is_staff = True
is_active = True
```

Permissões:

- acessar o Django Admin;
- criar usuários;
- editar usuários;
- desativar usuários;
- redefinir senhas;
- excluir usuários quando permitido;
- acessar todos os clientes;
- acessar todos os relatórios;
- acessar todos os arquivos privados;
- editar ou corrigir dados cadastrados;
- administrar permissões;
- executar operações administrativas do sistema.

### 4.2 Usuário comum

Configuração esperada:

```text
is_superuser = False
is_staff = False
is_active = True
```

Permissões:

- fazer login com e-mail e senha;
- editar o próprio perfil;
- alterar a própria senha, caso essa função seja disponibilizada;
- cadastrar clientes;
- editar clientes próprios;
- pesquisar clientes próprios;
- visualizar dashboard com dados próprios;
- emitir relatórios dos próprios dados;
- acessar arquivos privados próprios ou vinculados aos seus clientes;
- encerrar a própria sessão.

Restrições:

- não acessar o Django Admin;
- não criar usuários;
- não editar outros usuários;
- não acessar clientes de outros usuários;
- não acessar relatórios de outros usuários;
- não acessar arquivos de outros usuários;
- não elevar as próprias permissões.

---

## 5. Modelo de usuário

A aplicação Django deverá ser criada com o nome:

```text
usuarios
```

O modelo será:

```text
usuarios.Usuario
```

A classe deverá herdar de:

```python
django.contrib.auth.models.AbstractUser
```

Configuração obrigatória no Django:

```python
AUTH_USER_MODEL = "usuarios.Usuario"
```

Essa configuração deverá ser definida antes da aplicação das migrations definitivas do projeto.

---

## 6. Campos do modelo

### 6.1 Campos de autenticação e controle

| Campo | Tipo esperado | Obrigatório | Regra |
|---|---|---:|---|
| `id` | UUID | Sim | Chave primária |
| `email` | EmailField | Sim | Único e utilizado no login |
| `password` | Campo nativo Django | Sim | Armazenado somente como hash |
| `is_active` | BooleanField | Sim | Controla acesso sem exclusão |
| `is_staff` | BooleanField | Sim | Controla acesso ao Django Admin |
| `is_superuser` | BooleanField | Sim | Concede permissões administrativas totais |
| `last_login` | Campo nativo Django | Não | Atualizado pelo sistema |
| `date_joined` | DateTimeField | Sim | Data de criação da conta |

### 6.2 Campos de perfil

| Campo | Tipo esperado | Obrigatório | Observação |
|---|---|---:|---|
| `nome_completo` | CharField | Sim | Nome civil ou nome completo informado |
| `telefone` | CharField | Não | Armazenado normalizado quando possível |
| `cpf` | CharField | Não | Apenas números; único quando preenchido |
| `cargo` | CharField | Não | Cargo ou função |
| `foto` | ImageField ou referência de Storage | Não | Deve seguir arquitetura backend-only |
| `empresa` | CharField | Não | Informação descritiva; não representa multiempresa |
| `setor` | CharField | Não | Setor do usuário |
| `observacoes` | TextField | Não | Anotações administrativas |

### 6.3 Campos removidos

O campo padrão:

```python
username
```

deverá ser removido.

Configuração esperada:

```python
username = None
USERNAME_FIELD = "email"
REQUIRED_FIELDS = []
```

---

## 7. Regras de validação

1. O e-mail deve ser obrigatório.
2. O e-mail deve ser único, sem diferenciação indevida por letras maiúsculas e minúsculas.
3. O e-mail deve ser normalizado antes da persistência.
4. O CPF, quando informado, deve conter apenas números.
5. O CPF, quando informado, deve ser validado.
6. O CPF, quando informado, deve ser único.
7. Senhas nunca poderão ser armazenadas em texto puro.
8. A criação de usuários deve utilizar `set_password()` ou managers compatíveis.
9. Usuários inativos não poderão autenticar.
10. Usuários comuns não poderão alterar `is_staff`, `is_superuser` ou `is_active`.
11. Somente administradores poderão redefinir senha de terceiros.
12. O administrador não deve visualizar a senha atual de nenhum usuário.
13. Mensagens de erro não devem revelar informações sensíveis.

---

## 8. Manager customizado

Deverá existir um manager compatível com autenticação por e-mail.

Responsabilidades:

- normalizar e-mail;
- exigir e-mail;
- criar usuário comum;
- criar superusuário;
- configurar corretamente `is_staff`;
- configurar corretamente `is_superuser`;
- usar `set_password()`.

Métodos mínimos:

```python
create_user(email, password=None, **extra_fields)
create_superuser(email, password=None, **extra_fields)
```

---

## 9. Django Admin

O modelo `Usuario` deverá ser registrado no Django Admin.

O admin deverá permitir:

- listar usuários;
- pesquisar por e-mail e nome;
- filtrar por status ativo, staff e superusuário;
- criar usuários;
- editar dados do perfil;
- ativar e desativar usuários;
- redefinir senha;
- visualizar datas de criação e último login.

Campos sensíveis não poderão ser exibidos:

- hash da senha;
- chaves Supabase;
- tokens;
- `DATABASE_URL`;
- segredos de ambiente.

A exclusão física deverá ser tratada como operação excepcional.

---

## 10. Autenticação e sessão

O sistema utilizará sessões do Django.

Requisitos:

- cookie de sessão `HttpOnly`;
- cookie `Secure` em produção;
- proteção CSRF;
- `SameSite=Lax` ou configuração equivalente;
- logout invalidando a sessão;
- ausência de tokens em `localStorage`;
- ausência de credenciais Supabase no navegador;
- ausência de senhas em logs ou respostas.

Fluxo de login:

```text
Usuário informa e-mail e senha
        ↓
Django valida credenciais
        ↓
Django cria sessão
        ↓
Cookie seguro é enviado ao navegador
        ↓
Rotas protegidas usam request.user
```

---

## 11. Cadastro de usuários

O cadastro será exclusivamente administrativo.

Fluxo:

```text
Administrador
   ↓
Django Admin
   ↓
Cria usuário
   ↓
Define e-mail e senha inicial
   ↓
Usuário recebe credenciais por canal externo
```

Não haverá:

- formulário público de cadastro;
- autoinscrição;
- convite automático;
- login por provedor externo;
- criação de usuários por usuários comuns.

---

## 12. Recuperação e redefinição de senha

Não haverá recuperação automática por e-mail nesta fase.

Fluxo aprovado:

```text
Usuário solicita redefinição ao administrador
        ↓
Administrador acessa Django Admin
        ↓
Administrador define nova senha
        ↓
Usuário acessa com a nova senha
```

O sistema poderá permitir que o usuário altere a própria senha mediante confirmação da senha atual.

---

## 13. Desativação e exclusão

### 13.1 Desativação

A operação padrão será:

```python
is_active = False
```

Efeitos:

- bloqueio de login;
- preservação do histórico;
- preservação de clientes;
- preservação de arquivos;
- preservação de auditoria.

### 13.2 Exclusão física

A exclusão física:

- será permitida somente ao administrador;
- deverá ser excepcional;
- deverá verificar dependências;
- poderá ser bloqueada caso existam dados relacionados;
- poderá exigir transferência prévia dos dados;
- não deverá ser usada como fluxo comum de desligamento.

Relacionamentos de autoria importantes deverão considerar:

```python
on_delete=models.PROTECT
```

quando a preservação histórica for necessária.

---

## 14. Isolamento de dados

A regra central será:

```text
cada usuário comum acessa somente os dados que lhe pertencem
```

Todos os modelos de domínio relevantes deverão possuir relação com o usuário.

Exemplo previsto para Cliente:

```python
criado_por = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name="clientes_criados",
)
```

Consultas de usuários comuns deverão ser filtradas:

```python
Cliente.objects.filter(criado_por=request.user)
```

O administrador poderá acessar todos os registros por permissão explícita.

Essa regra deverá ser aplicada a:

- clientes;
- arquivos;
- dashboard;
- pesquisa;
- relatórios;
- exportações;
- histórico;
- operações de edição.

---

## 15. Arquivos privados

O modelo atual `ProtectedFile` possui relação de proprietário.

A regra continuará sendo:

```text
ProtectedFile.owner == request.user
```

ou acesso administrativo explícito.

O navegador deverá enviar apenas identificadores internos, nunca caminhos de Storage.

Fluxo:

```text
arquivo_id
   ↓
Django consulta o arquivo
   ↓
Django verifica proprietário ou administrador
   ↓
Django obtém storage_path internamente
   ↓
Django solicita URL assinada ao Supabase
```

A `SUPABASE_SECRET_KEY` nunca poderá chegar ao navegador.

---

## 16. Supabase Auth

O Supabase Auth não será adotado nesta etapa.

Motivos:

- autenticação Django já atende ao escopo;
- o projeto quer explorar recursos nativos do Django;
- evita duplicação entre usuários Django e `auth.users`;
- evita sincronização de sessões, senhas e bloqueios;
- mantém uma única fonte de identidade;
- preserva a arquitetura backend-only.

O Supabase será utilizado para:

- PostgreSQL;
- Storage privado;
- infraestrutura backend-only;
- administração e backup conforme o plano.

---

## 17. Subetapas previstas para implementação

### 17.1 Preparação

1. revisar `AGENTS.md`;
2. revisar Blueprint;
3. verificar migrations já existentes;
4. confirmar que ainda é seguro definir `AUTH_USER_MODEL`;
5. criar backup ou ponto de restauração local;
6. confirmar que nenhuma migration definitiva de domínio foi aplicada indevidamente.

### 17.2 Criação da app

1. criar a app `usuarios`;
2. adicionar a app ao `INSTALLED_APPS`;
3. organizar `models.py`, `managers.py`, `admin.py`, `forms.py`, `urls.py`, `views.py` e `tests/`;
4. definir `AUTH_USER_MODEL`.

### 17.3 Implementação do modelo

1. criar UUID;
2. remover `username`;
3. tornar e-mail obrigatório e único;
4. adicionar campos de perfil;
5. criar manager customizado;
6. implementar validações;
7. registrar no admin.

### 17.4 Autenticação

1. criar login por e-mail e senha;
2. criar logout;
3. proteger rotas internas;
4. implementar sessão Django;
5. criar edição de perfil;
6. criar alteração de senha própria, caso incluída.

### 17.5 Permissões

1. diferenciar administrador e usuário comum;
2. bloquear acesso ao admin para usuários comuns;
3. impedir edição de campos privilegiados;
4. aplicar isolamento de dados;
5. testar acesso administrativo.

### 17.6 Migrations

1. gerar migrations;
2. revisar migrations;
3. validar dependências;
4. executar testes em banco isolado;
5. somente depois aplicar no Supabase de forma controlada.

### 17.7 Testes

1. criação de usuário;
2. criação de superusuário;
3. login por e-mail;
4. bloqueio de e-mail duplicado;
5. bloqueio de usuário inativo;
6. acesso ao Django Admin;
7. usuário comum sem acesso ao admin;
8. edição do próprio perfil;
9. proibição de edição de outro perfil;
10. redefinição administrativa de senha;
11. proteção de dados entre usuários;
12. ausência de segredos em respostas e logs.

---

## 18. Critérios de aceite

A subetapa será considerada concluída quando:

1. `usuarios.Usuario` existir e herdar de `AbstractUser`;
2. `username` estiver removido;
3. e-mail for obrigatório, único e usado no login;
4. `AUTH_USER_MODEL` estiver configurado;
5. manager customizado funcionar;
6. superusuário puder ser criado;
7. login por e-mail funcionar;
8. usuário inativo não autenticar;
9. administrador acessar o Django Admin;
10. usuário comum não acessar o Django Admin;
11. usuário puder editar o próprio perfil;
12. usuário não puder editar outro perfil;
13. senhas forem armazenadas somente como hash;
14. migrations forem revisadas;
15. testes passarem;
16. `python backend/manage.py check` não apresentar erros;
17. nenhuma credencial privilegiada aparecer no frontend;
18. documentação for atualizada.

---

## 19. Itens fora do escopo

Não fazem parte desta etapa:

- Supabase Auth;
- login social;
- OAuth;
- recuperação automática por e-mail;
- cadastro público;
- convite automático;
- autenticação em dois fatores;
- multiempresa;
- grupos intermediários;
- hierarquia de operador, gestor ou consulta;
- compartilhamento de conta;
- Realtime;
- alteração do domínio de clientes;
- implementação completa de relatórios;
- deploy em produção.

---

## 20. Conclusão

A decisão aprovada é criar um modelo de usuário customizado baseado em `AbstractUser`, com login exclusivo por e-mail, sessões Django, administração pelo Django Admin e isolamento dos dados por proprietário.

O administrador será representado pelas flags nativas `is_superuser` e `is_staff`. Usuários comuns terão contas individuais, poderão operar os próprios dados e não poderão acessar dados de terceiros.

Essa definição deverá ser implementada antes da expansão das migrations do domínio de clientes.
