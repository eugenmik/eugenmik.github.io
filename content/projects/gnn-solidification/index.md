---
title: "GNN surrogate for casting solidification"
description: "A graph neural network that predicts solidification-time fields and hot spots from a STEP file in seconds."
weight: 20
metric: "Trained on 14,437 FEM simulations, hot-spot overlap 0.917"
stack: ["PyTorch Geometric", "FEniCSx", "CadQuery", "Gmsh"]
---

## The problem

A full solidification simulation takes minutes to hours. Early in design, an engineer wants to compare many variants in seconds and see where the hot spots are, and will give up some precision for that.

## What I built

The training data comes from a pipeline I wrote. CadQuery generates parametric geometry in 42 families, Gmsh heals the CAD and meshes it into tetrahedra, and FEniCSx runs the enthalpy simulations. The corpus has 14,437 thermal simulations: 9,710 across the geometry families and 4,727 across alloys and boundary conditions.

{{< figure src="geometry-families.jpg" alt="Nine examples of parametric casting geometries: plates with ribs and bosses, a spoked wheel, a flanged bush, a cross, a valve body and a U-channel" caption="Examples from the 42 parametric geometry families used to generate training data." >}}

The model follows the MeshGraphNets pattern: an encoder, a processor of 12 message-passing blocks with hidden width 128, and a decoder, with 15 features per node. FiLM layers condition it on alloy and boundary conditions, and two gradient-boosting heads are recombined with the network's field output at graph level. The repository has over 300 tests and a model card that states scope and limits. While building it I found a node-ordering defect that had silently corrupted 60% of the training targets, and I wrote tooling to recover them.

## Results

| Test set | Result |
|---|---|
| Held-out geometry families | nodal MAE 4.26 s, hot-spot overlap 0.917 |
| Six real castings never seen in training | median hot-spot overlap 0.738, median MAE 80.3 s |
| Feeder (sleeve) assemblies (n = 2) | median hot-spot overlap 0.932 |

These are comparisons against the same FEniCSx physics used for training, not a physical validation against measured castings.

The model was trained on meshes of around 10,000 nodes, and the default mesh density can under-resolve large or thin-walled parts. Generating high-resolution training data fast enough is what the GPU solver in [FoundryFlash](/projects/foundryflash/) is for.

{{< related_post "voxels-or-tetrahedra" >}}

## Links

The code and model card are at [github.com/eugenmik/casting-gnn-solidification](https://github.com/eugenmik/casting-gnn-solidification). Weights and training data are not public.

{{< publications >}}
