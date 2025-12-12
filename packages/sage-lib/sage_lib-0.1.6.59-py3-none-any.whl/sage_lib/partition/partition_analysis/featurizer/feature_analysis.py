# =============================
# feature_analysis.py
# =============================
import numpy as np
import pandas as pd

from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error

from xgboost import XGBRegressor


# ============================================================
# 1) Correlation-based clustering of descriptors
# ============================================================
def cluster_features(X: pd.DataFrame, corr_threshold: float = 0.85):
    """
    Groups redundant features using hierarchical clustering on (1 - |corr|).
    Returns dict: {cluster_id: [feature_names]}
    """

    # Compute absolute correlation matrix
    corr = np.abs(X.corr())
    dist = 1 - corr.values  # Distance matrix = 1 - |corr|

    # Correct scikit-learn API for v1.2+
    model = AgglomerativeClustering(
        metric='precomputed',       # replaces deprecated "affinity"
        linkage='average',
        distance_threshold=1 - corr_threshold,
        n_clusters=None
    )

    labels = model.fit_predict(dist)

    clusters = {}
    for i, label in enumerate(labels):
        clusters.setdefault(label, []).append(X.columns[i])

    return clusters


# ============================================================
# 2) Select representative feature per cluster
# ============================================================
def pick_representatives(X: pd.DataFrame, clusters: dict):
    """
    Picks one representative feature per cluster.
    Strategy: feature with highest variance inside cluster.
    """
    representatives = []

    for cid, feats in clusters.items():
        if len(feats) == 1:
            representatives.append(feats[0])
            continue

        # choose feature with highest variance
        variances = X[feats].var().sort_values(ascending=False)
        rep = variances.index[0]
        representatives.append(rep)

    return representatives


# ============================================================
# 3) PCA dimensionality analysis (optional)
# ============================================================
def pca_dimensionality(X: pd.DataFrame, explained_variance=0.95):
    pca = PCA().fit(X)
    cum = np.cumsum(pca.explained_variance_ratio_)
    d = np.searchsorted(cum, explained_variance) + 1
    return d, cum


# ============================================================
# 4) Stability selection on collapsed space
# ============================================================
def stability_selection(
    X: pd.DataFrame,
    y: np.ndarray,
    n_runs: int = 30,
    sample_fraction: float = 0.7,
    random_state: int = 123,
):
    """
    Repeated subsampling + training → counts how often each feature is used.
    """
    N = len(X)
    features = X.columns
    counts = np.zeros(len(features))

    for k in range(n_runs):
        np.random.seed(random_state + k)

        # bootstrap subsample of structures
        idx = np.random.choice(N, int(N * sample_fraction), replace=True)

        Xs = X.iloc[idx]
        ys = y[idx]

        model = XGBRegressor(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=random_state + k
        )
        model.fit(Xs, ys)

        imp = model.get_booster().get_score(importance_type="gain")

        for fname in imp:
            if fname in features:
                counts[X.columns.get_loc(fname)] += 1

    stability = counts / n_runs
    return pd.Series(stability, index=features).sort_values(ascending=False)

# ============================================================
# CLEANING: remove NaNs + constant features
# ============================================================
def clean_features(X: pd.DataFrame, nan_strategy="median", drop_thresh=0.2):
    """
    Cleans descriptor matrix before clustering:
    - Drops features with too many NaNs
    - Replaces remaining NaNs
    - Drops constant (zero-variance) features
    """

    # 1) Drop features with > drop_thresh NaNs (e.g. > 20%)
    nan_frac = X.isna().mean()
    to_drop = nan_frac[nan_frac > drop_thresh].index.tolist()
    if len(to_drop) > 0:
        print(f"Dropping {len(to_drop)} features with too many NaNs.")
        X = X.drop(columns=to_drop)

    # 2) Replace remaining NaNs
    if nan_strategy == "median":
        X = X.fillna(X.median())
    elif nan_strategy == "zero":
        X = X.fillna(0)
    else:
        raise ValueError("Invalid nan_strategy")

    # 3) Drop constant (zero-variance) features
    variances = X.var()
    const = variances[variances == 0].index.tolist()
    if len(const) > 0:
        print(f"Dropping {len(const)} constant features.")
        X = X.drop(columns=const)

    return X



def compute_feature_behavior_matrix(
    model,
    X,
    permutation_importance,
    stability_scores,
    gain_importance,
    cover_importance,
    weight_importance,
    pdp_curves=None
):
    """
    Build a feature-behavior matrix where each row encodes:
    - permutation importance
    - stability selection
    - split statistics
    - PDP shape signature (optional)
    """

    features = X.columns
    n = len(features)

    # Normalize all metrics before concatenation
    def normalize(v):
        v = np.array(v, dtype=float)
        if np.std(v) == 0:
            return v * 0
        return (v - np.mean(v)) / (np.std(v) + 1e-12)

    # Build matrix
    behavior_vectors = []

    for f in features:
        vec = []

        # Permutation importance
        vec.append(permutation_importance.get(f, 0.0))

        # Stability selection
        vec.append(stability_scores.get(f, 0.0))

        # XGBoost split statistics
        vec.append(gain_importance.get(f, 0.0))
        vec.append(cover_importance.get(f, 0.0))
        vec.append(weight_importance.get(f, 0.0))

        # PDP (if provided)
        if pdp_curves is not None and f in pdp_curves:
            vec.extend(normalize(pdp_curves[f]))

        behavior_vectors.append(vec)

    # Convert to matrix
    M = np.array(behavior_vectors)
    M = StandardScaler().fit_transform(M)

    return M, list(features)


def cluster_by_model_behavior(behavior_matrix, feature_names, n_clusters=None):
    """
    Cluster features based on their model-behavior signatures.
    Automatically determines number of clusters if n_clusters=None.
    """

    # Compute pairwise distances
    D = pairwise_distances(behavior_matrix, metric='euclidean')

    # If user wants automatic cluster number → must use distance_threshold
    if n_clusters is None:
        clustering = AgglomerativeClustering(
            metric='euclidean',
            linkage='ward',
            distance_threshold=0.0,  # allow dendrogram splitting
            n_clusters=None          # <-- REQUIRED for automatic mode
        )
    else:
        clustering = AgglomerativeClustering(
            metric='euclidean',
            linkage='ward',
            n_clusters=n_clusters
        )

    labels = clustering.fit_predict(behavior_matrix)

    clusters = {}
    for f, c in zip(feature_names, labels):
        clusters.setdefault(c, []).append(f)

    return clusters
