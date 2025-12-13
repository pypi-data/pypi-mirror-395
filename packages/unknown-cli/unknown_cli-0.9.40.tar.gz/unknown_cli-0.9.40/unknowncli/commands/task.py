import datetime
import logging
import os
import socket
import sys
from ..utils import abort
from .project import BASE_STREAM, SUB_STREAMS
from P4 import P4, P4Exception
from typing import Optional
from subprocess import check_call

log = logging.getLogger(__name__)

from typer import echo, secho, Option, Typer, confirm, prompt
from rich.progress import Progress, MofNCompleteColumn, TimeRemainingColumn, BarColumn, SpinnerColumn, TextColumn

app = Typer()

hostname = socket.gethostname().lower()
SUBST_DRIVE = "S:"
path = f"{SUBST_DRIVE}\\sn2-main\\"
STREAM_LIST_LOWER = [s.lower() for s in list(list(SUB_STREAMS.values())[0].values())]
STREAM_LIST_STRING = "\n\t" + "\n\t".join(STREAM_LIST_LOWER)

p4 = None


def connect_p4():
    p4_conn = P4()
    try:
        p4_conn.connect()
    except Exception as e:
        abort(f"Cannot establish connection with Perforce server: {e}...")
    return p4_conn


@app.callback()
def main():
    """
    Manage task streams.

    This tool is highly opinionated and expects you to be using the //Project/SN2-Main-UE stream and be working in a workspace called <username>_<label>_sn2-main
    """
    global p4
    p4 = connect_p4()
    ret = get_current_stream()
    ignore_file = (path + ".p4ignore.txt").lower()
    if p4.ignore_file.lower() != ignore_file:
        abort(
            f"Your p4ignore file should be set to '{ignore_file}', not '{p4.ignore_file}'.\nPlease change the setting in your {p4.env('P4CONFIG')} file"
        )

    if "Stream" not in ret:
        abort("Invalid workspace. You must be working in Streams to use this tool")
    stream_name = ret["Stream"]
    parent = ret["Parent"]
    secho(f"You are currently working in stream: {stream_name}", fg="blue")
    if parent.lower() not in STREAM_LIST_LOWER and stream_name.lower() not in STREAM_LIST_LOWER:
        abort(
            f"To use this tool you must be working in a valid stream but your workspace is set to {stream_name}." +
            "\nPlease change to a relevant workspace with 'p4 set p4client=<your_valid_workspace>'" +
            "\nOr set up a workspace with 'unk project setup'."
        )


def get_task_streams(owner: str=""):
    streams_filter = f"Type=task baseParent={BASE_STREAM}" + ( f" Owner={owner}" if owner else "" )
    lst = p4.run_streams("-F", streams_filter)
    return lst


def get_current_stream():
    try:
        ret = p4.run_stream("-o")[0]
    except P4Exception as e:
        client_name = "None"
        try:
            client = get_current_client()
            client_name = client["Client"]
        except:
            pass
        abort(
            f"Unable to get a stream from your current workspace, {client_name}. Make sure you are working in the {BASE_STREAM} stream. Error: {e}"
        )
    return ret


def get_current_client():
    ret = p4.run_client("-o")[0]
    return ret


def get_clients():
    try:
        specs = p4.run_clients("-u", p4.user)
    except Exception as e:
        abort(str(e))
    ret = {}
    for s in specs:
        if "Stream" not in s:
            continue
        host = s["Host"].lower()
        if host == hostname or not host:
            ret[s["Stream"].lower()] = s
    return ret


def sync():
    s = confirm("Sync latest?")

    if not s:
        return

    secho(f"Syncing latest...")
    try:
        ret = p4.run_client("-o")[0]
        root_path = ret["Root"]
        p4.run_sync("-q", os.path.join(root_path, "..."))
    except P4Exception as e:
        print(e)


@app.command()
def create(label: str = Option(None, prompt="Task branch label")):
    """
    Create a new task branch
    """

    if not label:
        abort("Aborted.")
    # This needs to be lower() when used as the parent for the new task stream.
    # TC is case sensitive so the parent stream needs to be '//project/sn2-main-ue'. (bug TW-87208)
    # You can edit a stream if you need to change the parent to lowercase:
    #   p4 stream -o -v //project/<stream_name> > spec.txt
    #   p4 stream -i -f < spec.txt
    current_stream_lower = get_current_stream()["Stream"].lower()
    if current_stream_lower not in STREAM_LIST_LOWER:
        abort(f"You are working in stream {current_stream_lower}. Please first run 'unk task switch' to a parent stream.\nValid parent streams:{STREAM_LIST_STRING}")

    ret = p4.run_opened()
    if len(ret):
        abort("You have opened files. Please revert or submit before creating new task stream.")

    client_root = get_current_client()["Root"]
    echo(f"Syncing parent branch {client_root}\...")
    try:
        ret = p4.run_sync("-q", f"{client_root}\...")
    except P4Exception as e:
        secho(str(e), fg="yellow")
        abort("Please fix the issues above before continuing")

    d = datetime.datetime.utcnow().isoformat().split("T")[0]
    label = label.replace(" ", "_").lower()
    stream_name = f"{p4.user}-{d}-{label}"
    full_stream_name = f"//Project/{stream_name}"
    secho(f"Creating task stream {stream_name} from {current_stream_lower} ...")
    args = f"""
Stream: {full_stream_name}
Owner:  {p4.user}
Name:   {stream_name}
Parent: {current_stream_lower}
Type:   task
Description:
    Created by {p4.user}.
Options:        allsubmit unlocked toparent fromparent mergedown
ParentView:     inherit
Paths:
    share ...
"""
    p4.input = args
    ret = p4.run_stream("-i", "-t", "task")
    # print(ret[0])

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("Populating {task.description}"),
            transient=True,
            ) as progress:
            progress.add_task(description=f"{full_stream_name} ...", total=None)
            ret = p4.run_populate("-o", "-S", full_stream_name, "-r", "-d", "Initial branch")

    except P4Exception as e:
        if e.errors:
            secho(e.errors[0], fg="yellow")

    secho(f"Switching current workspace {p4.client} to {full_stream_name} ...")
    p4.run_client("-s", "-S", full_stream_name)
    ret = p4.run_client("-o")[0]
    root_path = ret["Root"]

    ret = p4.run_stream("-o")[0]
    stream_name = ret["Stream"]
    parent = ret["Parent"]

    if ret["Type"] != "task":
        abort(f"Something went wrong. Current stream {stream_name} is not a task stream")

    # update the server without syncing
    ret = p4.run_sync("-q", "-k", f"{root_path}\...")

    secho(f"You are now working in task stream {stream_name} from parent {parent}", bold=True, fg="green")


@app.command()
def switch(owned: Optional[bool] = Option(True, help="See only owned task streams")):
    """
    Lists your current task streams and lets you switch between them
    """
    stream = get_current_stream()
    old_stream_name = stream["Stream"]
    client = p4.run_client("-o")[0]
    task_streams = get_task_streams(client["Owner"] if owned else "")
    if owned and not task_streams:
        secho("You have no owned task streams. You can create one with the 'create' command.", bold=True)
        if confirm("\nDo you want to instead see other streams that you don't own?"):
            switch(owned=False)
        abort("")
    parent = None
    if stream["Type"] == "task":
        parent = stream["Parent"]
    for i, t in enumerate(task_streams):
        secho(f"{i+1} : {t['Stream']}")
    if parent:
        secho(f"0 : (Parent stream) {parent}")
    if owned:
        secho(f"99 : <See other streams, including task streams that you don't own>")

    n = prompt("\nSelect a stream to work in")
    if n is None:
        abort("No stream selected")
    try:
        n = int(n)
    except:
        abort("Aborted.")
    if parent and n == 0:
        new_stream = parent
    elif owned and n == 99:
        switch(owned=False)
        abort("")
    else:
        try:
            new_stream = task_streams[n - 1]["Stream"]
        except:
            abort("Aborted.")

    secho(f"\nSwitching to stream {new_stream}", bold=True)
    try:
        p4.run_client("-s", "-S", new_stream)
    except P4Exception as e:
        abort(e)

    secho(f"Running sync...")

    try:
        p4.run_sync("-q")
    except P4Exception as e:
        err = e.errors[0]
        if "clobber" in err:
            secho(err, fg="yellow")
            if confirm("Would you like to overwrite writable files that are not open in your workspace?"):
                p4.run_sync("-q", "-f")
                return
        secho(f"Switching back to {old_stream_name}", fg="yellow")
        p4.run_client("-s", "-S", old_stream_name)
        secho(f"Aborted. {err}", fg="red")


@app.command()
def mergedown(nosubmit: Optional[bool] = Option(False, help="Do not submit the changelist after resolving")):
    """
    Merge from parent into your current task branch
    """
    ret = p4.run_stream("-o")[0]
    stream_name = ret["Stream"]
    parent_stream = ret["Parent"]
    if ret["Type"] != "task":
        abort(f"Current stream {stream_name} is not a task stream")

    ret = p4.run_client("-o")[0]
    root_path = ret["Root"]
    client = ret["Client"]

    ret = p4.run_opened()
    for r in ret:
        if r["change"] == "default":
            abort("Your default changelist must be empty before merging down from main.")

    merge_response = []

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            transient=True,
            ) as progress:
            progress.add_task(description=f"Merging files from {parent_stream} to {stream_name}/...", total=None)
            try:
                cmd = ["-Af", "-S", stream_name, "-r", f"{stream_name}/..."]
                merge_response = p4.run_merge(*cmd)
            except P4Exception as e:
                echo("\n")
                if e.errors:
                    secho(e.errors[0], fg="red")
                if e.warnings:
                    secho(e.warnings[0], fg="yellow")
                if "already integrated" in str(e):
                    secho(f"Your task stream is already up to date with {parent_stream}", fg="green")
                return

    except P4Exception as e:
        if e.errors:
            secho(e.errors[0], fg="yellow")

    num_files = len(merge_response)
    resolves = []
    with Progress(
        "[green]Resolving files...",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        MofNCompleteColumn(),
        "{task.description}",
        refresh_per_second=10,  # bit slower updates
    ) as progress:
        task = progress.add_task("", total=num_files)
        for resp in merge_response:
            depotFile = resp["depotFile"]
            try:
                ret = p4.run_resolve("-f", "-am", "-as", depotFile)
                if ret:
                    resolves.append(ret)
            except P4Exception as e:
                echo(str(e))
            progress.update(task, advance=1, description="..." + depotFile[-50:])
    try:
        ret = p4.run_fstat("-Olhp", "-Rco", "-e", "default", os.path.join(root_path, "..."))
    except P4Exception as e:
        echo(str(e))

    if not ret:
        abort("Your task stream is up to date.")

    unresolved = []
    for r in ret:
        if "unresolved" in r:
            unresolved.append(r)
            secho(f"  {r['clientFile']} ... conflict", fg="yellow")
        else:
            secho(f"  {r['clientFile']} ... ok", fg="green")

    if unresolved:
        secho(
            f"\nThere are conflicting files where you have changed files which have also been changed in {parent_stream}.\nYou can force overwrite these files in your task stream or resolve yourself via p4v."
        )
        overwrite_all = False
        overwrite_none = False
        num_skipped = 0
        for i, r in enumerate(unresolved):
            y = None
            if not overwrite_all and not overwrite_none:
                y = prompt(f"[{i+1}/{len(unresolved)}] Overwrite {r['clientFile']} [Yes/No/None/All] ").upper()
            if y not in ("YES", "Y", "NO", "N", "NONE", "ALL"):
                abort(
                    f"Please resolve remaining files in p4v. You can use this description: Automatically merge {parent_stream} to {stream_name}"
                )
            if y in ("ALL"):
                overwrite_none = False
                overwrite_all = True
            elif y in ("NONE"):
                overwrite_none = True
                overwrite_all = False

            if y in ("Y", "YES") or overwrite_all:
                ret = p4.run_resolve("-f", "-at", f"{r['clientFile']}")
            if y in ("N", "NO") or overwrite_none:
                secho(f"Skipping {r['clientFile']} ...")
                num_skipped += 1

        if num_skipped:
            abort(
                f"Please resolve remaining files in p4v. You can use this description: Automatically merge {parent_stream} to {stream_name}"
            )

        secho("All Unresolved files have been overwritten by parent stream")

    try:
        ret = p4.run_fstat("-Olhp", "-Rco", "-e", "default", os.path.join(root_path, "..."))
    except P4Exception as e:
        echo(str(e))
    filelist = ""
    for r in ret:
        if "unresolved" in r:
            abort("There are still unresolved files in your pending changelist. Please resolve them in p4v")
        filelist += f"    {r['depotFile']}\n"
    mr = ""
    if unresolved:
        mr = f"{len(unresolved)} unresolvable files were overwritten."

    if not nosubmit:
        txt = f"""
Change:	new
Client:	{client}
User:	{p4.user}

Description:
    Automatically merge {parent_stream} to {stream_name}. {mr}
Files:
{filelist}"""
        p4.input = txt
        p4.run_submit("-i")

        try:
            ret = p4.run_resolve("-f", "-am", "-as", os.path.join(root_path, "..."))
        except P4Exception as e:
            if "no file(s) to resolve" not in str(e):
                raise
        try:
            ret = p4.run_fstat("-Olhp", "-Rco", "-e", "default", os.path.join(root_path, "..."))
        except P4Exception as e:
            empty_changelist_msg_list = [
                "not opened on this client.",
                "not opened in that changelist",
                "no such file(s)."
            ]
            if any([msg for msg in empty_changelist_msg_list if msg in str(e)]):
                secho(f"Your task stream is now up to date with {parent_stream}", fg="green")
                return
            else:
                echo(str(e))
        if not ret:
            secho(f"Your task stream is now up to date with {parent_stream}", fg="green")
        else:
            abort("Something is amiss. Your task stream is not up to date after the merge. Take a look at p4v")
    else:
        echo(
            f"Your merge changelist is now ready for submitting. Use this description: 'Automatically merge {parent_stream} to {stream_name}. {mr}"
        )


@app.command()
def copyup(force: Optional[bool] = Option(False, help="Use p4 copy force arguments: -f -F")):
    """
    Finish the task and copy into the parent stream
    """
    ret = p4.run_opened()
    if ret:
        abort("There are unsubmitted files in your workspace")

    ## p4 copy -Af -S //Project/jonb-2023-03-03-plugin_functional_tests //Project/SN2-Main/...
    ret = get_current_stream()
    stream_name = ret["Stream"]
    parent = ret["Parent"]
    if ret["Type"] != "task":
        abort(f"Current stream {stream_name} is not a task stream")

    secho(f"Switching to parent stream {parent} ...", fg="blue")
    p4.run_client("-s", "-S", parent)

    p4.run_sync("-q")
    copy_target = f"{ret['baseParent']}/..."
    echo(f"Performing copy from {stream_name} to {copy_target}")
    copy_args = [ "-Af", "-S", stream_name, copy_target ]
    force_copy_args = [ "-f", "-F" ]
    try:
        copy_ret = p4.run_copy(*(force_copy_args if force else []), *copy_args)
    except P4Exception as e:
        if "up-to-date" in str(e):
            secho(f"Nothing to do. Parent {parent} is identical to task stream {stream_name}", fg="green")
            return
        elif "No such file(s)" in str(e):
            secho(f"Nothing to do. No changes were made yet in task stream {stream_name}", fg="green")
            return
        elif not force and "cannot 'copy' over outstanding 'merge' changes" in str(e):
            # Occurs when mergedown is not complete but it can be the case when P4 has issues
            # merging rename/move+edit and the fix is to force merge which causes "outstanding...".
            secho(f"\n{str(e)}", fg="yellow")
            if confirm("Try a force copy? (Do this if you're sure that you're done with mergedowns)"):
                copy_ret = p4.run_copy(*force_copy_args, *copy_args)
            else:
                secho("No action taken.")
                return
        else:
            raise
    else:
        echo("Adding files...")
        for r in copy_ret:
            echo(f"  {r['fromFile']} -> {r['depotFile']}")

    secho(f"You can now submit your changelist to {parent} in p4v", fg="green")


@app.command()
def delete(current: Optional[bool] = Option(False, help="Delete the current task stream")):
    """
    Permanently delete a named task stream or your current one"""

    ret = p4.run_stream("-o")[0]
    current_stream_name = ret["Stream"]
    parent = ret["Parent"]
    root_path = get_current_client()["Root"]

    if current:
        if ret["Type"] != "task":
            abort(f"Current stream {current_stream_name} is not a task stream")
        streams_to_delete = [current_stream_name]
    else:
        client = p4.run_client("-o")[0]
        client_owner = client["Owner"]
        task_streams = get_task_streams(client_owner)

        if not task_streams:
            abort("You have no task streams.")

        for i, t in enumerate(task_streams):
            secho(f"{i+1} : {t['Stream']}")
        secho(f"ALL : [Delete all your task streams]")
        n = prompt("\nSelect a stream to delete")
        streams_to_delete = []
        if n == "ALL":
            streams_to_delete = [t['Stream'] for t in task_streams]
        else:
            try:
                n = int(n)
            except:
                abort("Aborted.")
            if n <= 0 or n > len(task_streams):
                abort("Aborted.")
            stream_name = task_streams[n - 1]["Stream"]
            streams_to_delete = [stream_name]

    if streams_to_delete:
        streams_to_delete_string = "\n\t" + "\n\t".join(
            [f"(**YOUR CURRENT TASK STREAM**) {x}" if current_stream_name == x else x for x in streams_to_delete]
        )
        if not confirm(
            f"==============\nTask stream(s) to delete:{streams_to_delete_string}" +
            "\nAre you sure you want to delete these task stream(s)?"
        ):
            abort("Aborted.")

        if current_stream_name in streams_to_delete:
            if not parent:
                abort(f"Please run 'unk task switch' to a parent stream before continuing:{STREAM_LIST_STRING}")
            secho(f"Switching to {parent} before deleting the task stream ...")
            p4.run_client("-s", "-S", parent)
            ret = p4.run_sync("-q", f"{root_path}\...")

        for stream_name in streams_to_delete:
            cmd = [sys.executable, "s:/sn2-main/BuildScripts/trigger_task_stream_deletion.py", stream_name]
            secho(f"Deleting task stream {stream_name} ...")

            check_call(cmd)
        secho("Request to delete selected streams has been sent. It might take a few minutes to finish", fg="green")
    else:
        abort("Aborted")
    ret = p4.run_sync("-q", "-k", f"{root_path}\...")
    # sync()
