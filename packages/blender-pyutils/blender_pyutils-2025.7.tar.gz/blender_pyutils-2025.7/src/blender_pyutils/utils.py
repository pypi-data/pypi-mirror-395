#!/usr/bin/env python3
"""Utility functions."""

import logging
import subprocess

from .exceptions import SubprocessError

LOGGER = logging.getLogger(__name__)


def run(cmd, **kwargs):
    """
    Run a command with subprocess.run.

    Args:
        cmd:
            The command to run.

        **kwargs:
            Keyword arguments passed through to subprocess.run().

    Returns:
        The return value of subprocess.run().
    """
    cmd = [str(w) for w in cmd]
    LOGGER.debug("Running command: %s", cmd)
    kwargs["check"] = kwargs.get("check", True)
    # pylint: disable=subprocess-run-check
    try:
        return subprocess.run(cmd, **kwargs)
    except subprocess.CalledProcessError as err:
        raise SubprocessError(err) from err


def semantic_ver_to_cp(version):
    """
    Convert a semantic Python version (e.g. 3.13.7) to a "cp" version (e.g. cp313).

    Args:
        version:
            The semantic version string.

    Returns:
        The "cp" version string.
    """
    return f"cp{''.join(version.split('.')[:2])}"
