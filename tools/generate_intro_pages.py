"""
Gerador de páginas de introdução — High Protein Cookbook for Beginners
Páginas: Title | Copyright | Table of Contents (x2) | Introduction (x2)
Output: dist/high_protein_intro.pdf

Usage:
  python tools/generate_intro_pages.py
"""
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from tools.theme_engine import load_theme

THEME   = load_theme("high-protein-cookbook")
_c      = THEME["colors"]
_ty     = THEME["typography"]
DIST    = ROOT / "dist"
TMP     = ROOT / ".tmp"
DIST.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

BOOK_TITLE    = "High Protein Cookbook for Beginners"
BOOK_SUBTITLE = "50 Quick Recipes to Hit 130g Protein Daily\nWithout Chicken & Eggs Every Single Day"
AUTHOR        = "Marcus Laine"
YEAR          = "2026"

RECIPES = [
    # Breakfast
    ("01", "Greek Yogurt Power Bowl",              "Breakfast"),
    ("02", "Scrambled Egg & Cottage Cheese Toast", "Breakfast"),
    ("03", "Overnight Protein Oats",               "Breakfast"),
    ("04", "Turkey & Egg Breakfast Wrap",          "Breakfast"),
    ("05", "Protein Banana Pancakes",              "Breakfast"),
    ("06", "Smoked Salmon & Egg White Omelette",   "Breakfast"),
    ("07", "Peanut Butter Protein Smoothie",       "Breakfast"),
    ("08", "Cottage Cheese Breakfast Bowl",        "Breakfast"),
    ("09", "High-Protein French Toast",            "Breakfast"),
    ("10", "Tuna & Avocado Morning Toast",         "Breakfast"),
    # Lunch & Dinner
    ("11", "Classic Chicken & Rice Bowl",          "Lunch & Dinner"),
    ("12", "High-Protein Tuna Salad",              "Lunch & Dinner"),
    ("13", "Turkey Lettuce Wraps",                 "Lunch & Dinner"),
    ("14", "Egg White & Veggie Stir-Fry",          "Lunch & Dinner"),
    ("15", "Black Bean & Chicken Burrito Bowl",    "Lunch & Dinner"),
    ("16", "Cottage Cheese & Veggie Stuffed Pepper","Lunch & Dinner"),
    ("17", "Shrimp & Avocado Salad",               "Lunch & Dinner"),
    ("18", "Lemon Herb Chicken Pita",              "Lunch & Dinner"),
    ("19", "Protein-Packed Lentil Soup",           "Lunch & Dinner"),
    ("20", "Ground Beef Taco Bowl",                "Lunch & Dinner"),
    ("21", "Chicken Caesar Salad (High-Protein)",  "Lunch & Dinner"),
    ("22", "Egg Salad Protein Plate",              "Lunch & Dinner"),
    ("23", "Baked Salmon & Asparagus",             "Lunch & Dinner"),
    ("24", "Turkey Meatball Pasta",                "Lunch & Dinner"),
    ("25", "Chickpea & Spinach Curry",             "Lunch & Dinner"),
    ("26", "Sheet Pan Chicken Thighs & Veggies",   "Lunch & Dinner"),
    ("27", "Beef & Broccoli Stir-Fry",             "Lunch & Dinner"),
    ("28", "Baked Cod with Lemon & Herbs",         "Lunch & Dinner"),
    ("29", "Chicken Fajita Skillet",               "Lunch & Dinner"),
    ("30", "Ground Turkey Stuffed Zucchini",       "Lunch & Dinner"),
    ("31", "One-Pan Pork Tenderloin & Sweet Potato","Lunch & Dinner"),
    ("32", "Protein Pasta with Ricotta & Spinach", "Lunch & Dinner"),
    ("33", "Baked Chicken Parmesan (Light)",       "Lunch & Dinner"),
    ("34", "Shrimp Tacos with Greek Yogurt Slaw",  "Lunch & Dinner"),
    ("35", "Lemon Garlic White Bean & Chicken",    "Lunch & Dinner"),
    ("36", "Honey Garlic Salmon",                  "Lunch & Dinner"),
    ("37", "Greek Turkey Burger",                  "Lunch & Dinner"),
    ("38", "Egg Fried Rice (High-Protein)",        "Lunch & Dinner"),
    ("39", "Slow-Cooker Chicken & White Bean Soup","Lunch & Dinner"),
    ("40", "Baked Meatballs with Marinara",        "Lunch & Dinner"),
    # Snacks & Desserts
    ("41", "Peanut Butter Protein Balls",          "Snacks & Desserts"),
    ("42", "Hard-Boiled Eggs with Everything Bagel Seasoning", "Snacks & Desserts"),
    ("43", "Greek Yogurt Dip with Veggie Sticks",  "Snacks & Desserts"),
    ("44", "Tuna-Stuffed Mini Peppers",            "Snacks & Desserts"),
    ("45", "Ricotta & Honey Rice Cakes",           "Snacks & Desserts"),
    ("46", "Chocolate Protein Mug Cake",           "Snacks & Desserts"),
    ("47", "Frozen Greek Yogurt Bark",             "Snacks & Desserts"),
    ("48", "Banana Peanut Butter Ice Cream",       "Snacks & Desserts"),
    ("49", "Cottage Cheese Chocolate Mousse",      "Snacks & Desserts"),
    ("50", "Protein Cheesecake Cups",              "Snacks & Desserts"),
]

# Recipe pages start at page 7 (after 6 intro pages)
RECIPE_START_PAGE = 7


def _fonts_url() -> str:
    h = _ty["heading"]["family"].replace(" ", "+")
    b = _ty["body"]["family"].replace(" ", "+")
    return (
        f"https://fonts.googleapis.com/css2?"
        f"family={h}:ital,wght@0,700;1,400&"
        f"family={b}:wght@300;400;500;600&display=swap"
    )


BASE_CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 600px;
  height: 900px;
  font-family: '{_ty["body"]["family"]}', {_ty["body"]["fallback"]};
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
}}
"""


# ── PAGE 1: Title ────────────────────────────────────────────────────────────
def html_title() -> str:
    subtitle_lines = BOOK_SUBTITLE.replace("\\n", "\n").split("\n")
    subtitle_html  = "<br>".join(subtitle_lines)
    return f"""<!DOCTYPE html><html><head>
<meta charset="UTF-8">
<link href="{_fonts_url()}" rel="stylesheet">
<style>
{BASE_CSS}
body {{
  background: {_c['primary']};
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 48px;
}}
.top-rule {{
  width: 60px; height: 2px;
  background: {_c['accent']};
  margin: 0 auto 32px;
}}
.label {{
  font-family: '{_ty["body"]["family"]}', sans-serif;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: {_c['accent']};
  margin-bottom: 24px;
}}
h1 {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 56px;
  font-weight: 700;
  color: {_c['text_on_primary']};
  line-height: 1.0;
  letter-spacing: -1px;
  margin-bottom: 16px;
}}
.subtitle {{
  font-family: '{_ty["body"]["family"]}', sans-serif;
  font-size: 14px;
  font-weight: 300;
  color: {_c['accent']};
  line-height: 1.6;
  margin-bottom: 48px;
}}
.bottom-rule {{
  width: 40px; height: 1px;
  background: {_c['divider']};
  margin: 0 auto 24px;
}}
.author {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 13px;
  font-style: italic;
  color: {_c['divider']};
  letter-spacing: 1px;
}}
</style></head>
<body>
  <div class="top-rule"></div>
  <div class="label">A Complete Cookbook</div>
  <h1>High Protein<br>Cookbook</h1>
  <p class="subtitle">{subtitle_html}</p>
  <div class="bottom-rule"></div>
  <div class="author">{AUTHOR}</div>
</body></html>"""


# ── PAGE 2: Copyright ────────────────────────────────────────────────────────
def html_copyright() -> str:
    return f"""<!DOCTYPE html><html><head>
<meta charset="UTF-8">
<link href="{_fonts_url()}" rel="stylesheet">
<style>
{BASE_CSS}
body {{
  background: {_c['background']};
  color: {_c['text_on_background']};
  padding: 80px 60px 60px;
  justify-content: space-between;
}}
p, li {{
  font-family: '{_ty["body"]["family"]}', sans-serif;
  font-size: 10px;
  font-weight: 300;
  line-height: 1.8;
  color: {_c['muted']};
}}
.block {{ margin-bottom: 28px; }}
.label {{
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: {_c['accent']};
  margin-bottom: 8px;
}}
.copyright-line {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 11px;
  color: {_c['text_on_background']};
  margin-bottom: 20px;
}}
</style></head>
<body>
  <div>
    <p class="copyright-line">Copyright &copy; {YEAR} {AUTHOR}. All rights reserved.</p>

    <div class="block">
      <div class="label">AI Disclosure</div>
      <p>Portions of this book were created with the assistance of artificial intelligence tools, including recipe generation and text editing. All recipes have been reviewed and curated for accuracy and quality.</p>
    </div>

    <div class="block">
      <div class="label">Disclaimer</div>
      <p>This book is for informational purposes only and is not a substitute for professional nutritional or medical advice. Nutritional values are estimates and may vary based on ingredients and preparation methods. Consult a qualified healthcare provider before making significant dietary changes.</p>
    </div>

    <div class="block">
      <div class="label">No Part of This Book</div>
      <p>may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author, except for brief quotations in reviews.</p>
    </div>
  </div>

  <p style="text-align:center; font-size:9px; letter-spacing:1px;">
    First Edition &mdash; {YEAR} &mdash; Published via Amazon KDP
  </p>
</body></html>"""


# ── PAGES 3–4: Table of Contents ─────────────────────────────────────────────
def html_toc(page: int) -> str:
    """page=1 → Breakfast + first half Lunch; page=2 → rest Lunch + Snacks"""
    if page == 1:
        categories = ["Breakfast", "Lunch & Dinner"]
        recipes    = [r for r in RECIPES if r[2] in categories][:25]
        heading    = "Table of Contents"
        page_num   = "3"
    else:
        recipes  = [r for r in RECIPES if r[2] == "Lunch & Dinner"][14:] + \
                   [r for r in RECIPES if r[2] == "Snacks & Desserts"]
        heading  = "Table of Contents"
        page_num = "4"

    rows = ""
    for num, name, cat in recipes:
        p = RECIPE_START_PAGE + int(num) - 1
        rows += f"""
        <div class="toc-row">
          <span class="toc-num">{num}</span>
          <span class="toc-name">{name}</span>
          <span class="toc-dots"></span>
          <span class="toc-page">{p}</span>
        </div>"""

    cat_sections = ""
    current_cat  = None
    for num, name, cat in recipes:
        p = RECIPE_START_PAGE + int(num) - 1
        if cat != current_cat:
            current_cat = cat
            cat_sections += f'<div class="cat-label">{cat}</div>'
        cat_sections += f"""
        <div class="toc-row">
          <span class="toc-num">{num}</span>
          <span class="toc-name">{name}</span>
          <span class="toc-dots"></span>
          <span class="toc-page">{p}</span>
        </div>"""

    return f"""<!DOCTYPE html><html><head>
<meta charset="UTF-8">
<link href="{_fonts_url()}" rel="stylesheet">
<style>
{BASE_CSS}
body {{
  background: {_c['background']};
  color: {_c['text_on_background']};
  padding: 48px 48px 24px;
}}
.page-heading {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 22px;
  font-weight: 700;
  color: {_c['primary']};
  margin-bottom: 6px;
}}
.top-rule {{
  height: 1.5px;
  background: linear-gradient(to right, {_c['accent']} 0%, {_c['accent']} 40%, {_c['divider']} 40%);
  margin-bottom: 20px;
}}
.cat-label {{
  font-family: '{_ty["body"]["family"]}', sans-serif;
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: {_c['accent']};
  margin: 14px 0 6px;
}}
.toc-row {{
  display: flex;
  align-items: baseline;
  gap: 6px;
  padding: 3px 0;
  border-bottom: 0.5px solid {_c['divider']}40;
}}
.toc-num {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 10px;
  font-style: italic;
  color: {_c['accent']};
  min-width: 22px;
  flex-shrink: 0;
}}
.toc-name {{
  font-family: '{_ty["body"]["family"]}', sans-serif;
  font-size: 11px;
  font-weight: 300;
  color: {_c['text_on_background']};
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.toc-dots {{
  flex-shrink: 0;
  width: 20px;
  border-bottom: 1px dotted {_c['divider']};
}}
.toc-page {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 10px;
  font-style: italic;
  color: {_c['muted']};
  min-width: 18px;
  text-align: right;
  flex-shrink: 0;
}}
.footer {{
  margin-top: auto;
  padding-top: 10px;
  border-top: 0.5px solid {_c['divider']};
  display: flex;
  justify-content: space-between;
  font-size: 9px;
  color: {_c['muted']};
}}
</style></head>
<body>
  <div class="page-heading">{heading}</div>
  <div class="top-rule"></div>
  {cat_sections}
  <div style="flex:1"></div>
  <div class="footer">
    <span>{BOOK_TITLE}</span>
    <span>{page_num}</span>
  </div>
</body></html>"""


# ── PAGES 5–6: Introduction ──────────────────────────────────────────────────
def html_intro(page: int) -> str:
    page_num = str(4 + page)
    if page == 1:
        content = f"""
      <h2 class="section-title">Introduction</h2>
      <div class="rule"></div>
      <p>If you've picked up this book, you're probably tired of the same advice: eat chicken and eggs, repeat forever. You know protein matters. You want to build muscle, lose fat, or simply feel better. But eating the same two foods every single day? That's a recipe for burnout, not results.</p>
      <p>This book was written for one reason: to show you that hitting 130 grams of protein daily can be delicious, varied, and genuinely simple.</p>
      <p>Every recipe in these pages uses ingredients you can find at any grocery store. No specialty powders required, no complicated techniques, no hour-long meal preps. Most recipes take under 30 minutes from fridge to fork.</p>
      <p>The 50 recipes ahead are organized into three sections — <strong>Breakfast</strong>, <strong>Lunch &amp; Dinner</strong>, and <strong>Snacks &amp; Desserts</strong> — so you can build complete, satisfying days without ever repeating yourself.</p>
"""
    else:
        content = f"""
      <h2 class="section-title">How to Use This Book</h2>
      <div class="rule"></div>
      <p><strong>Start anywhere.</strong> There's no required order. Flip to a category that matches your next meal and pick something that looks good.</p>
      <p><strong>Track your protein first.</strong> Each recipe shows the protein count in grams. Use that number to build your day. Hit 130g by combining recipes freely across all three sections.</p>
      <p><strong>Swap freely.</strong> Most recipes include a <em>Pro Tip</em> with substitutions. Ground beef can replace turkey. Salmon can swap for cod. The framework matters more than the exact ingredient.</p>
      <p><strong>Batch when it makes sense.</strong> Recipes like the Overnight Protein Oats, Protein Balls, and Slow-Cooker Chicken Soup double beautifully. Make extra and refrigerate for the week.</p>
      <p style="margin-top: 20px; font-style: italic; color: {_c['muted']};">Ready? Your first 130-gram day starts on the next page.</p>
"""

    return f"""<!DOCTYPE html><html><head>
<meta charset="UTF-8">
<link href="{_fonts_url()}" rel="stylesheet">
<style>
{BASE_CSS}
body {{
  background: {_c['background']};
  color: {_c['text_on_background']};
  padding: 54px 56px 32px;
  justify-content: space-between;
}}
.section-title {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 26px;
  font-weight: 700;
  color: {_c['primary']};
  margin-bottom: 8px;
}}
.rule {{
  height: 1.5px;
  width: 100%;
  background: linear-gradient(to right, {_c['accent']} 0%, {_c['accent']} 30%, {_c['divider']} 30%);
  margin-bottom: 22px;
}}
p {{
  font-family: '{_ty["body"]["family"]}', sans-serif;
  font-size: 12px;
  font-weight: 300;
  line-height: 1.75;
  color: {_c['text_on_background']};
  margin-bottom: 14px;
}}
strong {{ font-weight: 600; color: {_c['primary']}; }}
.footer {{
  padding-top: 10px;
  border-top: 0.5px solid {_c['divider']};
  display: flex;
  justify-content: space-between;
  font-size: 9px;
  color: {_c['muted']};
  font-family: '{_ty["body"]["family"]}', sans-serif;
}}
</style></head>
<body>
  <div>
    {content}
  </div>
  <div class="footer">
    <span>{BOOK_TITLE}</span>
    <span>{page_num}</span>
  </div>
</body></html>"""


# ── Render + Merge ────────────────────────────────────────────────────────────
async def render_page(html: str, output_path: str):
    from playwright.async_api import async_playwright
    tmp = TMP / "_intro_tmp.html"
    tmp.write_text(html, encoding="utf-8")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        pg = await browser.new_page()
        await pg.goto(f"file:///{str(tmp).replace(chr(92), '/')}")
        await pg.wait_for_timeout(2500)
        await pg.pdf(path=output_path, width="600px", height="900px", print_background=True)
        await browser.close()
    print(f"  OK  {output_path}")


async def main():
    pages = [
        (html_title(),       str(TMP / "intro_01_title.pdf")),
        (html_copyright(),   str(TMP / "intro_02_copyright.pdf")),
        (html_toc(1),        str(TMP / "intro_03_toc1.pdf")),
        (html_toc(2),        str(TMP / "intro_04_toc2.pdf")),
        (html_intro(1),      str(TMP / "intro_05_intro1.pdf")),
        (html_intro(2),      str(TMP / "intro_06_intro2.pdf")),
    ]

    print("Renderizando páginas de introdução...")
    for html, path in pages:
        await render_page(html, path)

    print("\nMergeando em dist/high_protein_intro.pdf ...")
    import fitz
    merged = fitz.open()
    for _, path in pages:
        merged.insert_pdf(fitz.open(path))
    out = str(DIST / "high_protein_intro.pdf")
    merged.save(out)
    merged.close()
    print(f"  OK  {out}")

    print("\nMergeando intro + miolo -> dist/high_protein_manuscript_final.pdf ...")
    final = fitz.open()
    final.insert_pdf(fitz.open(out))
    final.insert_pdf(fitz.open(str(DIST / "high_protein_miolo_kdp.pdf")))
    final_out = str(DIST / "high_protein_manuscript_final.pdf")
    final.save(final_out)
    final.close()
    print(f"  OK  {final_out}")
    print("\nPronto! Manuscrito final gerado.")


if __name__ == "__main__":
    asyncio.run(main())
