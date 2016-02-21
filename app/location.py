from decimal import Decimal
import warnings

import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

from app.db import get_db, query_db

FIVE_PLACES = Decimal(10) ** -5


class CityNotFound(Exception):
    pass


class CityNotSpecificEnough(Exception):
    pass


def add_coordinates_to_db(city, coords):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'insert into locations(city, latitude, longitude) values (?, ?, ?)',
        [city, str(coords[0]), str(coords[1])],
    )
    db.commit()


def get_coordinates_from_db(city):
    row = query_db(
        'select latitude, longitude from locations where city = ?',
        [city],
        one=True,
    )
    if row:
        return (Decimal(row[0]), Decimal(row[1]))
    else:
        return None


def get_coordinates_for_city(city, state=None):
    """
    Get the latitude and longitude for the provided string, which can be
    anything you think Wikipedia will be able to disambiguate.

    Return tuple of discovered city name and coordinates tuple. Example:

    >>> get_coordinates_for_city('seattle')
    ('Seattle', (Decimal('47.60972'), Decimal('-122.33306')))
    """
    if state:
        search_str = ', '.join([city, state])
    else:
        search_str = city

    db_coords = get_coordinates_from_db(search_str)
    if db_coords:
        return (search_str, db_coords)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            page = wikipedia.page(search_str)
    except DisambiguationError as e:
        raise CityNotSpecificEnough(e.options) from e
    try:
        lat, lon = page.coordinates
    except (KeyError, PageError):
        # TODO: log
        raise CityNotFound()
    else:
        coords = (lat.quantize(FIVE_PLACES), lon.quantize(FIVE_PLACES))
        add_coordinates_to_db(search_str, coords)
        return (page.title, coords)
