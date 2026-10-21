# Correções — 21/10/2026

## Agendamento
- GitHub Actions alterado para 3 execuções diárias: 08h, 13h e 18h (Natal/Brasília, UTC-3).
- Cron UTC: `0 11,16,21 * * *`.

## Sólides
- Removida a dependência do seletor HTML antigo `li:has(h2 a)`.
- Busca migrada para o endpoint JSON público usado pelo próprio portal: `/api/vacancies`.
- Mantidas até 3 páginas por termo e deduplicação por link.
- Modalidade Remoto/Híbrido/Presencial é preservada para o filtro do JobRadar.

## Indeed
- Adicionado seletor alternativo para a listagem atual.
- Adicionada detecção de sinais de bloqueio/anti-bot.
- Adicionado circuit breaker: se a primeira busca não renderizar no GitHub Actions, os demais termos do ciclo são pulados, evitando vários timeouts consecutivos.
- Observação: o Indeed pode bloquear IPs de datacenter. Sem proxy/serviço externo, não é possível garantir coleta em toda execução; agora a falha é rápida e explícita em vez de consumir vários minutos por termo.

## Saúde das fontes
- Mensagem de alerta passa a distinguir fontes executadas no ciclo de fontes configuradas no perfil.
- Isso evita interpretar `2/4` como se o perfil tivesse somente quatro fontes; fontes de baixa frequência rodam apenas no primeiro ciclo do dia.

## Testes
- Adicionados testes do parser da API da Sólides.
- Corrigido teste antigo do perfil DEV para refletir a configuração atual (remoto somente Brasil; mercados internacionais estão comentados/desativados em `core/config_dev.py`).
- Resultado local: 314 testes aprovados.
