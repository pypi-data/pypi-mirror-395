import os
from typer import Typer, Context, Argument, Option, echo, secho, confirm


def read_version():
    directory = os.path.dirname(__file__)
    with open(os.path.join(directory, "VERSION"), "r") as version_file:
        version = version_file.readline().strip()
        return version


__version__ = read_version()


def get_version_string():
    return f"unknown-cli/{__version__}"
