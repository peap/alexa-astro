from decimal import Decimal
import warnings

import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

FIVE_PLACES = Decimal(10) ** -5


class CityNotFound(Exception):
    pass


class CityNotSpecificEnough(Exception):
    pass


def get_coordinates_for_city(city):
    """
    Get the latitude and longitude for the provided string, which can be
    anything you think Wikipedia will be able to disambiguate.

    Return tuple of discovered city name and coordinates tuple. Example:

    >>> get_coordinates_for_city("seattle")
    ("Seattle", (Decimal('47.60972'), Decimal('')))
    """
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            page = wikipedia.page(city)
    except DisambiguationError as e:
        raise CityNotSpecificEnough(e.options) from e
    try:
        lat, lon = page.coordinates
    except (KeyError, PageError):
        # TODO: log
        raise CityNotFound()
    else:
        return (
            page.title,
            (lat.quantize(FIVE_PLACES), lon.quantize(FIVE_PLACES)),
        )
