import json
import html
import hashlib
import os
import stripe

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
from .modules.user import modify_user
from .modules.user import validate_support_form
from functools import wraps
from flask_hcaptcha import hCaptcha
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = "a6cd02e9b1104ac0*c2a02391284cb!0"

stripe_keys = {
    "secret_key" : "sk_test_51LKsa0A5hdrVdRtKeyX3nEfmneDW2AcxnXF3KToFivuuttwyNih5Mqyd7RL562hu8BuHfgdI3wpf9ZZBAI6kiJRw006N97T3JI",
    "publishable_key": "pk_test_51LKsa0A5hdrVdRtKZhTWSDWZ7a49RgwH58gOCJ9uTWs1VKvaNLaHGv2hTA2KIL29hloRYZwpfGlMzxHSYgAvSMdH00vr5bZ3rk"
}
stripe.api_key = stripe_keys["secret_key"]

DATA_FILE_PATH = 'static/data.json'

app.config['HCAPTCHA_ENABLED'] = True
app.config['HCAPTCHA_SITE_KEY'] = "3c18dd0a-63ab-4e65-bf31-18704c39f732"
app.config['HCAPTCHA_SECRET_KEY'] = "0x58956B96080BFdBA80d7B228B4c460e3F7C"\
                                    "fDEFC"
HCAPTCHA_ERROR = 'Error in hCaptcha. Please try again'
hcaptcha = hCaptcha(app)
mail = Mail(app)


def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        g._database = Database()
    return g._database


def is_authenticated():
    return ("user" in session and
            get_db().read_user_username(session["user"]["name"]))


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated():
            return Response('Could not verify your access level for that URL.'
                            '\nYou have to login with proper credentials.',
                            401, {'WWW-Authenticate': 'Basic realm="Login"\
                                "Required"'})
        return f(*args, **kwargs)
    return decorated


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Not found'), 404


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.disconnect()


# Initialiser la base de données
@app.before_first_request
def init_database():
    if 'user' in session:
        session.pop("user")
    db = get_db()
    file = open(DATA_FILE_PATH, encoding="utf-8")
    data = json.load(file)
    for i, key in enumerate(data):
        db.insert_sujet(i, key, json.dumps(data[key]))
    file.close()
    # Temporaire pour tester
    progress = {
        "Python": {"Introduction": "S"},
        "Ruby": {"Introduction": "S"},
        "Java": {"Introduction": "S"},
        "Bash": {"Introduction": "S"},
        "C": {"Introduction": "S"},
        "Javascript": {"Introduction": "S"},
        "PHP": {"Introduction": "S"},
        "HTML": {"Introduction": "S"},
        "Go": {"Introduction": "S"},
        "C++": {"Introduction": "S"},
        "Swift": {"Introduction": "S"},
        "C#": {"Introduction": "S"},
        "Lua": {"Introduction": "S"}
    }
    user = create_user("username", "username@hotmail.com", "password")
    user.set_progress(progress)
    get_db().insert_user(user)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html', title='Home'), 200


@app.route('/support', methods=["GET"])
def support_get():
    message = session['message'] and session.pop(
        "message") if "message" in session else None
    error = session["error"] and session.pop(
        "error") if "error" in session else None
    return render_template('support.html', title='Support', error=error,
                           message=message), 200


@app.route('/support', methods=["POST"])
def support_post():
    message = request.form["message"]
    if is_authenticated():
        name = session["user"]["name"]
        email = session["user"]["email"]
    else:
        name = request.form["name"]
        email = request.form["email"]
    if hcaptcha.verify():
        # hCaptcha ok
        try:
            validate_support_form(name, email, message)
            send_message(name, email, message)
            session["message"] = "Message sent successfully."
        except Exception as error:
            session["error"] = str(error)
        return redirect("/support")
    else:
        # hCaptcha erreur
        session['error'] = HCAPTCHA_ERROR
        return redirect('/support')


def send_message(name, email, message):
    sender = "support_form@ezcoding.com"
    user = name + "<" + email + ">"
    emails = [user, "support@ezcoding.com"]
    subject = []
    subject.append("Your message from EZCoding support form")
    subject.append("Support form - " + user)
    for i in range(2):
        mssg = Message(subject=subject[i],
                       sender=sender,
                       recipients=[emails[i]])
        mssg.body = message
        mail.send(mssg)


@app.route('/about', methods=["GET"])
def a_propos():
    return render_template('about_us.html', title='About'), 200


@app.route('/account', methods=["GET"])
@authentication_required
def compte():
    sujets = get_db().read_all_sujet()
    langages = []
    for sujet in sujets:
        if sujet.get_nom() in session['user']['progress']:
            langages.append(
                {"name": sujet.get_nom(), "logo": sujet.get_logo()})
    return render_template('compte.html', title='My account',
                           langages=langages), 200


# ================================  register  ================================

# Retourner le formulaire de création de comptes utilisateur
@app.route('/register', methods=["GET"])
def register_get():
    if is_authenticated():
        return render_template("404.html", title="Not found"), 404
    error = session["error"] and session.pop(
        "error") if "error" in session else None
    return render_template("register.html", title='Sign up', error=error)


   # ================================  paiement  ================================

# Permettre a un utilisateur de devenir membre

@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

    
@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:        
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": "Membership",
                    "quantity": 1,
                    "currency": "cad",
                    "amount": "1000",
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")

@app.route("/paiement")
def paiement():
    return render_template("paiement.html")




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
            session["error"] = "Username already exists. Please enter"\
                " another one"
            return redirect('/register')
        if hcaptcha.verify():
            # hCaptcha ok
            user = create_user(username, email, password)  # ValueError
            db.insert_user(user)
            session["message"] = "Account created!"
            return redirect("/login")
        else:
            # hCaptcha erreur
            session['error'] = HCAPTCHA_ERROR
            return redirect('/register')
    except ValueError as error:
        session["error"] = str(error)
        return redirect("/register")


# ==================================  login  =================================

# Retourner le formulaire d'authentification
@app.route('/login', methods=["GET"])
def login_get():
    message = session['message'] and session.pop(
        "message") if "message" in session else None
    error = session["error"] and session.pop(
        "error") if "error" in session else None
    return render_template('login.html', title='Login',
                           error=error, message=message), 200


# Valider les données et créer une nouvelle session
@app.route('/login', methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    session['error'] = ""

    if hcaptcha.verify():
        user = is_authorized(username, password)
        if not user:
            # Accès non autorisé
            return redirect('/login')
        # hCaptcha ok
        session["user"] = user.session()
        if 'path' in session:
            # Redirection vers 'path' apres authentification
            path = session['path'] and session.pop(
                'path') if 'path' in session else None
            return redirect(path)
        return redirect("/account")
    else:
        # hCaptcha erreur
        session['error'] = HCAPTCHA_ERROR
        return redirect('/login')


def is_authorized(username, password):
    if len(username) == 0 or len(password) == 0:
        # Champs vide
        session['error'] = 'Please, fill out all the fields'
        return None
    db = get_db()
    user = db.read_user_username(username)
    if user is None:
        # Nom utilisateur inexistant
        session['error'] = 'Incorrect username or password'
        return None
    hash = hashlib.sha512(str(password + user.salt)
                          .encode("utf-8")).hexdigest()
    if user.hash != hash:
        # Mot de passe incorrect
        session['error'] = 'Incorrect password'
        return None
    return user


# =================================  logout  =================================

@app.route('/logout')
@authentication_required
def logout():
    session.pop('user')
    return redirect("/")


# ===============================  languages  ================================

# Retourne la page qui contient tous les sujets
@app.route('/languages', methods=["GET"])
def languages():
    sujets = get_db().read_all_sujet()
    sujets_info = [sujet.to_json() for sujet in sujets]
    return render_template('languages.html', sujets=sujets_info,
                           title='Languages'), 200


# Retourne l'arbre de progression d'un sujet
@app.route('/languages/<sujet>', methods=["GET"])
def languages_sujet(sujet):
    try:
        sujet = get_db().read_sujet_nom(sujet)  # TypeError
        sous_sujet_nom = request.args.get('sous-sujet')
        if sous_sujet_nom is None or len(sous_sujet_nom) == 0:
            return render_template('arbre_de_progression.html',
                                   sujet=sujet.to_json(), title='Languages',
                                   is_authorized=is_authenticated()), 200
        sous_sujet = sujet.get_sous_sujet(sous_sujet_nom)  # ValueError
    except TypeError:
        # Retourner un 404 si le sujet n'existe pas
        err = "Le sujet '" + html.escape(sujet) + "' n'existe pas."
        return render_template("404.html", title="Not found", err=err), 404
    except ValueError as error:
        # Retourner un 404 si le sous-sujet n'existe pas
        return render_template("404.html", title="Not found",
                               err=str(error)), 404
    if not is_authenticated():
        # Retourner une erreur si l'utilisateur n'est pas authentifie
        return render_template("404.html", title="Not found"), 404
    if sous_sujet_nom == "Introduction":
        return render_template("python/introduction.html",
                               title="Languages"), 200
    if sous_sujet_nom == "Variables":
        return render_template("python/variables.html", title="Languages"), 200
    return render_template('sous_sujet.html', sujet=sujet.to_json()["Nom"],
                           sous_sujet=sous_sujet, title='Languages'), 200


# Retourner la première question du quiz d'un 'sous_sujet_nom' appartenant
# à un 'sujet_nom'
@app.route('/languages/quiz/<sujet_nom>', methods=["GET"])
def quiz(sujet_nom):
    sous_sujet_nom = request.args.get('sous-sujet')
    if sous_sujet_nom is None or len(sous_sujet_nom) == 0:
        err = "Le parametre sous-sujet est obligatoire."
        return render_template("404.html", title="Not found", err=err), 404
    try:
        sujet = get_db().read_sujet_nom(sujet_nom)  # TypeError
        sous_sujet_index = sujet.get_sous_sujet_index(
            sous_sujet_nom)  # ValueError
    except TypeError:
        # Retourner un 404 si le sujet n'existe pas
        err = "Le sujet '" + html.escape(sujet) + "' n'existe pas."
        return render_template("404.html", title="Not found", err=err), 404
    except ValueError as error:
        # Retourner un 404 si le sous-sujet n'existe pas
        return render_template("404.html", title="Not found",
                               err=str(error)), 404
    quiz = sujet.get_quiz_question(sous_sujet_index, 0)
    return render_template('quiz.html', sujet=sujet_nom,
                           sous_sujet=sous_sujet_nom,
                           question=quiz['Question'],
                           choix=quiz['Choix'],
                           title='Languages')


# Retouner la page de resultat de quiz
@app.route('/languages/quiz/resultat', methods=["GET", "POST"])
def quiz_resultat():
    if request.method == "POST":
        # Evaluer les reponses
        evaluer(request.form['data'])
        if is_authenticated():
            update_user_progress()
        return redirect('/languages/quiz/resultat')
    if "result" in session:
        # Retourner le resultat du quiz
        sujet = session["result"]["sujet"]
        sous_sujet = session["result"]["sous-sujet"]
        resultats = session["result"]["resultats"]
        note = session["result"]["note"]
        session.pop("result")
        return render_template('resultat.html', sujet=sujet,
                               sous_sujet=sous_sujet, resultats=resultats,
                               note=note, title='Languages')
    return render_template("404.html", title="Not found"), 404


def evaluer(raw_data):
    data = json.loads(raw_data)
    sujet_obj = get_db().read_sujet_nom(data["sujet"])
    sous_sujet_index = sujet_obj.get_sous_sujet_index(data["sous-sujet"])
    note = 0
    resultats = []
    for i, choix in enumerate(data["reponses"]):
        reponse = sujet_obj.get_quiz_reponse(sous_sujet_index, i)
        question = {
            "Question": reponse["Question"],
            "Choix": choix,
            "Indice": reponse["Indice"],
            "Etat": "incorrecte"
        }
        if reponse["Reponse"] == choix:
            question["Etat"] = "correcte"
            note += 1
        resultats.append(question)
    note = (note / len(data["reponses"])) * 100
    quiz = {
        "sujet": data["sujet"],
        "sous-sujet": data["sous-sujet"],
        "resultats": resultats,
        "note": round(note)
    }
    session["result"] = quiz


def update_user_progress():
    db = get_db()
    user = db.read_user_username(session["user"]["name"])
    sujet = session["result"]["sujet"]
    sous_sujet = session["result"]["sous-sujet"]
    # Seuil de réussite
    resultat = "E"
    if session["result"]["note"] > 79:
        resultat = "S"
    user.update_progress(sujet, sous_sujet, resultat)
    db.update_user_progress(user)
    session["user"] = user.session()


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
        return render_template("404.html", title="Not found", err=err), 404
    except TypeError:
        # Retourner un statut 204 si aucun sujet n'a été trouvé
        return ('', 204)
    except KeyError:
        # Retourner une erreur si le nom du sous-sujet n'existe pas
        err = "Le sujet '" + html.escape(nom_sous_sujet) + "' n'existe pas."
        return render_template("404.html", title="Not found", err=err), 404
    except IndexError:
        # Retourner une erreur si le numero de la question du quiz n'existe pas
        err = "Le numero '" + str(numero) + "' n'existe pas."
        return render_template("404.html", title="Not found", err=err), 404
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


# Retourne True si les données sont valides
@app.route('/api/is_authorized', methods=["GET"])
def api_is_authorized():
    username = request.args.get('username')
    password = request.args.get('password')
    path = request.args.get('path')
    user = is_authorized(username, password)
    if not user:
        # Accès non autorisé
        error = session["error"]
        session.pop("error")
        return jsonify({"is_authorized": False, "reason": error})
    if len(path) != 0:
        session['path'] = path
    return jsonify({"is_authorized": True})


# Modifier les informations d'un utilisateur
@app.route('/api/compte/modifier', methods=["GET"])
def api_modifier_compte():
    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    try:
        db = get_db()
        if (username != session['user']['name']
                and db.read_user_username(username)):
            #  Nom utilisateur invalide
            error = "Username already exists. Please enter another one"
            return jsonify({"valid": False, "reason": error}), 404
        user = db.read_user_username(session['user']['name'])
        modify_user(user, username, email, password)  # ValueError
        session["user"] = user.session()
        db.update_user_info(user)
    except ValueError as error:
        return jsonify({"valid": False, "reason": str(error)}), 404
    return jsonify({"valid": True}), 200


# Temporaire pour tester la progression
@app.route('/test/session')
def test_session():
    user_session = None
    if "user" in session:
        user_session = session["user"]
    return jsonify({"session": user_session}), 200
