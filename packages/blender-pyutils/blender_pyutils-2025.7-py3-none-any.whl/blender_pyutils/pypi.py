#!/usr/bin/env python3
"""Retrieve metadata from PiPI."""

import json
from urllib.error import URLError
from urllib.request import urlopen

from .exceptions import BlenderPythonUtilsError


def get_pypi_metadata(pkg):
    """
    Get the parse JSON metadata for a PyPI package.

    Args:
        pkg:
            the PyPI package name.

    Returns:
        The parsed metadata.
    """
    url = f"https://pypi.org/pypi/{pkg}/json"
    try:
        with urlopen(url) as handle:
            return json.load(handle)
    except (URLError, json.JSONDecodeError) as err:
        raise BlenderPythonUtilsError(err) from err
