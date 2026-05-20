"""
Template de pagina de receita: High Protein Cookbook for Beginners
Manifesto visual: Honest Kitchen
Principio de design: Slide Escorregadio — cada elemento puxa o olho para o proximo

Uso:
  python generate_recipe_page.py --recipe "Lemon Herb Chicken Bowl" --protein 45 --time 25 --servings 2 --difficulty Easy

Ou importar como modulo:
  from generate_recipe_page import render_recipe
  render_recipe(recipe_data, output_path)
"""
import asyncio
import argparse
from playwright.async_api import async_playwright
from pathlib import Path

OUT_DIR = Path(r"C:\Users\gardi\OneDrive\Documentos\BRAIN\.tmp")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def build_html(recipe: dict) -> str:
    ingredients_html = "".join(
        f'<li class="ingredient"><span class="ing-amount">{i["amount"]}</span>{i["name"]}</li>'
        for i in recipe.get("ingredients", [])
    )
    steps_html = "".join(
        f'<li class="step"><span class="step-num">{idx+1:02d}</span><p>{step}</p></li>'
        for idx, step in enumerate(recipe.get("steps", []))
    )
    tip = recipe.get("tip", "")
    tip_html = f'<div class="tip-block"><span class="tip-label">PRO TIP</span><p class="tip-text">{tip}</p></div>' if tip else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    width: 600px;
    height: 960px;
    background: #FAF8F4;
    font-family: 'DM Sans', sans-serif;
    overflow: hidden;
    position: relative;
    color: #2C2C2C;
  }}

  /* Barra de capitulo — topo */
  .chapter-bar {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(to right, #C4622D 0%, #C4622D 30%, #6B8F71 30%, #6B8F71 100%);
  }}

  /* Numero da receita — canto sup esquerdo */
  .recipe-number {{
    position: absolute;
    top: 20px; left: 32px;
    font-family: 'Playfair Display', serif;
    font-size: 11px;
    font-style: italic;
    color: #C4622D;
    letter-spacing: 1px;
  }}

  /* Logotipo sutil — canto sup direito */
  .brand {{
    position: absolute;
    top: 22px; right: 32px;
    font-family: 'DM Sans', sans-serif;
    font-size: 6px;
    letter-spacing: 3px;
    color: #D0C8BE;
    text-transform: lowercase;
  }}

  /* Linha divisoria horizontal sutil */
  .top-rule {{
    position: absolute;
    top: 44px; left: 32px; right: 32px;
    height: 0.5px;
    background: #E8E0D5;
  }}

  /* ─── HEADER DA RECEITA ─── */
  .recipe-header {{
    position: absolute;
    top: 60px; left: 32px; right: 32px;
  }}

  .category-tag {{
    font-family: 'DM Sans', sans-serif;
    font-size: 7px;
    font-weight: 600;
    letter-spacing: 3px;
    color: #6B8F71;
    text-transform: uppercase;
    margin-bottom: 8px;
  }}

  .recipe-title {{
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 700;
    color: #2C2C2C;
    line-height: 1.05;
    letter-spacing: -0.5px;
    margin-bottom: 16px;
    max-width: 85%;
  }}

  /* Stats bar — 4 metricas em linha */
  .stats-bar {{
    display: flex;
    gap: 0;
    border-top: 0.5px solid #E8E0D5;
    border-bottom: 0.5px solid #E8E0D5;
    padding: 10px 0;
    margin-bottom: 20px;
  }}

  .stat {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    border-right: 0.5px solid #E8E0D5;
  }}

  .stat:last-child {{ border-right: none; }}

  .stat-value {{
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    color: #2C2C2C;
    line-height: 1;
  }}

  .stat-value.protein {{ color: #C4622D; }}

  .stat-label {{
    font-family: 'DM Sans', sans-serif;
    font-size: 6px;
    font-weight: 500;
    letter-spacing: 2px;
    color: #9B9B9B;
    text-transform: uppercase;
  }}

  /* ─── CORPO: 2 colunas ─── */
  .body-grid {{
    position: absolute;
    top: 230px; left: 32px; right: 32px; bottom: 60px;
    display: flex;
    gap: 24px;
  }}

  /* Coluna esquerda: ingredientes */
  .ingredients-col {{
    width: 38%;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
  }}

  .col-header {{
    font-family: 'DM Sans', sans-serif;
    font-size: 7px;
    font-weight: 600;
    letter-spacing: 3px;
    color: #6B8F71;
    text-transform: uppercase;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1.5px solid #6B8F71;
  }}

  .ingredients-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 7px;
  }}

  .ingredient {{
    font-family: 'DM Sans', sans-serif;
    font-size: 8.5px;
    font-weight: 300;
    color: #3C3C3C;
    line-height: 1.3;
    display: flex;
    gap: 6px;
    align-items: baseline;
  }}

  .ing-amount {{
    font-weight: 600;
    color: #C4622D;
    min-width: 28px;
    font-size: 8px;
  }}

  /* Coluna direita: instrucoes */
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
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: #E8E0D5;
    line-height: 1;
    min-width: 28px;
    flex-shrink: 0;
  }}

  .step p {{
    font-family: 'DM Sans', sans-serif;
    font-size: 8.5px;
    font-weight: 300;
    color: #3C3C3C;
    line-height: 1.55;
  }}

  /* Tip block */
  .tip-block {{
    margin-top: 14px;
    padding: 10px 12px;
    background: rgba(196, 98, 45, 0.06);
    border-left: 2px solid #C4622D;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .tip-label {{
    font-family: 'DM Sans', sans-serif;
    font-size: 6px;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: #C4622D;
    text-transform: uppercase;
  }}

  .tip-text {{
    font-family: 'DM Sans', sans-serif;
    font-size: 8px;
    font-weight: 300;
    color: #5A5A5A;
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
    border-top: 0.5px solid #E8E0D5;
    padding-top: 8px;
  }}

  .footer-title {{
    font-family: 'DM Sans', sans-serif;
    font-size: 6.5px;
    color: #C0B8B0;
    letter-spacing: 0.5px;
  }}

  .page-num {{
    font-family: 'Playfair Display', serif;
    font-size: 9px;
    font-style: italic;
    color: #C0B8B0;
  }}
</style>
</head>
<body>

<div class="chapter-bar"></div>

<div class="recipe-number">Recipe {recipe.get('number', '01')}</div>
<div class="brand">honest kitchen</div>
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
      <span class="stat-label">Servings</span>
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


def render_recipe(recipe: dict, output_path: str = None) -> str:
    """Gera HTML da receita. Retorna o HTML como string."""
    return build_html(recipe)


async def generate_pdf(recipe: dict, output_pdf: str):
    html_content = build_html(recipe)
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
            height="960px",
            print_background=True
        )
        await browser.close()
    print(f"Recipe PDF: {output_pdf}")


# ── DEMO: receita de exemplo ──────────────────────────────────────────────────
DEMO_RECIPE = {
    "number": "01",
    "name": "Lemon Herb Chicken & Quinoa Bowl",
    "category": "LUNCH",
    "protein": "48",
    "time": "25",
    "servings": "2",
    "difficulty": "Easy",
    "page": "24",
    "ingredients": [
        {"amount": "2x", "name": "chicken breasts (200g each)"},
        {"amount": "1 cup", "name": "quinoa, rinsed"},
        {"amount": "2 tbsp", "name": "olive oil"},
        {"amount": "1", "name": "lemon, zest and juice"},
        {"amount": "2 cloves", "name": "garlic, minced"},
        {"amount": "1 tsp", "name": "dried oregano"},
        {"amount": "1 tsp", "name": "smoked paprika"},
        {"amount": "2 cups", "name": "cherry tomatoes, halved"},
        {"amount": "1 cup", "name": "cucumber, diced"},
        {"amount": "2 tbsp", "name": "fresh parsley, chopped"},
        {"amount": "Salt &", "name": "pepper to taste"},
    ],
    "steps": [
        "Cook quinoa in 2 cups salted water. Bring to boil, reduce heat, cover and simmer 15 minutes. Fluff with fork.",
        "Mix olive oil, lemon zest, garlic, oregano, and paprika. Season chicken breasts and coat evenly.",
        "Heat a skillet over medium-high heat. Cook chicken 6–7 min per side until internal temp reaches 165°F (74°C). Rest 5 min, then slice.",
        "While chicken rests, toss tomatoes and cucumber with lemon juice, salt, and pepper.",
        "Divide quinoa between bowls. Top with sliced chicken, veggie mix, and fresh parsley. Drizzle with remaining lemon juice.",
    ],
    "tip": "Meal prep hack: cook double the quinoa on Sunday. It keeps refrigerated for 5 days and cuts your prep time in half all week."
}

if __name__ == "__main__":
    output = str(OUT_DIR / "recipe_demo.pdf")
    asyncio.run(generate_pdf(DEMO_RECIPE, output))
