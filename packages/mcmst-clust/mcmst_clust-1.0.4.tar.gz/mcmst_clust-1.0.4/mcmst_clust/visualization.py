"""
Visualization functions for MCMSTClustering.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from sklearn.decomposition import PCA


def plot_clusters_2d(model, X: np.ndarray, labels: np.ndarray = None, 
                    title: str = "MCMSTClustering Results"):
    """
    Plot clustering results in 2D.
    
    Parameters
    ----------
    model : MCMSTClustering
        Fitted MCMSTClustering model.
    X : array-like, shape (n_samples, n_features)
        Data points.
    labels : array-like, shape (n_samples,), optional
        Cluster labels. If None, uses model.labels_.
    title : str, default="MCMSTClustering Results"
        Plot title.
    """
    if labels is None:
        if model.labels_ is None:
            raise ValueError("Model must be fitted or labels must be provided.")
        labels = model.labels_
    
    # Reduce to 2D if needed
    if X.shape[1] > 2:
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X)
        micro_centers_2d = pca.transform(model.micro_clusters_[:, 3:])
        var_exp = pca.explained_variance_ratio_
    else:
        X_2d = X
        micro_centers_2d = model.micro_clusters_[:, 3:]
        var_exp = [1.0, 1.0]
    
    plt.figure(figsize=(12, 5))
    
    # Plot 1: True clusters (if available in model attributes)
    ax1 = plt.subplot(1, 2, 1)
    unique_labels = np.unique(labels)
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))
    
    for i, label in enumerate(unique_labels):
        mask = labels == label
        color = colors[i] if label > 0 else (0, 0, 0, 1)
        marker = 'o' if label > 0 else 'x'
        size = 30 if label > 0 else 20
        
        plt.scatter(X_2d[mask, 0], X_2d[mask, 1], 
                   color=color, marker=marker, s=size,
                   alpha=0.6, label=f'Cluster {int(label)}')
    
    # Plot micro-cluster centers
    for i in range(len(model.micro_clusters_)):
        mc_label = model.micro_clusters_[i, 2]
        if mc_label > 0:
            color = colors[int(mc_label) - 1] if mc_label <= len(colors) else (0, 0, 0, 1)
        else:
            color = (0, 0, 0, 1)
        
        plt.scatter(micro_centers_2d[i, 0], micro_centers_2d[i, 1],
                   color=color, marker='s', s=100,
                   edgecolors='black', linewidth=1.5)
        
        # Draw radius circles
        circle = Circle((micro_centers_2d[i, 0], micro_centers_2d[i, 1]),
                       model.r, color=color, fill=False,
                       linewidth=1.5, alpha=0.3)
        ax1.add_patch(circle)
    
    if X.shape[1] > 2:
        plt.xlabel(f'PC1 ({var_exp[0]:.1%})')
        plt.ylabel(f'PC2 ({var_exp[1]:.1%})')
    else:
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
    
    plt.title('Clustering Results with Micro-clusters')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Only micro-clusters
    ax2 = plt.subplot(1, 2, 2)
    
    # Plot data points colored by micro-cluster
    for mc_id in np.unique(model._processed_data[:, 1]):
        if mc_id == 0:
            continue
        
        mask = model._processed_data[:, 1] == mc_id
        mc_idx = np.where(model.micro_clusters_[:, 0] == mc_id)[0][0]
        mc_label = model.micro_clusters_[mc_idx, 2]
        
        if mc_label > 0:
            color = colors[int(mc_label) - 1] if mc_label <= len(colors) else (0, 0, 0, 1)
        else:
            color = (0.5, 0.5, 0.5, 1)
        
        plt.scatter(X_2d[mask, 0], X_2d[mask, 1],
                   color=color, marker='o', s=20, alpha=0.4)
    
    # Highlight micro-cluster centers
    for i in range(len(model.micro_clusters_)):
        mc_label = model.micro_clusters_[i, 2]
        if mc_label > 0:
            color = colors[int(mc_label) - 1] if mc_label <= len(colors) else (0, 0, 0, 1)
            plt.scatter(micro_centers_2d[i, 0], micro_centers_2d[i, 1],
                       color=color, marker='s', s=150,
                       edgecolors='black', linewidth=2,
                       label=f'Macro-cluster {int(mc_label)}' if i == 0 else "")
    
    if X.shape[1] > 2:
        plt.xlabel(f'PC1 ({var_exp[0]:.1%})')
    else:
        plt.xlabel('Feature 1')
    
    plt.title('Micro-cluster Assignment')
    if len(model.micro_clusters_) > 0:
        plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()