---
title: "GussCore: AI-assisted foundry ERP/MES"
description: "Production management for iron and steel foundries. Workers report by voice or photo, and a person confirms every AI proposal."
featured: true
weight: 30
metric: "Piloted at a two-plant foundry group"
stack: ["FastAPI", "SvelteKit", "PostgreSQL", "Ollama", "Whisper"]
---

## The problem

In many foundries, shop-floor data arrives late or not at all. Nobody types a report on a terminal in foundry gloves, so heats, moulds, scrap and chemistry get reconstructed from paper at the end of the shift.

## What I built

GussCore follows a casting from catalogue and order through the weekly plan, the production batch, the melt shop and quality control to shipment, and compares planned with actual cost.

{{< figure src="weekly-plan.jpg" alt="GussCore weekly work plan with one card per day listing planned castings, order numbers and quantities" caption="Weekly work plan in the public demo build, with generic data." >}}

On top of that sits an AI layer that never writes anything by itself. A worker says "poured 10 moulds of pump housing, heat 5". Speech-to-text and a local language model turn this into fields of a fixed JSON schema, a resolver matches the words to real stages, batches and heats, and the result appears as a proposal that a person confirms. Photos of lab chemistry protocols and of defects go through a vision model into the same loop. The models (Whisper and Qwen, served by Ollama) run on the plant's own GPU, so production data stays in the plant, and every confirmed proposal becomes an example for later prompts.

{{< figure src="voice-proposal.jpg" alt="A recognised voice report in GussCore showing quantity 30 and the spoken casting name, with Reject and Confirm buttons" caption="A recognised voice report waiting for confirmation." >}}

The backend uses FastAPI, Pydantic v2, SQLAlchemy 2 and PostgreSQL, and the frontend is a SvelteKit web app for phones. The architecture is hexagonal, every change goes into an append-only log of more than 60 event types, and 8 roles have field-level permissions. The code has more than 300 tests and 15 recorded architecture decisions.

## Status

GussCore has been piloted at a two-plant foundry group. A public evaluation build with generic data is on GitHub: [github.com/eugenmik/gusscore-erp](https://github.com/eugenmik/gusscore-erp).

{{< related_post "human-in-the-loop-ai-foundry-floor" >}}
