<a href="https://kappakit.readthedocs.io/en/latest/"><img alt="Documentation" src="https://img.shields.io/website?url=https%3A%2F%2Fkappakit.readthedocs.io%2Fen%2Flatest%2F&up_message=sphinx&label=docs&color=blue"></a>
<a href="https://pypi.org/project/kappakit/"><img alt="Python version" src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FWeber-GeoML%2Fkappakit%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&color=green"></a>
<a href="https://github.com/Weber-GeoML/kappakit/blob/main/LICENSE.txt"><img alt="Code license" src="https://img.shields.io/github/license/Weber-GeoML/kappakit?color=blue"></a>
<a href="https://github.com/Weber-GeoML/kappakit/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Weber-GeoML/kappakit?color=green"></a>

# KappaKit: Curvature Estimation on Data Manifolds with Diffusion-Augmented Sampling

`kappakit` is a Python library for estimating the curvature of a data manifold. 

Curvature is the fundamental descriptor of local geometry—useful in shape analysis, learning theory, and non-Euclidean algorithms—yet it proves elusive to estimate on sparse, noisy data.

KappaKit offers a modular base framework for various curvature estimation methods. In particular, it supports training diffusion models via the [HuggingFace](https://huggingface.co/) API to increase the sample density for downstream estimation methods.

## Installation

From pip:
```
pip install kappakit
```

From source:

```bash
git clone https://github.com/Weber-GeoML/kappakit.git
pip install -e .
```

## Usage

This repository contains the experiment scripts to reproduce the paper [Curvature Estimation on Data Manifolds with Diffusion-Augmented Sampling](https://openreview.net/pdf?id=zu24PDRqvB). If you use this repository, please use this paper as the citation.

You can reproduce the experiments by running `scripts/experiments/all.sh`. The figures in the paper were generated with `scripts/experiments/generate_figures.ipynb`.

A curvature estimation experiment may invoke the following routines in order:

1. `kappakit.routines.create_dataset`
2. `kappakit.routines.train_diffusion_model`
3. `kappakit.routines.estimate_curvature`

Please refer to the [documentation](https://kappakit.readthedocs.io/en/latest/) for the API reference as well as tutorials on how to use or expand this codebase.