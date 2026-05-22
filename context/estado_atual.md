# Estado Atual — Ponto de Retomada

_Última atualização: 2026-05-22 (sessão capa + recipe page + estrutura BRAIN)_

---

## Próximo passo IMEDIATO ao retornar

### Escolher a capa do ebook

4 candidatas foram geradas com o briefing correto (Verde Floresta + salmão + hook completo).
O usuário não conseguiu visualizar os thumbnails na última sessão.

**Ao retornar:** pedir ao usuário para abrir as URLs abaixo no browser e escolher uma:
- [Capa A](https://www.canva.com/d/WV5WtXHRBleHJN1)
- [Capa B](https://www.canva.com/d/K0ifl-NmPav8N_G)
- [Capa C](https://www.canva.com/d/iU8ZvuqMjfPQa7N)
- [Capa D](https://www.canva.com/d/lniIYfguoog67Yo)

**Job ID e Candidate IDs salvos em:** `context/ebooks/prompts_capa.md`

Após a escolha: usar `create-design-from-candidate` com o job_id e candidate_id para converter em design editável no Canva, depois exportar como PDF KDP.

---

## Estado do Projeto Ebook (High Protein Cookbook)

### Decisões estratégicas confirmadas ✅
- **Título:** "High Protein Cookbook for Beginners"
- **Subtítulo:** "50 Quick Recipes to Hit 130g Protein Daily — Without Eating Chicken & Eggs Every Single Day"
- **Pricing:** $2.99 lançamento → $4.99 (20 reviews) → $6.99 (50+ reviews)
- **50 receitas prontas** em `.tmp/recipes_high_protein.md` — 66% sem frango/ovo

### Design ✅
- Briefing completo em `context/ebooks/design_kdp_cookbook.md`
- Paleta: Verde Floresta `#1B3B2B` + Off-White `#FAF9F5` + Ouro `#C5A059`
- Hero image: salmão — **NUNCA frango ou ovo na capa**
- Theme engine: `themes/high-protein-cookbook.json`

### Páginas de receita ✅ PRONTO
- Script: `tools/generate_recipe_page.py` — funcional, theme-driven, sem hardcode
- Layout: flexbox (não absolute), KDP 600×900px (proporção 1:1.5)
- Tipografia: Playfair Display + Lato, fontes ≥ 9px
- Campo `blurb` opcional por receita
- Demo testado: Greek Yogurt Power Bowl → `.tmp/recipe_demo.pdf`
- **Pendente:** batch generator para as 50 receitas (decidir: 50 PDFs separados ou 1 PDF completo)

### Capa — status atual ⏳ AGUARDANDO ESCOLHA
- 4 candidatas geradas com briefing v2 — ver links acima
- Prompts e IDs salvos em `context/ebooks/prompts_capa.md`
- Capas antigas (12 designs sem briefing) ainda no Canva — podem ser ignoradas

### Próximos passos do ebook (após escolha da capa)
1. ✅ ~~Gerar candidatas de capa com briefing correto~~
2. ⏳ Escolher capa → converter candidate → exportar PDF KDP
3. Decidir batch: 50 PDFs separados ou 1 PDF completo do livro
4. Rodar batch generator nas 50 receitas
5. Montar ebook completo (capa + receitas + índice)
6. Escrever Amazon listing usando `skills/marketing-copywriting.md`
7. Upload no KDP

---

## Repositório Git ✅
- **Remote:** https://github.com/Gardy019/BRAIN (público)
- **Branch:** master — up to date

---

## Mercado Livre
- CNPJ 64.224.046/0001-77 ATIVO (MEI)
- Aguardando email do Mercado Pago confirmando migração para MEI
- Próximo: vincular Mercado Envios Full

---

## Infraestrutura disponível
- `tools/generate_recipe_page.py` — gerador de páginas theme-driven ✅
- `tools/theme_engine.py` — carrega temas JSON ✅
- `themes/high-protein-cookbook.json` — tema completo do livro ✅
- `context/ebooks/design_kdp_cookbook.md` — briefing de design ✅
- `context/ebooks/prompts_capa.md` — prompts e IDs das capas ✅
- `.tmp/recipes_high_protein.md` — 50 receitas prontas
- Canva MCP — conectado e funcionando
- `playwright`, `pymupdf`, `python-pptx`, `reportlab` — instalados
