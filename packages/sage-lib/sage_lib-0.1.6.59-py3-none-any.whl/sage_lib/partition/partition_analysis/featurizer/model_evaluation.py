# =============================
# model_evaluation.py
# =============================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.utils import shuffle


class ModelEvaluator:
    """
    Evaluation utilities for ML regression models (SHAP-free).
    Provides:
        - RMSE, MAE, R2
        - Parity plot
        - Residual analysis
        - XGBoost feature importances
        - Signed permutation importances (direction-aware relevance)
    """

    def __init__(self, model):
        self.model = model

    # -----------------------------------------------
    def compute_metrics(self, y_true, y_pred):
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        return {"RMSE": rmse, "MAE": mae, "R2": r2}

    # -----------------------------------------------
    def plot_parity(self, y_true, y_pred):
        plt.figure(figsize=(6, 6))
        plt.scatter(y_true, y_pred, s=14, alpha=0.6)
        lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
        plt.plot(lims, lims, 'k--')
        plt.xlabel("Ef (true)")
        plt.ylabel("Ef (predicted)")
        plt.title("Parity plot")
        plt.tight_layout()
        plt.show()

    # -----------------------------------------------
    def plot_residuals(self, y_true, y_pred):
        residuals = y_pred - y_true

        plt.figure(figsize=(6, 4))
        plt.hist(residuals, bins=40, alpha=0.7)
        plt.xlabel("Residual = Ef_pred - Ef_true")
        plt.ylabel("Count")
        plt.title("Residual distribution")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.scatter(y_true, residuals, s=12, alpha=0.6)
        plt.axhline(0, color="black", linestyle="--")
        plt.xlabel("Ef (true)")
        plt.ylabel("Residual")
        plt.title("Residuals vs Ef(true)")
        plt.tight_layout()
        plt.show()

    # -----------------------------------------------
    def plot_feature_importance(self, feature_names, top_k=20):
        booster = self.model.get_booster()
        scores = booster.get_score(importance_type="gain")

        items = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        names = [i[0] for i in items]
        values = [i[1] for i in items]

        plt.figure(figsize=(8, 6))
        plt.barh(names[::-1], values[::-1])
        plt.xlabel("Gain importance")
        plt.title(f"Top {top_k} XGBoost features")
        plt.tight_layout()
        plt.show()

    # -----------------------------------------------
    # SIGNED PERMUTATION IMPORTANCE (SHAP-free)
    # -----------------------------------------------
    def signed_permutation_importance(self, model, X, y, feature_names, top_k=20):
        """
        Sign-aware permutation importance.
        Returns a dict: {feature_name: signed_importance}
        """
        baseline = mean_squared_error(y, model.predict(X))

        signed_scores = {}

        for j in range(X.shape[1]):
            Xp = X.copy()
            Xp[:, j] = shuffle(Xp[:, j])  # permute feature j

            perm_err = mean_squared_error(y, model.predict(Xp))
            delta = perm_err - baseline

            # direction sign: from correlation with predictions
            corr = np.corrcoef(X[:, j], model.predict(X))[0, 1]
            sign = np.sign(corr) if not np.isnan(corr) else 0.0

            signed_scores[feature_names[j]] = delta * sign

        # Plot top-k
        items = sorted(signed_scores.items(), key=lambda x: abs(x[1]), reverse=True)[:top_k]
        names = [i[0] for i in items]
        values = [i[1] for i in items]

        plt.figure(figsize=(8, 6))
        plt.barh(names[::-1], values[::-1])
        plt.xlabel("Signed permutation importance")
        plt.title(f"Top {top_k} signed importance features")
        plt.tight_layout()
        plt.show()

        return signed_scores
