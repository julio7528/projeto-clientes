# Operação

Health: `/health/live/` não acessa banco; `/health/ready/` executa `SELECT 1`. Logs devem conter apenas request ID, release, status e latência; nunca PII, secrets, tokens, URLs assinadas ou conteúdo de exportação. Metas: RPO 24h, RTO 4h, disponibilidade 99,5%.
