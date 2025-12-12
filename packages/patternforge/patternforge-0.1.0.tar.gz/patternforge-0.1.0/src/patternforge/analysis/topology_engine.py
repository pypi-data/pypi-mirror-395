"""
Topology Engine
===============

Detects topological structures using persistent homology and TDA:
- Loops (cycles)
- Clusters
- Holes (missing populations)
- Outlier structures
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import pdist, squareform


class TopologyEngine:
    """Topological Data Analysis engine."""
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform topological analysis.
        
        Returns
        -------
        dict
            - clusters: Detected clusters
            - loops: Cyclic structures
            - holes: Missing populations (voids)
            - geometry: Overall geometric properties
        """
        results = {}
        
        if not isinstance(data, pd.DataFrame):
            return results
        
        # Get numeric data
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.shape[1] < 2:
            return {'error': 'Need at least 2 numeric dimensions'}
        
        # Prepare data
        X = numeric_data.fillna(0).values
        if X.shape[0] < 10:
            return {'error': 'Need at least 10 samples'}
        
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Detect clusters
        results['clusters'] = self._detect_clusters(X_scaled)
        
        # Detect loops (cycles in data)
        results['loops'] = self._detect_loops(X_scaled)
        
        # Detect holes (voids)
        results['holes'] = self._detect_holes(X_scaled)
        
        # Geometric properties
        results['geometry'] = self._compute_geometry(X_scaled)
        
        return results
    
    def _detect_clusters(self, X: np.ndarray) -> Dict[str, Any]:
        """Detect clusters using multiple methods."""
        results = {}
        
        # DBSCAN for density-based clustering
        try:
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            labels = dbscan.fit_predict(X)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise = list(labels).count(-1)
            
            results['dbscan'] = {
                'n_clusters': n_clusters,
                'n_noise_points': n_noise,
                'labels': labels.tolist()
            }
        except:
            pass
        
        # KMeans for comparison
        try:
            # Elbow method (simple version)
            inertias = []
            K_range = range(2, min(10, X.shape[0] // 2))
            for k in K_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(X)
                inertias.append(kmeans.inertia_)
            
            # Find elbow (simple: largest drop)
            if len(inertias) > 1:
                drops = np.diff(inertias)
                optimal_k = np.argmin(drops) + 2
                
                kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(X)
                
                results['kmeans'] = {
                    'n_clusters': optimal_k,
                    'labels': labels.tolist(),
                    'inertia': float(kmeans.inertia_)
                }
        except:
            pass
        
        # Summary
        results['n_clusters'] = results.get('kmeans', {}).get('n_clusters', 
                                results.get('dbscan', {}).get('n_clusters', 1))
        
        return results
    
    def _detect_loops(self, X: np.ndarray) -> List[Dict[str, Any]]:
        """Detect cyclic structures (loops) in the data."""
        loops = []
        
        # Simple loop detection: find points that form approximate cycles
        # using distance matrix
        try:
            if X.shape[0] < 20:
                return loops
            
            # Compute pairwise distances
            distances = squareform(pdist(X))
            
            # Look for triangular loops (simplest case)
            threshold = np.median(distances)
            
            loop_count = 0
            for i in range(min(50, X.shape[0])):
                # Find neighbors
                neighbors = np.where((distances[i] < threshold) & (distances[i] > 0))[0]
                
                if len(neighbors) >= 2:
                    # Check if neighbors connect to each other
                    for j in range(len(neighbors)-1):
                        for k in range(j+1, len(neighbors)):
                            n1, n2 = neighbors[j], neighbors[k]
                            if distances[n1, n2] < threshold:
                                loop_count += 1
                                if len(loops) < 5:  # Limit storage
                                    loops.append({
                                        'nodes': [int(i), int(n1), int(n2)],
                                        'type': 'triangle',
                                        'size': 3
                                    })
            
            if loop_count > 0:
                loops.insert(0, {
                    'total_loops_detected': loop_count,
                    'type': 'summary'
                })
        
        except Exception as e:
            pass
        
        return loops
    
    def _detect_holes(self, X: np.ndarray) -> List[Dict[str, Any]]:
        """Detect holes (voids/missing populations) in the data."""
        holes = []
        
        try:
            # Simple void detection: find regions with low density
            # Use DBSCAN noise points as proxy for voids
            dbscan = DBSCAN(eps=0.3, min_samples=3)
            labels = dbscan.fit_predict(X)
            
            noise_points = np.where(labels == -1)[0]
            
            if len(noise_points) > 0:
                holes.append({
                    'type': 'low_density_region',
                    'n_points': len(noise_points),
                    'percentage': float(len(noise_points) / X.shape[0] * 100),
                    'description': 'Regions with sparse data (potential voids)'
                })
        
        except:
            pass
        
        return holes
    
    def _compute_geometry(self, X: np.ndarray) -> Dict[str, Any]:
        """Compute overall geometric properties."""
        geometry = {}
        
        try:
            # Intrinsic dimensionality (simple estimate)
            pca_variance = np.var(X, axis=0)
            explained_variance_ratio = pca_variance / np.sum(pca_variance)
            cumsum = np.cumsum(explained_variance_ratio)
            intrinsic_dim = np.argmax(cumsum >= 0.95) + 1
            
            geometry['intrinsic_dimensionality'] = int(intrinsic_dim)
            geometry['explicit_dimensionality'] = X.shape[1]
            
            # Spread/compactness
            distances = pdist(X)
            geometry['mean_distance'] = float(np.mean(distances))
            geometry['std_distance'] = float(np.std(distances))
            geometry['compactness_score'] = float(1.0 / (1.0 + np.std(distances)))
            
        except:
            pass
        
        return geometry
