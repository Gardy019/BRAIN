# Workflow: Auto-Check COO

## Objetivo
Revisão rápida do estado do negócio. Executar no início de cada semana ou sob demanda.

## Inputs
- context/negocio.md
- context/estoque.md
- context/financeiro.md

## Perguntas do Auto-Check

1. **O que está travado ou em risco?**
   - Estoque parado há mais de 15 dias
   - Margem de algum produto abaixo de 20%
   - Capital imobilizado acima de 60% do total disponível

2. **Qual ação gera mais caixa nas próximas 48h?**
   - Produto com maior estoque × margem atual
   - Possibilidade de promoção relâmpago no ML

3. **O que pode ser delegado ao agente agora?**
   - Pesquisa de produto novo
   - Cálculo de precificação
   - Análise de concorrência no ML

## Output
Resposta direta às 3 perguntas acima, com números reais do contexto.
