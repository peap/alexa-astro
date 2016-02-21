from app.alexa import AlexaResponse
from app.location import (
    CityNotFound, CityNotSpecificEnough, get_coordinates_for_city,
)

INTENTS = {}


def intent_handler(name):

    def wrapper(func):
        INTENTS[name] = func

        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return wrapper


def welcome(alexa_request):
    return AlexaResponse('Hello. Try asking me what\'s visible in the sky.')


@intent_handler('AMAZON.HelpIntent')
def overview(alexa_request):
    return AlexaResponse(
        'Pluto the astronomer can tell you what\'s visible in the sky, what '
        'you\'re looking at, and when objects will rise and set. Try asking '
        'about a planet, or what\'s visible right now.'
    )


@intent_handler('SetLocation')
def set_location(alexa_request):
    requested_city = alexa_request.slots['City'].get('value')
    requested_state = alexa_request.slots['State'].get('value')
    if requested_city:
        if requested_state:
            search_str = ', '.join([requested_city, requested_state])
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
