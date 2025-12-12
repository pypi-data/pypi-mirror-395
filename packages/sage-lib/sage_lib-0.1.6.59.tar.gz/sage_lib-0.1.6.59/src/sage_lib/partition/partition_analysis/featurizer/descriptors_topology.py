# =============================
# descriptors_topology.py
# =============================

import numpy as np
import networkx as nx
from scipy.stats import skew

class TopologyDescriptors:
    @staticmethod
    def degree_stats(G, prefix):
        deg = np.array([d for _, d in G.degree()], float)
        if len(deg) == 0:
            return {f"{prefix}_deg_mean": 0, f"{prefix}_deg_std": 0, f"{prefix}_deg_skew": 0}

        return {
            f"{prefix}_deg_mean": float(np.mean(deg)),
            f"{prefix}_deg_std": float(np.std(deg)),
            f"{prefix}_deg_skew": float(skew(deg))
        }

    @staticmethod
    def cycle_stats(G, prefix):
        try:
            cycles = nx.cycle_basis(G)
        except Exception:
            cycles = []
        if not cycles:
            return {f"{prefix}_n_cycles": 0, f"{prefix}_cycle_mean": 0}
        lengths = [len(c) for c in cycles]
        return {
            f"{prefix}_n_cycles": len(cycles),
            f"{prefix}_cycle_mean": float(np.mean(lengths))
        }

    @staticmethod
    def clustering(G, prefix):
        if G.number_of_nodes() == 0:
            return {f"{prefix}_clust": 0}
        return {f"{prefix}_clust": nx.average_clustering(G, weight="weight")}

    @staticmethod
    def path_stats(G, prefix):
        if G.number_of_nodes() == 0:
            return {f"{prefix}_path_mean": 0, f"{prefix}_path_std": 0}
        comp = max(nx.connected_components(G), key=len)
        H = G.subgraph(comp)
        if H.number_of_nodes() <= 1:
            return {f"{prefix}_path_mean": 0, f"{prefix}_path_std": 0}
        sp = dict(nx.all_pairs_shortest_path_length(H))
        dist = []
        for i in sp:
            dist += list(sp[i].values())
        dist = np.array(dist, float)
        return {f"{prefix}_path_mean": float(np.mean(dist)), f"{prefix}_path_std": float(np.std(dist))}

