"""
Basic usage examples for MCMSTClustering.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs, make_circles
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score

# Import MCMSTClustering
from mcmst_clust import MCMSTClustering, plot_clusters_2d, find_optimal_parameters

def example_1_simple_clustering():
    """Example 1: Simple clustering with synthetic data."""
    print("=" * 60)
    print("EXAMPLE 1: Simple Clustering")
    print("=" * 60)
    
    # Generate synthetic data
    X, y_true = make_moons(n_samples=300, noise=0.05, random_state=42)
    
    # Create and fit the model
    model = MCMSTClustering(N=5, r=0.1, n_micro=3, random_state=42)
    y_pred = model.fit_predict(X)
    
    # Print results
    print(f"Number of samples: {X.shape[0]}")
    print(f"Number of micro-clusters: {model.n_micro_clusters_}")
    print(f"Number of macro-clusters: {model.n_macro_clusters_}")
    print(f"Adjusted Rand Index: {adjusted_rand_score(y_true, y_pred):.4f}")
    
    # Visualize
    plot_clusters_2d(model, X, title="Example 1: Moon Dataset Clustering")
    
    return model

def example_2_parameter_optimization():
    """Example 2: Finding optimal parameters."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Parameter Optimization")
    print("=" * 60)
    
    # Generate concentric circles
    X, y_true = make_circles(n_samples=300, factor=0.5, noise=0.05, random_state=42)
    
    # Find optimal parameters
    result = find_optimal_parameters(X, y_true, n_iter=50, random_state=42)
    
    print(f"Optimal parameters found in 50 iterations:")
    print(f"  N: {result['params']['N']}")
    print(f"  r: {result['params']['r']:.3f}")
    print(f"  n_micro: {result['params']['n_micro']}")
    print(f"  Best ARI: {result['score']:.4f}")
    
    # Train with optimal parameters
    model = MCMSTClustering(**result['params'], random_state=42)
    y_pred = model.fit_predict(X)
    
    # Visualize
    plot_clusters_2d(model, X, title="Example 2: Circles Dataset with Optimal Parameters")
    
    return model

def example_3_iris_dataset():
    """Example 3: Real-world dataset (Iris)."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Iris Dataset")
    print("=" * 60)
    
    # Load Iris dataset
    try:
        # Try to load from sklearn
        from sklearn.datasets import load_iris
        data = load_iris()
        X = data.data
        y_true = data.target
        feature_names = data.feature_names
        
        print(f"Dataset: Iris")
        print(f"Samples: {X.shape[0]}, Features: {X.shape[1]}")
        print(f"Feature names: {feature_names}")
        print(f"True classes: {len(np.unique(y_true))}")
        
    except:
        # Fallback to your file
        print("Loading from local file...")
        dataset = np.loadtxt("Datasets/iris.txt", dtype=float, delimiter=',')
        X = dataset[:, 0:4]
        y_true = dataset[:, 4]
    
    # Normalize data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Manual parameter search (similar to your original code)
    print("\nRunning parameter search (100 iterations)...")
    best_ari = -1
    best_params = {}
    best_model = None
    
    for i in range(100):
        N = np.random.randint(3, 15)
        r = np.random.uniform(0.05, 0.3)
        n_micro = np.random.randint(2, 8)
        
        try:
            model = MCMSTClustering(N=N, r=r, n_micro=n_micro, random_state=42)
            y_pred = model.fit_predict(X_scaled)
            
            ari = adjusted_rand_score(y_true, y_pred)
            if ari > best_ari:
                best_ari = ari
                best_params = {'N': N, 'r': r, 'n_micro': n_micro}
                best_model = model
                
                if i % 20 == 0:
                    print(f"  Iteration {i}: ARI = {ari:.4f}")
        except:
            continue
    
    print(f"\nBest parameters found:")
    print(f"  N: {best_params['N']}")
    print(f"  r: {best_params['r']:.3f}")
    print(f"  n_micro: {best_params['n_micro']}")
    print(f"  Best ARI: {best_ari:.4f}")
    
    print(f"\nModel statistics:")
    print(f"  Micro-clusters: {best_model.n_micro_clusters_}")
    print(f"  Macro-clusters: {best_model.n_macro_clusters_}")
    
    # Compare with paper results
    print("\nComparison with paper results:")
    print("  Paper ARI for Iris: 0.8446")
    print(f"  Our ARI: {best_ari:.4f}")
    
    return best_model

def example_4_comparison_with_other_algorithms():
    """Example 4: Compare with DBSCAN and K-means."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Comparison with Other Algorithms")
    print("=" * 60)
    
    # Generate complex dataset
    X1, y1 = make_blobs(n_samples=150, centers=3, cluster_std=0.6, random_state=0)
    X2, y2 = make_moons(n_samples=150, noise=0.05, random_state=0)
    X = np.vstack([X1, X2])
    y_true = np.hstack([y1, y2 + 3])  # Offset labels
    
    # Normalize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # MCMSTClustering
    print("\n1. MCMSTClustering:")
    mcmst_model = MCMSTClustering(N=5, r=0.15, n_micro=3, random_state=42)
    mcmst_labels = mcmst_model.fit_predict(X_scaled)
    mcmst_ari = adjusted_rand_score(y_true, mcmst_labels)
    print(f"   ARI: {mcmst_ari:.4f}")
    print(f"   Clusters found: {mcmst_model.n_macro_clusters_}")
    
    # DBSCAN
    print("\n2. DBSCAN:")
    try:
        from sklearn.cluster import DBSCAN
        dbscan = DBSCAN(eps=0.3, min_samples=5)
        dbscan_labels = dbscan.fit_predict(X_scaled)
        dbscan_ari = adjusted_rand_score(y_true, dbscan_labels)
        print(f"   ARI: {dbscan_ari:.4f}")
        print(f"   Clusters found: {len(np.unique(dbscan_labels)) - ( -1 in dbscan_labels)}")
    except:
        print("   DBSCAN not available")
    
    # K-means
    print("\n3. K-means:")
    try:
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=5, random_state=42)
        kmeans_labels = kmeans.fit_predict(X_scaled)
        kmeans_ari = adjusted_rand_score(y_true, kmeans_labels)
        print(f"   ARI: {kmeans_ari:.4f}")
    except:
        print("   K-means not available")
    
    # Visualize MCMSTClustering results
    plot_clusters_2d(mcmst_model, X_scaled, title="Example 4: Complex Dataset - MCMSTClustering")
    
    return mcmst_model

def example_5_custom_dataset():
    """Example 5: Using your own dataset."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Custom Dataset")
    print("=" * 60)
    
    # This example shows how to use your original datasets
    print("To use your custom datasets (like Half Kernel, Jain, etc.):")
    print("\n1. Load your data:")
    print("   dataset = np.loadtxt('Datasets/your_dataset.txt')")
    print("   X = dataset[:, :-1]  # Features")
    print("   y_true = dataset[:, -1]  # Labels (if available)")
    
    print("\n2. Normalize the data:")
    print("   from sklearn.preprocessing import MinMaxScaler")
    print("   scaler = MinMaxScaler()")
    print("   X_normalized = scaler.fit_transform(X)")
    
    print("\n3. Create and fit the model:")
    print("   model = MCMSTClustering(N=5, r=0.1, n_micro=3)")
    print("   labels = model.fit_predict(X_normalized)")
    
    print("\n4. Evaluate (if true labels available):")
    print("   from sklearn.metrics import adjusted_rand_score")
    print("   ari = adjusted_rand_score(y_true, labels)")
    print("   print(f'ARI: {ari:.4f}')")
    
    print("\n5. Find optimal parameters:")
    print("   from mcmstclustering import find_optimal_parameters")
    print("   result = find_optimal_parameters(X_normalized, y_true, n_iter=100)")
    print("   print(f'Best parameters: {result['params']}')")
    print("   print(f'Best ARI: {result['score']:.4f}')")
    
    # Provide a template for your specific datasets
    print("\n" + "-" * 40)
    print("Template for your datasets:")
    print("-" * 40)
    
    template_code = '''
import numpy as np
from mcmst_clust import MCMSTClustering, find_optimal_parameters
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import adjusted_rand_score

# Load your dataset
# Example for Half Kernel:
# data = np.loadtxt("Datasets/halfkernel.txt")
# X = data[:, :-1]
# y_true = data[:, -1]

# Normalize
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

# Parameter optimization (similar to your loop)
best_ari = -1
best_params = {}

for _ in range(1000):
    N = np.random.randint(3, 25)
    r = np.random.uniform(0.001, 1)
    n_micro = np.random.randint(2, 25)
    
    try:
        model = MCMSTClustering(N=N, r=r, n_micro=n_micro)
        labels = model.fit_predict(X_normalized)
        
        ari = adjusted_rand_score(y_true, labels)
        if ari > best_ari:
            best_ari = ari
            best_params = {'N': N, 'r': r, 'n_micro': n_micro}
    except:
        continue

print(f"Best ARI: {best_ari:.4f}")
print(f"Best parameters: {best_params}")
'''
    
    print(template_code)
    
    return None

def main():
    """Run all examples."""
    print("MCMSTClustering Examples")
    print("=" * 60)
    
    # Run examples
    model1 = example_1_simple_clustering()
    model2 = example_2_parameter_optimization()
    model3 = example_3_iris_dataset()
    model4 = example_4_comparison_with_other_algorithms()
    example_5_custom_dataset()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()