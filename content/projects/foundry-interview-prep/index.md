---
title: "Foundry Interview Prep: practice from a resume"
description: "A Streamlit app that reads a resume and runs a mock foundry interview, with a language model scoring the answers. Built as a course project."
weight: 50
metric: "Five prompting strategies compared side by side"
stack: ["Streamlit", "OpenRouter", "Python"]
---

## What it does

The app reads a resume as PDF, DOCX or text, pulls out the foundry experience, estimates seniority and finds the gaps. From that it writes interview questions across technical, metallurgical, quality and behavioural topics, then runs a live mock interview in chat. A second model call scores each answer from 0 to 10 and suggests a better one.

There are two modes. A candidate practises against their own resume. A recruiter uploads someone else's and gets an interview plan, a weighted scorecard and a list of things to probe. The interface runs in English, German and Russian, and the chosen language is passed to the model so the generated questions match.

{{< figure src="how-it-works.svg" alt="Diagram: a resume becomes an analysis, which generates interview questions, which feed a live mock interview; a judge model scores each answer" caption="From a resume to a scored mock interview." >}}

## Prompting and guards

The app carries five prompting strategies that you can switch between while using it: zero-shot, few-shot, chain of thought, persona and a structured contract. Running the same resume through each one shows the differences directly, which was the point of building it.

It also has three guards against prompt injection in an uploaded resume: input validation, a regex filter and a moderation call. A resume is a file from a stranger, so an interview app that feeds it straight into a model is an obvious target.

## Status

This was my first sprint project on the Turing College AI Engineering programme, and it stayed at that scope: no test suite, no licence file and no hosted demo. It is here as the place where I started working with language models, not as production software.

## Links

The code is at [github.com/eugenmik/foundry-interview-prep](https://github.com/eugenmik/foundry-interview-prep).
