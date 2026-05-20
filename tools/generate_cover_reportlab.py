"""
Capa do ebook: High Protein Cookbook for Beginners
Abordagem 1: reportlab
Manifesto visual: Honest Kitchen
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUT = r"C:\Users\gardi\OneDrive\Documentos\BRAIN\.tmp\cover_reportlab.pdf"

# Paleta Honest Kitchen
BG       = HexColor("#FAF8F4")
CHARCOAL = HexColor("#2C2C2C")
TERRA    = HexColor("#C4622D")
SAGE     = HexColor("#6B8F71")
DIVIDER  = HexColor("#E8E0D5")

# KDP ebook cover: 2560 x 1600 px → usamos 6x9 polegadas (proporção aproximada)
W, H = 6*inch, 9*inch

c = canvas.Canvas(OUT, pagesize=(W, H))

# --- BACKGROUND ---
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)

# --- FAIXA LATERAL TERRACOTA (acento vertical esquerdo) ---
c.setFillColor(TERRA)
c.rect(0, 0, 0.08*inch, H, fill=1, stroke=0)

# --- BLOCO DE FOTO SIMULADO (retângulo sage como placeholder de foto) ---
# Lado esquerdo, altura media
photo_w = W * 0.52
photo_h = H * 0.62
photo_x = 0
photo_y = H * 0.19

c.setFillColor(HexColor("#D4E0D8"))  # verde claro como placeholder
c.rect(photo_x, photo_y, photo_w, photo_h, fill=1, stroke=0)

# Texto placeholder na foto
c.setFillColor(SAGE)
c.setFont("Helvetica", 9)
c.drawCentredString(photo_w/2, photo_y + photo_h/2, "[food photo]")

# --- LINHA DIVISÓRIA VERTICAL ---
c.setStrokeColor(DIVIDER)
c.setLineWidth(1)
c.line(photo_w + 0.1*inch, H*0.12, photo_w + 0.1*inch, H*0.88)

# --- ÁREA DE TEXTO (lado direito) ---
tx = photo_w + 0.25*inch
tw = W - tx - 0.3*inch

# Número do receituário — pequeno acento no topo
c.setFillColor(TERRA)
c.setFont("Helvetica", 8)
c.drawString(tx, H - 0.5*inch, "EST. 2026")

# Tag categoria
c.setFillColor(SAGE)
c.setFont("Helvetica-Bold", 7)
c.drawString(tx, H - 0.75*inch, "COOKBOOK")

# Linha fina sage sob tag
c.setStrokeColor(SAGE)
c.setLineWidth(0.5)
c.line(tx, H - 0.82*inch, tx + tw, H - 0.82*inch)

# Título principal — HIGH PROTEIN
c.setFillColor(CHARCOAL)
c.setFont("Helvetica-Bold", 28)
title_y = H - 1.5*inch
c.drawString(tx, title_y, "HIGH")

c.setFillColor(TERRA)
c.setFont("Helvetica-Bold", 28)
c.drawString(tx, title_y - 0.45*inch, "PROTEIN")

c.setFillColor(CHARCOAL)
c.setFont("Helvetica-Bold", 22)
c.drawString(tx, title_y - 0.9*inch, "COOKBOOK")

# Linha divisória terracota
c.setStrokeColor(TERRA)
c.setLineWidth(1.5)
line_y = title_y - 1.1*inch
c.line(tx, line_y, tx + tw * 0.8, line_y)

# FOR BEGINNERS
c.setFillColor(CHARCOAL)
c.setFont("Helvetica", 10)
c.drawString(tx, line_y - 0.25*inch, "FOR BEGINNERS")

# Subtítulo
c.setFillColor(HexColor("#6B6B6B"))
c.setFont("Helvetica", 8)
subtitle_y = line_y - 0.65*inch
# Quebra manual do subtítulo
c.drawString(tx, subtitle_y, "50 Easy Recipes to Build")
c.drawString(tx, subtitle_y - 0.18*inch, "Muscle & Eat Well")

# Ícones de benefícios (círculos sage com texto)
benefits = ["HIGH PROTEIN", "30 MIN MEALS", "BEGINNER\nFRIENDLY"]
benefit_y = H * 0.38
circle_r = 0.28*inch
spacing = (tw + 0.1*inch) / 3

for i, b in enumerate(benefits):
    cx = tx + i * spacing + circle_r
    cy = benefit_y
    c.setFillColor(SAGE)
    c.circle(cx, cy, circle_r, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 5.5)
    lines = b.split("\n")
    for j, l in enumerate(lines):
        c.drawCentredString(cx, cy + 4 - j*8, l)

# Rodapé com linha sage
footer_y = H * 0.1
c.setStrokeColor(SAGE)
c.setLineWidth(0.5)
c.line(tx, footer_y + 0.15*inch, tx + tw, footer_y + 0.15*inch)

c.setFillColor(HexColor("#9B9B9B"))
c.setFont("Helvetica", 7)
c.drawString(tx, footer_y, "High Protein Cookbook for Beginners")

# Canto inferior direito — marca d'água sutil
c.setFillColor(DIVIDER)
c.setFont("Helvetica", 6)
c.drawRightString(W - 0.15*inch, 0.12*inch, "honest kitchen")

c.save()
print(f"PDF gerado: {OUT}")
