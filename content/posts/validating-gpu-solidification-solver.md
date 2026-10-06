---
title: "Validating a GPU solidification solver: from +51% to within 3.7%"
date: 2026-10-06
draft: false
math: true
description: "How I checked the FoundryFlash solver, and how the largest error turned out to be in the sand data."
tags: ["solidification", "simulation", "validation", "GPU"]
---

A fast solver that gives a wrong answer makes a wrong feeding decision look certain. When I wrote the solidification solver behind [FoundryFlash](/projects/foundryflash/), I spent as much time checking it as writing it. This post covers that checking and the error that mattered most.

## What the solver computes

The solver integrates the transient heat equation in enthalpy form, which handles the latent heat released during freezing without special treatment:

$$\rho \frac{\partial H}{\partial t} = \nabla \cdot \left( k \nabla T \right), \qquad T = T(H)$$

It uses control-volume finite elements on linear tetrahedra and balances energy on the dual volume around each node. Time stepping is implicit backward Euler, solved with a Jacobi-preconditioned conjugate-gradient method. The mould is a region of its own: heat crosses the metal-mould interface through a heat-transfer coefficient \(h\), with flux \(q = h \, (T_\text{metal} - T_\text{mould})\).

## Step 1: verification

First I checked that the equations are solved correctly. I solved the same enthalpy problem in FEniCSx, an independent open-source finite-element library, on a small verification test case (about 900 nodes, explicit time stepping) where the two codes can be compared node by node. These were the acceptance limits and the results:

| Check | Limit | Measured |
|---|---|---|
| Energy imbalance | 10⁻⁴ | 5.6 × 10⁻¹⁵ |
| Solid-fraction MAE | 0.01 | 0.0086 |
| Solidification time, relative error | 0.01 | 0.00088 |

The CPU and GPU backends agree to round-off (10⁻¹⁵). With the implicit scheme, a 20 s time step stays within 1.3% of the reference; an explicit scheme at the same step was off by 15.6%.

## Step 2: validation

Next came the question whether these are the right equations for a real casting. The reference was a commercial simulation of a ductile-iron (EN-GJS-400-15) production casting, which reached full solidification at 964 s. My first result was 51% longer.

Before touching the solver, I changed one input at a time and measured how far each one moved the total solidification time:

| Input changed | Change | Shift in total time |
|---|---|---|
| Interface heat-transfer coefficient | 4× (500 to 2000 W/m²K) | −5.5% |
| Alloy data | freezing range 21 K to 89 K | −12.3% |
| Mould thermal effusivity \(b = \sqrt{k \rho c}\) | 1.5× | −43.8% |

The mould dominates. The sand data I had used described a soft sand: \(k = 0.484\) W/(m·K) and \(\rho c = 1.466 \times 10^6\) J/(m³·K), which gives \(b \approx 842\). Typical published green-sand data (\(k = 0.7\), \(\rho = 1500\), \(c_p = 1100\)) gives \(b \approx 1075\), 1.28 times higher. With \(b\) raised by a factor of 1.30, the solver gives 1000 s against the reference 964 s, a difference of 3.7%. Nothing in the numerics changed.

## What this means for a foundry

In this case the number that drove the feeding decision came from the sand data. Measuring the plant's own moulding material (thermal diffusivity by laser flash, plus heat capacity and bulk density, which together give the conductivity) would do more for accuracy than any change to the code, and it costs less than a software licence.

## Speed

On a consumer RTX 3060, a case with 1.6 million elements solves in 9.9 s, against 44.9 s on eight CPU threads. A parallel mesher cut 3D meshing from 57 s to 4 s, and keeping the solver process running cut job start-up from about 27 s to under 0.1 s.

## Open points

One casting is one casting. A second validation package is ready: six runs on five castings against another commercial code, with acceptance criteria fixed in advance. The shrinkage model is a volume balance over liquid pools without melt flow or pressure, so it shows where defects form, but its percentages are only qualitative.

{{< publications >}}
