__author__ = "Altertech Group, https://www.altertech.com/"
__copyright__ = "Copyright (C) 2018 Altertech Group"
__license__ = "Apache License 2.0"
__version__ = "0.0.1"

import importlib
import logging


class WBLocation(object):

    def __init__(self):
        self.city_id = None
        self.lat = None
        self.lon = None
        self.city = None
        self.country = None


class Engine(object):
    """
    Class options (should be set manually)

        key: API key
        lang: language (provider specific)
        units: si (metrics, default) or us (imperial)
        timeout: provider request timeout (sec, default: 5)

    """

    def __init__(self, **kwargs):
        """
        Args:
           provider: provider module

        Raises:
            ModuleNotFoundError: weather provider module not found
            Exception: other errors
        """
        self.provider = None
        self.key = None
        self.lang = None
        self.location = WBLocation()
        self.units = 'si'
        self.timeout = 5
        if 'provider' in kwargs: self.set_provider(kwargs['provider'])

    def set_location(self, **kwargs):
        """Set location to get weather info for

        Args:
            city_id: city numeric ID
            lat: latitude
            lon: longitude
            city: city
            country: country

        Either city ID or lat/lon or city/country should be specified. Location
        variables priority is as listed in help. Note: some providers may not
        support certain location types.
        """
        self.location.city_id = kwargs.get('city_id')
        self.location.lat = kwargs.get('lat')
        self.location.lon = kwargs.get('lon')
        self.location.city = kwargs.get('city')
        self.location.country = kwargs.get('country')

    def set_provider(self, provider):
        """Set weather provider

        Args:
            provider: provider module

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ModuleNotFoundError: weather provider module not found
            Exception: other errors
        """
        try:
            provider_mod = importlib.import_module(
                'weatherbroker.providers.%s' % provider)
        except:
            self._log_error(
                'unable to import weather provider, module %s' % provider)
            return False
        try:
            self.provider = provider_mod.WeatherProvider()
        except:
            self._log_error('unable to init weather provider, module %s' % \
                    provider)
            return False
        self._log_debug('provider set: %s' % provider)
        return True

    def get_current(self):
        """Get current weather

        Returns JSON array with fields:

            time: unix timestamp
            lat: latitude
            lon: longitude
            clouds (%)
            temp: temperature
            hum: humidity (%)
            pres: pressure
            wind_spd: wind speed
            wind_deg: wind degree
            vis: visibility
            dewp: dew point
            uv: UV index
            icon: icon code (provider specific)
            description: human readable weather description
            precip_type: precip type
            precip_prob: precip probability (%)
            precip_int: precip intensity
            sunrise: HH:mm
            sunset: HH:mm

        Raises:
            provider exceptions
        """
        return self.provider.get_current(self.key, self.location, self.units,
                                         self.lang, self.timeout)

    def get_forecast(self, **kwargs):
        """Get weather forecast

        Not implemented (YET)
        """
        return None

    # internal functions

    @staticmethod
    def _log_debug(msg):
        logging.debug('weatherbroker: %s' % msg)

    @staticmethod
    def _log_error(msg, raise_exception=True):
        logging.error('weatherbroker: %s' % msg)
        if raise_exception: raise Exception(msg)
