# Python client and module for MMDB Server

This library offers a simple interface to query [MMDB Server](https://github.com/adulau/mmdb-server) using Python.
It provides both a command-line interface and a library.

## Installation

```bash
pip install pymmdbserver
```

## Usage

### Command line

You can use the `mmdbserver` command to query the MMDB Server from the command line.:

```bash
usage: mmdbserver [-h] [--url URL] [ip]

Query a thing.

positional arguments:
  ip          IP address to query. If not set, returns the geolookup information from the client IP.

options:
  -h, --help  show this help message and exit
  --url URL   URL of the instance.
```

### Library

See [API Reference](https://pymmdbserver.readthedocs.io/en/latest/api_reference.html)
