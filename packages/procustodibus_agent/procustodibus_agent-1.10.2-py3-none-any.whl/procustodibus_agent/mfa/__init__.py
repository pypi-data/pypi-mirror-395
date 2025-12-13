"""Pro Custodibus multifactor authentication."""

import sys
from datetime import datetime
from getpass import getpass
from os import fdopen
from re import fullmatch

from tabulate import tabulate

from procustodibus_agent.agent import ping
from procustodibus_agent.mfa.api import (
    check_mfa_api,
    do_mfa_api,
    list_mfa_api,
    login_api_with_password,
)

TZ = None


def check_mfa(cnf, endpoint, output=None):
    """Checks if MFA for specified endpoint has expired.

    Arguments:
        cnf (Config): Config object.
        endpoint (str): Endpoint ID.
        output (IOBase): Output stream.
    """
    state = check_mfa_api(cnf, endpoint).strip()
    print(state, file=output or sys.stdout)


def list_mfa(cnf, output=None):
    """Lists MFA state for all endpoints of the configured host.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream.
    """
    json = list_mfa_api(cnf)
    rows = _transform_rotation_list(json)
    _print_rotation_list(rows, output)


def _transform_rotation_list(json):
    """Transforms JSON from MFA list API to shallow rows of data.

    Arguments:
        json (dict): Full API result.

    Returns:
        list: List of shallow rows with rotation data.
    """
    return [_transform_rotation_item(x, json) for x in json["data"]]


def _transform_rotation_item(item, json):
    """Transforms JSON data item from MFA list API to shallow dict of data.

    Arguments:
        item (dict): Individual data item from API.
        json (dict): Full API result.

    Returns:
        dict: Shallow dict of data for an endpoint.
    """
    attributes = item.get("attributes", {})
    relationships = item.get("relationships", {})
    interface = _find_name_of_related(relationships.get("local_interface"), json)
    peer = _find_name_of_related(relationships.get("remote_peer"), json)
    endpoint = _find_id_of_related(relationships.get("local_endpoint"))
    return {
        "due": attributes.get("due"),
        "rotated": attributes.get("rotated"),
        "sync": attributes.get("sync"),
        "interface": interface,
        "peer": peer,
        "endpoint": endpoint,
    }


def _find_id_of_related(related):
    """Finds the ID of an included item.

    Arguments:
        related (dict): Related data item from API.

    Returns:
        str: ID or `None`.
    """
    if related:
        return related["data"][0]["id"]
    return None


# simpler for now to keep this logic together rather than subdivide it more functions
def _find_name_of_related(related, json):
    """Finds the name of an included item from a related item.

    Arguments:
        related (dict): Related data item from API.
        json (dict): Full API result.

    Returns:
        str: Name or `None`.
    """
    if related:
        for r in related["data"]:
            for i in json.get("included", []):
                if r.get("id") == i.get("id") and r.get("type") == i.get("type"):
                    return i.get("attributes", {}).get("name")
    return None


def _print_rotation_list(rows, output=None):
    """Prints transformed, shallow data from MFA list API.

    Arguments:
        rows (list): List of transformed shallow rows.
        output (IOBase): Output stream.
    """
    values = [
        [
            row["interface"],
            row["peer"],
            row["endpoint"],
            _format_rotation_state(row) or "-",
        ]
        for row in rows
    ]

    table = tabulate(values, ["Interface", "Endpoint", "ID", "State"], "simple")
    print(table, file=output or sys.stdout)


def do_mfa(cnf, endpoint, user, password, secondary_code=None, output=None):
    """Authenticates with specified user to sync the MFA key of the specified endpoint.

    Arguments:
        cnf (Config): Config object.
        endpoint (str): Endpoint ID.
        user (str): User ID.
        password (str): User password.
        secondary_code (str): Optional secondary verification code.
        output (IOBase): Output stream.
    """
    token = login_api_with_password(cnf, user, password, secondary_code)
    do_mfa_api(cnf, endpoint, user, token)
    ping(cnf)
    json = do_mfa_api(cnf, endpoint, user, token)
    _display_mfa_results(json, output)


def read_password(password=None, file_descriptor=None, prompt=False):  # noqa: FBT002
    """Reads a password.

    Returns the password if `password` directly specified; or if not,
    reads from the file descriptor if `file_descriptor` specified; or if not,
    prompts for the password if `prompt` is truthy; or if not,
    returns None.

    Arguments:
        password (str): Actual password.
        file_descriptor: File descriptor number.
        prompt: True (or prompt string) to prompt for password.

    Returns:
        str: Password or None.
    """
    if password:
        return password.strip()
    if file_descriptor:
        if fullmatch(r"\d+", str(file_descriptor)):
            with fdopen(int(file_descriptor)) as f:
                return f.readline().strip()
        else:
            with open(file_descriptor) as f:
                return f.readline().strip()
    if isinstance(prompt, str):
        return getpass(prompt)
    if prompt:
        return getpass()
    return None


def _display_mfa_results(json, output=None):
    """Prints result of syncing the MFA key via API.

    Arguments:
        json (dict): API result.
        output (IOBase): Output stream.
    """
    item = json["data"][0]["attributes"]
    content = _format_rotation_state(item)

    print(content, file=output or sys.stdout)


def _format_rotation_state(item):
    """Extracts and formats the rotation state from the specified shallow data item.

    Arguments:
        item (dict): Shallow data item (ie attributes dict).

    Returns:
        str: Rotation state string or blank.
    """
    sync = item.get("sync") or item.get("preshared_key_sync")
    due = item.get("due") or item.get("preshared_key_due")
    if due:
        due = datetime.strptime(due.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S%z")
    return _format_rotation_sync_and_due(sync, due)


# simpler for now to keep this logic together rather than subdivide it more functions
def _format_rotation_sync_and_due(sync, due):
    """Formats the rotation state from the specified sync data.

    Arguments:
        sync (str): Synchronization state (eg 'mismatch_pending').
        due (datetime): Synchronization due date.

    Returns:
        str: Rotation state string or blank.
    """
    if due:
        now = datetime.now().astimezone()
        if sync == "mismatch" and due:
            return "EXPIRED"
        if (not sync or sync == "match") and due > now:
            return f"OK until {due.astimezone(TZ):%x %X %Z}"
        if (not sync or sync == "match") and due < now:
            return "OK but rotation imminent"
    if sync:
        return sync.upper()
    return ""
