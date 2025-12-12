import numpy as np
import pandas as pd
from xgboost import plot_importance
import matplotlib.pyplot as plt
from sklearn.inspection import PartialDependenceDisplay, permutation_importance

# ============================================================
# Standard XGBoost importances
# ============================================================
def xgb_importances(model, X, top=20):
    importance_gain = model.get_booster().get_score(importance_type="gain")
    importance_weight = model.get_booster().get_score(importance_type="weight")
    importance_cover = model.get_booster().get_score(importance_type="cover")

    def normalize(d):
        s = sum(d.values())
        return {k: v/s for k, v in d.items()}

    gain = pd.Series(normalize(importance_gain)).sort_values(ascending=False)
    weight = pd.Series(normalize(importance_weight)).sort_values(ascending=False)
    cover = pd.Series(normalize(importance_cover)).sort_values(ascending=False)

    print("\n=== XGBoost Gain Importance ===")
    print(gain.head(top))
    print("\n=== XGBoost Weight Importance ===")
    print(weight.head(top))
    print("\n=== XGBoost Cover Importance ===")
    print(cover.head(top))

    return gain, weight, cover


# ============================================================
# Permutation importance
# ============================================================
def compute_permutation_importance(model, Xtest, ytest):
    print("\n=== Permutation Importance ===")
    imp = permutation_importance(model, Xtest, ytest, n_repeats=10)
    df = pd.DataFrame({
        "feature": Xtest.columns,
        "importance_mean": imp.importances_mean,
        "importance_std": imp.importances_std
    }).sort_values("importance_mean", ascending=False)
    print(df.head(15))
    return df


# ============================================================
# Partial Dependence and ICE curves
# ============================================================
def plot_pdp_ice(model, X, features, n_cols=3):
    n = len(features)
    n_rows = int(np.ceil(n / n_cols))

    fig, ax = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 3*n_rows))

    if n_rows == 1:
        ax = np.array([ax])

    for i, feat in enumerate(features):
        r = i // n_cols
        c = i % n_cols
        PartialDependenceDisplay.from_estimator(
            model, X, [feat], ax=ax[r, c], kind='both', ice_lines_kw={"alpha":0.1}
        )
        ax[r, c].set_title(f"PDP + ICE — {feat}")

    plt.tight_layout()
    plt.show()


# ============================================================
# Feature interaction strengths using XGB's built-in Gain
# ============================================================
# ============================================================
# Global interaction strength using Friedman's H-statistic
# ============================================================
import numpy as np
import pandas as pd
from sklearn.utils import check_array

def partial_dependence(model, X, feature, grid):
    """1D partial dependence for feature."""
    X_temp = X.copy()
    pdp = []

    for val in grid:
        X_temp[feature] = val
        pdp.append(model.predict(X_temp).mean())

    return np.array(pdp)


def partial_dependence_2d(model, X, f1, f2, grid1, grid2):
    """2D partial dependence for interaction computation."""
    X_temp = X.copy()
    pdp = np.zeros((len(grid1), len(grid2)))

    for i, v1 in enumerate(grid1):
        for j, v2 in enumerate(grid2):
            X_temp[f1] = v1
            X_temp[f2] = v2
            pdp[i, j] = model.predict(X_temp).mean()

    return pdp


def compute_interactions(model, X, top_k=20):
    """Computes pairwise Friedman H-statistics for top_k strongest features."""
    # --- FIX: ensure X is a DataFrame ---
    if isinstance(X, np.ndarray):
        raise ValueError("X must be a pandas DataFrame with column names.")
    df = X.copy()  # already a DataFrame
    
    # Select top features with highest importance
    importances = model.feature_importances_
    idx = np.argsort(importances)[::-1][:top_k]
    features = df.columns[idx]

    results = {}

    for i, f1 in enumerate(features):
        for f2 in features[i+1:]:
            x1 = df[f1].dropna()
            x2 = df[f2].dropna()
            grid1 = np.linspace(x1.min(), x1.max(), 20)
            grid2 = np.linspace(x2.min(), x2.max(), 20)

            # Compute PDPs
            pdp1 = partial_dependence(model, df.copy(), f1, grid1)
            pdp2 = partial_dependence(model, df.copy(), f2, grid2)
            pdp12 = partial_dependence_2d(model, df.copy(), f1, f2, grid1, grid2)

            # Friedman H-statistic
            f1_f2 = pdp12 - pdp1[:, None] - pdp2[None, :] + model.predict(df).mean()
            h_num = np.sum((f1_f2)**2)
            h_den = np.sum((pdp12 - model.predict(df).mean())**2)
            h = np.sqrt(h_num / h_den) if h_den > 0 else 0.0

            results[f"{f1} × {f2}"] = h

    return pd.Series(results).sort_values(ascending=False)



# ============================================================
# Interaction heatmap using Friedman's H-statistic output
# ============================================================
import matplotlib.pyplot as plt

def interaction_heatmap_from_H(interactions, n=20):
    """
    interactions: pd.Series from compute_interactions()
                  index format 'featA × featB'
    n: number of top pairs to plot
    """
    # Select top interaction pairs
    top = interactions.head(n)

    if len(top) == 0:
        print("No non-zero interactions to display.")
        return None

    # Extract features appearing in the top interactions
    pairs = [name.split(" × ") for name in top.index]
    feats = sorted(set([p[0] for p in pairs] + [p[1] for p in pairs]))

    # Initialize symmetric matrix
    mat = pd.DataFrame(0.0, index=feats, columns=feats)

    # Fill matrix with interaction values
    for (f1, f2), val in zip(pairs, top.values):
        mat.loc[f1, f2] = val
        mat.loc[f2, f1] = val

    # Plot heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(mat, cmap="viridis", vmin=0, vmax=mat.values.max())
    plt.xticks(range(len(feats)), feats, rotation=90)
    plt.yticks(range(len(feats)), feats)
    plt.colorbar(label="H-statistic (interaction strength)")
    plt.title("Top Feature Interactions (Friedman H-statistic)")
    plt.tight_layout()
    plt.show()

    return mat


# ============================================================
# Heatmap of pairwise interactions
# ============================================================
def interaction_heatmap(model, features, max_features=25):
    inter = model.get_booster().get_score(importance_type="interaction")
    df = pd.DataFrame(0.0, index=features, columns=features)

    for key, val in inter.items():
        f1, f2 = key.split("-")
        if f1 in df.index and f2 in df.columns:
            df.loc[f1, f2] = val
            df.loc[f2, f1] = val

    df = df.loc[features[:max_features], features[:max_features]]

    plt.figure(figsize=(10,8))
    plt.imshow(df, cmap="viridis")
    plt.xticks(range(len(df.columns)), df.columns, rotation=90)
    plt.yticks(range(len(df.index)), df.index)
    plt.colorbar(label="Interaction strength")
    plt.title("Pairwise XGB Feature Interaction Heatmap")
    plt.tight_layout()
    plt.show()

    return df
