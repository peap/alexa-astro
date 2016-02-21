#!/usr/bin/env python
import os

from app import app, settings
from app.db import get_db

SCHEMA_FILE = os.path.join(settings.BASE_DIR, 'schema.sql')


def main():
    with app.app_context():
        db = get_db()
        with app.open_resource(SCHEMA_FILE, mode='r') as f:
            db.cursor().executescript(f.read())
            db.commit()

if __name__ == '__main__':
    main()
