import time
import requests
import logging
from pathlib import Path
from ..utils import abort
from subprocess import Popen
import psutil
from  urllib.parse import quote_plus
from typer import echo, secho, Typer
from ..utils import set_url_handler

log = logging.getLogger(__name__)

UNREAL_EDITOR = r"s:\sn2-main\UE\Engine\Binaries\Win64\UnrealEditor.exe s:\sn2-main\UE\Subnautica2\Subnautica2.uproject"
EDITOR_URL = "http://127.0.0.1:8082"

app = Typer()

def ensure_editor_running():
    for proc in psutil.process_iter():
        if "UnrealEditor" in proc.name():
            return
    echo(f"Running editor: {UNREAL_EDITOR}")
    Popen(UNREAL_EDITOR, shell=True)
    time.sleep(3.0)
    echo("Checking for response...")
    n = 0
    num_tries = 10
    while n < num_tries:
        try:
            url = f"http://127.0.0.1:8082/"
            resp = requests.get(url)
            return
        except:
            time.sleep(1.0)
    abort("Could not start editor.")


@app.command()
def diff(first, second):
    """
    Diff two .uasset files in the editor.
    """
    ensure_editor_running()
    try:
        first_file = Path(first)
        second_file = Path(second)
        if not first_file.is_file() or not second_file.is_file():
            abort(f"{first} or {second} not found")
        secho(f"Diffing the following files:\n  {first}\n  {second}", bold=True)

        # with open("c:\\temp\\out.log", "w") as f:
        #     f.write(f"Diffing the following files:\n  {first}\n  {second}")
        left = quote_plus(first)
        right = quote_plus(second)
        left = first.replace("#", "%23")
        url = f"{EDITOR_URL}/diff?left={left}&right={right}"
        echo(url)
        resp = requests.get(url)
        print(resp.text)
    except Exception as e:
        raise
        # with open("c:\\temp\\out.log", "w") as f:
        #     f.write(str(e))

@app.command()
def asset(name):
    """
    Open an asset in a running editor or spawn an editor
    """
    ensure_editor_running()
    p = Path(name)
    if p.is_file():
        asset_name = p.stem
    else:
        asset_name = p.name
    print(f"Getting {asset_name}...")
    resp = requests.get(f"{EDITOR_URL}/asset/{asset_name}")
    print(resp.text)
    time.sleep(5.0)

@app.command()
def handler():
    """
    Set the URL handler
    """
    set_url_handler(True)
