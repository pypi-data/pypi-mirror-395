"""
MCMSTClustering: A novel clustering algorithm for arbitrary-shaped clusters
using Minimum Spanning Tree over KD-tree-based micro-clusters.
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from sklearn.neighbors import KDTree
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
import random
from typing import Tuple, Dict, List, Optional
import warnings


class MCMSTClustering:
    """
    MCMSTClustering: Defining Non-Spherical Clusters by using 
    Minimum Spanning Tree over KD-tree-based Micro-Clusters.
    
    Parameters
    ----------
    N : int, default=5
        Minimum number of data points to define a micro-cluster.
    
    r : float, default=0.1
        Radius for micro-cluster formation.
    
    n_micro : int, default=3
        Minimum number of micro-clusters to define a macro-cluster.
    
    random_state : int or None, default=None
        Random seed for reproducibility.
    
    Attributes
    ----------
    micro_clusters_ : array-like, shape (n_micro_clusters, n_features + 3)
        Micro-clusters information including center coordinates.
    
    macro_clusters_ : array-like
        Macro-clusters information.
    
    labels_ : array-like, shape (n_samples,)
        Cluster labels for each data point.
    
    n_micro_clusters_ : int
        Number of micro-clusters formed.
    
    n_macro_clusters_ : int
        Number of macro-clusters formed.
    
    References
    ----------
    Senol, A. (2023). MCMSTClustering: defining non-spherical clusters by using 
    minimum spanning tree over KD-tree-based micro-clusters. 
    Neural Computing and Applications, 35(18), 13239-13259.
    """
    
    def __init__(self, N: int = 5, r: float = 0.1, n_micro: int = 3, 
                 random_state: Optional[int] = None):
        self.N = N
        self.r = r
        self.n_micro = n_micro
        self.random_state = random_state
        
        # Initialize attributes
        self.micro_clusters_ = None
        self.macro_clusters_ = None
        self.labels_ = None
        self.n_micro_clusters_ = 0
        self.n_macro_clusters_ = 0
        self._processed_data = None
        
        if random_state is not None:
            np.random.seed(random_state)
            random.seed(random_state)
    
    def fit(self, X: np.ndarray) -> 'MCMSTClustering':
        """
        Fit the MCMSTClustering model to the data.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training instances to cluster.
            
        Returns
        -------
        self : object
            Returns self.
        """
        # Validate input
        X = self._validate_data(X)
        
        # Normalize data
        scaler = MinMaxScaler()
        X_normalized = scaler.fit_transform(X)
        
        # Initialize data structure
        self._initialize_data(X_normalized)
        
        # Three-stage clustering as per paper
        self._define_micro_clusters()
        self._regulate_clusters()
        self._define_macro_clusters()
        self._assign_labels()
        
        return self
    
    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """
        Fit the model and return cluster labels.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Data to cluster.
            
        Returns
        -------
        labels : array-like, shape (n_samples,)
            Cluster labels.
        """
        self.fit(X)
        return self.labels_
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict cluster labels for new data points.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            New data to predict.
            
        Returns
        -------
        labels : array-like, shape (n_samples,)
            Predicted cluster labels.
        """
        # For new data, assign to nearest micro-cluster
        warnings.warn("MCMSTClustering.predict() assigns points to nearest "
                     "micro-cluster. For optimal results, use fit_predict().")
        
        X = self._validate_data(X)
        scaler = MinMaxScaler()
        X_normalized = scaler.fit_transform(X)
        
        if self.micro_clusters_ is None:
            raise ValueError("Model must be fitted before prediction.")
        
        labels = np.zeros(len(X_normalized))
        
        if self.n_micro_clusters_ > 0:
            # Find nearest micro-cluster for each point
            tree = KDTree(self.micro_clusters_[:, 3:])
            for i in range(len(X_normalized)):
                dist, idx = tree.query(X_normalized[i].reshape(1, -1), k=1)
                if dist[0][0] <= 2 * self.r:
                    mc_id = int(self.micro_clusters_[idx[0][0], 0])
                    labels[i] = self.micro_clusters_[self.micro_clusters_[:, 0] == mc_id, 2][0]
        
        return labels
    
    def _validate_data(self, X: np.ndarray) -> np.ndarray:
        """Validate input data."""
        X = np.array(X, dtype=float)
        if len(X.shape) != 2:
            raise ValueError("Input data must be 2-dimensional.")
        if X.shape[0] < self.N:
            raise ValueError(f"Number of samples ({X.shape[0]}) must be >= N ({self.N}).")
        return X
    
    def _initialize_data(self, X: np.ndarray):
        """Initialize data structures."""
        n_samples = X.shape[0]
        indices = np.arange(1, n_samples + 1).reshape(-1, 1)
        mc_zeros = np.zeros((n_samples, 1))
        macro_zeros = np.zeros((n_samples, 1))
        self._processed_data = np.hstack([indices, mc_zeros, macro_zeros, X])
        self.micro_clusters_ = np.empty((0, X.shape[1] + 3), float)
        self.macro_clusters_ = np.empty((0, 4), dtype=object)
        self.n_micro_clusters_ = 0
        self.n_macro_clusters_ = 0
    
    def _define_micro_clusters(self):
        """Algorithm 3: Define micro-clusters using KD-Tree."""
        while True:
            # Get unassigned data
            unassigned_mask = self._processed_data[:, 1] == 0
            X_unassigned = self._processed_data[unassigned_mask, :]
            
            if X_unassigned.shape[0] < self.N:
                break
            
            # Create KD-Tree for unassigned data
            tree = KDTree(X_unassigned[:, 3:])
            
            # Shuffle indices for random selection
            indices = np.where(unassigned_mask)[0]
            np.random.shuffle(indices)
            
            for start_idx in indices:
                if self._processed_data[start_idx, 1] != 0:
                    continue
                
                # Range search
                point = self._processed_data[start_idx, 3:].reshape(1, -1)
                indices_arr = tree.query_radius(point, r=self.r)
                neighbor_indices = indices_arr[0]
                
                if len(neighbor_indices) >= self.N:
                    # Create new micro-cluster
                    self.n_micro_clusters_ += 1
                    points = X_unassigned[neighbor_indices, 3:]
                    center = np.mean(points, axis=0)
                    
                    # Add micro-cluster
                    new_mc = np.hstack([
                        [self.n_micro_clusters_, len(points), 0],
                        center
                    ])
                    self.micro_clusters_ = np.vstack([self.micro_clusters_, new_mc])
                    
                    # Assign points to micro-cluster
                    for idx in neighbor_indices:
                        original_idx = int(X_unassigned[idx, 0]) - 1
                        self._processed_data[original_idx, 1] = self.n_micro_clusters_
                    
                    break  # Restart after creating new micro-cluster
            else:
                break  # No new micro-clusters created
    
    def _regulate_clusters(self):
        """Algorithm 5: Assign points to closest micro-cluster within 2*r."""
        unassigned_mask = self._processed_data[:, 1] == 0
        X_unassigned = self._processed_data[unassigned_mask, :]
        
        if X_unassigned.shape[0] > 0 and self.n_micro_clusters_ > 0:
            tree = KDTree(self.micro_clusters_[:, 3:])
            
            for i in range(X_unassigned.shape[0]):
                point = X_unassigned[i]
                point_coords = point[3:].reshape(1, -1)
                
                dist, idx = tree.query(point_coords, k=1)
                
                if dist[0][0] <= 2 * self.r:
                    mc_id = int(self.micro_clusters_[idx[0][0], 0])
                    point_idx = int(point[0]) - 1
                    self._processed_data[point_idx, 1] = mc_id
                    
                    # Update micro-cluster
                    mc_idx = np.where(self.micro_clusters_[:, 0] == mc_id)[0][0]
                    self.micro_clusters_[mc_idx, 1] += 1
                    # Update center (weighted average)
                    n_old = self.micro_clusters_[mc_idx, 1] - 1
                    old_center = self.micro_clusters_[mc_idx, 3:]
                    new_point = point[3:]
                    new_center = (old_center * n_old + new_point) / (n_old + 1)
                    self.micro_clusters_[mc_idx, 3:] = new_center
    
    def _build_mst_graph(self) -> np.ndarray:
        """Build graph with edges only where distance <= 2*r."""
        if self.n_micro_clusters_ == 0:
            return np.array([])
        
        centers = self.micro_clusters_[:, 3:]
        n_mcs = len(centers)
        
        if n_mcs == 1:
            return np.zeros((1, 1))
        
        dist_matrix = squareform(pdist(centers))
        adj_matrix = np.where(dist_matrix <= 2 * self.r, dist_matrix, 0)
        np.fill_diagonal(adj_matrix, 0)
        
        return adj_matrix
    
    def _prim_mst(self, adj_matrix: np.ndarray) -> List[Tuple[int, int]]:
        """Prim's algorithm for MST."""
        n = len(adj_matrix)
        if n <= 1:
            return []
        
        in_mst = [False] * n
        edge_list = []
        
        # Start from micro-cluster with most points
        start_node = np.argmax(self.micro_clusters_[:, 1])
        in_mst[start_node] = True
        
        while len(edge_list) < n - 1:
            min_edge = (None, None, float('inf'))
            
            for i in range(n):
                if in_mst[i]:
                    for j in range(n):
                        if not in_mst[j] and adj_matrix[i, j] > 0:
                            if adj_matrix[i, j] < min_edge[2]:
                                min_edge = (i, j, adj_matrix[i, j])
            
            if min_edge[0] is None:
                break
            
            edge_list.append((min_edge[0] + 1, min_edge[1] + 1))
            in_mst[min_edge[1]] = True
        
        return edge_list
    
    def _find_connected_components(self, adj_matrix: np.ndarray, 
                                  mst_edges: List[Tuple[int, int]]) -> List[List[int]]:
        """Find connected components in MST."""
        n = len(adj_matrix)
        if n == 0:
            return []
        
        # Build adjacency list
        adj_list = {i: [] for i in range(n)}
        for u, v in mst_edges:
            u_idx, v_idx = u - 1, v - 1
            adj_list[u_idx].append(v_idx)
            adj_list[v_idx].append(u_idx)
        
        # Find connected components
        visited = [False] * n
        components = []
        
        for i in range(n):
            if not visited[i]:
                stack = [i]
                component = []
                
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        component.append(node + 1)
                        stack.extend(adj_list[node])
                
                if component:
                    components.append(component)
        
        return components
    
    def _define_macro_clusters(self):
        """Define macro-clusters from micro-clusters using MST."""
        adj_matrix = self._build_mst_graph()
        
        if len(adj_matrix) == 0:
            return
        
        mst_edges = self._prim_mst(adj_matrix)
        components = self._find_connected_components(adj_matrix, mst_edges)
        
        for comp in components:
            # Check criteria: enough micro-clusters or enough total points
            total_points = sum(self.micro_clusters_[int(mc_id) - 1, 1] for mc_id in comp)
            if len(comp) >= self.n_micro or total_points >= self.N * self.n_micro:
                self.n_macro_clusters_ += 1
                
                # Assign micro-clusters to macro-cluster
                for mc_id in comp:
                    mc_idx = int(mc_id) - 1
                    self.micro_clusters_[mc_idx, 2] = self.n_macro_clusters_
                
                # Store macro-cluster info
                new_row = np.array([
                    self.n_macro_clusters_,
                    len(comp),
                    comp,
                    None  # Color placeholder
                ], dtype=object)
                self.macro_clusters_ = np.vstack([self.macro_clusters_, new_row])
        
        # Handle large individual micro-clusters
        for i in range(len(self.micro_clusters_)):
            if (self.micro_clusters_[i, 2] == 0 and 
                self.micro_clusters_[i, 1] >= self.N * self.n_micro):
                self.n_macro_clusters_ += 1
                self.micro_clusters_[i, 2] = self.n_macro_clusters_
                
                new_row = np.array([
                    self.n_macro_clusters_,
                    1,
                    [int(self.micro_clusters_[i, 0])],
                    None
                ], dtype=object)
                self.macro_clusters_ = np.vstack([self.macro_clusters_, new_row])
    
    def _assign_labels(self):
        """Assign macro-cluster labels to processed data."""
        self.labels_ = np.zeros(len(self._processed_data))
        
        for i in range(len(self._processed_data)):
            mc_id = self._processed_data[i, 1]
            if mc_id > 0:
                mc_mask = self.micro_clusters_[:, 0] == mc_id
                if np.any(mc_mask):
                    self.labels_[i] = self.micro_clusters_[mc_mask, 2][0]
    
    def get_params(self, deep: bool = True) -> Dict:
        """Get parameters for this estimator."""
        return {
            'N': self.N,
            'r': self.r,
            'n_micro': self.n_micro,
            'random_state': self.random_state
        }
    
    def set_params(self, **params):
        """Set the parameters of this estimator."""
        for key, value in params.items():
            setattr(self, key, value)
        return self
    
    def score(self, X: np.ndarray, y: np.ndarray = None) -> float:
        """
        Compute clustering score.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Data to cluster.
        y : array-like, shape (n_samples,), optional
            True labels for external validation.
            
        Returns
        -------
        score : float
            Adjusted Rand Index if y is provided, 
            Silhouette Score otherwise.
        """
        labels = self.fit_predict(X)
        
        if y is not None:
            return adjusted_rand_score(y, labels)
        else:
            return silhouette_score(X, labels)