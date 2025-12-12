# ===========================
# graph_tester.py
# ===========================
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from ase.neighborlist import NeighborList
from ase.geometry.analysis import Analysis

class GraphTester:
    """
    Generic diagnostic tool to check if the graph construction
    is physically and algorithmically reasonable.
    """

    @staticmethod
    def summary(G):
        """Return basic graph statistics."""
        return {
            "n_nodes": G.number_of_nodes(),
            "n_edges": G.number_of_edges(),
            "density": nx.density(G),
            "connected_components": nx.number_connected_components(G),
            "avg_degree": np.mean([d for _, d in G.degree()]) if G.number_of_nodes() else 0,
        }

    @staticmethod
    def degree_distribution(G):
        """Return histogram of node degrees."""
        deg = [d for _, d in G.degree()]
        hist, bins = np.histogram(deg, bins=np.arange(0, max(deg)+2))
        return hist, bins

    @staticmethod
    def check_edges_against_cutoff(G, atoms, cutoff):
        """
        Verifies whether each graph edge corresponds to a 
        physical neighbor within the cutoff distance.
        """
        wrong_edges = []
        positions = atoms.positions

        for i, j in G.edges():
            d = np.linalg.norm(positions[i] - positions[j])
            if d > cutoff * 1.05:  # 5% tolerance
                wrong_edges.append((i, j, d))

        return wrong_edges

    @staticmethod
    def build_reference_neighbors(atoms, cutoff):
        """ASE-based neighbor list for comparison."""
        cutoffs = [cutoff / 2.0] * len(atoms)
        nl = NeighborList(cutoffs, skin=0.0, self_interaction=False, bothways=True)
        nl.update(atoms)
        pairs = set()
        for i in range(len(atoms)):
            indices, _ = nl.get_neighbors(i)
            for j in indices:
                if i < j:
                    pairs.add((i, j))
        return pairs

    @staticmethod
    def compare_graph_with_reference(G, ref_edges):
        """Check which edges are missing and which are extra."""
        G_edges = set(tuple(sorted(e)) for e in G.edges())

        missing = ref_edges - G_edges
        extra   = G_edges - ref_edges

        return missing, extra

    @staticmethod
    def plot(G, atoms, cutoff):
        """Simple 2D layout graph plot."""
        pos = {i: atoms.positions[i][:2] for i in range(len(atoms))}
        plt.figure(figsize=(6, 6))
        nx.draw(G, pos, node_size=50, with_labels=False)
        plt.title(f"Graph layout (cutoff = {cutoff} Å)")
        plt.show()
