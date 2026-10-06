#!/usr/bin/env bash
# Runs the pinned Hugo version; downloads it into .bin/ on first use.
set -euo pipefail
HUGO_VERSION=0.157.0
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$ROOT/.bin/hugo-$HUGO_VERSION"
if [ ! -x "$BIN" ]; then
  mkdir -p "$ROOT/.bin"
  tmp="$(mktemp -d)"
  curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" | tar xz -C "$tmp" hugo
  mv "$tmp/hugo" "$BIN"
  rm -rf "$tmp"
fi
exec "$BIN" "$@"
