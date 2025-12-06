# Banque de tests IA & Audit -- Modèles XGBoost, SVM, KNN, RandomForest

Contexte : SOGECAP -- Scoring risque souscription

Chaque test contient :\
- **Input** (profil assuré + variables)\
- **Expected Output** (score/classe par modèle)\
- **Explication**\
- **Output théorique pour comparaison**

------------------------------------------------------------------------

## 🔵 TEST 1 --- Profil Jeune & Faible Risque

### Input

-   age: 28\
-   capital_assure: 20_000\
-   prime_annuelle: 300\
-   anciennete_contrat: 0\
-   historique_sinistres: 0\
-   canal: "Agence"

### Expected Output

  -----------------------------------------------------------------------
  Modèle             Expected               Explication
  ------------------ ---------------------- -----------------------------
  XGBoost            Score ≈ **0.12**       Faible capital + faible âge →
                                            faible risque

  SVM                Classe **0** (faible   Profil loin de la frontière
                     risque)                haute

  KNN                Classe **0**           28 ans + sinistres = 0 →
                                            cluster faible risque

  RandomForest       Score ≈ **0.18**       Importance élevée d'âge +
                                            sinistres = 0
  -----------------------------------------------------------------------

### Output théorique (comparaison)

``` json
{
  "XGBoost": 0.12,
  "SVM": 0,
  "KNN": 0,
  "RandomForest": 0.18
}
```

------------------------------------------------------------------------

## 🔵 TEST 2 --- Profil Âgé & Capital Élevé

### Input

-   age: 63\
-   capital_assure: 180_000\
-   prime_annuelle: 2100\
-   anciennete_contrat: 12\
-   historique_sinistres: 1\
-   canal: "Courtier"

### Expected Output

  -----------------------------------------------------------------------
  Modèle             Expected               Explication
  ------------------ ---------------------- -----------------------------
  XGBoost            Score ≈ **0.78**       Âge + capital élevé +
                                            sinistre → très risqué

  SVM                Classe **1**           Proche zone de haute marge

  KNN                Classe **1**           Voisins proches = profils
                                            "haut risque"

  RandomForest       Score ≈ **0.72**       Les arbres réagissent
                                            fortement au capital/sinistre
  -----------------------------------------------------------------------

### Output théorique

``` json
{
  "XGBoost": 0.78,
  "SVM": 1,
  "KNN": 1,
  "RandomForest": 0.72
}
```

------------------------------------------------------------------------

## 🔵 TEST 3 --- Profil Atypique (Revenus faibles vs capital très haut)

### Input

-   age: 41\
-   capital_assure: 300_000\
-   prime_annuelle: 400\
-   anciennete_contrat: 1\
-   historique_sinistres: 0\
-   canal: "Online"

### Expected Output

  -----------------------------------------------------------------------
  Modèle             Expected               Explication
  ------------------ ---------------------- -----------------------------
  XGBoost            Score ≈ **0.65**       Incohérence capital/primes →
                                            suspicion

  SVM                Classe **1**           Contraintes non linéaires →
                                            classé haut risque

  KNN                Classe **1**           Très loin des clusters
                                            typiques → anomalie

  RandomForest       Score ≈ **0.60**       Capital énorme driver
                                            principal du score
  -----------------------------------------------------------------------

### Output théorique

``` json
{
  "XGBoost": 0.65,
  "SVM": 1,
  "KNN": 1,
  "RandomForest": 0.60
}
```

------------------------------------------------------------------------

## 🔵 TEST 4 --- Profil Multi-sinistres

### Input

-   age: 52\
-   capital_assure: 75_000\
-   prime_annuelle: 900\
-   anciennete_contrat: 7\
-   historique_sinistres: 4\
-   canal: "Agence"

### Expected Output

  Modèle         Expected           Explication
  -------------- ------------------ -----------------------------------------
  XGBoost        Score ≈ **0.82**   Le nombre de sinistres domine
  SVM            Classe **1**       Forte non-linéarité du signal sinistres
  KNN            Classe **1**       Très proche des clusters sinistrés
  RandomForest   Score ≈ **0.80**   L'ensemble des arbres convergent

### Output théorique

``` json
{
  "XGBoost": 0.82,
  "SVM": 1,
  "KNN": 1,
  "RandomForest": 0.80
}
```

------------------------------------------------------------------------

## 🔵 TEST 5 --- Profil "Bord de frontière" pour SVM

### Input

-   age: 45\
-   capital_assure: 100_000\
-   prime_annuelle: 1500\
-   anciennete_contrat: 3\
-   historique_sinistres: 0\
-   canal: "Courtier"

### Expected Output

  -----------------------------------------------------------------------
  Modèle             Expected               Explication
  ------------------ ---------------------- -----------------------------
  XGBoost            Score ≈ **0.48**       Ambigu → proche du seuil

  SVM                Classe **0** mais      Très proche de la frontière
                     score marge ≈ **0.02** 

  KNN                Classe **0**           Voisins légèrement plus sûrs

  RandomForest       Score ≈ **0.52**       Certains arbres votent
                                            risque, d'autres non
  -----------------------------------------------------------------------

### Output théorique

``` json
{
  "XGBoost": 0.48,
  "SVM": { "class": 0, "margin": 0.02 },
  "KNN": 0,
  "RandomForest": 0.52
}
```

------------------------------------------------------------------------

## 🔵 TEST 6 --- Profil jeune mais sinistre récent

### Input

-   age: 24\
-   capital_assure: 30_000\
-   prime_annuelle: 350\
-   anciennete_contrat: 2\
-   historique_sinistres: 1\
-   canal: "Online"

### Expected Output

  -----------------------------------------------------------------------
  Modèle             Expected               Explication
  ------------------ ---------------------- -----------------------------
  XGBoost            Score ≈ **0.34**       Impact modéré du sinistre

  SVM                Classe **0**           Pas assez fort pour franchir
                                            la frontière

  KNN                Classe **0**           Voisins : jeunes faibles
                                            risques

  RandomForest       Score ≈ **0.40**       L'arbre "sinistre" pèse, mais
                                            pas dominant
  -----------------------------------------------------------------------

### Output théorique

``` json
{
  "XGBoost": 0.34,
  "SVM": 0,
  "KNN": 0,
  "RandomForest": 0.40
}
```

------------------------------------------------------------------------

## 🔵 TEST 7 --- Profil incohérent (doit être rejeté en Data Quality)

### Input

-   age: 15\
-   capital_assure: 200_000\
-   prime_annuelle: -300\
-   anciennete_contrat: -1\
-   historique_sinistres: -2

### Expected Output

-   **Rejet DataQuality**\
-   Message :
    `"Invalid input: age < 18, prime < 0, anciennete_contrat < 0, sinistres < 0"`

### Output théorique

``` json
{
  "error": true,
  "message": "Invalid input: multiple inconsistencies detected"
}
```

------------------------------------------------------------------------

## 🔵 TEST 8 --- Profil "drift suspect"

Profil normal mais très éloigné statistiquement de la base
d'entraînement.

### Input

-   age: 91\
-   capital_assure: 500_000\
-   prime_annuelle: 600\
-   anciennete_contrat: 1\
-   historique_sinistres: 0

### Expected Output

-   Modèle doit répondre un score haut mais avec **flag drift** activé.

### Output théorique

``` json
{
  "XGBoost": 0.88,
  "RandomForest": 0.85,
  "drift_flag": true
}
```

------------------------------------------------------------------------

# FIN DU FICHIER
