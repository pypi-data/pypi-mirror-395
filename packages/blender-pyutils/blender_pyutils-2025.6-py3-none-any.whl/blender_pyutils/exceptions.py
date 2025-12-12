#!/usr/bin/env python
"""Custom exceptions."""


class BlenderPythonUtilsError(Exception):
    """Base class for custom exceptions raised by this module."""


class SubprocessError(BlenderPythonUtilsError):
    """Errors raised by subprocess calls."""


class BlenderError(SubprocessError):
    """Errors raised when invoking the Blender executable."""


class PipError(SubprocessError):
    """Errors raised when invoking pip."""
