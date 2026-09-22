# Resultados de validação

## Testes automatizados

34 testes passaram, cobrindo validação de entrada, regras de negócio,
decisões da API, divergência entre avaliações, regras duplicadas e timeout.

As chamadas ao LLM são simuladas nos testes da API.
Esses testes não medem a precisão do modelo real.

Foram observados três avisos de descontinuação em dependências,
sem falhas nos testes.

## Avaliações reais

Modelo configurado: gemini-3.6-flash.

| Cenário | Resultado observado |
|---|---|
| Orçamento de R$ 6.000, demais regras atendidas | Reprovado por POL-002 |
| Viagem dentro da política | Aprovada |
| Exatamente 15 dias e R$ 5.000 | Aprovada |
| Todas as regras violadas | Falha de avaliação na primeira tentativa; reprovação por POL-001, POL-002 e POL-003 na repetição |

A causa da falha inicial no último cenário não foi identificada.
Antes da repetição, foram adicionados logs da categoria da exceção,
sem alterar a lógica de avaliação.

## Limitações

As avaliações reais constituem uma amostra pequena e manual.
Não demonstram precisão geral nem disponibilidade garantida do modelo.

A solução depende da API externa. Falhas ou divergências impedem
a emissão de uma decisão e resultam em HTTP 503.