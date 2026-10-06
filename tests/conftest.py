import pathlib
import subprocess

import pytest
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
HUGO = ROOT / "scripts" / "hugo.sh"

# Tests about article content need the article files; drafts may exist only on the owner's disk.
HAS_POSTS = any(p.name != "_index.md" for p in (ROOT / "content" / "posts").glob("*.md"))
requires_drafts = pytest.mark.skipif(not HAS_POSTS, reason="article files are not present in this checkout")
POSTS_PUBLISHED = any("draft: false" in p.read_text(encoding="utf-8")
                      for p in (ROOT / "content" / "posts").glob("*.md") if p.name != "_index.md")


def run_hugo(dest, *extra):
    return subprocess.run(
        [str(HUGO), "--gc", "--minify", "--destination", str(dest), *extra],
        cwd=ROOT, capture_output=True, text=True,
    )


@pytest.fixture(scope="session")
def prod(tmp_path_factory):
    dest = tmp_path_factory.mktemp("public")
    return dest, run_hugo(dest)


@pytest.fixture(scope="session")
def drafts(tmp_path_factory):
    dest = tmp_path_factory.mktemp("public_drafts")
    return dest, run_hugo(dest, "--buildDrafts")


def soup(dest, rel):
    return BeautifulSoup((dest / rel).read_text(encoding="utf-8"), "html.parser")


def text(dest, rel):
    return soup(dest, rel).get_text(" ", strip=True)
