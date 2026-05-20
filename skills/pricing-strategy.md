# Skill: pricing-strategy
**Fonte:** davila7/claude-code-templates + princípios de psicologia de preço adaptados para KDP e Mercado Livre
**Quando carregar:** decisões de precificação de ebooks (KDP), produtos físicos (ML), promoções, lançamentos, reajustes de margem

---

## Princípio Central

Preço não é matemática — é percepção. O mesmo produto a R$9,99 e a R$14,99 é percebido de formas completamente diferentes. A decisão de preço afeta não só a margem mas o posicionamento e o perfil do comprador que você atrai.

---

## Psicologia de Preço

### Charm Pricing (Preço Psicológico)
- R$9,99 performa melhor que R$10,00 para produtos de consumo
- R$14,97 performa melhor que R$15,00
- Exceção: produtos premium — número redondo (R$50, R$97) transmite confiança e qualidade

### Anchoring (Âncora de Preço)
Mostrar um preço mais alto antes do preço real aumenta a percepção de valor.
- "De R$29,90 por R$9,99" — o preço original vira âncora
- No KDP: preço de capa no print vs. ebook cria âncora natural

### Decoy Pricing (Efeito Isca)
Três opções em que a do meio parece a mais racional:
- Básico: R$9,99 (ebook)
- Recomendado: R$19,99 (ebook + guia de meal prep)  
- Premium: R$39,99 (tudo + acesso a grupo)

---

## Precificação para Amazon KDP

### Faixas de Royalty
- **35% de royalty:** preços fora de $2,99–$9,99 (USD)
- **70% de royalty:** preços entre $2,99–$9,99 (USD) — sempre mirar aqui

### Estratégias de Lançamento
1. **Preço de lançamento baixo** (R$4,99–R$7,99): maximizar volume de vendas e reviews nas primeiras semanas → sobe o BSR → orgânico
2. **Preço normal** (R$12,99–R$19,99): após estabelecer ranking e reviews
3. **KDP Select / Countdown Deals:** promoções temporárias para reativar algoritmo

### Posicionamento por Preço
| Preço (USD) | Perfil |
|---|---|
| $0,99 | Impulso, sem resistência, royalty baixo |
| $2,99–$4,99 | Entrada, bom para lançamento |
| $5,99–$9,99 | Mainstream, melhor royalty |
| $9,99+ | Premium, precisa de prova social forte |

### Regra do Nicho
Pesquisar os top 10 do nicho e precificar no meio da faixa. Nunca ser o mais barato sem motivo — transmite baixa qualidade.

---

## Precificação para Mercado Livre

### Estrutura de Custo Obrigatória
Antes de definir preço, calcular:
```
Preço de venda
- Comissão ML (17% Premium / 13% Clássico)
- Frete (drop-off SP ~R$28 | Full ~R$8–12)
- Custo do produto
= Margem líquida
```
Margem mínima viável: 15%. Abaixo disso, rever custo ou preço.

### Estratégia de Buy Box
- Buy Box ML prioriza: preço competitivo + reputação + frete grátis + estoque
- Monitorar concorrentes semanalmente (usar `tools/ml_search.py`)
- Nunca entrar em guerra de preço sem verificar se o concorrente tem Full ativo

### Promoções no ML
- Descontos de 10–15% em datas comemorativas aumentam visibilidade no algoritmo
- Cupons custam menos que baixar o preço permanentemente
- Preço com frete incluído sempre converte melhor que preço + frete à parte

---

## Van Westendorp (Para Produtos Novos)

Quatro perguntas para encontrar a faixa de preço aceitável:
1. A que preço seria **tão barato** que duvidaria da qualidade?
2. A que preço seria **barato mas aceitável**?
3. A que preço seria **caro mas ainda compraria**?
4. A que preço seria **caro demais** e desistiria?

A faixa ideal está entre as respostas 2 e 3.

---

## Sinais de que o Preço Está Errado

- **Muito baixo:** alta conversão, reclamações de qualidade, margem insustentável
- **Muito alto:** baixa conversão, abandono de carrinho, poucos reviews
- **Certo:** conversão estável, reviews positivos, margem saudável
