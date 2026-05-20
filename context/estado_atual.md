# Estado Atual — Ponto de Retomada

_Última atualização: 2026-05-20 (sessão MEI + monitoramento email)_

## Sessão 2026-05-20 — Mercado Livre

- CCMEI lido e salvo em `context/pessoal/mei.md` — CNPJ 64.224.046/0001-77 ATIVO
- Conta Mercado Pago migrada para MEI (aguardando confirmação por email em até 24h)
- Monitoramento automático ativo: tarefa `monitorar-email-mercadopago-mei` rodando a cada 3h via Claude scheduled tasks

**Próximo passo ML:** aguardar email do Mercado Pago → vincular Mercado Envios Full

---

## O que foi feito nessa sessão

### CMO Mode — Estratégia Completa ✅

**Pricing decidido:**
- Lançamento: $2.99 USD (70% royalty, max BSR velocity)
- Após 20 reviews: $4.99
- Consolidado 50+ reviews: $6.99
- KDP Select ativo desde dia 1, Free Promotion na semana 2

**Nível de Consciência: Nível 2 — Consciente do Problema**
- Sabe que precisa de mais proteína
- Não tem sistema sustentável
- Hook: "You already know you need more protein. The problem is it gets boring by week two."

**Título refinado:**
- Main: "High Protein Cookbook for Beginners" (SEO intocado)
- Subtítulo: "50 Quick Recipes to Hit 130g Protein Daily — Without Eating Chicken & Eggs Every Single Day"

### Infra de Geração Visual ✅

**tools/generate_cover_html.py** — v2, subtítulo CMO integrado, Playfair+DM Sans
**tools/generate_cover_final.py** — v2 com foto real embutida em base64
**tools/generate_recipe_page.py** — template de receita, slide escorregadio, 2 colunas
**tools/generate_book_assets.py** — gerador de imagens:
  - Provider 1: Pollinations.ai (gratuito, sem API key, funciona agora)
  - Provider 2: Gemini Image Generation (requer GEMINI_API_KEY no .env)
  - Auto-integração: gera foto → injeta no cover → gera PDF final

**Capa final gerada:** `.tmp/cover_html.pdf` — foto overhead bowl quinoa+frango, tipografia editorial, manifesto Honest Kitchen completo

**Template de receita gerado:** `.tmp/recipe_demo.pdf` — Lemon Herb Chicken & Quinoa Bowl, stats bar, grid 2 colunas, PRO TIP block

## Próximas ações ao retornar

### Ebook (próximo passo imediato)
1. **Gerar foto alternativa** (opcional): `python tools/generate_book_assets.py --asset cover_alt`
2. **Montar o ebook completo**: script que itera as 50 receitas do `recipes_high_protein.md` e gera um PDF por receita usando `generate_recipe_page.py`
3. **Merge dos PDFs**: capa + intro + 50 receitas + índice → PDF final KDP
4. **Descrição do livro**: usar `skills/marketing-copywriting.md` + hook CMO para escrever a Amazon listing
5. **Upload KDP**: kdp.amazon.com → manuscrito + capa

### Se quiser chave Gemini (imagens melhores):
1. Acessar https://aistudio.google.com/app/apikey
2. Adicionar `GEMINI_API_KEY=sua_chave` no `.env`
3. Rodar: `python tools/generate_book_assets.py --asset cover --provider gemini`

### Mercado Livre
- Aguardar liberação CNPJ (~3-7 dias a partir de 2026-05-13)
- Vincular no Mercado Pago → Dados fiscais
- Solicitar Mercado Envios Full novamente

## Arquivos criados/modificados nessa sessão
- `tools/generate_cover_html.py` — v2 com copy CMO
- `tools/generate_cover_final.py` — versão com foto real embutida (auto-gerado)
- `tools/generate_recipe_page.py` — template de receita modular
- `tools/generate_book_assets.py` — gerador de imagens multi-provider
- `.tmp/cover_html.pdf` — capa final com foto IA + tipografia editorial
- `.tmp/cover.jpg` — foto gerada via Pollinations.ai (proprietária)
- `.tmp/recipe_demo.pdf` — preview do template de receita

## Infraestrutura disponível
- `tools/ml_search.py` — busca ML via Playwright
- `tools/kdp_amazon_research.py` — pesquisa Amazon KDP
- `tools/generate_book_assets.py` — geração de imagens (Pollinations/Gemini)
- `tools/generate_cover_final.py` — capa com foto real
- `tools/generate_recipe_page.py` — páginas de receita
- `skills/` — 6 skills carregadas conforme contexto
- `.env` — credenciais ML API
- `pymupdf`, `playwright`, `python-pptx`, `reportlab` — todos instalados
