#!/usr/bin/env python3
"""Utility functions."""


import logging
import subprocess

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
    return subprocess.run(cmd, **kwargs)
