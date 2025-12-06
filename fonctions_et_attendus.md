
# Fonctions et Attendus – Projet IA & Audit (SOGECAP)
## Version 2026 – Aligné sur la nouvelle arborescence GitHub

Ce document décrit pour chaque **fonction IA** du projet IA & Audit SOGECAP :
- son objectif,
- les algorithmes concernés (XGBoost, SVM, KNN, RandomForest),
- les entrées attendues,
- les sorties attendues,
- les tests associés dans l’arborescence GitHub,
- ce que l’audit ou la gouvernance doit vérifier.

Ce fichier est conçu pour être rangé à la racine du dépôt (`fonctions_et_attendus.md`).

---

# 1️⃣ Fonction : Prédiction / Scoring
## Objectif  
Évaluer un profil assuré et produire un **score de risque** ou une **classe** selon le modèle.

## Algorithmes concernés  
- **XGBoost** (principal)
- **RandomForest**
- **SVM**
- **KNN**

## Entrées (features obligatoires)
| Feature | Description |
|---------|-------------|
| age | Âge de l’assuré |
| capital_assure | Montant du capital assuré |
| prime_annuelle | Prime annuelle du contrat |
| anciennete_contrat | Nombre d’années de contrat |
| historique_sinistres | Nombre de sinistres |
| canal | Courtier / Agence / Online |

## Sorties attendues
- `score` (XGBoost / RF) : probabilité de risque
- `classe` (SVM / KNN) : 0 ou 1
- stabilité des modèles sur plusieurs jeux de test

## Tests associés
- `03_MODELES_IA/04_Test_&_Validation/Data_Quality/tests_dataset_sogecap.csv`
- `03_MODELES_IA/05_Mise_en_Production/Scripts_Rejeu/run_models_sogecap.py`

## Vérifications gouvernance / audit
- version du modèle utilisée
- traçabilité complète (entrée → sortie)
- pas de comportement erratique

---

# 2️⃣ Fonction : Data Quality Checking  
## Objectif  
Garantir que les données reçues sont conformes aux règles SOGECAP avant exécution d’un modèle IA.

## Ce qui est contrôlé
- valeurs manquantes
- types incorrects
- plages interdites (ex : capital < 1000)
- valeurs aberrantes

## Tests associés
- `03_MODELES_IA/04_Test_&_Validation/Data_Quality/tests_dataset_sogecap.csv`

## Attendus
- dataset **accepté** ou **rejeté**
- logs complets

## Vérification gouvernance / audit
- règles de validation documentées
- logs horodatés
- traitement uniforme entre environnements

---

# 3️⃣ Fonction : Tests Métier (Personas)
## Objectif  
Tester les comportements attendus du modèle avec des cas métier typiques (audit & actuariat).

## Dataset
`03_MODELES_IA/04_Test_&_Validation/Tests_Metier/tests_dataset_personas.csv`

## Attendus
- cohérence des scores par persona :
  - jeune faible risque → score faible
  - senior capital élevé → score élevé
  - multi-sinistres → score très élevé
  - profil atypique → score modéré mais documenté

## Vérification audit
- résultats stockés
- comparaison régulière avec une baseline
- justification des écarts

---

# 4️⃣ Fonction : Drift Detection  
## Objectif  
Détecter les dérives dans les données ou le comportement du modèle.

## Dataset
`03_MODELES_IA/04_Test_&_Validation/Tests_Derive_Donnees_Drift/tests_dataset_drift.csv`

## Attendus
- détection automatique d’un drift potentiel
- hausse généralisée des scores XGBoost / RF
- documentation dans `06_Monitoring/Suivi_Drift`

## Vérification audit
- dérives documentées
- actions correctrices éventuelles
- cohérence avec l’historique

---

# 5️⃣ Fonction : Fairness Testing  
## Objectif  
Vérifier l’absence de biais contre un groupe (âge, canal, etc.)

## Dataset
`03_MODELES_IA/04_Test_&_Validation/Tests_Fairness/tests_dataset_fairness.csv`

## Attendus
- scores moyens proches entre groupes
- aucun écart ≥ seuil interne (ex. ±15 %)
- aucune discrimination systémique

## Vérification audit
- justification des écarts
- conformité IA Act sur l’équité

---

# 6️⃣ Fonction : Stress Testing  
## Objectif  
Tester la résistance des modèles à des valeurs extrêmes.

## Dataset
`03_MODELES_IA/04_Test_&_Validation/Tests_Fonctionnels/tests_dataset_stress.csv`

## Attendus
- aucune erreur / NaN
- stabilité des scores même en limites hautes/basses
- logique métier respectée

## Vérification audit
- robustesse du modèle
- documentation des protections en entrée

---

# 7️⃣ Fonction : Explainability  
## Objectif  
Documenter et expliquer les décisions des modèles IA.

## Outils
- SHAP (global + persona)
- PDP / ICE

## Dossiers associés
`03_MODELES_IA/03_Explainability/`

## Attendus
- importance des features documentée
- comportement transparent par persona

## Vérification audit
- explications disponibles
- non-dépendance excessive à une seule variable
- traçabilité IA Act

---

# 8️⃣ Fonction : MLOps & Mise en Production  
## Objectif  
Assurer un pipeline stable et auditable.

## Script clé
`03_MODELES_IA/05_Mise_en_Production/Scripts_Rejeu/run_models_sogecap.py`

## Attendus
- exécution périodique
- logs
- résultats versionnés
- mises à jour du registre IA

---

# 9️⃣ Fonction : Monitoring  
## Objectif  
Surveiller les modèles IA post-déploiement.

## Dossiers associés
- `03_MODELES_IA/06_Monitoring/Suivi_Drift`
- `03_MODELES_IA/06_Monitoring/Suivi_Fairness`
- `03_MODELES_IA/06_Monitoring/Suivi_Performances`
- `03_MODELES_IA/06_Monitoring/Suivi_Stabilite`

## Attendus
- tableaux de bord
- alertes drift / fairness / performance
- archivage automatique

---

# 📌 Résumé général (mapping fonctions → arborescence)

| Fonction | Dossier principal |
|----------|-------------------|
| Scoring & modèles | 03_MODELES_IA/ |
| Data Quality | Data_Quality/ |
| Tests métier | Tests_Metier/ |
| Drift | Tests_Derive_Donnees_Drift/ |
| Fairness | Tests_Fairness/ |
| Stress testing | Tests_Fonctionnels/ |
| Explainability | 03_Explainability/ |
| Pipelines MLOps | 05_Mise_en_Production/ |
| Monitoring | 06_Monitoring/ |

---

Ce document est destiné :
- aux équipes data,
- au contrôle interne,
- à l’audit,
- à la conformité (IA Act, Solvabilité II, DORA),
- au CIG.

Il constitue la référence fonctionnelle et attendus pour l’ensemble du périmètre IA & Audit SOGECAP.
