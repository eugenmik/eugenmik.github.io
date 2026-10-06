---
title: "AlloyForge: superalloy design assistant"
description: "A tool for screening heat-resistant nickel, cobalt and iron superalloys, with a search over metallurgy literature."
featured: true
weight: 40
metric: "PHACOMP, CALPHAD and a literature search in one tool"
stack: ["FastAPI", "NiceGUI", "PostgreSQL / pgvector", "pycalphad"]
---

## What it does

AlloyForge takes an alloy composition and checks it in three ways. A PHACOMP engine computes Md, Bo and Nv and estimates the risk of TCP phases. A CALPHAD check with pycalphad and an open thermodynamic database looks at phase stability. A search over metallurgy textbooks, using pgvector and bge-m3 embeddings, finds what the literature says about similar alloys. The results come together in a shortlist with trade-offs and cost, drawn from a reference database of 40 alloys.

{{< figure src="how-it-works.svg" alt="Diagram: an alloy composition goes to PHACOMP screening, a CALPHAD check and a literature search, and the three results feed a shortlist with trade-offs and cost" caption="How AlloyForge combines the three checks." >}}

## Status

AlloyForge is a work in progress.

## Links

The code is on GitHub under the AGPL-3.0 licence: [github.com/eugenmik/alloyforge](https://github.com/eugenmik/alloyforge).
