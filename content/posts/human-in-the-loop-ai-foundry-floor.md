---
title: "Human-in-the-loop AI on the foundry floor"
date: 2026-10-06
draft: false
description: "Five design rules from building GussCore, a foundry ERP/MES where workers report by voice and a person confirms every AI proposal."
tags: ["LLM", "foundry", "shop floor", "human-in-the-loop"]
---

In many foundries the hardest data problem is capture. Nobody types a report on a terminal in foundry gloves, so heats, moulds, scrap and chemistry get reconstructed from paper at the end of the shift, and that is where errors come in.

[GussCore](/projects/gusscore/) lets shop-floor workers report by voice or photo. It has been piloted at a two-plant foundry group, and five rules shaped it.

## 1. The AI proposes and a person confirms

Nothing reaches the database without human confirmation. A wrong heat number spreads into metal traceability, costing and the weekly plan, so the model takes over the typing and the person keeps the responsibility.

## 2. Constrain the model, then check against real records

The language model must answer in a fixed JSON schema: intent, quantity, stage, heat and defect kind. A separate resolver then maps the words to entities that exist, using fuzzy matching in PostgreSQL. The model cannot invent an ID. At worst it fails to find one, and the person sees that.

## 3. Keep the data in the plant

Speech, photos of lab chemistry protocols and production numbers are sensitive. Speech recognition (Whisper) and the language and vision models (Qwen, served by Ollama) run on the plant's own GPU. Planning GPU memory for this was one of the first architecture decisions I recorded.

## 4. Learn from confirmations

Each proposal a person confirms becomes an example in later prompts, so recognition improves with use and no model needs retraining.

## 5. Record events and derive states

Nobody types stage progress by hand. It is derived from events: the open quantity is planned minus good minus scrap. A correction is a negative event, so costing rolls back cleanly, and every change has an author in an append-only log of more than 60 event types.

## What it took

Getting from a chat-bot prototype to a web app for phones took about three months, with more than 300 tests and 15 recorded architecture decisions along the way. The AI was the easier part. The harder part was the foundry itself: learning which words melters actually use, and which mistakes cost money.

{{< publications >}}
