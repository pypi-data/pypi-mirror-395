"""Graph Data Loader."""

import networkx as nx
from typing import Dict, Any


class GraphLoader:
    """Load and preprocess graph data."""
    
    def load(self, data: Dict[str, Any]) -> nx.Graph:
        """Load graph data."""
        if 'nodes' in data and 'edges' in data:
            G = nx.Graph()
            G.add_nodes_from(data['nodes'])
            G.add_edges_from(data['edges'])
            return G
        
        # Assume it's already a networkx graph
        return data
