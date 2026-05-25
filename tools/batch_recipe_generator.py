"""
Batch generator: parse 50 recipes from MD, render each as KDP PDF, merge into miolo.

Usage:
  python tools/batch_recipe_generator.py           # gera miolo completo
  python tools/batch_recipe_generator.py --merge-cover  # miolo + capa → completo

Outputs em dist/:
  recipe_01.pdf ... recipe_50.pdf   (páginas individuais)
  high_protein_miolo_kdp.pdf        (50 páginas mergeadas — upload KDP)
  high_protein_cookbook_completo.pdf (capa + miolo — ARCs, mockups, venda direta)
"""
import re
import asyncio
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from tools.generate_recipe_page import generate_pdf

RECIPES_MD = ROOT / ".tmp" / "recipes_high_protein.md"
DIST_DIR   = ROOT / "dist"
DIST_DIR.mkdir(parents=True, exist_ok=True)

# Normaliza caracteres Unicode que fontes web frequentemente não suportam
_NORMALIZE_MAP = str.maketrans({
    '½': '1/2', '¼': '1/4', '¾': '3/4',
    '⅓': '1/3', '⅔': '2/3', '⅛': '1/8',
    '⅜': '3/8', '⅝': '5/8', '⅞': '7/8',
    '—': '--',  '–': '-',   '’': "'",
    '“': '"',   '”': '"',
})

def _normalize(text: str) -> str:
    return text.translate(_NORMALIZE_MAP)

# Unidades de medida conhecidas para split de amount vs name
_UNITS = (
    "cup", "tbsp", "tsp", "oz", "lb", "g", "kg", "ml",
    "scoop", "slice", "slices", "piece", "pieces",
    "clove", "cloves", "pinch", "dash", "bunch",
    "can", "jar", "large", "medium", "small", "thick",
)
_AMOUNT_RE = re.compile(
    r'^([\d½¼¾⅓⅔⅛⅜⅝⅞/.\s]+'
    r'(?:' + '|'.join(_UNITS) + r')s?'
    r'(?:\s*\([^)]+\))?)\s+(.+)$',
    re.IGNORECASE,
)

def _split_amount(text: str) -> tuple[str, str]:
    m = _AMOUNT_RE.match(text.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return "", text.strip()

def _parse_difficulty(stars: str) -> str:
    return {1: "Easy", 2: "Medium", 3: "Hard"}.get(stars.count("★"), "Easy")

def parse_recipes(md_text: str) -> list[dict]:
    recipes: list[dict] = []
    current_category = "MAIN COURSE"
    recipe: dict | None = None
    section: str | None = None

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()

        # ── Capítulo ────────────────────────────────────────────────────────────
        ch = re.match(r"^# CHAPTER \d+:\s+(.+?)\s+\(", line)
        if ch:
            current_category = ch.group(1).strip().upper()
            continue

        # ── Cabeçalho da receita ─────────────────────────────────────────────
        rh = re.match(r"^## Recipe (\d+)\s+[—–-]\s+(.+)$", line)
        if rh:
            if recipe:
                recipes.append(recipe)
            num = int(rh.group(1))
            recipe = {
                "number":     str(num).zfill(2),
                "name":       _normalize(rh.group(2).strip()),
                "category":   current_category,
                "protein":    "0",
                "time":       "30",
                "difficulty": "Easy",
                "servings":   "2",
                "page":       str(num),
                "ingredients": [],
                "steps":      [],
                "tip":        "",
                "blurb":      "",
            }
            section = None
            continue

        if recipe is None:
            continue

        # ── Linha de stats ───────────────────────────────────────────────────
        st = re.search(r"Protein:.*?~?(\d+)g.*?Prep:.*?(\d+).*?Difficulty:\s*([★☆]+)", line)
        if st:
            recipe["protein"]    = st.group(1)
            recipe["time"]       = st.group(2)
            recipe["difficulty"] = _parse_difficulty(st.group(3))
            continue

        # ── Separadores de seção ─────────────────────────────────────────────
        if re.match(r"^\*\*Ingredients\*\*", line):
            section = "ingredients"; continue
        if re.match(r"^\*\*Instructions\*\*", line):
            section = "instructions"; continue

        # ── Tip (deve vir ANTES do handler de instructions) ─────────────────
        tip = re.match(r"^\*\*Tips?:\*\*\s*(.+)$", line)
        if tip:
            recipe["tip"] = tip.group(1).strip()
            section = None
            continue

        # ── Ingrediente ──────────────────────────────────────────────────────
        if section == "ingredients" and line.startswith("- "):
            amount, name = _split_amount(_normalize(line[2:]))
            recipe["ingredients"].append({"amount": amount, "name": name})
            continue

        # ── Passo de instrução (só linhas que começam com número) ────────────
        if section == "instructions" and re.match(r"^\d+\.", line):
            step = re.sub(r"^\d+\.\s*", "", _normalize(line))
            if step:
                recipe["steps"].append(step)
            continue

    if recipe:
        recipes.append(recipe)

    return recipes


async def build_miolo(recipes: list[dict]) -> list[str]:
    """Renderiza cada receita como PDF individual e retorna lista de paths."""
    pdfs: list[str] = []
    for recipe in recipes:
        out = str(DIST_DIR / f"recipe_{recipe['number']}.pdf")
        await generate_pdf(recipe, out)
        pdfs.append(out)
    return pdfs


def merge_pdfs(input_paths: list[str], output_path: str) -> None:
    import fitz
    doc = fitz.open()
    for p in input_paths:
        with fitz.open(p) as src:
            doc.insert_pdf(src)
    doc.save(output_path)
    doc.close()


def cover_image_to_pdf(image_path: str, output_pdf: str) -> None:
    """Converte JPG/PNG da capa em PDF de página única."""
    import fitz
    img  = fitz.open(image_path)
    rect = img[0].rect if img.page_count > 0 else fitz.Rect(0, 0, 1587, 2245)
    doc  = fitz.open()
    page = doc.new_page(width=rect.width, height=rect.height)
    page.insert_image(rect, filename=image_path)
    doc.save(output_pdf)
    doc.close()


async def main(merge_cover: bool = False, cover_image: str | None = None) -> None:
    md_text = RECIPES_MD.read_text(encoding="utf-8")
    recipes = parse_recipes(md_text)
    print(f"Receitas parseadas: {len(recipes)}")

    recipe_pdfs = await build_miolo(recipes)

    miolo_path = str(DIST_DIR / "high_protein_miolo_kdp.pdf")
    merge_pdfs(recipe_pdfs, miolo_path)
    print(f"Miolo KDP: {miolo_path}  ({len(recipes)} páginas)")

    if merge_cover:
        if not cover_image or not Path(cover_image).exists():
            print("AVISO: --cover-image não fornecido ou arquivo não encontrado. Pulando versão completa.")
            return
        capa_pdf = str(DIST_DIR / "high_protein_cover_kdp.pdf")
        cover_image_to_pdf(cover_image, capa_pdf)
        completo_path = str(DIST_DIR / "high_protein_cookbook_completo.pdf")
        merge_pdfs([capa_pdf, miolo_path], completo_path)
        print(f"Livro completo: {completo_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--merge-cover", action="store_true",
                        help="Inclui capa no PDF final")
    parser.add_argument("--cover-image", type=str, default=None,
                        help="Caminho para a imagem de capa exportada do Canva (JPG ou PNG)")
    args = parser.parse_args()
    asyncio.run(main(merge_cover=args.merge_cover, cover_image=args.cover_image))
