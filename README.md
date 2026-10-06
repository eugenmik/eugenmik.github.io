# eugenmik.github.io

Personal site of Eugen Miknevic — built with [Hugo](https://gohugo.io) 0.157.0 and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, deployed to GitHub Pages by `.github/workflows/hugo.yml`.

## Everyday tasks

| Task | Command |
|---|---|
| Local preview (with drafts) | `scripts/hugo.sh server -D` → http://localhost:1313 |
| Run all checks | `pip install -r requirements-dev.txt && python3 -m pytest tests -q` |
| New article | create `content/posts/<slug>.md` with front matter `title`, `date`, `description`, `tags`, `draft: true` (`math: true` for formulas) |
| Publish a draft | set `draft: false`, remove its line from `.gitignore`, run the checks, `git add` + commit + push |
| Update the CVs on the site | `scripts/make_web_cv.sh` (rebuilds both PDFs from `~/Projects/CV_2026/2026-10_master`, without phone number) |
| Regenerate photo / social image / icons | `python3 scripts/make_images.py <source-photo.jpg>` |
| Check external links | build to a folder, then `python3 scripts/check_external_links.py <folder>` |

Draft posts are kept out of git (see `.gitignore`) until approved, so the public repository only contains published articles.
