# Especificação Técnica — Estrutura Modular das Apps Django
## Projeto PC-DJANGO-001

## 1. Identificação da etapa

**Fase principal:** Fase 2 — Estruturação do domínio e autenticação  
**Subetapa:** 2.2 — Organização das apps `core`, `usuarios` e `clientes`  
**Status:** Especificação aprovada para implementação futura  
**Escopo deste documento:** definir os limites, responsabilidades, estrutura de diretórios, dependências, regras de organização e critérios de aceite das apps Django antes da implementação definitiva do domínio de clientes.

---

## 2. Objetivo

Organizar o backend Django em apps com responsabilidades claras, evitando que configurações de projeto, autenticação, regras de clientes, utilitários compartilhados e arquivos privados permaneçam misturados.

A arquitetura modular aprovada será:

```text
config
├── configuração do projeto
├── composição de URLs
├── ambiente e logging
└── integração de infraestrutura com Supabase

core
├── componentes compartilhados
├── classes abstratas
├── normalizações genéricas
└── utilitários independentes de domínio

usuarios
├── autenticação
├── usuário customizado
├── perfil
├── sessões
└── permissões de usuário

clientes
├── entidade Cliente
├── regras PF e PJ
├── endereço e contato principal
├── validações
├── formulários
└── operações do domínio

arquivos
└── decisão futura após a implementação de Cliente
```

---

## 3. Estado atual considerado

Esta especificação parte do seguinte estado do projeto:

1. o projeto Django está criado em `backend/`;
2. a app `usuarios` já existe;
3. `usuarios.Usuario` é o modelo de usuário customizado;
4. a autenticação usa e-mail, senha e sessões Django;
5. `AUTH_USER_MODEL` já está configurado;
6. existe integração backend-only com PostgreSQL e Storage do Supabase;
7. existe o modelo `ProtectedFile`;
8. o acesso ao Storage privado utiliza identificação interna e autorização por proprietário;
9. existem migrations e testes das etapas anteriores;
10. a app `clientes` ainda precisa ser estruturada;
11. a app `core` ainda precisa ser estruturada;
12. a criação de uma app `arquivos` está adiada.

A implementação desta etapa deverá preservar o comportamento existente de autenticação e segurança.

---

## 4. Decisões arquiteturais aprovadas

1. `config` será a app de configuração do projeto, não a localização definitiva das regras de negócio.
2. `core` conterá apenas elementos verdadeiramente compartilhados.
3. `usuarios` continuará responsável por identidade, autenticação, perfil e permissões.
4. `clientes` concentrará o domínio de clientes PF e PJ.
5. PF e PJ utilizarão uma única entidade `Cliente`.
6. Não serão criadas apps separadas para Pessoa Física e Pessoa Jurídica.
7. Não serão criadas apps separadas para endereço e contato nesta primeira versão.
8. Endereço e contato principal permanecerão dentro do domínio de `clientes`.
9. Não será criada a app `arquivos` nesta subetapa.
10. `ProtectedFile` não será movido nesta subetapa.
11. Nenhuma tabela existente será renomeada apenas por organização estética.
12. Nenhuma migration remota será aplicada automaticamente.
13. A app `core` não poderá se transformar em depósito genérico de código sem dono.
14. Código específico de clientes não poderá ser colocado em `core`.
15. Código específico de autenticação não poderá ser colocado em `clientes`.
16. Relações com usuários deverão usar `settings.AUTH_USER_MODEL`.
17. O isolamento de dados por usuário continuará obrigatório.
18. O administrador poderá acessar todos os dados somente por autorização explícita.
19. A estrutura deverá permanecer simples e compatível com Django Templates.
20. Não será introduzido framework adicional nesta etapa.

---

## 5. Estrutura alvo do backend

Estrutura conceitual esperada:

```text
backend/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── env.py
│   ├── logging.py
│   ├── settings.py
│   ├── supabase.py
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
│   ├── models.py
│   ├── migrations/
│   └── tests.py
├── core/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── normalizers.py
│   ├── permissions.py
│   ├── tests/
│   └── migrations/
├── usuarios/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── managers.py
│   ├── models.py
│   ├── permissions.py
│   ├── urls.py
│   ├── validators.py
│   ├── views.py
│   ├── templates/
│   ├── tests.py ou tests/
│   └── migrations/
├── clientes/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── choices.py
│   ├── forms.py
│   ├── models.py
│   ├── permissions.py
│   ├── services.py
│   ├── urls.py
│   ├── validators.py
│   ├── views.py
│   ├── templates/
│   ├── tests/
│   └── migrations/
├── templates/
├── static/
└── media/
```

A estrutura física poderá ser menor no início. Arquivos vazios não deverão ser criados apenas para aparentar completude. Cada módulo deverá existir quando possuir responsabilidade real.

---

## 6. Responsabilidade da app `config`

### 6.1 Finalidade

A app `config` continuará sendo o núcleo de configuração e inicialização do projeto Django.

Responsabilidades permitidas:

- `settings.py`;
- leitura de variáveis de ambiente;
- configuração de banco;
- configuração de cookies e segurança;
- logging;
- URLs principais;
- ASGI;
- WSGI;
- integração de infraestrutura com Supabase;
- health checks ou endpoints estritamente técnicos;
- composição das URLs das demais apps.

### 6.2 Restrições

Novas regras de negócio não deverão ser adicionadas em `config`.

Não deverão ser criados em `config`:

- modelo `Cliente`;
- validadores de CPF ou CNPJ de clientes;
- formulários de cliente;
- regras de pesquisa;
- regras de dashboard;
- relatórios de clientes;
- autorização específica de clientes;
- templates funcionais do domínio.

### 6.3 Situação temporária de `ProtectedFile`

`ProtectedFile` permanecerá temporariamente em `config` para evitar uma movimentação estrutural prematura.

Essa permanência é uma dívida técnica controlada.

Durante esta subetapa:

- não mover a classe;
- não renomear a tabela;
- não apagar migrations;
- não duplicar o modelo;
- não criar uma segunda implementação;
- preservar os testes existentes.

A decisão definitiva será tomada depois que o relacionamento entre arquivos e clientes estiver definido.

---

## 7. Responsabilidade da app `core`

### 7.1 Finalidade

A app `core` conterá componentes compartilhados que não pertencem exclusivamente a `usuarios`, `clientes`, `config` ou outra app de domínio.

### 7.2 Conteúdo permitido

Exemplos permitidos:

- modelos abstratos;
- geração de UUID;
- timestamps compartilhados;
- normalização genérica de texto;
- normalização de números;
- mixins reutilizáveis;
- helpers genéricos de autorização;
- constantes realmente globais;
- exceções compartilhadas;
- funções comuns para paginação ou respostas;
- classes base para testes, quando justificadas.

### 7.3 Conteúdo proibido

Não colocar em `core`:

- regras específicas de CPF e CNPJ de clientes;
- regras de tipo PF ou PJ;
- formulários de clientes;
- login;
- criação de usuários;
- consultas de dashboard;
- relatórios;
- acesso direto ao Storage;
- regras específicas de `ProtectedFile`;
- lógica que só é usada por uma app;
- funções genéricas chamadas apenas de `helper` sem responsabilidade clara.

### 7.4 Modelo abstrato recomendado

A app poderá oferecer uma base abstrata mínima:

```python
class UUIDTimestampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

A nomenclatura definitiva poderá ser ajustada para seguir o padrão do projeto.

Essa classe:

- não deverá criar tabela própria;
- não deverá gerar migration com operação de banco isolada;
- poderá ser herdada por modelos futuros;
- não deverá incluir autoria automaticamente se isso reduzir a clareza.

### 7.5 Auditoria de autoria

Os campos:

```text
criado_por
atualizado_por
```

poderão ser implementados diretamente em `Cliente` ou em uma classe abstrata separada.

A decisão deverá priorizar:

- clareza;
- ausência de conflitos de `related_name`;
- uso de `settings.AUTH_USER_MODEL`;
- preservação histórica;
- simplicidade de migrations.

Não criar uma abstração de auditoria se ela não for reutilizada por pelo menos dois modelos concretos.

### 7.6 Registro no Django

`core` deverá ser adicionada ao `INSTALLED_APPS` somente se for uma app Django real.

Se possuir somente módulos Python compartilhados e nenhuma necessidade de app registry, deverá ser avaliado se o registro é necessário.

---

## 8. Responsabilidade da app `usuarios`

### 8.1 Finalidade

A app `usuarios` continuará sendo a única fonte de identidade da aplicação.

Responsabilidades:

- modelo `Usuario`;
- manager customizado;
- autenticação por e-mail;
- login;
- logout;
- perfil;
- troca de senha;
- Django Admin de usuários;
- permissões relacionadas a usuários;
- validação de CPF do perfil do usuário;
- proteção contra edição cruzada;
- ativação e desativação de contas.

### 8.2 Preservação da implementação atual

Esta etapa não deverá reescrever a autenticação já implementada.

Alterações em `usuarios` serão permitidas somente quando necessárias para:

- corrigir importações;
- reutilizar um componente realmente genérico de `core`;
- manter compatibilidade com `clientes`;
- preservar relações com `settings.AUTH_USER_MODEL`;
- melhorar organização sem alterar comportamento.

### 8.3 Helpers de propriedade

Helpers atuais de ownership poderão permanecer em `usuarios.permissions`.

Eles somente deverão ser movidos para `core.permissions` quando:

1. forem realmente genéricos;
2. não dependerem de detalhes de perfil;
3. forem usados por mais de uma app;
4. todos os testes forem atualizados;
5. não houver mudança funcional.

A movimentação não é obrigatória nesta subetapa.

---

## 9. Responsabilidade da app `clientes`

### 9.1 Finalidade

A app `clientes` será responsável por todo o domínio de cadastro e gestão de clientes.

Responsabilidades futuras:

- modelo `Cliente`;
- Pessoa Física;
- Pessoa Jurídica;
- CPF;
- CNPJ;
- nome completo;
- nome empresarial;
- data de nascimento;
- data de abertura;
- e-mail;
- telefone principal;
- endereço;
- situação;
- observações;
- autoria;
- validações;
- normalização;
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

### 9.2 Entidade única

PF e PJ utilizarão a mesma entidade:

```text
Cliente
```

Diferenciação:

```text
tipo = PF ou PJ
```

Não criar:

- `PessoaFisica`;
- `PessoaJuridica`;
- tabelas separadas;
- apps separadas;
- herança multi-table para PF e PJ.

### 9.3 Campos previstos

O futuro modelo `Cliente` deverá considerar:

```text
id
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
situacao
criado_em
atualizado_em
criado_por
atualizado_por
```

Esta subetapa de estruturação não deverá inventar novos campos fora do Blueprint.

### 9.4 Endereço

Na primeira versão, o endereço permanecerá dentro de `Cliente`.

Não criar nesta etapa:

- app `enderecos`;
- modelo `Endereco`;
- múltiplos endereços;
- endereço de cobrança;
- endereço de entrega;
- endereço comercial separado.

### 9.5 Contato

Na primeira versão, o contato permanecerá dentro de `Cliente`.

Campos principais:

- telefone principal obrigatório;
- e-mail opcional.

Não criar nesta etapa:

- app `contatos`;
- tabela separada de contatos;
- telefone secundário;
- múltiplos e-mails;
- agenda de contatos relacionada.

### 9.6 Organização interna

Responsabilidades recomendadas:

```text
choices.py
→ TipoCliente e SituacaoCliente

validators.py
→ CPF, CNPJ, telefone, CEP, UF, data e nome

models.py
→ estrutura persistente e invariantes essenciais

forms.py
→ validação de entrada e comportamento PF/PJ

services.py
→ operações que coordenam mais de um objeto ou efeito

permissions.py
→ escopo por proprietário e acesso administrativo

views.py
→ coordenação HTTP, sem concentrar regras de negócio

admin.py
→ administração segura do domínio
```

Não criar camadas artificiais sem uso real.

---

## 10. Escopo exato desta subetapa

### 10.1 Deve ser implementado

1. criar a app `core`;
2. criar a app `clientes`;
3. registrar as apps necessárias;
4. definir claramente seus limites;
5. criar a estrutura mínima de módulos;
6. criar modelos abstratos de `core` apenas se justificados;
7. preparar `clientes` para a próxima subetapa;
8. configurar namespace de URLs quando houver rota real;
9. preservar `usuarios`;
10. preservar `ProtectedFile`;
11. atualizar documentação estrutural;
12. adicionar testes mínimos de carregamento das apps;
13. verificar migrations inesperadas;
14. executar a suíte existente.

### 10.2 Não deve ser implementado

Nesta subetapa, não implementar ainda:

- modelo definitivo `Cliente`;
- formulário completo de cadastro;
- validação completa de CPF e CNPJ de clientes;
- integração com CEP;
- pesquisa;
- dashboard;
- relatórios;
- exportações;
- app `arquivos`;
- movimentação de `ProtectedFile`;
- upload de arquivos;
- relacionamento arquivo-cliente;
- migrations remotas;
- frontend completo;
- alteração visual ampla.

---

## 11. Estrutura mínima recomendada para `core`

Estrutura inicial possível:

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

Somente criar `permissions.py`, `mixins.py`, `exceptions.py` ou outros módulos quando existir uso concreto.

---

## 12. Estrutura mínima recomendada para `clientes`

Estrutura inicial possível:

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

Arquivos sem implementação deverão conter apenas o mínimo necessário ou poderão ser adiados.

Não utilizar código placeholder que simule funcionalidade inexistente.

---

## 13. Dependências entre apps

Dependências permitidas:

```text
config
→ inclui URLs e configura apps

usuarios
→ pode usar core

clientes
→ pode usar core
→ depende de settings.AUTH_USER_MODEL
→ não importa diretamente config.models

config ProtectedFile
→ depende de settings.AUTH_USER_MODEL
```

Dependências proibidas:

```text
core → clientes
core → usuarios
core → config

usuarios → clientes

clientes → config para regras de domínio

clientes → implementação concreta de Usuario por import direto
```

Para obter o modelo de usuário em runtime:

```python
get_user_model()
```

Para relacionamentos:

```python
settings.AUTH_USER_MODEL
```

---

## 14. Regras para imports

1. evitar dependências circulares;
2. usar imports relativos dentro da mesma app;
3. evitar importações de views em models;
4. evitar importações de forms em models;
5. manter integração entre apps por contratos claros;
6. usar strings em relacionamentos quando necessário;
7. não importar `usuarios.Usuario` diretamente em models de domínio;
8. não importar `config.settings` diretamente;
9. usar `django.conf.settings`;
10. não criar módulos genéricos apenas para contornar ciclos mal projetados.

---

## 15. Regras para migrations

### 15.1 `core`

Se possuir somente modelos abstratos:

- nenhuma tabela deverá ser criada;
- não deverá haver migration com `CreateModel` concreto;
- `makemigrations --check --dry-run` deverá permanecer estável.

### 15.2 `clientes`

Como o modelo definitivo de Cliente está fora desta subetapa:

- não criar tabela `Cliente` ainda;
- não criar migration concreta de domínio;
- manter apenas `migrations/__init__.py`.

### 15.3 `usuarios`

- não alterar migrations aplicadas;
- não reescrever a migration inicial;
- criar nova migration somente quando houver mudança necessária e aprovada.

### 15.4 `ProtectedFile`

- não mover tabela;
- não alterar `db_table`;
- não apagar migration;
- não duplicar migration;
- não mudar ownership sem necessidade.

### 15.5 Banco remoto

Não executar automaticamente:

```powershell
python backend/manage.py migrate
```

contra o Supabase.

Qualquer aplicação remota dependerá de autorização explícita em etapa separada.

---

## 16. Estratégia futura para `arquivos`

A app `arquivos` será decidida depois da criação do modelo `Cliente`.

### 16.1 Criar app `arquivos` quando

- arquivos pertencerem a mais de um domínio;
- existirem arquivos de usuários, clientes, relatórios ou outros módulos;
- houver regras próprias de upload;
- houver versionamento;
- houver múltiplos tipos de vínculo;
- houver ciclo de vida próprio;
- houver permissões independentes.

Estrutura futura possível:

```text
arquivos/
├── models.py
├── services.py
├── permissions.py
├── validators.py
└── tests/
```

### 16.2 Manter em `clientes` quando

- todos os arquivos forem exclusivamente de clientes;
- o ciclo de vida depender do cliente;
- não existir reutilização em outros módulos;
- a autorização sempre decorrer da propriedade do cliente.

Modelo futuro possível:

```text
clientes.ClienteArquivo
```

### 16.3 Decisão adiada

Nesta subetapa:

```text
ProtectedFile permanece em config
```

A decisão futura deverá avaliar:

- dados existentes;
- migrations aplicadas;
- nome da tabela;
- vínculo com Cliente;
- compatibilidade com Storage;
- impacto em URLs assinadas;
- preservação de ownership;
- possibilidade de migration de estado separada da migration de banco.

---

## 17. Segurança

A reorganização deverá preservar:

- autenticação obrigatória;
- sessões Django;
- CSRF;
- cookies seguros;
- isolamento por usuário;
- acesso total apenas para administrador;
- segredos fora do frontend;
- Supabase backend-only;
- URLs assinadas curtas;
- filtragem de segredos em logs;
- `.env` ignorado;
- ausência de dados reais em testes.

Nenhuma reorganização deverá reduzir controles existentes.

---

## 18. Testes mínimos

A subetapa deverá testar:

1. app `core` carregada corretamente;
2. app `clientes` carregada corretamente;
3. app `usuarios` continua carregada;
4. `AUTH_USER_MODEL` permanece correto;
5. modelos abstratos de `core` são abstratos;
6. nenhum modelo concreto inesperado é criado em `core`;
7. nenhuma migration inesperada é gerada;
8. URLs existentes continuam funcionando;
9. login continua funcionando;
10. perfil continua funcionando;
11. usuário comum continua sem acesso ao admin;
12. Storage privado continua respeitando ownership;
13. imports não possuem ciclos;
14. suíte anterior continua passando;
15. nenhum segredo aparece em resposta ou log.

---

## 19. Comandos de verificação

Executar a partir da raiz do repositório:

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py test usuarios config core clientes
```

Se `core` ou `clientes` ainda não possuírem testes descobertos, executar a suíte completa:

```powershell
python backend/manage.py test
```

Não mascarar falhas existentes.

---

## 20. Documentação

Atualizar:

- `README.md`;
- relatório da implementação desta etapa;
- árvore da estrutura do backend;
- responsabilidades de cada app;
- situação temporária de `ProtectedFile`;
- decisão futura sobre `arquivos`;
- próxima etapa do roadmap.

Não alterar silenciosamente os arquivos de Blueprint.

Caso a estrutura aprovada conflite com o Blueprint, registrar a divergência e solicitar atualização documental separada.

---

## 21. Subetapas numeradas da implementação

### 21.1 Auditoria inicial

1. ler `AGENTS.md`;
2. ler os Blueprints relacionados;
3. revisar o relatório de usuários;
4. revisar migrations;
5. revisar `INSTALLED_APPS`;
6. revisar imports;
7. executar testes de baseline.

### 21.2 Criação de `core`

1. criar app;
2. definir `AppConfig`;
3. criar estrutura mínima;
4. implementar apenas abstrações justificadas;
5. testar abstrações;
6. registrar app quando necessário.

### 21.3 Criação de `clientes`

1. criar app;
2. definir `AppConfig`;
3. criar estrutura mínima;
4. definir namespaces;
5. documentar responsabilidades;
6. não implementar ainda o modelo definitivo;
7. adicionar testes de estrutura.

### 21.4 Integração

1. revisar `INSTALLED_APPS`;
2. revisar URLs;
3. evitar ciclos;
4. preservar autenticação;
5. preservar Storage;
6. revisar imports compartilhados.

### 21.5 Validação

1. executar `check`;
2. executar dry-run de migrations;
3. executar testes;
4. revisar diff;
5. verificar segredos;
6. atualizar documentação;
7. emitir relatório.

---

## 22. Critérios de aceite

A subetapa será considerada concluída quando:

1. `core` existir com responsabilidade clara;
2. `clientes` existir com responsabilidade clara;
3. `usuarios` permanecer funcional;
4. `config` permanecer funcional;
5. `ProtectedFile` não tiver sido movido;
6. nenhuma app `arquivos` tiver sido criada;
7. `INSTALLED_APPS` estiver correto;
8. não houver dependência circular;
9. não houver código de cliente em `core`;
10. não houver regra de autenticação em `clientes`;
11. não houver migration concreta inesperada;
12. `manage.py check` passar;
13. dry-run de migrations não indicar mudanças não revisadas;
14. testes existentes passarem;
15. novos testes de estrutura passarem;
16. documentação estiver atualizada;
17. nenhum segredo tiver sido exposto;
18. a próxima etapa estiver claramente identificada.

---

## 23. Próxima etapa após esta especificação

Depois da estrutura modular, a próxima subetapa será:

```text
Fase 2.3 — Implementação do modelo Cliente
```

Essa etapa deverá incluir:

- `TipoCliente`;
- `SituacaoCliente`;
- modelo `Cliente`;
- UUID;
- campos PF/PJ;
- endereço incorporado;
- contato principal;
- CPF e CNPJ;
- normalização;
- validações;
- autoria;
- índices;
- constraints;
- admin;
- migrations;
- testes de modelo.

---

## 24. Itens fora do escopo

Não fazem parte desta subetapa:

- modelo completo de Cliente;
- CRUD de clientes;
- pesquisa;
- dashboard;
- relatórios;
- exportação;
- upload;
- movimentação de `ProtectedFile`;
- app `arquivos`;
- Supabase Auth;
- API pública;
- React;
- Next.js;
- multiempresa;
- deploy;
- aplicação de migrations remotas.

---

## 25. Conclusão

A decisão aprovada é organizar o backend em apps com limites claros:

```text
config
→ configuração e infraestrutura

core
→ abstrações e componentes realmente compartilhados

usuarios
→ identidade, autenticação, perfil e permissões

clientes
→ domínio completo de clientes PF e PJ

arquivos
→ decisão futura
```

A implementação desta subetapa deverá criar a base estrutural de `core` e `clientes`, preservar integralmente `usuarios`, manter `ProtectedFile` temporariamente em `config` e preparar o projeto para a implementação definitiva do modelo `Cliente`.
