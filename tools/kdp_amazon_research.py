"""
Pesquisa nichos de ebook no Amazon.com (categoria Books).
Extrai titulo, preco, avaliacao, numero de reviews e identifica
se e publicacao independente (KDP) ou editora tradicional.

Uso:
    python tools/kdp_amazon_research.py
    python tools/kdp_amazon_research.py --json
"""

import asyncio
import sys
import json
import argparse
import re
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

NICHOS = {
    "Keto":        ["keto cookbook", "ketogenic cookbook"],
    "Low Carb":    ["low carb cookbook", "low carb recipes book"],
    "Detox":       ["detox cookbook", "cleanse cookbook"],
    "Hipertrofia": ["high protein cookbook", "bodybuilding cookbook"],
}

EDITORAS_TRADICIONAIS = [
    "penguin", "random house", "simon", "hachette", "macmillan",
    "harper", "rodale", "workman", "chronicle", "adams media",
]

async def search_amazon(page, keyword: str, limit: int = 10) -> list[dict]:
    url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}&i=stripbooks&rh=n%3A283155"
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)

    try:
        await page.wait_for_selector("[data-component-type='s-search-result']", timeout=15000)
    except Exception:
        return []

    items = await page.query_selector_all("[data-component-type='s-search-result']")
    results = []

    for item in items[:limit]:
        try:
            # Titulo
            title_el = await item.query_selector("h2 span, h2 a span")
            title = (await title_el.inner_text()).strip() if title_el else ""

            # Preco
            price = None
            price_el = await item.query_selector(".a-price .a-offscreen")
            if price_el:
                raw = (await price_el.inner_text()).replace("$", "").replace(",", "").strip()
                try:
                    price = float(raw)
                except ValueError:
                    pass

            # Avaliacao (estrelas)
            rating = None
            rating_el = await item.query_selector(".a-icon-star-small .a-icon-alt, [aria-label*='out of 5']")
            if rating_el:
                rating_text = await rating_el.get_attribute("aria-label") or await rating_el.inner_text()
                match = re.search(r"(\d+\.?\d*)", rating_text)
                if match:
                    rating = float(match.group(1))

            # Numero de reviews
            reviews = None
            reviews_el = await item.query_selector(".a-size-base.s-underline-text, [aria-label*='stars'] + span")
            if not reviews_el:
                reviews_el = await item.query_selector("span.a-size-base:not(.a-color-base)")
            if reviews_el:
                rev_text = await reviews_el.inner_text()
                rev_text = rev_text.replace(",", "").replace(".", "")
                match = re.search(r"(\d+)", rev_text)
                if match:
                    n = int(match.group(1))
                    if 10 <= n <= 500000:
                        reviews = n

            # Autor / editora
            author = ""
            author_el = await item.query_selector(".a-size-base.a-color-secondary .a-size-base")
            if author_el:
                author = (await author_el.inner_text()).strip()

            # Detecta se e KDP (independente) ou editora
            is_traditional = any(ed in author.lower() for ed in EDITORAS_TRADICIONAIS)

            if title:
                results.append({
                    "title": title[:70],
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                    "author": author[:40],
                    "traditional": is_traditional,
                })
        except Exception:
            continue

    return results


async def research_all(limit: int = 10) -> dict:
    all_results = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1280, "height": 800},
        )
        page = await context.new_page()

        for nicho, keywords in NICHOS.items():
            all_results[nicho] = []
            for kw in keywords:
                results = await search_amazon(page, kw, limit)
                all_results[nicho].extend(results)
                await asyncio.sleep(2)  # evita rate limit

        await browser.close()

    return all_results


def print_summary(all_results: dict):
    print("\n=== ANALISE DE MERCADO KDP — AMAZON.COM ===\n")

    for nicho, books in all_results.items():
        if not books:
            print(f"{nicho}: sem resultados\n")
            continue

        prices = [b["price"] for b in books if b["price"]]
        reviews = [b["reviews"] for b in books if b["reviews"]]
        ratings = [b["rating"] for b in books if b["rating"]]
        traditional = sum(1 for b in books if b["traditional"])

        avg_price = sum(prices) / len(prices) if prices else 0
        avg_reviews = sum(reviews) / len(reviews) if reviews else 0
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        kdp_pct = round((1 - traditional / len(books)) * 100) if books else 0

        # Score de oportunidade: preco alto + reviews baixo = oportunidade
        opportunity = round((avg_price * 10) / (avg_reviews / 100 + 1), 1) if avg_reviews else 0

        print(f"{'='*60}")
        print(f"  {nicho.upper()}")
        print(f"{'='*60}")
        print(f"  Livros analisados : {len(books)}")
        print(f"  Preco medio       : ${avg_price:.2f}")
        print(f"  Reviews medio     : {avg_reviews:.0f}")
        print(f"  Avaliacao media   : {avg_rating:.1f} estrelas")
        print(f"  % publicacao KDP  : {kdp_pct}%")
        print(f"  Score oportunidade: {opportunity}")
        print(f"\n  Top 3 livros:")
        for b in books[:3]:
            rev = f"{b['reviews']} reviews" if b["reviews"] else "s/ reviews"
            price = f"${b['price']:.2f}" if b["price"] else "s/ preco"
            print(f"    - {b['title'][:55]}")
            print(f"      {price} | {rev} | {b['rating'] or '?'} estrelas")
        print()

    # Ranking final
    ranked = sorted(
        all_results.items(),
        key=lambda x: (
            sum(b["price"] or 0 for b in x[1]) /
            (sum(b["reviews"] or 1 for b in x[1]) / 100 + 1)
            if x[1] else 0
        ),
        reverse=True,
    )
    print("=== RANKING DE OPORTUNIDADE ===")
    for i, (nicho, _) in enumerate(ranked, 1):
        print(f"  {i}. {nicho}")
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10, help="Livros por keyword")
    parser.add_argument("--json", action="store_true", help="Saida em JSON")
    args = parser.parse_args()

    print("Pesquisando Amazon.com... (pode levar 1-2 minutos)")
    results = asyncio.run(research_all(args.limit))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_summary(results)


if __name__ == "__main__":
    main()
