"""
Dashboard Generator
===================

Creates visualizations and dashboards:
- Feature importance plots
- Topology visualizations
- Anomaly plots
- Complexity metrics
- Pattern galleries
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
import io
import base64


class DashboardGenerator:
    """Generate visualizations and dashboards."""
    
    def __init__(self, figsize: tuple = (12, 8), style: str = 'default'):
        """
        Parameters
        ----------
        figsize : tuple
            Default figure size
        style : str
            Matplotlib style ('default', 'seaborn', 'ggplot')
        """
        self.figsize = figsize
        if style in plt.style.available:
            plt.style.use(style)
    
    def create_dashboard(self, analysis_results: Dict[str, Any],
                        data: pd.DataFrame = None,
                        output_file: str = None) -> Optional[str]:
        """
        Create comprehensive dashboard.
        
        Parameters
        ----------
        analysis_results : dict
            Results from PatternForge.analyze()
        data : DataFrame, optional
            Original data
        output_file : str, optional
            Save to file (PNG, PDF)
        
        Returns
        -------
        str or None
            Base64 encoded image if output_file is None
        """
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Feature importance
        if 'feature_patterns' in analysis_results:
            ax1 = fig.add_subplot(gs[0, :2])
            self._plot_feature_importance(ax1, analysis_results['feature_patterns'])
        
        # Complexity metrics
        if 'complexity' in analysis_results:
            ax2 = fig.add_subplot(gs[0, 2])
            self._plot_complexity(ax2, analysis_results['complexity'])
        
        # Topology - clusters
        if 'topology' in analysis_results and data is not None:
            ax3 = fig.add_subplot(gs[1, 0])
            self._plot_clusters(ax3, data, analysis_results['topology'])
        
        # Anomalies
        if 'anomalies' in analysis_results:
            ax4 = fig.add_subplot(gs[1, 1])
            self._plot_anomalies(ax4, analysis_results['anomalies'])
        
        # Feature interactions
        if 'feature_patterns' in analysis_results:
            ax5 = fig.add_subplot(gs[1, 2])
            self._plot_interactions(ax5, analysis_results['feature_patterns'])
        
        # Rules summary
        if 'rules' in analysis_results:
            ax6 = fig.add_subplot(gs[2, :])
            self._plot_rules_summary(ax6, analysis_results['rules'])
        
        fig.suptitle('PatternForge Analysis Dashboard', fontsize=16, fontweight='bold')
        
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()
            return None
        else:
            # Return base64 encoded
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            return img_base64
    
    def _plot_feature_importance(self, ax, patterns: Dict[str, Any]):
        """Plot feature importance."""
        if 'importance' not in patterns:
            ax.text(0.5, 0.5, 'No importance data', ha='center', va='center')
            ax.set_title('Feature Importance')
            return
        
        importance = patterns['importance'][:10]  # Top 10
        features = [f[0] for f in importance]
        scores = [f[1] for f in importance]
        
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(features)))
        bars = ax.barh(features, scores, color=colors)
        
        ax.set_xlabel('Importance Score')
        ax.set_title('Top Feature Importance', fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
    
    def _plot_complexity(self, ax, complexity: Dict[str, Any]):
        """Plot complexity components."""
        pci = complexity.get('pci', 0)
        components = complexity.get('components', {})
        
        # Gauge plot for PCI
        theta = np.linspace(0, np.pi, 100)
        r = 1
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        ax.plot(x, y, 'k-', linewidth=2)
        ax.fill_between(x, 0, y, alpha=0.2, color='gray')
        
        # Color regions
        colors = ['green', 'yellow', 'orange', 'red']
        boundaries = [0, 0.3, 0.5, 0.7, 1.0]
        
        for i in range(len(colors)):
            theta_seg = np.linspace(boundaries[i] * np.pi, boundaries[i+1] * np.pi, 50)
            x_seg = r * np.cos(theta_seg)
            y_seg = r * np.sin(theta_seg)
            ax.fill_between(x_seg, 0, y_seg, alpha=0.3, color=colors[i])
        
        # PCI needle
        pci_angle = pci * np.pi
        needle_x = [0, 0.9 * np.cos(pci_angle)]
        needle_y = [0, 0.9 * np.sin(pci_angle)]
        ax.plot(needle_x, needle_y, 'r-', linewidth=3)
        ax.plot(0, 0, 'ro', markersize=8)
        
        ax.text(0, -0.3, f'PCI: {pci:.3f}', ha='center', fontsize=12, fontweight='bold')
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.5, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Pattern Complexity Index', fontweight='bold')
    
    def _plot_clusters(self, ax, data: pd.DataFrame, topology: Dict[str, Any]):
        """Plot clusters (2D projection)."""
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.shape[1] < 2:
            ax.text(0.5, 0.5, 'Need 2+ numeric features', ha='center', va='center')
            ax.set_title('Cluster Visualization')
            return
        
        # Use first two numeric columns
        X = numeric_data.iloc[:, :2].fillna(0).values
        
        # Get cluster labels
        labels = None
        if 'clusters' in topology:
            if 'kmeans' in topology['clusters']:
                labels = topology['clusters']['kmeans'].get('labels', None)
            elif 'dbscan' in topology['clusters']:
                labels = topology['clusters']['dbscan'].get('labels', None)
        
        if labels is not None:
            labels = np.array(labels)
            unique_labels = np.unique(labels)
            colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))
            
            for i, label in enumerate(unique_labels):
                mask = labels == label
                if label == -1:  # Noise
                    ax.scatter(X[mask, 0], X[mask, 1], c='gray', marker='x', 
                             s=50, alpha=0.5, label='Noise')
                else:
                    ax.scatter(X[mask, 0], X[mask, 1], c=[colors[i]], 
                             s=50, alpha=0.7, label=f'Cluster {label}')
            
            ax.legend(fontsize=8)
        else:
            ax.scatter(X[:, 0], X[:, 1], alpha=0.5)
        
        ax.set_xlabel(numeric_data.columns[0])
        ax.set_ylabel(numeric_data.columns[1])
        ax.set_title('Clusters (2D Projection)', fontweight='bold')
        ax.grid(alpha=0.3)
    
    def _plot_anomalies(self, ax, anomalies: Dict[str, Any]):
        """Plot anomaly statistics."""
        data_type = anomalies.get('data_type', 'unknown')
        
        if data_type == 'tabular' and 'methods' in anomalies:
            methods = []
            counts = []
            
            for method, results in anomalies['methods'].items():
                if 'n_anomalies' in results:
                    methods.append(method.replace('_', '\n'))
                    counts.append(results['n_anomalies'])
            
            if methods:
                colors = ['#ff6b6b', '#ee5a6f', '#c44569']
                bars = ax.bar(methods, counts, color=colors[:len(methods)])
                ax.set_ylabel('Number of Anomalies')
                ax.set_title('Anomaly Detection Methods', fontweight='bold')
                ax.grid(axis='y', alpha=0.3)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}', ha='center', va='bottom')
            else:
                ax.text(0.5, 0.5, 'No anomalies detected', ha='center', va='center')
                ax.set_title('Anomaly Detection')
        else:
            n_anomalies = anomalies.get('n_anomalies', 0)
            ax.text(0.5, 0.5, f'{n_anomalies} anomalies\ndetected', 
                   ha='center', va='center', fontsize=14)
            ax.set_title(f'Anomalies ({data_type})', fontweight='bold')
        
        ax.set_xlim(-0.5, len(methods) - 0.5 if methods else 1)
    
    def _plot_interactions(self, ax, patterns: Dict[str, Any]):
        """Plot feature interactions as network."""
        if 'interactions' not in patterns or not patterns['interactions']:
            ax.text(0.5, 0.5, 'No interactions detected', ha='center', va='center')
            ax.set_title('Feature Interactions')
            ax.axis('off')
            return
        
        interactions = patterns['interactions'][:10]  # Top 10
        
        # Create simple network layout
        features = set()
        for interaction in interactions:
            features.update(interaction['features'])
        
        features = list(features)
        n_features = len(features)
        
        # Circular layout
        angles = np.linspace(0, 2*np.pi, n_features, endpoint=False)
        pos = {feat: (np.cos(angle), np.sin(angle)) 
               for feat, angle in zip(features, angles)}
        
        # Draw edges
        for interaction in interactions:
            feat1, feat2 = interaction['features']
            if feat1 in pos and feat2 in pos:
                x1, y1 = pos[feat1]
                x2, y2 = pos[feat2]
                
                strength = interaction.get('strength', 0)
                alpha = min(strength / 1.0, 1.0)  # Normalize
                
                ax.plot([x1, x2], [y1, y2], 'b-', alpha=alpha, linewidth=2*alpha)
        
        # Draw nodes
        for feat, (x, y) in pos.items():
            ax.plot(x, y, 'o', markersize=15, color='lightblue', 
                   markeredgecolor='navy', markeredgewidth=2)
            ax.text(x*1.2, y*1.2, feat, ha='center', va='center', 
                   fontsize=8, fontweight='bold')
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Feature Interactions Network', fontweight='bold')
    
    def _plot_rules_summary(self, ax, rules: Dict[str, Any]):
        """Plot rules summary as text."""
        ax.axis('off')
        
        text_lines = []
        
        # Decision rules
        if 'rules' in rules and rules['rules']:
            text_lines.append("🔹 Top Decision Rules:")
            for i, rule in enumerate(rules['rules'][:3], 1):
                rule_text = rule.get('rule', 'N/A')
                # Truncate if too long
                if len(rule_text) > 80:
                    rule_text = rule_text[:77] + '...'
                text_lines.append(f"  {i}. {rule_text}")
                
                if 'confidence' in rule:
                    conf = rule['confidence']
                    text_lines.append(f"     (confidence: {conf:.1%})")
            text_lines.append("")
        
        # Constraints
        if 'constraints' in rules and rules['constraints']:
            text_lines.append("🔹 Key Constraints:")
            for i, constraint in enumerate(rules['constraints'][:4], 1):
                const_text = constraint.get('constraint', 'N/A')
                text_lines.append(f"  {i}. {const_text}")
        
        if not text_lines:
            text_lines = ["No rules extracted"]
        
        # Display text
        y_pos = 0.95
        for line in text_lines:
            ax.text(0.05, y_pos, line, fontsize=9, verticalalignment='top',
                   family='monospace')
            y_pos -= 0.08
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('Extracted Rules & Constraints', fontweight='bold', loc='left')
