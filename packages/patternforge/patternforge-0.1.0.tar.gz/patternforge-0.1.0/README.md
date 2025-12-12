# 🔮 PatternForge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)]()

> **Universal Automatic Pattern Discovery Engine**  
> Combining Topological Data Analysis, Information Theory, and Symbolic AI

PatternForge is a zero-configuration pattern discovery engine that automatically detects complex patterns, structures, and anomalies across diverse data types—without requiring manual feature engineering or hyperparameter tuning.

---

## ✨ Key Features

### 🎯 Universal Pattern Discovery
- **Zero Configuration**: Just load your data and discover patterns automatically
- **Multi-Modal**: Works with tabular, time series, text, graph, and mixed data
- **Comprehensive Analysis**: 7 integrated pattern discovery engines

### 🔬 Advanced Techniques

| Capability | Technology | What It Discovers |
|-----------|-----------|-------------------|
| **Topological Structures** | Persistent Homology (TDA) | Loops, holes, clusters, voids |
| **Feature Patterns** | Information Theory | Important features, interactions, dependencies |
| **Anomaly Detection** | Multi-Method Ensemble | Outliers, deviations, structural anomalies |
| **Symbolic Rules** | Decision Trees + Logic | If-then rules, associations, constraints |
| **Complexity Metrics** | Pattern Complexity Index | Unified complexity quantification |
| **Hypothesis Generation** | AI-Powered Inference | Testable scientific hypotheses |
| **Natural Language Reports** | Automated Insights | Human-readable summaries |

---

## 🚀 Quick Start

### Installation

```bash
pip install patternforge
```

### Basic Usage

```python
from patternforge import PatternForge
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Discover patterns (zero configuration!)
pf = PatternForge()
results = pf.analyze(data)

# Get natural language report
report = pf.report(format='text')
print(report)

# Generate visualizations
pf.report(format='html', output_file='dashboard.html')
```

### Example Output

```
================================================================================
PATTERNFORGE ANALYSIS REPORT
================================================================================

📊 DATASET OVERVIEW
----------------------------------------------------------------------
• Samples: 1,000
• Features: 15
  - Numeric: 12
  - Categorical: 3

🔍 FEATURE PATTERNS
----------------------------------------------------------------------
Most Important Features:
  1. revenue: 0.847
  2. engagement_score: 0.692
  3. customer_lifetime_value: 0.581

Key Feature Interactions:
  1. revenue ↔ engagement_score (strength: 0.89)
  2. churn_risk ↔ support_tickets (strength: 0.76)

🌐 TOPOLOGICAL STRUCTURES
----------------------------------------------------------------------
• Detected 4 distinct cluster(s)
• Found 12 cyclic structure(s)
  → Indicates circular relationships in data

⚠️ ANOMALIES
----------------------------------------------------------------------
• 23 consensus anomaly(ies) detected
  (Confirmed by multiple detection methods)

📜 EXTRACTED RULES
----------------------------------------------------------------------
Decision Rules:
  1. IF revenue <= 5000.00 AND support_tickets > 3.50
     THEN churn_risk = HIGH (confidence: 87.3%)

🧮 PATTERN COMPLEXITY
----------------------------------------------------------------------
• Pattern Complexity Index (PCI): 0.642
  → High complexity - Rich patterns with multiple structures

💡 GENERATED HYPOTHESES
----------------------------------------------------------------------
1. Revenue and engagement show strong positive correlation (r=0.89),
   suggesting that increasing engagement may drive revenue growth.

2. Customers with >3 support tickets and revenue <$5K have 87% churn 
   probability—targeted intervention may reduce churn.

🎯 RECOMMENDATIONS
----------------------------------------------------------------------
• Feature interactions detected; use tree-based models or feature engineering
• Investigate 23 detected anomalies for data quality issues
• High complexity detected; consider ensemble models or deep learning
```

---

## 🎨 Advanced Features

### Custom Analysis

```python
# Targeted anomaly detection
anomalies = pf.detect_anomalies(data, contamination=0.05)

# Extract symbolic rules with target
rules = pf.extract_rules(data, target_col='churn')

# Compute complexity metrics
complexity = pf.compute_complexity(data)
print(f"Pattern Complexity Index: {complexity['pci']:.3f}")
```

### Visualization Dashboard

```python
# Generate interactive dashboard
pf.create_dashboard(data, output_file='patterns.html')

# Create specific plots
pf.plot_feature_importance()
pf.plot_topology()
pf.plot_anomalies()
```

### Get KPI Recommendations

```python
# Get data-driven KPI suggestions
kpis = pf.get_kpi_recommendations(data, domain='business')

for kpi in kpis[:5]:
    print(f"• {kpi}")
```

---

## 🧠 Pattern Complexity Index (PCI)

PatternForge introduces the **Pattern Complexity Index**, a unified metric combining:

$$
\text{PCI} = \alpha \cdot H_{\text{norm}} + \beta \cdot T_{\text{norm}} + \gamma \cdot V_{\text{norm}}
$$

Where:
- **H**: Shannon entropy (information content)
- **T**: Topological complexity (homology rank)
- **V**: Statistical variance (spread)

**Interpretation:**
- `PCI < 0.3`: Simple, uniform patterns → Linear models
- `0.3 ≤ PCI < 0.5`: Moderate complexity → Standard ML
- `0.5 ≤ PCI < 0.7`: High complexity → Advanced ML
- `PCI ≥ 0.7`: Very high complexity → Deep learning / ensembles

---

## 📊 Supported Data Types

### Tabular Data
```python
data = pd.read_csv('data.csv')
results = pf.analyze(data)
```

### Time Series
```python
timeseries = pd.read_csv('timeseries.csv', parse_dates=['timestamp'])
results = pf.analyze(timeseries)
```

### Text Data
```python
texts = ["document 1", "document 2", ...]
results = pf.analyze(texts, data_type='text')
```

### Graph/Network Data
```python
import networkx as nx
graph = nx.karate_club_graph()
results = pf.analyze(graph, data_type='graph')
```

---

## 🔬 Core Engines

### 1. Feature Pattern Analyzer
- Mutual information importance
- Pairwise interaction detection  
- Dependency discovery
- Nonlinear relationship identification

### 2. Topology Engine
- Persistent homology computation
- Cluster detection (DBSCAN, K-Means)
- Loop/cycle discovery
- Void/hole identification
- Intrinsic dimensionality estimation

### 3. Universal Anomaly Detector
- **Tabular**: Isolation Forest, Elliptic Envelope, Z-score
- **Time Series**: Moving average, sudden change detection
- **Text**: Length/character anomalies
- **Graph**: Degree anomalies, isolated nodes, bridges

### 4. Symbolic Rules Extractor
- Decision tree rules
- Association rules (co-occurrence)
- Logical constraints (bounds, correlations)

### 5. Pattern Complexity Calculator
- Shannon entropy computation
- Topological complexity scoring
- Variance analysis
- Unified PCI metric

### 6. Hypothesis Generator
- Correlation-based hypotheses
- Causal inference suggestions
- Anomaly explanations
- Pattern-driven insights

### 7. Natural Language Reporter
- Executive summaries
- Detailed findings
- Actionable recommendations
- Export to text/HTML/PDF

---

## 🛠️ Installation Options

### From PyPI (Stable)
```bash
pip install patternforge
```

### From Source (Latest)
```bash
git clone https://github.com/idrissbado/patternforge.git
cd patternforge
pip install -e .
```

### With Optional Dependencies
```bash
# Visualization extras
pip install patternforge[viz]

# Development tools
pip install patternforge[dev]

# Documentation
pip install patternforge[docs]

# All extras
pip install patternforge[viz,dev,docs]
```

---

## 📚 Documentation

- **Quick Start Guide**: [Getting Started](https://patternforge.readthedocs.io/quickstart)
- **API Reference**: [Full API Docs](https://patternforge.readthedocs.io/api)
- **Examples**: [Example Gallery](https://github.com/idrissbado/patternforge/tree/main/examples)
- **Theory**: [Mathematical Background](https://patternforge.readthedocs.io/theory)

---

## 🧪 Examples

### Business Analytics
```python
# Customer churn prediction patterns
customer_data = pd.read_csv('customers.csv')
pf = PatternForge()
results = pf.analyze(customer_data, target='churned')

# Get insights
print(pf.report())
pf.create_dashboard(customer_data, output_file='churn_analysis.html')
```

### Scientific Data
```python
# Experimental measurements
experiments = pd.read_csv('lab_results.csv')
pf = PatternForge()
results = pf.analyze(experiments)

# Extract hypotheses
hypotheses = results['hypotheses']
for h in hypotheses:
    print(f"Hypothesis: {h}")
```

### Anomaly Detection
```python
# Security logs
logs = pd.read_csv('access_logs.csv')
pf = PatternForge()
anomalies = pf.detect_anomalies(logs, contamination=0.01)

print(f"Detected {anomalies['n_anomalies']} suspicious events")
```

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repository
git clone https://github.com/idrissbado/patternforge.git
cd patternforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black src/ tests/
```

---

## 📄 License

PatternForge is released under the [MIT License](LICENSE).

---

## 👤 Author

**Idriss Olivier Bado**  
📧 Email: idrissbadoolivier@gmail.com  
🔗 GitHub: [@idrissbado](https://github.com/idrissbado)

---

## 🌟 Citation

If you use PatternForge in your research, please cite:

```bibtex
@software{bado2024patternforge,
  author = {Bado, Idriss Olivier},
  title = {PatternForge: Universal Automatic Pattern Discovery Engine},
  year = {2024},
  url = {https://github.com/idrissbado/patternforge}
}
```

---

## 🙏 Acknowledgments

PatternForge builds upon excellent open-source libraries:
- **GUDHI** for topological data analysis
- **scikit-learn** for machine learning primitives
- **NetworkX** for graph algorithms
- **pandas** and **NumPy** for data handling

---

## 📈 Roadmap

- [ ] Add GPU acceleration for large datasets
- [ ] Implement online/streaming pattern discovery
- [ ] Add causal inference engine
- [ ] Support for image and video data
- [ ] Interactive web UI
- [ ] Cloud deployment options
- [ ] AutoML integration

---

**Made with ❤️ by Idriss Olivier Bado**
