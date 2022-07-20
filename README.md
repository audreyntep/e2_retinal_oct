# AUTOCCAZ
## IA au service de l'automobile


### Installation des dépendances du projet

pip install requirements.txt

### Lancement de l'api et du website

$ env:FLASK_APP= "main"

$ falsk run

### URL

- website : 'http:localhost:5000/web'

- api : 'http:localhost:5000/'

- prediction avec random forest : 'http:localhost:5000/randomForest'
GET : retourne la liste des catégories pour les variables 'Marque', 'Carburant' et 'Transmission'
POST : prend en paramètre 'brand' (une catégorie de Marque), 'year' (année au format AAAA), 'fuel' (une catégorie de Carburant), 'location' (Code du département) et 'kimometers' (nombre entier) puis retourne une prédiction (nombre entier)


- prediction avec arbre de décision : 'http:localhost:5000/decisionTree'
GET : retourne la liste des catégories pour les variables 'Marque', 'Carburant' et 'Transmission'
POST : prend en paramètre 'year' (année au format AAAA), 'door' (le nombre de porte : 4 ou 5), 'seat' (le nombre de place : 3 ou 4) et 'kimometers' (nombre entier) puis retourne un id de prédiction stocké en BDD (nombre entier)