import os
import pickle
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

from app import settings
from app.location import get_coordinates_for_city

CITIES_ON_WIKIPEDIA = {
    'Austin': {
        'coords': ('30.25000', '-97.75000'),
        'pickle': os.path.join(settings.BASE_DIR, 'tests', 'data', 'austin.p'),
    },
    'Seattle': {
        'coords': ('47.60972', '-122.33306'),
        'pickle': os.path.join(settings.BASE_DIR, 'tests', 'data', 'seattle.p'),
    },
}


class CityCoordinatesTestCase(TestCase):
    @patch('app.location.add_coordinates_to_db')
    @patch('app.location.get_coordinates_from_db')
    @patch('wikipedia.page')
    def test_can_get_coords_for_large_cities(self, mock_page, mock_get, mock_add):
        mock_get.return_value = None
        for input_city, attrs in CITIES_ON_WIKIPEDIA.items():
            with open(attrs['pickle'], 'rb') as f:
                mock_page.return_value = pickle.load(f)
            expected_coords = attrs['coords']
            city, (lat, lon) = get_coordinates_for_city(input_city)
            self.assertEqual(Decimal(expected_coords[0]), lat)
            self.assertEqual(Decimal(expected_coords[1]), lon)
