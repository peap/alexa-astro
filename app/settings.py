import os

AMAZON_APPLICATION_ID = 'amzn1.echo-sdk-ams.app.6f2cd304-8d03-45ae-8135-18e6d3486035'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_FILE = os.path.join(BASE_DIR, 'db.sqlite')

SKILL_INVOCATION_NAME = 'Pluto'
SKILL_NAME = 'Pluto the Astronomer'
SKILL_VERSION = '0.2.1'
