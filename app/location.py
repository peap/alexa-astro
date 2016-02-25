import warnings
from contextlib import closing
from decimal import Decimal

from flask import g
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

FIVE_PLACES = Decimal(10) ** -5


class CityNotFound(Exception):
    pass


class CityNotSpecificEnough(Exception):
    pass


def add_coordinates_to_db(coords, city):
    query = 'insert into locations(latitude, longitude, city) values (?, ?, ?)'
    with closing(g.db.cursor()) as cursor:
        cursor.execute(query, [str(coords[0]), str(coords[1]), city])
        g.db.commit()


def get_coordinates_from_db(city):
    query = 'select latitude, longitude from locations where city = ?'
    with closing(g.db.cursor()) as cursor:
        cursor.execute(query, [city])
        row = cursor.fetchone()
    if row:
        return (Decimal(row[0]), Decimal(row[1]))
    else:
        return None


def get_coordinates_from_wikipedia(search_str):
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
        return (page.title, coords)


def get_coordinates_for_city(city, state=None):
    """
    Get the latitude and longitude for the provided string, which can be
    anything you think Wikipedia will be able to disambiguate.

    Return tuple of discovered city name and coordinates tuple. Example:

    >>> get_coordinates_for_city('seattle')
    ('Seattle', (Decimal('47.60972'), Decimal('-122.33306')))
    """
    search_str = ', '.join([city, state]) if state else city
    db_coords = get_coordinates_from_db(search_str)
    if db_coords:
        return (search_str, db_coords)
    else:
        page_title, coords = get_coordinates_from_wikipedia(search_str)
        add_coordinates_to_db(coords, search_str)
        return (page_title, coords)
