"""Build web images from the owner's source photo.

Usage: python3 scripts/make_images.py /home/eugen/Projects/CV_2026/addons/Beitragsbild_Eugen_Miknevic.jpg
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "static" / "images"
FONT_DIR = pathlib.Path("/usr/share/fonts/truetype/crosextra")
ACCENT = (31, 78, 121)


def main(src):
    OUT.mkdir(parents=True, exist_ok=True)
    photo = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    portrait = ImageOps.fit(photo, (600, 750), Image.LANCZOS, centering=(0.5, 0.35))
    portrait.save(OUT / "eugen-miknevic.jpg", quality=82, optimize=True, progressive=True)

    og = Image.new("RGB", (1200, 630), (255, 255, 255))
    og.paste(ImageOps.fit(photo, (504, 630), Image.LANCZOS, centering=(0.5, 0.35)), (0, 0))
    draw = ImageDraw.Draw(og)
    bold = ImageFont.truetype(str(FONT_DIR / "Carlito-Bold.ttf"), 64)
    regular = ImageFont.truetype(str(FONT_DIR / "Carlito-Regular.ttf"), 34)
    draw.text((560, 200), "Eugen Miknevic", font=bold, fill=(34, 34, 34))
    draw.text((560, 290), "AI Engineer for Casting &", font=regular, fill=ACCENT)
    draw.text((560, 334), "Manufacturing Simulation", font=regular, fill=ACCENT)
    draw.text((560, 410), "eugenmik.github.io", font=regular, fill=(90, 90, 90))
    og.save(OUT / "og-default.jpg", quality=85, optimize=True)
    make_icons()


def make_icons():
    """Monogram icons that PaperMod's head links to (favicon.ico, PNGs, mask icon)."""
    static = ROOT / "static"
    big = Image.new("RGB", (512, 512), ACCENT)
    draw = ImageDraw.Draw(big)
    font = ImageFont.truetype(str(FONT_DIR / "Carlito-Bold.ttf"), 290)
    box = draw.textbbox((0, 0), "EM", font=font)
    x = (512 - (box[2] - box[0])) / 2 - box[0]
    y = (512 - (box[3] - box[1])) / 2 - box[1]
    draw.text((x, y), "EM", font=font, fill=(255, 255, 255))
    big.resize((180, 180), Image.LANCZOS).save(static / "apple-touch-icon.png")
    big.resize((32, 32), Image.LANCZOS).save(static / "favicon-32x32.png")
    big.resize((16, 16), Image.LANCZOS).save(static / "favicon-16x16.png")
    big.save(static / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    (static / "safari-pinned-tab.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">'
        '<rect width="16" height="16" rx="3" fill="#000"/></svg>\n'
    )


if __name__ == "__main__":
    main(sys.argv[1])
