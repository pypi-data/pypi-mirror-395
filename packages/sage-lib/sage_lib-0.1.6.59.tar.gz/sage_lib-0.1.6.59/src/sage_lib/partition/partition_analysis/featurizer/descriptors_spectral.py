# =============================
# descriptors_spectral.py
# =============================

import numpy as np
import networkx as nx

class SpectralDescriptors:
    @staticmethod
    def spectral_invariants(G, prefix, k=20):
        n = G.number_of_nodes()
        if n == 0:
            return {f"{prefix}_lambda2": 0, f"{prefix}_spectral_entropy": 0}
        L = nx.laplacian_matrix(G).astype(float).todense()
        evals = np.linalg.eigvalsh(L)
        evals = np.sort(np.maximum(evals, 1e-12))
        if len(evals) > k:
            evals = evals[:k]
        lam2 = evals[1] if len(evals) > 1 else 0
        p = evals / np.sum(evals)
        sent = -np.sum(p * np.log(p))
        return {f"{prefix}_lambda2": float(lam2), f"{prefix}_spectral_entropy": float(sent)}

