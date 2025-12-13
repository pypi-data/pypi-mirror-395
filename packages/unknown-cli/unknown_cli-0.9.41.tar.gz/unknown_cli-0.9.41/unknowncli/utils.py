#!/usr/bin/env python

from subprocess import call
import botocore.session
from datetime import datetime, timedelta
import requests
import click
import typer
import configparser
import logging
import os
import sys
import json
from jsonpath_rw import parse
import yaml
import dateutil
from typer import secho, confirm
import json
import botocore
from loguru import logger
from pathlib import Path
from P4 import P4

try:
    import winreg
except:
    winreg = None
from . import read_version

log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.WARN)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(console_handler)

log = logging.getLogger(__name__)

PERFORCE_SERVERS = {
    "": "ssl:perforce.reginald.cloud:1666",
    "europe-edge": "ssl:perforce-europe.reginald.cloud:1666",
    "asia-edge": "ssl:perforce-asia.reginald.cloud:1666"
}

P4_TRUST = "D2:CA:D9:C9:67:64:CF:21:3C:32:ED:61:3F:93:DC:64:D5:7A:AA:C7"

import socket

def get_ip_from_url(url):
    timeout = 0.1
    try:
        # Set the default timeout for the socket
        socket.setdefaulttimeout(timeout)
        # Resolve the domain to an IP
        ip = socket.gethostbyname(url)
        return ip
    except Exception as e:
        return None

def print_error(*txt):
    color_print(*txt, color="red")


def print_warn(*txt):
    color_print(*txt, color="yellow")


def print_success(*txt):
    color_print(*txt, color="green")


def color_print(*args, **kwargs):
    color = kwargs.get("color", "reset")
    for x in args:
        typer.echo(typer.style(x, fg=color))


def get_datafile(filename):
    p = Path(__file__).parent / "data" / filename
    with p.open("rt") as f:
        return f.read()


def print_tab(key, val):
    val_txt = val
    if isinstance(val, dict):
        val_txt = ", ".join([f"{k}={v}" for k, v in val.items()])
    val = typer.style(str(val_txt), bold=True)
    typer.echo("{0:20}{1}".format(key, val))


def print_table(obj):
    try:
        for k, v in obj.items():
            print_tab(k, v)
    except Exception:
        typer.echo(obj)


def dumps(obj):
    try:
        return json.dumps(obj, indent=4, sort_keys=True)
    except Exception:
        return repr(obj)


def output_pretty_json(dct, keys):
    ret = ""
    for k in keys:
        jsonpath_expr = parse(k)
        ret = [match.value for match in jsonpath_expr.find(dct)]
        lst = [""]
        if ret:
            if isinstance(ret[0], list) or isinstance(ret[0], dict):
                lst = yaml.dump(ret[0]).split("\n")
            else:
                lst = [str(ret[0])]
        print_tab(k.split(".")[-1], lst[0])
        if len(lst) > 1:
            for v in lst[1:]:
                print_tab("", v)


def find_aws_credentials(profile):
    """
    Returns the aws credentials for the specified profile.
    If no profile is passed in, returns the credentials for the currently selected profile

    Args:
        profile name

    Returns:
        Dict containing at least aws_access_key_id, aws_secret_access_key

    Raises:
        RuntimeError is no default profile or the named profile was not found

    """
    if not profile:
        access_key = None
        secret_key = None
        token = ""
        credentials = botocore.session.get_session().get_credentials()
        if credentials:
            access_key = credentials.access_key
            secret_key = credentials.secret_key
            token = getattr(credentials, "token") or ""
        if not access_key or not secret_key:
            raise RuntimeError("No Default AWS profile set")

        return {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "aws_session_token": token,
        }

    folder = os.path.join(os.path.expanduser("~"), ".aws")
    filename = os.path.join(folder, "credentials")
    cfg = configparser.ConfigParser()
    with open(filename) as fp:
        cfg.readfp(fp)
        ret = {}
        if profile not in cfg:
            raise RuntimeError("No AWS profile '%s' found in %s" % (profile, filename))
        for key in cfg[profile]:
            ret[key] = cfg[profile][key]
    return ret


def abort(reason, code=1):
    """
    exit with non-zero exit code and write reason for error to stderr.
    If we are outside a typer context and exception will be raised instead
    """
    ctx = click.get_current_context(silent=True)
    if not ctx:
        raise Exception(f"Abnormal Termination: {reason}")

    if ctx.obj and ctx.obj.output == "json":
        ret = {"success": False, "exit_code": code, "message": str(reason)}
        typer.echo(json.dumps(ret))
    else:
        typer.echo(typer.style(str(reason), fg="red"), file=sys.stderr)
    sys.exit(code)


def out(txt, **kw):
    ctx = click.get_current_context(silent=True)
    if ctx and ctx.obj and ctx.obj.output == "json":
        log.info(txt)
    else:
        typer.secho(txt, **kw)


def success(reason, response=None, **kw):
    ctx = click.get_current_context(silent=True)
    if not ctx:
        print(reason)

    exit_code = 0
    if ctx.obj and ctx.obj.output == "json":
        ret = {
            "success": True,
            "exit_code": exit_code,
            "message": str(reason),
            "response": response,
        }
        typer.echo(json.dumps(ret))
    else:
        if not kw:
            kw = {"fg": "white", "bold": True}
        typer.secho(str(reason), **kw)
    sys.exit(exit_code)


def check_profile(ctx):
    if not ctx.obj.client:
        abort("You have no active profile or selected profile is invalid. Run 'unknown profile add [name]'")


def fmt_date(dt: str):
    try:
        return dateutil.parser.parse(dt).strftime("%Y-%m-%d %H:%M")
    except:
        return dt

def check_version():
    """
    Check for new version on pypi every 10 minutes
    """
    try:
        version_check_file = Path("~/.unknown-cli-version").expanduser()
        check_version = True
        if version_check_file.exists():
            with version_check_file.open() as f:
                dt_txt = f.read().strip()
                try:
                    dt = dateutil.parser.parse(dt_txt)
                    if dt >= datetime.utcnow() - timedelta(minutes=10):
                        check_version = False
                except:
                    pass

        if check_version:
            contents = requests.get("https://pypi.org/pypi/unknown-cli/json").json()
            v = contents["info"]["version"]
            my_version = read_version()

            if (v != my_version):
                upgrade_cmd = "pip install unknown-cli -U"
                secho(f"\nVersion {v} of this tool is available while you are on version {my_version}.", fg="yellow")
                if confirm("(RECOMMENDED) Upgrade now?", prompt_suffix=""):
                    if call(f"{sys.executable} -m {upgrade_cmd}") != 0:
                        abort(f"Upgrade failed, please try posting this in Slack, or try running the command manually: {upgrade_cmd}")
                    secho(f"\nUpgrade successful! Please run your original request or command again.", fg="green", bold=True)
                    sys.exit(0)

                secho(f"Please upgrade this tool using: {upgrade_cmd}\n", fg="yellow", bold=True)
                return
            else:
                with version_check_file.open("w") as f:
                    f.write(f"{fmt_date(datetime.utcnow())}")
    except:
        raise

def check_p4config():
    try:
        is_changes = False
        p4 = P4()
        ignore_file = "s:\\sn2-main\\.p4ignore.txt".lower()
        p4_ports = list(PERFORCE_SERVERS.values())
        cfg = Path(p4.env('P4CONFIG'))
        if p4.ignore_file == "unset":
            return
        if p4.ignore_file.lower() != ignore_file:
            secho(f"Your p4ignore file should be set to '{ignore_file}', not '{p4.ignore_file}'.", fg="yellow")
            y = confirm(f"Would you like to change the setting in your {cfg} file?")
            if y:
                _lines = []
                lines = []
                with cfg.open() as f:
                    _lines = f.readlines()
                for l in _lines:
                    if not l.upper().startswith("P4IGNORE"):
                        lines.append(l)
                lines.append(f"P4IGNORE={ignore_file}\n")
                with cfg.open("w") as f:
                    f.writelines(lines)
                is_changes = True

        if p4.port.lower() not in p4_ports:
            secho(f"Your p4 port should be set to '{p4_ports[0]}', not '{p4.port}'.", fg="yellow")
            y = confirm(f"Would you like to change the setting in your {cfg} file?")
            if y:
                _lines = []
                lines = []
                with cfg.open() as f:
                    _lines = f.readlines()
                for l in _lines:
                    if not l.upper().startswith("P4PORT"):
                        lines.append(l)
                lines.append(f"P4PORT={p4_ports[0]}\n")
                with cfg.open("w") as f:
                    f.writelines(lines)
                is_changes = True

        if is_changes:
            secho("Your p4config file now contains the following:")
            with cfg.open() as f:
                lines = f.readlines()
                for l in lines:
                    secho(f"{l.strip()}")

            secho("\nYou're all set!", fg="green")
            exit(0)
        #secho("p4 config looks good")

    except Exception as e:
        secho(f"Exception in check_p4config: {e}", fg="yellow")

def check_p4trust():
    try:
        p4 = P4()
        ssl_connection_list = list(PERFORCE_SERVERS.values())
        p4.port = ssl_connection_list[0] # any port just to connect
        p4.connect()
        trust_line_list = p4.run_trust("-l")[0].strip().split("\n")

        for ssl_connection in ssl_connection_list:
            p4_port = ssl_connection.replace("ssl:", "")
            ip = get_ip_from_url(p4_port.split(":")[0])
            matching_trust_line = next(
                (t for t in trust_line_list if (t.startswith(p4_port) or t.startswith(ip)) and t.endswith(P4_TRUST)),
                None
            )
            if matching_trust_line:
                # Connection fingerprint is up to date; no action needed. Assume other servers are also good
                return

            secho(f"Updating trust: {ssl_connection}", fg="green")
            p4 = P4()
            p4.port = ssl_connection
            # ignore error "WARNING P4PORT IDENTIFICATION HAS CHANGED" since we're setting the trust
            p4.exception_level = 0 # 2 by default which means raise all
            p4.connect()
            p4.run_trust("-i", P4_TRUST)
    except Exception as e:
        secho(f"Exception in check_p4trust: {e}", fg="yellow")

def set_url_handler(force=False):
    exe = Path(sys.argv[0] + ".exe")
    if not exe.exists():
        abort(f"Executable {exe} not found")
    handler_name = "sn2"
    key = f"{handler_name}\\shell\\open\\command"

    add_key = force
    try:
        val = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, key)
        if not val:
            raise
    except:
        add_key = True

    if add_key:
        path = Path(__file__).parent / "set_url_handler.py"
        cmd = f"{sys.executable} \"{path.resolve()}\" {exe}"
        call(cmd)
