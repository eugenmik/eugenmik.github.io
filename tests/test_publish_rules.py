"""Owner decisions before publishing (2026-10-06)."""
import subprocess

from conftest import ROOT


def test_web_cvs_have_no_phone_number():
    for name in ("Miknevic_Eugen_CV_EN.pdf", "Miknevic_Eugen_Lebenslauf_DE.pdf"):
        out = subprocess.run(["pdftotext", str(ROOT / "static" / "cv" / name), "-"],
                             capture_output=True, text=True, check=True).stdout
        assert "eugenmiknevic@gmail.com" in out, name
        assert "157" not in out and "+49" not in out, name


def test_no_draft_post_is_tracked():
    tracked = subprocess.run(["git", "ls-files", "content/posts"], cwd=ROOT,
                             capture_output=True, text=True).stdout.split()
    drafts = [p for p in tracked if "draft: true" in (ROOT / p).read_text(encoding="utf-8")]
    assert not drafts, drafts
