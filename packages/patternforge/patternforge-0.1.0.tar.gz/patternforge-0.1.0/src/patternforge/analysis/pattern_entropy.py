"""
Pattern Complexity Index (PCI)
================================

Combines:
- Shannon Entropy (information content)
- Topological complexity (homology rank)
- Statistical variance (spread)

Into a single unified complexity metric.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from scipy.stats import entropy


class PatternComplexityIndex:
    """
    Compute Pattern Complexity Index (PCI).
    
    PCI = α·H_norm + β·T_norm + γ·V_norm
    
    Where:
    - H_norm: Normalized Shannon entropy
    - T_norm: Normalized topological complexity
    - V_norm: Normalized variance
    - α, β, γ: Weights (default: equal weighting)
    """
    
    def __init__(self, alpha: float = 1/3, beta: float = 1/3, gamma: float = 1/3):
        """
        Parameters
        ----------
        alpha : float
            Weight for entropy component
        beta : float
            Weight for topological component
        gamma : float
            Weight for variance component
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        # Normalize weights
        total = alpha + beta + gamma
        self.alpha /= total
        self.beta /= total
        self.gamma /= total
    
    def compute(self, data: pd.DataFrame, topology_results: Dict = None) -> Dict[str, Any]:
        """
        Compute Pattern Complexity Index.
        
        Parameters
        ----------
        data : DataFrame
            Input data
        topology_results : dict, optional
            Results from TopologyEngine (for topological complexity)
        
        Returns
        -------
        dict
            PCI score and components
        """
        results = {
            'components': {},
            'pci': 0.0
        }
        
        # Entropy component
        entropy_score = self._compute_entropy(data)
        results['components']['entropy'] = entropy_score
        
        # Topological component
        topo_score = self._compute_topology_complexity(data, topology_results)
        results['components']['topology'] = topo_score
        
        # Variance component
        variance_score = self._compute_variance(data)
        results['components']['variance'] = variance_score
        
        # Compute PCI
        pci = (self.alpha * entropy_score + 
               self.beta * topo_score + 
               self.gamma * variance_score)
        
        results['pci'] = float(pci)
        results['weights'] = {
            'alpha': self.alpha,
            'beta': self.beta,
            'gamma': self.gamma
        }
        results['interpretation'] = self._interpret_pci(pci)
        
        return results
    
    def _compute_entropy(self, data: pd.DataFrame) -> float:
        """Compute normalized Shannon entropy."""
        total_entropy = 0.0
        n_cols = 0
        
        for col in data.columns:
            try:
                if data[col].dtype == 'object' or data[col].dtype.name == 'category':
                    # Categorical: compute entropy of value distribution
                    value_counts = data[col].value_counts(normalize=True)
                    col_entropy = entropy(value_counts)
                    # Normalize by log(n_categories)
                    max_entropy = np.log(len(value_counts))
                    if max_entropy > 0:
                        total_entropy += col_entropy / max_entropy
                        n_cols += 1
                
                elif np.issubdtype(data[col].dtype, np.number):
                    # Numeric: discretize and compute entropy
                    series = data[col].dropna()
                    if len(series) > 0:
                        # Bin into 10 bins
                        bins = min(10, len(series.unique()))
                        hist, _ = np.histogram(series, bins=bins)
                        hist = hist / hist.sum()  # Normalize
                        col_entropy = entropy(hist)
                        # Normalize by log(n_bins)
                        max_entropy = np.log(bins)
                        if max_entropy > 0:
                            total_entropy += col_entropy / max_entropy
                            n_cols += 1
            except:
                continue
        
        if n_cols == 0:
            return 0.0
        
        # Average across columns
        return total_entropy / n_cols
    
    def _compute_topology_complexity(self, data: pd.DataFrame, 
                                    topology_results: Dict = None) -> float:
        """Compute topological complexity."""
        if topology_results is None:
            # Simplified topology estimate
            numeric_data = data.select_dtypes(include=[np.number])
            
            if numeric_data.shape[1] < 2:
                return 0.0
            
            # Use number of clusters as proxy
            from sklearn.cluster import KMeans
            X = numeric_data.fillna(0).values
            
            try:
                # Estimate optimal clusters (simple method)
                max_k = min(10, X.shape[0] // 2)
                if max_k < 2:
                    return 0.0
                
                inertias = []
                for k in range(2, max_k + 1):
                    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                    kmeans.fit(X)
                    inertias.append(kmeans.inertia_)
                
                # Complexity increases with more distinct clusters
                # Normalize by maximum possible
                n_clusters = len(inertias) + 1
                return min(n_clusters / max_k, 1.0)
            
            except:
                return 0.0
        
        else:
            # Use actual topology results
            n_clusters = topology_results.get('clusters', {}).get('n_clusters', 1)
            n_loops = len(topology_results.get('loops', []))
            n_holes = len(topology_results.get('holes', []))
            
            # Combine: more structure = higher complexity
            complexity = (n_clusters / 10.0 +  # Normalize to 0-1
                         n_loops / 5.0 + 
                         n_holes / 5.0)
            
            return min(complexity, 1.0)
    
    def _compute_variance(self, data: pd.DataFrame) -> float:
        """Compute normalized variance component."""
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.shape[1] == 0:
            return 0.0
        
        # Coefficient of variation (CV) averaged across columns
        cv_values = []
        
        for col in numeric_data.columns:
            series = numeric_data[col].dropna()
            if len(series) > 1:
                mean = series.mean()
                std = series.std()
                
                if mean != 0:
                    cv = abs(std / mean)
                    cv_values.append(cv)
        
        if not cv_values:
            return 0.0
        
        # Average CV, normalized to 0-1 (using tanh to bound)
        mean_cv = np.mean(cv_values)
        normalized = np.tanh(mean_cv)  # Maps [0, inf) -> [0, 1)
        
        return float(normalized)
    
    def _interpret_pci(self, pci: float) -> str:
        """Interpret PCI score."""
        if pci < 0.3:
            return "Low complexity - Simple, uniform patterns"
        elif pci < 0.5:
            return "Moderate complexity - Some structure and variation"
        elif pci < 0.7:
            return "High complexity - Rich patterns with multiple structures"
        else:
            return "Very high complexity - Highly diverse, intricate patterns"
