from conftest import soup

EXPECTED = [
    ("https://linkedin.com/in/eugenmiknevic", "Linkedin"),
    ("https://github.com/eugenmik", "Github"),
    ("https://huggingface.co/eugenmik", "Hugging Face"),
    ("mailto:eugenmiknevic@gmail.com", "Email"),
]


def icons(dest):
    return soup(dest, "index.html").select(".social-icons a")


def test_social_icon_links_and_order(prod):
    dest, _ = prod
    assert [(a["href"], a["title"]) for a in icons(dest)] == EXPECTED


def test_every_social_icon_renders_a_glyph(prod):
    dest, _ = prod
    for a in icons(dest):
        svg = a.select_one("svg")
        assert svg is not None, f"no glyph for {a['href']}"
        assert svg.get("viewbox") or svg.get("viewBox"), f"no viewBox for {a['href']}"


def test_huggingface_glyph_matches_theme_icon_style(prod):
    dest, _ = prod
    a = soup(dest, "index.html").select_one('.social-icons a[href="https://huggingface.co/eugenmik"]')
    svg = a.select_one("svg")
    # Same 24x24 grid and currentColor fill as the theme's own brand glyphs,
    # so it inherits size and both colour schemes without extra CSS.
    assert (svg.get("viewbox") or svg.get("viewBox")) == "0 0 24 24"
    assert svg.get("fill") == "currentColor"
    # Stroked on top of the fill so its line weight matches the icons beside it.
    assert svg.get("stroke") == "currentColor"
    assert float(svg.get("stroke-width")) >= 0.5
