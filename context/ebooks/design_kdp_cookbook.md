# Design Guide — KDP Cookbook (High Protein)

_Fonte: briefing gerado via Gemini 2026-05-18, validado pelo contexto do projeto_

---

## Especificações Técnicas KDP

- **Miolo:** 6x9 polegadas (15,24 x 22,86 cm) — padrão ouro para livros de receita
- **Sangria (Bleed):** 0,125 polegadas (3,2 mm) nas bordas externas
- **Zona segura:** nenhum elemento importante a menos de 0,375 polegadas (9,5 mm) da borda
- **Capa Kindle:** JPG/TIFF, proporção 1,6:1, ideal 2560x1600px
- **Capa KDP Print:** PDF único (quarta capa + lombada + capa). Tamanho da lombada = nº páginas × 0,00225 polegadas (papel branco)

---

## Paleta "Premium Wellness"

| Função | Cor | Hex | Impacto |
|---|---|---|---|
| Dominante (Fundo) | Verde Floresta Profundo | `#1B3B2B` | Saúde, sofisticação, orgânico |
| Contraste (Texto) | Off-White Quente | `#FAF9F5` | Conforto visual, não clínico |
| Sotaque (Destaque) | Ouro Queimado / Terracota | `#D97757` ou `#C5A059` | Apetite, premium, finalizado |

**Por que não usar preto + verde-limão neon:** comunica "suor e marmita". A paleta Premium Wellness comunica liberdade gastronômica e prazer.

---

## Arquitetura Tipográfica

```
[ SERIFADA PESADA ]       → Título principal (HIGH PROTEIN) — 30–40% da largura
[ SANS-SERIF LEVE ]       → Facilitador (for Beginners)
[ SANS-SERIF MÉDIA ]      → Quebra de objeção (Without Chicken & Eggs)
```

- **Título:** Playfair Display, Cinzel ou Poppins Bold
- **Subtítulo:** Inter ou Montserrat Regular/Light — nunca itálico decorado (borra em telas pequenas)
- **Hierarquia de leitura:** HIGH PROTEIN → números (50, 130g) → gancho (Without Chicken & Eggs)

---

## Direção de Imagem

**Regra crítica:** NUNCA mostrar frango ou ovo na capa — contradiz o hook central do livro.

**Proteínas heroicas para a imagem de capa:**
- Filé de salmão selado (rosa-alaranjado contrasta perfeitamente com fundo verde)
- Flank steak / rump com crosta grelhada + alecrim + alho assado
- Bowl de quinoa + abacate + edamame + lascas de atum selado (explosão de cores)

**Estilo fotográfico:**
- Ângulo zenital (overhead / flat lay) — exibe geometria e organização do prato
- Luz natural lateral suave (simula janela) — sombras suaves = profundidade e textura
- Evitar flash estourado ou aparência de imagem AI genérica

---

## Thumbnail Test

Na Amazon a capa compete reduzida a ~120px de largura. Regra: fundo escuro (Verde Floresta) cria contraste natural contra a interface branca da Amazon — puxa o olhar durante a rolagem.

---

## Layout Interno — Páginas de Receita

Cada receita deve caber em **uma página ou duas páginas espelhadas** (nunca quebrar ingredientes/modo de preparo entre páginas).

```
+--------------------------------------------------+
|  [FOTO DA RECEITA — sangrada]                    |
+--------------------------------------------------+
|  TÍTULO DA RECEITA (serifada)                    |
|  ⏱ 20 min  |  🥩 45g Prot  |  🔥 420 kcal       |
|                                                  |
|  INGREDIENTES (2 colunas)  |  MODO DE PREPARO    |
|  - Item 1                  |  1. Passo um...     |
|  - Item 2                  |  2. Passo dois...   |
+--------------------------------------------------+
```

- Linhas finas (0,5pt) para separar macros do texto
- Números dos passos em tamanho maior (legível a 1m de distância na bancada)
- Espaço em branco generoso — as receitas devem "respirar"

---

## Decisão Pendente

Layout interno: **foto grande em página inteira (estilo arte)** vs. **compacto para leitura rápida na cozinha**?
→ Impacta o template `generate_recipe_page.py` e a diagramação final.
