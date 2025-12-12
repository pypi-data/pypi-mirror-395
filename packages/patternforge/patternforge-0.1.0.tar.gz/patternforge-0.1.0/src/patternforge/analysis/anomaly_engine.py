"""
Universal Anomaly Detection Engine
===================================

Detects anomalies across multiple data types:
- Tabular anomalies (outliers, deviations)
- Sequence anomalies (temporal, text)
- Graph anomalies (structural)
- Geospatial anomalies
- Categorical anomalies
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.preprocessing import StandardScaler
import networkx as nx


class UniversalAnomalyDetector:
    """Universal anomaly detection across data types."""
    
    def __init__(self, contamination: float = 0.1):
        """
        Parameters
        ----------
        contamination : float
            Expected proportion of anomalies (0.0 to 0.5)
        """
        self.contamination = contamination
    
    def detect(self, data: Any, data_type: str = 'auto') -> Dict[str, Any]:
        """
        Universal anomaly detection.
        
        Parameters
        ----------
        data : DataFrame, ndarray, list, or networkx.Graph
            Input data
        data_type : str
            Type hint: 'auto', 'tabular', 'timeseries', 'text', 'graph'
        
        Returns
        -------
        dict
            Anomaly detection results with indices/descriptions
        """
        # Auto-detect data type
        if data_type == 'auto':
            data_type = self._infer_data_type(data)
        
        # Route to appropriate detector
        if data_type == 'tabular':
            return self._detect_tabular(data)
        elif data_type == 'timeseries':
            return self._detect_timeseries(data)
        elif data_type == 'text':
            return self._detect_text(data)
        elif data_type == 'graph':
            return self._detect_graph(data)
        else:
            return {'error': f'Unsupported data type: {data_type}'}
    
    def _infer_data_type(self, data: Any) -> str:
        """Infer data type from structure."""
        if isinstance(data, nx.Graph):
            return 'graph'
        elif isinstance(data, pd.DataFrame):
            # Check for time series
            if any(col.lower() in ['date', 'time', 'datetime', 'timestamp'] 
                   for col in data.columns):
                return 'timeseries'
            return 'tabular'
        elif isinstance(data, (list, np.ndarray)):
            if len(data) > 0 and isinstance(data[0], str):
                return 'text'
            return 'timeseries'
        return 'tabular'
    
    def _detect_tabular(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Detect anomalies in tabular data."""
        results = {
            'data_type': 'tabular',
            'methods': {}
        }
        
        # Get numeric data
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.shape[1] < 2:
            return {'error': 'Need at least 2 numeric columns'}
        
        X = numeric_data.fillna(0).values
        
        # Isolation Forest
        try:
            iso_forest = IsolationForest(
                contamination=self.contamination,
                random_state=42,
                n_estimators=100
            )
            iso_labels = iso_forest.fit_predict(X)
            iso_scores = iso_forest.score_samples(X)
            
            anomaly_indices = np.where(iso_labels == -1)[0]
            
            results['methods']['isolation_forest'] = {
                'n_anomalies': len(anomaly_indices),
                'anomaly_indices': anomaly_indices.tolist(),
                'anomaly_scores': iso_scores[anomaly_indices].tolist()
            }
        except Exception as e:
            results['methods']['isolation_forest'] = {'error': str(e)}
        
        # Elliptic Envelope (Gaussian assumption)
        try:
            if X.shape[0] > X.shape[1]:  # Need more samples than features
                envelope = EllipticEnvelope(
                    contamination=self.contamination,
                    random_state=42
                )
                env_labels = envelope.fit_predict(X)
                
                anomaly_indices = np.where(env_labels == -1)[0]
                
                results['methods']['elliptic_envelope'] = {
                    'n_anomalies': len(anomaly_indices),
                    'anomaly_indices': anomaly_indices.tolist()
                }
        except Exception as e:
            results['methods']['elliptic_envelope'] = {'error': str(e)}
        
        # Statistical outliers (Z-score)
        try:
            z_scores = np.abs((X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10))
            outlier_mask = (z_scores > 3).any(axis=1)
            anomaly_indices = np.where(outlier_mask)[0]
            
            results['methods']['z_score'] = {
                'n_anomalies': len(anomaly_indices),
                'anomaly_indices': anomaly_indices.tolist(),
                'threshold': 3.0
            }
        except Exception as e:
            results['methods']['z_score'] = {'error': str(e)}
        
        # Consensus anomalies (detected by multiple methods)
        all_anomalies = []
        for method in results['methods'].values():
            if 'anomaly_indices' in method:
                all_anomalies.extend(method['anomaly_indices'])
        
        if all_anomalies:
            from collections import Counter
            anomaly_counts = Counter(all_anomalies)
            consensus = [idx for idx, count in anomaly_counts.items() if count >= 2]
            
            results['consensus_anomalies'] = {
                'indices': consensus,
                'n_anomalies': len(consensus)
            }
        
        return results
    
    def _detect_timeseries(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Detect anomalies in time series data."""
        results = {
            'data_type': 'timeseries',
            'anomalies': []
        }
        
        # Find numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            series = data[col].dropna().values
            
            if len(series) < 10:
                continue
            
            # Moving average anomalies
            window = min(7, len(series) // 3)
            if window >= 2:
                moving_avg = np.convolve(series, np.ones(window)/window, mode='valid')
                # Pad to match length
                moving_avg = np.pad(moving_avg, (window//2, window - window//2 - 1), 
                                   mode='edge')
                
                deviation = np.abs(series - moving_avg)
                threshold = np.mean(deviation) + 3 * np.std(deviation)
                
                anomaly_indices = np.where(deviation > threshold)[0]
                
                if len(anomaly_indices) > 0:
                    results['anomalies'].append({
                        'column': col,
                        'method': 'moving_average',
                        'n_anomalies': len(anomaly_indices),
                        'indices': anomaly_indices.tolist()
                    })
            
            # Sudden changes (derivatives)
            if len(series) > 1:
                changes = np.abs(np.diff(series))
                threshold = np.mean(changes) + 3 * np.std(changes)
                
                spike_indices = np.where(changes > threshold)[0]
                
                if len(spike_indices) > 0:
                    results['anomalies'].append({
                        'column': col,
                        'method': 'sudden_change',
                        'n_anomalies': len(spike_indices),
                        'indices': spike_indices.tolist()
                    })
        
        results['n_total_anomalies'] = sum(a['n_anomalies'] for a in results['anomalies'])
        
        return results
    
    def _detect_text(self, data: List[str]) -> Dict[str, Any]:
        """Detect anomalies in text data."""
        results = {
            'data_type': 'text',
            'anomalies': []
        }
        
        # Length anomalies
        lengths = [len(text) for text in data]
        mean_len = np.mean(lengths)
        std_len = np.std(lengths)
        
        for i, length in enumerate(lengths):
            z_score = abs(length - mean_len) / (std_len + 1e-10)
            if z_score > 3:
                results['anomalies'].append({
                    'index': i,
                    'type': 'unusual_length',
                    'length': length,
                    'z_score': float(z_score)
                })
        
        # Character anomalies (unusual characters)
        import string
        normal_chars = set(string.printable)
        
        for i, text in enumerate(data):
            unusual_chars = set(text) - normal_chars
            if unusual_chars:
                results['anomalies'].append({
                    'index': i,
                    'type': 'unusual_characters',
                    'characters': list(unusual_chars)
                })
        
        results['n_anomalies'] = len(results['anomalies'])
        
        return results
    
    def _detect_graph(self, graph: nx.Graph) -> Dict[str, Any]:
        """Detect structural anomalies in graph."""
        results = {
            'data_type': 'graph',
            'anomalies': []
        }
        
        # Degree anomalies
        degrees = dict(graph.degree())
        degree_values = list(degrees.values())
        
        mean_degree = np.mean(degree_values)
        std_degree = np.std(degree_values)
        
        for node, degree in degrees.items():
            z_score = abs(degree - mean_degree) / (std_degree + 1e-10)
            if z_score > 3:
                results['anomalies'].append({
                    'node': node,
                    'type': 'unusual_degree',
                    'degree': degree,
                    'z_score': float(z_score)
                })
        
        # Isolated nodes
        isolated = list(nx.isolates(graph))
        if isolated:
            results['anomalies'].append({
                'type': 'isolated_nodes',
                'nodes': isolated,
                'count': len(isolated)
            })
        
        # Bridge edges (critical connections)
        if nx.is_connected(graph):
            bridges = list(nx.bridges(graph))
            if bridges:
                results['anomalies'].append({
                    'type': 'bridge_edges',
                    'edges': [list(edge) for edge in bridges],
                    'count': len(bridges),
                    'description': 'Critical edges whose removal disconnects graph'
                })
        
        results['n_anomalies'] = len(results['anomalies'])
        
        return results
