"""
Pesquisa reviews de cookbooks no Goodreads por nicho.
Extrai reviews positivos e negativos para identificar lacunas de mercado.

Uso:
    python tools/kdp_goodreads_research.py
    python tools/kdp_goodreads_research.py --livros 2 --reviews 15
"""

import asyncio
import sys
import re
import argparse
from collections import defaultdict
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BUSCAS = {
    "Keto":        "keto cookbook beginner easy",
    "Low Carb":    "low carb cookbook beginner",
    "Detox":       "detox cookbook easy recipes",
    "Hipertrofia": "high protein cookbook beginner",
}

async def search_goodreads(page, query: str, limit: int = 3) -> list[dict]:
    url = f"https://www.goodreads.com/search?q={query.replace(' ', '+')}&search_type=books"
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(2)

    books = []
    rows = await page.query_selector_all("tr[itemtype='http://schema.org/Book']")

    for row in rows[:limit * 2]:
        if len(books) >= limit:
            break
        try:
            title_el = await row.query_selector("a.bookTitle span")
            title = (await title_el.inner_text()).strip() if title_el else ""

            link_el = await row.query_selector("a.bookTitle")
            href = await link_el.get_attribute("href") if link_el else ""
            full_url = f"https://www.goodreads.com{href}" if href else ""

            rating_el = await row.query_selector(".minirating")
            rating_text = (await rating_el.inner_text()).strip() if rating_el else ""

            if title and full_url:
                books.append({"title": title, "url": full_url, "rating_text": rating_text})
        except Exception:
            continue

    return books


async def get_goodreads_reviews(page, book_url: str, max_reviews: int = 15) -> list[dict]:
    await page.goto(book_url, wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(2)

    # Tenta expandir reviews
    try:
        show_more = await page.query_selector("button[aria-label*='Show more'], .Spoiler__button")
        if show_more:
            await show_more.click()
            await asyncio.sleep(1)
    except Exception:
        pass

    reviews = []

    # Seletores do Goodreads (estrutura atual)
    review_els = await page.query_selector_all(
        "[data-testid='review'], .ReviewCard, .friendReviews .review, section.ReviewsList .ShelfStatus"
    )

    if not review_els:
        # Tenta seletor alternativo
        review_els = await page.query_selector_all(".ReviewsList .TruncatedContent, .review")

    for el in review_els[:max_reviews]:
        try:
            # Estrelas
            stars = None
            star_el = await el.query_selector("[aria-label*='Rating'], .staticStars, [class*='star']")
            if star_el:
                aria = await star_el.get_attribute("aria-label") or ""
                m = re.search(r"(\d+)", aria)
                if m:
                    stars = int(m.group(1))

            # Texto
            body_el = await el.query_selector(
                "[data-testid='contentContainer'] span, .reviewText span, .TruncatedContent__text span"
            )
            body = (await body_el.inner_text()).strip() if body_el else ""
            body = body[:500]

            if body and len(body) > 30:
                reviews.append({"stars": stars, "body": body})
        except Exception:
            continue

    return reviews


def analyze_and_report(all_data: dict):
    stopwords = {
        "the", "and", "for", "this", "that", "with", "are", "was", "have",
        "but", "not", "you", "all", "can", "had", "they", "will", "from",
        "been", "has", "its", "more", "would", "about", "which", "when",
        "there", "their", "what", "out", "one", "book", "recipes", "recipe",
        "cookbook", "very", "just", "get", "i", "it", "is", "a", "an",
        "in", "of", "to", "so", "do", "be", "me", "we", "he", "she",
        "how", "if", "no", "on", "at", "by", "as", "or", "up", "my",
        "great", "good", "love", "really", "also", "food", "make", "made",
        "these", "those", "some", "even", "use", "used", "i've", "i'm",
    }

    def top_words(texts, n=12):
        freq = defaultdict(int)
        for text in texts:
            words = re.findall(r"\b[a-z]{4,}\b", text.lower())
            for w in words:
                if w not in stopwords:
                    freq[w] += 1
        return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:n]]

    print("\n" + "="*65)
    print("  ANALISE DE REVIEWS — GOODREADS")
    print("="*65)

    opp_scores = {}

    for nicho, books in all_data.items():
        all_reviews = []
        for b in books:
            all_reviews.extend(b.get("reviews", []))

        positivos = [r for r in all_reviews if r.get("stars") and r["stars"] >= 4]
        negativos = [r for r in all_reviews if r.get("stars") and r["stars"] <= 2]
        sem_nota  = [r for r in all_reviews if not r.get("stars")]

        print(f"\n{'='*65}")
        print(f"  {nicho.upper()}")
        print(f"{'='*65}")
        print(f"  Reviews coletados : {len(all_reviews)} ({len(positivos)}+ / {len(negativos)}-)")

        if len(all_reviews) == 0:
            print("  Sem reviews suficientes.")
            continue

        pos_texts = [r["body"] for r in positivos + sem_nota]
        neg_texts = [r["body"] for r in negativos]

        if pos_texts:
            print(f"\n  O que AMAM: {', '.join(top_words(pos_texts))}")
        if neg_texts:
            print(f"  O que RECLAMAM: {', '.join(top_words(neg_texts))}")

        print(f"\n  Amostras negativas:")
        for r in negativos[:2]:
            print(f"    [{r.get('stars','?')}★] {r['body'][:200]}")

        print(f"\n  Amostras positivas:")
        for r in positivos[:2]:
            print(f"    [{r.get('stars','?')}★] {r['body'][:200]}")

        opp_scores[nicho] = len(negativos) / max(len(all_reviews), 1)

    if opp_scores:
        print(f"\n{'='*65}")
        print("  RANKING DE OPORTUNIDADE (mais reclamacoes = mais lacunas)")
        print(f"{'='*65}")
        for i, (nicho, score) in enumerate(sorted(opp_scores.items(), key=lambda x: -x[1]), 1):
            print(f"  {i}. {nicho} — {round(score*100)}% insatisfacao")
    print()


async def main(max_livros: int, max_reviews: int):
    all_data = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1440, "height": 900},
        )
        page = await context.new_page()

        for nicho, query in BUSCAS.items():
            print(f"Buscando: {nicho}...")
            books = await search_goodreads(page, query, limit=max_livros)
            print(f"  {len(books)} livros encontrados")
            all_data[nicho] = []

            for book in books:
                print(f"  Reviews: {book['title'][:50]}...")
                reviews = await get_goodreads_reviews(page, book["url"], max_reviews)
                book["reviews"] = reviews
                print(f"  {len(reviews)} reviews coletados")
                all_data[nicho].append(book)
                await asyncio.sleep(2)

        await browser.close()

    analyze_and_report(all_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--livros", type=int, default=3)
    parser.add_argument("--reviews", type=int, default=15)
    args = parser.parse_args()

    print(f"Iniciando pesquisa Goodreads ({args.livros} livros x {args.reviews} reviews)...\n")
    asyncio.run(main(args.livros, args.reviews))
