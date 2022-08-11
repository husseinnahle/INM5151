# Projet de session du cours Projet d'analyse et de modélisation (INM5151-E22)

# :clipboard: Prérequis
- Installer une version Python3 de [python.org](https://www.python.org/downloads/)

<br>

# :wrench: Configuration

Installer le paquet `python3-venv` si ce n'est pas déjà fait et créer l'environnement virtuel `INM5151-virtualenv` :

```
# Linux
sudo apt-get install python3-venv
python3 -m venv INM5151-virtualenv
source INM5151-virtualenv/bin/activate

# macOS
python3 -m venv INM5151-virtualenv
source INM5151-virtualenv/bin/activate

# Windows
py -3 -m venv INM5151-virtualenv
INM5151-virtualenv\scripts\activate
```

Installer les dépendances :
```
$ sudo pip install -r requirements.txt
```
<br>

# :rocket: Démarrer l'application flask
```
$ make
```
Une fois l'application lancée, utiliser un fureteur pour accéder à l'application Flask. Utiliser la première adresse IP affichée dans la console. Par exemple : `Running on http://127.0.0.1:5000`
