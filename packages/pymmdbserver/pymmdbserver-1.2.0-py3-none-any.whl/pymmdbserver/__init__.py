from __future__ import annotations

import argparse
import json
import sys

from .api import PyMmdbServer

__all__ = ['PyMmdbServer']


def main() -> None:
    parser = argparse.ArgumentParser(description='Query a thing.')
    parser.add_argument('--url', default="https://ip.circl.lu/", type=str, required=False, help='URL of the instance.')
    parser.add_argument('ip', default=None, nargs="?", help='IP address to query. If not set, returns the geolookup information from the client IP.')
    args = parser.parse_args()

    client = PyMmdbServer(args.url)

    if not client.is_up:
        print(f'Unable to reach {client.root_url}. Is the server up?')
        sys.exit(1)
    if args.ip:
        response = client.geolookup(args.ip)
    else:
        response = client.my_geolookup()
    print(json.dumps(response, indent=2))
