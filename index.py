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
    return render_template('index.html', title='index'), 200