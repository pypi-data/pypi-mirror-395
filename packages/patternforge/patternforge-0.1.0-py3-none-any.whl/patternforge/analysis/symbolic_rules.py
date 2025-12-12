"""
Symbolic Rules Extraction
===========================

Extracts human-readable rules from patterns:
- Decision rules (if-then)
- Association rules
- Symbolic expressions
- Logical constraints
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, _tree
from collections import defaultdict


class SymbolicRulesExtractor:
    """Extract symbolic, human-readable rules."""
    
    def extract(self, data: pd.DataFrame, target_col: str = None, 
                max_rules: int = 10) -> Dict[str, Any]:
        """
        Extract symbolic rules from data.
        
        Parameters
        ----------
        data : DataFrame
            Input data
        target_col : str, optional
            Target column for supervised rules. If None, extract descriptive rules.
        max_rules : int
            Maximum number of rules to extract
        
        Returns
        -------
        dict
            Extracted rules and patterns
        """
        results = {
            'rules': [],
            'associations': [],
            'constraints': []
        }
        
        if target_col and target_col in data.columns:
            # Supervised rules (predict target)
            results['rules'] = self._extract_decision_rules(data, target_col, max_rules)
        
        # Association rules (co-occurrence)
        results['associations'] = self._extract_associations(data, max_rules)
        
        # Logical constraints (data patterns)
        results['constraints'] = self._extract_constraints(data, max_rules)
        
        return results
    
    def _extract_decision_rules(self, data: pd.DataFrame, target_col: str,
                                max_rules: int) -> List[Dict[str, Any]]:
        """Extract if-then decision rules using decision tree."""
        rules = []
        
        # Prepare data
        X = data.drop(columns=[target_col])
        y = data[target_col]
        
        # Get numeric features
        numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_features) < 1:
            return rules
        
        X_numeric = X[numeric_features].fillna(0)
        
        # Determine if classification or regression
        is_classification = (y.dtype == 'object' or 
                           y.dtype.name == 'category' or 
                           y.nunique() < 10)
        
        try:
            if is_classification:
                clf = DecisionTreeClassifier(max_depth=5, min_samples_split=10,
                                            random_state=42)
            else:
                clf = DecisionTreeRegressor(max_depth=5, min_samples_split=10,
                                           random_state=42)
            
            clf.fit(X_numeric, y)
            
            # Extract rules from tree
            tree_rules = self._tree_to_rules(clf, numeric_features, max_rules)
            
            for rule in tree_rules:
                rule['target'] = target_col
                rules.append(rule)
        
        except Exception as e:
            pass
        
        return rules
    
    def _tree_to_rules(self, tree_model, feature_names: List[str],
                      max_rules: int) -> List[Dict[str, Any]]:
        """Convert decision tree to rules."""
        tree_ = tree_model.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined"
            for i in tree_.feature
        ]
        
        rules = []
        
        def recurse(node, conditions):
            if len(rules) >= max_rules:
                return
            
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                
                # Left branch (<=)
                left_conditions = conditions + [(name, '<=', threshold)]
                recurse(tree_.children_left[node], left_conditions)
                
                # Right branch (>)
                right_conditions = conditions + [(name, '>', threshold)]
                recurse(tree_.children_right[node], right_conditions)
            
            else:
                # Leaf node - create rule
                if conditions:
                    rule_text = " AND ".join([
                        f"{name} {op} {val:.2f}" for name, op, val in conditions
                    ])
                    
                    value = tree_.value[node]
                    if isinstance(tree_model, DecisionTreeClassifier):
                        predicted_class = np.argmax(value)
                        n_samples = int(tree_.n_node_samples[node])
                        confidence = float(np.max(value) / np.sum(value))
                        
                        rules.append({
                            'rule': rule_text,
                            'prediction': predicted_class,
                            'support': n_samples,
                            'confidence': confidence
                        })
                    else:
                        predicted_value = float(value[0][0])
                        n_samples = int(tree_.n_node_samples[node])
                        
                        rules.append({
                            'rule': rule_text,
                            'prediction': predicted_value,
                            'support': n_samples
                        })
        
        recurse(0, [])
        
        # Sort by support (most common rules first)
        rules.sort(key=lambda x: x.get('support', 0), reverse=True)
        
        return rules[:max_rules]
    
    def _extract_associations(self, data: pd.DataFrame, 
                            max_rules: int) -> List[Dict[str, Any]]:
        """Extract association rules (simple co-occurrence)."""
        associations = []
        
        # Focus on categorical columns
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_cols) < 2:
            return associations
        
        # Pairwise associations
        for i, col1 in enumerate(categorical_cols[:5]):  # Limit columns
            for col2 in categorical_cols[i+1:5]:
                try:
                    # Cross-tabulation
                    crosstab = pd.crosstab(data[col1], data[col2])
                    
                    # Find strong associations
                    for idx in crosstab.index:
                        for col in crosstab.columns:
                            count = crosstab.loc[idx, col]
                            support = count / len(data)
                            
                            # Calculate confidence
                            col1_count = (data[col1] == idx).sum()
                            confidence = count / col1_count if col1_count > 0 else 0
                            
                            if support > 0.05 and confidence > 0.5:  # Thresholds
                                associations.append({
                                    'rule': f"IF {col1}={idx} THEN {col2}={col}",
                                    'support': float(support),
                                    'confidence': float(confidence),
                                    'count': int(count)
                                })
                
                except:
                    continue
        
        # Sort by confidence
        associations.sort(key=lambda x: x['confidence'], reverse=True)
        
        return associations[:max_rules]
    
    def _extract_constraints(self, data: pd.DataFrame,
                           max_rules: int) -> List[Dict[str, Any]]:
        """Extract logical constraints and patterns."""
        constraints = []
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        # Range constraints
        for col in numeric_cols[:10]:  # Limit
            try:
                series = data[col].dropna()
                
                if len(series) > 0:
                    min_val = series.min()
                    max_val = series.max()
                    mean_val = series.mean()
                    std_val = series.std()
                    
                    # Tight range constraint
                    if std_val / (mean_val + 1e-10) < 0.1:  # Low variance
                        constraints.append({
                            'type': 'tight_range',
                            'constraint': f"{col} ≈ {mean_val:.2f} (±{std_val:.2f})",
                            'description': f"{col} has low variance, mostly around {mean_val:.2f}"
                        })
                    
                    # Boundary constraint
                    constraints.append({
                        'type': 'bounds',
                        'constraint': f"{min_val:.2f} ≤ {col} ≤ {max_val:.2f}",
                        'description': f"{col} ranges from {min_val:.2f} to {max_val:.2f}"
                    })
            
            except:
                continue
        
        # Non-negativity constraints
        for col in numeric_cols[:10]:
            try:
                if (data[col].dropna() >= 0).all():
                    constraints.append({
                        'type': 'non_negative',
                        'constraint': f"{col} ≥ 0",
                        'description': f"{col} is always non-negative"
                    })
            except:
                continue
        
        # Correlation constraints (A increases with B)
        for i, col1 in enumerate(numeric_cols[:5]):
            for col2 in numeric_cols[i+1:5]:
                try:
                    corr = data[[col1, col2]].corr().iloc[0, 1]
                    
                    if abs(corr) > 0.7:
                        direction = "increases" if corr > 0 else "decreases"
                        constraints.append({
                            'type': 'correlation',
                            'constraint': f"{col1} {direction} with {col2}",
                            'correlation': float(corr),
                            'description': f"Strong {'positive' if corr > 0 else 'negative'} correlation"
                        })
                
                except:
                    continue
        
        return constraints[:max_rules]
