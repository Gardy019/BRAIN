"""
Scraper de reviews do Amazon para pesquisa de mercado KDP.
Busca os top livros de cada nicho, extrai reviews positivos e negativos,
e identifica padrões de oportunidade.

Uso:
    python tools/kdp_review_research.py
    python tools/kdp_review_research.py --nichos keto hipertrofia
    python tools/kdp_review_research.py --livros 3 --reviews 20
"""

import asyncio
import sys
import re
import argparse
from collections import defaultdict
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

NICHOS = {
    "Keto":        ["keto cookbook beginner", "ketogenic cookbook easy"],
    "Low Carb":    ["low carb cookbook beginner", "low carb recipes easy"],
    "Detox":       ["detox cookbook easy", "cleanse diet cookbook"],
    "Hipertrofia": ["high protein cookbook beginner", "bodybuilding cookbook easy"],
}

async def get_top_books(page, keyword: str, limit: int = 3) -> list[dict]:
    url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}&i=stripbooks"
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    try:
        await page.wait_for_selector("[data-component-type='s-search-result']", timeout=15000)
    except Exception:
        return []

    items = await page.query_selector_all("[data-component-type='s-search-result']")
    books = []

    for item in items:
        if len(books) >= limit:
            break
        try:
            # ASIN
            asin = await item.get_attribute("data-asin")
            if not asin:
                continue

            # Titulo
            title_el = await item.query_selector("h2 span")
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

            # Numero de reviews (na pagina de busca)
            reviews_count = None
            rev_el = await item.query_selector("span.a-size-base[aria-label]")
            if rev_el:
                aria = await rev_el.get_attribute("aria-label")
                if aria:
                    m = re.search(r"([\d,]+)", aria)
                    if m:
                        reviews_count = int(m.group(1).replace(",", ""))

            if title and asin:
                books.append({
                    "asin": asin,
                    "title": title,
                    "price": price,
                    "reviews_count": reviews_count,
                })
        except Exception:
            continue

    return books


async def get_reviews(page, asin: str, max_reviews: int = 20) -> list[dict]:
    reviews = []

    for page_num in range(1, 4):  # max 3 paginas de reviews
        if len(reviews) >= max_reviews:
            break

        url = (
            f"https://www.amazon.com/product-reviews/{asin}"
            f"?reviewerType=all_reviews&sortBy=helpful&pageNumber={page_num}"
        )
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_selector("[data-hook='review']", timeout=10000)
        except Exception:
            break

        items = await page.query_selector_all("[data-hook='review']")
        if not items:
            break

        for item in items:
            if len(reviews) >= max_reviews:
                break
            try:
                # Estrelas
                stars = None
                star_el = await item.query_selector("[data-hook='review-star-rating'] .a-icon-alt")
                if not star_el:
                    star_el = await item.query_selector("[data-hook='cmps-review-star-rating'] .a-icon-alt")
                if star_el:
                    star_text = await star_el.inner_text()
                    m = re.search(r"(\d+\.?\d*)", star_text)
                    if m:
                        stars = float(m.group(1))

                # Titulo do review
                title_el = await item.query_selector("[data-hook='review-title'] span:not(.a-icon-alt)")
                title = (await title_el.inner_text()).strip() if title_el else ""

                # Corpo do review
                body_el = await item.query_selector("[data-hook='review-body'] span")
                body = (await body_el.inner_text()).strip() if body_el else ""
                body = body[:500]  # limita tamanho

                if stars and body:
                    reviews.append({
                        "stars": stars,
                        "title": title,
                        "body": body,
                    })
            except Exception:
                continue

        await asyncio.sleep(1.5)

    return reviews


def analyze_reviews(reviews: list[dict]) -> dict:
    positive = [r for r in reviews if r["stars"] >= 4]
    negative = [r for r in reviews if r["stars"] <= 2]

    # Palavras-chave mais frequentes
    def top_words(texts: list[str], n: int = 15) -> list[str]:
        stopwords = {
            "the", "and", "for", "this", "that", "with", "are", "was", "have",
            "but", "not", "you", "all", "can", "had", "her", "his", "they",
            "will", "from", "been", "has", "its", "more", "would", "about",
            "which", "when", "there", "their", "what", "out", "one", "book",
            "recipes", "recipe", "cookbook", "very", "just", "get", "my",
            "i", "it", "is", "a", "an", "in", "of", "to", "i've", "i'm",
            "so", "do", "be", "me", "we", "he", "she", "how", "if", "no",
            "on", "at", "by", "as", "or", "up", "use", "used", "like",
        }
        freq = defaultdict(int)
        for text in texts:
            words = re.findall(r"\b[a-z]{3,}\b", text.lower())
            for w in words:
                if w not in stopwords:
                    freq[w] += 1
        return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:n]]

    pos_texts = [r["body"] for r in positive]
    neg_texts = [r["body"] for r in negative]

    # Frases de reclamacao (negativo)
    complaints = []
    complaint_patterns = [
        r"(too [a-z]+)",
        r"(not enough [a-z]+)",
        r"(hard to find [a-z\s]+)",
        r"(difficult [a-z\s]+)",
        r"(missing [a-z\s]+)",
        r"(wish [a-z\s]+)",
        r"(expected [a-z\s]+)",
        r"(disappointed [a-z\s]+)",
        r"(complicated [a-z\s]+)",
        r"(expensive [a-z\s]+)",
        r"(bland [a-z\s]+)",
        r"(repeat[a-z\s]+)",
    ]
    for text in neg_texts:
        for pattern in complaint_patterns:
            matches = re.findall(pattern, text.lower())
            complaints.extend(matches)

    return {
        "total": len(reviews),
        "positive_count": len(positive),
        "negative_count": len(negative),
        "positive_keywords": top_words(pos_texts),
        "negative_keywords": top_words(neg_texts),
        "complaints": list(set(complaints))[:10],
        "sample_negative": [r["body"][:200] for r in negative[:3]],
        "sample_positive": [r["body"][:200] for r in positive[:3]],
    }


def print_report(all_data: dict):
    print("\n" + "="*65)
    print("  RELATORIO DE MERCADO KDP — ANALISE DE REVIEWS")
    print("="*65)

    opportunities = {}

    for nicho, books_data in all_data.items():
        print(f"\n{'='*65}")
        print(f"  NICHO: {nicho.upper()}")
        print(f"{'='*65}")

        all_reviews = []
        for book in books_data:
            all_reviews.extend(book["reviews"])

        if not all_reviews:
            print("  Sem reviews coletados.")
            continue

        analysis = analyze_reviews(all_reviews)

        print(f"  Reviews analisados : {analysis['total']}")
        print(f"  Positivos (4-5★)  : {analysis['positive_count']}")
        print(f"  Negativos (1-2★)  : {analysis['negative_count']}")

        print(f"\n  O que os compradores AMAM:")
        print(f"  {', '.join(analysis['positive_keywords'][:10])}")

        print(f"\n  O que os compradores RECLAMAM:")
        print(f"  {', '.join(analysis['negative_keywords'][:10])}")

        if analysis["complaints"]:
            print(f"\n  Reclamacoes especificas encontradas:")
            for c in analysis["complaints"][:6]:
                print(f"    - {c}")

        print(f"\n  Exemplos de reviews negativos:")
        for i, rev in enumerate(analysis["sample_negative"], 1):
            print(f"    [{i}] {rev}")

        print(f"\n  Livros analisados neste nicho:")
        for book in books_data:
            n = len(book["reviews"])
            print(f"    - {book['title'][:55]} ({n} reviews coletados)")

        # Score de oportunidade: mais negativos = mais lacunas = mais oportunidade
        neg_pct = analysis["negative_count"] / max(analysis["total"], 1)
        opportunities[nicho] = {
            "neg_pct": neg_pct,
            "complaints": analysis["complaints"],
            "negative_keywords": analysis["negative_keywords"],
        }

    # Ranking final de oportunidade
    print(f"\n{'='*65}")
    print("  NICHOS COM MAIS LACUNAS (maiores oportunidades)")
    print(f"{'='*65}")
    ranked = sorted(opportunities.items(), key=lambda x: -x[1]["neg_pct"])
    for i, (nicho, data) in enumerate(ranked, 1):
        pct = round(data["neg_pct"] * 100)
        print(f"  {i}. {nicho} — {pct}% de reviews negativos")
        if data["complaints"]:
            print(f"     Lacunas: {', '.join(data['complaints'][:3])}")
    print()


async def main(nicho_filter: list, max_livros: int, max_reviews: int):
    nichos = {k: v for k, v in NICHOS.items() if not nicho_filter or k.lower() in [n.lower() for n in nicho_filter]}
    all_data = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1440, "height": 900},
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            },
        )
        page = await context.new_page()
        # Mascara flags de automacao
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        """)

        for nicho, keywords in nichos.items():
            print(f"\nPesquisando: {nicho}...")
            all_data[nicho] = []

            # Busca livros com o primeiro keyword
            books = await get_top_books(page, keywords[0], limit=max_livros)
            print(f"  {len(books)} livros encontrados")

            for book in books:
                print(f"  Coletando reviews: {book['title'][:50]}...")
                reviews = await get_reviews(page, book["asin"], max_reviews=max_reviews)
                book["reviews"] = reviews
                print(f"  {len(reviews)} reviews coletados")
                all_data[nicho].append(book)
                await asyncio.sleep(2)

        await browser.close()

    print_report(all_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nichos", nargs="+", default=[], help="Filtrar nichos (ex: keto hipertrofia)")
    parser.add_argument("--livros", type=int, default=3, help="Livros por nicho (default: 3)")
    parser.add_argument("--reviews", type=int, default=20, help="Reviews por livro (default: 20)")
    args = parser.parse_args()

    print(f"Iniciando pesquisa de reviews... ({args.livros} livros x {args.reviews} reviews por nicho)")
    print("Isso pode levar 5-10 minutos.\n")

    asyncio.run(main(args.nichos, args.livros, args.reviews))
