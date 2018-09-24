__author__ = "Altertech Group, https://www.altertech.com/"
__copyright__ = "Copyright (C) 2018 Altertech Group"
__license__ = "Apache License 2.0"
__version__ = "0.0.1"
__doc__ = """
Weather provider for DarkSky ( https://darksky.net/ )
"""

import requests
import json
import time


class WeatherProvider(object):

    def get_current(self, key, location, units=None, lang=None, timeout=5):
        url ='https://api.darksky.net/forecast/' + \
            '{key}/{lat},{lon},{t}?exclude=hourly,daily,flags'.format(
                    key=key,
                    lat=location.lat,
                    lon=location.lon,
                    t=int(time.time())
                    )
        if lang:
            url += '&lang=' + lang
        if units:
            url += '&units=' + units
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            try:
                err = json.loads(r.text).get('error')
            except:
                err = None
            raise Exception(err if err else 'data fetch error')
        data = json.loads(r.text)
        result = {}
        if not 'currently' in data:
            raise Exception('no data available')
        c = data['currently']
        result['time'] = c.get('time')
        result['lat'] = data.get('latitude')
        result['lon'] = data.get('longitude')
        result['clouds'] = c.get('cloudCover', -0.01) * 100
        result['temp'] = c.get('temperature')
        result['hum'] = c.get('humidity')
        result['pres'] = c.get('pressure')
        result['wind_spd'] = c.get('windSpeed')
        result['wind_deg'] = c.get('windBearing')
        result['vis'] = c.get('visibility')
        result['dewp'] = c.get('dewPoint')
        result['uv'] = c.get('uvIndex')
        result['icon'] = c.get('icon')
        result['description'] = c.get('summary')
        result['sunrise'] = None
        result['sunset'] = None
        result['precip_type'] = c.get('precipType')
        result['precip_prob'] = c.get('precipProbability')
        result['precip_int'] = c.get('precipIntensity')
        return result
