# =============================
# descriptors_chemistry.py
# =============================

import numpy as np
from collections import Counter


# ================================================================
#   LOW-LEVEL CHEMICAL DESCRIPTORS (based on graph + composition)
# ================================================================
class ChemistryDescriptors:

    # -----------------------------
    # Edge-based chemical features
    # -----------------------------
    @staticmethod
    def edge_fractions(G, prefix):
        """
        Returns the fraction of each element–element pair (A-B) in the graph.
        """
        edges = list(G.edges(data=True))
        if not edges:
            return {}

        feats = {}
        pair_count = {}

        for i, j, d in edges:
            a = G.nodes[i]["element"]
            b = G.nodes[j]["element"]
            pair = "-".join(sorted([a, b]))
            pair_count[pair] = pair_count.get(pair, 0) + 1

        total = len(edges)

        for p, c in pair_count.items():
            feats[f"{prefix}_frac_{p}"] = c / total

        return feats

    @staticmethod
    def edge_distance_stats(G, prefix):
        """
        Mean and std of bond lengths in the graph.
        """
        dist = [d["weight"] for _, _, d in G.edges(data=True)]
        if not dist:
            return {
                f"{prefix}_d_mean": 0.0,
                f"{prefix}_d_std": 0.0
            }

        d = np.array(dist)
        return {
            f"{prefix}_d_mean": float(np.mean(d)),
            f"{prefix}_d_std": float(np.std(d)),
        }

    # -----------------------------------------
    # Composition and element-count descriptors
    # -----------------------------------------
    @staticmethod
    def element_counts(atoms):
        """
        Returns a dict {el: count} for the structure.
        """
        symbols = atoms.get_chemical_symbols()
        cnt = Counter(symbols)
        return dict(cnt)

    @staticmethod
    def element_fractions(atoms):
        """
        Returns fractional composition of each element.
        """
        symbols = atoms.get_chemical_symbols()
        cnt = Counter(symbols)
        total = len(symbols)
        return {f"frac_{el}": cnt[el] / total for el in cnt}


# ================================================================
#   AUTOMATIC CHEMICAL POTENTIAL FITTING (µ_el)
# ================================================================
def fit_weighted_chemical_potentials(structures, percentile=20):
    """
    Fits chemical potentials µ_el via weighted least squares using low-energy structures.

    Parameters
    ----------
    structures : list of ASE Atoms
    percentile : int
        The fraction of lowest-energy structures used to fit µ.
        Example: percentile=20 → only the 20% lowest-energy structures.

    Returns
    -------
    mu_dict : dict {element: mu_value}
    """

    energies = []
    compositions = []
    unique_elements = set()

    # --- 1. Extract energy and composition ---
    for atoms in structures:
        info = atoms.info
        if not info:
            raise ValueError("Energy missing (atoms.info is empty).")

        # extract energy from known keys
        E = None
        for key in ("Ef", "E", "energy", "Energy", "dft_energy", "total_energy"):
            if key in info:
                E = float(info[key])
                break

        if E is None:
            raise ValueError("Energy not found in atoms.info.")

        symbols = atoms.get_chemical_symbols()
        cnt = Counter(symbols)
        for el in cnt:
            unique_elements.add(el)

        compositions.append(cnt)
        energies.append(E)

    energies = np.array(energies, float)
    unique_elements = sorted(list(unique_elements))

    # --- 2. Select low-energy subset ---
    cutoff_E = np.percentile(energies, percentile)
    mask = energies <= cutoff_E

    energies_low = energies[mask]
    compositions_low = [compositions[i] for i in range(len(compositions)) if mask[i]]

    # --- 3. Build matrix A (counts) and vector b (energies) ---
    A = []
    for cnt in compositions_low:
        A.append([cnt.get(el, 0) for el in unique_elements])
    A = np.array(A, float)
    b = energies_low

    # --- 4. Weighted least squares (energy weight = inverse deviation) ---
    weights = 1.0 / (1.0 + (b - b.min()))
    W = np.sqrt(weights)

    A_w = A * W[:, None]
    b_w = b * W

    # --- 5. Solve ---
    mu, *_ = np.linalg.lstsq(A_w, b_w, rcond=None)

    return {el: mu[i] for i, el in enumerate(unique_elements)}


# ================================================================
#   FORMATION ENERGY
# ================================================================
def formation_energy(atoms, total_energy, mu_dict):
    """
    Computes formation energy:
        Ef = E_total - sum(mu_el * n_el)
    """
    cnt = Counter(atoms.get_chemical_symbols())
    Ef = total_energy

    for el, n in cnt.items():
        Ef -= mu_dict.get(el, 0.0) * n

    return Ef
