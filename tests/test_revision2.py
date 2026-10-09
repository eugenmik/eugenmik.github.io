"""Owner's review round 2 (2026-10-06)."""
import re

from conftest import soup, text

SLUGS = ["foundryflash", "castsolid-gnn", "gusscore", "techbookocr", "alloyforge"]
PROSE = ".post-content, .hero, .home-section, .home-video, .page-header, .pub-entry, .project-card, .post-description, .pub-box"


def test_hero_offers_only_english_cv(prod):
    dest, _ = prod
    hrefs = [a["href"] for a in soup(dest, "index.html").select(".hero-buttons a")]
    assert any(h.endswith("cv/Miknevic_Eugen_CV_EN.pdf") for h in hrefs)
    assert not any("Lebenslauf" in h for h in hrefs)


def test_about_keeps_german_cv(prod):
    dest, _ = prod
    hrefs = [a["href"] for a in soup(dest, "about/index.html").select("a[href]")]
    assert any(h.endswith("cv/Miknevic_Eugen_Lebenslauf_DE.pdf") for h in hrefs)


def test_hero_mentions_software_tools_briefly(prod):
    dest, _ = prod
    sub = soup(dest, "index.html").select_one(".hero-subline").get_text(" ", strip=True)
    assert "software tools" in sub and "metallurgy" in sub
    assert len(sub) <= 190, len(sub)


def test_video_between_hero_and_projects(prod):
    dest, _ = prod
    main = soup(dest, "index.html").select_one("main")
    order = [el.get("class", [""])[0] for el in main.find_all(recursive=False)]
    assert order.index("hero") < order.index("home-video") < order.index("home-section"), order
    videos = main.select(".home-video video")
    assert {v.get("data-scheme") for v in videos} == {"light", "dark"}
    for v in videos:
        for attr in ("autoplay", "muted", "loop", "playsinline", "poster"):
            assert v.has_attr(attr), attr
        src = v.select_one("source")["src"]
        assert src.endswith(".mp4") and (dest / src.lstrip("/")).exists(), src


def test_every_project_page_has_an_image(prod):
    dest, _ = prod
    for slug in SLUGS:
        imgs = soup(dest, f"projects/{slug}/index.html").select(".post-content img")
        assert imgs, slug
        assert all(i.get("alt") for i in imgs), slug


def test_about_page_revision(prod):
    dest, _ = prod
    page = soup(dest, "about/index.html")
    body = page.get_text(" ")
    headings = [h.get_text(strip=True) for h in page.select(".post-content h2")]
    assert "Languages" not in headings
    assert "WandelBAR" not in body
    assert "1,000" in body
    assert "3D printing" in body
    assert "RAG" not in body
    assert "revolution" in body


def test_alloyforge_has_no_accuracy_claims(prod):
    dest, _ = prod
    for rel in ("projects/alloyforge/index.html", "index.html", "projects/index.html"):
        body = text(dest, rel)
        assert "0.05 eV" not in body and "ranking" not in body, rel


def test_prose_has_no_dashes_or_arrows(prod, drafts):
    for dest, _ in (prod, drafts):
        for path in dest.rglob("*.html"):
            for el in soup(path.parent, path.name).select(PROSE):
                for code in el.select("code, pre, .katex"):
                    code.decompose()
                found = re.findall(r"[—–→“”]", el.get_text(" "))
                assert not found, (path, found, el.get_text(" ")[:120])
