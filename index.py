from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import g
from flask import jsonify
from flask import Response
from .modules.database import Database
from .modules.user import create_user
import json
import html
import hashlib
import uuid
from functools import wraps

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = "a6cd02e9b1104ac0*c2a02391284cb!0"
DATA_FILE_PATH = 'static/data.json'


def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        g._database = Database()
    return g._database


def get_username():
    if "id" in session:
        return get_db().get_session(session["id"])
    return None


def is_authenticated(session):
    # TODO Next-level : Vérifier la session dans la base de données
    return "id" in session


def is_authorized(username, password):
    if len(username) == 0 or len(password) == 0:
        # Champs vide
        session['error'] = 'Please, fill out all the fields'
        return False
    db = get_db()
    user = db.read_user_username(username)
    if user is None:
        # Nom utilisateur inexistant
        session['error'] = 'Incorrect username or password'
        return False
    hash = hashlib.sha512(str(password + user.salt).encode("utf-8")).hexdigest()
    if user.hash != hash:
        # Mot de passe incorrect
        session['error'] = 'Incorrect password'
        return False        
    return True


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return Response('Could not verify your access level for that URL.\n'
                            'You have to login with proper credentials.', 401,
                            {'WWW-Authenticate': 'Basic realm="Login Required"'})        
        return f(*args, **kwargs)
    return decorated


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Not found', username=get_username()), 404


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.disconnect()


# Initialiser la base de données
@app.before_first_request
def init_database():
    db = get_db()
    file = open(DATA_FILE_PATH, encoding="utf-8")
    data = json.load(file)
    for i, key in enumerate(data):
        db.insert_sujet(i, key, json.dumps(data[key]))
    file.close()


@app.route('/', methods=["GET"])
def index():
    return render_template(
        'index.html', title='Home', username=get_username()), 200


@app.route('/support', methods=["GET"])
def aide():
    return render_template(
        'support.html', title='Support', username=get_username()), 200


@app.route('/about', methods=["GET"])
def a_propos():
    return render_template(
        'about_us.html', title='About', username=get_username()), 200
    

@app.route('/logout')
@authentication_required
def logout():
    id_session = session["id"]
    session.pop('id', None)
    get_db().delete_session(id_session)
    return redirect("/")


# =================================  sign up  ================================

# Retourner le formulaire de création de comptes utilisateur
@app.route('/register', methods=["GET"])
def register_get():
    error = session["error"] and session.pop("error") if "error" in session else None
    return render_template("register.html", title='Sign up', error=error, username=None)


# Valider les données et créer un nouveau compte utilisateur
@app.route('/register', methods=["POST"])
def register_post():
    try: 
        db = get_db()
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if db.read_user_username(username):
            # Nom utilisateur invalide
            session["error"] = "Username already exists. Please enter another one"
            return redirect('/register')
        user = create_user(username, email, password)  # ValueError        
        db.insert_user(user)
    except ValueError as error:
        session["error"] = str(error) 
        return redirect("/register")
    session["message"] = "Account successfully created."
    return redirect("/login")


# =================================  sign in  ================================

# Retourner le formulaire d'authentification
@app.route('/login', methods=["GET"])
def login_get():
    message = session['message'] and session.pop("message") if "message" in session else None
    error = session["error"] and session.pop("error") if "error" in session else None
    return render_template('login.html', title='Login', error=error, message=message, username=get_username()), 200


# Valider les données et créer une nouvelle session
@app.route('/login', methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if is_authorized(username, password):
        # Accès autorisé
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, username)
        session["id"] = id_session
        return redirect("/")
    return redirect('/login')


# ===============================  languages  ================================

# Retourne la page qui contient tous les sujets
@app.route('/languages', methods=["GET"])
def languages():
    sujets = get_db().read_all_sujet()
    sujets_info = [sujet.to_json() for sujet in sujets]
    return render_template(
        'languages.html', sujets=sujets_info, title='Languages',
        username=get_username()), 200


# Retourne l'arbre de progression d'un sujet
@app.route('/languages/<sujet>', methods=["GET"])
def languages_sujet(sujet):
    try:
        sujet = get_db().read_sujet_nom(sujet)  # TypeError
        sous_sujet_nom = request.args.get('sous-sujet')
        if sous_sujet_nom is None or len(sous_sujet_nom) == 0:
            return render_template(
                'arbre_de_progression.html', sujet=sujet.to_json(),
                title='Languages', username=get_username()), 200
        sous_sujet = sujet.get_sous_sujet(sous_sujet_nom)  # ValueError
    except TypeError:
        # Retourner un 404 si le sujet n'existe pas
        err = "Le sujet '" + html.escape(sujet) + "' n'existe pas."
        return render_template(
            "404.html", title="Not found", err=err,
            username=get_username()), 404
    except ValueError as error:
        # Retourner un 404 si le sous-sujet n'existe pas
        return render_template(
            "404.html", title="Not found", err=str(error),
            username=get_username()), 404
    if sous_sujet_nom == "Introduction":
        return render_template("sous_sujet_Python_Introduction.html", title="Languages", username=get_username()), 200
    return render_template(
        'sous_sujet.html', sujet=sujet.to_json()["Nom"], sous_sujet=sous_sujet,
        title='Languages', username=get_username()), 200


# Retourner la premiere question du quiz d'un 'sous_sujet_nom' appartenant a un 'sujet_nom'
@app.route('/languages/quiz/<sujet_nom>', methods=["GET"])
def quiz(sujet_nom):
    sous_sujet_nom = request.args.get('sous-sujet')
    if sous_sujet_nom is None or len(sous_sujet_nom) == 0:
        err = "Le parametre sous-sujet est obligatoire."
        return render_template(
            "404.html", title="Not found", err=err,
            username=get_username()), 404
    try:
        sujet = get_db().read_sujet_nom(sujet_nom)  # TypeError
        sous_sujet_index = sujet.get_sous_sujet_index(
            sous_sujet_nom)  # ValueError
    except TypeError:
        # Retourner un 404 si le sujet n'existe pas
        err = "Le sujet '" + html.escape(sujet) + "' n'existe pas."
        return render_template(
            "404.html", title="Not found", err=err,
            username=get_username()), 404
    except ValueError as error:
        # Retourner un 404 si le sous-sujet n'existe pas
        return render_template(
            "404.html", title="Not found", err=str(error),
            username=get_username()), 404
    quiz = sujet.get_quiz_question(sous_sujet_index, 0)
    return render_template(
        'quiz.html', sujet=sujet_nom, sous_sujet=sous_sujet_nom, question=quiz
        ['Question'], choix=quiz['Choix'], title='Languages',
        username=get_username())


# Retouner la page de resultat de quiz
@app.route('/languages/quiz/resultat', methods=["GET", "POST"])
def quiz_resultat():
    if request.method == "POST":
        # Evaluer les reponses
        evaluer(request.form['data'])
        return redirect('/languages/quiz/resultat')
    if "Resultat" in session:
        # Retourner le resultat du quiz
        sujet = session["Resultat"]["Sujet"]
        sous_sujet = session["Resultat"]["Sous-sujet"]
        total = session["Resultat"]["Total"]
        note = session["Resultat"]["Note"]
        session.pop("Resultat")
        return render_template(
            'resultat.html', sujet=sujet, sous_sujet=sous_sujet, total=total,
            note=note, title='Languages', username=get_username())
    return render_template(
        "404.html", title="Not found", username=get_username()), 404


# ==================================   api  ==================================

# Retourner un quiz
@app.route('/api/quiz', methods=["GET"])
def api_quiz():
    nom_sujet = request.args.get('sujet')
    nom_sous_sujet = request.args.get('sous-sujet')
    numero_raw = request.args.get('numero', type=int)
    try:
        numero = int(numero_raw)  # ValueError
        sujet = get_db().read_sujet_nom(nom_sujet)  # TypeError
        sous_sujet_index = sujet.get_sous_sujet_index(nom_sous_sujet)
        quiz = sujet.get_quiz_question(
            sous_sujet_index, numero)  # KeyError, IndexError
    except ValueError:
        # Retourner une erreur si le numero n'est pas un entier
        err = "Le numero '" + html.escape(numero_raw) + "' n'existe pas."
        return render_template(
            "404.html", title="Not found", err=err, username=get_username()), 404
    except TypeError:
        # Retourner un statut 204 si aucun sujet n'a été trouvé
        return ('', 204)
    except KeyError:
        # Retourner une erreur si le nom du sous-sujet n'existe pas
        err = "Le sujet '" + html.escape(nom_sous_sujet) + "' n'existe pas."
        return render_template(
            "404.html", title="Not found", err=err, username=get_username()), 404
    except IndexError:
        # Retourner une erreur si le numero de la question du quiz n'existe pas
        err = "Le numero '" + str(numero) + "' n'existe pas."
        return render_template(
            "404.html", title="Not found", err=err, username=get_username()), 404
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
