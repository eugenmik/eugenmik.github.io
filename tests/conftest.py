import pathlib
import subprocess

import pytest
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
HUGO = ROOT / "scripts" / "hugo.sh"

# Draft posts live only on the owner's disk (git-ignored until approved), so CI has none.
HAS_DRAFTS = any("draft: true" in p.read_text(encoding="utf-8")
                 for p in (ROOT / "content" / "posts").glob("*.md") if p.name != "_index.md")
requires_drafts = pytest.mark.skipif(not HAS_DRAFTS, reason="draft posts are kept locally, not in git")


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
