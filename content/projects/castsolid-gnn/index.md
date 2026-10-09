---
title: "castsolid-gnn: solidification surrogate"
description: "A graph neural network that predicts where a casting solidifies last, in seconds instead of hours. Weights published on Hugging Face under Apache-2.0."
weight: 20
featured: true
aliases:
  - /projects/gnn-solidification/
metric: "Open weights on Hugging Face, hot-spot overlap 0.917"
stack: ["PyTorch Geometric", "FEniCSx", "Gmsh", "Hugging Face", "trame"]
---

## The problem

A full solidification simulation takes minutes to hours. Early in design, an engineer wants to compare many variants in seconds and see where the metal freezes last, and will give up some precision for that.

## The model

The model takes a tetrahedral mesh of a casting with its alloy and mould properties, and returns the time at which every node solidifies. The nodes that solidify last are the hot spots, where feeding problems and shrinkage usually start.

It is a hybrid of three trained parts. A 12-block MeshGraphNet-style network with FiLM conditioning predicts the shape of the field, two gradient-boosted heads predict its overall level and its spread, and a fixed recomposition step combines them. The network alone is weaker on absolute magnitude, which depends on alloy and part size: adding the heads brought nodal error on held-out geometry families from 5.77 s down to 4.26 s. Together it is about 1.85 M parameters.

Training data came from a pipeline I wrote: parametric geometry in CadQuery, meshing in Gmsh, and enthalpy-method simulations in FEniCSx. The corpus is 14,937 simulations in three sets, 9,710 primitives across 42 geometry families, 4,727 multi-alloy cases and 500 real production parts, and the model was built as a chain of fine-tunes across them. Training ran on one RTX 3060.

{{< video src="castsolid-playback" alt="A predicted solidification field played back over time: solidified material turns translucent while the remaining liquid contracts toward the hot spot" caption="A predicted field played back in the viewer. The last liquid contracts toward the hot spot." >}}

{{< figure src="geometry-families.jpg" alt="Nine examples of parametric casting geometries: plates with ribs and bosses, a spoked wheel, a flanged bush, a cross, a valve body and a U-channel" caption="Examples from the 42 parametric geometry families used to generate training data." >}}

## The pipeline around it

The code takes a STEP file to a result you can open in ParaView. It heals the CAD through the OpenCASCADE kernel in Gmsh, meshes it at the density the model was trained on, caches the mesh, runs the model, and checks the part against the training envelope. A screening layer turns the predicted field into a Niyama proxy, a porosity-risk mask, macro-shrinkage regions, gravity-aware sinks and feeder modulus suggestions. There is also a local browser viewer built with trame and PyVista: upload a STEP file, pick the alloy, scrub a time slider and export a playback.

## Results

| Evaluation | n | Nodal MAE | Hot-spot overlap |
|---|---|---|---|
| Held-out geometry families | family split | 4.26 s | 0.917 |
| Unseen real castings | 6 | 80.3 s median | 0.738 median |

Two caveats travel with those numbers. One of the six real parts reached a hot-spot overlap of only 0.035, so the median says nothing certain about any single part. And the training data and the references come from the same FEniCSx model with the same material and boundary assumptions, so these figures show how well the surrogate carries over to new geometry. They are not evidence of physical accuracy against instrumented castings. A hot spot is a shrinkage-risk indicator, not a porosity label.

The release covers one setup: a single casting cooling into a green-sand mould over its whole outer surface, in ductile iron, cast steel or a custom property set.

While building the training set I found a defect that shaped the whole project. The solver stored temperatures in one node ordering and the geometry features in another, so about 60% of the targets were silently attached to the wrong positions. Every early model failure traced back to it. If you train on solver output, check node identity across every mesh interface before you tune anything.

## Links

The weights are public under Apache-2.0 on Hugging Face: [huggingface.co/eugenmik/castsolid-gnn](https://huggingface.co/eugenmik/castsolid-gnn). The card there documents the architecture, the training data and the limits in full.

The inference code and the STEP-to-result pipeline are at [github.com/eugenmik/castsolid-gnn](https://github.com/eugenmik/castsolid-gnn), also Apache-2.0, with 154 tests. Training code and the raw simulation corpus are not published.

{{< related_post "publishing-a-casting-model" >}}

{{< publications >}}
