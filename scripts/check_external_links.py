"""Report the HTTP status of every external link in a built site (manual check).

Usage: python3 scripts/check_external_links.py public
"""
import pathlib
import sys

import requests
from bs4 import BeautifulSoup

SKIP = ("https://eugenmik.github.io",)
HEADERS = {"User-Agent": "Mozilla/5.0 (link check for eugenmik.github.io)"}


def main(root):
    urls = set()
    for path in pathlib.Path(root).rglob("*.html"):
        page = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for a in page.select("a[href^=http]"):
            if not a["href"].startswith(SKIP):
                urls.add(a["href"])
    bad = 0
    for url in sorted(urls):
        try:
            status = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True).status_code
        except requests.RequestException as exc:
            status = f"error: {exc.__class__.__name__}"
        print(f"{status}\t{url}")
        if status != 200:
            bad += 1
    print(f"{len(urls)} external links, {bad} not 200")


if __name__ == "__main__":
    main(sys.argv[1])
