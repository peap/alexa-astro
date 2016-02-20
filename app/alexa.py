import logging
import sqlite3

from flask import abort

from app import settings
from app.db import get_db, query_db
from app.signatures import cert_chain_url_valid, parse_certificate, signature_valid

logger = logging.getLogger(__name__)


class AlexaResponse():
    card_text = None
    card_title = None
    ends_session = True
    reprompt_speech = None
    response_version = settings.SKILL_VERSION
    speech = None

    def __init__(self, speech_text, ends_session=True):
        self.speech = speech_text
        self.ends_session = ends_session
        self.session_attributes = {}

    def ask(self, question):
        self.reprompt_speech = question

    def card(self, title, text):
        self.card_title = title
        self.card_text = text

    def get_card_dict(self):
        return {
            'type': 'Simple',
            'title': self.card_title,
            'content': self.card_text,
        }

    def get_reprompt_dict(self):
        return {
            'outputSpeech': {
              'type': 'PlainText',
              'text': self.reprompt_speech,
            },
        }

    def get_speech_dict(self):
        return {
            'type': 'PlainText',
            'text': self.speech,
        }

    def to_dict(self):
        data = {
            'response': {
                'outputSpeech': self.get_speech_dict(),
                'shouldEndSession': self.ends_session,
            },
            'sessionAttributes': self.session_attributes,
            'version': self.response_version,
        }
        if self.card_text:
            data['response'].update({'card': self.get_card_dict()})
        if self.reprompt_speech:
            data['response'].update({'reprompt': self.get_reprompt_dict()})
        return data


class AlexaUser():
    new = False

    def __init__(self, user_id):
        self.user_id = user_id

        data = self.get_data_by_id(user_id)
        if data is None:
            self.new = True
            self.create(user_id)
            data = self.get_data_by_id(user_id)

        self.pk = data['id']
        self.latitude = data['latitude']
        self.longitude = data['longitude']

    @classmethod
    def create(cls, user_id):
        logging.info('Creating user record for {0}'.format(user_id))
        db = get_db()
        cur = db.cursor()
        cur.execute('insert into alexa_users(amazon_id) values (?)', [user_id])
        db.commit()

    @classmethod
    def get_data_by_id(self, user_id):
        query = (
            'select id, latitude, longitude from alexa_users '
            'where amazon_id = ?'
        )
        user_data = query_db(query, args=[user_id], one=True)
        if user_data is None:
            return None
        else:
            return {
                'id': user_data[0],
                'latitude': user_data[1],
                'longitude': user_data[2],
            }


def alexa_request_valid(request):
    # check Application ID
    event = request.json
    sent_id = event['session']['application']['applicationId']
    if sent_id != settings.AMAZON_APPLICATION_ID:
        # TODO: log
        return False

    # check timestamp
    # TODO!

    # check certificate URL
    cert_chain_url = request.headers.get('SignatureCertChainUrl')
    if not cert_chain_url_valid(cert_chain_url):
        # TODO: log
        return False

    # check signature
    signature = request.headers.get('Signature')
    cert_text = parse_certificate(cert_chain_url)
    request_body = request.data
    if not signature_valid(signature, cert_text, request_body):
        # TODO: log
        return False

    return True


def get_response(request):
    try:
        event = request.json
    except ValueError:
        abort(400)

    if not alexa_request_valid(request):
        abort(403)

    session = event.get('session', {})
    request = event.get('request', {})
    if not session or not request:
        # bad request
        return AlexaResponse('Sorry, there was an error.')

    user = AlexaUser(session['user']['userId'])

    event_type = request['type']

    intents = {
        'AMAZON.HelpIntent': help,
    }

    if event_type == 'LaunchRequest':
        return AlexaResponse(
            'Hi! Call me {0}. Try asking me about a planet.'
            .format(settings.SKILL_INVOCATION_NAME)
        )
    elif event_type == 'IntentRequest':
        intent_name = request['intent']['name']
        func = intents.get(intent_name)
        if func:
            return func(event)
        else:
            return AlexaResponse('Sorry, that feature isn\'t ready yet.')
    elif event_type == 'SessionEndedRequest':
        return AlexaResponse('Goodbye.')
    else:
        # weirrrrrd
        return AlexaResponse('I am not sure what you meant.')


def help(event):
    data = AlexaResponse(
        'Ask me about a planet, a moon, or what you see in the sky.'
    )
    return data
