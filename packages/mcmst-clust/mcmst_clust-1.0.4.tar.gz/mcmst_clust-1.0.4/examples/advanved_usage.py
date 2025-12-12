"""
Advanced usage examples for MCMSTClustering.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.model_selection import ParameterGrid
import time

from mcmstclustering import MCMSTClustering, evaluate_clustering

def example_grid_search():
    """Example of grid search for parameters."""
    print("Grid Search Example")
    print("=" * 60)
    
    # Generate dataset
    X, y_true = make_blobs(n_samples=500, centers=5, 
                          cluster_std=[0.5, 1.0, 0.3, 0.8, 0.6],
                          random_state=42)
    
    # Define parameter grid
    param_grid = {
        'N': [3, 5, 8, 10],
        'r': [0.05, 0.1, 0.15, 0.2],
        'n_micro': [2, 3, 4, 5]
    }
    
    best_score = -1
    best_params = None
    best_model = None
    
    results = []
    
    print("Running grid search...")
    for i, params in enumerate(ParameterGrid(param_grid)):
        try:
            start_time = time.time()
            
            model = MCMSTClustering(**params, random_state=42)
            labels = model.fit_predict(X)
            
            # Calculate metrics
            metrics = evaluate_clustering(y_true, labels)
            elapsed = time.time() - start_time
            
            results.append({
                'params': params,
                'ARI': metrics['ARI'],
                'NMI': metrics['NMI'],
                'Purity': metrics['Purity'],
                'time': elapsed,
                'n_clusters': model.n_macro_clusters_
            })
            
            if metrics['ARI'] > best_score:
                best_score = metrics['ARI']
                best_params = params
                best_model = model
            
            if (i + 1) % 5 == 0:
                print(f"  Completed {i + 1} configurations")
                
        except Exception as e:
            continue
    
    # Print results
    print(f"\nTotal configurations tested: {len(results)}")
    print(f"\nBest configuration:")
    print(f"  Parameters: {best_params}")
    print(f"  ARI: {best_score:.4f}")
    print(f"  Clusters found: {best_model.n_macro_clusters_}")
    
    # Show top 5 results
    print("\nTop 5 configurations:")
    sorted_results = sorted(results, key=lambda x: x['ARI'], reverse=True)[:5]
    for i, result in enumerate(sorted_results):
        print(f"{i+1}. ARI: {result['ARI']:.4f}, "
              f"N: {result['params']['N']}, "
              f"r: {result['params']['r']}, "
              f"n_micro: {result['params']['n_micro']}, "
              f"Clusters: {result['n_clusters']}")
    
    return best_model

def example_high_dimensional_data():
    """Example with high-dimensional data."""
    print("\n" + "=" * 60)
    print("High-Dimensional Data Example")
    print("=" * 60)
    
    # Generate high-dimensional data
    n_samples = 1000
    n_features = 20
    n_clusters = 4
    
    X, y_true = make_blobs(n_samples=n_samples, n_features=n_features,
                          centers=n_clusters, random_state=42)
    
    print(f"Dataset shape: {X.shape}")
    print(f"True clusters: {len(np.unique(y_true))}")
    
    # Apply MCMSTClustering
    model = MCMSTClustering(N=10, r=0.3, n_micro=4, random_state=42)
    labels = model.fit_predict(X)
    
    print(f"\nMCMSTClustering results:")
    print(f"  Micro-clusters: {model.n_micro_clusters_}")
    print(f"  Macro-clusters: {model.n_macro_clusters_}")
    
    # Evaluate
    metrics = evaluate_clustering(y_true, labels)
    print(f"\nEvaluation metrics:")
    for metric_name, value in metrics.items():
        print(f"  {metric_name}: {value:.4f}")
    
    return model

def example_handling_outliers():
    """Example showing outlier handling."""
    print("\n" + "=" * 60)
    print("Outlier Handling Example")
    print("=" * 60)
    
    # Generate data with outliers
    n_inliers = 400
    n_outliers = 50
    
    # Inliers
    X_inliers, y_inliers = make_blobs(n_samples=n_inliers, centers=3, 
                                     cluster_std=0.8, random_state=42)
    
    # Outliers (uniform noise)
    X_outliers = np.random.uniform(low=-10, high=10, size=(n_outliers, 2))
    y_outliers = -1 * np.ones(n_outliers)  # Label outliers as -1
    
    # Combine
    X = np.vstack([X_inliers, X_outliers])
    y_true = np.hstack([y_inliers, y_outliers])
    
    print(f"Total samples: {X.shape[0]}")
    print(f"  Inliers: {n_inliers}")
    print(f"  Outliers: {n_outliers}")
    
    # Apply MCMSTClustering
    model = MCMSTClustering(N=8, r=0.5, n_micro=3, random_state=42)
    labels = model.fit_predict(X)
    
    # Identify outliers (points not assigned to any cluster)
    outlier_mask = labels == 0
    detected_outliers = np.sum(outlier_mask)
    
    print(f"\nOutlier detection results:")
    print(f"  Detected outliers: {detected_outliers}")
    print(f"  True outliers: {n_outliers}")
    
    # Calculate detection accuracy
    true_outlier_mask = y_true == -1
    correct_detections = np.sum(outlier_mask & true_outlier_mask)
    detection_accuracy = correct_detections / n_outliers
    
    print(f"  Correctly detected: {correct_detections}")
    print(f"  Detection accuracy: {detection_accuracy:.2%}")
    
    # Visualize
    plt.figure(figsize=(10, 5))
    
    # True labels
    plt.subplot(1, 2, 1)
    plt.scatter(X[y_true != -1, 0], X[y_true != -1, 1], 
               c=y_true[y_true != -1], cmap='tab10', s=30, alpha=0.7)
    plt.scatter(X[y_true == -1, 0], X[y_true == -1, 1], 
               c='black', marker='x', s=50, label='True outliers')
    plt.title("True Data (Red = Outliers)")
    plt.legend()
    
    # Predicted clusters
    plt.subplot(1, 2, 2)
    unique_labels = np.unique(labels)
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))
    
    for i, label in enumerate(unique_labels):
        if label == 0:
            color = 'black'
            marker = 'x'
            label_text = 'Detected outliers'
            size = 50
        else:
            color = colors[i-1] if i > 0 else colors[0]
            marker = 'o'
            label_text = f'Cluster {int(label)}'
            size = 30
        
        mask = labels == label
        plt.scatter(X[mask, 0], X[mask, 1], 
                   color=color, marker=marker, 
                   s=size, alpha=0.7, label=label_text)
    
    plt.title("MCMSTClustering Results")
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return model

def main():
    """Run advanced examples."""
    print("MCMSTClustering - Advanced Examples")
    print("=" * 60)
    
    # Run examples
    example_grid_search()
    example_high_dimensional_data()
    example_handling_outliers()
    
    print("\n" + "=" * 60)
    print("Advanced examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()