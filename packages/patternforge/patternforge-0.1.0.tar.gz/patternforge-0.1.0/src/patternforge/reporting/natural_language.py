"""
Natural Language Reporter
==========================

Generates human-readable insights from analysis results:
- Pattern summaries
- Key findings
- Recommendations
- Executive summaries
"""

from typing import Dict, Any, List
import pandas as pd


class NaturalLanguageReporter:
    """Generate natural language insights."""
    
    def generate_report(self, analysis_results: Dict[str, Any],
                       data: pd.DataFrame = None) -> str:
        """
        Generate comprehensive natural language report.
        
        Parameters
        ----------
        analysis_results : dict
            Results from PatternForge.analyze()
        data : DataFrame, optional
            Original data for context
        
        Returns
        -------
        str
            Human-readable report
        """
        sections = []
        
        # Title
        sections.append("=" * 70)
        sections.append("PATTERNFORGE ANALYSIS REPORT")
        sections.append("=" * 70)
        sections.append("")
        
        # Dataset overview
        if data is not None:
            sections.append(self._dataset_summary(data))
            sections.append("")
        
        # Feature patterns
        if 'feature_patterns' in analysis_results:
            sections.append(self._feature_patterns_summary(analysis_results['feature_patterns']))
            sections.append("")
        
        # Topology
        if 'topology' in analysis_results:
            sections.append(self._topology_summary(analysis_results['topology']))
            sections.append("")
        
        # Anomalies
        if 'anomalies' in analysis_results:
            sections.append(self._anomalies_summary(analysis_results['anomalies']))
            sections.append("")
        
        # Rules
        if 'rules' in analysis_results:
            sections.append(self._rules_summary(analysis_results['rules']))
            sections.append("")
        
        # Complexity
        if 'complexity' in analysis_results:
            sections.append(self._complexity_summary(analysis_results['complexity']))
            sections.append("")
        
        # Hypotheses
        if 'hypotheses' in analysis_results:
            sections.append(self._hypotheses_summary(analysis_results['hypotheses']))
            sections.append("")
        
        # Key recommendations
        sections.append(self._generate_recommendations(analysis_results))
        
        return "\n".join(sections)
    
    def _dataset_summary(self, data: pd.DataFrame) -> str:
        """Summarize dataset characteristics."""
        lines = ["📊 DATASET OVERVIEW", "-" * 70]
        
        lines.append(f"• Samples: {len(data):,}")
        lines.append(f"• Features: {len(data.columns)}")
        
        numeric_cols = data.select_dtypes(include=['number']).columns
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        
        lines.append(f"  - Numeric: {len(numeric_cols)}")
        lines.append(f"  - Categorical: {len(categorical_cols)}")
        
        # Missing values
        missing = data.isnull().sum().sum()
        if missing > 0:
            missing_pct = missing / (len(data) * len(data.columns)) * 100
            lines.append(f"• Missing values: {missing:,} ({missing_pct:.1f}%)")
        
        return "\n".join(lines)
    
    def _feature_patterns_summary(self, patterns: Dict[str, Any]) -> str:
        """Summarize feature patterns."""
        lines = ["🔍 FEATURE PATTERNS", "-" * 70]
        
        # Importance
        if 'importance' in patterns:
            importance = patterns['importance']
            lines.append("\nMost Important Features:")
            for i, (feat, score) in enumerate(importance[:5], 1):
                lines.append(f"  {i}. {feat}: {score:.3f}")
        
        # Interactions
        if 'interactions' in patterns:
            interactions = patterns['interactions']
            if interactions:
                lines.append("\nKey Feature Interactions:")
                for i, interaction in enumerate(interactions[:3], 1):
                    feat1, feat2 = interaction['features']
                    strength = interaction['strength']
                    lines.append(f"  {i}. {feat1} ↔ {feat2} (strength: {strength:.2f})")
        
        # Dependencies
        if 'dependencies' in patterns:
            dependencies = patterns['dependencies']
            if dependencies:
                lines.append("\nFeature Dependencies:")
                for i, dep in enumerate(dependencies[:3], 1):
                    source, target = dep['features']
                    corr = dep['correlation']
                    lines.append(f"  {i}. {source} → {target} (correlation: {corr:.2f})")
        
        return "\n".join(lines)
    
    def _topology_summary(self, topology: Dict[str, Any]) -> str:
        """Summarize topological structures."""
        lines = ["🌐 TOPOLOGICAL STRUCTURES", "-" * 70]
        
        # Clusters
        if 'clusters' in topology:
            n_clusters = topology['clusters'].get('n_clusters', 0)
            lines.append(f"\n• Detected {n_clusters} distinct cluster(s)")
            
            if 'dbscan' in topology['clusters']:
                n_noise = topology['clusters']['dbscan'].get('n_noise_points', 0)
                if n_noise > 0:
                    lines.append(f"  - {n_noise} noise point(s) (outliers)")
        
        # Loops
        if 'loops' in topology and topology['loops']:
            loop_summary = [l for l in topology['loops'] if l.get('type') == 'summary']
            if loop_summary:
                n_loops = loop_summary[0].get('total_loops_detected', 0)
                lines.append(f"\n• Found {n_loops} cyclic structure(s)")
                lines.append("  → Indicates circular relationships in data")
        
        # Holes
        if 'holes' in topology and topology['holes']:
            lines.append(f"\n• Detected {len(topology['holes'])} void(s) or gap(s)")
            lines.append("  → Regions with sparse data or missing populations")
        
        # Geometry
        if 'geometry' in topology:
            geom = topology['geometry']
            if 'intrinsic_dimensionality' in geom:
                intrinsic_dim = geom['intrinsic_dimensionality']
                explicit_dim = geom.get('explicit_dimensionality', 0)
                lines.append(f"\n• Data dimensionality: {intrinsic_dim}/{explicit_dim} (intrinsic/explicit)")
                
                if intrinsic_dim < explicit_dim:
                    lines.append("  → Data has redundancy; dimensionality reduction applicable")
        
        return "\n".join(lines)
    
    def _anomalies_summary(self, anomalies: Dict[str, Any]) -> str:
        """Summarize anomaly detection results."""
        lines = ["⚠️  ANOMALIES", "-" * 70]
        
        data_type = anomalies.get('data_type', 'unknown')
        
        if data_type == 'tabular' and 'consensus_anomalies' in anomalies:
            consensus = anomalies['consensus_anomalies']
            n_anomalies = consensus.get('n_anomalies', 0)
            
            lines.append(f"\n• {n_anomalies} consensus anomaly(ies) detected")
            lines.append("  (Confirmed by multiple detection methods)")
            
            # Method breakdown
            if 'methods' in anomalies:
                lines.append("\nDetection methods:")
                for method, results in anomalies['methods'].items():
                    if 'n_anomalies' in results:
                        n = results['n_anomalies']
                        lines.append(f"  - {method}: {n} anomaly(ies)")
        
        elif data_type == 'timeseries':
            n_total = anomalies.get('n_total_anomalies', 0)
            lines.append(f"\n• {n_total} temporal anomaly(ies) detected")
            
            if 'anomalies' in anomalies:
                for anom in anomalies['anomalies'][:3]:
                    col = anom.get('column', 'unknown')
                    method = anom.get('method', 'unknown')
                    n = anom.get('n_anomalies', 0)
                    lines.append(f"  - {col}: {n} {method} anomaly(ies)")
        
        elif data_type == 'graph':
            n_anomalies = anomalies.get('n_anomalies', 0)
            lines.append(f"\n• {n_anomalies} structural anomaly(ies) in graph")
        
        return "\n".join(lines)
    
    def _rules_summary(self, rules: Dict[str, Any]) -> str:
        """Summarize extracted rules."""
        lines = ["📜 EXTRACTED RULES", "-" * 70]
        
        # Decision rules
        if 'rules' in rules and rules['rules']:
            lines.append("\nDecision Rules:")
            for i, rule in enumerate(rules['rules'][:3], 1):
                rule_text = rule.get('rule', 'N/A')
                lines.append(f"  {i}. IF {rule_text}")
                
                if 'prediction' in rule:
                    pred = rule['prediction']
                    lines.append(f"     THEN prediction = {pred}")
                
                if 'confidence' in rule:
                    conf = rule['confidence']
                    lines.append(f"     (confidence: {conf:.1%})")
        
        # Associations
        if 'associations' in rules and rules['associations']:
            lines.append("\nAssociation Rules:")
            for i, assoc in enumerate(rules['associations'][:3], 1):
                rule_text = assoc.get('rule', 'N/A')
                conf = assoc.get('confidence', 0)
                lines.append(f"  {i}. {rule_text} (confidence: {conf:.1%})")
        
        # Constraints
        if 'constraints' in rules and rules['constraints']:
            lines.append("\nData Constraints:")
            for i, constraint in enumerate(rules['constraints'][:5], 1):
                const_text = constraint.get('constraint', 'N/A')
                lines.append(f"  {i}. {const_text}")
        
        return "\n".join(lines)
    
    def _complexity_summary(self, complexity: Dict[str, Any]) -> str:
        """Summarize complexity metrics."""
        lines = ["🧮 PATTERN COMPLEXITY", "-" * 70]
        
        pci = complexity.get('pci', 0)
        interpretation = complexity.get('interpretation', 'Unknown')
        
        lines.append(f"\n• Pattern Complexity Index (PCI): {pci:.3f}")
        lines.append(f"  → {interpretation}")
        
        # Components
        if 'components' in complexity:
            components = complexity['components']
            lines.append("\nComplexity Components:")
            
            if 'entropy' in components:
                lines.append(f"  - Entropy: {components['entropy']:.3f}")
            if 'topology' in components:
                lines.append(f"  - Topology: {components['topology']:.3f}")
            if 'variance' in components:
                lines.append(f"  - Variance: {components['variance']:.3f}")
        
        return "\n".join(lines)
    
    def _hypotheses_summary(self, hypotheses: List[str]) -> str:
        """Summarize generated hypotheses."""
        lines = ["💡 GENERATED HYPOTHESES", "-" * 70]
        
        if hypotheses:
            lines.append("\nTestable hypotheses based on discovered patterns:")
            for i, hypothesis in enumerate(hypotheses, 1):
                lines.append(f"\n{i}. {hypothesis}")
        else:
            lines.append("\nNo specific hypotheses generated.")
        
        return "\n".join(lines)
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> str:
        """Generate actionable recommendations."""
        lines = ["🎯 RECOMMENDATIONS", "-" * 70]
        
        recommendations = []
        
        # Based on topology
        if 'topology' in results:
            geom = results['topology'].get('geometry', {})
            if geom.get('intrinsic_dimensionality', 0) < geom.get('explicit_dimensionality', 0):
                recommendations.append(
                    "• Apply dimensionality reduction (PCA, t-SNE) to simplify data"
                )
        
        # Based on anomalies
        if 'anomalies' in results:
            n_anomalies = results['anomalies'].get('consensus_anomalies', {}).get('n_anomalies', 0)
            if n_anomalies > 0:
                recommendations.append(
                    f"• Investigate {n_anomalies} detected anomalies for data quality issues"
                )
        
        # Based on complexity
        if 'complexity' in results:
            pci = results['complexity'].get('pci', 0)
            if pci > 0.7:
                recommendations.append(
                    "• High complexity detected; consider ensemble models or deep learning"
                )
            elif pci < 0.3:
                recommendations.append(
                    "• Low complexity; simple linear models may suffice"
                )
        
        # Based on feature patterns
        if 'feature_patterns' in results:
            interactions = results['feature_patterns'].get('interactions', [])
            if len(interactions) > 0:
                recommendations.append(
                    "• Feature interactions detected; use tree-based models or feature engineering"
                )
        
        if recommendations:
            lines.append("")
            lines.extend(recommendations)
        else:
            lines.append("\nNo specific recommendations at this time.")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
