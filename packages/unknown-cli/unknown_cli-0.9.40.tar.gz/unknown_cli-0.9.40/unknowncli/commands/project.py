import time
import sys, os
import requests
import logging
import socket
from tabulate import tabulate
from pathlib import Path
from pprint import pprint
from ..utils import dumps, abort, get_datafile, PERFORCE_SERVERS, P4_TRUST
from subprocess import check_call, call, check_output
from P4 import P4, P4Exception
import shutil

log = logging.getLogger(__name__)

from typer import Context, launch, echo, secho, Option, Typer, confirm, prompt, style, progressbar

app = Typer()

hostname = socket.gethostname().lower()
SUBST_DRIVE = "S:"
BASE_STREAM = "//Project/SN2-Main"
STREAMS = {
    "sn2-main": "//project/sn2-main-ue"
}
SUB_STREAMS = {
    "//project/sn2-main": {
        "Project"               : "//project/sn2-main-ue",
        "Project+RawRecommended": "//project/sn2-main-ue-raw-content",
        "Project+RawAll"        : "//project/sn2-main-ue-raw",
        "Everything"            : "//project/sn2-main",
        "Staging"               : "//project/sn2-staging",
    }
}

is_windows = os.name == "nt"
DEFAULT_FOLDER = "C:\\Work" if is_windows else "~/Work"
MIN_FREE_GB = 200


def get_clientspecs(p4):
    try:
        specs = p4.run_clients("-u", p4.user)
    except Exception as e:
        abort(str(e))
    ret = {}
    for s in specs:
        host = s["Host"].lower()
        # skip workspaces with no stream
        if "Stream" not in s:
            continue
        stream = s["Stream"].lower()
        if stream not in ret:
            ret[stream] = []
        if host == hostname or not host:
            ret[stream].append(s)
    return ret


def get_sync_stats(p4, force=False):
    # gah, p4 wrapper just returns text
    if force:
        ret = p4.run_sync("-N", "-f")
    else:
        ret = p4.run_sync("-N")
    lst = ret[0].split("=")
    ret = {
        "files": {"added": 0, "updated": 0, "deleted": 0, "total": 0},
        "mbytes": {"added": 0, "updated": 0, "total": 0},
    }
    lst2 = [int(l) for l in lst[1].split(",")[0].split("/")]
    ret["files"]["added"] = lst2[0]
    ret["files"]["updated"] = lst2[1]
    ret["files"]["deleted"] = lst2[2]
    ret["files"]["total"] = sum(lst2)

    lst2 = [int(l) // 1024 // 1024 for l in lst[-1].split(",")[0].split("/")]
    ret["mbytes"]["added"] = lst2[0]
    ret["mbytes"]["updated"] = lst2[1]
    ret["mbytes"]["total"] = sum(lst2)

    return ret


@app.command()
def setup(
    perforce_path: str = Option(DEFAULT_FOLDER, prompt="Folder to keep your workspace"),
    force: bool = Option(False, help="Forcefully overwrite an existing setup"),
):
    """
    Creates the virtual drive and perforce workspaces from
    //Project/[stream] -> s:/[stream]

    Perforce Setup: https://www.notion.so/unknownworlds/How-To-Version-Control-Setup-0fc38f99d29a4558ac32b24bdfc6904f

    Unreal Game Sync: https://www.notion.so/unknownworlds/How-To-Setup-Unreal-Game-Sync-59cc3348cdde449d8fdc7f39ee60c8b3
    """
    p4 = P4()
    if not p4.port or p4.port == "perforce:1666" or force:
        host = prompt("Perforce connection string (ssl:[url]:1666):", default=p4.port)
        lst = host.split(":")
        if len(lst) == 1:
            host = f"ssl:{host}:1666"
        elif len(lst) != 3 or lst[0] != "ssl" or not lst[2].isdigit():
            abort("Perforce connection string is mangled. Expecting ssl:[url]:[port]")

        username = prompt("Perforce username", default=p4.user)

        p4.port = host
        p4.user = username

    sys.stdout.write(f"Establishing connection to perforce server {p4.port}... ")
    sys.stdout.flush()
    try:
        p4.connect()
    except Exception as e:
        abort(f"Cannot establish connection with Perforce server: {e}...")

    try:
        all_client_specs = p4.run_clients("-u", p4.user)
    except Exception as e:
        if "P4PASSWD" in str(e):
            passwd = prompt(f"\nPlease enter perforce password for {p4.user}", hide_input=True)
            try:
                p4.password = passwd
                p4.run_login()
                all_client_specs = p4.run_clients("-u", p4.user)
            except Exception as e:
                abort(str(e))
        else:
            abort(f"Error fetching workspaces from Perforce: {e}")

    secho("OK", fg="green")
    if " " in perforce_path:
        abort("Workspace path cannot include spaces (sorry)")

    perforce_path = Path(perforce_path).expanduser()
    perforce_drive = perforce_path.drive or "C:"
    _, _, free = shutil.disk_usage(perforce_drive)
    free_gb = free // 1024 // 1024 // 1024
    if free_gb < MIN_FREE_GB:
        secho(
            f"You need to have at least {MIN_FREE_GB} GB free disk space but you have only {free_gb} GB on drive {perforce_path.drive}",
            fg="yellow",
        )
        y = confirm("Are you sure you want to continue?")
        if not y:
            abort("Aborted")

    config_filename = "p4config.txt"

    # ignore_path = Path("~").expanduser() / ".p4ignore.txt"
    # echo(f"Saving "+str(ignore_path))
    # with ignore_path.open("w") as f:
    #     ignore_contents = get_datafile(".p4ignore.txt")
    #     f.write(ignore_contents)
    ignore_file = "s:\\sn2-main\\.p4ignore.txt".lower()

    echo(f"Saving {config_filename}")
    config_file = Path("~").expanduser() / config_filename
    contents = {}
    if config_file.exists():
        with config_file.open("r") as f:
            contents = {ll[0]: ll[1] for ll in [l.strip().split("=") for l in f.readlines()]}

    contents["P4PORT"] = p4.port
    contents["P4USER"] = p4.user
    contents["P4IGNORE"] = str(ignore_file)

    with config_file.open("w") as f:
        for k, v in contents.items():
            f.write(f"{k}={v}\n")

    subst_cmd = f"subst {SUBST_DRIVE} {perforce_path}"
    if not perforce_path.exists():
        ret = prompt(f"Path {perforce_path} not found. Would you like to create it [y/n]?")
        if ret == "y":
            perforce_path.mkdir(parents=True, exist_ok=True)
        else:
            abort("Path not found")

    if is_windows:
        s_path = Path(SUBST_DRIVE)
        if s_path.exists():
            s_path_resolve = str(s_path.resolve()).lower()
            if s_path_resolve == str(perforce_path).lower():
                secho(f"{SUBST_DRIVE} virtual drive is already set up and pointing to {s_path_resolve}.", fg="green")
            elif not force:
                abort(f"{SUBST_DRIVE} virtual drive is pointing to another folder: {s_path_resolve}.")

        if not s_path.exists() or force:
            try:
                call(f"subst {SUBST_DRIVE} /D")
            except:
                pass
            check_call(subst_cmd)

        try:
            import winreg
            echo(f"Adding Virtual Drive {SUBST_DRIVE} -> {perforce_path} to startup")
            h = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
            winreg.SetValueEx(h, "Perforce Work Drive", 0, winreg.REG_SZ, subst_cmd)
        except:
            secho("Access denied setting subst registry key. Running elevated process...")
            path = Path(__file__).parent.parent / "set_registry_keys.py"
            cmd = f"{sys.executable} \"{path.resolve()}\" \"{subst_cmd}\""
            check_call(cmd)

        h = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\perforce\\environment")
        winreg.SetValueEx(h, "P4CONFIG", 0, winreg.REG_SZ, str(config_file))

        if not perforce_path.exists():
            abort(f"Failed to add subst for {SUBST_DRIVE}")
        root_path = SUBST_DRIVE
    else:
        root_path = str(perforce_path)

    computer_name = ""
    while not computer_name:
        input = prompt(
            "What would you like to call this computer in Perforce (work, home, laptop, etc)", default="work"
        )
        if not input.isalpha() or input != input.lower():
            secho("Computer name must be lowercase with no symbols or numbers", fg="red")
        else:
            computer_name = input
    for stream_name, stream in STREAMS.items():
        mapping = os.path.join(root_path, os.sep if root_path.endswith(":") else "", stream_name)
        found = False
        for r in all_client_specs:
            root = r["Root"].lower()
            client = r["client"]
            host = r["Host"].lower()
            if root == mapping.lower() and host == hostname:
                if force:
                    secho(f"Deleting workspace {client} which was mapped to {root}", fg="yellow")
                    try:
                        p4.run_client("-d", client)
                    except Exception as e:
                        abort(e)
                else:
                    secho(f"Workspace {client} already mapped to {root}", fg="green")
                    found = True
        if not found:
            client_spec = f"{p4.user}_{computer_name}_{stream_name}"
            echo(f"Creating workspace {client_spec} -> {mapping}")
            client = p4.fetch_client(client_spec)
            client["Root"] = mapping
            client["Stream"] = stream
            p4.save_client(client)
            p = Path(mapping)
            p.mkdir(parents=True, exist_ok=True)
            # set the client so all other operations like 'unk project stream' are ready for use
            check_call(f"p4 set P4CLIENT={client_spec}")

    secho("\nProject setup has been completed. Please sync your workspace through p4v.", fg="green")
    secho("\n  * Unreal Game Sync documentation: https://www.notion.so/unknownworlds/How-To-Setup-Unreal-Game-Sync-59cc3348cdde449d8fdc7f39ee60c8b3")
    secho("  * If you are located in Europe or Asia please run `unk project region` to access the appropriate edge server.")
    secho("  * If you require Raw content please run `unk project stream` to switch to the appropriate virtual stream")
    # sync_workspaces()


@app.command()
def sync(stream: str = Option(""), force: bool = Option(False)):
    """
    Runs a full Perforce sync of the Project streams. Intented for initial project sync
    """
    sync_workspaces(stream, force)

@app.command()
def stream():
    """
    Switch your current workspace to a virtual stream of your choosing
    """
    p4 = P4()
    p4.connect()
    # set the client for the user if not already set
    if not p4.env("P4CLIENT"):
        specs = get_clientspecs(p4)
        if not specs:
            secho("Please check if you skipped a step or post this error on Slack", fg="red")
            abort("No workspaces found, you need to first run 'unk project setup'")
        client_spec = ""
        main_stream = next(iter(STREAMS.values()), None)
        if main_stream and main_stream in specs.keys():
            # prefer the main stream client because users start with this if nothing is set
            client_spec = specs[main_stream][0]["client"]
        else:
            # otherwise choose the first available client
            client_spec = next(iter(specs.values()))[0]["client"]
        secho(f"Setting workspace {client_spec}", bold=True)
        check_call(f"p4 set P4CLIENT={client_spec}")
        p4.client = client_spec
    client = p4.run_client("-o")[0]
    stream = p4.run_stream("-o")[0]
    current_stream_name = client["Stream"].lower()
    secho(f"Your workspace {p4.client} is currently on stream {current_stream_name}")
    parent_stream = stream.get("Parent", "").lower()
    if not parent_stream or parent_stream == "none":
        parent_stream = current_stream_name
    if parent_stream not in SUB_STREAMS:
        abort(f"Your workspace has an invalid parent stream '{parent_stream}'")
    secho(f"Which stream from parent {parent_stream} would you like to use?\n")
    i = 1
    for desc, stream_name in SUB_STREAMS[parent_stream].items():
        secho(f"{i}\t{desc}\t{stream_name}")
        i += 1
    n = prompt("\nSelect a stream to work in")
    try:
        n = int(n)-1
        vals = list(SUB_STREAMS[parent_stream].values())
        if n < 0 or n > len(vals):
            raise Exception
        new_stream = vals[n]
    except:
        raise
        abort("Aborted.")
    secho(f"\nSwitching to stream {new_stream}", bold=True)
    try:
        p4.run_client("-s", "-S", new_stream)
    except P4Exception as e:
        abort(e)

from enum import Enum
class Region(str, Enum):
    USA = "USA"
    Europe = "Europe"
    Asia = "Asia"

@app.command()
def region():
    """
    Migrate your perforce connection to one of the edge regions and move all your workspaces to that server.
    https://www.notion.so/unknownworlds/How-To-Migrating-an-existing-workspace-b5adb9ef4a3e4e32a4b7b212df1e70e0#d90ecb2206ae4c2490c4752ed0ce89ea
    """
    p4 = P4()
    p4.connect()
    name = ""
    for k, v in PERFORCE_SERVERS.items():
        if v.lower() == p4.port.lower():
            name = k
    if name:
        secho(f"You are currently on edge perforce server {name} ({p4.port})")
    else:
        secho(f"You are currently on the primary perforce server {p4.port}")
    regions = ", ".join([k for k in PERFORCE_SERVERS.keys() if k])
    region = prompt(f"Select region to migrate to (usa, {regions})")
    region = region.lower()
    my_specs = get_clientspecs(p4)
    current_port = p4.port
    if region == "usa":
        region = ""
    try:
        p4_port = PERFORCE_SERVERS[region]
    except:
        abort("Please select a legitimate server")
    us_p4_port = PERFORCE_SERVERS[""]
    #if p4.port != us_p4_port:
    #    abort(f"You can only migrate your connection from {us_p4_port}. You are currently on {current_port}")

    cfg = Path(p4.env('P4CONFIG'))

    #if p4.port.lower() == p4_port:
    #    secho("You are already connected to the requested region", fg="green")
    #    return
    my_workspaces = get_workspaces_from_all_servers()

    secho(f"Logging you into server {p4_port}...")
    try:
        check_call(f"p4 -p {p4_port} login -a")
    except Exception as e:
        abort("Could not log you in. Wrong password?")
    secho(f"Adding trust for server...")
    check_call(f"p4 -p {p4_port} trust -i {P4_TRUST}")
    #
    for spec in my_workspaces:
        server_id = spec.get("ServerID", "")
        client_name = spec["client"]
        prev_server = PERFORCE_SERVERS.get(server_id)
        if server_id not in PERFORCE_SERVERS:
            secho(f"Server '{server_id}' in workspace {client_name} not found", fg="yellow")
        if prev_server == p4_port:
            secho(f"Workspace {client_name} already on server {server_id}", fg="yellow")
            continue
        secho(f"Moving {client_name} from {prev_server} to {p4_port}...")
        try:
            cmd = f"p4 -p {p4_port} reload -c {client_name} -p {prev_server}"
            echo(f"Running command '{cmd}'...")
            check_output(cmd)
        except Exception as e:
            secho(f"Error moving {client_name}.", fg="red")
    secho(f"Updating your perforce config file {str(cfg)}...")
    _lines = []
    lines = []
    with cfg.open() as f:
        _lines = f.readlines()
    for l in _lines:
        if not l.upper().startswith("P4PORT"):
            lines.append(l)
    lines.append(f"P4PORT={p4_port}\n")
    with cfg.open("w") as f:
        f.writelines(lines)

    secho(f"\nMigration completed. Make sure Rider, Unreal Game Sync, Perforce Client and the Unreal Editor are all configured to use connection string: {p4_port}", fg="green", bold=True)

def sync_workspaces(stream="", force=False):
    files_completed = 0
    old_files_completed = 0
    files_remaining = 0
    num_files = 0

    p4 = P4()
    p4.connect()
    specs = get_clientspecs(p4)
    stream = stream.lower()

    for stream_name, stream in STREAMS.items():
        if stream in stream and stream not in specs:
            abort(f"Stream {stream} has no workspace. Please run init")

    if not stream:
        options = style("Available streams:\n", bold=True)
        for i, s in enumerate(STREAMS.values(), 1):
            folder = specs[s.lower()][0]["Root"]
            options += f"  {i}: {s} -> {folder}\n"
        options += f"  0: ALL\n"
        options += "\n\nWhich Stream would you like to sync?"
        ret = prompt(options)
        if ret.isnumeric():
            ret = int(ret)
            for i, s in enumerate(STREAMS.values(), 1):
                if ret == i:
                    stream = s
                    break
            else:
                if ret != 0:
                    abort("No stream selected")
        else:
            abort("No stream selected")

    for stream_name, s in STREAMS.items():
        if stream not in s:
            continue
        folder = specs[s.lower()][0]["Root"]
        echo(f"Syncing {s} -> {folder}...")
        p4.client = specs[s][0]["client"]
        stats = get_sync_stats(p4, force)
        num_files = stats["files"]["total"]
        batch_size = 1000
        threads = 8

        if force:
            secho(f"Refetching all files in {s} (this will take a while)...")
            ret = p4.run_sync("--parallel", threads, "-f")
            num_files = get_sync_stats(p4)["files"]["total"]

        if num_files > 0:
            echo(f"Syncing {num_files} files...")
            with progressbar(length=num_files, show_pos=True) as progress:
                for i in range(num_files // batch_size):
                    p4.run_sync("-m", batch_size, "--parallel", threads, "-q")
                    progress.update(batch_size)
            p4.run_sync()
            files_remaining = get_sync_stats(p4)["files"]["total"]
            if files_remaining == 0:
                secho(f"{s} is now up-to-date", fg="green")
            else:
                abort(f"{s} is not up to date after sync. Please sync manually")
        else:
            secho(f"{s} is already up-to-date", fg="green")


@app.command()
def workspaces(selective: bool = Option(True), sn2: bool = Option(False), all: bool = Option(False)):
    """
    Shows a list of your perforce workspaces
    """

    from operator import itemgetter
    ret = get_workspaces_from_all_servers(all)
    for r in ret:
        r["Owner"] = r["Owner"].lower()
    ret.sort(key=itemgetter("Owner"))
    rows = []
    for r in ret:
        if "Stream" not in r:
            continue
        if sn2 and "sn2-main" not in r["Stream"].lower():
            continue
        if selective and (r["Owner"] == "build" or r["client"].startswith("swarm")):
            continue
        h = r["Host"]
        if h.lower() == socket.gethostname().lower():
            h = style(h, bold=True)
        else:
            h = style(h, fg="red")
        rows.append([r["Owner"], r["client"], r["Stream"], r["Root"][:32], h, r.get("ServerID")])
    tbl = tabulate(rows, headers=["Owner", "Client", "Stream", "Root", "Host", "Server"])
    echo(tbl)

def get_workspaces_from_all_servers(all=False):
    ret = []
    for k, v in PERFORCE_SERVERS.items():
        p4 = P4()
        p4.port = v
        p4.connect()
        args = ("-u", p4.user) if not all else ()
        secho(f"Querying {p4.port}...")
        try:
            ret.extend(p4.run_clients(*args))
        except P4Exception as e:
            passwd = prompt(f"\nPlease enter perforce password for {p4.user}", hide_input=True)
            p4.password = passwd
            try:
                p4.run_login()
                ret.extend(p4.run_clients(*args))
            except P4Exception as e:
                abort(e)
    return ret