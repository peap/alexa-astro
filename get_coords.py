#!/usr/bin/env python
import sys

from app.location import (
    get_coordinates_from_wikipedia, CityNotFound, CityNotSpecificEnough,
)


search_str = ' '.join(sys.argv[1:])
if not search_str:
    sys.stderr.write('Enter a location name to search for.\n')
    sys.exit(1)

sys.stdout.write('Getting coordinates of "{0}"...\n'.format(search_str))
try:
    city, coords = get_coordinates_from_wikipedia(search_str)
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
