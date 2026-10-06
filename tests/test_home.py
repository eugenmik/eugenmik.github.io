from conftest import POSTS_PUBLISHED, ROOT, run_hugo, soup


def test_hero_content(prod):
    dest, _ = prod
    page = soup(dest, "index.html")
    hero = page.select_one(".hero")
    assert "Eugen Miknevic" in hero.get_text()
    assert "AI Engineer for Casting & Manufacturing Simulation" in hero.get_text()
    img = hero.select_one("img.hero-photo")
    assert img["src"].endswith("images/eugen-miknevic.jpg")
    assert img["alt"]


def test_cv_buttons(prod):
    dest, _ = prod
    hrefs = [a["href"] for a in soup(dest, "index.html").select(".hero-buttons a")]
    assert any(h.endswith("cv/Miknevic_Eugen_CV_EN.pdf") for h in hrefs)


def test_home_project_cards(prod):
    dest, _ = prod
    assert len(soup(dest, "index.html").select(".home-section .project-card")) == 4


def test_published_in_strip(prod):
    dest, _ = prod
    links = [a["href"] for a in soup(dest, "index.html").select(".published-in a")]
    assert any("foundrymag.com" in h for h in links)
    assert any("foundry-planet.com" in h for h in links)


def test_home_latest_writing_follows_published_posts(prod):
    dest, _ = prod
    page = soup(dest, "index.html")
    if POSTS_PUBLISHED:
        assert "Latest writing" in page.get_text()
        assert page.select(".post-list li")
    else:
        assert "Latest writing" not in page.get_text()
        assert not page.select(".post-list")


def test_hero_without_photo(tmp_path):
    result = run_hugo(tmp_path, "--config", f"{ROOT}/hugo.toml,{ROOT}/tests/fixtures/no-photo.toml")
    assert result.returncode == 0, result.stderr
    hero = soup(tmp_path, "index.html").select_one(".hero")
    assert hero is not None
    assert hero.select_one("img") is None
