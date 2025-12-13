"""Routing and addressing utilities."""

import time
from ipaddress import IPv4Address, IPv4Interface
from itertools import zip_longest
from json import loads
from platform import system
from re import fullmatch, match, sub
from subprocess import PIPE, run

FAKE_WIRESOCK_HANDSHAKES = {}


def run_ip_address_show(device):
    """Runs `ip address show` command for specified device.

    Arguments:
        device (str): Device name (eg 'wg0').

    Returns:
        dict: Parsed JSON from `ip --json address show` command.
    """
    args = ["ip", "--json", "address", "show", "dev", device]
    result = run(args, stdout=PIPE, check=False)  # noqa: S603
    output = result.stdout.decode("utf-8")
    return loads(output)[0] if fullmatch(r"\[\{.*\}\]\s*", output) else {}


def run_netsh_show_addresses(device):
    """Runs `netsh` addresses command for specified device.

    Arguments:
        device (str): Device name (eg 'wg0').

    Returns:
        list: Lines from `netsh` command.
    """
    ipv4 = _run_netsh_show_addresses_for_family(device, "ipv4")
    ipv6 = _run_netsh_show_addresses_for_family(device, "ipv6")
    return ipv4 + ipv6


def _run_netsh_show_addresses_for_family(device, family):
    """Runs `netsh` addresses command for specified device and IP version.

    Arguments:
        device (str): Device name (eg 'wg0').
        family (str): IP family ('ipv4' or 'ipv6')

    Returns:
        list: Lines from `netsh` command.
    """
    args = ["netsh", "interface", family, "show", "addresses", device]
    result = run(args, stdout=PIPE, check=False)  # noqa: S603
    output = result.stdout.decode("utf-8")
    return [x.strip() for x in output.split("\n")]


def run_ifconfig(device):
    """Runs `ifconfig` command for specified device.

    Arguments:
        device (str): Device name (eg 'wg0').

    Returns:
        list: Lines from `ifconfig` command.
    """
    args = ["ifconfig", device]
    result = run(args, stdout=PIPE, check=False)  # noqa: S603
    output = result.stdout.decode("utf-8")
    return [x.strip() for x in output.split("\n")]


def annotate_wg_show_with_ip_address_show(interfaces):
    """Annotates parsed output of `wg show` with output of `ip address show`.

    Arguments:
        interfaces (dict): Dict parsed from `wg show` command.

    Returns:
        dict: Same dict with additional properties.
    """
    for name, properties in interfaces.items():
        _annotate_interface(name, properties)
        properties["up"] = bool(properties.get("address"))
    return interfaces


def _annotate_interface(name, properties):
    """Annotates specified dict with wg config for specified interface.

    Arguments:
        name (str): Interface name (eg 'wg0').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    if system() == "Linux":
        _annotate_interface_with_ip_address_show(name, properties)
    elif system() == "Windows":
        _annotate_interface_with_netsh_show_addresses(name, properties)
    else:
        _annotate_interface_with_ifconfig(name, properties)
    return properties


def _annotate_interface_with_ip_address_show(name, properties):
    """Annotates specified dict with wg config for specified interface.

    Arguments:
        name (str): Interface name (eg 'wg0').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    info = run_ip_address_show(name)
    if info:
        properties["address"] = [_format_address_info(a) for a in info["addr_info"]]
    return properties


def _format_address_info(info):
    """Formats the addr_info object from `ip address show` as a CIDR.

    Arguments:
        info (dict): addr_info object.

    Returns:
        string: CIDR.
    """
    return f"{info['local']}/{info['prefixlen']}"


def _annotate_interface_with_netsh_show_addresses(name, properties):
    """Annotates specified dict with wg config for specified interface.

    Arguments:
        name (str): Interface name (eg 'wg0').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    output = run_netsh_show_addresses(name)
    addresses = list(filter(None, [_parse_netsh_address(x) for x in output]))

    if addresses:
        prefixes = list(filter(None, [_parse_netsh_prefix_length(x) for x in output]))
        combined = [f"{a}/{p}" if p else a for a, p in zip_longest(addresses, prefixes)]
        properties["address"] = combined

    return properties


def _parse_netsh_address(line):
    """Parses the ip address out of the specified netsh output line.

    Arguments:
        line (str): netsh output line (eg 'IP Address:    10.0.0.1').

    Returns:
        str: Address or empty string (eg '10.0.0.1').
    """
    m = match(r"(?:IP )?Address:?\s+([\da-f.:%]+)", line)
    return m.group(1) if m else ""


def _parse_netsh_prefix_length(line):
    """Parses the subnet prefix length out of the specified netsh output line.

    Arguments:
        line (str): netsh output line (eg 'Subnet Prefix:    10.0.0.0/24').

    Returns:
        int: Prefix or None (eg 0).
    """
    m = match(r"Subnet Prefix:\s+[\da-f.:%]+/(\d+).*", line)
    return int(m.group(1)) if m else None


def _annotate_interface_with_ifconfig(name, properties):
    """Annotates specified dict with wg config for specified interface.

    Arguments:
        name (str): Interface name (eg 'wg0').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    addresses = list(filter(None, [_parse_inet_address(x) for x in run_ifconfig(name)]))
    if addresses:
        properties["address"] = addresses
    return properties


def _parse_inet_address(line):
    """Parses the inet or inet6 address out of the specified ifconfig output line.

    Arguments:
        line (str): ifconfig output line (eg 'inet6 ffc0:: prefixlen 64').

    Returns:
        str: CIDR or empty string (eg 'ffc0::/64').
    """
    if not line.startswith("inet"):
        return ""

    parts = line.split()
    if len(parts) < 4:
        return ""
    if parts[2] == "-->" and len(parts) >= 6:
        del parts[2:4]

    return _format_inet_address_parts(parts)


def _format_inet_address_parts(parts):
    """Formats the specified ifconfig output tokens as a CIDR.

    Arguments:
        parts (list): ifconfig output tokens
            (eg ['inet6', 'ffc0::', 'prefixlen', '64']).

    Returns:
        str: CIDR or empty string (eg 'ffc0::/64').
    """
    if parts[1] == "addr:":
        return _strip_interface_id(parts[2])
    if parts[1].startswith("addr:"):
        ip = parts[1][5:]
        mask = parts[3][5:] if parts[3].startswith("Mask:") else 32
        return str(IPv4Interface((ip, mask)))
    if parts[2] == "prefixlen":
        ip = _strip_interface_id(parts[1])
        mask = parts[3]
        return f"{ip}/{mask}"
    if parts[2] == "netmask":
        ip = _strip_interface_id(parts[1])
        mask = str(IPv4Address(int(parts[3], 16)))
        return str(IPv4Interface((ip, mask)))
    return ""


def _strip_interface_id(ip):
    """Strips the interface number or name from the specified IP address.

    Arguments:
        ip (str): IP address (eg 'fe80::169d:99ff:fe7f:8c67%utun0').

    Returns:
        str: IP address (eg 'fe80::169d:99ff:fe7f:8c67').
    """
    return sub(r"%[^/]*", "", ip)


def annotate_wg_show_with_up(interfaces):
    """Annotates parsed output of `wg show` with 'up' property.

    Arguments:
        interfaces (dict): Dict parsed from `wg show` command.

    Returns:
        dict: Same dict with additional properties.
    """
    output = []
    for name, properties in interfaces.items():
        if not output:
            output = _run_netsh_show_interface()
        properties["up"] = _parse_up_for_interface(output, name)
    return interfaces


def _run_netsh_show_interface(device=None):
    """Runs `netsh` interface command for specified device.

    Arguments:
        device (str): Device name (eg 'wg0').

    Returns:
        list: Lines from `netsh` command.
    """
    args = ["netsh", "interface", "show", "interface"]
    if device:
        args.append(device)
    result = run(args, stdout=PIPE, check=False)  # noqa: S603
    output = result.stdout.decode("utf-8")
    return [x.split() for x in output.split("\n")]


def _parse_up_for_interface(rows, device):
    """Calculates whether the specified device is up or not.

    Arguments:
        rows (list): Netsh subinterfaces output as a list of a list of columns.
        device (str): Device name (eg 'wg0').

    Returns:
        int: Total or 0.
    """
    for row in rows:
        if len(row) > 3 and row[3] == device:
            return row[0] == "Enabled" and row[1] == "Connected"
    return False


def annotate_wg_show_with_tx(interfaces):
    """Annotates parsed output of `wg show` with peer tx and rx.

    Arguments:
        interfaces (dict): Dict parsed from `wg show` command.

    Returns:
        dict: Same dict with additional properties.
    """
    output = []
    for name, properties in interfaces.items():
        peers = properties.get("peers", [])
        if len(peers) == 1 and properties.get("up"):
            if not output:
                output = run_netsh_show_subinterfaces()
            peer = next(iter(peers.values()))
            peer["transfer_rx"] = _parse_total_for_subinterface(output, name, 2)
            peer["transfer_tx"] = _parse_total_for_subinterface(output, name, 3)
            _fake_wiresock_handshake(name, peer)
    return interfaces


def run_netsh_show_subinterfaces(device=None):
    """Runs `netsh` subinterfaces command for specified device.

    Arguments:
        device (str): Device name (eg 'wg0'); default all devices.

    Returns:
        list: Lines from `netsh` command.
    """
    ipv4 = _run_netsh_show_subinterfaces_for_family(device, "ipv4")
    ipv6 = _run_netsh_show_subinterfaces_for_family(device, "ipv6")
    return ipv4 + ipv6


def _run_netsh_show_subinterfaces_for_family(device, family):
    """Runs `netsh` subinterfaces command for specified device and IP version.

    Arguments:
        device (str): Device name (eg 'wg0').
        family (str): IP family ('ipv4' or 'ipv6')

    Returns:
        list: Lines from `netsh` command.
    """
    args = ["netsh", "interface", family, "show", "subinterfaces"]
    if device:
        args.append(device)
    result = run(args, stdout=PIPE, check=False)  # noqa: S603
    output = result.stdout.decode("utf-8")
    return [x.split() for x in output.split("\n")]


def _parse_total_for_subinterface(rows, device, column):
    """Calculates the total of a subinterfaces column for the specified device.

    Arguments:
        rows (list): Netsh subinterfaces output as a list of a list of columns.
        device (str): Device name (eg 'wg0').
        column (int): Zero-based column (eg 2).

    Returns:
        int: Total or 0.
    """
    total = 0
    for row in rows:
        if len(row) > 4 and row[4] == device:
            total += int(row[column])
    return total


def _fake_wiresock_handshake(device, peer):
    """Fakes the latest_handshake time for WireSock.

    (So that the API will record an entry for the transfer stats.)

    Arguments:
        device (str): Device name (eg 'wg0').
        peer (dict): Peer properties to read and update.
    """
    rx = peer.get("transfer_rx")
    tx = peer.get("transfer_tx")
    # skip if device has not transferred anything ever
    if not rx and not tx:
        return

    fake = FAKE_WIRESOCK_HANDSHAKES.get(device)
    if not fake:
        fake = {"rx": 0, "tx": 0, "handshake": 0}
        FAKE_WIRESOCK_HANDSHAKES[device] = fake

    # skip if device has not transferred anything since last time
    if rx <= fake["rx"] and tx <= fake["tx"]:
        return

    handshake = int(time.time())
    # don't increment handshake if less than 2 minutes since last time
    if handshake <= fake["handshake"] + 120:
        handshake = fake["handshake"]

    fake["rx"] = rx
    fake["tx"] = tx
    fake["handshake"] = handshake
    peer["latest_handshake"] = handshake
