import json
import logging

logger = logging.getLogger(__name__)

__program__ = 'Astro'
__version__ = '0.1.0'


class AlexaResponse():
    card_text = None
    card_title = None
    ends_session = True
    reprompt_speech = None
    response_version = __version__
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


def get_response(event):
    session = event.get('session', {})
    request = event.get('request', {})
    if not session or not request:
        # bad request
        return AlexaResponse('Sorry, there was an error.')

    event_type = request['type']

    intents = {
        'AMAZON.HelpIntent': help,
    }

    if event_type == 'LaunchRequest':
        return AlexaResponse(
            'Welcome to {0}. Try asking me about a planet.'
            .format(__program__)
        )
    elif event_type == 'IntentRequest':
        intent_name = request['intent']['name']
        func = intents[intent_name]
        return func(event)
    elif event_type == 'SessionEndedRequest':
        return AlexaResponse('Goodbye.')
    else:
        # weirrrrrd
        return AlexaResponse('I am not sure what you meant.')


def help(event):
    data = AlexaResponse(
        'Ask me about a planet, a moon, or what you see.'
    )
    return data
