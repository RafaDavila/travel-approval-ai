# Política de viagens — demonstração

Versão: 1.0

## Contexto

Esta política é fictícia e foi criada exclusivamente para a prova de
conceito. A política original não foi disponibilizada, e a continuidade
sem esse documento foi autorizada no processo seletivo.

Os limites abaixo são premissas de demonstração e não representam
necessariamente as regras reais da empresa.

## Dados obrigatórios

Toda solicitação deve informar:

- Nome do colaborador.
- Departamento.
- Origem.
- Destino.
- Data e hora de partida, com fuso horário.
- Data e hora de retorno, com fuso horário.
- Orçamento total estimado, em reais (BRL).

## Validação da solicitação

- Os campos de texto não podem estar vazios.
- As datas devem ser válidas e incluir fuso horário.
- O retorno deve ser posterior à partida.
- O orçamento deve ser um número positivo, com até duas casas decimais.

Solicitações inválidas devem retornar um erro de validação,
sem passar pela avaliação de aprovação.

## Regras de aprovação

### POL-001 — Duração máxima

A duração da viagem não pode ultrapassar 15 períodos de 24 horas,
calculados pela diferença entre retorno e partida.

Uma viagem com duração exata de 15 dias é permitida.

### POL-002 — Orçamento máximo

O orçamento total estimado não pode ultrapassar R$ 5.000,00 por viagem.

Um orçamento de exatamente R$ 5.000,00 é permitido.

O valor representa o custo total da viagem, não apenas a passagem.

### POL-003 — Origem e destino

A origem e o destino devem ser diferentes.

A comparação deve ignorar diferenças entre letras maiúsculas e
minúsculas e espaços no início e no fim dos textos.

## Critério de decisão

A solicitação será aprovada somente se cumprir todas as regras.

Quando houver reprovação, a resposta deverá identificar todas as
regras violadas.

As mesmas regras se aplicam a todos os departamentos.
Não há exceções previstas nesta versão da política.