# =============================
# featurizer.py
# =============================
from graph_builder import GraphBuilder
from descriptors_topology import TopologyDescriptors as TD
from descriptors_chemistry import ChemistryDescriptors as CD
from descriptors_spectral import SpectralDescriptors as SD
import numpy as np
from tqdm import tqdm

# ==============================================
# GraphComplexityDescriptors
# ==============================================
class GraphComplexityDescriptors:
    @staticmethod
    def global_complexity(G, prefix):
        import networkx as nx
        feats = {}
        if G.number_of_nodes() == 0:
            feats[f"{prefix}_n_comp"] = 0
            feats[f"{prefix}_diameter"] = 0
            feats[f"{prefix}_radius"] = 0
            feats[f"{prefix}_core_max"] = 0
            return feats

        comps = list(nx.connected_components(G))
        feats[f"{prefix}_n_comp"] = len(comps)
        largest = G.subgraph(max(comps, key=len))

        try:
            feats[f"{prefix}_diameter"] = nx.diameter(largest)
        except:
            feats[f"{prefix}_diameter"] = 0
        try:
            feats[f"{prefix}_radius"] = nx.radius(largest)
        except:
            feats[f"{prefix}_radius"] = 0

        core = nx.core_number(G)
        feats[f"{prefix}_core_max"] = max(core.values()) if core else 0

        return feats

# ==============================================
# FeatureAssembler (dense matrices)
# ==============================================
class FeatureAssembler:
    def __init__(self):
        self.columns = None

    def to_matrix(self, rows):
        import pandas as pd
        df = pd.DataFrame(rows)
        if self.columns is None:
            self.columns = list(df.columns)
        df = df[self.columns]
        return df.values, self.columns

# ==============================================
# FeatureNormalizer
# ==============================================
class FeatureNormalizer:
    def __init__(self):
        self.mean = None
        self.std = None

    def fit(self, X):
        self.mean = X.mean(axis=0)
        self.std = X.std(axis=0) + 1e-12

    def transform(self, X):
        return (X - self.mean) / self.std

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

# ==============================================
# FeatureBatchProcessor (parallel)
# ==============================================
class FeatureBatchProcessor:
    def __init__(self, extractor, n_jobs=4, batch_size=64):
        self.extractor = extractor
        self.n_jobs = n_jobs
        self.batch_size = batch_size

    def process(self, partition):
        from multiprocessing import Pool
        batches = [partition[i:i+self.batch_size] for i in range(0, len(partition), self.batch_size)]

        rows = []
        with Pool(self.n_jobs) as P:
            for result in tqdm(P.imap(self.extractor._compute_batch, batches), total=len(batches)):
                rows.extend(result)
        return rows


class GraphFeatureExtractor:
    def __init__(self, cutoffs, mu_dict=None):
        """
        cutoffs: list of neighbor distances (Å)
        mu_dict: optional dict {element: mu_value}.
                 If None, the user must call fit_mu(structures) before computing Ef.
        """
        self.builder = GraphBuilder(cutoffs)
        self.cutoffs = cutoffs
        self.mu = mu_dict   # chemical potentials

    # ------------------------------------
    # ENERGY EXTRACTOR
    # ------------------------------------
    def _extract_energy(self, atoms):
        """
        Attempts to extract total energy from atoms.info
        using common ASE/EXTXYZ keys.
        """
        return float(atoms.AtomPositionManager.E)

    def formation_energy(self, dataset):
        unique_labels = None
        reference_potentials = None
        def _fit_mu_lstsq(X: np.ndarray, y: np.ndarray) -> np.ndarray:
            # Columns with zero variance carry no information; keep them but set μ=0.
            col_var = X.var(axis=0)
            informative = col_var > 0.0
            mu = np.zeros(X.shape[1], dtype=float)
            if np.any(informative):
                mu_inf, *_ = np.linalg.lstsq(X[:, informative].astype(float),
                                             y.astype(float),
                                             rcond=None)
                mu[informative] = mu_inf
            return mu

        # Energies
        y = np.asarray(dataset.get_all_energies(), dtype=float)
        y = np.nan_to_num(y, nan=0.0)
        N = y.shape[0]

        # Compositions and species ordering
        X_all, species_order = dataset.get_all_compositions(return_species=True)
        mapping = dataset.get_species_mapping(order="stored")

        # Choose labels
        labels = list(unique_labels) if unique_labels is not None else list(species_order)

        # Build X for the selected labels (missing labels => zero column)
        idx = np.fromiter((mapping.get(lbl, -1) for lbl in labels), dtype=int, count=len(labels))
        valid = (idx >= 0)

        X = np.zeros((N, len(labels)), dtype=float)
        if np.any(valid):
            X[:, valid] = X_all[:, idx[valid]]

        # μ vector
        if reference_potentials is None:
            mu_vec = _fit_mu_lstsq(X, y)
        else:
            mu_vec = np.array([reference_potentials.get(lbl, 0.0) for lbl in labels], dtype=float)

        # Formation energy
        fE = y - X.dot(mu_vec)
        print( np.sum(X, axis=1).shape )
        return fE / np.sum(X, axis=1)

    # ------------------------------------
    # FIT CHEMICAL POTENTIALS FROM DATASET
    # ------------------------------------
    def fit_mu(self, structures, percentile=20):
        """
        Fit chemical potentials from full dataset using low-energy structures.
        Stores result in self.mu.
        """
        from descriptors_chemistry import fit_weighted_chemical_potentials
        self.mu = fit_weighted_chemical_potentials(structures, percentile=percentile)
        return self.mu

    # ------------------------------------
    # COMPUTE FEATURES FOR A SINGLE STRUCTURE
    # ------------------------------------
    def compute(self, partition, subsample:int=None):
        rows = []
        self.Ef = self.formation_energy(partition)

        for i, c in enumerate(tqdm(partition, desc="Computing features")):
            if isinstance(subsample, int) and i > subsample:
                break
            feats = self.compute_features(c)
            feats["id"] = i
            feats["Ef"] = self.Ef[i]

            rows.append(feats)
        return rows


    # ------------------------------------
    # COMPUTE FEATURES FOR MANY STRUCTURES
    # ------------------------------------
    def compute_features(self, container):

        # graph construction
        graphs = self.builder.build(container)
        feats = {}

        # Choose 2.60 Å graph (or first key)
        c0 = sorted(graphs.keys())[0]
        G0 = graphs[c0]
        # self.plot_graph(G0) << DEBUG PLOT

        # multi-cutoff graph descriptors
        for c, G in graphs.items():
            p = f"c{c:.2f}"

            feats.update(TD.degree_stats(G, p))
            feats.update(TD.cycle_stats(G, p))
            feats.update(TD.clustering(G, p))
            feats.update(TD.path_stats(G, p))

            feats.update(CD.edge_fractions(G, p))
            feats.update(CD.edge_distance_stats(G, p))

            feats.update(SD.spectral_invariants(G, p))

        # ------------------------------------
        #  ENERGY + FORMATION ENERGY
        # ------------------------------------
        feats["E"] = self._extract_energy(container)

        return feats

    # ---------------------------
    def _compute_batch(self, batch):
        rows = []
        for c in batch:
            rows.append(self.compute_features(c))
        return rows


    # ---------------------------
    def compute_many_df(self, structures):
        import pandas as pd
        return pd.DataFrame(self.compute(structures))

    def plot_graph(self, G):
        import matplotlib.pyplot as plt
        import networkx as nx

        pos = nx.spring_layout(G)  # automatic layout
        nx.draw(G, pos, node_size=1, width=0.5)
        plt.show()


if __name__ == "__main__":
    from ase.io import read
    import pandas as pd
    from sage_lib.partition.Partition import Partition
    import multiprocessing
    multiprocessing.set_start_method("spawn", force=True)

    # 1. Featurizer
    cutoffs = [2.6, 3.2, 4.8]   # short, medium, long range
    feature_extractor = GraphFeatureExtractor(cutoffs)
    feature_extractor.mu = {'Ni':-1,'V':-1,'Fe':-1,'K':-1,'O':-1,'H':-1,}

    # 2. Load many structures
    p_store = Partition(storage='hybrid', local_root="/Users/dimitry/Documents/Data/EZGA/11-LDH/runs/00/", access='ro')
    #p_store.read_files("/Users/dimitry/Documents/Data/EZGA/11-LDH/runs/00/config_ss.xyz")
    #structures = read("/Users/dimitry/Documents/Data/EZGA/11-LDH/runs/00/config_ss.xyz", index=":10") 

    # 3. Compute features for all
    F = feature_extractor.compute(p_store)   # auto-detects list → returns list of dicts
    '''
    processor = FeatureBatchProcessor(
        extractor=feature_extractor,
        n_jobs=8,       # number of CPU cores
        batch_size=32   # number of structures per batch
    )

    # Compute features in parallel
    F = processor.process(p_store)
    '''


    # 4. Put into DataFrame
    df = pd.DataFrame(F)

    # 5. Save features
    df.to_csv("graph_features.csv", index=False)

    # 6. Train/Test Split
    X = df.drop(columns=["Ef", "id"])
    y = df["Ef"]

    from xgboost import XGBRegressor
    from sklearn.model_selection import train_test_split

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2)

    model = XGBRegressor(
        n_estimators=800,
        learning_rate=0.05,
        max_depth=1,
        subsample=0.8
    )

    model.fit(Xtrain, ytrain)

    # 7. Feature importances
    gain_importances = model.get_booster().get_score(importance_type="gain")
    sorted_importances = sorted(
        gain_importances.items(), key=lambda x: x[1], reverse=True
    )[:20]

    print(sorted_importances)

    # ============================================
    #  FEATURE REDUNDANCY + STABILITY ANALYSIS
    # ============================================
    from feature_reduction import cluster_features_by_correlation, pca_energy, stability_selection

    # Remove "id" if present – it is NOT a physical feature
    if "id" in X.columns:
        X = X.drop(columns=["id"])
        Xtrain = Xtrain.drop(columns=["id"])
        Xtest = Xtest.drop(columns=["id"])

    print("\n=== 1. Feature Clustering (Correlation) ===")
    clusters = cluster_features_by_correlation(Xtrain)
    for cid, feats in clusters.items():
        print(f"Cluster {cid}: {feats}")

    print("\n=== 2. PCA Feature Overlap Analysis ===")
    n_components, cum = pca_energy(Xtrain)
    print(f"Effective descriptor dimension ≈ {n_components} components "
          f"for 95% variance.")

    print("\n=== 3. Stability Selection (ROBUST IMPORTANCE) ===")
    stability = stability_selection(Xtrain, ytrain.values)
    print(stability.sort_values(ascending=False).head(20))

    print("\nTOP STABLE FEATURES:")
    print(stability.sort_values(ascending=False).head(20))


    # ----------------------------------------
    # Evaluation
    # ----------------------------------------
    from model_evaluation import ModelEvaluator

    evaluator = ModelEvaluator(model)
    y_pred = model.predict(Xtest)

    # Metrics
    metrics = evaluator.compute_metrics(ytest, y_pred)
    print("Performance:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    # Plots
    evaluator.plot_parity(ytest, y_pred)
    evaluator.plot_residuals(ytest, y_pred)
    evaluator.plot_feature_importance(X.columns)

    # Signed importance (direction-aware)
    signed_scores = evaluator.signed_permutation_importance(
        model, Xtest.values, ytest.values, X.columns
    )