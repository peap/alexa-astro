#!/usr/bin/env python
import sys

from app.location import (
    get_coordinates_for_city, CityNotFound, CityNotSpecificEnough,
)


input_city = ' '.join(sys.argv[1:])
sys.stdout.write('Getting coordinates of "{0}"...\n'.format(input_city))

try:
    city, coords = get_coordinates_for_city(input_city)
except CityNotFound:
    sys.stdout.write('...city not found.\n')
except CityNotSpecificEnough as e:
    sys.stdout.write(
        '...be more specific.\nDid you mean {0}, {1}, or something else?\n'
        .format(*e.args[0][:2])
    )
else:
    sys.stdout.write('...found "{0}"\n'.format(city))
    sys.stdout.write('Latitude:  {0}\nLongitude: {1}\n'.format(*coords))
