import pytest
from conftest import soup

PAGES = ["index.html", "about/index.html", "projects/index.html"]


@pytest.mark.parametrize("rel", PAGES)
def test_theme_toggle_sits_at_the_end_of_the_nav(prod, rel):
    dest, _ = prod
    page = soup(dest, rel)
    assert len(page.select("#theme-toggle")) == 1
    assert page.select_one(".logo #theme-toggle") is None, "toggle still next to the site name"
    items = page.select_one("nav.header-nav ul#menu").find_all("li", recursive=False)
    assert [li.get_text(strip=True) for li in items[:4]] == [
        "Writing", "Projects", "Publications", "About",
    ]
    assert items[-1].select_one("#theme-toggle") is not None, "toggle is not the last nav item"


def test_theme_toggle_keeps_its_label_and_shortcut(prod):
    dest, _ = prod
    button = soup(dest, "index.html").select_one("#theme-toggle")
    assert button.get("aria-label") == "Toggle theme"
    # bs4 reports accesskey as a list of tokens.
    assert button.get("accesskey") in ("t", ["t"])
    assert button.select_one("svg.moon") and button.select_one("svg.sun")


def test_name_carries_the_professional_title(prod):
    dest, _ = prod
    page = soup(dest, "index.html")
    assert page.select_one("nav.header-nav .logo a").get_text(strip=True) == "Eugen Miknevic, Ing."
    assert page.select_one(".hero h1").get_text(strip=True) == "Eugen Miknevic, Ing."
    # The legal name stays in metadata: page titles, feeds and structured data.
    assert page.select_one("title").get_text(strip=True) == "Eugen Miknevic"
    assert page.select_one('meta[property="og:title"]')["content"] == "Eugen Miknevic"
