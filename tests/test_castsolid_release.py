"""The castsolid-gnn release: public weights on Hugging Face, renamed repo (2026-10-09)."""
import re
import subprocess

import pytest

from conftest import ROOT, soup, text

PAGE = "projects/castsolid-gnn/index.html"
HF = "https://huggingface.co/eugenmik/castsolid-gnn"
GH = "https://github.com/eugenmik/castsolid-gnn"


def test_project_page_moved_and_old_url_redirects(prod):
    dest, _ = prod
    assert (dest / "projects" / "castsolid-gnn" / "index.html").exists()
    old = dest / "projects" / "gnn-solidification" / "index.html"
    assert old.exists(), "the published URL must keep working"
    assert "castsolid-gnn" in old.read_text(encoding="utf-8")


def test_page_links_model_and_code(prod):
    dest, _ = prod
    hrefs = [a["href"] for a in soup(dest, PAGE).select("a[href]")]
    assert any(h.startswith(HF) for h in hrefs)
    assert GH in hrefs


def test_weights_described_as_public(prod):
    dest, _ = prod
    body = text(dest, PAGE)
    assert "Apache-2.0" in body
    assert "not public" not in body


def test_unsupported_assembly_claim_is_gone(prod, drafts):
    for dest, _ in (prod, drafts):
        for path in dest.rglob("*.html"):
            body = soup(path.parent, path.name).get_text(" ")
            assert "0.932" not in body, path
            assert "sleeve assemblies" not in body, path


def test_numbers_match_the_model_card(prod):
    dest, _ = prod
    body = text(dest, PAGE)
    for needle in ["14,937", "0.917", "0.738", "4.26", "1.85"]:
        assert needle in body, needle


def test_page_keeps_the_honest_caveats(prod):
    dest, _ = prod
    body = text(dest, PAGE)
    assert "0.035" in body, "the one real part that scored badly"
    assert "not evidence of physical accuracy" in body


def test_new_sources_are_reachable_from_the_site(prod):
    dest, _ = prod
    home = [a["href"] for a in soup(dest, "index.html").select(".project-card a, .post-list a")]
    assert any("castsolid-gnn" in h for h in home)


def test_release_post_exists_and_links_the_model(prod):
    dest, _ = prod
    post = dest / "posts" / "publishing-a-casting-model" / "index.html"
    assert post.exists()
    page = soup(post.parent, post.name)
    hrefs = [a["href"] for a in page.select("a[href]")]
    assert any(h.startswith(HF) for h in hrefs)
    body = page.get_text(" ")
    assert "safetensors" in body and "Apache-2.0" in body


def _pdf_text(path):
    return subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, check=True).stdout


def test_published_cvs_point_to_the_new_repo_and_model():
    """The PDFs the site serves are the artifact visitors download."""
    for name in ("Miknevic_Eugen_CV_EN.pdf", "Miknevic_Eugen_Lebenslauf_DE.pdf"):
        body = _pdf_text(ROOT / "static" / "cv" / name)
        assert "castsolid-gnn" in body, name
        assert "0,932" not in body and "0.932" not in body, name


CV_SRC = ROOT.parent / "CV_2026" / "2026-10_master"


@pytest.mark.skipif(not CV_SRC.is_dir(), reason="CV LaTeX sources live on the owner's machine only")
def test_cv_sources_point_to_the_new_repo_and_model():
    for name in ("Miknevic_Eugen_CV_2026-10.tex", "Miknevic_Eugen_Lebenslauf_2026-10.tex"):
        tex = (CV_SRC / name).read_text(encoding="utf-8")
        assert "casting-gnn-solidification" not in tex, name
        assert "huggingface.co/eugenmik/castsolid-gnn" in tex, name
        assert "0,932" not in tex and "0.932" not in tex, name


def test_no_stale_test_count_claim(prod):
    dest, _ = prod
    body = text(dest, PAGE)
    assert not re.search(r"300\+? tests", body)


def test_page_shows_the_model_output(prod):
    dest, _ = prod
    vid = soup(dest, PAGE).select_one(".post-video video")
    assert vid is not None
    for attr in ("autoplay", "muted", "loop", "playsinline", "poster"):
        assert vid.has_attr(attr), attr
    assert vid.select_one("source")["src"].endswith("castsolid-playback.mp4")
    assert (dest / "media" / "castsolid-playback.mp4").exists()
