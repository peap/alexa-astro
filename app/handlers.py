import logging
from functools import wraps

from app import settings
from app.alexa import AlexaResponse
from app.astro import get_visible_objects
from app.location import (
    CityNotFound, CityNotSpecificEnough, get_coordinates_for_city,
)

logger = logging.getLogger(__name__)

# Decorators for handler registration

INTENT_HANDLERS = {}
REQUEST_TYPE_HANDLERS = {}


def intent_handler(name):
    """Register an intent handler for the given intent name."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        INTENT_HANDLERS[name] = func
        return wrapper
    return decorator


def request_handler(name):
    """Register an request-type handler for the given request type."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        REQUEST_TYPE_HANDLERS[name] = func
        return wrapper
    return decorator


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
    if alexa_request.user.new:
        return AlexaResponse(
            'Welcome to {0}. Try asking me what\'s visible in the sky by saying '
            '"ask {1} what\'s up."'
            .format(settings.SKILL_NAME, settings.SKILL_INVOCATION_NAME)
        )
    else:
        return whats_visible(alexa_request)


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
        '{0} can tell you what\'s visible in the sky, what '
        'you\'re looking at, and when objects will rise and set. Try asking '
        'about a planet, or what\'s visible right now.'
        .format(settings.SKILL_NAME)
    )


@intent_handler('AMAZON.NoIntent')
def no(alexa_request):
    # look in session for what this no means...
    return AlexaResponse('fine')


@intent_handler('AMAZON.YesIntent')
def yes(alexa_request):
    # look in session for what this yes means...
    return AlexaResponse('great!')


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
                'I have the following coordinates for {0}:\n'
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
    in_city = alexa_request.slots['City'].get('value')
    in_state = alexa_request.slots['State'].get('value')
    if in_city:
        search_str = ', '.join([in_city, in_state]) if in_state else in_city
        try:
            city, coords = get_coordinates_for_city(in_city, state=in_state)
        except CityNotFound:
            response = AlexaResponse(
                'I couldn\'t find a city called {0}. What\'s another city that '
                'is nearby?'
                .format(search_str)
            )
            response.reprompt('Where are you located?')
        except CityNotSpecificEnough:
            response = AlexaResponse(
                'There are multiple places named {0}. Which one did you mean?'
                .format(search_str)
            )
            response.reprompt('Which {0} did you mean?'.format(search_str))
            response.add_to_session('city', in_city)
        else:
            alexa_request.user.set_location(coords[0], coords[1], city)
            response = AlexaResponse('Location set to {0}.'.format(city))
        return response
    else:
        if in_state:
            previous_city = alexa_request.session.get('city')
            search_str = (
                ', '.join([previous_city, in_state]) if previous_city else in_state
            )
            try:
                if previous_city:
                    city, coords = get_coordinates_for_city(previous_city, state=in_state)
                else:
                    # this seems to work, but... naming :/
                    city, coords = get_coordinates_for_city(in_state)
            except CityNotFound:
                response = AlexaResponse(
                    'I couldn\'t find a city called {0}.'.format(search_str)
                )
            except CityNotSpecificEnough:
                response = AlexaResponse(
                    'There are multiple places named {0}. Which one did you mean?'
                    .format(search_str)
                )
                response.reprompt('Which {0} did you mean?'.format(search_str))
                response.add_to_session('city', in_city)
            else:
                alexa_request.user.set_location(coords[0], coords[1], city)
                response = AlexaResponse('Location set to {0}.'.format(city))
        else:
            return AlexaResponse('You can set your location by telling me a city.')


@intent_handler('WhatsVisible')
def whats_visible(alexa_request):
    response = None
    user = alexa_request.user
    lat, lon, city = user.get_location()
    if city:
        if lat and lon:
            visible_objects = get_visible_objects(lat, lon)
            if len(visible_objects) == 0:
                response = AlexaResponse(
                    'Currently, there are no interesting objects visible. '
                    'To find out when something will rise, say "Alexa, ask '
                    '{0} when Jupiter will rise."'
                    .format(settings.SKILL_INVOCATION_NAME)
                )
            if len(visible_objects) == 1:
                obj = visible_objects[0]
                response = AlexaResponse(
                    'There\'s only one object visible right now, {0.name}. '
                    'You can find it at {0.azimuth} degrees azimuth and '
                    '{0.altitude} degrees altitude.'
                    .format(obj)
                )
            elif len(visible_objects) == 2:
                obj1, obj2 = visible_objects[:2]
                response = AlexaResponse(
                    'There are a couple objects visible right now, {0.name} '
                    'and {1.name}.'
                    .format(obj1, obj2, settings.SKILL_INVOCATION_NAME)
                )
            elif len(visible_objects) == 3:
                obj1, obj2, obj3 = visible_objects[:3]
                response = AlexaResponse(
                    'There are a few objects visible right now, {0.name}, '
                    '{1.name}, and {2.name}.'
                    .format(obj1, obj2, obj3)
                )
            else:
                obj1, obj2, obj3 = visible_objects[:3]
                response = AlexaResponse(
                    'There are a several objects visible right now, including '
                    '{0.name}, {1.name}, and {2.name}. '
                    'Would you like to hear the entire list?'
                    .format(obj1, obj2, obj3)
                )
                response.reprompt(
                    'Would you like to hear the entire list of visible objects?'
                )
                response.add_to_session('previousIntent', 'WhatsVisible')
                response.add_to_session('question', 'hear full list')
        else:
            # have a city, but not lat and lon...
            logging.error(
                'User {0} has a city ({1}), but is missing latitude and/or longitude.'
                .format(user, city)
            )
    if response is None:
        if alexa_request.session['new']:
            response = AlexaResponse(
                'Hello from {0}. To get started, I need to know where you\'re '
                'located. What city is closest to you?'
                .format(settings.SKILL_NAME)
            )
        else:
            response = AlexaResponse(
                'I don\'t know your location. What city is closest to you?'
            )
        response.reprompt('What city is closest to you?')
        response.add_to_session('previousIntent', 'WhatsVisible')
        response.add_to_session('question', 'closest city')
    return response
