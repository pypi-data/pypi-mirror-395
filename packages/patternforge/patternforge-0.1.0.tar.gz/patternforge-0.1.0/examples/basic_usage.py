"""
Basic PatternForge Usage Example
=================================

Demonstrates the core functionality of PatternForge:
1. Loading data
2. Running automatic analysis
3. Generating reports
4. Creating visualizations
"""

import pandas as pd
import numpy as np
from patternforge import PatternForge


def generate_sample_data(n_samples=500):
    """Generate synthetic dataset for demonstration."""
    np.random.seed(42)
    
    # Create features with patterns
    data = {
        'feature_1': np.random.randn(n_samples) * 10 + 50,
        'feature_2': np.random.exponential(5, n_samples),
        'feature_3': np.random.uniform(0, 100, n_samples),
    }
    
    # Add correlated feature
    data['feature_4'] = data['feature_1'] * 0.7 + np.random.randn(n_samples) * 5
    
    # Add categorical feature
    data['category'] = np.random.choice(['A', 'B', 'C'], n_samples)
    
    # Add target with pattern
    data['target'] = (
        data['feature_1'] * 0.5 + 
        data['feature_2'] * 0.3 + 
        np.random.randn(n_samples) * 10
    )
    
    # Add some anomalies
    anomaly_indices = np.random.choice(n_samples, size=20, replace=False)
    for idx in anomaly_indices:
        data['feature_1'][idx] *= 3  # Make extreme values
    
    return pd.DataFrame(data)


def main():
    """Run PatternForge demonstration."""
    
    print("=" * 70)
    print("PatternForge Basic Example")
    print("=" * 70)
    print()
    
    # Step 1: Load or generate data
    print("Step 1: Loading data...")
    data = generate_sample_data(n_samples=500)
    print(f"✓ Loaded {len(data)} samples with {len(data.columns)} features")
    print(f"  Columns: {', '.join(data.columns)}")
    print()
    
    # Step 2: Initialize PatternForge
    print("Step 2: Initializing PatternForge...")
    pf = PatternForge()
    print("✓ PatternForge engine ready")
    print()
    
    # Step 3: Run automatic analysis
    print("Step 3: Running automatic pattern discovery...")
    print("  (This may take a few seconds...)")
    results = pf.analyze(data)
    print("✓ Analysis complete!")
    print()
    
    # Step 4: Display key findings
    print("Step 4: Key Findings")
    print("-" * 70)
    
    # Feature patterns
    if 'feature_patterns' in results:
        print("\n🔍 Top Features:")
        importance = results['feature_patterns'].get('importance', [])
        for i, (feat, score) in enumerate(importance[:5], 1):
            print(f"  {i}. {feat}: {score:.3f}")
    
    # Topology
    if 'topology' in results:
        n_clusters = results['topology'].get('clusters', {}).get('n_clusters', 0)
        print(f"\n🌐 Topological Structures:")
        print(f"  • Detected {n_clusters} cluster(s)")
    
    # Anomalies
    if 'anomalies' in results:
        n_anomalies = results['anomalies'].get('consensus_anomalies', {}).get('n_anomalies', 0)
        print(f"\n⚠️  Anomalies:")
        print(f"  • Found {n_anomalies} consensus anomaly(ies)")
    
    # Complexity
    if 'complexity' in results:
        pci = results['complexity'].get('pci', 0)
        interpretation = results['complexity'].get('interpretation', '')
        print(f"\n🧮 Pattern Complexity:")
        print(f"  • PCI: {pci:.3f}")
        print(f"  • {interpretation}")
    
    print()
    
    # Step 5: Generate natural language report
    print("Step 5: Generating natural language report...")
    report = pf.report(format='text')
    print("✓ Report generated!")
    print()
    
    # Display report
    print("=" * 70)
    print("FULL ANALYSIS REPORT")
    print("=" * 70)
    print(report)
    
    # Step 6: Get recommendations
    print("\nStep 6: Getting KPI recommendations...")
    kpis = pf.get_kpi_recommendations(data, domain='general')
    print("✓ Recommended KPIs:")
    for i, kpi in enumerate(kpis[:5], 1):
        print(f"  {i}. {kpi}")
    print()
    
    # Step 7: Save results (optional)
    print("Step 7: Saving results...")
    
    # Save HTML report
    print("  • Saving HTML dashboard...")
    html_report = pf.report(format='html', output_file='patternforge_report.html')
    print("    ✓ Saved to: patternforge_report.html")
    
    print()
    print("=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()
