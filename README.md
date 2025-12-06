# IA & Audit – SOGECAP  
## Framework opérationnel, gouvernance & modèles IA (2026-ready)

Ce dépôt GitHub centralise la **documentation**, les **jeux de données de test**, les **scripts** et les **artefacts de gouvernance** du projet **IA & Audit** pour SOGECAP.

Il complète / remplace l’organisation initiale sur Drive en apportant :
- une meilleure **synchro** entre postes,
- un **versionning fin** (historique, tags, branches),
- une base solide pour les **tests réguliers** des modèles IA.

---

## 🎯 Objectifs du dépôt

- Documenter le **Framework Opérationnel IA & Audit 2026**  
- Structurer la **gouvernance IA** (IA Act, DORA, Solvabilité II)  
- Organiser les **modèles IA** (XGBoost, SVM, KNN, RandomForest) et leurs tests  
- Fournir une base exploitable par :
  - les équipes **Data / Modèle**
  - **l’Audit interne**
  - le **Contrôle interne**
  - la **Conformité IA Act / DORA / Solvabilité II**

---

## 📁 Structure du dépôt (vue d’ensemble)

### Fichiers racine

- `README.md` : ce document
- `arbo.txt` : export texte de l’arborescence complète
- `fonctions_et_attendus.md` : description des algorithmes utilisés et des fonctions attendues
- `tests_ia_audit_sogecap.md` : banque de tests IA (cas explicites + attendus théoriques)

### Dossiers principaux

- `00._ADMINISTRATION_DU_PROJET/`  
  Cahier des charges, note de cadrage, budget, planning, reporting, contrats.

- `01_GOUVERNANCE_&_IA_ACT/`  
  Conformité IA Act, décisions de gouvernance IA, politiques IA, registre IA.

- `02_RISQUES_&_CONTROLE_INTERNE/`  
  Taxonomie des risques, plan de contrôle, incidents IA, actions & remédiations.

- `03_MODELES_IA/`  
  **Cœur technique** : données, modèles, tests, pipelines, monitoring.  
  Voir détail ci-dessous.

- `04_AUDIT_INTERNE_IA/`  
  Missions, programme annuel, rapports d’audit, suivi des recommandations IA.

- `05_DORA/`  
  Conformité DORA, incidents ICT, tests de résilience, PenTests.

- `06_SOLVABILITE_II/`  
  Impacts IA sur provisions, SCR, modèles internes, ORSA.

- `07_COMMUNICATION_&_FORMATION/`  
  Supports de formation internes, communication aux instances, supports de sensibilisation.

- `08_OUTILS_&_RESSOURCES/`  
  Outils annexes, bibliographie, templates, références externes.

- `09_ARCHIVES/`  
  Archives des versions précédentes, documents obsolètes mais conservés.

- `10._DISTRIBUTION_OFFICIELLE/`  
  Dossiers/formats prêts à être transmis à la Direction, au CIG, aux régulateurs, etc.

---

## 🔬 Focus : dossier `03_MODELES_IA/`

Ce dossier regroupe tout ce qui concerne les **modèles IA** et leur exploitation.

### `03_MODELES_IA/01_Jeux_de_Donnees/`

- `Training/`, `Test/`, `Validation/`, `Synthetic_Data/`  
  Jeux de données utilisés pour entraîner et valider les modèles.

### `03_MODELES_IA/02_Developpement_Modeles/`

- `XGBoost/`, `SVM/`, `KNN/`, `RandomForest/`  
  Code, notebooks, specs liés à chaque algorithme.

### `03_MODELES_IA/03_Explainability/`

- `SHAP_Global_SOGECAP/`, `SHAP_Par_Persona/`, `PDP_ICE/`  
  Artefacts d’explicabilité (plots, analyses).

### `03_MODELES_IA/04_Test_&_Validation/`

Contient la **banque de tests IA & Audit** :

- `Data_Quality/`  
  - `tests_dataset_sogecap.csv` : dataset principal de test (2 000 profils SOGECAP).

- `Tests_Derive_Donnees_Drift/`  
  - `tests_dataset_drift.csv` : dataset pour tester la dérive (drift).

- `Tests_Fairness/`  
  - `tests_dataset_fairness.csv` : dataset équilibré pour tester l’équité / biais.

- `Tests_Fonctionnels/`  
  - `tests_dataset_stress.csv` : dataset de stress (valeurs extrêmes).

- `Tests_Metier/`  
  - `tests_dataset_personas.csv` : personas SOGECAP pour validation métier & audit.

- `Banque_Tests_SOGECAP/`  
  - `tests_ia_audit_sogecap.md` : cas de test détaillés + outputs théoriques.

- `Tests_Gouvernance/`  
  - `Matrice_Tests_Algorithmes_IA_Audit_SOGECAP.md` : matrice “tests × algos”.

- `Documentation/`  
  - `Documentation_Datasets_Tests_IA_Audit_SOGECAP.md` : documentation des jeux de test.

### `03_MODELES_IA/05_Mise_en_Production/`

- `Pipelines_MLOps/`  
  - `Pipeline_Tests_MLOps_IA_Audit_SOGECAP.md` : description du pipeline de tests & MLOps.

- `Scripts_Rejeu/`  
  - `run_models_sogecap.py` : script d’exécution des 4 modèles (XGBoost, SVM, KNN, RF) sur les datasets de test.

- `Documentation_MEP/`  
  Documentation des mises en production modèles IA.

### `03_MODELES_IA/06_Monitoring/`

- `Suivi_Performances/`  
- `Suivi_Drift/`  
- `Suivi_Fairness/`  
- `Suivi_Stabilite/`  

Dossiers destinés aux rapports de monitoring récurrents.

---

## ▶️ Exécution des tests modèles (vue rapide)

Une fois les modèles entraînés et sérialisés (ex. `xgboost_model.joblib`, etc.) :

1. Placer les modèles dans un répertoire `models/` (aux côtés du script `run_models_sogecap.py` ou adapter le chemin dans le script).
2. Vérifier la présence des datasets dans `03_MODELES_IA/04_Test_&_Validation/…`.
3. Depuis la racine du repo, exécuter par exemple :

```bash
python 03_MODELES_IA/05_Mise_en_Production/Scripts_Rejeu/run_models_sogecap.py
