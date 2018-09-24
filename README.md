# weatherbroker
Weather broker for Python

License: Apache License 2.0

Warning: Refer to weather provider license about caching, storing and
redistributing weather information.

Provides current weather information as an unified dict:

* time: monitoring time, unix timestamp
* lat: latitude
* lon: longitude
* clouds (%)
* temp: temperature
* hum: humidity (%)
* pres: pressure
* wind_spd: wind speed
* wind_deg: wind degree
* vis: visibility
* dewp: dew point
* uv: UV index
* icon: icon code (provider specific)
* description: human readable weather description
* precip_type: precip type
* precip_prob: precip probability (%)
* precip_int: precip intensity
* sunrise: HH:mm
* sunset: HH:mm

Weather forecast is not implemented (yet).

Note: some providers may not provide certain data fields, in this case they are
set to None.

The module contains providers for:

 * weatherbit: https://www.weatherbit.io/
 * darksky: https://darksky.net/
 
Usage example:
 
```python
from weatherbroker import WeatherEngine

w = WeatherEngine()
w.set_provider('darksky')
w.key = 'my secret api key'
w.set_location(lat=50.08804, lon=14.42076)

# the code below sets the same location, but DarkSky supports only coordinates,
# so we use them instead

# w.set_location(city_id=3067696)
# w.set_location(city='Prague', country='CZ')

# w.lang = 'cs'

print(w.get_current())
```

(c) 2018 Altertech Group, https://www.altertech.com/
