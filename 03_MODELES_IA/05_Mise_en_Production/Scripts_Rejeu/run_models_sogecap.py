"""
Script d’exécution des modèles IA & Audit (SOGECAP)
--------------------------------------------------
Objectif :
  - Charger un dataset CSV (ex : tests_dataset_sogecap.csv)
  - Encoder les variables catégorielles
  - Appliquer 4 modèles : XGBoost, SVM, KNN, RandomForest
  - Sauvegarder les résultats dans un fichier CSV de sortie

Hypothèses :
  - Vous disposez déjà de modèles entraînés, sérialisés
    dans un répertoire `models/` sous forme de fichiers .joblib ou .pkl :
      - models/xgboost_model.joblib
      - models/svm_model.joblib
      - models/knn_model.joblib
      - models/rf_model.joblib

  - Le fichier d’entrée contient au minimum les colonnes :
      age, capital_assure, prime_annuelle, anciennete_contrat,
      historique_sinistres, canal

Dépendances (exemple) :
  pip install pandas scikit-learn joblib xgboost
"""

import pandas as pd
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# ---------------------------------------------------------------------
# Configuration de base
# ---------------------------------------------------------------------

INPUT_CSV = "tests_dataset_sogecap.csv"
OUTPUT_CSV = "results_tests_dataset_sogecap.csv"
MODELS_DIR = Path("models")

MODEL_FILES = {
    "xgboost": MODELS_DIR / "xgboost_model.joblib",
    "svm": MODELS_DIR / "svm_model.joblib",
    "knn": MODELS_DIR / "knn_model.joblib",
    "rf": MODELS_DIR / "rf_model.joblib",
}

FEATURE_COLS_NUM = [
    "age",
    "capital_assure",
    "prime_annuelle",
    "anciennete_contrat",
    "historique_sinistres",
]

FEATURE_COLS_CAT = [
    "canal"
]

# ---------------------------------------------------------------------
# Chargement des données
# ---------------------------------------------------------------------

def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    missing_cols = set(FEATURE_COLS_NUM + FEATURE_COLS_CAT) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Colonnes manquantes dans {csv_path} : {missing_cols}")
    return df

# ---------------------------------------------------------------------
# Préprocesseur commun (OneHotEncoder sur les variables catégorielles)
# ---------------------------------------------------------------------

def build_preprocessor():
    transformers = []

    if FEATURE_COLS_CAT:
        transformers.append(
            ("cat", OneHotEncoder(handle_unknown="ignore"), FEATURE_COLS_CAT)
        )

    # Les variables numériques sont laissées telles quelles,
    # mais on pourrait ajouter un StandardScaler au besoin.
    if FEATURE_COLS_NUM:
        transformers.append(
            ("num", "passthrough", FEATURE_COLS_NUM)
        )

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
    )

    return preprocessor

# ---------------------------------------------------------------------
# Chargement des modèles
# ---------------------------------------------------------------------

def load_models():
    models = {}
    for name, path in MODEL_FILES.items():
        if not path.exists():
            print(f"[WARN] Modèle non trouvé : {path} – il sera ignoré.")
            continue
        models[name] = joblib.load(path)
    if not models:
        raise RuntimeError("Aucun modèle chargé. Vérifiez le répertoire `models/`.")
    return models

# ---------------------------------------------------------------------
# Exécution des modèles
# ---------------------------------------------------------------------

def run_models_on_dataset(df: pd.DataFrame) -> pd.DataFrame:
    preprocessor = build_preprocessor()
    X = df[FEATURE_COLS_CAT + FEATURE_COLS_NUM]

    # On ajuste le préprocesseur (fit) sur le dataset de test
    # (ou idéalement sur les données d’entraînement et on recharge l’objet fit).
    X_transformed = preprocessor.fit_transform(X)

    models = load_models()

    results = df.copy()

    for name, model in models.items():
        print(f"[INFO] Exécution du modèle : {name}")
        # Pour les modèles de classification, on peut choisir
        # de sortir la probabilité de la classe positive si disponible.
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_transformed)[:, 1]
            results[f"{name}_score"] = proba
        else:
            # SVM sans proba, KNN régressif, etc.
            pred = model.predict(X_transformed)
            results[f"{name}_pred"] = pred

    return results

# ---------------------------------------------------------------------
# Point d’entrée principal
# ---------------------------------------------------------------------

def main():
    print("[INFO] Chargement du dataset…")
    df = load_data(INPUT_CSV)

    print("[INFO] Exécution des modèles…")
    results = run_models_on_dataset(df)

    print(f"[INFO] Sauvegarde des résultats dans {OUTPUT_CSV}")
    results.to_csv(OUTPUT_CSV, index=False)

    print("[OK] Terminé.")

if __name__ == "__main__":
    main()
