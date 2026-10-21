# Job Radar — atualização 2026-10-21 v2

Pacote de atualização para ser copiado **sobre a raiz do repositório Job Radar**.
Ele contém somente os arquivos alterados e não inclui `data/jobs.db`, `.git`, `.venv` ou caches.

## Alterações

- GitHub Actions: execução 3x/dia — 08h, 13h e 18h em Natal/Brasília (11h, 16h e 21h UTC).
- Desenvolvimento: reforço de PHP/Laravel (`PHP Junior`, `Desenvolvedor Laravel`, `Laravel Junior`, `PHP Laravel`, além dos termos já existentes).
- Suporte: inclusão de ServiceNow (`ServiceNow Developer`, `Analista ServiceNow`, `ServiceNow Administrator`, `ServiceNow Support`, etc.).
- Sólides: removida dependência do seletor antigo de card; busca agora se ancora nos links públicos `/vaga/<id>` e tolera mudanças de h2/h3/li/div.
- Indeed: após duas falhas consecutivas de carregamento/anti-bot, a fonte é interrompida no ciclo para não desperdiçar vários minutos repetindo timeouts.
- Telegram: alerta de saúde deixa explícito que o denominador representa as fontes executadas naquele ciclo (fontes de baixa frequência podem não rodar em todos os ciclos).
- Testes atualizados para os novos cargos e para refletir a configuração atual do perfil DEV (remoto Brasil).

## Validação local

- `python -m py_compile` nos arquivos Python alterados: OK.
- `python -m pytest -q`: 312 testes aprovados.
- O seletor antigo do Sólides não existe mais em `scrapers/solides.py`.

## Observação sobre Indeed

O tratamento evita perda de tempo quando o runner do GitHub é bloqueado. Ele não promete contornar mecanismos anti-bot do Indeed; quando houver bloqueio, a fonte será marcada como problemática e as demais continuarão normalmente.
