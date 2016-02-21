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


class AstroObject():
    def __init__(self, ephem_object, observer):
        self.altitude = round(ephem_object.alt / ephem.degree)
        self.azimuth = round(ephem_object.az / ephem.degree)
        self.ephem_object = ephem_object
        self.name = ephem_object.name
        self.observer = observer


def get_visible_objects(lat, lon):
    """
    Get interesting objects currently visible from the given latitude and
    longitude.

    TODO: add other things besides planets
    """
    visible = []
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    for Planet in INTERESTING_PLANETS:
        planet = Planet()
        planet.compute(observer)
        if planet.alt >= MIN_ALT:
            visible.append(AstroObject(planet, observer))
    return visible
