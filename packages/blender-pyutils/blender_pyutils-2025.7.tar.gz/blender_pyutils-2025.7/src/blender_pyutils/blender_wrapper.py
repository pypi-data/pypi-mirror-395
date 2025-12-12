#!/usr/bin/env python3
"""Invoke the Blender executable."""

import contextlib
import functools
import logging
import pathlib
import shutil
import subprocess
import tempfile
import textwrap
import tomllib

import tomli_w
from xdg.BaseDirectory import xdg_config_home

from .common import ENCODING
from .exceptions import BlenderError, PipError, SubprocessError
from .utils import run

LOGGER = logging.getLogger(__name__)


class BlenderWrapper:
    """
    Simple wrapper around the Blender command-line executable.
    """

    def __init__(self, exe="blender", ext_dir=None):
        """
        Args:
            exe:
                The blender command to execute.

            ext_dir:
                The path to the directory with the extension to validate and
                build.
        """
        self.exe = str(exe)
        self.set_ext_dir(ext_dir=ext_dir)

    def set_ext_dir(self, ext_dir=None):
        """
        Set the extension directory.

        Args:
            path:
                The new path. If None, use the current working directory.
        """
        if ext_dir is None:
            ext_dir = pathlib.Path.cwd()
        else:
            ext_dir = pathlib.Path(ext_dir).resolve()
        self.ext_dir = ext_dir

    def run_blender(self, args, **kwargs):
        """
        Invoke blender.

        Args:
            Arguments to pass to the blender command.

        **kwargs:
            Keyword arguments passed through to subprocess.run().

        Returns:
            The return value of subprocess.run()
        """
        return run((self.exe, *args), **kwargs)

    @functools.cached_property
    def info(self):
        """
        A dict with information about Blender and its embedded Python
        environment. It contains the following keys:
            Blender version:
                The Blender version.

            Python version:
                The Python version.

            Python executable:
                The path to the Python executable.
        """
        delim = "###"
        blver = "Blender version"
        pyexe = "Python executable"
        code = textwrap.dedent(
            f"""\
            import pathlib
            import sys
            import bpy
            print(f"{blver}{delim}{{bpy.app.version_string}}")
            print(f"{pyexe}{delim}{{sys.executable}}")
            ver = sys.version_info
            print(f"Python version{delim}{{ver.major}}.{{ver.minor}}.{{ver.micro}}")
            paths = (str(pathlib.Path(p).resolve()) for p in sys.path)
            print(f"Python path{delim}{{':'.join(paths)}}")
            bpy.ops.wm.quit_blender()
            """
        )
        cmd = ["--background", "--python-expr", code]
        try:
            response = self.run_blender(cmd, stdout=subprocess.PIPE)
        except SubprocessError as err:
            raise BlenderError(
                f"Failed to determine Blender's Python version: {err}"
            ) from err
        info = {}
        for line in response.stdout.decode(ENCODING).splitlines():
            try:
                key, value = line.strip().split(delim, 1)
            except ValueError:
                continue
            value = value.strip()
            if key == pyexe:
                value = pathlib.Path(value).resolve()
            info[key] = value

        bldir = ".".join(info[blver].split(".", 2)[:2])
        info["Blender module directory"] = (
            pathlib.Path(xdg_config_home) / "blender" / bldir / "scripts/modules"
        )

        return info

    def run_python(self, args, **kwargs):
        """
        Invoke Blender's Python interpreter.

        Args:
            Arguments to pass to the python command.

        **kwargs:
            Keyword arguments passed through to subprocess.run().

        Returns:
            The return value of subprocess.run()
        """
        return run((self.info["Python executable"], *args), **kwargs)

    def validate(self):
        """
        Validate the extension.
        """
        try:
            self.run_blender(["--command", "extension", "validate"])
        except SubprocessError as err:
            raise BlenderError(f"Failed to validate the extension: {err}") from err
        LOGGER.info("The extension has been validated.")

    @contextlib.contextmanager
    def py_venv(self):
        """
        Context manager to provide a temporary Python virtual environment with
        pip using the same version as Blender's Python.

        Returns:
            A wrapper around run that invokes the virtual environments Python
            executable with the given arguments.
        """
        LOGGER.info("Creating temporary Python virtual environment.")
        with tempfile.TemporaryDirectory() as venv_dir:
            venv_dir = pathlib.Path(venv_dir)
            self.run_python(("-m", "venv", venv_dir))
            py_exe = venv_dir / "bin/python"
            LOGGER.info("Ensuring that pip is installed in the virtual environment...")
            run([py_exe, "-m", "ensurepip", "-U"])
            run([py_exe, "-m", "pip", "install", "-U", "pip"])

            def venv_run(args, **kwargs):
                run([py_exe, *args], **kwargs)

            yield venv_run

    def download_wheel_deps(self, wheels_dir="wheels"):
        """
        Download the wheels of all external dependencies to the local wheel
        directory and update the manifest to point to them.
        """
        wheels_dir = self.ext_dir / wheels_dir
        wheels_dir.mkdir(parents=True, exist_ok=True)
        req_file = self.ext_dir / "requirements.txt"
        if not req_file.exists():
            return

        with self.py_venv() as venv_run:
            LOGGER.info("Downloading wheels...")
            try:
                venv_run(
                    (
                        "-m",
                        "pip",
                        "wheel",
                        "-w",
                        wheels_dir,
                        "-r",
                        req_file,
                    )
                )
            except SubprocessError as err:
                raise PipError(f"Failed to download dependency wheels: {err}") from err

        manifest_file = self.ext_dir / "blender_manifest.toml"
        LOGGER.info("Loading %s", manifest_file)
        with manifest_file.open("rb") as handle:
            manifest = tomllib.load(handle)
        manifest["wheels"] = sorted(
            str(p.relative_to(manifest_file.parent)) for p in wheels_dir.glob("*.whl")
        )

        # Write the updated manifest to a temporary file to avoid truncating the
        # original on error. The temporary file is moved into place on
        # success.
        manifest_tmp_file = manifest_file.with_suffix(".tmp.toml")
        with manifest_tmp_file.open("wb") as handle:
            tomli_w.dump(manifest, handle)
        LOGGER.info("Saving updated wheels to %s", manifest_file)
        shutil.move(manifest_tmp_file, manifest_file)

    def build(self):
        """
        Build the extension (i.e. the .zip file).
        """
        try:
            self.run_blender(["--command", "extension", "build"])
        except subprocess.CalledProcessError as err:
            raise BlenderError(f"Failed to build the extension: {err}") from err
        LOGGER.info("The extension has been built.")

    def pip(self, args, path=None, uv=False):
        """
        Manage Python packages in Blender's module directory with pip or uv.

        Args:
            args:
                Arguments to pass through to the pip command.

            path:
                The target directory. If None, the default location will be
                used.

            uv:
                If True, use "uv pip" instead of pip.
        """
        if path is None:
            path = self.info["Blender module directory"]
        else:
            path = pathlib.Path(path).resolve()
        LOGGER.info("Pip target directory: %s", path)
        with self.py_venv() as venv_run:
            if uv:
                LOGGER.info("Installing uv in virtual environment.")
                venv_run(("-m", "pip", "install", "-U", "uv"))
                cmd = ("uv", "pip")
            else:
                cmd = ("pip",)
            try:
                venv_run(("-m", *cmd, *args, "--target", path))
            except subprocess.CalledProcessError as err:
                raise PipError(f"Failed to run pip command: {err}") from err
