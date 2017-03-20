import json
import os
import requests

class Client(object):

    """ basic Meraki API client """

    DEFAULT_URL = "https://dashboard.meraki.com/api"
    DEFAULT_VERSION = 'v0'

    TIMEOUT = 30

    MERAKI_APIKEY = os.environ['MERAKI_APIKEY']

    def __init__(self, api_key=MERAKI_APIKEY,
                 default_url=DEFAULT_URL,
                 version=DEFAULT_VERSION,
                 timeout=TIMEOUT,
                 endpoint=''):

        try:
            import http.client as http_client
        except ImportError:
            # Python 2
            import httplib as http_client
            http_client.HTTPConnection.debuglevel = 1 

        self.base_url = '%s/%s' % (default_url, version)
        self.api_key = api_key
        self.endpoint = endpoint
        self._session = requests.Session()

        self.headers = {
                "X-Cisco-Meraki-API-Key": self.api_key,
                "Content-Type": "application/json",
                }

    def _request(self, method, path, **kwargs):
        url = '{}{}'.format(self.base_url, path)
        response = self._session.request(method, url, headers=self.headers, timeout=self.TIMEOUT, **kwargs)
        response.raise_for_status()
        return response

    def clients(self, serial_number, timespan):
        path = '/devices/{}/clients?timespan={}'.format(serial_number, timespan)
        return self._request('GET', path).json()
