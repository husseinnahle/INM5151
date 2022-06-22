import json
import html
from flask import Flask
from flask import render_template
from flask import request
from flask import g
from flask import jsonify
from .modules.database import Database

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
DATA_FILE_PATH = 'static/data.json'


def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.disconnect()


# Initialiser la base de données
@app.before_first_request
def init_database():
    db = get_db()
    file = open(DATA_FILE_PATH)
    data = json.load(file)
    for i, key in enumerate(data):
        db.insert_sujet(i, key, json.dumps(data[key]))
    file.close()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title="Erreur 404"), 404


@app.route('/')
def index():
    return render_template('index.html', title='Accueil'), 200


@app.route("/<name>")
def exercice(name):
    return render_template("exercices.html", content=name)

@app.route('/tutoriels')
def tutoriels():
    return render_template('tutoriels.html', title='Tutoriels'), 200


@app.route('/connexion')
def connexion():
    return render_template('connexion.html', title='Connexion'), 200


@app.route('/aide')
def aide():
    return render_template('aide.html', title='Aide'), 200


@app.route('/a_propos')
def a_propos():
    return render_template('a_propos.html', title='À propos'), 200


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

 
# Retourner un quiz
@app.route('/api/quiz')
def quiz():
    nom_sujet = request.args.get('sujet')
    nom_sous_sujet = request.args.get('sous-sujet')
    numero_raw = request.args.get('numero', type=int)
    try:
        numero = int(numero_raw)  # ValueError
        sujet = get_db().read_sujet_nom(nom_sujet)  # TypeError
        quiz = sujet.get_quiz(nom_sous_sujet, numero)  # KeyError, IndexError
    except ValueError:
        # Retourner une erreur si le numero n'est pas un entier
        err = "Le numero '" + html.escape(numero_raw) + "' n'existe pas."
        return render_template("404.html", title="Erreur 404", err=err), 404
    except TypeError:
        # Retourner un statut 204 si aucun sujet n'a été trouvé
        return ('', 204)
    except KeyError:
        # Retourner une erreur si le nom du sous-sujet n'existe pas
        err = "Le sujet '" + html.escape(nom_sous_sujet) + "' n'existe pas."
        return render_template("404.html", title="Erreur 404", err=err), 404
    except IndexError:
        # Retourner une erreur si le numero de la question du quiz n'existe pas
        err = "Le numero '" + str(numero) + "' n'existe pas."
        return render_template("404.html", title="Erreur 404", err=err), 404
    return jsonify(quiz)


# Retourner les sujets disponibles
@app.route('/api/sujets')
def sujets():
    nom = request.args.get('nom')
    if nom is None or len(nom) == 0:
        # Retourner tous les sujets
        sujets = get_db().read_all_sujet()
        return jsonify({e.get_nom(): e.to_json() for e in sujets}), 200
    # Retourner un sujet selon 'nom'
    try:
        sujet = get_db().read_sujet_nom(nom)
    except TypeError:
        return jsonify("Aucun sujet trouvé."), 204
    return jsonify({sujet.get_nom(): sujet.to_json()}), 200