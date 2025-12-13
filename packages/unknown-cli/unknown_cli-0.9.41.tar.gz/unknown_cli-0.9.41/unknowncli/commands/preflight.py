import json
import logging
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from ..utils import abort
from collections import OrderedDict
from datetime import datetime
from enum import Enum
from P4 import P4, P4Exception
from psutil import process_iter
from shutil import which
from subprocess import CalledProcessError, check_output
from typing import List, Optional
from typer import confirm, Option, prompt, secho
from rich.live import Live
from rich.progress import Progress, BarColumn, MofNCompleteColumn, SpinnerColumn, TaskProgressColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.spinner import Spinner
from rich.style import Style

log = logging.getLogger(__name__)
p4 = None
p4_client = ""
DEFAULT_CHANGE = "default"
PREFLIGHT_TAG = "#preflight"
SCRIPTS_DIR = "BuildScripts"


class CustomToolDef:
    name = ""
    command = ""
    arguments = ""
    add_to_context = True
    add_separator_before = False
    def __init__(self, name: str, command: str, arguments: str, add_to_context: bool=True, add_separator_before: bool=False) -> None:
        self.name = name
        self.command = command
        self.arguments = arguments
        self.add_to_context = add_to_context
        self.add_separator_before = add_separator_before


class CustomToolFolder:
    name = ""
    custom_tool_def_list = []
    add_to_context = True
    def __init__(self, name: str, custom_tool_def_list: List[CustomToolDef], add_to_context: bool=True) -> None:
        self.name = name
        self.custom_tool_def_list = custom_tool_def_list
        self.add_to_context = add_to_context
    def tool_count(self) -> int:
        return len(self.custom_tool_def_list)


class P4VConfigType(str, Enum):
    wt_and_pwsh = "wt_and_pwsh"
    powershell  = "powershell"


class CustomTool:
    name = ""
    required_exe_list = []
    custom_tool_folder = None
    def __init__(self, name: P4VConfigType, required_exe_list: List[str], custom_tool_folder: CustomToolFolder) -> None:
        self.name = name
        self.required_exe_list = required_exe_list
        self.custom_tool_folder = custom_tool_folder
    def is_compatible(self) -> bool:
        return all([which(exe) != None for exe in self.required_exe_list])


custom_tool_list = []
base_cmd_quick = "unk preflight --changelist %c --type quick"
base_cmd_full = "unk preflight --changelist %c --type full"
base_cmd_quick_no_commit = "unk preflight --no-commit-on-success --changelist %c --type quick"
base_cmd_full_no_commit = "unk preflight --no-commit-on-success --changelist %c --type full"


pwsh_tool_exe = "wt.exe"
pwsh_cmd_base = "new-tab pwsh -NoExit -Command"
custom_tool_list.append(
    CustomTool(
        name=P4VConfigType.wt_and_pwsh,
        required_exe_list=[pwsh_tool_exe, "pwsh.exe"],
        custom_tool_folder=CustomToolFolder(
            name = "Preflight",
            custom_tool_def_list = [
                CustomToolDef(
                    name="Preflight Only - Quick", command = pwsh_tool_exe, add_separator_before = True,
                    arguments = f"{pwsh_cmd_base} {base_cmd_quick_no_commit}"
                ),
                CustomToolDef(
                    name="Preflight Only - Full", command = pwsh_tool_exe,
                    arguments = f"{pwsh_cmd_base} {base_cmd_full_no_commit}"
                ),
                CustomToolDef(
                    name="Preflight and Commit - Quick", command = pwsh_tool_exe, add_separator_before = True,
                    arguments = f"{pwsh_cmd_base} {base_cmd_quick}"
                ),
                CustomToolDef(
                    name="Preflight and Commit - Full", command = pwsh_tool_exe,
                    arguments = f"{pwsh_cmd_base} {base_cmd_full}"
                )
            ]
        )
    )
)


powershell_tool_exe = "powershell.exe"
powershell_cmd_base = "start-process powershell -ArgumentList '-noexit -command"
custom_tool_list.append(
    CustomTool(
        name=P4VConfigType.powershell,
        required_exe_list=[powershell_tool_exe],
        custom_tool_folder=CustomToolFolder(
            name = "Preflight",
            custom_tool_def_list = [
                CustomToolDef(
                    name = "Preflight Only - Quick", command = powershell_tool_exe, add_separator_before = True,
                    arguments = f"{powershell_cmd_base} \"{base_cmd_quick_no_commit}\" '"
                ),
                CustomToolDef(
                    name = "Preflight Only - Full", command = powershell_tool_exe,
                    arguments = f"{powershell_cmd_base} \"{base_cmd_full_no_commit}\" '"
                ),
                CustomToolDef(
                    name = "Preflight and Commit - Quick", command = powershell_tool_exe, add_separator_before = True,
                    arguments = f"{powershell_cmd_base} \"{base_cmd_quick}\" '"
                ),
                CustomToolDef(
                    name = "Preflight and Commit - Full", command = powershell_tool_exe,
                    arguments = f"{powershell_cmd_base} \"{base_cmd_full}\" '"
                )
            ]
        )
    )
)


class Changelist:
    change = ""
    client = ""
    is_shelved = False
    def __init__(self, dict=None, is_default=False, change="", client="") -> None:
        if dict:
            for k, v in dict.items():
                setattr(self, k.lower(), v)
            if "shelved" in dict.keys() or "shelveUpdate" in dict.keys():
                self.is_shelved = True
        else:
            if is_default:
                self.change = DEFAULT_CHANGE
            elif change:
                self.change = change
            if client:
                self.client = client
    def is_default(self) -> bool:
        return self.change == DEFAULT_CHANGE


class Status:
    type = ""
    count = 0
    def __init__(self, status_str: str) -> None:
        status_str_split = status_str.split()
        if status_str_split[0].isdigit():
            self.type = " ".join(status_str_split[1:])
            self.count = int(status_str_split[0])
        else:
            self.type = status_str_split[0].rstrip(":")
            self.count = int(status_str_split[1])
    @staticmethod
    def get_completed_list():
        return [
            BuildStatus.FINISHED,
            BuildStatus.SUCCESS,
            BuildStatus.FAILED,
            BuildStatus.CANCELLED,
            BuildStatus.CANCELED
        ]


class PreflightType(str, Enum):
    QUICK   = "quick"
    FULL    = "full"


class BuildState(str, Enum):
    QUEUED      = "queued"
    RUNNING     = "running"
    FINISHED    = "finished"
    DELETED     = "deleted"
    UNKNOWN     = "unknown"


class BuildStatus(str, Enum):
    IN_QUEUE    = "in queue"
    RUNNING     = "running"
    FINISHED    = "finished"
    SUCCESS     = "success"
    FAILED      = "failed"
    # Both spellings are used between running and finished build states:
    CANCELLED   = "cancelled"
    CANCELED    = "canceled"


def add_custom_tool_folder(root: ET.Element, custom_tool_folder: CustomToolFolder):
    folder = ET.SubElement(root, "CustomToolFolder")

    folder_name = ET.SubElement(folder, "Name")
    folder_name.text = custom_tool_folder.name

    if custom_tool_folder.add_to_context:
        add_to_context = ET.SubElement(folder, "AddToContext")
        add_to_context.text = "true"

    tool_def_list = ET.SubElement(folder, "CustomToolDefList")
    for custom_tool_def in custom_tool_folder.custom_tool_def_list:
        if custom_tool_def.add_separator_before:
            ET.SubElement(tool_def_list, "Separator")

        tool_def = ET.SubElement(tool_def_list, "CustomToolDef")
        definition = ET.SubElement(tool_def, "Definition")
        definition_name = ET.SubElement(definition, "Name")
        definition_name.text = custom_tool_def.name

        definition_command = ET.SubElement(definition, "Command")
        definition_command.text = custom_tool_def.command

        definition_arguments = ET.SubElement(definition, "Arguments")
        definition_arguments.text = custom_tool_def.arguments

        if custom_tool_def.add_to_context:
            add_to_context = ET.SubElement(tool_def, "AddToContext")
            add_to_context.text = "true"
    return


def install_p4v_tools(type_override: P4VConfigType=None):
    customtools_file_path = os.path.join(os.environ["USERPROFILE"], ".p4qt", "customtools.xml")
    if not os.path.isfile(customtools_file_path):
        secho("P4V tools configuration not found...", bold=True)
        return

    custom_tool = None
    if type_override:
        custom_tool = next((t for t in custom_tool_list if t.name.value == type_override), None)
    else:
        custom_tool = next((t for t in custom_tool_list if t.is_compatible()), None)
    if not custom_tool:
        secho("No compatible P4V tools configuration found...", bold=True)
        return

    tree = None
    root = None
    tool_folder_to_add = custom_tool.custom_tool_folder
    if os.path.getsize(customtools_file_path) == 0:
        root = ET.Element("CustomToolDefList", attrib={"varName": "customtooldeflist"})
        tree = ET.ElementTree(root)
    else:
        tree = ET.parse(customtools_file_path)
        root = tree.getroot()
        for sub_element in list(root):
            if sub_element.tag != "CustomToolFolder":
                continue
            if sub_element.findtext("Name") == tool_folder_to_add.name:
                # Compare number of defined tools in the XML vs. tool count in the tool list to see if
                # we need to update. This should be replaced with a deeper comparison, in case we modify
                # any of the tools to support changes to parameters and such.
                tool_def_list = list(sub_element.find("CustomToolDefList"))
                tool_def_count = sum([t.tag == "CustomToolDef" for t in tool_def_list])
                if tool_def_count == tool_folder_to_add.tool_count():
                    secho("P4V Preflight context menu already added.", bold=True)
                    if not type_override:
                        return
                root.remove(sub_element)
                break
    add_custom_tool_folder(root, tool_folder_to_add)
    ET.indent(tree, space=" ")
    tree.write(customtools_file_path, encoding="utf-8", xml_declaration=True)
    secho("Added P4V Preflight context menu.", bold=True)
    return


def connect_p4():
    p4_conn = P4()
    if p4_client:
        p4_conn.client = p4_client
    try:
        p4_conn.connect()
    except Exception as e:
        abort(f"Cannot establish connection with Perforce server: {e}...")
    global p4
    p4 = p4_conn
    return


def set_p4_client(client_name: str):
    global p4_client
    p4_client = client_name
    connect_p4()
    return


def get_sorted_change_obj_list():
    connect_p4()
    client_pending_dict = OrderedDict()
    # Collect pending changelists for all user clients.
    for change in p4.run_changes("--me", "-s", "pending", "-L"):
        client_pending_dict.setdefault(change["client"], []).append(Changelist(change))

    # Check each user client for default changelists with open files.
    for client in p4.run_clients("--me"):
        if p4.run_opened("-c", "default", "-C", client["client"]):
            default_obj = Changelist(is_default=True, client=client["client"])
            client_pending_dict.setdefault(client["client"], []).append(default_obj)
    if not client_pending_dict:
        abort("No pending changelists found.")

    # Move the current client to the front for user visibility and easier selection.
    current_client = p4.client
    if current_client in client_pending_dict:
        client_pending_dict.move_to_end(current_client, last=False)

    def sort_func(change_obj):
        return int(change_obj.change) if change_obj.change.isdigit() else -1
    sorted_change_obj_list = []
    for change_obj_list in client_pending_dict.values():
        sorted_change_obj_list.extend(sorted(change_obj_list, key=sort_func))
    return sorted_change_obj_list


def get_client_from_changelist(changelist):
    connect_p4()
    if changelist == DEFAULT_CHANGE:
        return p4.client
    return p4.run_describe("-s", changelist)[0]["client"]


def get_client_root(client_name):
    return p4.run_client("-o", client_name)[0]["Root"]


def get_client_stream(client_name):
    return p4.run_client("-o", client_name)[0]["Stream"]


def print_change_obj_list(sorted_change_obj_list):
    if not sorted_change_obj_list:
        abort("No changes to display")

    def print_client(client_name):
        stream_name = get_client_stream(client_name)
        secho(f"{client_name} ({stream_name})", bold=True)

    # Expect sorted by client so that changes print in client groups.
    current_client = sorted_change_obj_list[0].client
    print_client(current_client)
    for i, change_obj in enumerate(sorted_change_obj_list):
        client = change_obj.client
        if not client == current_client:
            current_client = client
            print_client(client)
        description = ""
        if hasattr(change_obj, "desc"):
            description = change_obj.desc.replace("\n", " ").replace("\r", "")
        elif change_obj.is_default():
            description = "<default>"
        secho(f" {i} : {description}")
    return


def check_for_forbidden_files(changelist):
    describe_shelve = get_describe_shelve(changelist)[0]
    for shelf_file in describe_shelve["depotFile"]:
        if re.search("^\/\/[^\/]*\/[^\/]*\/Raw", shelf_file):
            abort(f"Cannot preflight a CL containing Raw files.")
    return

def verify_changelist(change_obj, change_obj_list):
    if not change_obj:
        abort("No changelist selected")
    changelist = change_obj.change
    client = change_obj.client
    describe = get_describe_shelve(changelist)[0]

    if change_obj.is_default() and not get_opened_file_list(changelist):
        abort(f"Selected changelist does not have any opened files: {changelist} ({client})")
    if not any([c for c in change_obj_list if c.client == client and c.change == changelist]):
        abort(f"Selected changelist not owned by current user: {changelist} ({client})")
    return


def get_change_obj(changelist):
    if not changelist.isdigit():
        return Changelist(is_default=True, client=p4.client)
    return Changelist(dict=p4.run_change("-o", changelist)[0])


def get_opened_file_list(changelist):
    return p4.run_opened("-c", changelist)


def get_describe_shelve(shelve_changelist):
    return p4.run_describe("-s", "-S", shelve_changelist)


def revert_file_in_default(depot_file, *extra_args):
    return p4.run_revert(*extra_args, "-c", "default", depot_file)

def revert_file_in_cl(depot_file, clnumber, *extra_args):
    return p4.run_revert(*extra_args, "-c", clnumber, depot_file)

def flush_file(depot_file):
    return p4.run_sync("-k", depot_file)


def open_file_for_edit(depot_file):
    return p4.run_edit(depot_file)


def attempt_shelve_changelist(changelist):
    set_p4_client(get_client_from_changelist(changelist))
    if changelist == DEFAULT_CHANGE:
        secho("Creating a changelist from default.", bold=True)
        description = prompt("Input a description for the new changelist")
        new_change = p4.run_change("-o")[0]
        new_change["Description"] = description
        p4.input = new_change
        changelist = p4.run_change("-i")[0].split()[1]
        secho(f"Changelist created from default: {changelist}.")
    secho(f"Shelving opened files in {changelist}...")
    p4.run_shelve("-f", "-c", changelist)
    return changelist


def attempt_revert_unchanged(depot_file_list):
    secho("Cleaning up unchanged files...")
    changed_file_list = []
    for depot_file in depot_file_list:
        if not p4.run_revert("-a", depot_file):
            changed_file_list.append(depot_file)
            secho(f"(SKIPPED) This file has new changes: {depot_file}", fg="yellow", bold=True)
    return changed_file_list


def attempt_resolve(depot_file_list):
    has_reverted_file = False
    has_new_edits = False
    needs_manual_resolve = False
    for i, depot_file in enumerate(depot_file_list):
        progress = f"[{i+1}/{len(depot_file_list)}]"
        fstat = p4.run_fstat("-Ro", "-e", "default", depot_file)[0]
        if "unresolved" in fstat:
            if confirm(f"{progress} Keep your new changes: {depot_file}"):
                has_new_edits = True
                p4.run_resolve("-f", "-ay", depot_file)
            else:
                has_reverted_file = True
                revert_file_in_default(depot_file)
        elif fstat["action"] == "edit":
            has_new_edits = True
            secho(f"{progress} Has new changes: {depot_file}", fg="yellow", bold=True)
        else:
            needs_manual_resolve = True
            secho(f"{progress} Needs manual investigation: {depot_file}", fg="yellow", bold=True)

    if has_reverted_file:
        secho("\nThere were reverted files. If you are working in the editor, reload it or the level/asset.", fg="yellow", bold=True)
    if has_new_edits:
        secho("\nFiles with new changes have been moved to the default changelist.", fg="yellow", bold=True)
    if needs_manual_resolve:
        secho("\nPlease resolve the remaining files in P4V.", fg="yellow", bold=True)
    return


def reopen_changelist_to_default(changelist):
    secho(f"\nMoving open files in {changelist} to the default changelist...")
    for depot_file in [x["depotFile"] for x in get_opened_file_list(changelist)]:
        secho(p4.run_reopen("-c", "default", depot_file), fg="white", bg="black")
    return


def submit_shelve(changelist):
    secho(f"\nSubmitting shelve {changelist}...")
    ret = p4.run_submit("-e", changelist)
    submitted_cl = next((x for x in ret if "submittedChange" in x))["submittedChange"]
    secho(f"Changelist '{changelist}' submitted as '{submitted_cl}'", fg="green", bold=True)
    return submitted_cl


def sync_changelist(changelist, clobber=True):
    secho(f"\nSyncing to {changelist}...")
    try:
        p4_resp = p4.run_sync(f"@={changelist}")
        secho("\n".join([str(r) for r in p4_resp]), fg="white", bg="black")
    except P4Exception as e:
        for error in e.errors:
            match = re.search("^Can't clobber writable file (.*)$", error)
            if clobber and match:
                secho(p4.run_sync("-f", f"{match.group(1)}@{changelist}"), fg="white", bg="black")
            else:
                secho(error, fg="yellow", bg="black")
    return


def sync_scripts():
    # Prevent warnings from raising exceptions; p4 files and sync will warn if it does not action.
    p4.exception_level = 1 # 2 by default which means raise all.
    # Sync the scripts for each client if they exist in that client stream.
    for client in p4.run_clients("--me"):
        if "Stream" not in client:
            continue
        client_name = client["client"]
        p4.client = client_name
        client_root = client["Root"]
        # Use 'p4 where' on the local path to figure out where the scripts depot path would be.
        # Note this is needed because the stream path can be different from the actual depot path.
        try:
            scripts_depot_path = p4.run_where(os.path.join(client_root, SCRIPTS_DIR, "*"))[0]["depotFile"]
        except:
            # Path is not under the root which will be the case for generated unix Swarm workspaces.
            continue
        if not p4.run_files(scripts_depot_path):
            # Scripts are not in this client.
            continue
        if p4.run_sync(scripts_depot_path):
            secho(f"Updated scripts for {client_name}")
    p4.exception_level = 2


def get_script_path(script_file_name):
    main_path = os.path.join("s:", os.sep, "sn2-main", SCRIPTS_DIR, script_file_name)
    if os.path.isfile(main_path):
        return main_path
    if p4_client:
        p4_path = os.path.join(get_client_root(p4_client), SCRIPTS_DIR, script_file_name)
        if os.path.isfile(p4_path):
            return p4_path
    client_root = p4.run_info()[0]["clientRoot"]
    if client_root:
        p4_path = os.path.join(client_root, SCRIPTS_DIR, script_file_name)
        if os.path.isfile(p4_path):
            return p4_path
    abort(f"Failed to find script '{script_file_name}', post for help on Slack!")


def get_shelve_preflight_build_id(shelve_changelist, type=PreflightType.FULL, stream="", find=False, print_output=True, abort_on_fail=True, submit_on_server=True, content_only_build=False):
    cmd = [
        sys.executable,
        get_script_path("trigger_shelve_preflight.py"),
        "--shelve_change", shelve_changelist,
        "--retry_count", "5"
    ] + (
        ["--find"] if find else ["--preflight_type", type]
    ) + (
        ["--shelve_stream", stream] if stream else []
    ) + (
        ["--submit_on_server"] if submit_on_server else []
    ) + (
        ["--content_only"] if content_only_build else []
    )
    build_id = ""
    try:
        secho(f"{'Finding' if find else 'Triggering'} preflight for shelve {shelve_changelist}...")
        output = check_output(cmd).strip().decode("ascii")
        if print_output:
            secho(output, fg="green")
        build_id = output.split("\n")[-1]
    except CalledProcessError as e:
        secho(e.output.decode("ascii"), fg="red")
        if abort_on_fail:
            abort(f"Failed to {'find' if find else 'trigger'} preflight.")
    if build_id and print_output:
        secho(f"Found TeamCity build id: {build_id}")
    return build_id


def update_description_tag(changelist, build_id, state=""):
    connect_p4()
    change = p4.run_change("-o", changelist)[0]
    current_description = change["Description"]
    new_tag = f"{PREFLIGHT_TAG}-tc-{build_id}" + (f"-{state.replace(' ', '')}" if state else "")
    match = re.search(f".*({PREFLIGHT_TAG}-tc-\\d+(-\\w+)?).*", current_description)
    if match:
        change["Description"] = current_description.replace(match.group(1), new_tag)
    else:
        change["Description"] = f"{current_description}\n{new_tag}"
    p4.input = change
    p4.run_change("-i")


def is_build_success(build_json):
    # Check 'statusText' which has the result for all actual build steps; 'status' includes the parent trigger.
    # Some builds succeed on all steps but fail on the parent trigger due to infrastructure bugs or issues.
    status_list = parse_status_list(build_json)
    return len(status_list) > 0 and all([s.type == BuildStatus.SUCCESS for s in status_list])


def parse_status_list(build_json):
    match = re.search("^.*\\(([\\s\\w:,]*)\\).*$", get_build_status_text(build_json))
    return [Status(s) for s in match.group(1).split(", ")] if match else []


def get_build_state(build_json):
    return build_json["state"]


def get_build_status(build_json):
    return build_json["status"]


def get_build_status_text(build_json):
    return build_json.get("statusText", get_build_wait_reason(build_json))


def get_build_wait_reason(build_json):
    return build_json.get("waitReason", "")


def get_build_start_estimate(build_json):
    # example:  20231006T210047+0000 (%Y%m%dT%H%M%S%z)
    return build_json.get("startEstimate", "")


def teamcity_strptime(teamcity_time_str):
    return datetime.strptime(teamcity_time_str, "%Y%m%dT%H%M%S%z")


def get_time_from_now_str(future_date_time):
    current_datetime = datetime.now(future_date_time.tzinfo)
    delta_seconds = int((future_date_time - current_datetime).total_seconds())
    return get_time_str(delta_seconds)


def get_time_str(seconds):
    remaining_minutes = seconds // 60
    remaining_seconds = seconds - (remaining_minutes * 60)
    return f"{remaining_minutes}m {remaining_seconds:02}s"


def get_build_start_estimate_str(build_json):
    build_start_estimate = get_build_start_estimate(build_json)
    if not build_start_estimate:
        return ""
    return get_time_from_now_str(teamcity_strptime(build_start_estimate))


def get_build_finish_estimate_str(build_json):
    running_info = get_build_running_info(build_json)
    if not running_info:
        return ""
    
    if not 'estimatedTotalSeconds' in running_info:
        return 'Cannot estimate finish time due to lack of trend data on TeamCity.'

    elapsed_seconds = int(running_info["elapsedSeconds"])
    estimated_total_seconds = int(running_info["estimatedTotalSeconds"])
    return get_time_str(estimated_total_seconds - elapsed_seconds)


def get_build_running_info(build_json):
    return build_json.get("running-info", "")


def wait_on_teamcity_build(build_id, changelist, submit_on_server):
    def get_build_web_url(build_json): return build_json["webUrl"]
    def parse_total(build_json):
        total = 1
        if get_build_state(build_json) in [BuildState.RUNNING, BuildState.FINISHED]:
            total = max(total, sum([s.count for s in parse_status_list(build_json)]))
        return total
    def parse_completed(build_json):
        completed = 0
        if get_build_state(build_json) in [BuildState.RUNNING, BuildState.FINISHED]:
            completed = sum(
                s.count if s.type in Status.get_completed_list() else 0 for s in parse_status_list(build_json)
            )
        return completed
    def generate_state_table(build_json):
        table = Table(box=None, padding=(0,0), show_header=False)
        table.add_row(Text(get_build_web_url(build_json), style="blue on white"))
        progress_style = Style(color="magenta", bold=True)
        table.add_row(
            Spinner(
                'simpleDotsScrolling',
                speed=.5,
                style=progress_style,
                text=Text(
                    f"PREFLIGHT [{get_build_status_text(build_json)}]",
                    style="bold magenta"
                )
            )
        )

        suffix = ""
        build_start_estimate = get_build_start_estimate_str(build_json)
        build_state = get_build_state(build_json)
        if build_start_estimate:
            suffix += f", {build_start_estimate} to start"
        elif build_state == BuildState.RUNNING:
            dependecy_finish_estimate_str = get_build_finish_estimate_str(build_json)
            if dependecy_finish_estimate_str:
                suffix += f", {dependecy_finish_estimate_str} left"

        steps_completed = progress_completed = parse_completed(build_json)
        steps_total = progress_total = parse_total(build_json)
        running_info = get_build_running_info(build_json)
        if running_info:
            # Show a more fine-percentaged progress based on TeamCity estimate instead of steps.
            if "percentageComplete" in running_info:
                progress_completed = int(running_info["percentageComplete"])
            else:
                progress_completed = 0
            progress_total = 100

        progressOverall = Progress(
            TextColumn(f"{build_state}{suffix} | ", style=progress_style),
            BarColumn(
                style=Style(color="white"),
                complete_style=progress_style,
                finished_style=progress_style
            ),
            TaskProgressColumn(style=progress_style),
            TextColumn(f"{steps_completed}/{steps_total}", style=Style(color="green"))
        )
        taskOverall = progressOverall.add_task("", total=progress_total)
        progressOverall.update(taskOverall, completed=progress_completed)
        table.add_row(progressOverall)
        return table

    build_json = get_teamcity_build_json(build_id)
    estimate_build_id = build_id
    running_info = get_build_running_info(build_json)
    if not 'estimatedTotalSeconds' in running_info:
        snapshot_dependencies = build_json.get("snapshot-dependencies")
        estimate_build_id = str(snapshot_dependencies.get("build")[0].get("id"))
    prev_state = None
    with Live(generate_state_table(build_json), refresh_per_second=3) as live:
        while get_build_state(build_json) in [BuildState.QUEUED, BuildState.RUNNING, BuildState.FINISHED]:
            build_json = get_teamcity_build_json(build_id)
            if estimate_build_id != build_id and "startDate" in build_json:
                estimate_json = get_teamcity_build_json(estimate_build_id)
                if "finishEstimate" in estimate_json:
                    finish_estimate = datetime.strptime(estimate_json["finishEstimate"], "%Y%m%dT%H%M%S%z")
                    start_date = datetime.strptime(build_json["startDate"], "%Y%m%dT%H%M%S%z")
                    build_json["running-info"]["estimatedTotalSeconds"] = (finish_estimate - start_date).seconds

            live.update(generate_state_table(build_json))
            curr_state = get_build_state(build_json)
            # Skip updating if we did a submit on server as that process already updated the tag.
            if submit_on_server and curr_state == BuildState.FINISHED:
                break
            if prev_state != curr_state:
                prev_state = curr_state
                update_description_tag(changelist, build_id, curr_state)
            if curr_state == BuildState.FINISHED:
                break
            time.sleep(5)
    return


def get_teamcity_build_json(build_id):
    cmd = [
        sys.executable,
        get_script_path("get_teamcity_build_json.py"),
        "--build_id", build_id
    ]
    build_json = ""
    try:
        output = check_output(cmd).strip().decode("ascii")
        build_json = output.split("\n")[-1]
    except CalledProcessError as e:
        secho(e.output.decode("ascii"), fg="red")
        abort(f"Failed to find TeamCity build: {build_id}")
    return json.loads(build_json)

def move_open_files_to_default(shelve_changelist: str):
    opened_file_list = get_opened_file_list(shelve_changelist)
    if opened_file_list:
        reopen_changelist_to_default(shelve_changelist)
    return opened_file_list

def shelf_is_content_only(shelve_changelist: str) -> bool:
    describe_shelve = get_describe_shelve(shelve_changelist)[0]
    for shelf_file in describe_shelve["depotFile"]:
        if re.search("/Source/", shelf_file):
            return False
    return True

def commit(shelve_changelist: str):
    """
    Commit a shelve
    """
    set_p4_client(get_client_from_changelist(shelve_changelist))
    secho(f"\nLooking to commit shelve: {shelve_changelist}")

    # Move opened files to default so that the shelve can be submitted.
    opened_file_list = move_open_files_to_default(shelve_changelist)
    describe_shelve = get_describe_shelve(shelve_changelist)[0]
    submitted_changelist = submit_shelve(shelve_changelist)

    # Clean up non-edit action open files that were moved.
    edit_file_list = []
    for opened_file in opened_file_list:
        # add, move/add, move/delete, edit, delete, branch, integrate
        action = opened_file["action"]
        depot_file = opened_file["depotFile"]
        if action in ["add", "move/add", "edit"]:
            edit_file_list.append(depot_file)
            # Prefer diffing the shelve/submitted but this is not available for local add-actioned files.
            # So reopen the file as edit and we can attempt to revert unchanged later.
            # Doing this for edit files to avoid needing resolve; the file gets treated as having new edits.
            revert_file_in_default(depot_file, "-k")
            flush_file(f"{depot_file}@{submitted_changelist}")
            open_file_for_edit(depot_file)
            continue
        elif action == "move/delete":
            # This file is reverted when the paired move/add file is reverted.
            continue

        # Remaining delete, branch, integrate should be reverted because these can't be edited after such action.
        try:
            # Compare open and shelve file action before reverting.
            shelve_file_index = describe_shelve["depotFile"].index(depot_file)
            if action == describe_shelve["action"][shelve_file_index]:
                revert_file_in_default(depot_file)
        except ValueError:
            secho(f"Extra file not found in submitted shelve: {depot_file}", fg="yellow", bg="black", bold=True)

    sync_changelist(submitted_changelist)
    if edit_file_list:
        changed_file_list = attempt_revert_unchanged(edit_file_list)
        if changed_file_list:
            secho("\nThere are files with new changes...", fg="yellow", bg="black", bold=True)
            attempt_resolve(changed_file_list)
            return

    secho("Cleanup done.")
    return


def tailscale_is_connected() -> bool:
    try:
        result = check_output('tailscale status')
        return True
    except CalledProcessError as e:
        return False


def editor_is_running():
    for proc in process_iter(['name']):
        if proc.info['name'] == "Subnautica2Editor.exe":
            return True
    return False


def main(
    changelist: str = Option("", help="The changelist you own and want to preflight."),
    commit_on_success: Optional[bool] = Option(True, help="Commit the shelve on successful preflight."),
    type: PreflightType = Option(PreflightType.QUICK, help="The type of preflight to run."),
    p4v_config_type: P4VConfigType = Option(None, help="The command to use when running from P4V context menus."),
    use_server_submit: Optional[bool] = Option(True, help="If committing on successful preflight, should server side commit be used."),
    verbose: Optional[bool] = Option(False, help="Enables extra debug output.")
):
    """
    Preflight a changelist
    """
    
    secho("Initializing, this may take a moment...\n", bold=True)

    # Check for Tailscale connection
    if not "tailscale" in os.environ["PATH"].lower() or not tailscale_is_connected():
        abort("In order to preflight you must be connected to Tailscale.")

    try:
        install_p4v_tools(p4v_config_type)
    except Exception as e:
        abort(f"Failed to add P4V Preflight context menu:\n{e}...")

    connect_p4()
    try:
        sync_scripts()
    except Exception as e:
        abort(f"Failed to sync scripts; ask for help!\n{e}...")

    # Check for editor, if running wait for it to be closed
    if use_server_submit and editor_is_running():
        secho("\nEditor is running, save your work and close it to continue..")
        while editor_is_running():
            time.sleep(1)

    sorted_change_obj_list = get_sorted_change_obj_list()
    if changelist:
        change_obj = get_change_obj(changelist)
    else:
        print_change_obj_list(sorted_change_obj_list)
        chosen_index = prompt(f"\nSelect a changelist")
        choice_count = len(sorted_change_obj_list)
        if not chosen_index.isdigit() or not (int(chosen_index) in range(choice_count)):
            abort("Invalid option.")
        else:
            change_obj = sorted_change_obj_list[int(chosen_index)]

    verify_changelist(change_obj, sorted_change_obj_list)
    shelve_changelist = changelist
    if get_opened_file_list(change_obj.change):
        shelve_changelist = attempt_shelve_changelist(change_obj.change)
        check_for_forbidden_files(shelve_changelist)
        if use_server_submit and commit_on_success:
            secho(f"Reverting files from CL {shelve_changelist} to allow for submit on the server..")
            revert_file_in_cl("//...", shelve_changelist, "-w")
    else:
        if change_obj.is_shelved:
            shelve_changelist = change_obj.change
        else:
            abort(f"No opened files or shelve to work with in changelist '{change_obj.change}'...")
    
    use_content_build = shelf_is_content_only(shelve_changelist)
    build_id = get_shelve_preflight_build_id(
        shelve_changelist, type=type, stream=get_client_stream(change_obj.client), print_output=verbose, submit_on_server=(use_server_submit and commit_on_success), content_only_build=use_content_build
    )

    if type == PreflightType.QUICK:
        secho("\n** Quick Build Preflight is being used!", fg="yellow", bg="black", bold=True)
        secho("** If your preflight should test cooking please cancel and run a Full Build Preflight from P4V.", fg="yellow", bg="black", bold=True)

    if use_server_submit:
        secho("\nBuild is requested, it is safe to close this window at any time!\n", fg="white", bg="black", bold=True)

    wait_on_teamcity_build(build_id, shelve_changelist, use_server_submit)

    build_json = get_teamcity_build_json(build_id)
    if not is_build_success(build_json):
        abort(f"Preflight failed ({get_build_status(build_json)})")

    secho("Preflight finished successfully.", fg="green", bold=True)
    if commit_on_success and not use_server_submit:
        commit(shelve_changelist)

    return
