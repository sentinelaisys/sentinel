# Matrice Tests × Algorithmes – Projet IA & Audit (SOGECAP)

Cette matrice indique pour chaque **type de test** :
- si les modèles doivent être exécutés,
- quels algorithmes sont concernés (XGBoost, SVM, KNN, RandomForest),
- l’objectif principal du test.

## Légende
- ✅ : le modèle est exécuté dans ce type de test
- (✅) : le modèle est exécuté, mais l’analyse porte surtout sur ses sorties (drift, fairness…)
- ❌ : le modèle n’est pas exécuté

| Type de test                            | Exécution algos ? | XGBoost | SVM | KNN | RandomForest | Objectif principal |
|----------------------------------------|-------------------|---------|-----|-----|--------------|--------------------|
| Tests unitaires modèle                 | ✅ Oui            | ✅      | ✅  | ✅  | ✅           | Vérifier que chaque modèle réagit correctement à des inputs simples / extrêmes |
| Tests fonctionnels (prédiction)        | ✅ Oui            | ✅      | ✅  | ✅  | ✅           | Vérifier la cohérence globale des scores / classes avec les règles métier |
| Tests métier (personas SOGECAP)        | ✅ Oui            | ✅      | ✅  | ✅  | ✅           | Confirmer que les profils-types sont scorés comme attendu par les métiers |
| Tests de non-régression                | ✅ Oui            | ✅      | ✅  | ✅  | ✅           | Comparer les versions de modèles dans le temps |
| Tests sur `tests_dataset_sogecap.csv`  | ✅ Oui            | ✅      | ✅  | ✅  | ✅           | Campagne de test large : stabilité, performance, comportements globaux |
| Tests dérive / drift                   | (✅) Oui          | (✅)    | (✅)| (✅)| (✅)         | Détecter les changements de distribution / comportement des scores |
| Tests fairness / biais                 | (✅) Oui          | (✅)    | (✅)| (✅)| (✅)         | Identifier des biais éventuels par sous-populations |
| Explainability (SHAP, PDP, ICE)        | (✅) Oui          | (✅)    | ❌* | ❌*| (✅)         | Produire des explications (surtout XGBoost / RF) |
| Data Quality                           | ❌ Non            | ❌      | ❌  | ❌  | ❌           | Contrôler les données d’entrée avant modèle |
| Gouvernance / IA Act                   | ❌ Non            | ❌      | ❌  | ❌  | ❌           | Versioning, logs, conformité réglementaire |
| Tests de logging / traçabilité         | ❌* (sauf E2E)    | ❌      | ❌  | ❌  | ❌           | Vérifier que chaque appel modèle est journalisé |
| Tests MLOps (pipeline CI/CD)           | ✅ / partiel      | ✅      | ✅  | ✅  | ✅           | Vérifier que les jobs d’exécution modèles tournent correctement |

\* SVM et KNN ne sont en général pas utilisés pour la production d’explications locales type SHAP/PDP dans ce cadre. On privilégie XGBoost et RandomForest.

## Résumé
- Tous les **tests orientés “prédiction / comportement”** → execution des 4 algorithmes.
- Les **tests d’enveloppe (Data Quality, Gouvernance, IA Act)** → ne requièrent pas l’exécution des modèles.
- Les **tests drift / fairness / explainability** utilisent les modèles mais se concentrent sur l’analyse de leurs sorties.
