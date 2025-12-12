"""
PatternForge - Universal Automatic Pattern Discovery Engine
============================================================

Author: Idriss Olivier Bado
License: MIT

PatternForge automatically discovers hidden structures, rules, anomalies, 
and mathematical patterns in any dataset using:
- Topological Data Analysis (TDA)
- Information Theory
- Symbolic Regression
- Graph Mining
- Auto-clustering & dimensionality detection
"""

__version__ = "0.1.0"
__author__ = "Idriss Olivier Bado"
__email__ = "idrissbadoolivier@gmail.com"

from patternforge.core import PatternForge
from patternforge.analysis.pattern_entropy import PatternComplexityIndex

__all__ = [
    "PatternForge",
    "PatternComplexityIndex",
]
