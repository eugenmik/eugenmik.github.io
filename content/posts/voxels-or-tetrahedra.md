---
title: "Voxels or tetrahedra: what casting AI needs from the mesh"
date: 2026-10-06
draft: false
math: true
description: "A staircase boundary misstates the cooling rate where feeding decisions are made. What my own voxel prototype measured, and why a tetrahedral mesh suits a neural network."
tags: ["meshing", "simulation", "physics-ML", "solidification"]
---

Many casting simulation codes discretise the part on a structured cubic grid. That made sense on the hardware of the 1980s, and for many parts it still works. It is a weak base for two things foundries want now: simulating the free-form shapes that 3D-printed moulds and cores make possible, and training AI that proposes casting technology.

## Where the staircase hurts

A cubic grid turns a curved or inclined surface into a staircase. On a plane inclined at 45°, the staircase overstates the wetted area by \(\sqrt{2} \approx 1.41\), and doubly curved surfaces are worse. The surface normal also points along a grid axis everywhere instead of following the real surface.

Interface heat flux is \(q = h \, A \, (T_\text{metal} - T_\text{mould})\), so both errors go straight into the local cooling rate, which is what feeding decisions rest on. The error is largest on organic, undercut shapes, the same parts customers order printed moulds and cores for.

## What my voxel prototype measured

Voxels have real advantages, so I built a voxel prototype for my own solver. It used a cut-cell correction (true volume fractions and clipped interface areas), and I compared it with the tetrahedral solution on a production casting at 4, 3 and 2 mm cells.

The first comparison was far off because of my own mistake: the rule for conductance across the casting-mould contact layer was wrong by a factor that did not depend on cell size. After fixing it I got these numbers:

| Cell size | 4 mm | 3 mm | 2 mm |
|---|---|---|---|
| Total solidification time vs tetrahedral | +4.2% | +1.4% | +4.1% |
| Field median of \(\lvert \Delta t \rvert / t\) | 10.1% | 3.4% | 9.6% |

Halving the cell did not halve the error, and on this casting it did not reduce it at all. The remaining error sits in thin sections that freeze early (20 to 46% in the first 200 s band), while heavy sections stay within 2 to 6%. I kept the tetrahedral mesh.

Voxels do have strengths. The voxel path meshed three castings with defective CAD that the tetrahedral path could not mesh at all, and its stencil is well behaved by construction. In the tetrahedral mesh of the reference casting, 16.5% of the edge conductances were negative. I keep measuring both.

## Why the mesh matters for AI

A graph neural network learns on nodes and edges, and an unstructured tetrahedral mesh already has that form: its nodes carry temperatures and solidification times, and its edges carry the geometry. My [GNN surrogate](/projects/gnn-solidification/) learns directly on the simulation mesh, following the MeshGraphNets pattern.

A voxel grid leads to 3D convolutions instead. Their memory grows with the cube of the resolution, and the network has to learn the staircase along with the physics. For AI that proposes gating and feeding on free-form castings, the choice of discretisation decides what the model can learn.

{{< publications >}}
