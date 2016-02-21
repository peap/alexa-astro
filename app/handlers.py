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
    if requested_city:
        city, coords = get_coordinates_for_city(requested_city)
        try:
            alexa_request.user.set_location(city, *coords)
        except CityNotFound:
            response = AlexaResponse(
                'I couldn\'t find a city called "{0}".'
                .format(requested_city)
            )
            response.ask('Where are you located?')
        except CityNotSpecificEnough:
            response = AlexaResponse(
                'There are multiple places named "{0}".'
                .format(requested_city)
            )
            response.ask('Which one do you mean?')
        else:
            response = AlexaResponse('Location set to "{0}".'.format(city))
        return response
    else:
        return AlexaResponse(
            'Please request a city. Setting latitude and longitude is not yet '
            'supported.'
        )
