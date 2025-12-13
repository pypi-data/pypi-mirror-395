"""Executor logic."""

from contextlib import contextmanager
from logging import getLogger
from os import devnull, unlink
from platform import system
from subprocess import CompletedProcess
from tempfile import NamedTemporaryFile

from procustodibus_agent.executor.sys_cmd import _sc_query_state, get_sys_cmd
from procustodibus_agent.resolve_hostname import split_endpoint_address
from procustodibus_agent.wg import separate_dns_and_search

SYS_CMD = get_sys_cmd()


def set_sys_cmd(sys_cmd):
    """Sets the global command object.

    Arguments:
        sys_cmd: Command object.
    """
    global SYS_CMD  # noqa: PLW0603
    SYS_CMD = sys_cmd


def execute_desired(cnf, interfaces, data):
    """Executes desired changes from API.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.

    Returns:
        list: Executed changes.
    """
    data = normalize_data(data)
    if not data:
        return []
    if cnf.read_only:
        getLogger(__name__).warning("in read only mode: rejected %d changes", len(data))
        return []

    shut_down_interfaces(cnf, interfaces, data)
    delete_interfaces(cnf, interfaces, data)
    delete_endpoints(cnf, interfaces, data)
    update_interfaces(cnf, interfaces, data)
    update_routings(cnf, interfaces, data)
    update_endpoints(cnf, interfaces, data)
    create_interfaces(cnf, interfaces, data)
    create_routings(cnf, interfaces, data)
    create_endpoints(cnf, interfaces, data)
    rename_interfaces(cnf, interfaces, data)
    start_up_interfaces(cnf, interfaces, data)
    update_down_scripts(cnf, interfaces, data)

    return aggregate_executed_results(data)


def normalize_data(data):
    """Removes invalid desired change objects.

    And ensures they contain a fow core properties:
        type (str): Change type (eg 'desired_routings').
        id (str): Change ID (eg 'ABC123').
        attributes (dict): Properties to change.
        key (str): Log key to identify change (eg 'desired_interfaces ABC123').
        interface (str): Name of wg interface (eg 'wg0').
        results (list): List of change results (to append to).

    Arguments:
        data (list): List of desired change objects.

    Returns:
        list: Normalized list of desired change objects.
    """
    normalized = []

    for x in data:
        if (
            x.get("type")
            and x.get("id")
            and x.get("attributes")
            and (x["attributes"].get("name") or x["attributes"].get("interface"))
        ):
            x["key"] = f"{x['type']} {x['id']}"
            x["interface"] = x["attributes"].get("interface") or x["attributes"].get(
                "name"
            )
            x["results"] = []
            normalized.append(x)

    return normalized


def aggregate_executed_results(data):
    """Extracts result output from processed list of desired change objects.

    Arguments:
        data (list): Processed list of desired change objects.

    Returns:
        list: Flattened list of executed result output.
    """
    return [x for x in [executed_result(x) for x in data] if x]


def executed_result(change):
    """Extracts result output from a processed desired change object.

    Arguments:
        change (dict): Processed desired change object.

    Returns:
        list: Executed result output.
    """
    results = change["results"]
    output = []

    if next((x for x in results if x.returncode), None):
        output.append(f"fail {change['key']}")
    elif results:
        output.append(f"success {change['key']}")

    for x in results:
        stdout = x.stdout.strip() if x.stdout else ""
        if stdout not in ("", "Ok."):
            output.append(stdout)

    return "\n".join(output)


def shut_down_interfaces(cnf, interfaces, data):
    """Shuts down interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_shut_down_interface(cnf, interfaces, x):
            shut_down_interface(cnf, interfaces, x)


def delete_interfaces(cnf, interfaces, data):
    """Deletes existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_delete_interface(interfaces, x):
            delete_interface(cnf, interfaces, x)


def delete_endpoints(cnf, interfaces, data):
    """Deletes existing peers for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_delete_endpoint(interfaces, x):
            delete_endpoint(cnf, interfaces, x)


def update_interfaces(cnf, interfaces, data):
    """Updates existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_update_interface(interfaces, x):
            update_interface(cnf, interfaces, x)


def update_routings(cnf, interfaces, data):
    """Updates the routing info of existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_update_routing(interfaces, x):
            update_routing(cnf, interfaces, x)


def update_endpoints(cnf, interfaces, data):
    """Updates existing peers for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_update_endpoint(interfaces, x):
            update_endpoint(cnf, interfaces, x)


def create_interfaces(cnf, interfaces, data):
    """Creates new interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_create_interface(interfaces, x):
            create_interface(cnf, interfaces, x)


def create_routings(cnf, interfaces, data):
    """Creates the routing info for new interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_create_routing(interfaces, x):
            create_routing(cnf, interfaces, x)


def create_endpoints(cnf, interfaces, data):
    """Creates new peers for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_create_endpoint(interfaces, x):
            create_endpoint(cnf, interfaces, x)


def rename_interfaces(cnf, interfaces, data):
    """Renames existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_rename_interface(interfaces, x):
            rename_interface(cnf, interfaces, x)


def start_up_interfaces(cnf, interfaces, data):
    """Starts up new or existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    desired_interfaces = {
        x["interface"]: x for x in data if x["type"] == "desired_interfaces"
    }

    to_start = {}
    for x in data:
        if _is_start_up_interface(cnf, interfaces, x):
            changes = to_start.get(x["interface"])
            if changes:
                changes.append(x)
            else:
                to_start[x["interface"]] = [x]

    for name, changes in to_start.items():
        desired = desired_interfaces.get(name)
        # if most recent interface change explicitly commands to shut it down
        # override other desires and don't start interface back up
        if not (desired and desired["attributes"].get("up") is False):
            start_up_interface(cnf, interfaces, name, changes)


def update_down_scripts(cnf, interfaces, data):
    """Updates the down scripts of existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_update_down_script(cnf, interfaces, x):
            update_down_script(cnf, interfaces, x)


def shut_down_interface(cnf, interfaces, change):
    """Shuts down an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    results = change["results"]
    name = change["interface"]

    # remove to signal to other steps that the interface is down
    interface = interfaces.pop(name, {})
    # remember to start back up at end if previously was up
    if interface and interface.get("up"):
        change["attributes"]["was_up"] = True

    stop_results = []
    SYS_CMD.stop_service(cnf, name, stop_results)
    # don't fail change for errors shutting down
    for x in stop_results:
        x.returncode = 0
    results.extend(stop_results)


def delete_interface(cnf, _interfaces, change):
    """Deletes an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    results = change["results"]
    name = change["interface"]
    SYS_CMD.delete_wg_cnf(cnf, name, results)


def delete_endpoint(cnf, interfaces, change):
    """Deletes an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)
    pk = change["attributes"].get("public_key")
    peer = interface["peers"].pop(pk, None) if interface else None

    if peer and interface.get("up"):
        SYS_CMD.set_peer(cnf, name, pk, "remove", "", results)
        _delete_endpoint_routes(interface, peer, change)

    if SYS_CMD.check_wg_cnf(cnf, name, results) == "found":
        SYS_CMD.update_wg_cnf(cnf, name, {}, [change["attributes"]], results)
    else:
        results.append(CompletedProcess([], 0))

    _restart_if_wiresock(cnf, change)


def _delete_endpoint_routes(interface, peer, change):
    """Deletes an existing peer from a desired change object.

    Arguments:
        interface (dict): Interface info parsed from wg etc.
        peer (dict): Peer info parsed from wg etc.
        change (dict): Desired change object.
    """
    table = interface.get("table") or "auto"
    if table == "off":
        return

    allowed_ips = peer.get("allowed_ips") or []
    default_route = _uses_default_route(allowed_ips)

    if table != "auto" or not default_route:
        name = change["interface"]
        results = change["results"]
        for x in allowed_ips:
            SYS_CMD.update_route("del", x, name, table, results)
    else:
        change["restart"] = True


def update_interface(cnf, interfaces, change):
    """Updates an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    to_set = {k: change["attributes"].get(k) for k in ["id", "description"]}
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)

    _update_interface_private_key(cnf, interface, change, name, to_set, results)
    _update_interface_port(cnf, interface, change, name, to_set, results)

    fwmark = change["attributes"].get("fwmark")
    if fwmark is not None and fwmark != interface.get("fwmark"):
        to_set["fwmark"] = fwmark
        change["restart"] = True

    SYS_CMD.update_wg_cnf(cnf, name, to_set, None, results)
    _restart_if_wiresock(cnf, change)


def _update_interface_private_key(cnf, interface, change, name, to_set, results):
    """Updates the private key of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    pk = change["attributes"].get("private_key")
    if pk is not None and pk != interface.get("private_key"):
        to_set["private_key"] = pk
        if interface.get("up"):
            if pk:
                with _named_temporary_file() as (f, close_file):
                    f.write(pk)
                    f.write("\n")
                    close_file()
                    SYS_CMD.set_interface(cnf, name, "private-key", f.name, results)
            else:
                SYS_CMD.set_interface(cnf, name, "private-key", devnull, results)
        interface["private_key"] = pk


def _update_interface_port(cnf, interface, change, name, to_set, results):
    """Updates the listen port of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    port = change["attributes"].get("listen_port") or change["attributes"].get("port")
    if port is not None and port != interface.get("listen_port"):
        to_set["port"] = port
        if interface.get("up"):
            SYS_CMD.set_interface(cnf, name, "listen-port", str(port), results)
        interface["listen_port"] = port


def update_routing(cnf, interfaces, change):
    """Updates the routing info for an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    to_set = {}
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)

    _update_routing_address(cnf, interface, change, name, to_set, results)
    _update_routing_dns(cnf, interface, change, name, to_set, results)
    _update_routing_mtu(cnf, interface, change, name, to_set, results)
    _update_routing_table(cnf, interface, change, name, to_set, results)
    _update_routing_scripts(cnf, interface, change, name, to_set, results)

    SYS_CMD.update_wg_cnf(cnf, name, to_set, None, results)
    _restart_if_wiresock(cnf, change)


def _update_routing_address(_cnf, interface, change, name, to_set, results):
    """Updates the address list of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    new_addresses = change["attributes"].get("address")
    old_addresses = interface.get("address") or []
    if new_addresses is not None:
        for x in old_addresses:
            if x not in new_addresses:
                to_set["address"] = new_addresses
                if interface.get("up"):
                    SYS_CMD.update_address("del", x, name, results)
        for x in new_addresses:
            if x not in old_addresses:
                to_set["address"] = new_addresses
                if interface.get("up"):
                    SYS_CMD.update_address("add", x, name, results)
        interface["address"] = new_addresses


def _update_routing_dns(_cnf, interface, change, name, to_set, results):
    """Updates the DNS list of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    dns = change["attributes"].get("dns")
    search = change["attributes"].get("search")
    if dns is None and search is None:
        return

    old_dns, old_search = separate_dns_and_search(interface.get("dns"))
    if dns is None:
        dns = old_dns
    if search is None:
        search = old_search
    if dns == old_dns and search == old_search:
        return

    to_set["dns"] = dns
    to_set["search"] = search
    if interface.get("up"):
        SYS_CMD.update_dns(dns, search, name, results)
    combined = dns + search if dns and search else dns if dns else search
    interface["dns"] = ",".join(combined)


def _update_routing_mtu(_cnf, interface, change, name, to_set, results):
    """Updates the MTU of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    mtu = change["attributes"].get("mtu")
    if mtu is not None and mtu != interface.get("mtu"):
        to_set["mtu"] = mtu
        if mtu == 0:
            change["restart"] = True
        elif interface.get("up"):
            SYS_CMD.update_mtu(mtu, name, results)
        interface["mtu"] = mtu


def _update_routing_table(_cnf, interface, change, _name, to_set, _results):
    """Updates the routing table of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    table = change["attributes"].get("table")
    if table is not None and table != interface.get("table"):
        to_set["table"] = table
        # update_endpoint() needs to know the table to add routes to
        interface["new_table"] = table or "auto"
        change["restart"] = True


def _update_routing_scripts(_cnf, interface, change, _name, to_set, _results):
    """Updates the scripts of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    for key in ["extras", "pre_up", "post_up", "save_config"]:
        value = change["attributes"].get(key)
        if value is not None and value != interface.get(key):
            to_set[key] = value
            if key != "save_config":
                change["restart"] = True


def update_endpoint(cnf, interfaces, change):
    """Updates an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    to_set = {k: change["attributes"].get(k) for k in ["id", "name", "public_key"]}
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)
    pk = change["attributes"].get("public_key")
    peer = interface["peers"].get(pk)
    if not peer:
        interface["peers"][pk] = peer = {}

    old_table = interface.get("table") or "auto"
    new_table = interface.get("new_table") or old_table
    not_auto_table = old_table != "auto" and new_table != "auto"

    new_allowed_ips = change["attributes"].get("allowed_ips")
    old_allowed_ips = peer.get("allowed_ips") or []
    default_route = _uses_default_route(old_allowed_ips) or _uses_default_route(
        new_allowed_ips
    )
    allowed_ips_different = new_allowed_ips is not None and set(
        old_allowed_ips
    ).symmetric_difference(new_allowed_ips)

    if _restart_if_wiresock(cnf, change):
        to_set = change["attributes"]

    elif not_auto_table or not default_route or not allowed_ips_different:
        _update_endpoint_preshared_key(
            cnf, interface, peer, change, name, pk, to_set, results
        )
        if allowed_ips_different:
            _update_endpoint_allowed_ips(
                cnf,
                interface,
                peer,
                old_allowed_ips,
                new_allowed_ips,
                name,
                pk,
                old_table,
                new_table,
                to_set,
                results,
            )
        _update_endpoint_address(
            cnf, interface, peer, change, name, pk, to_set, results
        )
        _update_endpoint_keepalive(
            cnf, interface, peer, change, name, pk, to_set, results
        )

    else:
        to_set = change["attributes"]
        change["restart"] = True

    SYS_CMD.update_wg_cnf(cnf, name, {}, [to_set], results)


def _uses_default_route(ips):
    """True if the specified AllowedIPs list should override the default route.

    Arguments:
        ips (list): AllowedIPs list (eg ['0.0.0.0/0, ::/0']).

    Returns:
        boolean: True if should override the default route.
    """
    if ips:
        for ip in ips:
            if "/0" in ip:
                return True
    return False


def _update_endpoint_preshared_key(
    cnf, interface, peer, change, name, pk, to_set, results
):
    """Updates the preshared key of an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        peer (dict): Peer info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        pk (str): Peer public key (eg 'ABC...123=').
        to_set (dict): Dict of peer properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    shared = change["attributes"].get("preshared_key")
    if shared is not None and shared != peer.get("preshared_key"):
        if shared and shared != "off":
            to_set["preshared_key"] = shared
            if interface.get("up"):
                with _named_temporary_file() as (f, close_file):
                    f.write(shared)
                    f.write("\n")
                    close_file()
                    SYS_CMD.set_peer(cnf, name, pk, "preshared-key", f.name, results)
            peer["preshared_key"] = shared
        else:
            to_set["preshared_key"] = ""
            if interface.get("up"):
                SYS_CMD.set_peer(cnf, name, pk, "preshared-key", devnull, results)
            peer["preshared_key"] = ""


def _update_endpoint_allowed_ips(
    cnf,
    interface,
    peer,
    old_allowed_ips,
    new_allowed_ips,
    name,
    pk,
    old_table,
    new_table,
    to_set,
    results,
):
    """Updates the allowed IPs list an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        peer (dict): Peer info parsed from wg etc.
        old_allowed_ips (list): Old list of AllowedIPs.
        new_allowed_ips (list): New list of AllowedIPs.
        name (str): Interface name (eg 'wg0').
        pk (str): Peer public key (eg 'ABC...123=').
        old_table (str): Old route table name (eg 'auto').
        new_table (str): New route table name (eg 'off').
        to_set (dict): Dict of peer properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    to_set["allowed_ips"] = new_allowed_ips
    if not interface.get("up"):
        return

    SYS_CMD.set_peer(cnf, name, pk, "allowed-ips", ",".join(new_allowed_ips), results)
    peer["allowed_ips"] = new_allowed_ips

    if old_table != "off":
        for x in old_allowed_ips:
            if x not in new_allowed_ips:
                SYS_CMD.update_route("del", x, name, old_table, results)

    if new_table != "off":
        for x in new_allowed_ips:
            if x not in old_allowed_ips:
                SYS_CMD.update_route("add", x, name, new_table, results)


def _update_endpoint_address(cnf, interface, peer, change, name, pk, to_set, results):
    """Updates the endpoint address an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        peer (dict): Peer info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        pk (str): Peer public key (eg 'ABC...123=').
        to_set (dict): Dict of peer properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    endpoint = change["attributes"].get("endpoint")
    if endpoint is None:
        return

    old_endpoint = peer.get("endpoint") or ""
    old_hostname = peer.get("hostname") or ""
    if old_hostname:
        old_ip, old_port, _ = split_endpoint_address(old_endpoint)
        old_endpoint = f"{old_hostname}:{old_port}" if old_ip else old_hostname

    if endpoint != old_endpoint:
        to_set["endpoint"] = endpoint
        if endpoint and interface.get("up"):
            SYS_CMD.set_peer(cnf, name, pk, "endpoint", endpoint, results)
        peer["endpoint"] = endpoint
        peer.pop("hostname", None)


def _update_endpoint_keepalive(cnf, interface, peer, change, name, pk, to_set, results):
    """Updates the keepalive value an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        peer (dict): Peer info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        pk (str): Peer public key (eg 'ABC...123=').
        to_set (dict): Dict of peer properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    keepalive = change["attributes"].get("keepalive")
    if keepalive is not None and keepalive != peer.get("persistent_keepalive"):
        to_set["keepalive"] = keepalive
        if interface.get("up"):
            SYS_CMD.set_peer(
                cnf, name, pk, "persistent-keepalive", str(keepalive), results
            )
        peer["persistent_keepalive"] = keepalive


def create_interface(cnf, _interfaces, change):
    """Sets up a new interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    change["restart"] = True
    results = change["results"]
    name = change["interface"]
    to_set = change["attributes"]
    SYS_CMD.create_wg_cnf(cnf, name, to_set, None, results)


def create_routing(cnf, interfaces, change):
    """Sets up the routing info for a new interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    create_interface(cnf, interfaces, change)


def create_endpoint(cnf, _interfaces, change):
    """Sets up a new peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    change["restart"] = True
    results = change["results"]
    name = change["interface"]
    to_set = change["attributes"]
    SYS_CMD.update_wg_cnf(cnf, name, {}, [to_set], results)
    _restart_if_wiresock(cnf, change)


def rename_interface(cnf, interfaces, change):
    """Renames an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    results = change["results"]
    old_name = change["interface"]
    new_name = change["attributes"].get("rename")

    if not new_name or new_name == old_name:
        update_interface(cnf, interfaces, change)
    elif SYS_CMD.check_wg_cnf(cnf, old_name, results) == "found":
        change["interface"] = new_name
        change["restart"] = True
        SYS_CMD.rename_wg_cnf(cnf, old_name, new_name, results)
    else:
        change["interface"] = new_name
        create_interface(cnf, interfaces, change)


def start_up_interface(cnf, _interfaces, name, changes):
    """Starts up a new or existing interface for a list of desired changes.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        name (str): Interface name to start up (eg `wg0`).
        changes (list): List of desired change objects.
    """
    results = []
    SYS_CMD.start_service(cnf, name, results)
    for x in changes:
        x["results"].extend(results)


def update_down_script(cnf, interfaces, change):
    """Updates the routing info for an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    to_set = {}
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)

    for key in ["pre_down", "post_down"]:
        value = change["attributes"].get(key)
        if value is not None and value != interface.get(key):
            to_set[key] = value

    SYS_CMD.update_wg_cnf(cnf, name, to_set, None, results)


def _is_shut_down_interface(cnf, interfaces, change):
    """Checks if the specified change object should shut down an interface.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should shut down an interface.
    """
    return (
        _is_interface_up(cnf, interfaces, change)
        and (
            change["type"] == "desired_interfaces"
            and (
                change["attributes"].get("up") is False
                or change["attributes"].get("delete")
                or change["attributes"].get("rename")
            )
        )
    ) or (change["type"] == "desired_routings" and change["attributes"].get("extras"))


def _is_delete_interface(_interfaces, change):
    """Checks if the specified change object should delete an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should delete an interface
    """
    return change["type"] == "desired_interfaces" and change["attributes"].get("delete")


def _is_delete_endpoint(_interfaces, change):
    """Checks if the specified change object should delete a peer.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should delete a peer.
    """
    return change["type"] == "desired_endpoints" and change["attributes"].get("delete")


def _is_update_interface(interfaces, change):
    """Checks if the specified change object should update an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should update an interface.
    """
    return (
        change["type"] == "desired_interfaces"
        and not change["attributes"].get("delete")
        and interfaces.get(change["interface"])
    )


def _is_update_routing(interfaces, change):
    """Checks if the specified change object should update the routing for an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should update the routing.
    """
    return change["type"] == "desired_routings" and interfaces.get(change["interface"])


def _is_update_endpoint(interfaces, change):
    """Checks if the specified change object should update a peer.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should update a peer.
    """
    return (
        change["type"] == "desired_endpoints"
        and not change["attributes"].get("delete")
        and interfaces.get(change["interface"])
    )


def _is_create_interface(interfaces, change):
    """Checks if the specified change object should create an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should create an interface.
    """
    return (
        change["type"] == "desired_interfaces"
        and not change["attributes"].get("delete")
        and not change["attributes"].get("rename")
        and not interfaces.get(change["interface"])
    )


def _is_create_routing(interfaces, change):
    """Checks if the specified change object should create the routing for an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should create the routing.
    """
    return change["type"] == "desired_routings" and not interfaces.get(
        change["interface"]
    )


def _is_create_endpoint(interfaces, change):
    """Checks if the specified change object should create a peer.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should create a peer.
    """
    return (
        change["type"] == "desired_endpoints"
        and not change["attributes"].get("delete")
        and not interfaces.get(change["interface"])
    )


def _is_rename_interface(_interfaces, change):
    """Checks if the specified change object should rename an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should rename an interface.
    """
    return (
        change["type"] == "desired_interfaces"
        and not change["attributes"].get("delete")
        and change["attributes"].get("rename")
    )


def _is_start_up_interface(cnf, interfaces, change):
    """Checks if the specified change object should start up an interface.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should start up an interface.
    """
    return (
        change["attributes"].get("restart")
        or (change.get("restart") and _is_interface_up(cnf, interfaces, change))
        or (
            (change["attributes"].get("up") or change["attributes"].get("was_up"))
            and not change["attributes"].get("delete")
            and not _is_interface_up(cnf, interfaces, change)
        )
    )


def _is_interface_up(cnf, interfaces, change):
    """Checks if the specified change object's interface is currently up.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if the interface is up.
    """
    if cnf.wiresock:
        if not cnf.get("wiresock_service_status_checked"):
            cnf.wiresock_service_status = _sc_query_state(cnf, "")
            cnf.wiresock_service_status_checked = True
        state = cnf.wiresock_service_status
        return state and state != "STOPPED"
    interface = interfaces.get(change["interface"])
    return interface and interface.get("up")


def _is_update_down_script(cnf, interfaces, change):
    """Checks if the specified change object should update the down scripts.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should update the down scripts.
    """
    return change["type"] == "desired_routings" and _is_interface_up(
        cnf, interfaces, change
    )


def _restart_if_wiresock(cnf, change):
    """Flags need to restart if running WireSock.

    Arguments:
        cnf (Config): Config object.
        change (dict): Desired change object.

    Returns:
        boolean: True if using wiresock.
    """
    if cnf.wiresock:
        change["restart"] = True
        return True
    return False


@contextmanager
def _named_temporary_file():
    """Opens a named temporary file for writing.

    Yields:
        tuple: File object to write, function to close the file.
    """
    if system() == "Windows":
        # file must be closed and deleted explicitly on windows
        with NamedTemporaryFile(mode="w", buffering=1, delete=False) as f:
            try:
                yield f, lambda: f.close()
            finally:
                f.close()
                unlink(f.name)  # noqa: PTH108
    else:
        # file will be closed & deleted automatically when exiting context manager
        with NamedTemporaryFile(mode="w", buffering=1) as f:
            yield f, lambda: None
