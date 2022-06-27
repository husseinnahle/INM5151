from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import g
from flask import jsonify
from flask import Response
from .modules.database import Database
from functools import wraps

import json
import html
import hashlib
import uuid

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
DATA_FILE_PATH = 'static/data.json'
app.secret_key = "a6cd02e9b1104ac0*c2a02391284cb!0"

def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        g._database = Database()
    return g._database


def get_username():
    username = None
    if "id" in session:
        username = get_db().get_session(session["id"])
    return username


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)
    return decorated


def is_authenticated(session):
    # TODO Next-level : Vérifier la session dans la base de données
    return "id" in session


def send_unauthorized():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials.', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


# Evaluer les reponses du quiz et enregistrer le resultat dans une session
def evaluer(raw_data):
    data = json.loads(raw_data)
    sujet_obj = get_db().read_sujet_nom(data["Sujet"])
    sous_sujet_index = sujet_obj.get_sous_sujet_index(data["Sous-sujet"])
    note = 0
    for i, choix in enumerate(data["Reponses"]):  
        reponse = sujet_obj.get_quiz_reponse(sous_sujet_index, i)
        if reponse == choix:
            note += 1
    resultat = {
        "Sujet": data["Sujet"],
        "Sous-sujet": data["Sous-sujet"],
        "Total": len(data["Reponses"]),
        "Note": note
    }
    session["Resultat"] = resultat


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.disconnect()
        

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title="Erreur 404", username=get_username()), 404


# Initialiser la base de données
@app.before_first_request
def init_database():
    db = get_db()
    file = open(DATA_FILE_PATH)
    data = json.load(file)
    for i, key in enumerate(data):
        db.insert_sujet(i, key, json.dumps(data[key]))
    file.close()


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html', title='Accueil', username=get_username()), 200


@app.route('/aide', methods=["GET"])
def aide():
    return render_template(
        'aide.html', title='Aide', username=get_username()), 200


@app.route('/a_propos', methods=["GET"])
def a_propos():
    return render_template(
        'a_propos.html', title='À propos', username=get_username()), 200


@app.route('/connexion', methods=["GET"])
def connexion():
    return render_template(
        'connexion.html', title='Connexion', username=get_username()), 200


# Retourne la page qui contient tous les sujets
@app.route('/langages', methods=["GET"])
def langages():
    sujets = get_db().read_all_sujet()
    sujets_info = [sujet.to_json() for sujet in sujets]
    return render_template('langages.html', sujets=sujets_info), 200


# Retourne l'arbre de progression d'un sujet
@app.route('/langages/<sujet>', methods=["GET"])
def langages_sujet(sujet):
    try:
        sujet = get_db().read_sujet_nom(sujet)  # TypeError
        sous_sujet_nom = request.args.get('sous-sujet')
        if sous_sujet_nom is None or len(sous_sujet_nom) == 0:
            return render_template('arbre_de_progression.html', sujet=sujet.to_json()), 200
        sous_sujet = sujet.get_sous_sujet(sous_sujet_nom)  # ValueError
    except TypeError:
        # Retourner un 404 si le sujet n'existe pas
        err = "Le sujet '" + html.escape(sujet) + "' n'existe pas."
        return render_template("404.html", title="Erreur 404", err=err), 404
    except ValueError as error:
        # Retourner un 404 si le sous-sujet n'existe pas
        return render_template("404.html", title="Erreur 404", err=str(error)), 404
    if sous_sujet_nom == "Introduction":
        return render_template('sous_sujet_Python_Introduction.html'), 200     
    return render_template('sous_sujet.html', sujet=sujet.to_json()["Nom"], sous_sujet=sous_sujet), 200


# Retourner la premiere question du quiz d'un 'sous_sujet_nom' appartenant a un 'sujet_nom'
@app.route('/langages/quiz/<sujet_nom>', methods=["GET"])
def quiz(sujet_nom):
    sous_sujet_nom = request.args.get('sous-sujet')
    if sous_sujet_nom is None or len(sous_sujet_nom) == 0:
        err = "Le parametre sous-sujet est obligatoire."
        return render_template("404.html", title="Erreur 404", err=err), 404 
    try:
        sujet = get_db().read_sujet_nom(sujet_nom)  # TypeError
        sous_sujet_index = sujet.get_sous_sujet_index(sous_sujet_nom)  # ValueError
    except TypeError:
        # Retourner un 404 si le sujet n'existe pas
        err = "Le sujet '" + html.escape(sujet) + "' n'existe pas."
        return render_template("404.html", title="Erreur 404", err=err), 404
    except ValueError as error:
        # Retourner un 404 si le sous-sujet n'existe pas
        return render_template("404.html", title="Erreur 404", err=str(error)), 404
    quiz = sujet.get_quiz_question(sous_sujet_index, 0)
    return render_template('quiz.html', sujet=sujet_nom, sous_sujet=sous_sujet_nom, question=quiz['Question'], choix=quiz['Choix'])


# Retouner la page de resultat de quiz
@app.route('/langages/quiz/resultat', methods=["GET", "POST"])
def quiz_resultat():
    if request.method == "POST":
        # Evaluer les reponses
        evaluer(request.form['data'])
        return redirect('/langages/quiz/resultat')
    if "Resultat" in session:
        # Retourner le resultat du quiz
        sujet = session["Resultat"]["Sujet"]
        sous_sujet = session["Resultat"]["Sous-sujet"]
        total = session["Resultat"]["Total"]
        note = session["Resultat"]["Note"]
        session.pop("Resultat")
        return render_template('resultat.html', sujet=sujet, sous_sujet=sous_sujet, total=total, note=note)
    return render_template("404.html", title="Erreur 404"), 404


# Retourner les donnees d'un quiz
@app.route('/api/quiz', methods=["GET"])
def api_quiz():
    nom_sujet = request.args.get('sujet')
    nom_sous_sujet = request.args.get('sous-sujet')
    numero_raw = request.args.get('numero', type=int)
    try:
        numero = int(numero_raw)  # ValueError
        sujet = get_db().read_sujet_nom(nom_sujet)  # TypeError
        sous_sujet_index = sujet.get_sous_sujet_index(nom_sous_sujet)
        quiz = sujet.get_quiz_question(sous_sujet_index, numero)  # KeyError, IndexError
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
@app.route('/api/sujets', methods=["GET"])
def api_sujets():
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


@app.route('/inscription', methods=["GET", "POST"])
def inscription():
    if request.method == "GET":
        return render_template("inscription.html")
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    # Champs vides
    if username == "" or password == "" or email == "":
        return render_template(
            "inscription.html", error="Tous les champs sont obligatoires.")

    # Validation du formulaire ...
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(
        str(password + salt).encode("utf-8")).hexdigest()
    db = get_db()
    db.create_user(username, email, salt, hashed_password)

    return redirect("/confirm_inscription")


# Confirmation de compte créé
@app.route('/confirm_inscription')
def confirmation_page():
    return render_template('confirm_inscription.html', username=get_username())


@app.route('/login', methods=["POST"])
def log_user():
    username = request.form["username"]
    password = request.form["password"]
    # Vérifier que les champs ne sont pas vides
    if username == "" or password == "":
        # TODO Faire la gestion de l'erreur
        return redirect("/")

    user = get_db().get_user_login_info(username)
    if user is None:
        # TODO Faire la gestion de l'erreur
        return redirect("/")

    salt = user[0]
    hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
    if hashed_password != user[1]:
        # Accès non autorisé
        # TODO Faire la gestion de l'erreur
        return redirect("/")
    
    id_session = uuid.uuid4().hex
    get_db().save_session(id_session, username)
    session["id"] = id_session
    return redirect("/")


@app.route('/logout')
@authentication_required
def logout():
    id_session = session["id"]
    session.pop('id', None)
    get_db().delete_session(id_session)
    return redirect("/")
