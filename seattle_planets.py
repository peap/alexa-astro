#!/usr/bin/env python
import sys

from app.astro import get_visible_objects


if __name__ == '__main__':
    lat, lon = 47.606, -122.332
    sys.stdout.write('Things visible from Seattle right now:\n')
    for obj in get_visible_objects(lat, lon):
        sys.stdout.write(
            '* {0.name}: azimuth {1} degrees, altitude {2} degrees\n'
            .format(obj, obj.azimuth, obj.altitude)
        )
