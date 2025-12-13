from nlannuzel.sgrain.geo import Location
from nlannuzel.sgrain.graph import Color, Image, Pixel, YELLOW, BLACK, BlobFinder
import png
import urllib.request
import datetime
import time
import os
import shutil
import fcntl

class RainAreas:
    # Coordinates from the HTML/js code of
    # https://www.weather.gov.sg/weather-rain-area-50km but these
    # values give high misalignment. Keeping here for reference.
    #
    # var map_latitude_top = 1.4572;
    # var map_longitude_left = 103.565;
    # var map_latitude_bottom = 1.1450;
    # var map_longitude_right = 104.130;

    # Coordinates of covered area estimated by aliging the map image
    # on https://www.weather.gov.sg/weather-rain-area-50km/ with
    # Google Maps, and hand picking the coordinates of the corners.
    top_left = Location(1.47721, 103.555423)
    bottom_right = Location(1.15320, 104.13393)

    # 32 levels color scale from
    # https://www.weather.gov.sg/wp-content/themes/wiptheme/images/rain-intensity.jpg
    #
    # Used to convert a RGB color from the rain map image into a
    # intensity from 0 (no rain) to 31 (maximum rain level)
    color_scale = [Color(r, g, b) for r, g, b in [
            [ 0  , 0  , 0   ],
            [ 0  , 255, 255 ],
            [ 0  , 238, 238 ],
            [ 0  , 208, 212 ],
            [ 0  , 185, 191 ],
            [ 0  , 149, 153 ],
            [ 0  , 130, 125 ],
            [ 0  , 128, 70  ],
            [ 0  , 137, 59  ],
            [ 0  , 161, 57  ],
            [ 0  , 182, 46  ],
            [ 0  , 201, 29  ],
            [ 0  , 217, 30  ],
            [ 0  , 244, 32  ],
            [ 0  , 255, 31  ],
            [ 0  , 255, 77  ],
            [ 255, 255, 68  ],
            [ 255, 255, 31  ],
            [ 255, 239, 30  ],
            [ 255, 219, 24  ],
            [ 255, 197, 20  ],
            [ 255, 177, 19  ],
            [ 255, 164, 16  ],
            [ 255, 136, 13  ],
            [ 255, 113, 9   ],
            [ 255, 74 , 5   ],
            [ 255, 31 , 3   ],
            [ 227, 2  , 1   ],
            [ 194, 2  , 1   ],
            [ 180, 3  , 104 ],
            [ 212, 8  , 168 ],
            [ 255, 16 , 251 ]
    ]]

    def __init__(self, cache_dir=None):
        self._cache_dir = cache_dir
        self._blobs = None
        self._intensity_map = None

    def round_to_previous_5_min(self, dt):
        """Round the time down to previous 5 minute, because images on
        the remote site are updated exactly every 5 minutes"""
        return datetime.datetime(
            year   = dt.year,
            month  = dt.month,
            day    = dt.day,
            hour   = dt.hour,
            minute = 5 * (dt.minute//5),
        )

    def _download_image_to_cache(self):
        """Download the remote image and save it in a file locally"""
        url = f"https://www.weather.gov.sg/files/rainarea/50km/v2/{self.filename}"

        with open(self.filepath, "ab") as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # wait until we get the lock...
            # we got the lock
            try:
                if os.fstat(f.fileno()).st_size == 0:  # file is empty, create it
                    with urllib.request.urlopen(url) as response:
                        shutil.copyfileobj(response, f)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def _read_image_from_cache(self):
        """read the local image file, and load it in memory"""
        with open(self.filepath, "rb") as f:
            reader = png.Reader(f)
            width, height, data, info = reader.read()
            self.original_image = Image.from_rgb_rows(rows=data, has_alpha=True)

    @property
    def cache_dir(self):
        if self._cache_dir is None:
            if 'TMPDIR' in os.environ:
                self._cache_dir = os.environ['TMPDIR']
            else:
                self._cache_dir = '/tmp'
        return self._cache_dir

    @property
    def intensity_map(self):
        def to_bw(pixel):
            intensity = pixel.col.posterize(self.color_scale)
            return Color.grey(intensity)
        if self._intensity_map is None:
            self._intensity_map = self.original_image.transform(to_bw)
        return self._intensity_map

    def _try_to_load_image(self):
        """Download the image if needed, then load it in memory"""
        self.filename = f"dpsri_70km_{self.image_time.year}{self.image_time.month:02d}{self.image_time.day:02d}{self.image_time.hour:02d}{self.image_time.minute:02d}0000dBR.dpsri.png"
        self.filepath = f"{self.cache_dir}/{self.filename}"
        try:
            self._read_image_from_cache()
        except (FileNotFoundError, EOFError):
            self._download_image_to_cache()
            self._read_image_from_cache()

    def load_image(self, when=None):
        """get the latest available image, try to look back in 5 minutes steps if needed"""
        self.image_time  = self.round_to_previous_5_min( when if when is not None else datetime.datetime.fromtimestamp( time.time()) )
        max_tries = 3
        while max_tries > 0:
            try:
                self._try_to_load_image()
                return
            except urllib.error.HTTPError as e:
                if e.code == 403:  # 403 is returned when the image is not yet available
                    self.image_time -= datetime.timedelta(minutes=5)  # Try 5 minutes before
                    max_tries -= 1
                else:
                    raise RuntimeError(f"Unable to download the rain areas image: the server returned a unexpected status code {e.code}: {e.reason}")
        raise RuntimeError("Unable to download the rain areas image")

    def location_is_inside_map(self, location):
        """Return True if the given Location (latitude, longitude) is
        inside the map area, and False otherwise"""
        if location.lat > self.top_left.lat:
            return False
        if location.lat < self.bottom_right.lat:
            return False
        if location.lon < self.top_left.lon:
            return False
        if location.lon > self.bottom_right.lon:
            return False
        return True

    def _interpolate(self, xa, ya, xb, yb, x):
        """linear interpolation"""
        return ya + (yb - ya) / (xb - xa) * (x - xa)

    def location_to_pixel(self, location):
        """Take a Location(latitude,logintude) and return the
        corresponding Pixel location in the image map"""
        if not self.location_is_inside_map(location):
            raise Exception('location is outside of covered area')
        return Pixel(
            i = round(self._interpolate(self.top_left.lon, 0, self.bottom_right.lon, self.intensity_map.width - 1, location.lon)),
            j = round(self._interpolate(self.top_left.lat, 0, self.bottom_right.lat, self.intensity_map.height - 1, location.lat)),
        )

    def pixel_to_location(self, pixel):
        """Take a Pixel and return the corresponding
        Location(latitude, longitude) by using a linear
        interpolation"""
        return Location(
            lon = self._interpolate(0, self.top_left.lon, self.intensity_map.width - 1, self.bottom_right.lon, pixel.i),
            lat = self._interpolate(0, self.top_left.lat, self.intensity_map.height - 1, self.bottom_right.lat, pixel.j),
        )

    def intensity_at(self, location, d=0):
        """Returns the rain intensity (int from 0 to 31) at the given
        Location(latitude,logitude).

        If d is 0, consider this exact location only; otherwise also
        consider neighbours pixels at distance d onthe left, d on the
        right, d above, and d below."""
        pixel = self.location_to_pixel(location)
        if d == 0:
            return self.intensity_map.get_pixel(pixel).col.g

        # averaging around pixel's neighbours
        count = 0
        intensity = 0
        box = self.intensity_map.box_around(pixel, d)
        for pn in self.intensity_map.iter_rectangle_area(box):
            count += 1
            intensity += pn.col.g
        intensity /= count
        return intensity

    def save_intensity_map(self, file_path, location=None, color=YELLOW, d=0):
        """save the intensity map to a PNG file, optionally, draw the
        location as a dot or square. The intensity is scaled from
        0..31 to 0..255"""
        pixel = self.location_to_pixel(location)

        def brighten(pixel):
            intensity = self.intensity_map.get_pixel(pixel).col.g
            grey_level = round(self._interpolate(0, 0, 31, 255, intensity))
            return Color.grey(grey_level)
        output_image = self.intensity_map.transform(brighten)
        if (d == 0):
            output_image.set_color_at(pixel.i, pixel.j, color)  # draw a dot
        else:
            box = output_image.box_around(pixel, d)
            output_image.draw_box(box, color)
        png.from_array(output_image.to_rgb_rows(), mode='RGB').save(file_path)

    @property
    def blobs(self):
        if self._blobs is None:
            self._blobs = BlobFinder(self.intensity_map).blobs
        return self._blobs

    def grep_blobs(self, f):
        """returns all blobs satisfying f(blob)==True, where f() is a
        function taking a list of Pixel as argument and returing True
        or False"""
        for blob in self.blobs:
            if f(blob):
                yield blob

    def remove_blobs(self, max_size=1):
        """removes all blobs with a size equal or less than max_size
        and less. Used to remove noise on the radar image"""
        leavers = [b for b in self.grep_blobs(lambda b: len(b) <= max_size)]
        for noise in leavers:
            for pixel in noise:
                self.original_image.set_color_at(pixel.i, pixel.j, BLACK)
                self.intensity_map.set_color_at(pixel.i, pixel.j, BLACK)
            self.blobs.remove(noise)

    def nearest_rain_location(self, location):
        """returns the rain spot location that is the nearest to this
        location"""
        loc_pixel = self.location_to_pixel(location)
        min_distance = None
        rain_pixel = None
        for b in self.blobs:
            for p in b:
                d = loc_pixel.distance_to(p)
                if min_distance is None or d < min_distance:
                    min_distance = d
                    rain_pixel = p
        if min_distance is None:
            return None
        rain_location = self.pixel_to_location(rain_pixel)
        return rain_location
