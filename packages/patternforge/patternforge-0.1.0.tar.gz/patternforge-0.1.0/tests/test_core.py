"""
Tests for PatternForge core functionality
"""

import pytest
import pandas as pd
import numpy as np
from patternforge import PatternForge


@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    np.random.seed(42)
    n = 100
    
    data = pd.DataFrame({
        'feature_1': np.random.randn(n) * 10 + 50,
        'feature_2': np.random.exponential(5, n),
        'feature_3': np.random.uniform(0, 100, n),
        'category': np.random.choice(['A', 'B', 'C'], n),
    })
    
    return data


class TestPatternForge:
    """Test PatternForge class."""
    
    def test_initialization(self):
        """Test PatternForge initialization."""
        pf = PatternForge()
        assert pf is not None
    
    def test_analyze(self, sample_data):
        """Test analyze method."""
        pf = PatternForge()
        results = pf.analyze(sample_data)
        
        # Check that results dictionary has expected keys
        assert isinstance(results, dict)
        assert 'feature_patterns' in results
        assert 'topology' in results
        assert 'anomalies' in results
    
    def test_report_text(self, sample_data):
        """Test text report generation."""
        pf = PatternForge()
        pf.analyze(sample_data)
        
        report = pf.report(format='text')
        assert isinstance(report, str)
        assert len(report) > 0
        assert 'PATTERNFORGE' in report
    
    def test_get_kpi_recommendations(self, sample_data):
        """Test KPI recommendations."""
        pf = PatternForge()
        kpis = pf.get_kpi_recommendations(sample_data)
        
        assert isinstance(kpis, list)
        assert len(kpis) > 0


class TestFeaturePatterns:
    """Test feature pattern analysis."""
    
    def test_importance_calculation(self, sample_data):
        """Test feature importance calculation."""
        from patternforge.analysis.feature_patterns import FeaturePatternAnalyzer
        
        analyzer = FeaturePatternAnalyzer()
        results = analyzer.analyze(sample_data)
        
        assert 'importance' in results
        assert len(results['importance']) > 0


class TestTopology:
    """Test topology engine."""
    
    def test_cluster_detection(self, sample_data):
        """Test cluster detection."""
        from patternforge.analysis.topology_engine import TopologyEngine
        
        engine = TopologyEngine()
        results = engine.analyze(sample_data)
        
        assert 'clusters' in results


class TestAnomalyDetection:
    """Test anomaly detection."""
    
    def test_tabular_anomalies(self, sample_data):
        """Test tabular anomaly detection."""
        from patternforge.analysis.anomaly_engine import UniversalAnomalyDetector
        
        detector = UniversalAnomalyDetector(contamination=0.1)
        results = detector.detect(sample_data, data_type='tabular')
        
        assert 'data_type' in results
        assert results['data_type'] == 'tabular'


class TestComplexity:
    """Test complexity metrics."""
    
    def test_pci_calculation(self, sample_data):
        """Test Pattern Complexity Index calculation."""
        from patternforge.analysis.pattern_entropy import PatternComplexityIndex
        
        pci = PatternComplexityIndex()
        results = pci.compute(sample_data)
        
        assert 'pci' in results
        assert 0 <= results['pci'] <= 1


if __name__ == '__main__':
    pytest.main([__file__])
