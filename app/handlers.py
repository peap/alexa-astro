import logging

from app import settings
from app.alexa import AlexaResponse
from app.location import (
    CityNotFound, CityNotSpecificEnough, get_coordinates_for_city,
)

logger = logging.getLogger(__name__)

# Decorators for handler registration

INTENT_HANDLERS = {}
REQUEST_TYPE_HANDLERS = {}


def intent_handler(name):
    """Register an intent handler for the given intent name."""
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        INTENT_HANDLERS[name] = func
        return inner
    return wrapper


def request_handler(name):
    """Register an request-type handler for the given request type."""
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        REQUEST_TYPE_HANDLERS[name] = func
        return inner
    return wrapper


# Main controller

def dispatch(alexa_request):
    """
    Dispatch the incoming, valid AlexaRequest to the appropriate request-type
    handler.
    """
    request_type = alexa_request.request_type
    request_type_handler = REQUEST_TYPE_HANDLERS.get(request_type)
    if callable(request_type_handler):
        return request_type_handler(alexa_request)
    else:
        logger.error('Unhandled request type: {0}'.format(request_type))
        return AlexaResponse('Sorry, that feature isn\'t ready yet.')


# Request-type handlers

@request_handler('LaunchRequest')
def welcome(alexa_request):
    return AlexaResponse(
        'Welcome to {0}. Try asking me what\'s visible in the sky by saying '
        '"Alexa, ask {1} what\'s up."'
        .format(settings.SKILL_NAME, settings.SKILL_INVOCATION_NAME)
    )


@request_handler('IntentRequest')
def intent_dispatcher(alexa_request):
    """Dispatch the incoming AlexaRequest to the appropriate intent handler."""
    intent_name = alexa_request.intent_name
    intent_handler = INTENT_HANDLERS.get(intent_name)
    if callable(intent_handler):
        return intent_handler(alexa_request)
    else:
        logger.error('Unhandled intent: {0}'.format(intent_name))
        return AlexaResponse('Sorry, that feature isn\'t ready yet.')


@request_handler('SessionEndedRequest')
def session_ended(alexa_request):
    # No response is allowed for a SessionEndedRequest, but just in case Amazon
    # changes their mind about that...
    return AlexaResponse('So long, and keep looking up!')


# Intent handlers

@intent_handler('AMAZON.HelpIntent')
def help(alexa_request):
    return AlexaResponse(
        'Pluto the astronomer can tell you what\'s visible in the sky, what '
        'you\'re looking at, and when objects will rise and set. Try asking '
        'about a planet, or what\'s visible right now.'
    )


@intent_handler('AMAZON.StopIntent')
def stop(alexa_request):
    return AlexaResponse('So long, and keep looking up!')


@intent_handler('GetLocation')
def get_location(alexa_request):
    lat, lon, city = alexa_request.user.get_location()
    if city:
        response = AlexaResponse(
            'I have {0} as your current location.'.format(city)
        )
        if lat and lon:
            card_text = (
                'Pluto has the following coordinates for {0}:\n'
                'Latitude:  {1}\n'
                'Longitude: {2}'
                .format(city, lat, lon)
            )
            response.card('Coordinates of {0}'.format(city), card_text)
    else:
        response = AlexaResponse('hi')
    return response


@intent_handler('SetLocation')
def set_location(alexa_request):
    requested_city = alexa_request.slots['City'].get('value')
    requested_state = alexa_request.slots['State'].get('value')
    if requested_city:
        if requested_state:
            search_str = ', '.join([requested_city, requested_state])
        else:
            search_str = requested_city
        try:
            city, coords = get_coordinates_for_city(
                requested_city, state=requested_state)
        except CityNotFound:
            response = AlexaResponse(
                'I couldn\'t find a city called {0}.'.format(search_str)
            )
            response.ask('Where are you located?')
        except CityNotSpecificEnough:
            response = AlexaResponse(
                'There are multiple places named {0}.'
                .format(search_str)
            )
            response.ask('Which one do you mean?')
        else:
            alexa_request.user.set_location(coords[0], coords[1], city)
            response = AlexaResponse('Location set to {0}.'.format(city))
        return response
    else:
        return AlexaResponse(
            'Please request a city. Setting latitude and longitude is not yet '
            'supported.'
        )
