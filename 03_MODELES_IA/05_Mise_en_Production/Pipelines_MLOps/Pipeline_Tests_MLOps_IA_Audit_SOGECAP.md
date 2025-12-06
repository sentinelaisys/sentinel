# Pipeline de Tests & MLOps – IA & Audit (SOGECAP)

Objectif : disposer d’un pipeline standardisé permettant de :
- exécuter régulièrement les tests sur les modèles (XGBoost, SVM, KNN, RandomForest),
- surveiller la dérive, la performance, la fairness,
- produire les éléments nécessaires à l’audit et à la conformité IA Act.

---

## 1. Étapes du pipeline (vue globale)

1. **Ingestion des données de test**
   - Source : `03_MODELES_IA/04_Test_&_Validation/Data_Quality/tests_dataset_sogecap.csv`
   - Autres sources possibles : jeux de drift, fairness, stress.

2. **Contrôles Data Quality (pré-modèle)**
   - Vérification des colonnes obligatoires,
   - Contrôle des types, plages de valeurs, valeurs manquantes,
   - Rejet ou correction selon des règles définies.

3. **Préprocessing (feature engineering standardisé)**
   - Encodage des variables catégorielles (OneHotEncoder),
   - Traitement des variables numériques (scaling éventuel),
   - Application du même pipeline que celui utilisé à l’entraînement.

4. **Chargement des modèles en production**
   - Répertoire : `models/`
   - Fichiers : `xgboost_model.joblib`, `svm_model.joblib`, `knn_model.joblib`, `rf_model.joblib`,
   - Chaque modèle est versionné (ex : `xgboost_model_v2026_01.joblib`).

5. **Exécution des modèles**
   - Application des 4 modèles sur le dataset de test,
   - Production d’un fichier de résultats (ex. `results_tests_dataset_sogecap.csv`),
   - Enregistrement des horodatages, versions de modèles, checksum du dataset.

6. **Post-traitement & Analyses**
   - Calcul des métriques globales (AUC, F1, précision, etc. si labels disponibles),
   - Analysis drift (population vs historique),
   - Analyse fairness (écarts par sous-groupes),
   - Génération de rapports PDF/HTML pour audit.

7. **Journalisation & Archivage**
   - Sauvegarde des logs d’exécution,
   - Archivage des résultats, des versions de modèles et de datasets,
   - Mise à jour du registre IA et du registre d’audit.

---

## 2. Schéma de dossiers recommandé

- `03_MODELES_IA/`
  - `01_Jeux_de_Donnees/`
    - `Training/`
    - `Test/`
    - `Validation/`
    - `Synthetic_Data/`
  - `02_Developpement_Modeles/`
  - `03_Explainability/`
  - `04_Test_&_Validation/`
    - `Data_Quality/tests_dataset_sogecap.csv`
    - `Tests_Unitaires/`
    - `Tests_Fonctionnels/`
    - `Tests_Metier/`
    - `Tests_Gouvernance/`
    - `Tests_Derive_Donnees_Drift/`
    - `Tests_Fairness/`
    - `Banque_Tests_SOGECAP/tests_ia_audit_sogecap.md`
  - `05_Mise_en_Production/`
    - `Pipelines_MLOps/`
    - `Documentation_MEP/`
    - `Scripts_Rejeu/`
  - `06_Monitoring/`
    - `Suivi_Performances/`
    - `Suivi_Drift/`
    - `Suivi_Stabilite/`
    - `Suivi_Fairness/`

---

## 3. Intégration CI/CD (exemple générique)

Exemple de logique à intégrer dans un pipeline CI/CD (GitHub Actions, GitLab CI, Jenkins, etc.) :

1. **Étape 1 – Préparation**
   - Récupération du code et des modèles,
   - Installation des dépendances (`pip install -r requirements.txt`).

2. **Étape 2 – Tests unitaires & lint**
   - Exécution des tests Python classiques (pytest),
   - Vérification du style (flake8, black…).

3. **Étape 3 – Exécution du script de tests modèles**
   - Commande : `python run_models_sogecap.py`
   - Entrée : `tests_dataset_sogecap.csv`
   - Sortie : `results_tests_dataset_sogecap.csv`

4. **Étape 4 – Calcul des métriques & Drift**
   - Script dédié (ex : `analyse_results.py`) qui :
     - charge `results_tests_dataset_sogecap.csv`,
     - calcule les métriques,
     - compare aux seuils définis,
     - déclenche une alerte si dépassement (drift, baisse de performance…).

5. **Étape 5 – Génération d’un rapport**
   - Génération d’un rapport (Markdown, HTML ou PDF),
   - Stockage dans `06_Monitoring/`.

6. **Étape 6 – Mise à jour du Registre IA**
   - Mise à jour automatique d’un fichier (CSV/JSON/Excel) dans `01_GOUVERNANCE_&_IA_ACT/Registre_IA/`
     avec : date, version des modèles, résultat des tests, statut (OK / ALERTE).

---

## 4. Lien avec l’Audit & IA Act

- Chaque exécution du pipeline constitue une **preuve d’audit** :
  - données → transformation → modèles → sorties → métriques → décision,
  - tout est journalisé et versionné.
- En cas de contrôle ou d’incident, on peut :
  - rejouer un batch de données,
  - prouver quel modèle était en production,
  - fournir les métriques et explications associées.

---

## 5. Prochaine étape possible

- Ajouter un script `analyse_results.py` pour calculer les métriques et générer les rapports,
- Ajouter un job CRON / scheduler (Airflow, GitHub Actions planifié, etc.) pour exécuter régulièrement le pipeline,
- Connecter ce pipeline au système de monitoring de SOGECAP (tableau de bord, alertes).
