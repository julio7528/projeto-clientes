# Relatorio de Implementacao de Usuarios e Autenticacao

## Arquitetura

O Django e a unica fonte de identidade e sessao. O fluxo e `Browser -> Django Session -> Django ORM -> PostgreSQL Supabase`. Nao existe Supabase Auth, signup publico, OAuth, recuperacao por e-mail, MFA ou credencial privilegiada no browser.

`usuarios.Usuario` herda de `AbstractUser`, usa UUID, remove `username` e autentica por e-mail unico normalizado. Administradores sao exclusivamente usuarios ativos com `is_staff` e `is_superuser`; usuarios comuns operam dados proprios.

## Subetapas Implementadas

1. App `usuarios` criada e registrada.
2. `UsuarioManager` com criacao segura de usuario e superusuario.
3. Modelo customizado com campos aprovados, CPF validado e referencia backend-only de foto.
4. `AUTH_USER_MODEL = usuarios.Usuario` configurado.
5. Admin customizado com criacao, edicao, busca, filtros, ativacao, desativacao e reset nativo de senha.
6. Login por e-mail, logout POST, perfil, edicao e troca da propria senha com sessao e CSRF.
7. Usuarios comuns sem Admin, criacao de contas, edicao cruzada ou alteracao de flags privilegiadas.
8. Helpers reutilizaveis de ownership com bypass administrativo explicito.
9. Storage privado compativel com o usuario customizado e `owner` protegido contra exclusao.
10. Migrations geradas e revisadas sem aplicacao remota.
11. Testes de modelo, autenticacao, autorizacao, Admin, Storage, segredos e logging.
12. Documentacao atualizada.

## Arquivos

- `config/models.py`, `config/settings.py`, `config/urls.py`, `config/views.py`, `config/tests.py`
- `config/migrations/0002_alter_protectedfile_owner.py`
- `usuarios/apps.py`, `usuarios/managers.py`, `usuarios/models.py`, `usuarios/validators.py`
- `usuarios/forms.py`, `usuarios/admin.py`, `usuarios/permissions.py`, `usuarios/views.py`, `usuarios/urls.py`
- `usuarios/templates/usuarios/*.html`, `usuarios/tests.py`
- `usuarios/migrations/0001_initial.py`
- `README.md`, `usuarios_implementation_report.md`

## Estrategia de Migration

A consulta somente leitura `showmigrations --plan` confirmou que o PostgreSQL Supabase nao possui migrations aplicadas. Portanto, a definicao do custom user ainda e segura para o ambiente alvo.

O `db.sqlite3` local ignorado possui 18 migrations nativas aplicadas com o usuario padrao. Ele e descartavel, mas incompativel com a troca; nao foi alterado. Deve ser reconstruido de forma controlada antes de migrations locais. Os testes e `makemigrations` usam SQLite em memoria.

Migrations novas:

- `usuarios/0001_initial.py`: cria `Usuario` antes das dependencias swappable.
- `config/0002_alter_protectedfile_owner.py`: altera ownership de `CASCADE` para `PROTECT`.

Nenhuma migration foi aplicada ao Supabase.

## Comandos e Resultados

- `python manage.py showmigrations --plan`: remoto acessivel; todas as migrations marcadas como nao aplicadas.
- `python backend/manage.py check`: `System check identified no issues (0 silenced).`
- `python backend/manage.py makemigrations --check --dry-run`: `No changes detected`.
- `python backend/manage.py test usuarios config`: 35 testes, `OK`, banco de teste criado e destruido.

## Controles de Seguranca

- E-mail normalizado, senha via `set_password()` e usuario inativo bloqueado.
- Mensagem generica de login e nenhum password, token ou segredo em respostas/logs.
- Forms de perfil usam allowlist e excluem flags de acesso, e-mail, foto e observacoes administrativas.
- Logout somente POST com CSRF; paginas internas usam `login_required`.
- Admin exige simultaneamente staff e superuser.
- Storage aceita UUID interno, aplica ownership ou acesso administrativo e nunca confia em path do browser.
- Segredos Supabase permanecem na camada backend existente.

## Riscos e Proximos Passos

- Reconstruir o SQLite local antigo antes de desenvolvimento com migrations.
- Revisar backup e aplicar todas as migrations em ordem no Supabase apenas em janela controlada.
- Criar o primeiro superusuario por canal administrativo seguro depois da migration.
- Adicionar rate limiting ao login na camada de deploy ou middleware escolhido.
- Revisar politica de upload/foto quando a funcionalidade de imagem for implementada.
- Aplicar `scope_owned_queryset()` a Cliente, dashboard, pesquisa, relatorios e exportacoes nas proximas fases.
