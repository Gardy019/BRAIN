"""
KDP Upload — Patchright + perfil persistente (autônomo)

Pré-requisito:
  python tools/kdp_session_bootstrap.py    # roda 1x pra criar o perfil

Arquitetura:
  - Patchright (Chromium patched anti-detect) abre perfil persistente → entra direto no Bookshelf
  - Preenche metadados, faz upload de manuscrito + capa, configura preço, publica
  - Pausa em pontos críticos pra revisão visual (Enter pra prosseguir)
  - Salva screenshots em .tmp/ a cada etapa

Quando rodar:
  python tools/kdp_upload.py

Falhas comuns:
  - "Perfil não existe" → rode o bootstrap primeiro
  - Cai no /ap/signin → sessão expirou, rode o bootstrap de novo
"""
import sys
import time
from pathlib import Path
from patchright.sync_api import sync_playwright
from dotenv import load_dotenv

# Windows console default é cp1252 e quebra com caracteres Unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv()

# Se True: clica em Publish automaticamente após preencher tudo
# Se False: para na tela final, deixa Chrome aberto por 10min pra revisão e publish manual
AUTO_PUBLISH = False

ROOT = Path(__file__).parent.parent
TMP = ROOT / ".tmp"
TMP.mkdir(exist_ok=True)

PROFILE_DIR = Path.home() / ".kdp" / "chrome_profile"
# Forçar /en_US/ — interface em inglês (seletores documentados são pra essa versão)
KDP_BOOKSHELF = "https://kdp.amazon.com/en_US/bookshelf"
KDP_NEW_TITLE = "https://kdp.amazon.com/en_US/title-setup/kindle/new/details?language=en_US"

BOOK = {
    "title":        "High Protein Cookbook for Beginners",
    "subtitle":     "50 Quick Recipes to Hit 130g Protein Daily — Without Eating Chicken & Eggs Every Single Day",
    "author_first": "Marcus",
    "author_last":  "Laine",
    "description": (
        "<b>Tired of eating the same dry chicken breast and scrambled eggs every single day "
        "just to hit your protein goals?</b>\n\n"
        "You already know protein matters. You've set the macros, tried the meal preps, powered through "
        "another grilled chicken bowl. But somewhere between the 14th identical lunch and the 22nd egg white "
        "omelette, it stops working — not because your body gave up, but because you did.\n\n"
        "<b>There's a better way. And it starts here.</b>\n\n"
        "<i>High Protein Cookbook for Beginners</i> gives you 50 complete recipes built around one simple "
        "promise: hitting 130g of protein daily while actually enjoying what you eat. Every recipe uses "
        "ingredients you can find at any grocery store, takes under 30 minutes from fridge to fork, and was "
        "written for people who are new to cooking — not professional chefs.\n\n"
        "<b>Inside you'll find:</b>\n"
        "<ul>"
        "<li><b>10 high-protein breakfasts</b> that aren't eggs again — from Peanut Butter Protein Smoothies "
        "to Overnight Protein Oats</li>"
        "<li><b>30 lunch and dinner recipes</b> featuring salmon, beef, shrimp, turkey, pork, lentils, "
        "and chickpeas</li>"
        "<li><b>10 snacks and desserts</b> — including a 5-minute Chocolate Mousse made with cottage cheese "
        "that tastes like the real thing</li>"
        "<li>Exact protein counts, prep time, serving size, and difficulty level on every single page</li>"
        "<li>A <b>Pro Tip</b> with substitutions on every recipe, so you can swap freely based on what's "
        "in your fridge</li>"
        "<li>No specialty equipment, no complicated techniques, no $40 protein powders required</li>"
        "</ul>\n\n"
        "Whether you're building muscle, cutting fat, or simply trying to eat better without making cooking "
        "your second job — this book gives you the exact framework to do it.\n\n"
        "<b>Scroll up and click Buy Now to start hitting your protein goals today.</b>"
    ),
    "keywords": [
        "high protein cookbook for beginners",
        "protein recipes under 30 minutes",
        "muscle building meal prep cookbook",
        "high protein diet recipes no chicken",
        "130g protein daily meal plan book",
        "easy high protein meals weight loss",
        "high protein cookbook salmon beef shrimp",
    ],
    "price":      "2.99",
    "manuscript": str(ROOT / "dist" / "high_protein_manuscript_final.pdf"),
    "cover":      str(ROOT / "dist" / "high_protein_cover.png"),
}


# ── Helpers ─────────────────────────────────────────────────────────────────────

def shot(page, name: str) -> None:
    path = TMP / f"kdp_{name}.png"
    try:
        page.screenshot(path=str(path), full_page=False)
        print(f"   📸 {path.name}")
    except Exception as e:
        print(f"   ⚠️  Falha no screenshot {name}: {e}")


def try_fill(page, selector: str, value: str, label: str, timeout: int = 5000) -> bool:
    try:
        el = page.locator(selector).first
        el.wait_for(timeout=timeout)
        el.fill(value)
        print(f"   ✓ {label}")
        return True
    except Exception as e:
        print(f"   ✗ {label}: {type(e).__name__}")
        return False


def try_click(page, selector: str, label: str, timeout: int = 5000) -> bool:
    try:
        page.locator(selector).first.click(timeout=timeout)
        print(f"   ✓ {label}")
        return True
    except Exception as e:
        print(f"   ✗ {label}: {type(e).__name__}")
        return False


def confirm(prompt: str, wait_seconds: int = 6) -> None:
    """Pausa pra revisão visual (rodando autônomo, não bloqueia stdin)."""
    print(f"\n   👀 {prompt} — aguardando {wait_seconds}s")
    time.sleep(wait_seconds)


# ── Verifica pré-requisitos ─────────────────────────────────────────────────────

def preflight() -> None:
    errors = []
    if not PROFILE_DIR.exists() or not any(PROFILE_DIR.iterdir()):
        errors.append(
            f"Perfil Chrome KDP não existe em {PROFILE_DIR}\n"
            f"   → Rode primeiro: python tools/kdp_session_bootstrap.py"
        )
    for key in ("manuscript", "cover"):
        if not Path(BOOK[key]).exists():
            errors.append(f"{key} não encontrado: {BOOK[key]}")
    if errors:
        print("\n❌ Pré-requisitos faltando:")
        for e in errors:
            print(f"   - {e}")
        sys.exit(1)


# ── Etapas do upload ────────────────────────────────────────────────────────────

def step_metadata(page) -> None:
    """Etapa 1 — Book Details. Seletores reais mapeados via kdp_discover_form.py."""
    print("\n━━━ Etapa 1: Book Details ━━━")
    page.goto(KDP_NEW_TITLE, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    shot(page, "01_details_loaded")

    # Language
    try:
        page.select_option("#data-language-native", "en")
        print("   ✓ language=English")
    except Exception as e:
        print(f"   ✗ language: {type(e).__name__}")

    # Title + Subtitle
    try_fill(page, "#data-title", BOOK["title"], "title")
    try_fill(page, "#data-subtitle", BOOK["subtitle"], "subtitle")

    # Author
    try_fill(page, "#data-primary-author-first-name", BOOK["author_first"], "author first name")
    try_fill(page, "#data-primary-author-last-name", BOOK["author_last"], "author last name")

    # Description — CKEditor dentro de iframe
    try:
        desc_frame = page.frame_locator("iframe[title*='Rich Text Editor']")
        desc_body = desc_frame.locator("body")
        desc_body.wait_for(timeout=5000)
        # innerHTML direto + dispara evento input pro CKEditor reconhecer
        desc_body.evaluate(
            "(el, html) => { el.innerHTML = html; el.dispatchEvent(new Event('input', {bubbles: true})); }",
            BOOK["description"],
        )
        print("   ✓ description (CKEditor)")
    except Exception as e:
        print(f"   ✗ description: {type(e).__name__}: {e}")

    # Publishing rights — "I own the copyright" (data-is-public-domain = false)
    try:
        page.locator("input[name='data-is-public-domain'][value='false']").check()
        print("   ✓ publishing rights: I own copyright")
    except Exception as e:
        print(f"   ✗ publishing rights: {type(e).__name__}")

    # Primary Audience — sexually explicit images = No (false)
    try:
        page.locator("input[name='data[is_adult_content]-radio'][value='false']").check()
        print("   ✓ adult content: No")
    except Exception as e:
        print(f"   ✗ adult content: {type(e).__name__}")

    # Primary marketplace
    try:
        page.select_option("select[name='data[digital][home_marketplace]']", "US")
        print("   ✓ primary marketplace: Amazon.com (US)")
    except Exception as e:
        print(f"   ✗ marketplace: {type(e).__name__}")

    # Keywords
    try:
        for i, kw in enumerate(BOOK["keywords"][:7]):
            page.locator(f"#data-keywords-{i}").fill(kw)
        print(f"   ✓ {len(BOOK['keywords'][:7])} keywords")
    except Exception as e:
        print(f"   ✗ keywords: {type(e).__name__}")

    shot(page, "01_details_filled")

    # Categories — CAMPO COMPLEXO (modal de árvore). Aguarda o user fazer manualmente.
    # Poll: detecta quando o erro vermelho "Answer the Adult-only question" + "category" desaparece.
    print("\n" + "!" * 70)
    print("   AÇÃO MANUAL: vai no Chrome (já aberto) e clica em 'Choose categories'.")
    print("   Escolhe 2 categorias (ex: Cookbooks > Special Diet > High Protein).")
    print("   Vou esperar até 4 minutos polling pra detectar que escolheu.")
    print("!" * 70)
    elapsed = 0
    WAIT_MS = 4 * 60 * 1000
    POLL_MS = 5000
    category_chosen = False
    while elapsed < WAIT_MS:
        try:
            # Quando o erro vermelho some, ou aparecem chips de categoria selecionada,
            # consideramos que terminou
            has_error = page.locator(
                "text=/Answer the Adult-only question before choosing a category/i"
            ).count() > 0
            chips = page.locator("[class*='category-chip'], [class*='selected-category']").count()
            if not has_error and chips > 0:
                print(f"\n   ✓ Categories detectadas ({chips} chips, sem erro). Avançando.")
                category_chosen = True
                break
        except Exception:
            pass
        time.sleep(POLL_MS / 1000)
        elapsed += POLL_MS
        if elapsed % 30000 == 0:
            print(f"   ⏳ Aguardando ({elapsed // 1000}s / {WAIT_MS // 1000}s)...")

    if not category_chosen:
        print("\n   ⚠️  Timeout esperando categorias. Tentando Save and Continue mesmo assim...")

    shot(page, "01_after_manual_category")
    try_click(page, "button:has-text('Save and Continue')", "Save and Continue (Etapa 1)")
    page.wait_for_load_state("networkidle", timeout=15000)
    page.wait_for_timeout(3000)
    shot(page, "01_after_save_continue")


def step_content(page) -> None:
    print("\n━━━ Etapa 2: Content (upload de arquivos) ━━━")
    shot(page, "02_content_loaded")

    try:
        page.locator("input[type='file']").nth(0).set_input_files(BOOK["manuscript"])
        print(f"   ✓ manuscript: {Path(BOOK['manuscript']).name}")
        print("   ⏳ Aguardando upload + processamento (até 60s)...")
        page.wait_for_timeout(15000)
    except Exception as e:
        print(f"   ✗ manuscript: {e}")

    try:
        page.locator("input[type='file']").nth(1).set_input_files(BOOK["cover"])
        print(f"   ✓ cover: {Path(BOOK['cover']).name}")
        page.wait_for_timeout(10000)
    except Exception as e:
        print(f"   ✗ cover: {e}")

    shot(page, "02_content_uploaded")
    confirm("Confirme que manuscrito e capa subiram com sucesso (sem erro vermelho)")

    try_click(page, "button:has-text('Save and Continue')", "Save and Continue (Etapa 2)")
    page.wait_for_load_state("networkidle", timeout=15000)
    page.wait_for_timeout(2000)


def step_pricing(page) -> None:
    print("\n━━━ Etapa 3: Pricing ━━━")
    shot(page, "03_pricing_loaded")

    try_click(page, "input[id*='kdp-select']", "KDP Select")
    try_click(page, "input[value='0.70'], label:has-text('70%')", "Royalty 70%")

    try:
        price = page.locator("input[id*='price'][id*='us'], input[id*='listPrice']").first
        price.fill(BOOK["price"])
        price.press("Tab")
        page.wait_for_timeout(1000)
        print(f"   ✓ preço $ {BOOK['price']}")
    except Exception as e:
        print(f"   ✗ preço: {type(e).__name__}")

    shot(page, "03_pricing_filled")

    if AUTO_PUBLISH:
        confirm("🚨 REVISÃO FINAL — vai publicar")
        try_click(
            page,
            "button:has-text('Publish Your Kindle eBook'), button:has-text('Publish')",
            "Publish",
        )
        page.wait_for_load_state("networkidle", timeout=20000)
        shot(page, "04_published")
        print("\n🎉 PUBLICADO! Amazon leva 24–72h pra aprovar e colocar no ar.")
    else:
        print("\n" + "=" * 70)
        print("  TUDO PREENCHIDO — sem publicar (AUTO_PUBLISH=False)")
        print("=" * 70)
        print("  → Revise no Chrome que está aberto")
        print("  → Clique 'Publish Your Kindle eBook' manualmente quando quiser")
        print("  → Chrome ficará aberto por 10 minutos (depois fecha sozinho)")
        print("  → Screenshots de cada etapa em .tmp/kdp_*.png")
        print("=" * 70)
        time.sleep(600)


# ── Main ────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 70)
    print("  KDP Upload — Patchright (autônomo via perfil persistente)")
    print("=" * 70)
    preflight()

    print(f"\nPerfil Chrome:  {PROFILE_DIR}")
    print(f"Manuscript:     {BOOK['manuscript']}")
    print(f"Cover:          {BOOK['cover']}")
    print(f"Title:          {BOOK['title']}")
    print(f"Preço:          $ {BOOK['price']}\n")

    with sync_playwright() as p:
        # channel='chrome' usa o Chrome real instalado (Chromium patcheado tem erro SxS no Windows).
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=False,
            no_viewport=True,
        )
        page = context.pages[0] if context.pages else context.new_page()

        try:
            page.goto(KDP_BOOKSHELF, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            if "signin" in page.url.lower() or "/ap/" in page.url.lower():
                print("\n❌ Sessão expirou (redirecionou pro login).")
                print("   → Rode: python tools/kdp_session_bootstrap.py")
                context.close()
                sys.exit(1)
            print(f"✓ Logado: {page.url}")
            shot(page, "00_bookshelf")

            step_metadata(page)
            step_content(page)
            step_pricing(page)

            print("\n" + "=" * 70)
            print("  Concluído. Fechando browser...")
            print("=" * 70)
        finally:
            context.close()


if __name__ == "__main__":
    main()
