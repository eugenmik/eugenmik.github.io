import json

from conftest import POSTS_PUBLISHED, ROOT, requires_drafts, soup, text

POSTS = ["validating-gpu-solidification-solver", "voxels-or-tetrahedra", "human-in-the-loop-ai-foundry-floor"]


def test_publications_page(prod):
    dest, _ = prod
    page = soup(dest, "publications/index.html")
    entries = page.select(".pub-entry")
    assert len(entries) == 2
    assert "12,373" in page.get_text()


def test_about_page(prod):
    dest, _ = prod
    body = text(dest, "about/index.html")
    for needle in ["SLR-Elsterheide", "Head of Design & Metallurgy", "Turing College", "M.Sc. Foundry Engineering"]:
        assert needle in body, needle
    hrefs = [a["href"] for a in soup(dest, "about/index.html").select("a[href]")]
    assert any(h.endswith("cv/Miknevic_Eugen_CV_EN.pdf") for h in hrefs)


def test_legal_page(prod):
    dest, _ = prod
    body = text(dest, "legal/index.html")
    assert "Eugen Miknevic" in body and "Senftenberg" in body and "eugenmiknevic@gmail.com" in body
    assert "GitHub Pages" in body and "cookies" in body


def test_search_page(prod):
    dest, _ = prod
    assert (dest / "search" / "index.html").exists()
    assert (dest / "index.json").exists()


def test_footer_links(prod):
    dest, _ = prod
    hrefs = [a["href"] for a in soup(dest, "index.html").select("footer a")]
    assert any(h.rstrip("/").endswith("/legal") for h in hrefs)
    assert any(h.rstrip("/").endswith("/search") for h in hrefs)


def test_only_published_posts_reach_prod(prod):
    dest, _ = prod
    for path in (ROOT / "content" / "posts").glob("*.md"):
        if path.name == "_index.md":
            continue
        is_draft = "draft: true" in path.read_text(encoding="utf-8")
        assert (dest / "posts" / path.stem).exists() != is_draft, path.name


@requires_drafts
def test_drafts_render_with_publication_links(drafts):
    dest, _ = drafts
    for slug in POSTS:
        hrefs = [a["href"] for a in soup(dest, f"posts/{slug}/index.html").select(".pub-box a")]
        assert any("foundrymag.com" in h for h in hrefs), slug
        assert any("foundry-planet.com" in h for h in hrefs), slug


@requires_drafts
def test_katex_only_on_math_pages(drafts):
    dest, _ = drafts
    math_page = str(soup(dest, "posts/validating-gpu-solidification-solver/index.html"))
    assert "/vendor/katex/katex.min.js" in math_page
    assert "/vendor/katex/katex.min.js" not in str(soup(dest, "about/index.html"))


def test_home_jsonld_person(prod):
    dest, _ = prod
    tags = soup(dest, "index.html").select('script[type="application/ld+json"]')
    people = [json.loads(t.string) for t in tags if '"Person"' in t.string]
    assert people and people[0]["name"] == "Eugen Miknevic"
    assert "https://github.com/eugenmik" in people[0]["sameAs"]


@requires_drafts
def test_related_post_links_follow_publication(prod, drafts):
    prod_dest, _ = prod
    drafts_dest, _ = drafts
    in_prod = soup(prod_dest, "projects/foundryflash/index.html").select(".related-post a")
    assert bool(in_prod) == POSTS_PUBLISHED
    links = soup(drafts_dest, "projects/foundryflash/index.html").select(".related-post a")
    assert links and links[0]["href"].rstrip("/").endswith("validating-gpu-solidification-solver")


@requires_drafts
def test_home_shows_writing_in_drafts_build(drafts):
    dest, _ = drafts
    assert len(soup(dest, "index.html").select(".post-list li")) == 3
