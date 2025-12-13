# sgrain

Tells if it's currently raining at a given latitude and longitude in
Singapore, or if there's rain nearbie. The data comes from rain radar
images at https://www.weather.gov.sg/weather-rain-area-50km/. The
images are updated every 5 minutes.


**Link to project:** https://github.com/nlannuzel/sgrain

## Package installation
From PyPI
```shell
pip3 install nlannuzel.sgrain
```

## Package usage
### With the built-in script:
```shell
LAT=1.313383
LONG=103.815203
# shows rain here:
rain-intensity-at -a $LAT -o $LONG -n
# shows distance to nearest rain spot:
nearest-rain -a $LAT -o $LONG -c $(pwd) -n 1
# shows location of nearest rain spot:
nearest-rain -a $LAT -o $LONG -c $(pwd) -n 1 -l
# shows location of nearest rain spot of significant size (size of more than 20 pixels on the rain map):
nearest-rain -a $LAT -o $LONG -c $(pwd) -n 20 -l
```
### With a custom script:
```python
#!/usr/bin/env python3

from nlannuzel.sgrain.rain import RainAreas
from nlannuzel.sgrain.geo import Location

rain = RainAreas()

# Download the latest radar image from https://www.weather.gov.sg/weather-rain-area-50km/
rain.load_image()

# https://maps.app.goo.gl/9aA7i8chryYwuhUT8
picnic_spot = Location(1.313383, 103.815203)

# Returns a number between 0 and 31
intensity = rain.intensity_at(picnic_spot)

message = f"At location {picnic_spot}, time {rain.image_time}: "
if intensity == 0:
    rain.remove_blobs(max_size = 10)
    nearest_rain = rain.nearest_rain_location(picnic_spot)
    if nearest_rain is None:
        message += "it's not raining around here."
    else:
        d = picnic_spot.distance_to(nearest_rain)
        message += f"it's not raining, but there's rain about {d:.2f}km away."
elif intensity < 10:
	message += "it's raining a little bit ({intensity}), bring a umbrella."
else:
	message += "it's raining a lot ({intensity}), cancel the picnic."
print(message)
```

### In [home-assistant](https://www.home-assistant.io/)
Log into the home-assistant box, for example by connecting to the console of the VM where HA is installed and running. Then, attach to the homeasistant container:
```shell
docker exec -ti homeassistant bash
```

You are now inside the homeassistant container. Create a new venv under /config.
```shell
cd /config
python3 -m venv python_venv
```

Install this package inside the venv
```shell
cd python_venv
./bin/pip3 install nlannuzel.sgrain
```

Verify that the module works, this command should display a number between 0 and 31:
```shell
./bin/rain-intensity-at -a 1.313383 -o 103.815203 -p 1
```

Open the home-assistant GUI in a browser. If not already done, install the File Editor add-on. Open the configuration.yaml file (`/homeassistant/configuration.yaml`), and add a section like below:
```yaml
command_line:
  - sensor:
      command: /config/venv/bin/python3 /config/venv/bin/rain-intensity-at -a LATITUDE -o LONGITUDE -p 1 -n 1
      name: rain-sensor
      unique_id: rain
      scan_interval: 300
      icon: mdi:weather-pouring
      availability: 1
      #device_class: None
      state_class: MEASUREMENT
      value_template: '{{ value | float | round(2) }}'
  - sensor:
      command: /config/venv/bin/python3 /config/venv/bin/nearest-rain -a LATITUDE -o LONGITUDE -n 10
      name: rain-sensor-distance
      unique_id: rain-distance
      scan_interval: 300
      icon: mdi:weather-pouring
      availability: 1
      device_class: distance
      unit_of_measurement: km
      state_class: MEASUREMENT
      value_template: '{{ value | float | round(2) }}'
```
Be sure to replace LATITUDE and LONGITUDE by the the actual coordinates. Finally, in the "developer tools", validate and then reload the config. You should have a new sensor available in Home Assistant.

Command line sensors are explained in HA website: https://www.home-assistant.io/integrations/command_line/
