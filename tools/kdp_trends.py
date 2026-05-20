"""
Analisa tendência dos nichos de ebook no Google Trends (mercado americano).
Compara volume relativo e identifica queries relacionadas em alta.

Uso:
    python tools/kdp_trends.py
"""

import sys
import time
from pytrends.request import TrendReq

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

NICHOS = {
    "Keto":        "keto cookbook",
    "Low Carb":    "low carb cookbook",
    "Detox":       "detox cookbook",
    "Hipertrofia": "high protein cookbook",
}

def get_trends():
    pt = TrendReq(hl="en-US", tz=300)  # fuso US Eastern
    keywords = list(NICHOS.values())

    # Interesse dos ultimos 12 meses nos EUA
    pt.build_payload(keywords, timeframe="today 12-m", geo="US")
    interest = pt.interest_over_time()

    if interest.empty:
        print("Sem dados do Google Trends. Tente novamente em alguns minutos.")
        return

    # Media de interesse por nicho
    medias = interest[keywords].mean().sort_values(ascending=False)

    print("\n=== TENDENCIA 12 MESES (EUA) ===")
    print(f"{'Nicho':<20} {'Keyword':<30} {'Score medio':>12}")
    print("-" * 65)
    for kw, score in medias.items():
        nome = next(k for k, v in NICHOS.items() if v == kw)
        print(f"{nome:<20} {kw:<30} {score:>12.1f}")

    # Queries relacionadas em alta para cada nicho
    print("\n=== QUERIES EM ALTA POR NICHO ===")
    for nome, kw in NICHOS.items():
        pt.build_payload([kw], timeframe="today 12-m", geo="US")
        try:
            related = pt.related_queries()
            rising = related[kw].get("rising")
            if rising is not None and not rising.empty:
                print(f"\n{nome} ({kw}) — top queries em alta:")
                for _, row in rising.head(5).iterrows():
                    print(f"  +{row['value']:>6}%  {row['query']}")
            time.sleep(1)  # evita rate limit
        except Exception as e:
            print(f"\n{nome}: erro ao buscar related queries ({e})")

    print()

if __name__ == "__main__":
    get_trends()
