# CHAT 2GP
Bienvenue sur Chat 2GP, le chat réalisé par Guillaume Pedrona et Gaétan Pardon.
Créez une nouvelle conversation et discutez avec le modèle d'IA "z-ai/glm-4.5-air:free", grâce à Openrouter !

## Comment faire fonctionner l'application ?

### Variables d'environnement

Dans le dossier ```back```, créez un fichier ```.env``` et initialisez les variables suivantes :    
```SECRET_KEY = "une_phrase_vraiment_secrète"```  
```ALGORITHM = "HS256"```  
```TOKEN_EXPIRE_MINUTES = 30```  
```TOKEN_OPENROUTER = "votre_clé_openrouter"```  

La variable ```SECRET_KEY``` est une clé personnelle, vous pouvez mettre dedans ce que vous voulez. Elle sera utilisée pour la création de votre json web token (JWT).   
La variable ```ALGORITHM``` permet de définir l'algorithme utilisé pour la création du JWT. Vous pouvez laisser ```HS256``` ou en choisir un autre.   
La variable ```TOKEN_EXPIRE_MINUTES``` définit le temps de validité du TOKEN en minutes. Vous pouvez changer la durée.   
La variable ```TOKEN_OPENROUTER``` est à créer sur le site suivant : https://openrouter.ai/.  
  
### Préparation du backend   
  
Dans le dossier ```back```, tapez la commande suivante afin d'installer toutes les dépendances Python requises :   
```pip install -r requirements.txt```  
   
### Préparation du frontend   
  
Dans le dossier ```front```, tapez la commande suivante afin d'installer toutes les dépendances React requises :   
```npm install```  
   
### Lancement de l'application   
  
Dans le dossier ```back```, tapez :   
```./launch.bat```  
L'API réalisée avec FastAPi sera lancée grâce à uvicorn et écoutera sur le port 8000.  

Dans le dossier ```front```, tapez :  
```npm run dev```  
Le site sera accessible sur le port 5173 à l'adresse http://localhost:5173.  

## Les endpoints  

- POST `/register`
- POST `/login`
- GET `/protected-route`
- GET `/history`
- GET `/history/{history_id}`
- POST `/history`
- POST `/history/{history_id}/message`
- DELETE `/history/{history_id}`

## Versions du projet  
  
Branche ```main``` : Chat Bot avec seulement les fonctionnalités de base et celles bonus (liste des conversations, suppression, création, passage d'une conversation à l'autre)  
Branche ```sqlalchemy``` : Tentative de conversion de la BDD avec Sqlalchemy