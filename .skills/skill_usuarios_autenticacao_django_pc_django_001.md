---
name: usuario-autenticacao-django
description: Implementa e valida o modelo de usuário customizado, autenticação por e-mail, sessões Django, administração, permissões e isolamento de dados do projeto PC-DJANGO-001.
---

# Skill — Usuários e Autenticação Django
## Projeto PC-DJANGO-001

## 1. Finalidade

Esta skill orienta agentes de desenvolvimento na implementação da Fase 2.1 do projeto PC-DJANGO-001: criação do modelo de usuário customizado, autenticação por e-mail e senha, sessões Django, administração de usuários, edição de perfil, controle de acesso e isolamento de dados por proprietário.

A especificação funcional e técnica aprovada é a fonte principal para esta etapa.

## 2. Quando usar

Use esta skill quando a tarefa envolver qualquer um destes itens:

- criação da app `usuarios`;
- definição de `AUTH_USER_MODEL`;
- modelo customizado baseado em `AbstractUser`;
- login por e-mail;
- logout;
- sessões Django;
- edição de perfil;
- alteração ou redefinição de senha;
- Django Admin para usuários;
- ativação ou desativação de contas;
- permissões entre administrador e usuário comum;
- isolamento de clientes, arquivos, relatórios ou dashboards por usuário;
- testes de autenticação e autorização;
- migrations relacionadas ao modelo de usuário.

## 3. Fontes de verdade

Antes de alterar código, leia nesta ordem:

1. `AGENTS.md`;
2. `README.md`;
3. `Blueprint/`;
4. arquivo de especificação da etapa de usuários e autenticação;
5. migrations já existentes;
6. estado atual do Git;
7. implementação atual de segurança e Storage privado.

Em caso de conflito, prevalece:

```text
Especificação aprovada da etapa
→ AGENTS.md
→ Blueprint
→ README.md
→ código atual
```

Não assuma que a estrutura documentada já existe. Verifique o repositório real.

## 4. Decisões obrigatórias

A implementação deve respeitar estas decisões:

1. Usar Django Auth como autenticação principal.
2. Não usar Supabase Auth nesta etapa.
3. Usar e-mail e senha no login.
4. Tornar e-mail obrigatório e único.
5. Remover o campo `username`.
6. Criar contas individuais.
7. Proibir compartilhamento de contas.
8. Permitir criação de usuários somente pelo administrador.
9. Não criar cadastro público.
10. Não implementar login social.
11. Não implementar recuperação automática de senha por e-mail.
12. Não implementar MFA.
13. Usar sessões Django.
14. Manter tokens fora de `localStorage`.
15. Manter segredos Supabase somente no backend.
16. Permitir que usuários comuns acessem apenas os próprios dados.
17. Permitir que administradores acessem todos os dados.
18. Preferir desativação por `is_active=False`.
19. Tratar exclusão física como operação excepcional.
20. Preservar vínculo entre usuário e arquivos privados.

## 5. Modelo esperado

Criar a app:

```text
usuarios
```

Criar o modelo:

```text
usuarios.Usuario
```

Base:

```python
AbstractUser
```

Configuração obrigatória:

```python
AUTH_USER_MODEL = "usuarios.Usuario"
```

Configuração do login:

```python
username = None
email = models.EmailField(unique=True)
USERNAME_FIELD = "email"
REQUIRED_FIELDS = []
```

A chave primária deve ser UUID.

## 6. Campos esperados

### 6.1 Acesso e controle

- `id`;
- `email`;
- `password`;
- `is_active`;
- `is_staff`;
- `is_superuser`;
- `last_login`;
- `date_joined`.

### 6.2 Perfil

- `nome_completo`;
- `telefone`;
- `cpf`;
- `cargo`;
- `foto`;
- `empresa`;
- `setor`;
- `observacoes`.

Campos opcionais devem usar `blank=True` quando apropriado.

CPF, quando preenchido:

- deve conter apenas números;
- deve ser validado;
- deve ser único;
- não deve ser usado como identificador de login.

## 7. Manager customizado

Criar manager compatível com autenticação por e-mail.

Métodos mínimos:

```python
create_user(email, password=None, **extra_fields)
create_superuser(email, password=None, **extra_fields)
```

Regras:

- exigir e-mail;
- normalizar e-mail;
- usar `set_password()`;
- configurar corretamente `is_staff`;
- configurar corretamente `is_superuser`;
- rejeitar superusuário inválido;
- nunca armazenar senha em texto puro.

## 8. Perfis de acesso

### 8.1 Administrador

Esperado:

```text
is_superuser=True
is_staff=True
is_active=True
```

Pode:

- acessar Django Admin;
- criar, editar, desativar e redefinir senha de usuários;
- acessar todos os dados;
- administrar permissões;
- excluir usuários quando seguro;
- acessar todos os arquivos privados.

### 8.2 Usuário comum

Esperado:

```text
is_superuser=False
is_staff=False
is_active=True
```

Pode:

- fazer login;
- editar o próprio perfil;
- alterar a própria senha, quando implementado;
- cadastrar e consultar os próprios clientes;
- acessar apenas os próprios relatórios, dashboards e arquivos.

Não pode:

- acessar Django Admin;
- criar usuários;
- editar outros usuários;
- elevar permissões;
- acessar dados de terceiros.

## 9. Autorização e isolamento

Toda consulta de domínio deve considerar o usuário autenticado.

Exemplo:

```python
Cliente.objects.filter(criado_por=request.user)
```

Relações de autoria devem usar:

```python
settings.AUTH_USER_MODEL
```

Evite importação direta do modelo `Usuario`.

Para relações históricas importantes, prefira:

```python
on_delete=models.PROTECT
```

quando a exclusão do usuário não puder apagar rastreabilidade.

O administrador pode ignorar o filtro apenas por permissão explícita.

## 10. Arquivos privados

O fluxo obrigatório é:

```text
arquivo_id
→ consulta ORM
→ verificação de proprietário ou administrador
→ obtenção interna de storage_path
→ geração de URL assinada
```

Nunca aceite `storage_path` fornecido pelo navegador como fonte confiável.

A chave secreta do Supabase nunca deve aparecer em:

- respostas;
- templates;
- JavaScript;
- logs;
- headers retornados;
- mensagens de erro;
- testes exibidos ao usuário.

## 11. Django Admin

Registrar o modelo customizado no admin.

O admin deve permitir:

- criação de usuário;
- alteração de usuário;
- busca por e-mail e nome;
- filtros por ativo, staff e superusuário;
- redefinição de senha;
- edição de campos de perfil;
- ativação e desativação.

O formulário de criação deve solicitar senha corretamente e usar hashing.

Não exibir segredos de ambiente ou credenciais externas.

## 12. Autenticação

Implementar:

- login por e-mail e senha;
- logout;
- proteção de rotas internas;
- redirecionamento coerente;
- sessão Django;
- mensagens genéricas em falha de login;
- bloqueio de usuário inativo.

Requisitos de segurança:

- cookie `HttpOnly`;
- cookie `Secure` em produção;
- `SameSite=Lax` ou equivalente;
- proteção CSRF;
- ausência de tokens em `localStorage`;
- ausência de credenciais Supabase no navegador.

## 13. Senhas

Nesta etapa:

- não implementar recuperação por e-mail;
- permitir redefinição administrativa pelo Django Admin;
- opcionalmente permitir alteração da própria senha com confirmação da senha atual;
- nunca permitir leitura da senha existente;
- nunca registrar senha em logs;
- nunca retornar detalhes de validação sensíveis.

## 14. Desativação e exclusão

Fluxo padrão:

```python
is_active = False
```

Usuários inativos não podem autenticar.

Exclusão física:

- somente administrador;
- excepcional;
- revisar dependências;
- bloquear se houver dados que precisem ser preservados;
- considerar transferência de propriedade antes de excluir.

## 15. Ordem de implementação

Execute nesta sequência:

1. inspecionar Git e migrations;
2. confirmar que ainda é seguro alterar `AUTH_USER_MODEL`;
3. criar app `usuarios`;
4. criar manager;
5. criar modelo;
6. configurar `AUTH_USER_MODEL`;
7. registrar admin;
8. criar formulários;
9. criar login e logout;
10. criar edição de perfil;
11. aplicar permissões;
12. gerar migrations;
13. revisar migrations;
14. testar em banco isolado;
15. executar checks;
16. atualizar documentação;
17. somente depois avaliar aplicação no Supabase.

## 16. Regras para migrations

Antes de gerar migrations:

- verificar migrations existentes;
- verificar se tabelas padrão de auth já foram aplicadas no Supabase;
- não apagar migrations sem justificativa;
- não executar `migrate` em banco remoto automaticamente;
- documentar qualquer incompatibilidade;
- interromper se a troca de usuário puder corromper o histórico.

Comandos seguros esperados:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py test usuarios
```

Gere migration somente após validar a estratégia.

## 17. Testes obrigatórios

Cobrir no mínimo:

1. criação de usuário comum;
2. criação de superusuário;
3. e-mail obrigatório;
4. e-mail único;
5. normalização de e-mail;
6. senha com hash;
7. login por e-mail;
8. falha de login inválido;
9. usuário inativo bloqueado;
10. administrador acessa admin;
11. usuário comum não acessa admin;
12. usuário edita o próprio perfil;
13. usuário não edita outro perfil;
14. usuário comum não altera flags privilegiadas;
15. redefinição administrativa de senha;
16. isolamento de dados;
17. autorização de arquivos privados;
18. ausência de segredos em respostas;
19. ausência de senhas e tokens em logs;
20. migrations sem alterações pendentes.

## 18. Critérios de aceite

Considere a etapa pronta somente quando:

- `usuarios.Usuario` estiver implementado;
- `AUTH_USER_MODEL` estiver configurado;
- login por e-mail funcionar;
- `username` não existir;
- e-mail for obrigatório e único;
- manager customizado funcionar;
- superusuário puder ser criado;
- usuário inativo não autenticar;
- admin funcionar;
- isolamento por usuário estiver testado;
- testes passarem;
- `manage.py check` passar;
- migrations estiverem revisadas;
- documentação estiver atualizada;
- nenhum segredo estiver exposto.

## 19. Fora do escopo

Não implementar:

- Supabase Auth;
- OAuth;
- login social;
- cadastro público;
- convite automático;
- recuperação automática por e-mail;
- MFA;
- multiempresa;
- perfis intermediários;
- Realtime;
- compartilhamento de contas;
- alterações completas do módulo de clientes;
- deploy.

## 20. Restrições do agente

O agente deve:

- trabalhar com mudanças mínimas;
- preservar segurança existente;
- não expor `.env`;
- não imprimir segredos;
- não fazer commit;
- não fazer push;
- não executar operações destrutivas;
- não aplicar migration remota sem autorização;
- registrar bloqueadores de forma objetiva;
- distinguir fatos verificados de recomendações.

## 21. Saída esperada

Ao concluir uma tarefa baseada nesta skill, apresentar:

1. arquivos alterados;
2. decisões aplicadas;
3. migrations criadas;
4. testes executados;
5. resultados dos checks;
6. riscos restantes;
7. bloqueadores;
8. próxima subetapa;
9. veredito:
   - `READY`;
   - `READY WITH RESERVATIONS`;
   - `NOT READY`.
