---
name: fase-final-pesquisa-dashboard-relatorios-operacao
description: Implementa pesquisa e filtros, dashboard, relatórios e exportações, testes completos, separação de ambientes, CI/CD, deploy, observabilidade e correção documental do projeto PC-DJANGO-001.
---

# Skill — Fase Final: Pesquisa, Dashboard, Relatórios, Qualidade e Operação
## Projeto PC-DJANGO-001

## 1. Finalidade

Esta skill orienta agentes de desenvolvimento na execução da Fase 3 do projeto PC-DJANGO-001:

```text
3.1 — Pesquisa e filtros de clientes
3.2 — Dashboard de clientes
3.3 — Relatórios e exportações
3.4 — Testes completos e qualidade
3.5 — Separação de ambientes
3.6 — Deploy, observabilidade e operação
3.7 — Correção documental e preparação da release
```

O objetivo é concluir o MVP funcional, preparar QA e produção e deixar o projeto operacionalmente documentado.

---

## 2. Quando usar

Use esta skill quando a tarefa envolver:

- busca e filtros de clientes;
- ordenação e paginação;
- preservação de filtros;
- dashboard;
- agregações;
- indicadores;
- gráficos;
- rankings geográficos;
- relatórios;
- exportação CSV;
- exportação XLSX;
- exportação PDF;
- cobertura de testes;
- PostgreSQL em CI;
- settings por ambiente;
- Docker;
- Gunicorn;
- WhiteNoise;
- health checks;
- CI/CD;
- backups;
- monitoramento;
- logs;
- runbooks;
- atualização de README;
- preparação de QA;
- preparação de produção.

---

## 3. Fontes de verdade

Antes de alterar código, leia nesta ordem:

1. `AGENTS.md`;
2. `README.md`;
3. `backend/README.md`;
4. `Blueprint/01-requisitos/pesquisa_clientes_skill.md`;
5. `Blueprint/01-requisitos/dashboard_clientes_skill.md`;
6. `Blueprint/01-requisitos/relatorios_clientes_skill.md`;
7. `Blueprint/03-ui-ux/wireframes_navegacao_skill.md`;
8. especificação técnica da fase final;
9. relatórios das fases anteriores;
10. código atual de `config`, `core`, `usuarios` e `clientes`;
11. migrations existentes;
12. requirements;
13. estado atual do Git;
14. workflows existentes;
15. documentação operacional existente.

Em caso de conflito:

```text
Especificação aprovada da fase final
→ AGENTS.md
→ Blueprint
→ README.md
→ código atual
```

Não invente funcionalidades fora do escopo.

---

## 4. Marco atual esperado

Considere como baseline:

```text
Fase 1 concluída
Fase 2 concluída
Fase 3 próxima
```

O projeto já deve possuir:

- Django;
- PostgreSQL no Supabase;
- Storage privado backend-only;
- usuário customizado;
- login por e-mail;
- sessões;
- apps modulares;
- modelo Cliente;
- validadores;
- migrations aplicadas em desenvolvimento;
- superusuário de desenvolvimento;
- cadastro;
- lista inicial;
- detalhes;
- edição;
- ativação;
- inativação;
- ownership;
- testes das fases anteriores.

Se o repositório divergir, registre antes de implementar.

---

## 5. Decisões obrigatórias

A implementação deve respeitar:

1. Pesquisa permanece em `clientes`.
2. Dashboard será app própria: `dashboard`.
3. Relatórios serão app própria: `relatorios`.
4. `clientes` fornecerá consulta reutilizável.
5. Usuário comum acessa somente próprios dados.
6. Administrador acessa todos.
7. Filtros são validados no backend.
8. Documentos ficam mascarados em listas, dashboard, relatórios e exports.
9. Documento completo não será exportado no MVP.
10. Exportações são geradas sob demanda.
11. Exportações não são persistidas.
12. Exportações possuem limite configurável.
13. Dashboard usa agregações no banco.
14. Gráficos não substituem valores textuais.
15. Não usar Realtime.
16. Não usar Supabase Auth.
17. Não criar API pública.
18. Não criar multiempresa.
19. Development, QA e production usam bancos e Storage distintos.
20. Produção exige aprovação manual.
21. Produção exige backup.
22. Logs não contêm PII.
23. Secrets não vão ao frontend.
24. README deve refletir o estado real.
25. Não mover `ProtectedFile` nesta fase.
26. Não criar app `arquivos` sem decisão separada.
27. Não fazer commit ou push automaticamente.
28. Não executar deploy real sem autorização.
29. Não aplicar migrations em produção sem gate.
30. Não ampliar escopo silenciosamente.

---

# PARTE I — PESQUISA E FILTROS

## 6. Estrutura esperada

Criar ou completar:

```text
clientes/
├── filters.py
├── querying.py
├── views.py
├── urls.py
├── templates/clientes/
└── tests/
```

Não duplicar regras entre pesquisa, dashboard e relatórios.

---

## 7. Formulário de pesquisa

Criar:

```text
clientes.filters.ClienteSearchForm
```

Campos:

```text
q
tipo
situacao
cidade
estado
criado_de
criado_ate
atualizado_de
atualizado_ate
ordenar
direcao
```

Regras:

- todos os filtros usam GET;
- filtros vazios não restringem;
- datas devem ser coerentes;
- valores inválidos não chegam diretamente ao ORM;
- ordenação usa allowlist;
- ownership nunca é alterado por parâmetros.

---

## 8. Busca geral

O campo `q` deve pesquisar:

- nome;
- documento;
- telefone;
- e-mail.

Regras:

- nome parcial e case-insensitive;
- documento com ou sem máscara;
- telefone com ou sem máscara;
- e-mail em minúsculas;
- espaços duplicados normalizados;
- documento e telefone preferencialmente exatos;
- tamanho máximo do termo;
- sem busca automática por caractere no MVP.

---

## 9. Camada de consulta

Criar em `clientes.querying`:

```text
ClienteFilterSpec
apply_cliente_filters()
apply_cliente_ordering()
```

A camada deve:

- receber valores já validados;
- trabalhar sobre queryset autorizado;
- não conhecer request;
- não aplicar ownership;
- ser reutilizável por pesquisa, dashboard e relatórios;
- evitar duplicação de filtros.

---

## 10. Ownership

A ordem obrigatória é:

```text
queryset autorizado
→ filtros
→ ordenação
→ paginação
```

Exemplo:

```python
queryset = scope_owned_queryset(
    Cliente.objects.all(),
    request.user,
    owner_field="criado_por",
)
```

Nunca filtre o queryset global antes de aplicar ownership.

---

## 11. Filtros

Implementar:

- tipo;
- situação;
- cidade;
- estado;
- período de criação;
- período de atualização.

Regras:

- lógica AND entre filtros;
- cidade case-insensitive;
- UF validada;
- início não pode ser posterior ao fim;
- fim inclui o dia completo;
- datas inválidas exibem erro.

---

## 12. Estado inicial

Sem parâmetros:

```text
somente ativos
nome crescente
20 por página
```

O usuário poderá selecionar explicitamente Todos para incluir inativos.

---

## 13. Ordenação

Allowlist:

```text
nome
criado_em
atualizado_em
cidade
situacao
```

Direção:

```text
asc
desc
```

Nunca usar diretamente no ORM um campo enviado pelo usuário.

---

## 14. Paginação

Configuração inicial:

```text
20 registros por página
```

Preservar:

- busca;
- filtros;
- ordenação;
- página.

Exibir quantidade total e intervalo atual.

---

## 15. Privacidade

Na lista:

```text
CPF: ***.456.789-**
CNPJ: **.345.678/0001-**
```

Não inserir PII desnecessária em:

- atributos HTML;
- query strings;
- logs;
- elementos ocultos;
- scripts.

---

## 16. Estados da tela

Sem registros:

```text
Nenhum cliente cadastrado.
```

Sem resultados:

```text
Nenhum cliente encontrado com os critérios informados.
```

Oferecer:

- limpar filtros;
- cadastrar novo cliente;
- voltar à visão padrão.

---

# PARTE II — DASHBOARD

## 17. App

Criar:

```text
backend/dashboard/
```

Namespace:

```text
dashboard
```

Rota:

```text
GET /dashboard/
dashboard:index
```

Depois da implementação, o login deve redirecionar por padrão para `dashboard:index`.

---

## 18. Filtros do dashboard

Criar:

```text
DashboardFilterForm
```

Campos:

```text
periodo
data_inicial
data_final
tipo
situacao
estado
cidade
```

Períodos:

- hoje;
- últimos 7 dias;
- últimos 30 dias;
- mês atual;
- ano atual;
- personalizado;
- todos.

---

## 19. Indicadores

Implementar:

1. total;
2. PF;
3. PJ;
4. ativos;
5. inativos;
6. novos no período;
7. incompletos.

Cadastro incompleto:

- sem e-mail;
- sem data de referência;
- sem logradouro;
- sem número;
- sem bairro;
- sem cidade;
- sem estado.

Não considerar complemento.

---

## 20. Gráficos e rankings

Implementar:

- PF/PJ;
- ativos/inativos;
- novos clientes no tempo;
- top 10 estados;
- top 10 cidades.

Usar agregações no banco.

Não carregar todos os clientes em memória.

---

## 21. Tabelas resumidas

Exibir:

- 5 criados recentemente;
- 5 atualizados recentemente;
- 5 incompletos prioritários.

Exibir somente:

- nome;
- tipo;
- cidade/UF;
- data;
- ação.

---

## 22. Serviço

Criar:

```text
dashboard.services.DashboardService
```

Responsabilidades:

- receber queryset autorizado;
- aplicar filtros;
- calcular indicadores;
- calcular séries;
- limitar rankings;
- retornar dados estruturados;
- evitar queries ocultas no template.

---

## 23. Gráficos seguros

Regras:

- backend calcula dados;
- usar `json_script` ou equivalente;
- sem JSON interpolado manualmente;
- biblioteca local;
- sem CDN em produção;
- sem envio a terceiros;
- alternativa textual;
- acessível;
- sem PII.

---

## 24. Segurança

Dashboard deve:

- exigir login;
- respeitar ownership;
- usar no-store;
- não exibir documento;
- não exibir endereço completo;
- não exibir observações;
- não registrar PII;
- validar filtros.

---

# PARTE III — RELATÓRIOS

## 25. App

Criar:

```text
backend/relatorios/
```

Namespace:

```text
relatorios
```

Rotas:

```text
/relatorios/
/relatorios/clientes/
/relatorios/clientes/exportar/csv/
/relatorios/clientes/exportar/xlsx/
/relatorios/clientes/exportar/pdf/
```

---

## 26. Tipos

Implementar:

1. geral;
2. por tipo;
3. por situação;
4. geográfico;
5. cadastros por período;
6. atualizações por período;
7. incompletos.

---

## 27. Filtros

Criar:

```text
RelatorioClienteFilterForm
```

Campos:

```text
tipo_relatorio
q
tipo
situacao
cidade
estado
criado_de
criado_ate
atualizado_de
atualizado_ate
campo_presente
campo_ausente
ordenar
direcao
```

Reutilizar `clientes.querying`.

---

## 28. Visualização

Relatórios detalhados:

- tabela;
- resumo;
- paginação de 50;
- filtros preservados.

Relatórios consolidados:

- totais;
- percentuais;
- agrupamentos;
- gráfico opcional.

---

## 29. Privacidade

Em tela e exports:

- documento mascarado;
- observações fora do relatório padrão;
- endereço completo fora do padrão;
- autoria não exportada;
- documento completo fora do MVP.

Não permitir parâmetro para remover mascaramento.

---

## 30. Limite

Variável:

```text
REPORT_EXPORT_MAX_ROWS
```

Padrão:

```text
10000
```

Regras:

- contar antes;
- bloquear acima do limite;
- não truncar;
- pedir filtros mais específicos;
- não implementar job assíncrono.

---

## 31. CSV

Usar `csv`.

Requisitos:

- UTF-8 com BOM;
- cabeçalhos;
- separador compatível;
- acentos;
- datas;
- documento mascarado;
- todos os registros filtrados;
- no-store;
- filename seguro.

Neutralizar valores iniciados por:

```text
= + - @
```

---

## 32. XLSX

Usar `openpyxl`.

Requisitos:

- aba Dados;
- aba Resumo;
- cabeçalhos;
- autofiltro;
- freeze panes;
- datas;
- largura controlada;
- sem fórmulas perigosas;
- documento mascarado;
- geração em memória;
- no-store.

---

## 33. PDF

Usar `ReportLab`, salvo justificativa aprovada.

Requisitos:

- título;
- data/hora;
- filtros;
- resumo;
- tabela;
- cabeçalho repetido;
- páginas numeradas;
- acentos;
- documento mascarado;
- nenhum recurso remoto;
- geração em memória;
- no-store.

---

## 34. Exporters

Criar:

```text
relatorios/exporters/csv.py
relatorios/exporters/xlsx.py
relatorios/exporters/pdf.py
```

Exporters:

- recebem dados prontos;
- não acessam request;
- não consultam banco;
- não persistem arquivo.

---

## 35. Fluxo de exportação

```text
autenticar
→ validar filtros
→ aplicar ownership
→ aplicar filtros
→ validar limite
→ montar dados
→ gerar arquivo
→ retornar resposta
```

---

# PARTE IV — TESTES

## 36. Cobertura

Adicionar coverage.

Meta:

```text
85% de linhas do backend
```

A CI falha abaixo da meta.

Migrations podem ser omitidas.

---

## 37. Pesquisa

Testar:

- login;
- ownership;
- admin;
- todos os campos;
- filtros combinados;
- datas;
- ordenação;
- paginação;
- query string;
- mascaramento;
- estados vazios.

---

## 38. Dashboard

Testar:

- autenticação;
- ownership;
- indicadores;
- filtros;
- incompletos;
- rankings;
- séries;
- recentes;
- base vazia;
- no-store;
- JSON seguro;
- ausência de PII;
- timezone.

---

## 39. Relatórios

Testar:

- tipos;
- filtros;
- ownership;
- agrupamentos;
- resumos;
- paginação;
- mascaramento;
- limite;
- no-store.

---

## 40. CSV

Testar:

- content type;
- filename;
- BOM;
- cabeçalho;
- acentos;
- filtros;
- ownership;
- documento mascarado;
- CSV injection;
- limite.

---

## 41. XLSX

Testar:

- workbook válido;
- abas;
- cabeçalhos;
- autofiltro;
- freeze panes;
- datas;
- mascaramento;
- filtros;
- ownership;
- ausência de fórmulas perigosas.

---

## 42. PDF

Testar:

- `%PDF`;
- content type;
- filename;
- título;
- filtros;
- resumo;
- paginação;
- mascaramento;
- ownership;
- limite.

---

## 43. PostgreSQL em CI

A CI deve usar PostgreSQL.

A versão deve corresponder ao Supabase verificado na implementação.

SQLite pode continuar apenas para suíte local rápida.

---

## 44. Orçamento de queries

Metas:

```text
lista: até 5
detalhes: até 5
dashboard: até 20
relatório: até 10
```

Documentar exceções justificadas.

---

# PARTE V — AMBIENTES

## 45. Settings

Refatorar para:

```text
config/settings/base.py
config/settings/development.py
config/settings/test.py
config/settings/qa.py
config/settings/production.py
```

Regras:

- sem defaults inseguros;
- sem credenciais;
- ambientes explícitos;
- test isolado;
- sem migration.

---

## 46. Ambientes

### Development

- `DEBUG=True`;
- dados fictícios;
- Supabase de desenvolvimento.

### Test

- banco efêmero;
- sem serviços reais.

### QA

- `DEBUG=False`;
- banco e Storage próprios;
- dados fictícios;
- semelhante à produção.

### Production

- `DEBUG=False`;
- banco e Storage exclusivos;
- HTTPS;
- backups;
- monitoramento;
- secrets próprios.

---

## 47. Variáveis

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

---

## 48. Examples

Versionar:

```text
.env.example
.env.development.example
.env.qa.example
.env.production.example
```

Ignorar envs reais.

---

## 49. Segurança de produção

Obrigatório:

```text
DEBUG=False
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SECURE_SSL_REDIRECT=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY
```

Configurar também HSTS, allowed hosts, trusted origins e proxy confiável.

Executar:

```powershell
python backend/manage.py check --deploy --settings=config.settings.production
```

---

# PARTE VI — DEPLOY

## 50. Container

Criar:

```text
Dockerfile
.dockerignore
```

Requisitos:

- build reproduzível;
- usuário não-root;
- dependências fixadas;
- sem `.env`;
- sem Git na imagem final;
- logs stdout/stderr;
- health check;
- processo WSGI.

---

## 51. Servidor

Usar:

```text
Gunicorn
```

Nunca usar `runserver` em QA ou produção.

---

## 52. Static

Estratégia:

```text
collectstatic + WhiteNoise
```

Requisitos:

- manifest;
- compressão;
- cache;
- falha bloqueia deploy;
- private Storage permanece no Supabase.

---

## 53. Health checks

Criar:

```text
/health/live/
/health/ready/
```

Liveness:

- sem banco;
- resposta mínima.

Readiness:

- conexão read-only com banco;
- timeout;
- sem detalhes sensíveis.

---

## 54. CI

Workflow de PR:

1. checkout;
2. Python;
3. dependências;
4. PostgreSQL;
5. `check`;
6. dry-run;
7. migrate;
8. testes;
9. coverage;
10. exports;
11. `check --deploy`;
12. `collectstatic`;
13. build Docker;
14. secret scan.

Sem secrets de produção em PR.

---

## 55. CD

QA:

- após merge;
- environment `qa`;
- secrets de QA;
- migrations controladas;
- smoke tests.

Produção:

- workflow manual ou tag;
- environment `production`;
- aprovação;
- backup;
- migrate plan;
- migrate;
- deploy;
- smoke test;
- monitoramento;
- rollback.

---

## 56. Migrations no deploy

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
- uma instância aplica;
- sem fake;
- sem edição de histórico;
- sem rollback automático de schema.

---

## 57. Logs

Logs devem ser:

- estruturados;
- com request ID;
- com release;
- sem CPF/CNPJ;
- sem telefone/e-mail;
- sem senha/token;
- sem connection string;
- sem URL assinada.

---

## 58. Monitoramento

Monitorar:

- disponibilidade;
- latência;
- 5xx;
- banco;
- exportações;
- memória;
- reinícios;
- health checks;
- backups.

---

## 59. Backups e rollback

Produção exige:

- backup automatizado;
- retenção;
- backup antes de migration relevante;
- restore testado;
- acesso restrito.

Metas iniciais:

```text
RPO 24h
RTO 4h
Disponibilidade 99,5%
```

---

## 60. Runbooks

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

# PARTE VII — DOCUMENTAÇÃO

## 61. README

Corrigir:

- estrutura atual;
- Cliente já existe;
- rotas já existem;
- setup concluído;
- migrations aplicadas;
- superusuário criado;
- autenticação concluída;
- cadastro concluído;
- Storage em uso;
- Fase 3 atual;
- comandos reais;
- ambientes;
- deploy.

Remover texto obsoleto sobre setup futuro.

---

## 62. Roadmap

Atualizar:

```text
Fase 1 concluída
Fase 2 concluída
Fase 3 em execução
```

Não manter cadastro, setup ou superusuário como pendentes.

---

## 63. Storage

Documentar:

```text
Storage privado no Supabase,
acessado somente pelo Django,
com URLs assinadas curtas,
após autenticação e ownership.
```

Em documentos históricos, adicionar atualização sem apagar o histórico.

---

## 64. Outros documentos

Atualizar:

- `backend/README.md`;
- `AGENTS.md`, quando necessário;
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

---

# PARTE VIII — ORDEM DE EXECUÇÃO

## 65. Sequência obrigatória

1. auditoria;
2. baseline de testes;
3. camada de consulta;
4. pesquisa;
5. dashboard;
6. relatórios;
7. CSV;
8. XLSX;
9. PDF;
10. expansão dos testes;
11. coverage;
12. PostgreSQL em CI;
13. settings por ambiente;
14. examples;
15. Docker;
16. Gunicorn;
17. WhiteNoise;
18. health checks;
19. CI;
20. CD de QA;
21. preparação de produção;
22. logs;
23. monitoramento;
24. backups;
25. runbooks;
26. README;
27. changelog;
28. relatório final.

---

## 66. Comandos mínimos

```powershell
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python backend/manage.py test
python backend/manage.py check --deploy --settings=config.settings.production
python backend/manage.py collectstatic --noinput --settings=config.settings.production
```

Também:

```text
coverage run
coverage report
docker build
```

---

## 67. Dependências previstas

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
- separar dev e produção;
- não instalar sem uso;
- atualizar requirements;
- atualizar documentação.

---

## 68. Critérios de aceite

### Pesquisa

- busca e filtros completos;
- ownership;
- ordenação segura;
- paginação;
- mascaramento;
- testes verdes.

### Dashboard

- indicadores corretos;
- filtros;
- rankings;
- séries;
- ownership;
- acessibilidade;
- no-store;
- testes verdes.

### Relatórios

- tipos;
- filtros;
- ownership;
- CSV;
- XLSX;
- PDF;
- limite;
- mascaramento;
- testes verdes.

### Qualidade

- suíte verde;
- coverage >= 85%;
- PostgreSQL em CI;
- dry-run limpo;
- deploy check;
- collectstatic;
- Docker build.

### Ambientes

- settings separados;
- bancos separados;
- Storage separado;
- secrets separados;
- examples;
- produção segura.

### Deploy

- container;
- Gunicorn;
- static;
- health;
- CI/CD;
- backups;
- rollback;
- logs;
- monitoramento;
- runbooks.

### Documentação

- README correto;
- roadmap correto;
- Storage correto;
- fase atual correta;
- nenhum segredo.

---

## 69. Bloqueadores de produção

Interromper deploy real quando faltar:

- provedor;
- domínio;
- DNS;
- banco de produção;
- Storage de produção;
- secrets;
- backup;
- monitoramento;
- rollback;
- autorização;
- QA;
- CI verde.

Artefatos de deploy podem ser preparados antes.

---

## 70. Restrições do agente

O agente deve:

- trabalhar incrementalmente;
- preservar comportamento existente;
- não expor `.env`;
- não imprimir secrets;
- não registrar PII;
- não fazer commit;
- não fazer push;
- não executar deploy real;
- não aplicar production migrations sem autorização;
- não alterar Blueprint silenciosamente;
- não mover `ProtectedFile`;
- não criar app `arquivos`;
- não ampliar escopo;
- interromper em ambiguidade operacional.

---

## 71. Saída esperada

Ao concluir, apresentar:

1. subetapas concluídas;
2. apps criadas;
3. arquivos alterados;
4. filtros implementados;
5. dashboard;
6. relatórios;
7. exports;
8. testes;
9. cobertura;
10. settings;
11. CI;
12. CD;
13. container;
14. health checks;
15. documentação;
16. migrations;
17. resultados;
18. bloqueadores;
19. riscos;
20. ações manuais;
21. próximo marco;
22. veredito:
   - `READY FOR QA`;
   - `READY FOR PRODUCTION`;
   - `READY WITH RESERVATIONS`;
   - `NOT READY`.

---

## 72. Próximo marco

Ao concluir esta skill:

```text
MVP FUNCIONAL E OPERACIONALMENTE PREPARADO
```

Produção somente poderá receber `READY FOR PRODUCTION` após QA aprovada, CI verde, backups verificados, domínio, HTTPS, monitoramento e autorização.
