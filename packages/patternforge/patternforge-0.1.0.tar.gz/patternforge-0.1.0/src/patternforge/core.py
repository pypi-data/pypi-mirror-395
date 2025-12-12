"""
PatternForge Core Engine
========================

Main interface for automatic pattern discovery.
"""

import pandas as pd
import numpy as np
from typing import Union, Dict, Any, Optional, List
from pathlib import Path

from patternforge.loaders.tabular import TabularLoader
from patternforge.loaders.timeseries import TimeSeriesLoader
from patternforge.loaders.text import TextLoader
from patternforge.loaders.graph import GraphLoader
from patternforge.analysis.feature_patterns import FeaturePatternAnalyzer
from patternforge.analysis.topology_engine import TopologyEngine
from patternforge.analysis.anomaly_engine import UniversalAnomalyDetector
from patternforge.analysis.pattern_entropy import PatternComplexityIndex
from patternforge.analysis.symbolic_rules import SymbolicRuleExtractor
from patternforge.reporting.natural_language import NaturalLanguageReporter
from patternforge.reporting.dashboards import DashboardGenerator


class PatternForge:
    """
    Universal Automatic Pattern Discovery Engine.
    
    Automatically discovers hidden structures, rules, anomalies, and mathematical
    patterns in any dataset with zero configuration.
    
    Parameters
    ----------
    data : str, pd.DataFrame, dict, or array-like
        Input data. Can be:
        - File path (CSV, JSON, Excel, Parquet)
        - DataFrame
        - Dictionary (for graph data)
        - NumPy array
    data_type : str, optional
        Type of data: 'tabular', 'timeseries', 'text', 'graph', 'geospatial'
        Auto-detected if not specified
    
    Examples
    --------
    >>> from patternforge import PatternForge
    >>> pf = PatternForge(data="transactions.csv")
    >>> results = pf.analyze()
    >>> pf.report(show_graphs=True)
    """
    
    def __init__(
        self,
        data: Union[str, pd.DataFrame, Dict, np.ndarray],
        data_type: Optional[str] = None,
        verbose: bool = True
    ):
        self.verbose = verbose
        self.data_type = data_type
        self.raw_data = data
        self.data = None
        self.results = {}
        
        # Initialize components
        self._load_data()
        self._initialize_analyzers()
    
    def _load_data(self):
        """Load and preprocess data based on type."""
        if self.verbose:
            print("🔄 Loading data...")
        
        # Auto-detect data type if not specified
        if self.data_type is None:
            self.data_type = self._detect_data_type()
        
        # Load based on type
        if self.data_type == 'tabular':
            loader = TabularLoader()
        elif self.data_type == 'timeseries':
            loader = TimeSeriesLoader()
        elif self.data_type == 'text':
            loader = TextLoader()
        elif self.data_type == 'graph':
            loader = GraphLoader()
        else:
            raise ValueError(f"Unknown data type: {self.data_type}")
        
        self.data = loader.load(self.raw_data)
        
        if self.verbose:
            print(f"✅ Loaded {self.data_type} data")
            if hasattr(self.data, 'shape'):
                print(f"   Shape: {self.data.shape}")
    
    def _detect_data_type(self) -> str:
        """Auto-detect data type."""
        if isinstance(self.raw_data, str):
            # File path - check extension
            ext = Path(self.raw_data).suffix.lower()
            if ext in ['.csv', '.xlsx', '.parquet']:
                return 'tabular'
            elif ext in ['.txt', '.json']:
                return 'text'
        elif isinstance(self.raw_data, pd.DataFrame):
            return 'tabular'
        elif isinstance(self.raw_data, dict):
            if 'nodes' in self.raw_data or 'edges' in self.raw_data:
                return 'graph'
        
        return 'tabular'  # Default
    
    def _initialize_analyzers(self):
        """Initialize all analysis engines."""
        self.feature_analyzer = FeaturePatternAnalyzer()
        self.topology_engine = TopologyEngine()
        self.anomaly_detector = UniversalAnomalyDetector()
        self.complexity_calculator = PatternComplexityIndex()
        self.rule_extractor = SymbolicRuleExtractor()
        self.reporter = NaturalLanguageReporter()
        self.dashboard = DashboardGenerator()
    
    def analyze(self, **kwargs) -> Dict[str, Any]:
        """
        Run complete automatic pattern discovery.
        
        Returns
        -------
        dict
            Comprehensive analysis results including:
            - feature_patterns: Important features and interactions
            - topology: Topological structures (loops, holes, clusters)
            - anomalies: Detected anomalies and outliers
            - rules: Extracted symbolic rules
            - complexity: Pattern Complexity Index
            - hypotheses: Generated hypotheses for testing
        """
        if self.verbose:
            print("\n🔍 Starting Automatic Pattern Discovery...\n")
        
        # 1. Feature Pattern Intelligence
        if self.verbose:
            print("1️⃣  Analyzing feature patterns...")
        self.results['feature_patterns'] = self.feature_analyzer.analyze(self.data)
        
        # 2. Topological Analysis
        if self.verbose:
            print("2️⃣  Detecting topological structures...")
        self.results['topology'] = self.topology_engine.analyze(self.data)
        
        # 3. Anomaly Detection
        if self.verbose:
            print("3️⃣  Running universal anomaly detection...")
        self.results['anomalies'] = self.anomaly_detector.detect(self.data)
        
        # 4. Symbolic Rules Extraction
        if self.verbose:
            print("4️⃣  Extracting symbolic rules...")
        self.results['rules'] = self.rule_extractor.extract(
            self.data, 
            self.results['feature_patterns']
        )
        
        # 5. Pattern Complexity Index
        if self.verbose:
            print("5️⃣  Computing Pattern Complexity Index...")
        self.results['complexity'] = self.complexity_calculator.compute(
            self.data,
            self.results['topology'],
            self.results['feature_patterns']
        )
        
        # 6. Hypothesis Generation
        if self.verbose:
            print("6️⃣  Generating hypotheses...")
        self.results['hypotheses'] = self._generate_hypotheses()
        
        if self.verbose:
            print("\n✅ Analysis complete!\n")
        
        return self.results
    
    def _generate_hypotheses(self) -> List[Dict[str, Any]]:
        """Generate testable hypotheses from discovered patterns."""
        hypotheses = []
        
        # From feature patterns
        if 'important_features' in self.results['feature_patterns']:
            for feature in self.results['feature_patterns']['important_features'][:3]:
                hypotheses.append({
                    'type': 'feature_importance',
                    'hypothesis': f"Feature '{feature['name']}' is a key driver of the target variable",
                    'confidence': feature.get('importance', 0),
                    'test_suggestion': f"Run SHAP analysis on {feature['name']}"
                })
        
        # From topology
        if 'clusters' in self.results['topology']:
            n_clusters = self.results['topology']['clusters'].get('n_clusters', 0)
            if n_clusters > 1:
                hypotheses.append({
                    'type': 'segmentation',
                    'hypothesis': f"Data naturally segments into {n_clusters} distinct groups",
                    'confidence': 0.8,
                    'test_suggestion': "Validate clusters using domain knowledge"
                })
        
        # From anomalies
        if 'detected' in self.results['anomalies']:
            n_anomalies = len(self.results['anomalies']['detected'])
            if n_anomalies > 0:
                hypotheses.append({
                    'type': 'anomaly',
                    'hypothesis': f"Found {n_anomalies} potential outliers or errors",
                    'confidence': 0.7,
                    'test_suggestion': "Investigate anomalies for data quality issues or special cases"
                })
        
        return hypotheses
    
    def report(
        self, 
        show_graphs: bool = True,
        save_path: Optional[str] = None,
        format: str = 'html'
    ):
        """
        Generate comprehensive natural language report.
        
        Parameters
        ----------
        show_graphs : bool
            Whether to include visualizations
        save_path : str, optional
            Path to save the report
        format : str
            Report format: 'html', 'pdf', 'markdown'
        """
        if not self.results:
            print("⚠️  No results yet. Run .analyze() first.")
            return
        
        # Generate natural language summary
        report_text = self.reporter.generate(self.results, self.data_type)
        
        if self.verbose:
            print("\n" + "="*70)
            print("📊 PATTERNFORGE ANALYSIS REPORT")
            print("="*70 + "\n")
            print(report_text)
        
        # Generate dashboard if requested
        if show_graphs:
            self.dashboard.create(self.data, self.results, save_path)
        
        # Save report
        if save_path:
            self._save_report(report_text, save_path, format)
    
    def _save_report(self, text: str, path: str, format: str):
        """Save report to file."""
        if format == 'markdown':
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
        elif format == 'html':
            html_content = self._text_to_html(text)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        if self.verbose:
            print(f"\n💾 Report saved to: {path}")
    
    def _text_to_html(self, text: str) -> str:
        """Convert text report to HTML."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>PatternForge Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>PatternForge Analysis Report</h1>
            <pre>{text}</pre>
        </body>
        </html>
        """
        return html
    
    def get_kpi_recommendations(self) -> List[Dict[str, str]]:
        """Get recommended KPIs based on discovered patterns."""
        if not self.results:
            return []
        
        kpis = []
        
        # Based on complexity
        pci = self.results.get('complexity', {}).get('pci', 0)
        if pci > 0.7:
            kpis.append({
                'name': 'Pattern Complexity Index',
                'value': f'{pci:.2f}',
                'insight': 'High complexity - consider dimensionality reduction'
            })
        
        # Based on topology
        if 'loops' in self.results.get('topology', {}):
            n_loops = len(self.results['topology']['loops'])
            if n_loops > 0:
                kpis.append({
                    'name': 'Topological Loops',
                    'value': str(n_loops),
                    'insight': 'Cyclic dependencies detected - investigate relationships'
                })
        
        return kpis
