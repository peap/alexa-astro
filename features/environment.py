import os
import tempfile
from unittest.mock import Mock

from app import app, init_db
from app.alexa import AlexaRequest

original_is_valid = AlexaRequest.is_valid


def before_feature(context, feature):
    app.config['TESTING'] = True
    context.db, app.config['DATABASE_FILE'] = tempfile.mkstemp()
    context.client = app.test_client()
    init_db()
    AlexaRequest.is_valid = Mock(return_value=True)


def after_feature(context, feature):
    AlexaRequest.is_valid = original_is_valid
    os.close(context.db)
    os.remove(app.config['DATABASE_FILE'])
