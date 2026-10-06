#!/usr/bin/env bash
# Builds web copies of the CVs without the phone number into static/cv/.
# Source: ~/Projects/CV_2026/2026-10_master/*.tex (the application PDFs keep the phone).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${CV_SRC:-$HOME/Projects/CV_2026/2026-10_master}"
tmp="$(mktemp -d)"
build() {  # $1 source basename, $2 target name
  sed '/href{tel:/d' "$SRC/$1.tex" > "$tmp/$1.tex"
  (cd "$tmp" && xelatex -interaction=nonstopmode "$1.tex" >/dev/null)
  cp "$tmp/$1.pdf" "$ROOT/static/cv/$2"
}
build Miknevic_Eugen_CV_2026-10 Miknevic_Eugen_CV_EN.pdf
build Miknevic_Eugen_Lebenslauf_2026-10 Miknevic_Eugen_Lebenslauf_DE.pdf
rm -rf "$tmp"
