[![PyPI version](https://badge.fury.io/py/mcmstclustering.svg)](https://badge.fury.io/py/mcmstclustering)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

# Motivation

MCMSTClustering is a minimum-cost MST based clustering algorithm.  
It uses MST distances and optional DBSCAN to detect clusters in high-dimensional data.

## Installation

```bash
pip install MCMSTClustering
```

## Usage

```bash
import numpy as np
from mcmstclustering import MCMSTClustering
from sklearn.datasets import make_moons

# Generate sample data
X, _ = make_moons(n_samples=200, noise=0.05, random_state=42)

# Create and fit the model
model = MCMSTClustering(N=5, r=0.1, n_micro=3, random_state=42)
labels = model.fit_predict(X)

# Evaluate results
print(f"Number of clusters: {model.n_macro_clusters_}")
print(f"Number of micro-clusters: {model.n_micro_clusters_}")

# Visualize results
from mcmstclustering import plot_clusters_2d
plot_clusters_2d(model, X)

```

## Oerview

MCMSTClustering (Defining Non-Spherical Clusters by using Minimum Spanning Tree over KD-Tree-based Micro-Clusters) is designed to overcome limitations of conventional clustering algorithms when handling:

	- High-dimensional data
	
	- Imbalanced datasets
	
	- Clusters with varying densities
	
	- Noisy data/outliers
	
	- Arbitrary-shaped clusters
	

The algorithm consists of three main steps:

	1. Micro-cluster Formation: Defines micro-clusters using a KD-Tree data structure with range search.
	
	2. Macro-cluster Construction: Builds a minimum spanning tree (MST) over the micro-clusters to form macro-clusters.
	
	3. Cluster Regulation: Refines the clusters to improve accuracy and overall clustering quality.
	

Extensive experiments against state-of-the-art algorithms show that MCMSTClustering achieves high-quality clustering results with acceptable runtime.

Key Features

	- Clusters datasets with high quality

	- Detects arbitrary-shaped clusters

	- Robust against outliers/noisy data

	- Handles clusters with varying densities

	- Efficient on imbalanced datasets


## Advanced Usage

```bash
from mcmstclustering import find_optimal_parameters, evaluate_clustering
from sklearn.datasets import load_iris

# Load dataset
data = load_iris()
X = data.data
y = data.target

# Find optimal parameters
result = find_optimal_parameters(X, y, n_iter=50, random_state=42)
print(f"Best parameters: {result['params']}")
print(f"Best ARI: {result['score']:.4f}")

# Use optimal parameters
model = MCMSTClustering(**result['params'], random_state=42)
labels = model.fit_predict(X)

# Evaluate clustering
metrics = evaluate_clustering(y, labels)
for metric_name, value in metrics.items():
    print(f"{metric_name}: {value:.4f}")
```


## Cite

If you use the code in your works, please cite the paper given below:
```bash
Şenol, A. MCMSTClustering: defining non-spherical clusters by using minimum 
spanning tree over KD-tree-based micro-clusters. Neural Comput & Applic 35, 
13239–13259 (2023). https://doi.org/10.1007/s00521-023-08386-3
```

## BibTeX

```bash
@article{csenol2023mcmstclustering,
  title={MCMSTClustering: defining non-spherical clusters by using minimum spanning tree over KD-tree-based micro-clusters},
  author={{\c{S}}enol, Ali},
  journal={Neural Computing and Applications},
  volume={35},
  number={18},
  pages={13239--13259},
  year={2023},
  publisher={Springer}
}
```