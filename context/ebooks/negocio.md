# Projeto Ebooks

_Última atualização: 2026-05-13_

## Status
Pesquisa de mercado concluída — piloto definido, pronto para produção.

## Modelo
- Plataforma: **Amazon KDP** (publicação independente, royalties 35–70%, mercado global)
- Criação: IA (Claude para conteúdo, Nano Banana para imagens, Canva para layout)
- Idioma: **Inglês** (mercado americano — 10x maior que o brasileiro)
- PLR: descartado (risco de conteúdo duplicado, Amazon penaliza)

## Piloto definido
- **Nicho:** High Protein (Hipertrofia)
- **Título candidato:** *"High Protein Cookbook for Beginners: 50 Easy Recipes with Everyday Ingredients"*
- **Público-alvo:** adultos ocupados, sem experiência culinária, que querem ganhar músculo ou perder peso
- **Ângulo:** ingredientes comuns de supermercado, até 5 ingredientes, menos de 30 min, tom acessível (não sofisticado)
- **Preço médio de mercado:** $18,58 (maior entre os nichos pesquisados)
- **Concorrência:** 100% KDP — sem editoras tradicionais dominando

## Dados de mercado coletados
- Scripts criados em `tools/`:
  - `kdp_amazon_research.py` — scraper de livros Amazon (preço, avaliação, título)
  - `kdp_review_research.py` — scraper de reviews Amazon (bloqueado por anti-bot)
  - `kdp_goodreads_research.py` — scraper Goodreads (poucos reviews nesses livros)
  - `kdp_trends.py` — Google Trends (bloqueio 429, usar com moderação)
- Conclusão: scraping de reviews não é viável diretamente; dados de título/preço são suficientes para decisão

## Padrão de títulos que vendem no KDP
- "5-Ingredient" → simplicidade
- "For Beginners" → público iniciante
- "Quick & Easy" → sem tempo
- "$X/Day" → apelo econômico

## Ferramentas testadas
- **Inkfluence AI** (inkfluenceai.com) — gerou 5 receitas com boa estrutura (plano grátis = 5 chapters)
  - Watermark "Made with Inkfluence AI" no manuscrito — não usar para publicação
  - Estrutura das receitas é boa referência: prep time, dificuldade, ingredientes, instruções, tips, swaps
  - Decisão: não pagar — Claude replica o formato com mais controle e sem watermark
- **Canva** — templates gratuitos compatíveis com KDP (6x9 pol)

## Próximas ações (retomada)
1. Ver print do `ebook.pdf` do Inkfluence para avaliar design visual
2. Decidir: imitar layout do Inkfluence no Canva ou usar outro template
3. Gerar as 50 receitas completas com Claude no formato do manuscrito KDP
4. Criar capa com Nano Banana + Canva
5. Publicar no KDP (disclosure de IA obrigatório)

## Observações importantes
- KDP exige disclosure de uso de IA na publicação
- Preço recomendado para nicho: $9,99–$14,99 (ebook) / $14,99–$19,99 (impresso)
- Royalty KDP: 70% para ebooks entre $2,99–$9,99; 35% fora dessa faixa
