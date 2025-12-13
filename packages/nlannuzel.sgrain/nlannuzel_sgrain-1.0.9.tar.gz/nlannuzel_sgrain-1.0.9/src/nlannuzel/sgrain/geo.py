from math import sqrt, cos, asin, radians


class Location:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f"(lat={self.lat},lon={self.lon})"

    def distance_to(self, other):
        """Returns the distance to another point, in kilometers, using the Haversine formula."""
        # https://en.wikipedia.org/wiki/Haversine_formula
        # r = 6356.752  # Radius of the earth at the poles
        r = 6378.137  # Radius of the earth on the equator

        def to_rad(loc):
            yield radians(loc.lon)
            yield radians(loc.lat)
        lambda1, phi1 = to_rad(self)
        lambda2, phi2 = to_rad(other)
        d_phi = phi2 - phi1
        d_lambda = lambda2 - lambda1
        return 2 * r * asin( sqrt( 1/2 * (1 - cos(d_phi) + cos(phi1) * cos(phi2) * (1 - cos(d_lambda))) ) )
