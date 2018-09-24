# weatherbroker
Weather broker for Python

License: Apache License 2.0

Warning: Refer to weather provider license about caching, storing and
redistributing weather information.

Displays current weather condition in unified JSON format:

* time: unix timestamp
* lat: latitude
* lon: longitude
* clouds (%)
* temp: temperature
* hum: humidity (%)
* press: pressure
* wind_spd: wind speed
* wind_deg: wind degree
* vis: visibility
* dewp: dew point
* uv: UV index
* icon: icon code (provider specific)
* description: human readable weather description
* percip_type: percip type
* percip_prob: percip probability (%)
* percip_int: percip intensity
* sunrise: HH:mm
* sunset: HH:mm

Weather forecast is not implemented (yet).

The module contains providers for:

 * DarkSky: https://darksky.net/
 
Usage example:
 
```python
from weatherbroker import WeatherEngine

w = WeatherEngine()
w.set_provider('darksky')
w.key = 'my secret api key'
w.set_location(lat=50.08804, lon=14.42076)

# below sets the same location 
# w.set_location(city_id=3067696)
# w.set_location(city='Prague', country='CZ')
# w.lang = 'cs'

print(w.get_current())

```

(c) 2018 Altertech Group, https://www.altertech.com/
