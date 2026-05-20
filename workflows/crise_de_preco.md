# Workflow: Crise de Preço

## Objetivo
Responder de forma estruturada quando um concorrente queima o preço de um produto em estoque, sem precisar escalar para o usuário.

## Gatilho
- Preço médio de mercado cai abaixo do preço de venda atual
- Margem líquida do produto cai abaixo de 15%
- Reclamação ou queda de vendas sem explicação óbvia

## Diagnóstico (executar primeiro)

### 1. Confirmar a queima
- Buscar o produto no ML via MCP
- Comparar preço atual dos top 10 vendedores com o preço registrado em `context/mercado_livre/estoque.md`
- Se a queda for > 20%, confirmar crise de preço

### 2. Identificar a origem
- É um vendedor novo com estoque grande? → guerra de preço temporária
- É o preço médio do mercado todo caindo? → produto com vida útil de margem acabando
- É sazonalidade? → aguardar janela de recuperação

## Respostas Possíveis

### Cenário A — Queima temporária (1–2 sellers despejando estoque)
**Ação:** Manter preço. Monitorar por 7 dias. Se normalizar, sem mudança.

### Cenário B — Novo patamar de preço no mercado
**Ação:** Calcular novo breakeven.
```
Preço mínimo = Custo / (1 - comissão_ML - margem_frete_%) 
```
Se o novo patamar está abaixo do breakeven → liquidar estoque imediatamente.
Se está acima → ajustar preço para o novo patamar e manter.

### Cenário C — Margem zerada, estoque grande
**Ação:** Liquidar. Recuperar capital. Reinvestir em produto novo.
- Baixar preço para 5–10% acima do custo
- Criar promoção relâmpago no ML
- Usar capital recuperado para pesquisa de produto novo (ver `workflows/pesquisa_produto.md`)

## Buscar Diferenciação (antes de liquidar)
Antes de baixar o preço, verificar se existe oportunidade de bundling:
- Existe acessório complementar que justifique preço maior?
- Exemplo TC-90: vender kit com fluido de corte → novo produto, novo posicionamento, margem recuperada
- Buscar fornecedores do complemento antes de decidir liquidar

## Output
Relatório com:
1. Diagnóstico: queima temporária ou novo patamar?
2. Margem atual vs. margem no novo preço
3. Recomendação: segurar / ajustar / liquidar / diferenciar
4. Atualizar `context/mercado_livre/estoque.md` com novo status

## Notas
- Nunca baixar preço por impulso sem rodar o diagnóstico
- Queima de preço do vizinho é diferente de colapso do mercado
- Capital parado tem custo — estoque que não gira precisa de decisão em até 15 dias
