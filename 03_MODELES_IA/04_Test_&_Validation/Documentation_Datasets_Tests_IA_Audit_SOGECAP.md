
# Documentation des datasets de tests – IA & Audit (SOGECAP)  
## Version 2026 – Conformité IA Act & Gouvernance Modèles

Ce document décrit les 4 jeux de données techniques utilisés pour tester les modèles algorithmiques (XGBoost, SVM, KNN, RandomForest) dans le cadre du dispositif IA & Audit SOGECAP.

Ils permettent de vérifier :
- la robustesse des algorithmes  
- la détection de dérive  
- l’équité (fairness)  
- la résistance aux valeurs extrêmes  
- la cohérence métier via les “personas SOGECAP”  

---

# 1️⃣ Dataset : `tests_dataset_drift.csv`
## Objectif : Détection de dérive (Data Drift & Concept Drift)

Dataset volontairement décalé par rapport au dataset principal :

- Âges entre **75 et 95 ans**  
- Capital assuré entre **200 000 et 600 000**  
- Faible ancienneté de contrat  
- Canaux variés  

### Pourquoi ?
Pour tester si les modèles :
- détectent un changement inhabituel de population,  
- restent cohérents hors distribution,  
- déclenchent une alerte **drift** dans le monitoring.

### Résultats attendus
- Scores XGBoost / RF plus élevés  
- Classes 1 plus fréquentes pour SVM / KNN  
- Activation possible d’un drift flag  

---

# 2️⃣ Dataset : `tests_dataset_fairness.csv`
## Objectif : Tests de biais et équité (Fairness)

Dataset équilibré en trois sous-populations :
- 18–40 ans  
- 40–60 ans  
- 60–90 ans  

### Pourquoi ?
Pour vérifier :
- l’absence de biais par âge ou par canal,  
- la stabilité des scores entre groupes,  
- la conformité IA Act sur l’équité algorithmique.

### Résultats attendus
- Pas d’écart énorme entre groupes (ex. pas > ±15%)  
- Courbes SHAP global similaires par sous-groupe  

---

# 3️⃣ Dataset : `tests_dataset_stress.csv`
## Objectif : Stress Testing (valeurs extrêmes)

Dataset avec valeurs extrêmes :
- âge = 18 ou 90  
- capital = 1 000 ou 1 000 000  
- prime = 0 ou 10 000  
- sinistres = 0 ou 6  

### Pourquoi ?
Pour vérifier :
- la stabilité numérique des modèles  
- l’absence d’erreurs (NaN, crash SVM/KNN)  
- la cohérence sur des situations limites  

### Résultats attendus
- Pas d’erreurs ou NaN  
- Scores extrêmes mais logiques  

---

# 4️⃣ Dataset : `tests_dataset_personas.csv`
## Objectif : Tests métier & audit (Personas SOGECAP)

Dataset contenant 7 profils représentatifs :

| Persona | Description |
|--------|-------------|
| P1 | Jeune faible risque |
| P2 | Senior capital élevé |
| P3 | Profil atypique capital très haut / prime faible |
| P4 | Multi-sinistres |
| P5 | Bord de frontière SVM |
| P6 | Jeune + sinistre isolé |
| P7 | Profil drift extrême (91 ans – 500k capital) |

### Pourquoi ?
Pour :
- la validation métier,  
- l’audit interne,  
- la démonstration de cohérence modèle,  
- la documentation IA Act (comportements attendus).  

### Résultats attendus
- Comportements en ligne avec les règles SOGECAP  
- Pas d’anomalies sur profils attendus  

---

# Résumé global

| Dataset | Objectif | Dossier |
|--------|----------|---------|
| tests_dataset_drift.csv | Drift | Tests_Derive_Donnees_Drift |
| tests_dataset_fairness.csv | Fairness | Tests_Fairness |
| tests_dataset_stress.csv | Stress test | Tests_Fonctionnels |
| tests_dataset_personas.csv | Métier / Audit | Tests_Metier |

---

Ce document est destiné :
- aux équipes Data / Modèle  
- à la Gouvernance IA  
- au Contrôle Interne  
- à l’Audit interne  
- à la conformité IA Act  

Il sert de référence officielle pour comprendre les différents jeux de test et leurs objectifs.
