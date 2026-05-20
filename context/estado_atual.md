# Estado Atual — Ponto de Retomada

_Última atualização: 2026-05-20 (sessão ebook + git setup)_

---

## Próximo passo IMEDIATO ao retornar

### 1. Autenticar o GitHub CLI e subir o repositório
O repo local já está criado e com commits. Falta só o push.

```bash
# No terminal do Windows (PowerShell ou CMD):
gh auth login
# Escolher: GitHub.com → HTTPS → Login with a web browser
# Copiar o código exibido, colar no browser, autorizar
```

Depois que autenticar, rodar no terminal (ou me avisar que eu faço):
```bash
cd "C:\Users\gardi\OneDrive\Documentos\BRAIN"
gh repo create BRAIN --private --source=. --remote=origin --push
```

---

## Estado do Projeto Ebook (High Protein Cookbook)

### Decisões estratégicas confirmadas ✅
- **Título:** "High Protein Cookbook for Beginners"
- **Subtítulo:** "50 Quick Recipes to Hit 130g Protein Daily — Without Eating Chicken & Eggs Every Single Day"
- **Pricing:** $2.99 lançamento → $4.99 (20 reviews) → $6.99 (50+ reviews)
- **50 receitas prontas** em `.tmp/recipes_high_protein.md` — 66% sem frango/ovo

### Design — Briefing Gemini incorporado ✅
- Referência salva em `docs/ebooks/design_kdp_cookbook.md`
- Paleta: Verde Floresta `#1B3B2B` + Off-White `#FAF9F5` + Ouro `#C5A059`
- Hero image: salmão, carne bovina ou bowl colorido — **NUNCA frango ou ovo na capa**
- Canva MCP conectado e funcionando — gera designs via prompt

### Capa — status atual
- 4 opções geradas via Canva MCP com briefing completo (salmão, sem frango)
- **Nenhuma foi escolhida ainda** — usuário precisa escolher uma das 4 opções
- Candidate IDs disponíveis:
  - `dg-3778c773-78fe-4c85-a516-e867e7a34fcf`
  - `dg-69f722c0-f709-4dcd-91fa-2f59b9d394ac`
  - `dg-e7e9dab9-616e-4132-9b64-5873ef1d2fad`
  - `dg-eade4920-cd06-4d1d-a63f-ccb6158dfeb2`

### Decisão pendente — layout interno
"Foto grande em página inteira (estilo arte)" vs. "compacto para leitura rápida na cozinha"?
→ Define o template das páginas de receita

### Próximos passos do ebook (após escolha da capa)
1. Salvar capa escolhida na conta Canva → exportar PDF KDP
2. Criar template de página de receita no mesmo estilo visual
3. Montar ebook completo (capa + 50 receitas + índice)
4. Escrever Amazon listing usando `skills/marketing-copywriting.md`
5. Upload no KDP

---

## Repositório Git

- **Local:** `C:\Users\gardi\OneDrive\Documentos\BRAIN`
- **Branch:** master
- **Commits:** 3 commits (initial + submodule patches)
- **Remote:** ainda não criado — aguardando `gh auth login`
- **gh CLI:** instalado em `C:\Program Files\GitHub CLI\gh.exe`

---

## Mercado Livre
- CNPJ 64.224.046/0001-77 ATIVO (MEI)
- Aguardando email do Mercado Pago confirmando migração para MEI
- Próximo: vincular Mercado Envios Full

---

## Infraestrutura disponível
- `tools/` — scripts Python para KDP, ML e geração de assets
- `skills/` — 6 skills de comportamento
- `docs/ebooks/design_kdp_cookbook.md` — briefing de design KDP completo
- `.tmp/recipes_high_protein.md` — 50 receitas prontas
- Canva MCP — conectado e funcionando
- `pymupdf`, `playwright`, `python-pptx`, `reportlab` — instalados
