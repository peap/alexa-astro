import os
import sqlite3
from contextlib import closing

from flask import Flask, abort, jsonify, g, render_template, request

from app import settings

SCHEMA_FILE = os.path.join(settings.BASE_DIR, 'schema.sql')


app = Flask('alexa-astro')
app.config.from_object(settings)


def connect_db():
    return sqlite3.connect(app.config['DATABASE_FILE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(SCHEMA_FILE, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before():
    g.db = connect_db()


@app.teardown_appcontext
@app.teardown_request
def teardown(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')


@app.route('/alexa/', methods=['POST'])
def incoming_alexa_request():
    from app.alexa import AlexaRequest
    from app.handlers import dispatch
    try:
        alexa_request = AlexaRequest(request)
    except ValueError:
        abort(400)

    if alexa_request.is_valid():
        alexa_response = dispatch(alexa_request)
    else:
        abort(403)

    return jsonify(alexa_response.to_dict())
