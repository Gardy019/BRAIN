"""
tools/generate_book_assets.py
Gerador de imagens para o ebook High Protein Cookbook for Beginners
Manifesto visual: Honest Kitchen

Providers suportados:
  1. Pollinations.ai — gratuito, sem API key, executa agora
  2. Gemini Image Generation — requer GEMINI_API_KEY no .env
  3. Stability AI — requer STABILITY_API_KEY no .env

Uso:
  python generate_book_assets.py --asset cover    # gera foto da capa
  python generate_book_assets.py --asset recipe   # gera foto de receita
  python generate_book_assets.py --asset all      # gera todos
"""
import requests
import base64
import json
import os
import time
import argparse
from pathlib import Path
from urllib.parse import quote
from dotenv import dotenv_values

OUT_DIR = Path(r"C:\Users\gardi\OneDrive\Documentos\BRAIN\.tmp")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ENV = dotenv_values(r"C:\Users\gardi\OneDrive\Documentos\BRAIN\.env")

# ── PROMPTS DO MANIFESTO HONEST KITCHEN ──────────────────────────────────────
# Principio: especificidade > genericidade. Cada prompt define luz, angulo, fundo.

PROMPTS = {
    "cover": (
        "Professional food photography, overhead flat lay, high-protein meal bowl, "
        "quinoa with grilled chicken slices, fresh herbs, cherry tomatoes, avocado, "
        "ceramic bowl on rustic linen cloth, warm natural side lighting, "
        "cream and terracotta color palette, neutral off-white background #FAF8F4, "
        "editorial cookbook style, Kinfolk magazine aesthetic, no text, no watermark, "
        "ultra sharp focus, 4K quality, portrait orientation"
    ),
    "cover_alt": (
        "Professional food photography, overhead shot, salmon fillet with roasted vegetables, "
        "asparagus, sweet potato, lemon slices, fresh dill, matte ceramic plate, "
        "sage green napkin, warm morning light from left, "
        "earthy tones, terracotta and cream palette, minimalist editorial style, "
        "no text, no logo, crisp focus, cookbook quality"
    ),
    "recipe_hero": (
        "Close-up food photography, 45-degree angle, lemon herb chicken and quinoa bowl, "
        "vibrant colors, fresh parsley garnish, steam rising gently, "
        "rustic wooden cutting board background, warm side lighting, "
        "sage green and terracotta accent colors, shallow depth of field, "
        "restaurant quality plating, no text, editorial food photography"
    ),
    "breakfast": (
        "Overhead food photography, high-protein Greek yogurt parfait, "
        "layers of thick yogurt, granola, mixed berries, honey drizzle, "
        "white ceramic bowl on marble surface, soft morning light, "
        "fresh and clean aesthetic, no text, cookbook style"
    ),
}


# ── PROVIDER 1: POLLINATIONS.AI (gratuito, sem API key) ──────────────────────

def generate_pollinations(prompt: str, output_path: str, width: int = 600, height: int = 900, seed: int = 42) -> bool:
    """
    Gera imagem via Pollinations.ai — completamente gratuito, sem API key.
    Modelo: flux (melhor qualidade disponivel gratuitamente)
    """
    encoded = quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={width}&height={height}&model=flux&nologo=true"
        f"&seed={seed}&enhance=true"
    )
    print(f"[Pollinations] Gerando: {output_path}")
    print(f"[Pollinations] Prompt: {prompt[:80]}...")

    try:
        response = requests.get(url, timeout=120, stream=True)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        size_kb = Path(output_path).stat().st_size // 1024
        print(f"[Pollinations] Salvo: {output_path} ({size_kb} KB)")
        return True

    except Exception as e:
        print(f"[Pollinations] Erro: {e}")
        return False


# ── PROVIDER 2: GEMINI IMAGE GENERATION ──────────────────────────────────────

def generate_gemini(prompt: str, output_path: str, aspect_ratio: str = "3:4") -> bool:
    """
    Gera imagem via Gemini API (gemini-2.0-flash-exp ou gemini-3.1-flash-image-preview).
    Requer GEMINI_API_KEY no .env
    """
    api_key = ENV.get("GEMINI_API_KEY")
    if not api_key:
        print("[Gemini] GEMINI_API_KEY nao encontrado no .env — usando Pollinations como fallback")
        return False

    # Tenta os modelos de imagem disponiveis
    models = [
        "gemini-2.0-flash-preview-image-generation",
        "gemini-3.1-flash-image-preview",
        "gemini-2.0-flash-exp",
    ]

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": aspect_ratio}
            }
        }

        try:
            print(f"[Gemini] Tentando modelo: {model}")
            response = requests.post(url, json=payload, timeout=90)

            if response.status_code == 404:
                print(f"[Gemini] Modelo {model} nao disponivel, tentando proximo...")
                continue

            response.raise_for_status()
            result = response.json()

            parts = result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            img_part = next((p for p in parts if "inlineData" in p), None)

            if img_part:
                img_data = base64.b64decode(img_part["inlineData"]["data"])
                with open(output_path, "wb") as f:
                    f.write(img_data)
                size_kb = len(img_data) // 1024
                print(f"[Gemini] Gerado com {model}: {output_path} ({size_kb} KB)")
                return True
            else:
                print(f"[Gemini] Sem imagem na resposta do modelo {model}")

        except requests.exceptions.HTTPError as e:
            print(f"[Gemini] HTTP {e.response.status_code} para {model}: {e}")
            continue
        except Exception as e:
            print(f"[Gemini] Erro com {model}: {e}")
            continue

    return False


# ── GERADOR PRINCIPAL ─────────────────────────────────────────────────────────

def generate_asset(asset_type: str, provider: str = "auto") -> str | None:
    """
    Gera ativo visual. Tenta Gemini primeiro se key disponivel, fallback Pollinations.
    Retorna path do arquivo gerado ou None se falhar.
    """
    if asset_type not in PROMPTS:
        print(f"Asset type desconhecido: {asset_type}. Opcoes: {list(PROMPTS.keys())}")
        return None

    prompt = PROMPTS[asset_type]
    output_path = str(OUT_DIR / f"{asset_type}.jpg")

    # Tenta Gemini se tiver API key
    if provider in ("auto", "gemini") and ENV.get("GEMINI_API_KEY"):
        if generate_gemini(prompt, output_path):
            return output_path
        print("[Auto] Gemini falhou, usando Pollinations como fallback...")

    # Pollinations como primary ou fallback
    if provider in ("auto", "pollinations"):
        if generate_pollinations(prompt, output_path):
            return output_path

    print(f"[ERROR] Nenhum provider conseguiu gerar: {asset_type}")
    return None


# ── INTEGRACAO COM COVER HTML ─────────────────────────────────────────────────

def build_cover_with_photo(photo_path: str) -> bool:
    """
    Gera a capa final integrando a foto gerada no HTML v2.
    A foto e embutida como base64 para garantir que o PDF capture corretamente.
    """
    with open(photo_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    cover_gen_path = r"C:\Users\gardi\OneDrive\Documentos\BRAIN\tools\generate_cover_html.py"

    # Le o script atual e substitui o placeholder CSS pelo background-image real
    with open(cover_gen_path, "r", encoding="utf-8") as f:
        cover_code = f.read()

    # Injeta a imagem como background-image no .photo-area
    old_bg = ".photo-area::before {\n    content: '';\n    position: absolute;\n    inset: 0;\n    background: linear-gradient(160deg, #C8D8CB 0%, #A8C4AE 40%, #8BAF92 70%, #6B9472 100%);\n  }"
    new_bg = f".photo-area {{\n    background-image: url('data:image/jpeg;base64,{img_b64}');\n    background-size: cover;\n    background-position: center;\n  }}\n\n  .photo-area::before {{\n    content: '';\n    position: absolute;\n    inset: 0;\n    background: rgba(0,0,0,0.04);\n  }}"

    if old_bg in cover_code:
        new_code = cover_code.replace(old_bg, new_bg)
        # Salva versao com foto real
        final_path = cover_gen_path.replace("generate_cover_html.py", "generate_cover_final.py")
        with open(final_path, "w", encoding="utf-8") as f:
            f.write(new_code)
        print(f"[Cover] Script final gerado: {final_path}")
        return True
    else:
        print("[Cover] Padrao CSS nao encontrado — integrando via arquivo separado")
        # Alternativa: salva o path da foto para o script principal ler
        photo_ref_path = str(OUT_DIR / "cover_photo_path.txt")
        with open(photo_ref_path, "w") as f:
            f.write(photo_path)
        print(f"[Cover] Referencia salva em: {photo_ref_path}")
        return True


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de assets visuais para ebooks")
    parser.add_argument("--asset", default="cover", choices=list(PROMPTS.keys()) + ["all"],
                        help="Tipo de asset a gerar")
    parser.add_argument("--provider", default="auto", choices=["auto", "pollinations", "gemini"],
                        help="Provider de imagem")
    args = parser.parse_args()

    if args.asset == "all":
        for asset_type in PROMPTS.keys():
            path = generate_asset(asset_type, args.provider)
            if path:
                print(f"OK: {path}")
            time.sleep(2)  # rate limit gentil
    else:
        path = generate_asset(args.asset, args.provider)
        if path:
            print(f"\nAsset gerado: {path}")
            # Auto-integra na capa se for cover
            if args.asset in ("cover", "cover_alt"):
                print("\nIntegrando na capa HTML...")
                build_cover_with_photo(path)
                print("Executando geracao da capa final...")
                import subprocess
                final_script = r"C:\Users\gardi\OneDrive\Documentos\BRAIN\tools\generate_cover_final.py"
                if Path(final_script).exists():
                    subprocess.run(["python", final_script], check=False)
                else:
                    subprocess.run(["python", r"C:\Users\gardi\OneDrive\Documentos\BRAIN\tools\generate_cover_html.py"], check=False)
