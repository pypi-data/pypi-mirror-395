#!/usr/bin/env python3
"""Utility script for validating and packaging Blender extensions."""

import argparse
import getpass
import json
import logging
import os
import pathlib
import shlex
import sys
import textwrap

from xdg.BaseDirectory import xdg_config_home

from .blender_wrapper import BlenderWrapper
from .common import ENCODING
from .exceptions import BlenderPythonUtilsError
from .pypi import get_pypi_metadata
from .utils import run, semantic_ver_to_cp

LOGGER = logging.getLogger(__name__)


def configure_logging(level=logging.INFO):
    """
    Configure logging.

    Args:
        level:
            The logging level.
    """
    logging.basicConfig(
        style="{",
        format="[{asctime}] {levelname} {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )


def _mask_home_dir(info):
    """
    Mask the user's home directory for example output. This is used for
    generating the README without revealing any information about the user's
    home directory path.
    """
    # Generic replacements for the home, XDG config and current working
    # directories.
    gen_home = pathlib.Path("/home/user")
    gen_conf = gen_home / ".config"
    gen_cwd = pathlib.Path("/tmp/cwd")

    home = os.environ["HOME"]
    conf = xdg_config_home
    cwd = str(pathlib.Path.cwd())

    replacements = {home: str(gen_home), conf: str(gen_conf), cwd: str(gen_cwd)}

    # Include the resolved paths.
    for old, new in list(replacements.items()):
        replacements[str(pathlib.Path(old).resolve())] = new

    # As an extra precaution, replace the user's name as well.
    replacements[getpass.getuser()] = "user"

    for key, value in info.items():
        vtype = type(value)
        value = str(value)
        for old, new in replacements.items():
            value = value.replace(old, new)
        info[key] = vtype(value)
    return info


class CommandRunner:
    """
    Run selected commands. The only real purpose of this class is to avoid
    redundant subprocess calls to retrieve Blender information.
    """

    def __init__(self):
        self.blender = BlenderWrapper()

    def _get_info(self, example=False):
        """
        Get Blender information.

        Args:
            example:
                If True, mask the user's home directory.

        Returns:
            The dict of Blender information.
        """
        info = self.blender.info
        if example:
            info = _mask_home_dir(info)
        return info

    def build(self, pargs):
        """
        Validate and build an extension. If a requirements.txt file is found in the
        extension directory then the wheels for its dependencies will be downloaded
        to the wheels directory and the manifest will be updated to include them.
        """
        bld = self.blender
        bld.set_ext_dir(ext_dir=pargs.path)
        bld.download_wheel_deps()
        bld.validate()
        bld.build()

    def env(self, pargs):
        """
        Create a soureable shell configuration file that will set the Python
        path environment variable to match Blender's Python path. This will
        allow scripts and editors to detect Blender's internal Python modules.
        """
        info = self._get_info(example=pargs.example)
        path = info["Python path"]
        content = textwrap.dedent(
            f"""\
        #!/usr/bin/sh
        export PYTHONPATH={shlex.quote(path)}
        """
        )
        path = pargs.out
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=ENCODING)
            return
        print(content)

    def info(self, pargs):
        """
        Print Blender information.
        """
        info = self._get_info(example=pargs.example)
        if pargs.json:
            print(json.dumps(info, indent=2, sort_keys=True, default=str))
            return
        for key, value in sorted(info.items()):
            print(f"{key}: {value}")

    def pip(self, pargs):
        """
        Install Python packages to Blender's module directory. Additional
        arguments as passed through to pip.
        """
        self.blender.pip(pargs.pip_args, path=pargs.path, uv=pargs.uv)

    def venv(self, pargs):
        """
        Create a Python virtual environment with the PyPI bpy package installed.
        This will try to match the version to the currently installed version of
        Blender but it will default to the latest version if the installed
        version cannot be found. The created virtual environment will also use
        the version of Python required by the bpy package. Officially, Blender
        only supports a single version of Python with each release but packagers
        sometimes patch Blender to work with different versions.
        """
        pkg = "bpy"
        info = self._get_info()
        pypi_data = get_pypi_metadata(pkg)
        local_pyver = semantic_ver_to_cp(info["Python version"])
        blver = info["Blender version"].split(maxsplit=1)[0]
        try:
            release = pypi_data["releases"][blver][0]
        except KeyError:
            latest_blver = pypi_data["info"]["version"]
            LOGGER.warning(
                "No PyPI bpy package for local Blender version %s: using version %s",
                blver,
                latest_blver,
            )
            blver = latest_blver
            release = pypi_data["releases"][blver][0]
        req_pyver = release["python_version"]
        if local_pyver != req_pyver:
            LOGGER.warning(
                "The installed version of Blender uses Python %s "
                "but the bpy package requires Python %s",
                local_pyver,
                req_pyver,
            )

        path = pargs.path.resolve()
        LOGGER.info("Creating virtual environment with bpy at %s", path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.blender.py_venv() as venv_run:
            venv_run(["-m", "pip", "install", "-U", "uv"])
            venv_run(
                ["-m", "uv", "venv", "--allow-existing", f"--python={req_pyver}", path]
            )

        pyexe = path / "bin/python3"
        for cmd in (
            ("-m", "ensurepip"),
            ("-m", "pip", "install", "-U", "pip"),
            ("-m", "pip", "install", "-U", "uv"),
            (
                "-m",
                "uv",
                "pip",
                "install",
                "-U",
                f"bpy=={blver}",
                "--extra-index-url",
                "https://download.blender.org/pypi/",
            ),
        ):
            run([pyexe, *cmd])


def main(args=None):
    """
    Main function.

    Args:
        args:
            Passed through to ArgumentParser.parse_args().
    """
    cmd_runner = CommandRunner()

    # --------------------------- common arguments --------------------------- #

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--example",
        action="store_true",
        help="Mask user name in home directory paths for example output.",
    )

    # ----------------------------- main parser ------------------------------ #

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(required=True)

    # -------------------------------- build --------------------------------- #

    parser_build = subparsers.add_parser("build", description=cmd_runner.build.__doc__)
    parser_build.add_argument(
        "-p",
        "--path",
        type=pathlib.Path,
        help=(
            "The path to the extension's root directory. "
            "If not given, the current working directory is assumed."
        ),
    )
    parser_build.set_defaults(func=cmd_runner.build)

    # --------------------------------- env ---------------------------------- #

    parser_env = subparsers.add_parser(
        "env", description=cmd_runner.env.__doc__, parents=[parent_parser]
    )
    parser_env.add_argument(
        "-o",
        "--out",
        type=pathlib.Path,
        help="The output path. If not specified, the file will be printed to STDOUT.",
    )
    parser_env.set_defaults(func=cmd_runner.env)

    # --------------------------------- info --------------------------------- #

    parser_info = subparsers.add_parser(
        "info", description=cmd_runner.info.__doc__, parents=[parent_parser]
    )
    parser_info.add_argument(
        "-j", "--json", action="store_true", help="Use JSON output format."
    )
    parser_info.set_defaults(func=cmd_runner.info)

    # --------------------------------- pip ---------------------------------- #

    parser_pip = subparsers.add_parser("pip", description=cmd_runner.pip.__doc__)
    parser_pip.add_argument(
        "--path",
        type=pathlib.Path,
        help=(
            "Installation directory for Python packages. "
            "If not given, the default Blender module directory will be used. "
            'Use the "info" command to show the path to the module directory.'
        ),
    )
    parser_pip.add_argument(
        "--uv", action="store_true", help='Use "uv pip" instead of pip.'
    )
    parser_pip.add_argument(
        "pip_args",
        nargs="+",
        help=(
            "Arguments to pass through to pip. "
            'Precede these arguments with "--" if any of them begin with "-".'
        ),
        metavar="<PIP ARG>",
    )
    parser_pip.set_defaults(func=cmd_runner.pip)

    # --------------------------------- venv --------------------------------- #

    parser_venv = subparsers.add_parser("venv", description=cmd_runner.venv.__doc__)
    parser_venv.add_argument(
        "path", type=pathlib.Path, help="The virtual environment path."
    )
    parser_venv.set_defaults(func=cmd_runner.venv)

    # ------------------------------------------------------------------------ #

    pargs = parser.parse_args(args)
    pargs.func(pargs)


def run_main(*args, **kwargs):
    """
    Run the main function with exception handling.

    Args:
        *args:
            Positional arguments passed through to main().

        **kwargs:
            Keyword arguments passed through to main().
    """
    configure_logging()
    try:
        main(*args, **kwargs)
    except BlenderPythonUtilsError as err:
        sys.exit(err)


if __name__ == "__main__":
    run_main()
