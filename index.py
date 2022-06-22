from flask import Flask
from flask import render_template
from flask import g

from .modules.database import Database

app = Flask(__name__)


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


@app.route('/')
def index():
    return render_template('index.html', title='Accueil'), 200


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
