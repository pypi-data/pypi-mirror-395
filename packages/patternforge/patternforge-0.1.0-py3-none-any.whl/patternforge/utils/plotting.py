"""
Plotting Utilities
==================

Helper functions for visualizations.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Optional


def plot_distribution(data, title: str = "Distribution", 
                     bins: int = 30, ax: Optional[plt.Axes] = None):
    """Plot data distribution."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.hist(data, bins=bins, alpha=0.7, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.grid(alpha=0.3)
    
    return ax


def plot_correlation_matrix(corr_matrix, title: str = "Correlation Matrix",
                           ax: Optional[plt.Axes] = None):
    """Plot correlation matrix as heatmap."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    
    im = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
    
    # Set ticks
    ax.set_xticks(np.arange(len(corr_matrix.columns)))
    ax.set_yticks(np.arange(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
    ax.set_yticklabels(corr_matrix.columns)
    
    # Colorbar
    plt.colorbar(im, ax=ax)
    
    ax.set_title(title)
    
    return ax


def plot_scatter_2d(X, labels=None, title: str = "2D Scatter",
                   ax: Optional[plt.Axes] = None):
    """Plot 2D scatter with optional labels."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    
    if labels is not None:
        unique_labels = np.unique(labels)
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))
        
        for i, label in enumerate(unique_labels):
            mask = labels == label
            ax.scatter(X[mask, 0], X[mask, 1], c=[colors[i]], 
                      label=f'Cluster {label}', alpha=0.6)
        ax.legend()
    else:
        ax.scatter(X[:, 0], X[:, 1], alpha=0.6)
    
    ax.set_title(title)
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    ax.grid(alpha=0.3)
    
    return ax
