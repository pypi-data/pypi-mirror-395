import os, sys
import logging
import pathlib
import requests
from .utils import console_handler, abort, check_version, check_p4config, check_p4trust, set_url_handler
from pathlib import Path
from . import read_version

log = logging.getLogger(__name__)
help_string = """A utility for managing Unknown projects"""
help_string += f" (unknown-cli/{read_version()})\n"

base_path = pathlib.Path(os.path.dirname(__file__))
commands_folder = base_path / "commands"

from typer import Typer, Context, Argument, Option, echo, secho, confirm, prompt

help_string += """
    This tool handles the initial setup of Perforce Projects and helps you work with task streams.
    It creates workspaces for you according to naming conventions and sets up a virtual drive.
    Please run the 'project setup' command to get started.
    """

check_version()
app = Typer(add_completion=False)

@app.callback(context_settings={"allow_extra_args": True, "ignore_unknown_options": True}, no_args_is_help=True, help=help_string)
def cli(
    ctx: Context,
    #verbose: str = Option(None, "-v", "--verbose", help="Verbose logging: info or debug"),
    #output: str = Option("text", "-o", "--output", help="Output text or json"),
):
    # by default we log out to console WARN and higher but can view info with -v
    #if verbose:
    #    console_handler.setLevel(getattr(logging, verbose.upper()))
    set_url_handler()
check_p4config()
check_p4trust()


from unknowncli.commands import preflight
from unknowncli.commands import project
from unknowncli.commands import task
from unknowncli.commands import unreal

app.command(name="preflight", help="Manage preflighting changelists")(preflight.main)
app.add_typer(project.app, name="project", help="Manage initial project setup")
app.add_typer(task.app, name="task", help="Manage perforce task streams")
app.add_typer(unreal.app, name="unreal", help="Unreal commands")
