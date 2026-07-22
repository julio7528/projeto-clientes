# Especificação Técnica — Fase Final do PC-DJANGO-001

## 1. Identificação

**Fase:** 3 — Finalização funcional, qualidade e operação  
**Subetapas:**

1. Pesquisa e filtros;
2. Dashboard;
3. Relatórios e exportações;
4. Testes completos;
5. Separação de ambientes;
6. Deploy e operação;
7. Correção documental.

O objetivo desta fase é concluir o MVP e deixá-lo preparado para QA e produção.

---

## 2. Marco atual correto

```text
Fase 1 — Bootstrap, Supabase e segurança: CONCLUÍDA
Fase 2 — Usuários, autenticação e domínio de clientes: CONCLUÍDA
Fase 3 — Pesquisa, análise, qualidade e operação: PRÓXIMA
```

Já estão concluídos:

- projeto Django e arquitetura modular;
- PostgreSQL e Storage privado no Supabase;
- integração backend-only;
- usuário customizado;
- login por e-mail e sessões Django;
- migrations de desenvolvimento;
- superusuário de desenvolvimento;
- modelo Cliente PF/PJ;
- validações, ownership e Admin;
- cadastro, lista inicial, detalhes, edição, ativação e inativação;
- testes das fases anteriores.

---

## 3. Decisões arquiteturais

1. Pesquisa e filtros permanecem em `clientes`.
2. O dashboard será uma app própria: `dashboard`.
3. Relatórios e exportações serão uma app própria: `relatorios`.
4. `clientes` fornecerá uma camada reutilizável de consulta.
5. `dashboard` e `relatorios` dependerão de `clientes`.
6. Usuário comum verá apenas seus clientes.
7. Administrador verá todos.
8. Filtros serão validados no backend.
9. Documentos ficarão mascarados em listas, dashboard, relatórios e exportações.
10. Exportação com documento completo fica fora do MVP.
11. Exportações serão geradas sob demanda e não serão armazenadas.
12. Haverá limite configurável de registros exportados.
13. Dashboard usará agregações no banco.
14. Não haverá Realtime, Supabase Auth ou API pública.
15. Desenvolvimento, QA e produção usarão bancos, Storage e credenciais distintos.
16. Produção exigirá aprovação manual, backup e CI verde.
17. Logs não conterão PII nem segredos.
18. O README deverá refletir o código real.

---

## 4. Estrutura alvo

```text
backend/
├── config/
│   └── settings/
│       ├── base.py
│       ├── development.py
│       ├── test.py
│       ├── qa.py
│       └── production.py
├── clientes/
│   ├── filters.py
│   ├── querying.py
│   └── tests/
├── dashboard/
│   ├── forms.py
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/dashboard/
│   └── tests/
└── relatorios/
    ├── choices.py
    ├── forms.py
    ├── services.py
    ├── exporters/
    │   ├── csv.py
    │   ├── xlsx.py
    │   └── pdf.py
    ├── views.py
    ├── urls.py
    ├── templates/relatorios/
    └── tests/
```

Não criar arquivos vazios sem responsabilidade real.

---

# PARTE I — PESQUISA E FILTROS

## 5. Rota e formulário

A rota atual será expandida:

```text
GET /clientes/
clientes:list
```

Criar:

```text
clientes.filters.ClienteSearchForm
```

Campos:

- `q`;
- `tipo`;
- `situacao`;
- `cidade`;
- `estado`;
- `criado_de`;
- `criado_ate`;
- `atualizado_de`;
- `atualizado_ate`;
- `ordenar`;
- `direcao`.

Todos os filtros usarão `GET`.

---

## 6. Busca geral

O campo `q` pesquisará:

- nome;
- documento;
- telefone;
- e-mail.

Regras:

- nome: correspondência parcial e case-insensitive;
- documento: aceitar com ou sem máscara e priorizar correspondência exata;
- telefone: aceitar com ou sem máscara e comparar o número normalizado;
- e-mail: normalizar para minúsculas e aceitar correspondência parcial;
- espaços duplicados serão tratados;
- o termo terá tamanho máximo definido;
- não haverá busca automática a cada caractere no MVP.

---

## 7. Filtros

Filtros disponíveis:

- PF/PJ;
- ativo/inativo/todos;
- cidade;
- UF;
- período de criação;
- período de atualização.

Datas:

- início não pode ser posterior ao fim;
- um único limite é permitido;
- o fim deve incluir o dia completo;
- erros serão exibidos no formulário.

Os filtros serão combinados com `AND`. A busca geral poderá usar `OR` entre seus campos.

---

## 8. Ownership e segurança

A consulta sempre começará pelo queryset autorizado:

```python
scope_owned_queryset(
    Cliente.objects.all(),
    request.user,
    owner_field="criado_por",
)
```

Depois serão aplicados busca, filtros, ordenação e paginação.

Nenhum parâmetro poderá ampliar o escopo de acesso.

---

## 9. Estado inicial, ordenação e paginação

Estado inicial:

- apenas ativos;
- nome crescente;
- 20 registros por página.

Ordenações permitidas:

- nome;
- criação;
- atualização;
- cidade;
- situação.

Usar allowlist. Nunca aplicar diretamente ao ORM um nome de campo vindo do navegador.

A paginação deverá preservar filtros, ordenação e página.

---

## 10. Resultado e privacidade

Colunas:

- nome;
- tipo;
- documento mascarado;
- telefone;
- e-mail;
- cidade/UF;
- situação;
- atualizado em;
- ações.

Ações:

- visualizar;
- editar;
- ativar/inativar.

Não exibir exclusão física.

Documentos:

```text
CPF: ***.456.789-**
CNPJ: **.345.678/0001-**
```

O documento completo continuará restrito às telas autorizadas de detalhes e edição.

---

## 11. Estados da pesquisa

Sem cadastros:

```text
Nenhum cliente cadastrado.
```

Sem resultados:

```text
Nenhum cliente encontrado com os critérios informados.
```

Exibir:

- limpar filtros;
- cadastrar novo cliente;
- quantidade encontrada;
- intervalo exibido.

Ao retornar de detalhes ou edição, preservar filtros e página por URL local validada.

---

## 12. Camada de consulta compartilhada

Criar em `clientes.querying`:

```text
ClienteFilterSpec
apply_cliente_filters()
apply_cliente_ordering()
```

Essa camada deverá:

- receber valores validados;
- trabalhar sobre queryset já autorizado;
- não conhecer `request`;
- ser reutilizada por pesquisa, dashboard e relatórios;
- evitar duplicação das regras.

---

# PARTE II — DASHBOARD

## 13. App e rota

Criar app:

```text
dashboard
```

Rota:

```text
GET /dashboard/
dashboard:index
```

Depois da implementação, o login redirecionará por padrão para `dashboard:index`.

---

## 14. Filtros do dashboard

Criar `DashboardFilterForm` com:

- período;
- data inicial;
- data final;
- tipo;
- situação;
- estado;
- cidade.

Períodos:

- hoje;
- últimos 7 dias;
- últimos 30 dias;
- mês atual;
- ano atual;
- personalizado;
- todos os períodos.

Padrão: todos os períodos.

---

## 15. Indicadores

O dashboard deverá exibir:

1. total de clientes;
2. total PF;
3. total PJ;
4. ativos;
5. inativos;
6. novos no período;
7. cadastros incompletos.

Cadastro incompleto: falta de pelo menos um campo relevante entre:

- e-mail;
- data de referência;
- logradouro;
- número;
- bairro;
- cidade;
- estado.

`complemento` não será usado para classificar incompletude.

---

## 16. Gráficos e rankings

Implementar:

- distribuição PF/PJ;
- distribuição ativos/inativos;
- novos clientes no tempo;
- 10 estados com mais clientes;
- 10 cidades com mais clientes.

As agregações serão feitas no banco usando `Count`, `Q`, `values`, `annotate` e funções de data.

Não carregar todos os clientes em memória para agrupar.

---

## 17. Tabelas resumidas

Exibir:

- 5 clientes criados recentemente;
- 5 clientes atualizados recentemente;
- 5 cadastros incompletos prioritários.

Mostrar apenas dados mínimos:

- nome;
- tipo;
- cidade/UF;
- data;
- ação.

Sempre respeitar ownership.

---

## 18. Gráficos acessíveis

Os dados serão fornecidos pelo backend.

Regras:

- usar `json_script` ou equivalente;
- não interpolar JSON manualmente;
- biblioteca de gráfico local, sem CDN em produção;
- nenhum envio de dados a terceiros;
- valores também exibidos em texto/tabela;
- não depender apenas de cor;
- nenhuma PII desnecessária.

Não haverá Realtime, polling ou WebSocket.

---

## 19. Serviço do dashboard

Criar:

```text
dashboard.services.DashboardService
```

O serviço deverá:

- receber queryset autorizado;
- aplicar filtros;
- calcular cards;
- calcular séries;
- limitar rankings;
- retornar dados estruturados;
- evitar queries ocultas no template.

A página será autenticada, com `Cache-Control: private, no-store`.

---

# PARTE III — RELATÓRIOS E EXPORTAÇÕES

## 20. App e rotas

Criar app:

```text
relatorios
```

Rotas:

```text
GET /relatorios/
GET /relatorios/clientes/
GET /relatorios/clientes/exportar/csv/
GET /relatorios/clientes/exportar/xlsx/
GET /relatorios/clientes/exportar/pdf/
```

Namespace:

```text
relatorios
```

---

## 21. Tipos de relatório

1. geral de clientes;
2. por tipo;
3. por situação;
4. por cidade e estado;
5. cadastros por período;
6. atualizações por período;
7. cadastros incompletos.

Filtros:

- busca geral;
- tipo;
- situação;
- cidade;
- estado;
- criação;
- atualização;
- campo preenchido/ausente;
- ordenação.

Reutilizar a camada de consulta de `clientes`.

---

## 22. Visualização

Relatórios detalhados:

- tabela;
- resumo;
- 50 registros por página;
- filtros preservados.

Relatórios consolidados:

- totais;
- percentuais;
- tabela;
- gráfico opcional.

A exportação incluirá todos os registros filtrados dentro do limite, e não apenas a página atual.

---

## 23. Privacidade

Em telas e arquivos:

- CPF/CNPJ mascarados;
- observações fora do relatório geral;
- endereço completo fora do relatório padrão;
- autoria não exportada;
- documento completo fora do MVP.

Nenhum parâmetro do usuário poderá desativar o mascaramento.

---

## 24. Limite de exportação

Variável:

```text
REPORT_EXPORT_MAX_ROWS
```

Padrão:

```text
10000
```

Regras:

- contar antes de gerar;
- bloquear acima do limite;
- não truncar silenciosamente;
- solicitar filtros mais específicos;
- processamento assíncrono fica fora do MVP.

---

## 25. CSV

Usar biblioteca padrão `csv`.

Requisitos:

- UTF-8 com BOM;
- cabeçalho;
- acentos preservados;
- separador compatível com planilhas;
- datas formatadas;
- documento mascarado;
- todos os registros filtrados;
- filename seguro;
- `no-store`.

Nome:

```text
relatorio_clientes_YYYY-MM-DD.csv
```

Neutralizar CSV injection para valores iniciados por:

```text
= + - @
```

---

## 26. XLSX

Implementação recomendada:

```text
openpyxl
```

Requisitos:

- aba Dados;
- aba Resumo quando aplicável;
- cabeçalhos;
- autofiltro;
- primeira linha congelada;
- datas formatadas;
- larguras com limite;
- documentos mascarados;
- nenhuma fórmula originada de dados;
- geração em memória;
- `no-store`.

Nome:

```text
relatorio_clientes_YYYY-MM-DD.xlsx
```

---

## 27. PDF

Implementação recomendada:

```text
ReportLab
```

Requisitos:

- server-side;
- título;
- data/hora;
- filtros;
- resumo;
- tabela;
- cabeçalho repetido;
- número de página;
- quebra correta;
- documento mascarado;
- suporte a acentos;
- nenhum recurso remoto;
- geração em memória;
- `no-store`.

Nome:

```text
relatorio_clientes_YYYY-MM-DD.pdf
```

Outra biblioteca exigirá justificativa e teste de deploy.

---

## 28. Exporters

Estrutura:

```text
relatorios/exporters/csv.py
relatorios/exporters/xlsx.py
relatorios/exporters/pdf.py
```

Exporters receberão dados prontos e não consultarão o banco.

Fluxo da view:

1. autenticar;
2. validar filtros;
3. aplicar ownership;
4. aplicar filtros;
5. verificar limite;
6. construir dados;
7. gerar arquivo;
8. retornar download.

Nenhum relatório será salvo permanentemente.

---

# PARTE IV — TESTES COMPLETOS

## 29. Tipos de teste

Cobrir:

- unitários;
- modelos;
- validadores;
- forms;
- autenticação;
- CSRF;
- permissões;
- CRUD;
- pesquisa;
- dashboard;
- relatórios;
- exports;
- ambientes;
- deploy;
- regressão.

Checklist manual de navegador será obrigatório em QA.

---

## 30. Cobertura

Adicionar medição de cobertura.

Meta:

```text
85% de cobertura de linhas do backend
```

A CI falhará abaixo da meta.

Migrations poderão ser omitidas. Cobertura não substitui testes explícitos de comportamento e segurança.

---

## 31. Pesquisa

Testar:

- ownership e admin;
- nome;
- documento formatado e sem máscara;
- telefone;
- e-mail;
- cidade;
- estado;
- tipo;
- situação;
- períodos;
- filtros combinados;
- datas inválidas;
- allowlist de ordenação;
- paginação;
- preservação de query string;
- mascaramento;
- estados vazios.

---

## 32. Dashboard

Testar:

- autenticação;
- ownership;
- todos os indicadores;
- períodos;
- filtros combinados;
- incompletos;
- rankings;
- recentes;
- base vazia;
- filtro sem dados;
- JSON seguro;
- ausência de PII;
- no-store;
- timezone.

---

## 33. Relatórios e exportações

Testar:

- cada tipo;
- filtros;
- ownership;
- resumo;
- agrupamento;
- paginação;
- mascaramento;
- limite.

CSV:

- BOM;
- cabeçalho;
- acentos;
- filtros;
- CSV injection.

XLSX:

- workbook válido;
- abas;
- cabeçalhos;
- autofiltro;
- freeze panes;
- datas;
- ausência de fórmulas perigosas.

PDF:

- assinatura `%PDF`;
- título;
- filtros;
- resumo;
- múltiplas páginas;
- dados autorizados.

---

## 34. PostgreSQL em CI

A CI deverá usar PostgreSQL, não apenas SQLite.

A versão principal deverá corresponder à versão do Supabase verificada durante a implementação.

A suíte rápida local poderá continuar usando SQLite quando compatível.

---

## 35. Orçamento de queries

Metas iniciais:

```text
Pesquisa/lista: até 5 queries
Detalhes: até 5 queries
Dashboard: até 20 queries
Preview de relatório: até 10 queries
```

Alterações justificadas deverão ser documentadas.

---

# PARTE V — AMBIENTES

## 36. Ambientes obrigatórios

```text
development
test
qa
production
```

### Development

- local;
- `DEBUG=True`;
- dados fictícios;
- Supabase de desenvolvimento;
- Storage de desenvolvimento.

### Test

- banco efêmero;
- sem serviços externos reais;
- configuração determinística.

### QA

- `DEBUG=False`;
- semelhante à produção;
- banco e Storage próprios;
- dados fictícios;
- domínio próprio.

### Production

- dados reais;
- `DEBUG=False`;
- HTTPS;
- banco e Storage exclusivos;
- backups;
- logs;
- monitoramento;
- credenciais próprias.

---

## 37. Settings

Refatorar:

```text
config/settings.py
```

para:

```text
config/settings/base.py
config/settings/development.py
config/settings/test.py
config/settings/qa.py
config/settings/production.py
```

Regras:

- `base.py` sem defaults inseguros;
- ambientes explícitos;
- nenhuma credencial no código;
- `manage.py` poderá usar development localmente;
- WSGI/ASGI usarão `DJANGO_SETTINGS_MODULE`;
- refatoração sem migration.

---

## 38. Variáveis

Mínimas:

```text
APP_ENV
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
DJANGO_CSRF_TRUSTED_ORIGINS
DATABASE_URL
SUPABASE_URL
SUPABASE_SECRET_KEY
SUPABASE_STORAGE_BUCKET
DJANGO_TRUST_PROXY_SSL_HEADER
LOG_LEVEL
REPORT_EXPORT_MAX_ROWS
```

Opcionais:

```text
ERROR_MONITORING_DSN
RELEASE_VERSION
BUILD_SHA
```

Nada será enviado ao frontend.

---

## 39. Arquivos de exemplo

Versionar:

```text
.env.example
.env.development.example
.env.qa.example
.env.production.example
```

Ignorar arquivos reais equivalentes.

Usar somente placeholders.

---

## 40. Isolamento

Cada ambiente persistente terá:

- banco separado;
- credenciais separadas;
- Storage separado;
- bucket separado;
- backups separados.

Proibido:

- QA usar produção;
- development usar produção;
- test usar banco remoto real.

Antes de migrations, confirmar `APP_ENV`, projeto, banco, backup e autorização.

---

## 41. Produção segura

Obrigatório:

- `DEBUG=False`;
- cookies Secure e HttpOnly;
- CSRF seguro;
- HTTPS;
- HSTS;
- allowed hosts restritos;
- trusted origins restritas;
- proxy confiável apenas quando configurado;
- logs sanitizados;
- no-store em páginas sensíveis.

Executar:

```powershell
python backend/manage.py check --deploy --settings=config.settings.production
```

---

# PARTE VI — DEPLOY E OPERAÇÃO

## 42. Estratégia

Baseline provider-neutral com container.

Artefatos:

```text
Dockerfile
.dockerignore
infrastructure/
.github/workflows/
```

O deploy real de produção exige escolha e aprovação de:

- provedor;
- domínio;
- banco;
- Storage;
- secrets;
- backup;
- monitoramento;
- rollback.

---

## 43. Container e servidor

Requisitos:

- build reproduzível;
- dependências fixadas;
- usuário não-root;
- sem `.env` na imagem;
- sem ferramentas desnecessárias;
- logs em stdout/stderr;
- health check;
- Gunicorn ou WSGI equivalente.

Nunca usar `runserver` em QA ou produção.

---

## 44. Arquivos estáticos

Estratégia inicial:

```text
collectstatic + WhiteNoise
```

Requisitos:

- manifest;
- compressão;
- cache para assets versionados;
- falha de `collectstatic` bloqueia deploy;
- arquivos privados continuam no Supabase;
- sem media local persistente.

---

## 45. Health checks

```text
GET /health/live/
GET /health/ready/
```

Liveness:

- processo ativo;
- sem acesso ao banco;
- resposta mínima.

Readiness:

- aplicação pronta;
- conexão read-only com banco;
- timeout;
- sem host, credenciais ou detalhes sensíveis.

---

## 46. CI

Workflow de Pull Request:

1. checkout;
2. Python;
3. dependências;
4. PostgreSQL de serviço;
5. `manage.py check`;
6. dry-run de migrations;
7. migrations no CI;
8. testes;
9. coverage;
10. testes de exports;
11. `check --deploy`;
12. `collectstatic`;
13. build do container;
14. verificação de segredos.

PRs não recebem secrets de produção.

---

## 47. CD

QA:

- após merge em `main`;
- GitHub Environment `qa`;
- secrets de QA;
- migrations controladas;
- smoke tests.

Produção:

- workflow manual ou tag;
- GitHub Environment `production`;
- aprovação manual;
- backup;
- migrate plan;
- migrations;
- deploy;
- smoke test;
- monitoramento;
- rollback disponível.

---

## 48. Migrations em deploy

Fluxo:

```text
backup
→ migrate --plan
→ aprovação
→ migrate
→ verificação
→ aplicação
```

Regras:

- release step separado;
- uma única instância aplica migrations;
- sem `--fake`;
- sem edição de `django_migrations`;
- sem rollback automático de schema;
- mudanças destrutivas exigem plano próprio.

---

## 49. Logs e monitoramento

Logs:

- estruturados;
- request ID;
- release;
- stdout/stderr;
- sem CPF/CNPJ;
- sem telefone/e-mail;
- sem senha/token;
- sem URL assinada;
- sem connection string.

Monitorar:

- uptime;
- latência;
- 5xx;
- banco;
- falhas agregadas de login;
- falhas de exportação;
- memória;
- reinícios;
- health checks;
- backups.

---

## 50. Backups e rollback

Produção:

- backup automatizado;
- retenção documentada;
- backup antes de migration relevante;
- restore testado periodicamente;
- acesso restrito.

Metas iniciais:

```text
RPO: 24 horas
RTO: 4 horas
Disponibilidade: 99,5%
```

Rollback da aplicação usará imagem anterior. Banco será restaurado ou corrigido por plano controlado; não reverter migrations destrutivas automaticamente.

---

## 51. Runbooks

Criar:

```text
docs/OPERATIONS.md
docs/ENVIRONMENTS.md
docs/DEPLOYMENT.md
docs/BACKUP_RESTORE.md
docs/INCIDENT_RESPONSE.md
```

Sem credenciais.

---

# PARTE VII — CORREÇÃO DOCUMENTAL

## 52. README

Corrigir:

- estrutura atual das apps;
- `clientes` já tem modelo e rotas;
- setup concluído;
- migrations aplicadas em desenvolvimento;
- superusuário criado;
- autenticação concluída;
- cadastro concluído;
- Storage privado em uso;
- Fase 3 como etapa atual;
- comandos reais;
- variáveis atuais;
- ambientes e deploy.

Remover afirmações como:

```text
As versões e dependências serão definidas durante o setup.
Os comandos serão adicionados quando o setup estiver concluído.
```

---

## 53. Roadmap

Atualizar para refletir:

```text
Fase 1 concluída
Fase 2 concluída
Fase 3 em execução
```

O roadmap atual não poderá continuar indicando cadastro, superusuário ou setup como pendentes.

---

## 54. Storage

Documentar:

```text
Storage privado no Supabase,
acessado apenas pelo Django,
com URLs assinadas curtas,
após autenticação e ownership.
```

Em documentos históricos que afirmem que Storage não seria usado, adicionar uma seção de atualização de implementação em vez de apagar o histórico.

---

## 55. Outros documentos

Atualizar:

- `backend/README.md`;
- `AGENTS.md` quando necessário;
- árvore do backend;
- comandos;
- ambientes;
- deploy;
- troubleshooting.

Criar:

```text
CHANGELOG.md
fase_final_implementation_report.md
```

O changelog não conterá e-mails, secrets, project refs ou dados de clientes.

---

# PARTE VIII — CRITÉRIOS DE ACEITE

## 56. Pesquisa

Concluída quando:

- todos os campos pesquisáveis funcionarem;
- filtros combinados funcionarem;
- ownership estiver correto;
- admin visualizar todos;
- ordenação segura;
- paginação preservar filtros;
- documento mascarado;
- testes verdes.

---

## 57. Dashboard

Concluído quando:

- rota protegida;
- login direcionar ao dashboard;
- cards corretos;
- filtros corretos;
- rankings e séries corretos;
- ownership correto;
- gráficos acessíveis;
- no-store;
- queries agregadas;
- testes verdes.

---

## 58. Relatórios

Concluídos quando:

- todos os tipos funcionarem;
- filtros e ownership funcionarem;
- CSV, XLSX e PDF forem válidos;
- documentos estiverem mascarados;
- exportação respeitar todos os filtros;
- limite funcionar;
- CSV injection neutralizada;
- arquivos não forem persistidos;
- testes verdes.

---

## 59. Qualidade

Concluída quando:

- suíte completa verde;
- CI com PostgreSQL;
- cobertura mínima de 85%;
- `check` verde;
- dry-run sem mudanças;
- `check --deploy` verde;
- `collectstatic` verde;
- container build verde;
- regressões anteriores verdes.

---

## 60. Ambientes e deploy

Concluídos quando:

- settings separados;
- bancos e Storage separados;
- examples versionados;
- secrets reais ignorados;
- produção segura;
- Docker funcional;
- Gunicorn funcional;
- health checks;
- CI/CD;
- backups;
- rollback;
- logs sanitizados;
- runbooks.

Deploy de produção somente poderá receber `READY FOR PRODUCTION` após QA aprovada, CI verde, domínio, HTTPS, backups, monitoramento e autorização.

---

## 61. Ordem de implementação

1. auditoria e baseline;
2. camada de consulta;
3. pesquisa e filtros;
4. dashboard;
5. relatórios;
6. CSV;
7. XLSX;
8. PDF;
9. expansão dos testes;
10. cobertura;
11. settings por ambiente;
12. container;
13. health checks;
14. CI;
15. CD de QA;
16. preparação de produção;
17. documentação;
18. relatório final.

---

## 62. Dependências previstas

```text
openpyxl
reportlab
gunicorn
whitenoise
coverage
```

Regras:

- confirmar compatibilidade;
- fixar versões;
- separar desenvolvimento e produção;
- não instalar dependência sem uso;
- atualizar requirements e documentação.

---

## 63. Bloqueadores de produção

Interromper deploy real se faltar:

- provedor;
- domínio;
- DNS;
- banco de produção;
- Storage de produção;
- secrets;
- backup;
- monitoramento;
- rollback;
- aprovação;
- CI verde;
- QA aprovada.

Artefatos de deploy poderão ser criados antes disso.

---

## 64. Próximo marco

Ao concluir:

```text
MVP FUNCIONAL E OPERACIONALMENTE PREPARADO
```

Vereditos:

```text
READY FOR QA
READY FOR PRODUCTION
READY WITH RESERVATIONS
NOT READY
```

---

## 65. Conclusão

A fase final será concluída em sete frentes:

```text
Pesquisa
Dashboard
Relatórios
Testes
Ambientes
Deploy
Documentação
```

A arquitetura continuará sendo:

```text
Navegador
→ Django autenticado
→ ownership e regras de negócio
→ Django ORM e serviços backend-only
→ PostgreSQL e Storage privado no Supabase
```
