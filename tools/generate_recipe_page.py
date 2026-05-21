"""
Template de pagina de receita: High Protein Cookbook for Beginners
Manifesto visual: Honest Kitchen
Principio de design: Slide Escorregadio — cada elemento puxa o olho para o proximo

Uso:
  python tools/generate_recipe_page.py

Ou importar como modulo:
  from tools.generate_recipe_page import render_recipe, generate_pdf
"""
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from tools.theme_engine import load_theme

OUT_DIR = ROOT / ".tmp"
OUT_DIR.mkdir(parents=True, exist_ok=True)

THEME = load_theme("high-protein-cookbook")
_c  = THEME["colors"]
_rp = THEME["recipe_page"]
_ty = THEME["typography"]


def _google_fonts_url(theme: dict) -> str:
    h = theme["typography"]["heading"]["family"].replace(" ", "+")
    b = theme["typography"]["body"]["family"].replace(" ", "+")
    return (
        f"https://fonts.googleapis.com/css2?"
        f"family={h}:ital,wght@0,700;1,400&"
        f"family={b}:wght@300;400;500;600&display=swap"
    )


def build_css(theme: dict) -> str:
    c  = theme["colors"]
    rp = theme["recipe_page"]
    ty = theme["typography"]
    heading_font = f"'{ty['heading']['family']}', {ty['heading']['fallback']}"
    body_font    = f"'{ty['body']['family']}', {ty['body']['fallback']}"

    return f"""
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    width: 600px;
    height: 900px;
    background: {c['background']};
    font-family: {body_font};
    overflow: hidden;
    position: relative;
    color: {c['text_on_background']};
  }}

  /* Barra de capitulo — topo */
  .chapter-bar {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(
      to right,
      {c['accent']} 0%, {c['accent']} 30%,
      {c['primary']} 30%, {c['primary']} 100%
    );
  }}

  /* Numero da receita — canto sup esquerdo */
  .recipe-number {{
    position: absolute;
    top: 20px; left: 32px;
    font-family: {heading_font};
    font-size: 11px;
    font-style: italic;
    color: {c['accent']};
    letter-spacing: 1px;
  }}

  /* Logotipo sutil — canto sup direito */
  .brand {{
    position: absolute;
    top: 22px; right: 32px;
    font-family: {body_font};
    font-size: 6px;
    letter-spacing: 3px;
    color: {c['divider']};
    text-transform: lowercase;
  }}

  /* Linha divisoria horizontal sutil */
  .top-rule {{
    position: absolute;
    top: 44px; left: 32px; right: 32px;
    height: 0.5px;
    background: {c['divider']};
  }}

  /* HEADER DA RECEITA */
  .recipe-header {{
    position: absolute;
    top: 60px; left: 32px; right: 32px;
  }}

  .category-tag {{
    font-family: {body_font};
    font-size: 7px;
    font-weight: 600;
    letter-spacing: 3px;
    color: {c['primary']};
    text-transform: uppercase;
    margin-bottom: 8px;
  }}

  .recipe-title {{
    font-family: {heading_font};
    font-size: 32px;
    font-weight: 700;
    color: {c['text_on_background']};
    line-height: 1.05;
    letter-spacing: -0.5px;
    margin-bottom: 16px;
    max-width: 85%;
  }}

  /* Stats bar — 4 metricas em linha */
  .stats-bar {{
    display: flex;
    gap: 0;
    border-top: 0.5px solid {c['divider']};
    border-bottom: 0.5px solid {c['divider']};
    padding: 10px 0;
    margin-bottom: 20px;
  }}

  .stat {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    border-right: 0.5px solid {c['divider']};
  }}

  .stat:last-child {{ border-right: none; }}

  .stat-value {{
    font-family: {heading_font};
    font-size: 18px;
    font-weight: 700;
    color: {c['text_on_background']};
    line-height: 1;
  }}

  .stat-value.protein {{ color: {c['accent']}; }}

  .stat-label {{
    font-family: {body_font};
    font-size: 6px;
    font-weight: 500;
    letter-spacing: 2px;
    color: {c['muted']};
    text-transform: uppercase;
  }}

  /* CORPO: 2 colunas */
  .body-grid {{
    position: absolute;
    top: 230px; left: 32px; right: 32px; bottom: 60px;
    display: flex;
    gap: 24px;
  }}

  .ingredients-col {{
    width: 38%;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
  }}

  .col-header {{
    font-family: {body_font};
    font-size: 7px;
    font-weight: 600;
    letter-spacing: 3px;
    color: {c['primary']};
    text-transform: uppercase;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1.5px solid {c['primary']};
  }}

  .ingredients-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 7px;
  }}

  .ingredient {{
    font-family: {body_font};
    font-size: 8.5px;
    font-weight: 300;
    color: {c['text_on_background']};
    line-height: 1.3;
    display: flex;
    gap: 6px;
    align-items: baseline;
  }}

  .ing-amount {{
    font-weight: 600;
    color: {c['accent']};
    min-width: 28px;
    font-size: 8px;
  }}

  .steps-col {{
    flex: 1;
    display: flex;
    flex-direction: column;
  }}

  .steps-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  .step {{
    display: flex;
    gap: 10px;
    align-items: flex-start;
  }}

  .step-num {{
    font-family: {heading_font};
    font-size: 20px;
    font-weight: 700;
    color: {c['divider']};
    line-height: 1;
    min-width: 28px;
    flex-shrink: 0;
  }}

  .step p {{
    font-family: {body_font};
    font-size: 8.5px;
    font-weight: 300;
    color: {c['text_on_background']};
    line-height: 1.55;
  }}

  /* Tip block */
  .tip-block {{
    margin-top: 14px;
    padding: 10px 12px;
    background: {c['accent']}18;
    border-left: 2px solid {c['accent']};
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .tip-label {{
    font-family: {body_font};
    font-size: 6px;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: {c['accent']};
    text-transform: uppercase;
  }}

  .tip-text {{
    font-family: {body_font};
    font-size: 8px;
    font-weight: 300;
    color: {c['muted']};
    line-height: 1.5;
    font-style: italic;
  }}

  /* Footer */
  .page-footer {{
    position: absolute;
    bottom: 16px; left: 32px; right: 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 0.5px solid {c['divider']};
    padding-top: 8px;
  }}

  .footer-title {{
    font-family: {body_font};
    font-size: 6.5px;
    color: {c['muted']};
    letter-spacing: 0.5px;
  }}

  .page-num {{
    font-family: {heading_font};
    font-size: 9px;
    font-style: italic;
    color: {c['muted']};
  }}
"""


def build_html(recipe: dict, theme: dict = None) -> str:
    if theme is None:
        theme = THEME

    ingredients_html = "".join(
        f'<li class="ingredient"><span class="ing-amount">{i["amount"]}</span>{i["name"]}</li>'
        for i in recipe.get("ingredients", [])
    )
    steps_html = "".join(
        f'<li class="step"><span class="step-num">{idx+1:02d}</span><p>{step}</p></li>'
        for idx, step in enumerate(recipe.get("steps", []))
    )
    tip = recipe.get("tip", "")
    tip_html = (
        f'<div class="tip-block">'
        f'<span class="tip-label">PRO TIP</span>'
        f'<p class="tip-text">{tip}</p>'
        f'</div>'
    ) if tip else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="{_google_fonts_url(theme)}" rel="stylesheet">
<style>
{build_css(theme)}
</style>
</head>
<body>

<div class="chapter-bar"></div>

<div class="recipe-number">Recipe {recipe.get('number', '01')}</div>
<div class="brand">{theme.get('name', '').lower()}</div>
<div class="top-rule"></div>

<div class="recipe-header">
  <div class="category-tag">{recipe.get('category', 'MAIN COURSE')}</div>
  <h1 class="recipe-title">{recipe.get('name', 'Recipe Name')}</h1>

  <div class="stats-bar">
    <div class="stat">
      <span class="stat-value protein">{recipe.get('protein', '0')}g</span>
      <span class="stat-label">Protein</span>
    </div>
    <div class="stat">
      <span class="stat-value">{recipe.get('time', '30')}</span>
      <span class="stat-label">Minutes</span>
    </div>
    <div class="stat">
      <span class="stat-value">{recipe.get('servings', '2')}</span>
      <span class="stat-label">{'Serving' if str(recipe.get('servings', '2')) == '1' else 'Servings'}</span>
    </div>
    <div class="stat">
      <span class="stat-value">{recipe.get('difficulty', 'Easy')}</span>
      <span class="stat-label">Level</span>
    </div>
  </div>
</div>

<div class="body-grid">
  <div class="ingredients-col">
    <div class="col-header">Ingredients</div>
    <ul class="ingredients-list">
      {ingredients_html}
    </ul>
  </div>

  <div class="steps-col">
    <div class="col-header">Instructions</div>
    <ol class="steps-list">
      {steps_html}
    </ol>
    {tip_html}
  </div>
</div>

<div class="page-footer">
  <span class="footer-title">High Protein Cookbook for Beginners</span>
  <span class="page-num">{recipe.get('page', '1')}</span>
</div>

</body>
</html>"""


def render_recipe(recipe: dict, theme: dict = None) -> str:
    """Retorna o HTML da receita como string."""
    return build_html(recipe, theme)


async def generate_pdf(recipe: dict, output_pdf: str, theme: dict = None):
    from playwright.async_api import async_playwright

    html_content = build_html(recipe, theme)
    tmp_html = str(OUT_DIR / "recipe_tmp.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{tmp_html.replace(chr(92), '/')}")
        await page.wait_for_timeout(2500)
        await page.pdf(
            path=output_pdf,
            width="600px",
            height="900px",
            print_background=True,
        )
        await browser.close()
    print(f"PDF gerado: {output_pdf}")


# ── Recipe 1 das 50 receitas reais do livro ──────────────────────────────────
DEMO_RECIPE = {
    "number": "01",
    "name": "Greek Yogurt Power Bowl",
    "category": "BREAKFAST",
    "protein": "28",
    "time": "5",
    "servings": "1",
    "difficulty": "Easy",
    "page": "12",
    "ingredients": [
        {"amount": "1 cup",  "name": "plain Greek yogurt (0% or 2%)"},
        {"amount": "1 scoop","name": "vanilla protein powder"},
        {"amount": "1/2 cup","name": "mixed berries (fresh or frozen, thawed)"},
        {"amount": "2 tbsp", "name": "granola"},
        {"amount": "1 tbsp", "name": "honey"},
        {"amount": "1 tbsp", "name": "chia seeds"},
    ],
    "steps": [
        "Spoon Greek yogurt into a bowl.",
        "Stir in protein powder until fully combined.",
        "Top with berries, granola, and chia seeds.",
        "Drizzle honey over the top.",
        "Serve immediately.",
    ],
    "tip": "Prep the night before by mixing yogurt and protein powder — store covered in the fridge. Add toppings in the morning.",
}

if __name__ == "__main__":
    output = str(OUT_DIR / "recipe_demo.pdf")
    asyncio.run(generate_pdf(DEMO_RECIPE, output))
