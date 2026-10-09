---
title: "FoundryFlash: GPU casting simulator"
description: "A casting solidification simulator that runs in the browser, from STEP upload to a feeding decision, with a Julia and CUDA solver behind it."
featured: true
weight: 10
metric: "1.6M elements in 9.9 s on a GPU, within 3.7% of a commercial reference"
stack: ["Julia", "CUDA.jl", "Gmsh", "FastAPI", "React", "three.js"]
---

## The problem

Feeding decisions depend on where and when the metal freezes last: where risers go, where a chill helps, whether a sleeve is needed. A full process simulation answers that, but it takes setup time and licences, so early in design many of these decisions are still made by rule of thumb.

## What I built

FoundryFlash takes a STEP model to a solidification answer in the browser. It has two engines. The [GNN surrogate](/projects/castsolid-gnn/) screens a design in seconds; that is the version described in the trade articles below. The full solver described here is for the final check.

{{< figure src="solidification-time.jpg" alt="Solidification-time field on a flanged casting in the FoundryFlash viewer, coloured from 0 to 595 seconds" caption="Solidification time on a flanged casting in the FoundryFlash viewer." >}}

The solver is written in Julia. It uses control-volume finite elements on linear tetrahedra and an enthalpy formulation, so the latent heat released during freezing needs no special handling. Time stepping is implicit, solved with a preconditioned conjugate-gradient method, and the mould is a region of its own with a heat-transfer coefficient at the interface. The same code runs on CPUs and on NVIDIA GPUs through CUDA.jl, and the two give results identical to round-off (10⁻¹⁵). Gmsh meshes the casting and the sand mould with its parallel HXT mesher.

On the web side, a FastAPI backend keeps a solver process warm, and a React and three.js viewer shows solidification time, fraction liquid, temperature and thermal modulus. The viewer masks hot spots, helps size feeders and writes a PDF report.

## Results

| What | Measured |
|---|---|
| Full solve, 1.6M elements | 9.9 s on an RTX 3060, 44.9 s on 8 CPU threads |
| 3D meshing, 1.6M-element test body | 57 s before, 4 s after (14× faster) |
| Job start-up | about 27 s before, under 0.1 s after |
| Verification against an independent FEniCSx reference | solid-fraction MAE 0.0086 |
| Comparison with a commercial simulation of a production casting | +51% at first, 3.7% after a sensitivity study traced the gap to the mould's thermal properties |
| Automated tests | about 7,500 in Julia, Python and TypeScript |

{{< related_post "validating-gpu-solidification-solver" >}}

## Status

FoundryFlash is my own product and is still in development. The source code is private; I can share technical details on request.

{{< publications >}}
