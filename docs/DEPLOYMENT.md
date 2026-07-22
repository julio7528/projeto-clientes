# Deploy

CI valida `check --deploy`, migrations, testes, coverage, `collectstatic` e imagem. QA ocorre após merge com secrets do Environment `qa`. Produção é manual, com Environment protegido, backup, `migrate --plan`, aprovação e smoke test. Não há deploy real configurado neste repositório.
