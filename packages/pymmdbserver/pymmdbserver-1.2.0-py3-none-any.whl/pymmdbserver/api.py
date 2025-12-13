#!/usr/bin/env python3

from __future__ import annotations

from importlib.metadata import version
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import urljoin, urlparse

import requests


class PyMmdbServer():

    def __init__(self, root_url: str="https://ip.circl.lu/", useragent: str | None=None,
                 *, proxies: dict[str, str] | None=None):
        '''Query a specific instance.

        :param root_url: URL of the instance to query, defaults to https://ip.circl.lu/
        :param useragent: The User Agent used by requests to run the HTTP requests against the instance.
        :param proxies: The proxies to use to connect to theinstance - More details: https://requests.readthedocs.io/en/latest/user/advanced/#proxies
        '''
        self.root_url = root_url

        if not urlparse(self.root_url).scheme:
            self.root_url = 'http://' + self.root_url
        if not self.root_url.endswith('/'):
            self.root_url += '/'
        self.session = requests.session()
        self.session.headers['user-agent'] = useragent if useragent else f'PyMmdbServer / {version("pymmdbserver")}'
        if proxies:
            self.session.proxies.update(proxies)

    @property
    def is_up(self) -> bool:
        '''Test if the given instance is accessible'''
        try:
            r = self.session.head(self.root_url)
        except requests.exceptions.ConnectionError:
            return False
        # the server returns a 405 (not allowed), which means it's up.
        return r.status_code in (200, 405)

    def my_geolookup(self) -> list[dict[str, Any]]:
        '''Get the geolocation of the IP address of the client making the request.

        :return: A dictionary with the geolocation information.
        '''
        r = self.session.get(self.root_url)
        return r.json()

    def geolookup(self, ip: str) -> list[dict[str, Any]]:
        '''Get the geolocation of a specific IP address.

        :param ip: The IP address to look up.
        :return: A dictionary with the geolocation information.
        '''
        r = self.session.get(urljoin(self.root_url, str(PurePosixPath('geolookup', ip))))
        return r.json()
