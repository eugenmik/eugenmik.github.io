---
title: "Publishing a casting model: what it took to make the weights runnable"
date: 2026-10-09
draft: false
description: "Releasing the solidification surrogate was not a matter of uploading a checkpoint. Checking that the published files reproduce the internal ones, and reporting the results honestly, took longer than the upload."
tags: ["physics-ML", "solidification", "open source", "reproducibility"]
---

The solidification surrogate behind [castsolid-gnn](/projects/castsolid-gnn/) is now public under Apache-2.0, weights included. I had expected that to be an afternoon of uploading a checkpoint. It was not. The model had lived in my training setup for months, and a training checkpoint is not something a stranger can run.

Here is what stood between the checkpoint and a model someone else can use.

## A checkpoint carries the training rig with it

My internal artifacts were a PyTorch `.pt` file and two scikit-learn models saved with joblib. All three were written by my own code and read by my own code, so they were full of assumptions I had stopped seeing: how features were normalized, what the architecture config was, which node ordering the mesh used, which scikit-learn version wrote the file.

Unpacking that is most of the work. The published GNN carries its normalization statistics and its architecture config inside the file metadata, so the loader does not need my training repository to rebuild the network. The alloy and mould properties became eight named numbers with documented units instead of positional arguments.

## Proving the published file is the same model

A converted file is a new file, and I did not want to find out later that it had drifted from the checkpoint it came from.

For the network, I checked every tensor against the internal checkpoint for bit identity, along with the config and the normalization statistics. The gradient-boosted heads cannot be compared that way, because the file format differs, so I compared behaviour instead: 10,002 probe rows spanning the training range of each input feature, with identical predictions required. Then I ran the published inference code beside the internal pipeline on five production parts, two of them in both alloys, plus a mesh with a custom property set. Every output field matched.

That last check is the one I would skip if I were in a hurry, and it is the one that would have caught a mistake in the loading path rather than in the weights.

## File formats that cannot run code

A pickle file executes code when you load it. Asking a foundry engineer to download a pickle from the internet and open it is asking them to run a stranger's code on their workstation.

The network ships as [safetensors](https://github.com/huggingface/safetensors), which stores tensors and nothing executable. The two boosted heads use [skops](https://skops.readthedocs.io/), and before the loader opens one it checks every type named in the file against an allowlist of scikit-learn and NumPy types. Neither file can execute anything when loaded.

The cost is a version constraint. The heads were trained with scikit-learn 1.5.2, and other versions may refuse to load them. That is stated on the card rather than discovered at runtime.

## Reporting the evaluation so it cannot be misread

This was the part I rewrote most often.

The headline numbers are good: nodal error of 4.26 s and hot-spot overlap of 0.917 on held-out geometry families. On six real castings the median overlap is 0.738. A median over six parts invites the reader to treat it as typical, so the card also says that one of those six reached an overlap of 0.035. Someone deciding whether to trust this on their own part needs the bad case more than the median.

The more important caveat is structural. The training data and the real-part references come from the same FEniCSx heat-transfer model, the same material database and the same boundary assumptions. The evaluation measures how well the surrogate carries over to geometry it has not seen. It is not evidence of physical accuracy against instrumented castings, and the card says so in those words. A foundry engineer reading an overlap of 0.917 could otherwise reasonably assume someone had poured the part and measured it.

## What is not in the release

Training code and the simulation corpus, about 100 GB, stay unpublished. The release is the model, the inference code and the pipeline that goes from a STEP file to a field you can open in ParaView.

A surrogate like this is useful for screening: comparing early concepts, finding candidate last-to-solidify regions, and deciding which designs are worth a full simulation. It does not sign off a process. Keeping that line visible in the documentation matters more to me than the accuracy numbers, because the numbers are only meaningful to someone who knows which question they answer.

If you try it on a casting of your own, especially one where it fails, the [discussions tab](https://huggingface.co/eugenmik/castsolid-gnn/discussions) is the place I would most like to hear about it.
