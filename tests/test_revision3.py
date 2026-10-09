"""Owner's review round 3 (2026-10-06)."""
import json
import subprocess

from conftest import ROOT, soup, text


def _duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(json.loads(out)["format"]["duration"])


def test_videos_play_twice_as_fast():
    for scheme in ("light", "dark"):
        assert _duration(ROOT / "static" / "media" / f"solidification-{scheme}.mp4") < 7.0


def test_video_has_no_caption(prod):
    dest, _ = prod
    assert not soup(dest, "index.html").select(".home-video figcaption")


def test_footer_has_about_and_no_theme_credit(prod):
    dest, _ = prod
    footer = soup(dest, "index.html").select_one("footer")
    assert "Powered by" not in footer.get_text()
    assert any(a["href"].rstrip("/").endswith("/about") for a in footer.select("a[href]"))


def test_about_uses_since_2006(prod):
    dest, _ = prod
    body = text(dest, "about/index.html")
    assert "Since 2006" in body and "For twenty years" not in body


def test_home_projects_heading(prod):
    dest, _ = prod
    headings = [h.get_text(strip=True) for h in soup(dest, "index.html").select(".home-section h2")]
    assert "My projects" in headings and "Selected projects" not in headings


def test_theme_follows_system_setting():
    config = (ROOT / "hugo.toml").read_text(encoding="utf-8")
    assert 'defaultTheme = "auto"' in config
    css = (ROOT / "assets/css/extended/custom.css").read_text(encoding="utf-8")
    assert "prefers-color-scheme: dark" in css


def test_hero_says_since_2006(prod):
    dest, _ = prod
    sub = soup(dest, "index.html").select_one(".hero-subline").get_text(" ", strip=True)
    assert "since 2006" in sub and "20 years" not in sub


def test_russian_howto_stays_local():
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    assert "ARTICLES_HOWTO.md" not in tracked
    assert "ARTICLES_HOWTO" not in (ROOT / "README.md").read_text(encoding="utf-8")


def test_home_shows_only_featured_projects(prod):
    dest, _ = prod
    home = [a["href"].strip("/").split("/")[-1] for a in soup(dest, "index.html").select(".home-section .project-card h3 a")]
    assert home == ["foundryflash", "castsolid-gnn", "gusscore", "alloyforge"]
    assert len(soup(dest, "projects/index.html").select(".project-card")) == 5
