import os
import sqlite3
from contextlib import closing

from flask import g

from app import app, settings

SCHEMA_FILE = os.path.join(settings.BASE_DIR, 'schema.sql')


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
