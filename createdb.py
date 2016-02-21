#!/usr/bin/env python
from app import app
from app.db import get_db


def main():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            db.commit()

if __name__ == '__main__':
    main()
