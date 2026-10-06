import re

from conftest import ROOT, requires_drafts, soup

FORBIDDEN = re.compile(r"\bconsult\w*|\bservices?\b|self-employed|freelanc\w*", re.I)
VENDOR_FREE = ["projects/foundryflash/index.html", "posts/validating-gpu-solidification-solver/index.html"]


def _pages(dest):
    return [p for p in dest.rglob("*.html")]


def _visible_text(path):
    page = soup(path.parent, path.name)
    for tag in page(["script", "style"]):
        tag.decompose()
    return page.get_text(" ")


def test_forbidden_words(prod, drafts):
    for dest, _ in (prod, drafts):
        for path in _pages(dest):
            hits = FORBIDDEN.findall(_visible_text(path))
            assert not hits, (path, hits)




@requires_drafts
def test_no_vendor_named_in_validation(drafts):
    dest, _ = drafts
    for rel in VENDOR_FREE:
        body = _visible_text(dest / rel)
        assert "MAGMA" not in body and "ProCAST" not in body, rel


def test_internal_links_resolve(prod, drafts):
    for dest, _ in (prod, drafts):
        for path in _pages(dest):
            page = soup(path.parent, path.name)
            for tag in page.select("[href], [src]"):
                url = tag.get("href") or tag.get("src")
                if url.startswith(("http://", "https://", "mailto:", "#", "data:", "//")):
                    if not url.startswith("https://eugenmik.github.io/"):
                        continue
                    url = url[len("https://eugenmik.github.io"):]
                url = url.split("#")[0].split("?")[0]
                if not url:
                    continue
                target = (dest / url.lstrip("/")) if url.startswith("/") else (path.parent / url)
                if url.endswith("/") or target.is_dir():
                    target = target / "index.html"
                assert target.exists(), (path, url)


def test_posts_section_exists_in_prod(prod):
    dest, _ = prod
    assert (dest / "posts" / "index.html").exists()


def test_no_fixed_widths_over_viewport():
    css = open(ROOT / "assets/css/extended/custom.css", encoding="utf-8").read()
    widths = [int(w) for w in re.findall(r"(?<!max-)(?<!min-)width:\s*(\d+)px", css)]
    assert all(w <= 360 for w in widths), widths
