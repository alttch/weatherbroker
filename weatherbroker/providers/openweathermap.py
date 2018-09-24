__author__ = "Altertech Group, https://www.altertech.com/"
__copyright__ = "Copyright (C) 2018 Altertech Group"
__license__ = "Apache License 2.0"
__version__ = "0.0.1"
__doc__ = """
Weather provider for OpenWeatherMap API v2.5 ( https://openweathermap.org/ )
"""

import requests
import json
import datetime


class WeatherProvider(object):

    def get_current(self, key, location, units=None, lang=None, timeout=5):
        url = 'https://api.openweathermap.org/data/2.5/weather?APPID={}'.format(
            key)
        if units == 'us':
            url += '&units=imperial'
        else:
            url += '&units=metric'
        if lang:
            url += '&lang=' + lang
        if location.city_id:
            url += '&id={}'.format(location.city_id)
        elif location.lat and location.lon:
            url += '&lat={}&lon={}'.format(location.lat, location.lon)
        elif location.city and location.country:
            url += '&q={},{}'.format(location.city, location.country)
        else:
            raise Exception('no location specified')
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            try:
                err = json.loads(r.text).get('message')
            except:
                err = None
            raise Exception(err if err else 'data fetch error')
        data = json.loads(r.text)
        result = {}
        result['time'] = data.get('dt')
        result['lat'] = data.get('coord', {}).get('lat')
        result['lon'] = data.get('coord', {}).get('lon')
        result['clouds'] = data.get('clouds', {}).get('all')
        main = data.get('main', {})
        result['temp'] = main.get('temp')
        result['hum'] = main.get('humidity')
        result['pres'] = main.get('pressure')
        result['wind_spd'] = data.get('wind', {}).get('speed')
        result['wind_deg'] = data.get('wind', {}).get('deg')
        result['vis'] = data.get('visibility', 0) / 1000.0
        result['dewp'] = None
        result['uv'] = None
        weather = data.get('weather')
        if isinstance(weather, list):
            weather = weather[0]
        if not weather: weather = {}
        result['icon'] = weather.get('icon')
        result['description'] = weather.get('description')
        result['sunrise'] = self.convert_time(
            data.get('sys', {}).get('sunrise'))
        result['sunset'] = self.convert_time(data.get('sys', {}).get('sunset'))
        result['precip_type'] = None
        result['precip_prob'] = None
        result['precip_int'] = None
        return result

    @staticmethod
    def convert_time(t):
        local_dt = datetime.datetime.fromtimestamp(t)
        return '{:02}:{:02}'.format(local_dt.hour, local_dt.minute)
