from PIL import Image


def test_photo_size(prod):
    dest, _ = prod
    im = Image.open(dest / "images" / "eugen-miknevic.jpg")
    assert im.size == (600, 750)
    assert (dest / "images" / "eugen-miknevic.jpg").stat().st_size < 150_000


def test_og_image_size(prod):
    dest, _ = prod
    assert Image.open(dest / "images" / "og-default.jpg").size == (1200, 630)


def test_cv_pdfs_present(prod):
    dest, _ = prod
    for name in ("Miknevic_Eugen_CV_EN.pdf", "Miknevic_Eugen_Lebenslauf_DE.pdf"):
        data = (dest / "cv" / name).read_bytes()
        assert data[:5] == b"%PDF-"


def test_katex_vendored(prod):
    dest, _ = prod
    for rel in ("katex.min.css", "katex.min.js", "contrib/auto-render.min.js"):
        assert (dest / "vendor" / "katex" / rel).exists()
    assert any((dest / "vendor" / "katex" / "fonts").glob("*.woff2"))
