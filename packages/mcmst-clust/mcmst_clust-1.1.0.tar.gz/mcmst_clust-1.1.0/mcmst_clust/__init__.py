"""
MCMSTClustering: A novel clustering algorithm for arbitrary-shaped clusters
using Minimum Spanning Tree over KD-tree-based micro-clusters.
"""

from .core import MCMSTClustering
from .utils import purity_score, find_optimal_parameters, evaluate_clustering

__version__ = "1.1.0"
__author__ = "Ali Senol"
__email__ = "alisenol@tarsus.edu.tr"

__all__ = [
    'MCMSTClustering',
    'purity_score',
    'find_optimal_parameters',
    'evaluate_clustering',
    'plot_clusters_2d'
]