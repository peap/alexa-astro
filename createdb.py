#!/usr/bin/env python
from app import app
from app.db import init_db


if __name__ == '__main__':
    with app.app_context():
        init_db()
