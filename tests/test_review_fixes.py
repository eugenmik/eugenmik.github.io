"""Regression tests for the final-review findings (2026-10-06)."""
import hashlib
import re
import subprocess

from conftest import POSTS_PUBLISHED, ROOT, requires_drafts, soup, text

# sha256(lower-case name)[:16] of names that must never appear, so the list itself stays private.
DENY_HASHES = {
    "5d4f2123bdb6bf81", "99dbfb2d5e5aa505", "c85edbcb07d59d7c", "4da00f644ac70dc0",
    "5b45c65a44e1cce3", "f003811220cfb9c6", "9466829dbe1e826e",
}


def _denied(body):
    words = re.findall(r"[a-zа-яäöüß]+", body.lower())
    grams = words + [f"{a} {b}" for a, b in zip(words, words[1:])]
    return sorted({g for g in grams if hashlib.sha256(g.encode()).hexdigest()[:16] in DENY_HASHES})


def test_tracked_files_contain_no_denied_names():
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    hits = {}
    for rel in files:
        path = ROOT / rel
        if path.suffix in {".png", ".jpg", ".ico", ".pdf", ".woff", ".woff2", ".ttf"} or "vendor/katex" in rel:
            continue
        try:
            found = _denied(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        if found:
            hits[rel] = len(found)
    assert not hits, hits


def test_built_pages_contain_no_denied_names(prod, drafts):
    for dest, _ in (prod, drafts):
        for path in dest.rglob("*.html"):
            assert not _denied(soup(path.parent, path.name).get_text(" ")), path


@requires_drafts
def test_validation_post_names_ductile_iron(drafts):
    dest, _ = drafts
    body = text(dest, "posts/validating-gpu-solidification-solver/index.html")
    assert "ductile-iron" in body and "cast-steel" not in body


@requires_drafts
def test_validation_post_physics_wording(drafts):
    dest, _ = drafts
    body = text(dest, "posts/validating-gpu-solidification-solver/index.html")
    assert "conductivity (laser flash)" not in body
    assert "test case" in body  # verification table states its test case and integrator


@requires_drafts
def test_voxel_post_does_not_name_the_part(drafts):
    dest, _ = drafts
    assert "hub casting" not in text(dest, "posts/voxels-or-tetrahedra/index.html")


def test_gnn_page_caveats(prod):
    dest, _ = prod
    body = text(dest, "projects/gnn-solidification/index.html")
    assert "up to about 10,000" not in body
    assert "(n = 2)" in body
    assert "not a physical validation" in body


def test_foundryflash_card_and_page_wording(prod):
    dest, _ = prod
    assert "validated to within" not in text(dest, "index.html")
    assert "GNN" in text(dest, "projects/foundryflash/index.html")


def test_alloyforge_symbol_consistent(prod):
    dest, _ = prod
    assert "Md_γ" not in text(dest, "projects/alloyforge/index.html")


def test_legal_discloses_us_processing(prod):
    dest, _ = prod
    assert "United States" in text(dest, "legal/index.html")


def test_writing_page_note_only_without_published_posts(prod):
    dest, _ = prod
    note = "First articles are in review" in text(dest, "posts/index.html")
    assert note != POSTS_PUBLISHED