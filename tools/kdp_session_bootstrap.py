"""
KDP Session Bootstrap — Patchright

Roda UMA VEZ pra criar perfil persistente do KDP.

Fluxo:
  1. Abre Patchright (Chrome stealth) com user_data_dir persistente
  2. Navega pro login do KDP
  3. Você loga manualmente (e resolve qualquer CAPTCHA, se aparecer)
  4. Script detecta sozinho quando você chegar no Bookshelf e encerra
  5. Sessão fica salva em ~/.kdp/chrome_profile/ (perfil Chrome completo)

Depois disso, tools/kdp_upload.py reabre o mesmo perfil e entra direto
no Bookshelf sem login. Refazer só quando a sessão expirar.

Uso:
  python tools/kdp_session_bootstrap.py
"""
import sys
from pathlib import Path
from patchright.sync_api import sync_playwright

# Windows console default é cp1252 e quebra com caracteres Unicode (─, ✓, 📸, etc.)
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Perfil persistente fora do repo
PROFILE_DIR = Path.home() / ".kdp" / "chrome_profile"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

KDP_LOGIN_URL = (
    "https://www.amazon.com/ap/signin"
    "?openid.return_to=https://kdp.amazon.com/bookshelf"
    "&openid.assoc_handle=amzn_dtp"
    "&pageId=kdp-ap"
    "&openid.ns=http://specs.openid.net/auth/2.0"
)


def main() -> None:
    print("=" * 70)
    print("  KDP Session Bootstrap (Patchright)")
    print("=" * 70)
    print(f"\nPerfil persistente: {PROFILE_DIR}")
    print("\nAbrindo Chrome stealth (Patchright)...\n")

    with sync_playwright() as p:
        # launch_persistent_context é a forma recomendada pra evasão no Patchright
        # (mantém cookies, localStorage, IndexedDB, tudo entre execuções)
        # channel='chrome' usa o Chrome real instalado no sistema.
        # (O Chromium patcheado do Patchright tem erro SxS no Windows do user — bug ambiental.)
        # Patchright ainda aplica stealth via JS injection no Chrome do sistema.
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=False,
            no_viewport=True,
        )
        page = context.pages[0] if context.pages else context.new_page()

        print(f"[1] Navegando para login KDP...")
        page.goto(KDP_LOGIN_URL, wait_until="domcontentloaded")

        print("\n" + "─" * 70)
        print("AGORA É CONTIGO:")
        print("  1. Loga na conta KDP no Chrome que abriu")
        print("  2. Resolve qualquer CAPTCHA / verificação que aparecer")
        print("  3. Quando chegar no Bookshelf, o script detecta sozinho e sai")
        print("─" * 70)
        print("\n[2] Aguardando você chegar no Bookshelf (timeout: 10min)...")

        TIMEOUT_SECONDS = 600
        POLL_INTERVAL_MS = 2000
        elapsed = 0
        last_url_logged = ""
        try:
            while elapsed < TIMEOUT_SECONDS * 1000:
                current_url = page.url
                if current_url != last_url_logged:
                    print(f"   URL: {current_url}")
                    last_url_logged = current_url
                # ATENÇÃO: a URL de login tem `bookshelf` no query param `openid.return_to`.
                # Checagem correta: estar no domínio kdp.amazon.com (não no signin amazon.com)
                # e path conter bookshelf.
                url_lower = current_url.lower()
                is_signin = "signin" in url_lower or "/ap/" in url_lower
                is_kdp_domain = url_lower.startswith("https://kdp.amazon.com")
                if is_kdp_domain and "bookshelf" in url_lower and not is_signin:
                    print(f"\n[3] ✓ Detectado Bookshelf!")
                    page.wait_for_timeout(3000)
                    break
                page.wait_for_timeout(POLL_INTERVAL_MS)
                elapsed += POLL_INTERVAL_MS
            else:
                print(f"\n❌ Timeout. Você não chegou no Bookshelf em {TIMEOUT_SECONDS}s.")
                print(f"   URL atual: {page.url}")
                context.close()
                return

            print(f"\n[4] Perfil salvo automaticamente em {PROFILE_DIR}")
            print("\n✅ Bootstrap concluído!")
            print(f"\nAgora rode: python tools/kdp_upload.py")
            print("\nFechando browser em 3s...")
            page.wait_for_timeout(3000)
        finally:
            context.close()


if __name__ == "__main__":
    main()
