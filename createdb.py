#!/usr/bin/env python
from app import app, init_db


if __name__ == '__main__':
    with app.app_context():
        init_db()
