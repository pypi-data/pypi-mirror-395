
if __name__ == "__main__":
    from ase.io import read
    import pandas as pd
    from sage_lib.partition.Partition import Partition
    import multiprocessing
    from featurizer import GraphFeatureExtractor, FeatureBatchProcessor
    import numpy as np

    multiprocessing.set_start_method("spawn", force=True)

    # 1. Featurizer
    cutoffs = [1.9, 2.2, 4.8]   # short, medium, long range
    feature_extractor = GraphFeatureExtractor(cutoffs)
    feature_extractor.mu = {'Ni':-1,'V':-1,'Fe':-1,'K':-1,'O':-1,'H':-1,}

    # 2. Load many structures
    p_store = Partition(storage='hybrid', local_root="/Users/dimitry/Documents/Data/EZGA/11-LDH/runs/03", access='ro')
    #p_store.read_files("/Users/dimitry/Documents/Data/EZGA/11-LDH/runs/03/config_g100.xyz")
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
    X = df.drop(columns=["Ef", 'E'])
    y = df["Ef"]

    from xgboost import XGBRegressor
    from sklearn.model_selection import train_test_split

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2)

    model = XGBRegressor(
        n_estimators=800,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8
    )

    model.fit(Xtrain, ytrain)

    # ============================================================
    # PIPELINE A: INTERPRETABILITY-FOCUSED FEATURE REDUCTION
    # ============================================================
    from feature_analysis import (
        cluster_features, pick_representatives,
        pca_dimensionality, stability_selection
    )

    # Remove "id" – it is not a physical feature
    if "id" in X.columns:
        X = X.drop(columns=["id"])
        Xtrain = Xtrain.drop(columns=["id"])
        Xtest = Xtest.drop(columns=["id"])

    print("\n=== STEP 1: Clustering redundant features ===")
    from feature_analysis import clean_features

    print("\n=== CLEANING DESCRIPTORS ===")
    Xtrain = clean_features(Xtrain, nan_strategy="median", drop_thresh=0.2)
    Xtest = Xtest[Xtrain.columns]  # keep same columns in test set

    clusters = cluster_features(Xtrain, corr_threshold=0.75)
    for cid, feats in clusters.items():
        print(f"Cluster {cid}: {feats}")

    print("\n=== STEP 2: Selecting cluster representatives ===")
    representatives = pick_representatives(Xtrain, clusters)
    print("Representatives:", representatives)

    # Construct reduced feature matrix
    Xtrain_reduced = Xtrain[representatives]
    Xtest_reduced = Xtest[representatives]

    print(f"Reduced from {Xtrain.shape[1]} → {Xtrain_reduced.shape[1]} features.")

    print("\n=== STEP 3: Re-train model on collapsed feature space ===")
    model_reduced = XGBRegressor(
        n_estimators=600,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    model_reduced.fit(Xtrain_reduced, ytrain)
    y_pred_reduced = model_reduced.predict(Xtest_reduced)

    rmse = np.sqrt(((y_pred_reduced - ytest) ** 2).mean())
    print(f"RMSE after collapsing features: {rmse:.4f} eV")

    print("\n=== STEP 4: PCA dimensionality check (optional) ===")
    d_eff, cum = pca_dimensionality(Xtrain_reduced, 0.95)
    print(f"Effective dimensionality: {d_eff} principal components explain 95% variance.")

    print("\n=== STEP 5: Stability selection in reduced feature space ===")
    stability = stability_selection(Xtrain_reduced, ytrain.values)
    print(stability)

    print("\nTOP STABLE FEATURES:")
    print(stability.head(10))

    from xgb_postanalysis import (
        xgb_importances, compute_permutation_importance,
        plot_pdp_ice, compute_interactions, interaction_heatmap_from_H
    )

    print("\n===========================================================")
    print("      XGBOOST FULL INTERPRETABILITY POST-ANALYSIS")
    print("===========================================================\n")

    # 1. Standard importances
    gain, weight, cover = xgb_importances(model_reduced, Xtrain_reduced)

    gain_importance = gain
    weight_importance = weight
    cover_importance = cover

    # 2. Permutation importance
    perm = compute_permutation_importance(model_reduced, Xtest_reduced, ytest)
    perm_df = perm.copy()   # IMPORTANT FIX

    # 3. Partial dependence + ICE curves for top 6 features
    top_features = gain.head(6).index.tolist()
    plot_pdp_ice(model_reduced, Xtrain_reduced, top_features)

    # 4. Interaction strengths
    interactions = compute_interactions(model_reduced, Xtrain_reduced, top_k=20)
    print(interactions)

    # 5. Interaction heatmap
    interaction_matrix = interaction_heatmap_from_H(interactions, n=20)

    print("\n===========================================================")
    print("      feature_behavior POST-ANALYSIS")
    print("===========================================================\n")

    from feature_analysis import compute_feature_behavior_matrix, cluster_by_model_behavior

    M, f_names = compute_feature_behavior_matrix(
        model_reduced,
        Xtrain_reduced,
        permutation_importance=dict(zip(perm_df["feature"], perm_df["importance_mean"])),
        stability_scores=stability.to_dict(),
        gain_importance=gain_importance.to_dict(),
        cover_importance=cover_importance.to_dict(),
        weight_importance=weight_importance.to_dict(),
        pdp_curves=None   # <-- DISABLED FOR NOW
    )

    clusters_behavior = cluster_by_model_behavior(M, f_names)
    print("\n=== MODEL-BEHAVIOR FEATURE GROUPS ===")
    for cid, feats in clusters_behavior.items():
        print(f"Group {cid}: {feats}")


    print("\n===========================================================")
    print("      feature_explanation POST-ANALYSIS")
    print("===========================================================\n")

    from feature_explanation import explain_feature_behavior

    explanation = explain_feature_behavior(
        stability_scores=stability.to_dict(),
        gain_importance=gain.to_dict(),
        weight_importance=weight.to_dict(),
        cover_importance=cover.to_dict(),
        permutation_importance=dict(zip(perm["feature"], perm["importance_mean"])),
        interactions=interactions,
        clusters_behavior=clusters_behavior,
    )

    print("\n" + explanation)
