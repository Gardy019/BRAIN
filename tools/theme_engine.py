"""
theme_engine.py — load and apply themes from themes/*.json

Usage (as module):
    from tools.theme_engine import load_theme, colors, mm

Usage (standalone test):
    python tools/theme_engine.py high-protein-cookbook
"""

import json
import os
import sys
from pathlib import Path

THEMES_DIR = Path(__file__).parent.parent / "themes"


def load_theme(slug: str) -> dict:
    path = THEMES_DIR / f"{slug}.json"
    if not path.exists():
        available = [p.stem for p in THEMES_DIR.glob("*.json")]
        raise FileNotFoundError(
            f"Theme '{slug}' not found. Available: {available}"
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    """Return (r, g, b) as 0–1 floats for ReportLab."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return r / 255, g / 255, b / 255


def mm(value_mm: float) -> float:
    """Convert millimetres to ReportLab points (1mm = 2.8346pt)."""
    return value_mm * 2.8346


def build_reportlab_styles(theme: dict):
    """
    Return a dict of ReportLab ParagraphStyles keyed by role.
    Requires: pip install reportlab
    """
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.colors import HexColor

    c = theme["colors"]
    typo = theme["typography"]

    return {
        "title": ParagraphStyle(
            "title",
            fontName=typo["heading"]["fallback"].split(",")[0].strip(),
            fontSize=typo["heading"]["size_title"],
            textColor=HexColor(c["text_on_background"]),
            leading=typo["heading"]["size_title"] * 1.2,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName=typo["heading"]["fallback"].split(",")[0].strip(),
            fontSize=typo["heading"]["size_h1"],
            textColor=HexColor(c["primary"]),
            leading=typo["heading"]["size_h1"] * 1.3,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName=typo["heading"]["fallback"].split(",")[0].strip(),
            fontSize=typo["heading"]["size_h2"],
            textColor=HexColor(c["primary"]),
            leading=typo["heading"]["size_h2"] * 1.4,
        ),
        "body": ParagraphStyle(
            "body",
            fontName=typo["body"]["fallback"].split(",")[0].strip(),
            fontSize=typo["body"]["size_normal"],
            textColor=HexColor(c["text_on_background"]),
            leading=typo["body"]["size_normal"] * typo["body"]["line_height"],
        ),
        "small": ParagraphStyle(
            "small",
            fontName=typo["body"]["fallback"].split(",")[0].strip(),
            fontSize=typo["body"]["size_small"],
            textColor=HexColor(c["muted"]),
            leading=typo["body"]["size_small"] * typo["body"]["line_height"],
        ),
        "label": ParagraphStyle(
            "label",
            fontName=typo["body"]["fallback"].split(",")[0].strip(),
            fontSize=typo["accent_label"]["size"],
            textColor=HexColor(c["muted"]),
            leading=typo["accent_label"]["size"] * 1.4,
        ),
    }


def page_size(theme: dict) -> tuple[float, float]:
    """Return (width_pt, height_pt) for ReportLab SimpleDocTemplate."""
    layout = theme["layout"]
    return mm(layout["page_width_mm"]), mm(layout["page_height_mm"])


def margins(theme: dict) -> dict[str, float]:
    """Return margin dict in points, keyed top/bottom/inner/outer."""
    layout = theme["layout"]
    return {
        "top":    mm(layout["margin_top_mm"]),
        "bottom": mm(layout["margin_bottom_mm"]),
        "inner":  mm(layout["margin_inner_mm"]),
        "outer":  mm(layout["margin_outer_mm"]),
    }


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "high-protein-cookbook"
    theme = load_theme(slug)

    print(f"\nTheme: {theme['name']}")
    print(f"Description: {theme['description']}\n")

    print("Colors:")
    for key, value in theme["colors"].items():
        rgb = hex_to_rgb(value)
        print(f"  {key:<25} {value}  ->  rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})")

    layout = theme["layout"]
    w, h = mm(layout["page_width_mm"]), mm(layout["page_height_mm"])
    print(f"\nPage size: {layout['page_width_mm']}mm x {layout['page_height_mm']}mm  ({w:.1f}pt x {h:.1f}pt)")
    print(f"Margins: top={layout['margin_top_mm']}mm  bottom={layout['margin_bottom_mm']}mm  "
          f"inner={layout['margin_inner_mm']}mm  outer={layout['margin_outer_mm']}mm")
