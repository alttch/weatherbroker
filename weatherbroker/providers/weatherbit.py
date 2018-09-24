__author__ = "Altertech Group, https://www.altertech.com/"
__copyright__ = "Copyright (C) 2018 Altertech Group"
__license__ = "Apache License 2.0"
__version__ = "0.0.1"
__doc__ = """
Weather provider for WeatherBit API v2.0 ( https://www.weatherbit.io/ )
"""

import requests
import json
import datetime
import calendar


class WeatherProvider(object):

    def get_current(self, key, location, units=None, lang=None, timeout=5):
        url = 'https://api.weatherbit.io/v2.0/current?key={}'.format(key)
        if units == 'us':
            url += '&units=I'
        if lang:
            url += '&lang=' + lang
        if location.city_id:
            url += '&city_id={}'.format(location.city_id)
        elif location.lat and location.lon:
            url += '&lat={}&lon={}'.format(location.lat, location.lon)
        elif location.city and location.country:
            url += '&city={}&country={}'.format(location.city, location.country)
        else:
            raise Exception('no location specified')
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            try:
                err = json.loads(r.text).get('error')
            except:
                err = None
            raise Exception(err if err else 'data fetch error')
        data = json.loads(r.text)
        result = {}
        if not 'data' in data:
            raise Exception('no data available')
        c = data['data'][0]
        result['time'] = int(c.get('ts'))
        result['lat'] = float(c.get('lat'))
        result['lon'] = float(c.get('lon'))
        result['clouds'] = c.get('clouds')
        result['temp'] = c.get('temp')
        result['hum'] = c.get('rh')
        result['pres'] = c.get('pres')
        result['wind_spd'] = c.get('wind_spd')
        result['wind_deg'] = c.get('wind_dir')
        result['vis'] = c.get('vis')
        result['dewp'] = c.get('dewpt')
        result['uv'] = c.get('uv')
        result['icon'] = c.get('weather', {}).get('icon')
        result['description'] = c.get('weather', {}).get('description')
        result['sunrise'] = self.convert_time(c.get('sunrise'))
        result['sunset'] = self.convert_time(c.get('sunset'))
        result['precip_type'] = None
        result['precip_prob'] = None
        result['precip_int'] = c.get('precip')
        if not result['precip_int']:
            result['precip_int'] = 0.0
        return result

    @staticmethod
    def convert_time(t):
        try:
            h, m = t.split(':')
            h = int(h)
            m = int(m)
        except:
            return None
        t = datetime.datetime.now().replace(hour=h, minute=m)
        timestamp = calendar.timegm(t.timetuple())
        local_dt = datetime.datetime.fromtimestamp(timestamp)
        return '{:02}:{:02}'.format(local_dt.hour, local_dt.minute)
