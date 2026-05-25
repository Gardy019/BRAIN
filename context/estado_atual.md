# Estado Atual — Ponto de Retomada

_Última atualização: 2026-05-25 (sessão ebook — upload KDP refatorado para Camoufox)_

---

## 🔴 PRÓXIMO TÓPICO DA PRÓXIMA SESSÃO (2026-05-26)

**Usuário quer revisar minha organização + lógica + comportamento.**

Contexto pendente: durante a sessão de 2026-05-25 (publicação do ebook KDP), houve queima excessiva de tokens em:
- Tentativas de instalar Camoufox antes de testar Patchright
- Não pensar em Chrome MCP de cara pra fluxos interativos
- Iterar com Patchright antes de mapear seletores reais
- Muitos screenshots redundantes

Possíveis pontos de feedback a esperar:
1. Quando usar Chrome MCP vs script Python autônomo
2. Como decidir "vale escalar" vs "para e pergunta"
3. Pra evitar gastar tokens em troubleshooting de stacks que vão ser abandonadas
4. Organização da resposta (verbosidade vs concisão)
5. Frequência de updates de task list / docs

**Ação ao retomar:** ler esse bloco, depois perguntar o que ele quer mudar e ESCUTAR antes de propor solução.

---

## 🎉 STATUS ATUAL: PUBLICADO! (2026-05-25)

**High Protein Cookbook for Beginners** foi SUBMETIDO ao KDP em 2026-05-25.
- Autor: Marcus Laine (pen name)
- Preço: $2.99 USD
- Royalty plan: 70% (KDP Select ativo)
- Marketplaces: All territories
- Retenção fiscal: 30% (Brasil sem treaty formal — compensar via crédito IR)
- Conta bancária: C6 Empresas (CNPJ MEI)

**Aguardando:** aprovação Amazon (24-72h). Live esperado entre 26 e 28/05/2026.

---

## Próximo passo IMEDIATO ao retornar

### Acompanhar liberação do livro + ações pós-publicação
1. Checar Bookshelf KDP — status (Draft → In Review → Live)
2. Quando Live: capturar ASIN e URL `amazon.com/dp/[ASIN]`
3. Pedir reviews pra rede pessoal (sem trocar review por nada — Amazon bane)
4. Semana 2: planejar 1 Free Promo Day (KDP Select) pra boost
5. Após 20 reviews orgânicos: subir pra $4.99
6. Após 50 reviews: subir pra $6.99
7. Paperback: só considerar após semana 3-4 com ebook validado

### Histórico (antiga referência)

**Decisão arquitetural (2026-05-25):** Após tentativa frustrada com Camoufox (abandonou builds Windows desde mar/2025; v135-beta.24 tem bug de manifest SxS que impede iniciar), migrei para **Patchright** — fork do Playwright com Chromium patcheado anti-detect, sem binário customizado. Funciona perfeito em Windows.

**Stack instalada e pronta:**
- `patchright` 1.60.0 + Chromium patcheado (~180 MB em `~/AppData/Local/ms-playwright/`)
- `python-dotenv` para credenciais
- Credenciais movidas para `.env` (AMAZON_EMAIL, AMAZON_PASSWORD)

**Arquivos novos:**
- `tools/kdp_session_bootstrap.py` — roda 1x, login manual, salva `~/.kdp/storage_state.json`
- `tools/kdp_upload.py` — reescrito; carrega storage_state, entra direto no Bookshelf, faz upload completo
- `docs/integracoes/kdp.md` — documentação completa: arquitetura, seletores DOM, troubleshooting

**Passo 1 — Bootstrap (faltando, requer login manual):**
```bash
python tools/kdp_session_bootstrap.py
```
- Chrome abre na tela de login KDP
- Logar normalmente (resolver CAPTCHA se aparecer)
- Script auto-detecta quando você chega no Bookshelf e fecha sozinho
- Perfil persistente em `~/.kdp/chrome_profile/` (~30 dias de validade)

**Passo 2 — Upload do High Protein Cookbook:**
```bash
python tools/kdp_upload.py
```
- Browser visível, 3 pausas pra revisão humana (Etapa 1/2/3)
- Screenshots em `.tmp/kdp_*.png` a cada etapa

---

## Sessão 2026-05-25 — Estado do Upload em Andamento

### O que foi feito ✅
1. **Etapa 1 (Book Details) COMPLETE** via Chrome MCP — todos campos preenchidos:
   - Title, Subtitle, Author Marcus/Laine
   - Description em CKEditor (via modo Source HTML)
   - Publishing rights = I own copyright
   - Adult content = No
   - Marketplace = Amazon.com
   - 2 categorias: Cookbooks > Special Diet > Healthy + Health/Fitness > Diets & Weight Loss > Diets > Weight Loss
   - 7 keywords (todas <50 chars)
2. **Capa convertida PNG → JPG:** `dist/high_protein_cover.jpg` (1.17 MB, 2579×3648)
3. **Manuscrito uploaded** no KDP (PDF, "Continue with PDF" escolhido — mantém layout visual)
4. **Book ID gerado:** `ANBONJC1HF70L`

### Onde parou 🟡
Etapa 2 (Content) sendo preenchida manualmente pelo usuário. Faltam:
- Confirmar DRM = No
- Marcar "Upload a cover you already have" + selecionar `dist/high_protein_cover.jpg`
- AI-Generated Content = Yes (Some/Some/None)
- ISBN/Publisher vazios
- Accessibility = "None of the informative images..."
- Save and Continue → Etapa 3

### Bloqueador descoberto 🚨
**Account Information Incomplete** — botão Publish esmaecido até completar:
- Detalhes da conta (Nome empresarial MEI, endereço, telefone)
- Conta bancária BR
- Tax interview (W-8BEN-E, TIN=CNPJ 64224046000177, tratado Brasil = 0% retenção)

### Aprendizados técnicos (pra próxima sessão)
- **Camoufox** abandonou Windows desde mar/2025 — não rola usar
- **Patchright** funciona mas:
  - Usar `channel="chrome"` (Chromium próprio dá erro SxS no Windows)
  - Forçar UTF-8 no stdout (Windows console default é cp1252)
  - File upload via MCP Chrome NÃO funciona (restrição de segurança) — só manualmente
- **Chrome MCP**: melhor pra dev/discovery do que Patchright autônomo de cara
- **Categories modal KDP**: `form_input` em checkbox não dispara React event — usar `left_click`
- **Description CKEditor**: clicar Source button + preencher textarea com HTML + clicar Source de novo pra renderizar

### Próximos passos quando retomar
1. Usuário termina Etapa 2 + Etapa 3 (Pricing: $2.99, 70%, KDP Select, All Territories)
2. Save as Draft
3. Completar cadastro de conta (task #8)
4. Publish
5. Consolidar `tools/kdp_upload.py` com seletores validados (task #9) — pra próximos livros serem autônomos

**Arquivos prontos para upload:**
- `dist/high_protein_manuscript_final.pdf` — 4.9 MB (56 páginas: 6 intro + 50 receitas)
- `dist/high_protein_cover.png` — 7.3 MB (2580×3648px)
- Pen name: **Marcus Laine**
- Preço lançamento: **$2.99**
- Amazon listing completo embutido no `BOOK` dict do `kdp_upload.py`

### Montar páginas de intro + Amazon listing ✅ CONCLUÍDO

Arquivos prontos em `dist/`:
- `high_protein_miolo_kdp.pdf` — 50 receitas (upload KDP manuscrito)
- `high_protein_cookbook_completo.pdf` — capa + miolo (ARCs, mockups, venda direta)
- Capa original: `C:\Users\gardi\Downloads\Striking Minimalist Cookbook Cover (1).png`

**Próximos passos:**
1. Gerar páginas de intro: folha de rosto, copyright, índice, introdução (mesmo template do miolo)
2. Escrever Amazon listing (título, subtítulo, 7 bullets, descrição) usando `skills/marketing-copywriting.md`
3. Upload no KDP: capa PNG + miolo PDF separados

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

### Capa — status atual ✅ DESIGN EDITÁVEL CRIADO
- Capa A venceu (veredito Gemini: perfeição de prompt, hook completo, melhor thumbnail)
- Design editável: `DAHKZn4RK_0` — https://www.canva.com/d/E--jkBehmOgkDi1
- **Próximo:** abrir no Canva, aplicar ajustes finos e exportar como imagem KDP (2560×1600px ou proporção equivalente)

**Ajustes finos confirmados pelo Gemini antes de exportar:**
1. Margem inferior: garantir bloco de texto não colado na borda
2. Fontes: confirmar Playfair Display no título + Lato no subtítulo

### Próximos passos do ebook
1. ✅ ~~Gerar candidatas de capa com briefing correto~~
2. ✅ ~~Escolher capa → converter candidate em design editável~~
3. ✅ ~~Ajustes finos na capa (hífen removido, "Cookbook for Beginners" adicionado)~~
4. ✅ ~~Batch generator das 50 receitas~~ → `dist/high_protein_miolo_kdp.pdf` (versão definitiva: frações ASCII, HTML-safe, 12px, bullets dourados)
5. ⏳ Exportar capa do Canva como PNG em alta resolução
6. ⏳ Merge capa + miolo → `dist/high_protein_cookbook_completo.pdf`
7. Montar páginas de intro (folha de rosto, índice, introdução)
8. Escrever Amazon listing usando `skills/marketing-copywriting.md`
9. Upload no KDP

---

## Repositório Git ✅
- **Remote:** https://github.com/Gardy019/BRAIN (público)
- **Branch:** master — up to date

---

## Mercado Livre
- CNPJ 64.224.046/0001-77 ATIVO (MEI)
- ✅ Migração para conta MEI confirmada (2026-05-24) — conta tem tag `business`
- ✅ Token ML renovado e salvo no .env
- ⚠️ Full NÃO ativado ainda — logistic_type ainda é drop_off
- ⚠️ DOIS anúncios idênticos TC-90 ativos — risco de bloqueio por duplicata
  - MLB6487463452 — Gold Pro (Premium) | R$57,57 | 15 vendidos | **MANTER**
  - MLB6832051948 — Gold Special (Clássico) | R$56,30 | 0 vendidos | **DELETAR**
- ⚠️ Margem provavelmente negativa no preço atual sem Full (~-R$15/venda)
- Nutella descontinuada (último pedido fev/2026)

**Próximos passos ML (em ordem):**
1. Deletar anúncio duplicado MLB6832051948
2. Ativar Mercado Envios Full (seguir com painel ou contato ML)
3. Repreczar TC-90 após Full ativado (referência: R$79,90 → margem ~R$21)

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
