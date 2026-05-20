"""
Capa do ebook: High Protein Cookbook for Beginners
Abordagem 3: HTML + CSS -> PDF via Playwright
Manifesto visual: Honest Kitchen - v2 (CMO refinement)

Decisoes estrategicas:
- Subtitulo: "50 Quick Recipes to Hit 130g Protein Daily"
- Tipografia: Playfair Display (titulos) + DM Sans (corpo)
- Layout: split assimetrico, barra terracota, foto esquerda, texto direita
"""
import asyncio
from playwright.async_api import async_playwright

OUT_HTML = r"C:\Users\gardi\OneDrive\Documentos\BRAIN\.tmp\cover.html"
OUT_PDF  = r"C:\Users\gardi\OneDrive\Documentos\BRAIN\.tmp\cover_html.pdf"

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    width: 600px;
    height: 960px;
    background: #FAF8F4;
    font-family: 'DM Sans', sans-serif;
    overflow: hidden;
    position: relative;
  }

  .accent-bar {
    position: absolute;
    left: 0; top: 0;
    width: 7px; height: 100%;
    background: #C4622D;
  }

  .photo-area {
    position: absolute;
    left: 0; top: 0;
    width: 50%;
    height: 100%;
    overflow: hidden;
  }

  .photo-area::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(160deg, #C8D8CB 0%, #A8C4AE 40%, #8BAF92 70%, #6B9472 100%);
  }

  .bowl-outer {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 220px; height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle at 38% 32%,
      #F0E6D0 0%, #DCCBA8 25%, #C8A878 55%, #A07848 80%, #7A5830 100%);
    box-shadow: 0 20px 60px rgba(0,0,0,0.25), 0 4px 16px rgba(0,0,0,0.12);
  }

  .bowl-inner {
    position: absolute;
    top: 22%; left: 18%;
    width: 64%; height: 55%;
    border-radius: 50%;
    background: radial-gradient(circle at 45% 40%,
      rgba(107,143,113,0.85) 0%, rgba(75,110,80,0.7) 50%, transparent 80%);
  }

  .divider {
    position: absolute;
    left: 50%;
    top: 6%; bottom: 6%;
    width: 1px;
    background: linear-gradient(to bottom, transparent, #D8CFC4 15%, #D8CFC4 85%, transparent);
  }

  .text-area {
    position: absolute;
    left: 52%;
    top: 0; bottom: 0; right: 0;
    padding: 48px 24px 36px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .meta-top { display: flex; flex-direction: column; gap: 6px; }

  .est-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 7.5px; font-weight: 500;
    letter-spacing: 3.5px; color: #C4622D;
    text-transform: uppercase;
  }

  .tag {
    font-family: 'DM Sans', sans-serif;
    font-size: 6.5px; font-weight: 600;
    letter-spacing: 3px; color: #6B8F71;
    text-transform: uppercase;
  }

  .tag-rule {
    width: 100%; height: 0.5px;
    background: #6B8F71; opacity: 0.5; margin-top: 2px;
  }

  .title-block { display: flex; flex-direction: column; gap: 0; }

  .title-high {
    font-family: 'Playfair Display', serif;
    font-size: 52px; font-weight: 900;
    color: #2C2C2C; line-height: 0.9; letter-spacing: -2px;
  }

  .title-protein {
    font-family: 'Playfair Display', serif;
    font-size: 52px; font-weight: 900;
    color: #C4622D; line-height: 0.9; letter-spacing: -2px;
  }

  .title-cookbook {
    font-family: 'Playfair Display', serif;
    font-size: 30px; font-weight: 700;
    color: #2C2C2C; line-height: 1;
    letter-spacing: -0.5px; margin-top: 6px;
  }

  .terra-rule {
    width: 75%; height: 1.5px;
    background: #C4622D;
    margin-top: 14px; margin-bottom: 12px;
  }

  .for-beginners {
    font-family: 'DM Sans', sans-serif;
    font-size: 8px; font-weight: 400;
    letter-spacing: 5px; color: #2C2C2C;
    text-transform: uppercase;
  }

  .subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 8px; font-weight: 300;
    color: #7A7A7A; line-height: 1.65;
    margin-top: 10px; max-width: 90%;
  }

  .badges { display: flex; gap: 10px; align-items: center; }

  .badge {
    background: #6B8F71; color: #FAF8F4;
    border-radius: 50%; width: 60px; height: 60px;
    display: flex; align-items: center; justify-content: center;
    text-align: center;
    font-family: 'DM Sans', sans-serif;
    font-size: 5.5px; font-weight: 700;
    letter-spacing: 0.3px; line-height: 1.4; flex-shrink: 0;
  }

  .footer { display: flex; flex-direction: column; gap: 5px; }

  .footer-rule {
    width: 100%; height: 0.5px;
    background: #6B8F71; opacity: 0.4;
  }

  .footer-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 6px; color: #ADADAD; letter-spacing: 0.5px;
  }

  .watermark {
    position: absolute;
    bottom: 10px; right: 10px;
    font-family: 'DM Sans', sans-serif;
    font-size: 5.5px; color: #E0D8D0;
    letter-spacing: 2.5px; text-transform: lowercase;
  }
</style>
</head>
<body>

<div class="accent-bar"></div>

<div class="photo-area">
  <div class="bowl-outer">
    <div class="bowl-inner"></div>
  </div>
</div>

<div class="divider"></div>

<div class="text-area">
  <div class="meta-top">
    <div class="est-label">EST. 2026</div>
    <div class="tag">COOKBOOK</div>
    <div class="tag-rule"></div>
  </div>

  <div class="title-block">
    <div class="title-high">HIGH</div>
    <div class="title-protein">PROTEIN</div>
    <div class="title-cookbook">COOKBOOK</div>
    <div class="terra-rule"></div>
    <div class="for-beginners">FOR BEGINNERS</div>
    <div class="subtitle">50 Quick Recipes to Hit 130g Protein Daily —<br>Without Eating Chicken &amp; Eggs Every Single Day</div>
  </div>

  <div class="badges">
    <div class="badge">HIGH<br>PROTEIN</div>
    <div class="badge">30 MIN<br>MEALS</div>
    <div class="badge">BEGINNER<br>FRIENDLY</div>
  </div>

  <div class="footer">
    <div class="footer-rule"></div>
    <div class="footer-text">High Protein Cookbook for Beginners</div>
  </div>
</div>

<div class="watermark">honest kitchen</div>

</body>
</html>"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{OUT_HTML.replace(chr(92), '/')}")
        await page.wait_for_timeout(2500)
        await page.pdf(
            path=OUT_PDF,
            width="600px",
            height="960px",
            print_background=True
        )
        await browser.close()
    print(f"PDF gerado: {OUT_PDF}")

asyncio.run(main())
