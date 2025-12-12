import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs, make_circles
from sklearn.preprocessing import MinMaxScaler
# Import the MCMSTClustering package
from mcmst_clust import MCMSTClustering, normalize

# =============================================================================
# EXAMPLE 1: BASIC USAGE WITH SYNTHETIC DATA
# =============================================================================

print("=" * 60)
print("EXAMPLE: BASIC USAGE WITH SYNTHETIC DATA")
print("=" * 60)

# Generate synthetic data (two moons)
X_moons, y_moons = make_moons(n_samples=300, noise=0.05, random_state=42)

# Normalize the data (important for distance-based clustering)
X_moons_normalized = normalize(X_moons)

# Initialize the MCMSTClustering model
# Parameters from the paper:
# N: Minimum number of data points to define a Micro Cluster (default: 5)
# r: Radius of the Micro Cluster (default: 0.05)
# n_micro: Minimum number of Micro Clusters to define a Macro Cluster (default: 5)
model = MCMSTClustering(N=5, r=0.05, n_micro=3)

# Fit the model to the data
model.fit(X_moons_normalized)

# Get cluster labels
labels = model.labels_

