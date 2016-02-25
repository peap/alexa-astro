import json
from datetime import datetime

from behave import given, then, when

from app import settings


def base_alexa_request(request_type, new=True):
    request_id = 'amzn1.echo-api.request.0000000-0000-0000-0000-00000000000'
    session_id = 'amzn1.echo-api.session.0000000-0000-0000-0000-00000000000'
    user_id = 'amzn1.account.AM3B00000000000000000000000'
    return {
        'version': '1.0',
        'session': {
            'new': new,
            'sessionId': session_id,
            'application': {
                'applicationId': settings.AMAZON_APPLICATION_ID,
            },
            'attributes': {},
            'user': {
                'userId': user_id,
            },
        },
        'request': {
            'type': request_type,
            'requestId': request_id,
            'timestamp': datetime.now().isoformat(),
        },
    }


@given('our skill is enabled')
def flask_setup(context):
    assert context.client and context.db


@when('a new user launches Pluto')
def launched_by_new_user(context):
    data = base_alexa_request('LaunchRequest')
    context.response = context.client.post(
        '/alexa/',
        data=json.dumps(data),
        content_type='application/json',
    )
    assert context.response


@then('Alexa greets them and offers advice')
def new_user_greeting(context):
    assert context.response.status_code == 200
    data = json.loads(context.response.data.decode('utf-8'))
    assert isinstance(data, dict)
    assert 'Welcome' in data['response']['outputSpeech']['text']
