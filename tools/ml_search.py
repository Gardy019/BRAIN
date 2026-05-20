"""
Busca produtos no Mercado Livre via Playwright.
Retorna lista com nome, preco, vendidos, frete gratis, origem e URL.

Uso:
    python tools/ml_search.py "cortador de vidro tc-90"
    python tools/ml_search.py "cortador de vidro tc-90" --limit 20 --json
"""

import asyncio
import json
import sys
import re
import argparse
from playwright.async_api import async_playwright

# Forcar UTF-8 no stdout do Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def search_ml(query: str, limit: int = 15) -> list[dict]:
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="pt-BR",
            viewport={"width": 1280, "height": 800},
        )
        page = await context.new_page()

        slug = query.strip().replace(" ", "-")
        url = f"https://lista.mercadolivre.com.br/{slug}_OrderId_PRICE_NoIndex_True"
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        try:
            await page.wait_for_selector(".ui-search-layout__item", timeout=25000)
        except Exception:
            print("Timeout aguardando resultados.", file=sys.stderr)

        items = await page.query_selector_all(".ui-search-layout__item")

        for item in items[:limit]:
            try:
                # Titulo
                title_el = await item.query_selector("h2, h3")
                title = (await title_el.inner_text()).strip() if title_el else ""

                # Preco
                price = None
                price_el = await item.query_selector(".andes-money-amount__fraction")
                if price_el:
                    raw = (await price_el.inner_text()).replace(".", "").replace(",", ".")
                    try:
                        price = float(raw)
                    except ValueError:
                        pass

                # Vendidos — classe real: poly-phrase-label
                sold = None
                sold_el = await item.query_selector(".poly-phrase-label")
                if sold_el:
                    sold_text = await sold_el.inner_text()
                    mil_match = re.search(r"\+?(\d+)\s*mil", sold_text, re.IGNORECASE)
                    if mil_match:
                        sold = int(mil_match.group(1)) * 1000
                    else:
                        digits = re.search(r"(\d[\d\.]*)", sold_text)
                        if digits:
                            sold = int(digits.group(1).replace(".", ""))

                # Frete gratis — classe real: poly-component__shipping-v2
                free_shipping = False
                ship_el = await item.query_selector(".poly-component__shipping-v2")
                if ship_el:
                    txt = (await ship_el.inner_text()).lower()
                    free_shipping = "gr" in txt  # gratis / grátis

                # Origem internacional — classe poly-component__cbt ou texto "Compra internacional"
                international = False
                cbt_el = await item.query_selector(".poly-component__cbt, [class*='cbt']")
                if cbt_el:
                    international = True

                # URL limpa
                link_el = await item.query_selector("a.poly-component__title")
                raw_url = await link_el.get_attribute("href") if link_el else ""
                clean_url = raw_url.split("#")[0] if raw_url else ""

                if title and price:
                    results.append({
                        "title": title,
                        "price": price,
                        "sold": sold,
                        "free_shipping": free_shipping,
                        "international": international,
                        "url": clean_url,
                    })

            except Exception as e:
                print(f"Erro ao parsear item: {e}", file=sys.stderr)
                continue

        await browser.close()

    return results


def print_table(results: list[dict]):
    header = f"\n{'#':<3} {'Preco':>7}  {'Vendidos':>10}  {'Frete':^5}  {'Origem':^9}  Titulo"
    print(header)
    print("-" * 95)
    for i, r in enumerate(results, 1):
        sold_str = str(r["sold"]) if r["sold"] else "-"
        frete = "SIM" if r["free_shipping"] else "NAO"
        origem = "IMPORT" if r["international"] else "nacional"
        title = r["title"][:55]
        print(f"{i:<3} R${r['price']:>6.0f}  {sold_str:>10}  {frete:^5}  {origem:^9}  {title}")
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Termo de busca")
    parser.add_argument("--limit", type=int, default=15)
    parser.add_argument("--json", action="store_true", help="Saida em JSON")
    args = parser.parse_args()

    results = asyncio.run(search_ml(args.query, args.limit))

    if not results:
        print("Nenhum resultado encontrado.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_table(results)


if __name__ == "__main__":
    main()
