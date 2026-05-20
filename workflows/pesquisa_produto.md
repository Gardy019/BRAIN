# Workflow: Pesquisa de Produto para Revenda no ML

## Objetivo
Avaliar se um produto X vale a pena comprar para revender no Mercado Livre, antes de imobilizar capital.

## Inputs Necessários
- Nome ou categoria do produto
- Custo de compra estimado (ou fornecedor)
- Capital disponível para o lote

## Passos

### 1. Pesquisa de mercado no ML
- Buscar o produto no ML
- Anotar: preço mínimo, preço médio, preço mais vendido
- Verificar quantos sellers ativos existem
- Verificar reviews e volume de vendas do líder
- Checar se tem "Mais Vendidos" com badge

### 2. Análise de margem
Usar a fórmula:
```
Lucro líquido = Preço venda - Custo - (Preço × 0.16) - Frete - Embalagem
Margem % = Lucro líquido / Preço venda
```
Margem mínima aceitável: **25%**

### 3. Análise de risco
- O produto tem muitos concorrentes com estoque grande? (risco de guerra de preço)
- O produto tem sazonalidade? (risco de encalhe)
- Tem fornecedor confiável com preço estável?
- O produto é frágil ou tem alto risco de devolução?

### 4. Decisão
| Score | Decisão |
|---|---|
| Margem >30%, poucos concorrentes, giro rápido | Comprar |
| Margem 20–30%, concorrência moderada | Testar com lote pequeno |
| Margem <20% ou risco alto | Não comprar |

## Output
Relatório com: preço de venda sugerido, margem estimada, volume de concorrentes, recomendação final.

## Notas
- Sempre pesquisar ANTES de comprar — nunca ao contrário
- Verificar se o preço do fornecedor é sustentável ou promoção pontual
- Monitorar o produto por 1 semana antes de fechar lote grande
