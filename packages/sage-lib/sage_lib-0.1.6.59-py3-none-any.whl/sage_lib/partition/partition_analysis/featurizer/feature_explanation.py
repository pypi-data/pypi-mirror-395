import numpy as np
import pandas as pd


def _rank_dict(d):
    """Normalize dictionary values into ranks 0–1."""
    if len(d) == 0:
        return {}
    values = np.array(list(d.values()), dtype=float)
    if values.max() == values.min():
        return {k: 0.0 for k in d}
    norm = (values - values.min()) / (values.max() - values.min())
    return {k: float(v) for k, v in zip(d.keys(), norm)}


def explain_feature_behavior(
    stability_scores,
    gain_importance,
    weight_importance,
    cover_importance,
    permutation_importance,
    interactions,
    clusters_behavior,
    top_k=5,
):
    """
    Produce *fully automatic* and *unbiased* text explanations.
    No physics, no human priors.
    Only describes statistical/structural patterns.

    Inputs:
        stability_scores        dict {feature: stability score}
        gain_importance         dict {feature: xgb gain}
        weight_importance       dict {feature: xgb weight}
        cover_importance        dict {feature: xgb cover}
        permutation_importance  dict {feature: perm importance}
        interactions            pd.Series (Friedman H)
        clusters_behavior       dict {cluster_id: [features]}
    """

    # rank-normalize all signals
    stab_r = _rank_dict(stability_scores)
    gain_r = _rank_dict(gain_importance)
    weight_r = _rank_dict(weight_importance)
    cover_r = _rank_dict(cover_importance)
    perm_r = _rank_dict(permutation_importance)

    # aggregate composite relevance score
    # keeps it *purely statistical*
    all_feats = set(stab_r) | set(gain_r) | set(weight_r) | set(cover_r) | set(perm_r)

    composite = {}
    for f in all_feats:
        composite[f] = (
            0.30 * stab_r.get(f, 0)
            + 0.25 * perm_r.get(f, 0)
            + 0.25 * gain_r.get(f, 0)
            + 0.10 * weight_r.get(f, 0)
            + 0.10 * cover_r.get(f, 0)
        )

    composite = pd.Series(composite).sort_values(ascending=False)

    # find top interacting pairs
    top_inter = interactions.sort_values(ascending=False).head(top_k)

    # build explanation text
    text = []

    text.append("=== AUTOMATIC MODEL-BEHAVIOR SUMMARY ===")

    text.append("\nTop globally influential features (data-driven):")
    for f in composite.head(top_k).index:
        text.append(f" • {f} (score={composite[f]:.3f})")

    text.append("\nMost persistent features across re-trainings (stability):")
    stab_sorted = pd.Series(stability_scores).sort_values(ascending=False)
    for f, v in stab_sorted.head(top_k).items():
        text.append(f" • {f} (stability={v:.2f})")

    text.append("\nFeatures with strongest two-way interaction effects:")
    for pair, val in top_inter.items():
        text.append(f" • {pair} (H={val:.3f})")

    text.append("\nBehaviorally coherent feature groups:")
    for cid, feats in clusters_behavior.items():
        if len(feats) > 1:
            text.append(f" • Group {cid}: {', '.join(feats)}")
        else:
            text.append(f" • Group {cid}: {feats[0]}")

    text.append("\n=== END OF AUTOMATIC SUMMARY ===")

    return "\n".join(text)
