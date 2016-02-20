#!/usr/bin/env python
import sys

import ephem


INTERESTING_PLANETS = [
    ephem.Mercury,
    ephem.Venus,
    ephem.Mars,
    ephem.Jupiter,
    ephem.Saturn,
    ephem.Uranus,
    ephem.Neptune,
]

MIN_ALT = 5.0 * ephem.degree


def get_observer(city):
    observer = ephem.Observer()
    # TODO: lookup coordinates... it's just Seattle, for now
    observer.lat = 47.606
    observer.lon = -122.332
    return observer


def get_visible_planets(observer):
    visible = []
    for Planet in INTERESTING_PLANETS:
        planet = Planet()
        planet.compute(observer)
        if planet.alt >= MIN_ALT:
            visible.append(planet)
    return visible


if __name__ == '__main__':
    seattle_observer = get_observer('Seattle, WA')
    for planet in get_visible_planets(seattle_observer):
        altitude = round(planet.alt / ephem.degree)
        azimuth = round(planet.az / ephem.degree)
        sys.stdout.write(
            '{0.name}: azimuth {1} degrees, altitude {2} degrees\n'
            .format(planet, azimuth, altitude)
        )
