from decimal import Decimal
from unittest import TestCase

from app.location import get_coordinates_for_city

CITIES_ON_WIKIPEDIA = {
    'Austin': ('30.25000', '-97.75000'),
    'Seattle': ('47.60972', '-122.33306'),
}


class CityCoordinatesTestCase(TestCase):
    def test_can_get_coordinates_for_large_cities(self):
        for input_city, coords in CITIES_ON_WIKIPEDIA.items():
            city, (lat, lon) = get_coordinates_for_city(input_city)
            self.assertEqual(Decimal(coords[0]), lat)
            self.assertEqual(Decimal(coords[1]), lon)
