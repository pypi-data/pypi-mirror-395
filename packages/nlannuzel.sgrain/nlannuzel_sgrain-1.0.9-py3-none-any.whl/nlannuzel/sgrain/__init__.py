import datetime
import argparse
from nlannuzel.sgrain.rain import RainAreas
from nlannuzel.sgrain.geo import Location


def rain_intensity_at():
    parser = argparse.ArgumentParser(
        prog='rain-intensity-at',
        description="Tells if it's raining at the given location")
    parser.add_argument('-a', '--latitude', required=True, help='latitude in decimal')
    parser.add_argument('-o', '--longitude', required=True, help='longitude in decimal')
    parser.add_argument('-c', '--cachedir', help='directory that holds downloaded images')
    parser.add_argument('-O', '--output', help='output file')
    parser.add_argument('-p', '--squaresize', help='square area to consider around location (in pixels)')
    parser.add_argument('-Y', '--year', help='year to consider instead of current date/time' )
    parser.add_argument('-M', '--month', help='month to consider instead of current date/time' )
    parser.add_argument('-D', '--day', help='day to consider instead of current date/time' )
    parser.add_argument('-H', '--hour', help='hour to consider instead of current date/time' )
    parser.add_argument('-m', '--minute', help='minute to consider instead of current date/time. Will be rounded down to 5 min.' )
    parser.add_argument('-n', '--filter-noise', help='remove small pixel blobs (noise) in the radar image.' )
    args = parser.parse_args()

    rain = RainAreas(cache_dir=args.cachedir if args.cachedir else None)

    dt = None
    if args.year:
        dt = datetime.datetime(
            year=int(args.year),
            month=int(args.month),
            day=int(args.day),
            hour=int(args.hour),
            minute=int(args.minute))
    rain.load_image(dt)

    location = Location(
        lat = float(args.latitude),
        lon = float(args.longitude))
    if args.filter_noise:
        rain.remove_blobs(int(args.filter_noise))
    squaresize = int(args.squaresize) if args.squaresize else 0
    if args.output:
        rain.save_intensity_map(file_path=args.output, location=location, d=squaresize)
    print(rain.intensity_at(location, squaresize))


def nearest_rain_spot():
    parser = argparse.ArgumentParser(
        prog='nearest-rain-spot',
        description="Tells where, or how far, is the nearest rain spot")
    parser.add_argument('-a', '--latitude', required=True, help='latitude in decimal')
    parser.add_argument('-o', '--longitude', required=True, help='longitude in decimal')
    parser.add_argument('-c', '--cachedir', help='directory that holds downloaded images')
    parser.add_argument('-O', '--output', help='output file')
    parser.add_argument('-Y', '--year', help='year to consider instead of current date/time' )
    parser.add_argument('-M', '--month', help='month to consider instead of current date/time' )
    parser.add_argument('-D', '--day', help='day to consider instead of current date/time' )
    parser.add_argument('-H', '--hour', help='hour to consider instead of current date/time' )
    parser.add_argument('-m', '--minute', help='minute to consider instead of current date/time. Will be rounded down to 5 min.' )
    parser.add_argument('-n', '--filter-noise', help='remove small pixel blobs (noise) in the radar image.' )
    parser.add_argument('-l', '--location', action='store_true', help='report coordinates instead of distance' )
    args = parser.parse_args()

    rain = RainAreas(cache_dir=args.cachedir if args.cachedir else None)

    dt = None
    if args.year:
        dt = datetime.datetime(
            year=int(args.year),
            month=int(args.month),
            day=int(args.day),
            hour=int(args.hour),
            minute=int(args.minute))
    rain.load_image(dt)

    location = Location(
        lat = float(args.latitude),
        lon = float(args.longitude))
    if args.filter_noise:
        rain.remove_blobs(int(args.filter_noise))
    nearest_rain = rain.nearest_rain_location(location)
    if nearest_rain is None:
        print(100.0)   # home assistant doesn't seem to understand "NaN" or "inf"
        return
    if args.location:
        print(f"{nearest_rain.lat},{nearest_rain.lon}")
        return
    print(location.distance_to(nearest_rain))
