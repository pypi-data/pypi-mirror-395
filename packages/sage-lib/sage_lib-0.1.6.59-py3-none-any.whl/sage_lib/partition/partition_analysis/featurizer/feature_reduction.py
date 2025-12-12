# =============================
# feature_reduction.py
# =============================
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor


# -------------------------------------------------------
# 1. FEATURE CORRELATION + CLUSTERING
# -------------------------------------------------------
def cluster_features_by_correlation(X: pd.DataFrame, threshold: float = 0.8):
    """
    Groups features that carry redundant information via correlation clustering.
    Returns: {cluster_id: [feature_names]}.
    """
    corr = np.abs(X.corr().values)
    dist = 1 - corr

    model = AgglomerativeClustering(
        affinity='precomputed',
        linkage='average',
        distance_threshold=1 - threshold,
        n_clusters=None
    )
    labels = model.fit_predict(dist)

    clusters = {}
    for i, label in enumerate(labels):
        clusters.setdefault(label, []).append(X.columns[i])
    return clusters


# -------------------------------------------------------
# 2. PCA REDUCTION (OPTIONAL)
# -------------------------------------------------------
def pca_energy(X: pd.DataFrame, explained_variance_target=0.95):
    """
    Computes how many principal components retain most of the descriptor variance.
    Helps detect descriptor overcompleteness.
    """
    pca = PCA().fit(X)
    cum = np.cumsum(pca.explained_variance_ratio_)
    d = np.searchsorted(cum, explained_variance_target) + 1
    return d, cum


# -------------------------------------------------------
# 3. STABILITY SELECTION (THE KEY!)
# -------------------------------------------------------
def stability_selection(
    X: pd.DataFrame,
    y: np.ndarray,
    n_runs: int = 40,
    feature_subsample: float = 0.7,
    sample_subsample: float = 0.7,
):
    """
    Repeated subsampling of features + data.
    Counts how often each feature is discovered as important.
    Returns stability score per feature.
    """
    F = X.shape[1]
    N = len(X)
    counts = np.zeros(F)

    for seed in range(n_runs):
        # Random feature subset
        feat_idx = np.random.choice(F, int(F * feature_subsample), replace=False)
        feat_names = X.columns[feat_idx]

        # Random sample subset
        samp_idx = np.random.choice(N, int(N * sample_subsample), replace=True)

        Xs = X.iloc[samp_idx][feat_names]
        ys = y[samp_idx]

        model = XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=seed,
        )
        model.fit(Xs, ys)

        # Feature importance for this run
        imp = model.get_booster().get_score(importance_type="gain")

        for k in imp.keys():
            if k in feat_names:
                counts[X.columns.get_loc(k)] += 1

    stability = counts / n_runs
    return pd.Series(stability, index=X.columns)
