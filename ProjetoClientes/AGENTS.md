# AGENTS.md

## 1. Finalidade

Este arquivo orienta agentes de desenvolvimento, incluindo Codex e agentes executados no Antigravity, sobre como trabalhar neste repositório.

O projeto deve ser desenvolvido de forma incremental, seguindo a documentação existente em `Blueprint/`.

Os agentes devem tratar o Blueprint como a principal fonte de requisitos, arquitetura funcional, comportamento da interface e modelagem de dados.

---

## 2. Visão Geral do Projeto

O projeto consiste em um sistema web de cadastro e gestão de clientes Pessoa Física e Pessoa Jurídica.

O sistema será utilizado inicialmente por um único usuário e deverá oferecer:

- autenticação;
- dashboard;
- cadastro de clientes;
- edição;
- visualização de detalhes;
- pesquisa;
- filtros;
- ativação e inativação;
- relatórios;
- exportações;
- proteção e privacidade dos dados.

Arquitetura inicial:

```text
Django
├── interface web
├── autenticação
├── regras de negócio
├── validações
├── pesquisa
├── dashboard
├── relatórios
└── acesso ao banco pelo Django ORM

Supabase
└── banco de dados PostgreSQL
```

---

## 3. Tecnologias Previstas

- Python;
- Django;
- PostgreSQL;
- Supabase;
- Django Templates;
- HTML;
- CSS;
- JavaScript;
- Git;
- testes automatizados com as ferramentas do ecossistema Django.

As versões exatas serão definidas durante o setup técnico.

Não introduza frameworks adicionais sem necessidade ou sem decisão explícita.

---

## 4. Fonte de Verdade do Projeto

Antes de implementar ou alterar uma funcionalidade, leia:

1. `Blueprint/00-overview/overview_roadmap_projeto_clientes.md`;
2. o arquivo especializado relacionado à tarefa;
3. `Blueprint/02-modelagem/modelagem_dados_clientes_skill.md`, quando houver impacto em dados;
4. `Blueprint/03-ui-ux/wireframes_navegacao_skill.md`, quando houver impacto visual ou de navegação.

Arquivos especializados:

```text
Blueprint/
├── 00-overview/
│   ├── overview_roadmap_projeto_clientes.md
│   └── relatorio_definicao_projeto_cadastro_clientes.md
├── 01-requisitos/
│   ├── campocadastroskill.md
│   ├── comportamento_dinamico_interface_skill.md
│   ├── dashboard_clientes_skill.md
│   ├── pesquisa_clientes_skill.md
│   └── relatorios_clientes_skill.md
├── 02-modelagem/
│   └── modelagem_dados_clientes_skill.md
└── 03-ui-ux/
    └── wireframes_navegacao_skill.md
```

Em caso de conflito:

1. não invente uma decisão;
2. identifique o conflito;
3. preserve a implementação atual;
4. solicite decisão explícita antes de alterar comportamento relevante.

---

## 5. Regras Fundamentais

### 5.1 Trabalhar de forma incremental

- implemente uma funcionalidade por vez;
- evite alterações amplas e não relacionadas;
- mantenha commits pequenos e objetivos;
- não reestruture todo o projeto sem necessidade.

### 5.2 Não ampliar o escopo

Não implemente funcionalidades fora do MVP sem solicitação explícita.

Exemplos atualmente fora do escopo:

- aplicativo mobile nativo;
- integração com WhatsApp;
- emissão fiscal;
- módulo financeiro;
- CRM completo;
- automações de marketing;
- API pública;
- múltiplos perfis avançados;
- Supabase Auth;
- frontend separado em React ou Next.js.

### 5.3 Não expor segredos

Nunca inclua no código, documentação, logs ou commits:

- senhas;
- `DJANGO_SECRET_KEY`;
- URLs privadas com credenciais;
- chaves do Supabase;
- tokens;
- dados reais de clientes.

Use variáveis de ambiente.

O arquivo `.env` não deve ser versionado.

### 5.4 Não editar o Blueprint silenciosamente

A documentação em `Blueprint/` representa decisões aprovadas.

Não altere esses arquivos durante uma implementação comum.

Quando uma mudança funcional exigir atualização documental:

- informe a necessidade;
- proponha o arquivo afetado;
- altere apenas quando solicitado.

---

## 6. Estrutura Esperada do Repositório

```text
ProjetoClientes/
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── pyproject.toml
├── Blueprint/
├── backend/
├── infrastructure/
├── requirements/
├── scripts/
├── staticfiles/
└── tests/
```

Estrutura prevista para o Django:

```text
backend/
├── manage.py
├── config/
├── apps/
│   ├── clientes/
│   ├── dashboard/
│   └── relatorios/
├── templates/
├── static/
└── media/
```

A estrutura final poderá ser ajustada durante o setup, desde que permaneça simples e coerente.

---

## 7. Convenções de Código

### 7.1 Python

- siga PEP 8;
- use nomes claros;
- evite abreviações obscuras;
- mantenha funções pequenas;
- adicione type hints quando aumentarem a clareza;
- não duplique regras de negócio;
- prefira código explícito a soluções excessivamente abstratas.

### 7.2 Django

- use Django ORM para acesso ao banco;
- use migrations para alterações estruturais;
- não crie ou altere tabelas manualmente no Supabase;
- mantenha regras reutilizáveis em validadores ou serviços;
- use formulários Django para validação de entrada;
- proteja páginas internas com autenticação;
- use `settings.AUTH_USER_MODEL` em relacionamentos;
- evite lógica complexa diretamente nos templates;
- evite views excessivamente grandes.

### 7.3 Templates

- reutilize `base.html`;
- use partials para cabeçalho, menu, mensagens, paginação e modais;
- preserve acessibilidade;
- use HTML semântico;
- não dependa apenas de cor;
- mantenha responsividade;
- evite JavaScript desnecessário.

### 7.4 Banco de Dados

- CPF e CNPJ devem ser armazenados somente com números;
- telefone deve ser armazenado somente com números;
- CEP deve ser armazenado somente com números;
- documento deve ser único;
- PF e PJ devem utilizar a mesma entidade `Cliente`;
- inativação deve ser preferida à exclusão;
- toda alteração estrutural deve possuir migration;
- índices devem seguir a modelagem aprovada.

---

## 8. Regras de Negócio Essenciais

### Cliente

Campos obrigatórios:

- tipo;
- nome;
- documento;
- telefone principal;
- CEP.

Tipo:

- `PF`;
- `PJ`.

Documento:

- CPF para PF;
- CNPJ para PJ;
- obrigatório;
- válido;
- único.

Situação:

- `ATIVO`;
- `INATIVO`;
- novos clientes iniciam como ativos.

Duplicidade:

- CPF ou CNPJ duplicado: bloquear;
- telefone repetido: alertar;
- e-mail repetido: alertar;
- nome semelhante: alertar, sem bloquear.

Privacidade:

- documentos mascarados em listagens e relatórios;
- documento completo apenas em telas autorizadas;
- não expor dados desnecessários no dashboard.

---

## 9. Validação e Normalização

Antes de salvar:

- remover espaços laterais;
- reduzir espaços duplicados;
- converter e-mail para minúsculas;
- remover pontuação de documento;
- remover pontuação de telefone;
- remover pontuação de CEP;
- converter UF para letras maiúsculas.

Validações obrigatórias:

- CPF;
- CNPJ;
- telefone com 10 ou 11 dígitos;
- CEP com 8 dígitos;
- data não futura;
- UF válida;
- nome com conteúdo útil.

A validação deve existir no backend mesmo que também exista na interface.

---

## 10. Interface e Navegação

A interface seguirá arquitetura híbrida:

- dashboard separado;
- pesquisa em tela própria;
- cadastro em tela própria;
- edição reutiliza o formulário;
- detalhes em tela própria;
- relatórios em módulo próprio;
- menu lateral no desktop;
- menu recolhível no mobile;
- breadcrumb;
- tabelas no desktop;
- cartões no mobile.

Consulte:

```text
Blueprint/03-ui-ux/wireframes_navegacao_skill.md
```

Não altere fluxos aprovados sem solicitação.

---

## 11. Testes

Toda funcionalidade relevante deve possuir testes adequados.

Prioridades:

1. modelos;
2. validadores;
3. formulários;
4. autenticação;
5. permissões;
6. views;
7. filtros;
8. relatórios;
9. exportações;
10. fluxos críticos.

Casos mínimos:

- cadastrar PF válido;
- cadastrar PJ válido;
- rejeitar CPF inválido;
- rejeitar CNPJ inválido;
- rejeitar documento duplicado;
- validar telefone;
- validar CEP;
- impedir acesso sem login;
- editar cliente;
- ativar e inativar;
- pesquisar por nome e documento;
- aplicar filtros;
- mascarar documento.

Não considere uma tarefa concluída quando os testes relacionados estiverem falhando.

---

## 12. Qualidade Antes de Concluir uma Tarefa

Antes de informar conclusão:

1. revise o diff;
2. confirme que a alteração atende ao Blueprint;
3. execute testes relevantes;
4. execute lint e formatação quando configurados;
5. confira migrations;
6. verifique se não há segredos;
7. valide comportamento em caso de erro;
8. confira acessibilidade básica;
9. verifique se a alteração não quebrou funcionalidades existentes.

---

## 13. Comandos

Os comandos definitivos serão atualizados após o setup.

Exemplos previstos:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements\development.txt
python backend\manage.py migrate
python backend\manage.py runserver
python backend\manage.py test
```

Não invente comandos de ferramentas ainda não configuradas.

---

## 14. Migrations

Ao modificar models:

1. revise o impacto;
2. crie migration;
3. leia a migration gerada;
4. aplique no ambiente de desenvolvimento;
5. execute testes;
6. não altere migrations já aplicadas em QA ou produção;
7. crie uma nova migration para correções.

Não execute migrations destrutivas sem confirmação explícita.

---

## 15. Ambientes

O projeto terá:

- desenvolvimento;
- QA ou homologação;
- produção.

Cada ambiente deverá possuir:

- banco separado;
- credenciais próprias;
- variáveis próprias;
- configurações apropriadas;
- dados independentes.

Nunca use dados reais de produção em desenvolvimento.

---

## 16. Git

- não versionar `.env`;
- não versionar `.venv`;
- não versionar caches;
- não versionar arquivos gerados;
- não versionar dados reais;
- manter commits focados;
- descrever claramente alterações;
- revisar arquivos antes de commit;
- não fazer force push sem solicitação explícita.

---

## 17. Segurança

- autenticação obrigatória para páginas internas;
- proteção CSRF;
- validação no backend;
- `DEBUG=False` em produção;
- `ALLOWED_HOSTS` configurado;
- HTTPS em produção;
- cookies seguros em produção;
- queries pelo ORM;
- princípio de menor privilégio;
- logs sem dados sensíveis.

---

## 18. Comportamento Esperado do Agente

Ao receber uma tarefa:

1. identificar o módulo envolvido;
2. ler a documentação relevante;
3. inspecionar a implementação atual;
4. propor ou executar a menor alteração necessária;
5. implementar;
6. testar;
7. informar arquivos alterados;
8. informar testes executados;
9. registrar limitações ou decisões pendentes.

O agente não deve:

- assumir requisitos não documentados;
- alterar arquitetura sem necessidade;
- apagar código funcional sem justificativa;
- introduzir dependências sem explicar;
- esconder testes falhando;
- afirmar que algo funciona sem verificar.

---

## 19. Definição de Pronto

Uma tarefa está pronta quando:

- atende ao requisito;
- segue a arquitetura;
- possui validação;
- possui tratamento de erro;
- possui testes relevantes;
- não expõe segredos;
- migrations estão corretas;
- interface está consistente;
- documentação afetada foi identificada;
- o diff está limitado à tarefa.

---

## 20. Prioridade de Implementação

Ordem prevista:

```text
1. Setup do projeto
2. Configuração dos ambientes
3. Autenticação
4. Modelo Cliente
5. Validadores
6. Django Admin
7. Cadastro
8. Detalhes
9. Edição
10. Pesquisa
11. Dashboard
12. Relatórios
13. Exportações
14. Testes integrados
15. QA
16. Produção
```

Trabalhe respeitando essa sequência, salvo decisão explícita em contrário.
