---
name: estrutura-modular-apps-django
description: Cria e valida a estrutura modular das apps config, core, usuarios e clientes do projeto PC-DJANGO-001, preservando autenticação, segurança, migrations e limites de domínio.
---

# Skill — Estrutura Modular das Apps Django
## Projeto PC-DJANGO-001

## 1. Finalidade

Esta skill orienta agentes de desenvolvimento na implementação da Fase 2.2 do projeto PC-DJANGO-001: organização modular do backend Django por responsabilidades claras.

O objetivo é estruturar as apps:

```text
config
core
usuarios
clientes
```

sem implementar ainda o modelo definitivo de `Cliente` e sem mover `ProtectedFile`.

## 2. Quando usar

Use esta skill quando a tarefa envolver:

- criação da app `core`;
- criação da app `clientes`;
- revisão de `INSTALLED_APPS`;
- organização de módulos Django;
- separação entre configuração, infraestrutura e domínio;
- criação de modelos abstratos compartilhados;
- revisão de imports entre apps;
- definição de limites entre `config`, `core`, `usuarios` e `clientes`;
- preparação do projeto para o modelo `Cliente`;
- validação de migrations após reorganização;
- testes de carregamento e regressão das apps;
- documentação da arquitetura modular.

## 3. Fontes de verdade

Antes de alterar código, leia nesta ordem:

1. `AGENTS.md`;
2. `README.md`;
3. `Blueprint/00-overview/`;
4. `Blueprint/01-requisitos/`;
5. `Blueprint/02-modelagem/modelagem_dados_clientes_skill.md`;
6. especificação técnica da estrutura modular das apps;
7. relatório de implementação de usuários;
8. migrations existentes;
9. estado atual do Git;
10. código atual de `config` e `usuarios`.

Em caso de conflito:

```text
Especificação aprovada da etapa
→ AGENTS.md
→ Blueprint
→ README.md
→ código atual
```

Não invente decisões. Preserve a implementação atual quando houver dúvida relevante.

## 4. Estado atual esperado

Considere como baseline:

- Django configurado em `backend/`;
- `usuarios.Usuario` implementado;
- `AUTH_USER_MODEL` configurado;
- login por e-mail e sessões Django funcionando;
- `ProtectedFile` existente;
- integração backend-only com Supabase;
- testes de autenticação e segurança existentes;
- migrations anteriores preservadas;
- `core` ainda não estruturada;
- `clientes` ainda não estruturada.

Se o repositório não corresponder a esse estado, registre a divergência antes de modificar.

## 5. Decisões obrigatórias

A implementação deve respeitar:

1. `config` permanece responsável por configuração e infraestrutura.
2. `core` conterá apenas componentes realmente compartilhados.
3. `usuarios` continuará responsável por autenticação, perfil e permissões.
4. `clientes` concentrará o domínio de clientes PF e PJ.
5. PF e PJ usarão uma única entidade `Cliente`.
6. Não criar apps separadas para PF e PJ.
7. Não criar apps separadas para endereço ou contato.
8. Não criar app `arquivos` nesta etapa.
9. Não mover `ProtectedFile` nesta etapa.
10. Não renomear tabelas existentes por estética.
11. Não aplicar migrations no Supabase automaticamente.
12. Não introduzir novos frameworks.
13. Não reescrever a autenticação já implementada.
14. Não adicionar regras de clientes em `config`.
15. Não adicionar regras específicas de clientes em `core`.
16. Não adicionar regras de autenticação em `clientes`.
17. Relações com usuários devem usar `settings.AUTH_USER_MODEL`.
18. O isolamento de dados por usuário deve ser preservado.
19. Administradores só podem ignorar filtros de ownership por autorização explícita.
20. A estrutura deve permanecer simples e compatível com Django Templates.

## 6. Responsabilidade de `config`

Permitido em `config`:

- settings;
- ambiente;
- logging;
- ASGI;
- WSGI;
- URLs principais;
- integração com Supabase;
- endpoints técnicos;
- configuração de segurança;
- composição das URLs das apps.

Proibido em `config`:

- modelo `Cliente`;
- validadores de CPF e CNPJ de clientes;
- formulários de clientes;
- regras de pesquisa;
- regras de dashboard;
- relatórios;
- templates funcionais do domínio;
- autorização específica de clientes.

`ProtectedFile` deve permanecer temporariamente em `config`.

Não mover, duplicar, renomear tabela, apagar migrations, alterar `db_table` ou criar nova versão do modelo.

## 7. Responsabilidade de `core`

`core` deve conter apenas elementos reutilizáveis e independentes de domínio.

Permitido:

- modelos abstratos;
- UUID compartilhado;
- timestamps;
- normalização genérica de texto;
- normalização genérica de números;
- mixins reutilizáveis;
- exceções compartilhadas;
- permissões genéricas;
- utilitários comuns;
- bases de testes justificadas.

Proibido:

- CPF ou CNPJ de clientes;
- regras PF/PJ;
- formulários de clientes;
- login;
- criação de usuário;
- Storage;
- regras de `ProtectedFile`;
- relatórios;
- dashboard;
- código usado por uma única app;
- módulos genéricos sem responsabilidade clara.

## 8. Modelo abstrato permitido

Pode ser criado um modelo abstrato semelhante a:

```python
class UUIDTimestampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

Regras:

- não criar tabela;
- não gerar migration concreta;
- não incluir autoria automaticamente sem justificativa;
- usar apenas se houver benefício real para modelos futuros.

Não crie abstração de auditoria se ela não tiver reutilização concreta.

## 9. Responsabilidade de `usuarios`

Preservar:

- modelo `Usuario`;
- manager;
- login;
- logout;
- perfil;
- troca de senha;
- Django Admin;
- ativação e desativação;
- permissões;
- proteção contra edição cruzada.

Alterações permitidas apenas para corrigir imports, reutilizar abstração realmente genérica, manter compatibilidade com `clientes`, preservar relações com `settings.AUTH_USER_MODEL` ou melhorar organização sem mudar comportamento.

Helpers de ownership podem permanecer em `usuarios.permissions`.

Só mover para `core.permissions` se forem genéricos, usados por mais de uma app, independentes do domínio de usuários, cobertos por testes e funcionalmente equivalentes.

## 10. Responsabilidade de `clientes`

`clientes` será responsável por:

- entidade `Cliente`;
- PF e PJ;
- tipo;
- nome;
- documento;
- data de referência;
- e-mail;
- telefone;
- endereço;
- situação;
- observações;
- autoria;
- normalização;
- validações;
- formulários;
- criação;
- edição;
- detalhes;
- ativação;
- inativação;
- pesquisa;
- filtros;
- integração futura com dashboard;
- integração futura com relatórios;
- integração futura com arquivos.

Nesta etapa, a app será apenas estruturada.

Não implementar ainda modelo definitivo `Cliente`, CRUD completo, validação completa, integração com CEP, pesquisa, dashboard, relatórios, exportações, upload ou relação com arquivos.

## 11. Estrutura mínima de `core`

```text
core/
├── __init__.py
├── apps.py
├── models.py
├── normalizers.py
├── tests/
│   ├── __init__.py
│   └── test_models.py
└── migrations/
    └── __init__.py
```

Criar somente módulos que possuam uso real.

## 12. Estrutura mínima de `clientes`

```text
clientes/
├── __init__.py
├── admin.py
├── apps.py
├── choices.py
├── forms.py
├── models.py
├── permissions.py
├── services.py
├── urls.py
├── validators.py
├── views.py
├── tests/
│   ├── __init__.py
│   └── test_app_structure.py
└── migrations/
    └── __init__.py
```

Arquivos sem responsabilidade concreta podem ser adiados. Não criar placeholders que aparentem funcionalidade pronta.

## 13. Dependências permitidas

```text
config
→ configura apps e inclui URLs

usuarios
→ pode usar core

clientes
→ pode usar core
→ depende de settings.AUTH_USER_MODEL

config.ProtectedFile
→ depende de settings.AUTH_USER_MODEL
```

## 14. Dependências proibidas

```text
core → clientes
core → usuarios
core → config

usuarios → clientes

clientes → config para regras de domínio

clientes → usuarios.Usuario por import direto
```

Para relacionamentos:

```python
settings.AUTH_USER_MODEL
```

Para obter o usuário em runtime:

```python
get_user_model()
```

## 15. Regras para imports

1. Evitar ciclos.
2. Usar imports relativos dentro da mesma app.
3. Não importar views em models.
4. Não importar forms em models.
5. Não importar `config.settings`.
6. Usar `django.conf.settings`.
7. Usar strings em relacionamentos quando necessário.
8. Não importar diretamente `usuarios.Usuario` em models de domínio.
9. Não criar módulos genéricos apenas para contornar ciclos.
10. Manter contratos claros entre apps.

## 16. Escopo de implementação

### Deve fazer

1. auditar o estado atual;
2. criar `core`;
3. criar `clientes`;
4. definir `AppConfig`;
5. registrar apps quando necessário;
6. criar estrutura mínima;
7. criar abstrações justificadas;
8. adicionar testes mínimos;
9. preservar `usuarios`;
10. preservar `ProtectedFile`;
11. revisar imports;
12. executar checks;
13. validar migrations;
14. executar testes;
15. atualizar documentação;
16. criar relatório da etapa.

### Não deve fazer

- modelo completo de Cliente;
- CRUD;
- pesquisa;
- dashboard;
- relatórios;
- exportações;
- app `arquivos`;
- movimentação de `ProtectedFile`;
- upload;
- migrations remotas;
- frontend completo;
- mudanças visuais amplas;
- Supabase Auth;
- API pública;
- React;
- Next.js;
- deploy.

## 17. Migrations

### `core`

Se contiver apenas modelos abstratos:

- nenhuma tabela;
- nenhuma migration concreta;
- nenhum `CreateModel` concreto.

### `clientes`

Nesta etapa:

- não criar modelo `Cliente`;
- não criar tabela;
- manter apenas `migrations/__init__.py`.

### `usuarios`

- não reescrever migrations;
- não alterar migrations aplicadas;
- criar nova migration somente se estritamente necessário.

### `ProtectedFile`

- não mover;
- não renomear tabela;
- não duplicar;
- não apagar migrations;
- não alterar ownership sem necessidade.

### Banco remoto

Nunca executar automaticamente:

```powershell
python backend/manage.py migrate
```

contra o Supabase.

## 18. Estratégia futura para `arquivos`

Não criar `arquivos` agora.

Criar futuramente se arquivos pertencerem a vários domínios, houver ciclo de vida próprio, versionamento, múltiplos vínculos, permissões independentes ou regras próprias de upload.

Manter arquivos em `clientes` futuramente se todos forem exclusivamente de clientes, o ciclo de vida depender do cliente e a autorização decorrer sempre do cliente.

Até essa decisão:

```text
ProtectedFile permanece em config
```

## 19. Segurança

Preservar:

- login obrigatório;
- sessão Django;
- CSRF;
- cookies seguros;
- isolamento por usuário;
- acesso administrativo explícito;
- segredos fora do frontend;
- Supabase backend-only;
- URLs assinadas curtas;
- redaction de logs;
- `.env` ignorado;
- testes sem dados reais.

Nenhuma reorganização pode reduzir controles existentes.

## 20. Ordem de execução

### 20.1 Auditoria

1. ler documentação;
2. revisar `INSTALLED_APPS`;
3. revisar migrations;
4. revisar imports;
5. revisar `config`;
6. revisar `usuarios`;
7. executar baseline de testes.

### 20.2 `core`

1. criar app;
2. definir `AppConfig`;
3. criar estrutura mínima;
4. implementar somente abstrações justificadas;
5. testar;
6. registrar app quando necessário.

### 20.3 `clientes`

1. criar app;
2. definir `AppConfig`;
3. criar estrutura mínima;
4. definir namespace;
5. documentar responsabilidades;
6. não criar modelo definitivo;
7. adicionar testes estruturais.

### 20.4 Integração

1. revisar apps instaladas;
2. revisar URLs;
3. revisar imports;
4. evitar ciclos;
5. preservar autenticação;
6. preservar Storage.

### 20.5 Validação

1. executar check;
2. executar dry-run de migrations;
3. executar testes;
4. revisar diff;
5. verificar segredos;
6. atualizar documentação;
7. gerar relatório.

## 21. Testes obrigatórios

Cobrir no mínimo:

1. `core` carrega corretamente;
2. `clientes` carrega corretamente;
3. `usuarios` permanece funcional;
4. `AUTH_USER_MODEL` permanece correto;
5. modelo abstrato de `core` é abstrato;
6. nenhuma tabela concreta é criada em `core`;
7. nenhuma migration inesperada é criada;
8. URLs existentes continuam funcionando;
9. login continua funcionando;
10. perfil continua funcionando;
11. usuário comum continua sem admin;
12. Storage continua respeitando ownership;
13. imports não possuem ciclos;
14. suíte anterior continua passando;
15. nenhum segredo aparece em resposta ou log.

## 22. Comandos de verificação

Executar:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py test usuarios config core clientes
```

Quando necessário:

```powershell
python backend/manage.py test
```

Não mascarar falhas.

## 23. Critérios de aceite

A etapa só estará pronta quando:

1. `core` existir;
2. `clientes` existir;
3. responsabilidades estiverem claras;
4. `usuarios` continuar funcional;
5. `config` continuar funcional;
6. `ProtectedFile` permanecer em `config`;
7. nenhuma app `arquivos` tiver sido criada;
8. `INSTALLED_APPS` estiver correto;
9. não houver ciclos;
10. não houver código de clientes em `core`;
11. não houver autenticação em `clientes`;
12. não houver migrations concretas inesperadas;
13. `manage.py check` passar;
14. dry-run de migrations estiver estável;
15. testes passarem;
16. documentação estiver atualizada;
17. nenhum segredo tiver sido exposto;
18. a próxima etapa estiver identificada.

## 24. Próxima etapa

Após esta skill, a próxima etapa será:

```text
Fase 2.3 — Implementação do modelo Cliente
```

Ela deverá incluir:

- `TipoCliente`;
- `SituacaoCliente`;
- modelo `Cliente`;
- UUID;
- campos PF/PJ;
- endereço incorporado;
- contato principal;
- validação de CPF e CNPJ;
- normalização;
- autoria;
- constraints;
- índices;
- admin;
- migrations;
- testes.

## 25. Restrições do agente

O agente deve:

- trabalhar de forma incremental;
- preservar o comportamento atual;
- não expor `.env`;
- não imprimir segredos;
- não fazer commit;
- não fazer push;
- não aplicar migration remota;
- não executar operações destrutivas;
- não alterar Blueprint silenciosamente;
- não criar camadas artificiais;
- não ampliar o escopo;
- registrar bloqueadores objetivamente.

## 26. Saída esperada

Ao concluir, apresentar:

1. subetapas concluídas;
2. apps criadas;
3. arquivos alterados;
4. abstrações criadas;
5. imports revisados;
6. migrations geradas ou não geradas;
7. testes executados;
8. resultados dos checks;
9. documentação atualizada;
10. bloqueadores;
11. riscos restantes;
12. próxima etapa;
13. veredito:
   - `READY`;
   - `READY WITH RESERVATIONS`;
   - `NOT READY`.
