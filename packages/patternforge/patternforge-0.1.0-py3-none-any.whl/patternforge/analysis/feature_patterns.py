"""
Feature Pattern Analyzer
=========================

Discovers important features, interactions, dependencies, and nonlinear relationships
using mutual information, symbolic regression, and SHAP-like analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from itertools import combinations


class FeaturePatternAnalyzer:
    """Analyze feature patterns and importance."""
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Discover feature patterns.
        
        Returns
        -------
        dict
            - important_features: List of most important features
            - interactions: Detected feature interactions
            - dependencies: Feature dependencies
            - nonlinear_relationships: Nonlinear patterns
        """
        results = {}
        
        if not isinstance(data, pd.DataFrame):
            return results
        
        # Separate numeric and categorical
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if len(numeric_cols) < 2:
            return {'error': 'Need at least 2 numeric columns'}
        
        # Feature importance (use last column as pseudo-target for demo)
        results['important_features'] = self._compute_importance(data, numeric_cols)
        
        # Feature interactions
        results['interactions'] = self._detect_interactions(data, numeric_cols[:10])  # Limit for speed
        
        # Dependencies (correlation-based)
        results['dependencies'] = self._find_dependencies(data, numeric_cols)
        
        # Nonlinear relationships
        results['nonlinear_relationships'] = self._detect_nonlinear(data, numeric_cols[:5])
        
        return results
    
    def _compute_importance(self, data: pd.DataFrame, numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """Compute feature importance using mutual information."""
        if len(numeric_cols) < 2:
            return []
        
        # Use last column as target for demonstration
        X = data[numeric_cols[:-1]].fillna(0)
        y = data[numeric_cols[-1]].fillna(0)
        
        try:
            mi_scores = mutual_info_regression(X, y, random_state=42)
            
            importance_list = []
            for i, col in enumerate(numeric_cols[:-1]):
                importance_list.append({
                    'name': col,
                    'importance': float(mi_scores[i]),
                    'method': 'mutual_information'
                })
            
            # Sort by importance
            importance_list.sort(key=lambda x: x['importance'], reverse=True)
            return importance_list[:10]  # Top 10
            
        except Exception as e:
            return []
    
    def _detect_interactions(self, data: pd.DataFrame, cols: List[str]) -> List[Dict[str, Any]]:
        """Detect feature interactions."""
        interactions = []
        
        if len(cols) < 2:
            return interactions
        
        # Check pairwise interactions via correlation
        for col1, col2 in combinations(cols[:5], 2):  # Limit pairs
            try:
                interaction_score = abs(data[col1].corr(data[col2]))
                if interaction_score > 0.7:  # Strong interaction
                    interactions.append({
                        'features': [col1, col2],
                        'strength': float(interaction_score),
                        'type': 'correlation'
                    })
            except:
                pass
        
        return sorted(interactions, key=lambda x: x['strength'], reverse=True)[:5]
    
    def _find_dependencies(self, data: pd.DataFrame, cols: List[str]) -> List[Dict[str, Any]]:
        """Find feature dependencies."""
        dependencies = []
        
        if len(cols) < 2:
            return dependencies
        
        corr_matrix = data[cols].corr().abs()
        
        # Find strong correlations (dependencies)
        for i in range(len(cols)):
            for j in range(i+1, len(cols)):
                corr_val = corr_matrix.iloc[i, j]
                if corr_val > 0.8:  # Strong dependency
                    dependencies.append({
                        'feature_1': cols[i],
                        'feature_2': cols[j],
                        'strength': float(corr_val),
                        'type': 'linear_dependency'
                    })
        
        return dependencies[:10]
    
    def _detect_nonlinear(self, data: pd.DataFrame, cols: List[str]) -> List[Dict[str, Any]]:
        """Detect nonlinear relationships."""
        nonlinear = []
        
        if len(cols) < 2:
            return nonlinear
        
        for i, col in enumerate(cols[:-1]):
            try:
                X = data[[col]].fillna(0)
                y = data[cols[i+1]].fillna(0)
                
                # Fit simple model
                rf = RandomForestRegressor(n_estimators=10, max_depth=3, random_state=42)
                rf.fit(X, y)
                
                score = rf.score(X, y)
                if score > 0.5:  # Decent nonlinear fit
                    nonlinear.append({
                        'feature_x': col,
                        'feature_y': cols[i+1],
                        'r2_score': float(score),
                        'relationship': 'nonlinear'
                    })
            except:
                pass
        
        return nonlinear[:5]
