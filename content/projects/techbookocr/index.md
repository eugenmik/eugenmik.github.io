---
title: "techbookocr: scanned technical books to Markdown"
description: "Local OCR that turns old scanned metallurgy and foundry handbooks into Markdown with tables, formulas and figures, for a knowledge base in Obsidian."
weight: 35
metric: "Numbers F1 0.997 on 31 hand-checked handbook pages"
stack: ["Python", "vLLM", "llama.cpp", "dots.mocr", "Qwen3.5", "OpenTUI"]
---

## Why I built it

I have a very large library of old scanned books on metallurgy and foundry practice. Most of it exists only as DjVu and PDF scans: I can read a page, but I cannot search across books, copy a table or link one handbook to another. I built techbookocr for myself, to turn that library into a knowledge base on my subject in Obsidian.

## What it does

techbookocr reads a DjVu or PDF file in Russian, English or German and writes a Markdown book. Tables become HTML with their merged header cells, formulas become LaTeX, and figures are cropped into separate files, including the small drawings that old handbooks put inside table cells. Every page starts with an anchor that points back to the scan, and a quality report lists each correction the pipeline made and each word the spell checker did not know. Every book gets front matter and a table-of-contents note for Obsidian.

{{< figure src="nbs-page.jpg" width="460" alt="Scanned page 17 of a 1955 U.S. National Bureau of Standards research paper with equations, a table with a two-level header and a plot" caption="A test page from a 1955 U.S. National Bureau of Standards paper (public domain). techbookocr read all 48 numbers in its table correctly and 13 of the 14 equations exactly." >}}

Everything runs on my own computer with one 12 GB GPU, so no book leaves the machine. A layout model (dots.mocr) reads each page, a second detector finds drawings inside tables, and a vision-language model (Qwen3.5-9B in llama.cpp) settles the blocks where readings disagree. Fixed rules then check every change that model wants to make: a changed digit, deleted text or a technical term replaced by an everyday word is rejected, and the printed text stays. A queue daemon works through the library one book after another and can run for weeks, and a terminal panel shows its progress.

## Results

On 31 hand-checked pages from Russian foundry handbooks, mostly tables with formulas and figures, compared with the best single model:

| | Character error rate | Numbers F1 | Table structure (TEDS) | Seconds per page |
|---|---|---|---|---|
| dots.mocr alone | 0.148 | 0.882 | 0.824 | 26 |
| techbookocr, default mode | 0.027 | 0.997 | 0.883 | 43 |

A 750-page handbook takes about 11 hours on an RTX 3060. Formulas are the weak spot: their character error rate (0.41) is no better than the single model's. A value printed once for several table columns is also sometimes assigned to only one of them. The code has more than 600 tests.

## Links

The code is on GitHub under the MIT licence: [github.com/eugenmik/techbookocr](https://github.com/eugenmik/techbookocr).
