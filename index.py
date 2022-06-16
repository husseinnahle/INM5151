import json
from flask import Flask
from flask import render_template
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


@app.route('/')
def index():
    return render_template('index.html', title='index'), 200


# Tester si la lecture et l'ecriture des donnees fonctionne
@app.route('/test/sujets')
def sujets():
    db = get_db()
    sujets = db.read_all_sujet()
    return jsonify([sujet.to_json() for sujet in sujets]), 200
