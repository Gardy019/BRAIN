"""
KDP Form Discovery — mapeia todos os campos da Etapa 1 (Book Details)

Abre a página de novo livro, faz screenshot full_page, e dumpa estrutura DOM
de todos os elementos de formulário (inputs, selects, textareas, radios)
em formato legível pra atualizar o script de upload.
"""
import sys
import json
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from patchright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
TMP = ROOT / ".tmp"
TMP.mkdir(exist_ok=True)
PROFILE_DIR = Path.home() / ".kdp" / "chrome_profile"

KDP_NEW_TITLE = "https://kdp.amazon.com/en_US/title-setup/kindle/new/details?language=en_US"


def main() -> None:
    print(f"Abrindo {KDP_NEW_TITLE}...")
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=True,
        )
        page = ctx.new_page() if not ctx.pages else ctx.pages[0]
        page.goto(KDP_NEW_TITLE, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        # Screenshot da página inteira
        shot_path = TMP / "kdp_discover_full.png"
        page.screenshot(path=str(shot_path), full_page=True)
        print(f"✓ Screenshot full-page: {shot_path}")

        # Dump todos os campos de formulário
        js = """
        () => {
            const result = [];
            // inputs, selects, textareas
            const els = document.querySelectorAll('input, select, textarea, [contenteditable="true"]');
            els.forEach((el, i) => {
                // Tenta achar label associado
                let labelText = '';
                if (el.id) {
                    const lab = document.querySelector(`label[for="${el.id}"]`);
                    if (lab) labelText = lab.innerText.trim();
                }
                // Se não achou via 'for', sobe na árvore procurando label parent
                if (!labelText) {
                    let p = el.parentElement;
                    for (let i = 0; i < 5 && p; i++) {
                        const lab = p.querySelector('label');
                        if (lab && lab.innerText.trim()) {
                            labelText = lab.innerText.trim().substring(0, 80);
                            break;
                        }
                        p = p.parentElement;
                    }
                }
                // Pega texto visível próximo (parent text)
                const rect = el.getBoundingClientRect();
                result.push({
                    idx: i,
                    tag: el.tagName.toLowerCase(),
                    type: el.type || el.getAttribute('contenteditable'),
                    id: el.id,
                    name: el.name,
                    placeholder: el.placeholder,
                    value: (el.value || '').substring(0, 50),
                    label: labelText,
                    visible: rect.width > 0 && rect.height > 0,
                    required: el.required || el.getAttribute('aria-required') === 'true',
                });
            });
            return result;
        }
        """
        fields = page.evaluate(js)
        # Filtra só visíveis
        visible_fields = [f for f in fields if f.get('visible')]

        out_path = TMP / "kdp_discover_fields.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(visible_fields, f, indent=2, ensure_ascii=False)
        print(f"✓ Campos visíveis ({len(visible_fields)}): {out_path}")

        # Resumo no terminal
        print(f"\n--- RESUMO DOS CAMPOS VISÍVEIS ---")
        for f in visible_fields:
            req = " [REQUIRED]" if f.get('required') else ""
            label = f.get('label', '')[:50]
            print(f"  {f['tag']}[{f['type']}] id={f['id'] or '-'} name={f['name'] or '-'} → {label}{req}")

        ctx.close()


if __name__ == "__main__":
    main()
