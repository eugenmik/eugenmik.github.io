from conftest import soup, text

SLUGS = ["foundryflash", "gnn-solidification", "gusscore", "techbookocr", "alloyforge"]


def test_projects_index_lists_four_cards_in_order(prod):
    dest, _ = prod
    cards = soup(dest, "projects/index.html").select(".project-card h3 a")
    assert [a["href"].strip("/").split("/")[-1] for a in cards] == SLUGS


def test_project_pages_exist_with_key_numbers(prod):
    dest, _ = prod
    expected = {
        "foundryflash": ["9.9 s", "44.9 s", "3.7%", "7,500"],
        "gnn-solidification": ["14,437", "0.917", "0.932", "0.738"],
        "gusscore": ["two-plant foundry group", "confirm"],
        "alloyforge": ["PHACOMP", "CALPHAD"],
        "techbookocr": ["Obsidian", "0.997", "12 GB", "library"],
    }
    for slug, needles in expected.items():
        body = text(dest, f"projects/{slug}/index.html")
        for needle in needles:
            assert needle in body, (slug, needle)


def test_github_links(prod):
    dest, _ = prod
    for slug, repo in [("gnn-solidification", "casting-gnn-solidification"),
                       ("gusscore", "gusscore-erp"), ("alloyforge", "alloyforge"),
                       ("techbookocr", "techbookocr")]:
        hrefs = [a["href"] for a in soup(dest, f"projects/{slug}/index.html").select("a[href]")]
        assert f"https://github.com/eugenmik/{repo}" in hrefs, slug


def test_foundryflash_has_no_code_link_and_no_vendor(prod):
    dest, _ = prod
    page = soup(dest, "projects/foundryflash/index.html")
    hrefs = [a["href"] for a in page.select("a[href]")]
    assert not any("github.com/eugenmik/foundryflash" in h for h in hrefs)
    body = page.get_text(" ")
    assert "MAGMA" not in body and "ProCAST" not in body
    assert "private" in body


def test_foundryflash_links_both_publications(prod):
    dest, _ = prod
    hrefs = [a["href"] for a in soup(dest, "projects/foundryflash/index.html").select(".pub-box a")]
    assert any("foundrymag.com" in h for h in hrefs)
    assert any("foundry-planet.com" in h for h in hrefs)
