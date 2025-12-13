"""WireGuard utilities."""

import re
from base64 import b64decode, b64encode
from hashlib import sha256
from pathlib import Path
from platform import system
from subprocess import PIPE, run

from nacl.encoding import Base64Encoder
from nacl.public import PrivateKey


def get_wg_version(cnf):
    """Returns WireGuard client version.

    Arguments:
        cnf (Config): Config object.

    Returns:
        str: Version string (eg '1.2.3').
    """
    if system() == "Windows":
        return _get_windows_wg_version(cnf)
    return _get_standard_wg_version(cnf)


def _get_standard_wg_version(cnf):
    """Returns standard WireGuard client version.

    Arguments:
        cnf (Config): Config object.

    Returns:
        str: Version string (eg '1.2.3').
    """
    result = run([cnf.wg, "--version"], stdout=PIPE, check=False)  # noqa: S603
    output = result.stdout.decode("utf-8")
    return re.search(r"\sv(\S+)", output)[1]


def _get_windows_wg_version(cnf):
    """Returns Windows WireGuard client version.

    Arguments:
        cnf (Config): Config object.

    Returns:
        str: Version string (eg '1.2.3').
    """
    exe = _get_windows_wireguard_exe(cnf)
    escaped = re.sub(r"[/\\]", r"\\\\", str(exe))
    try:
        args = [f"(Get-Item -path '{escaped}').VersionInfo.ProductVersion"]
        result = run(["powershell", *args], stdout=PIPE, check=False)  # noqa: S603 S607
        return result.stdout.decode("utf-8").strip()
    except OSError:
        args = ["datafile", "where", f"name='{escaped}'", "get", "version", "/value"]
        result = run(["wmic", *args], stdout=PIPE, check=False)  # noqa: S603 S607
        output = result.stdout.decode("utf-8").strip()
        return re.sub(r"Version=", "", output)


def _get_windows_wireguard_exe(cnf):
    """Returns path to Windows WireGuard client.

    Arguments:
        cnf (Config): Config object.

    Returns:
        Path: Path to WireGuard executable.
    """
    wg = Path(cnf.wg)
    if cnf.wiresock:
        return wg
    directory = wg.parent
    if not directory.name:
        directory = Path("C:/Program Files/WireGuard/")
    return Path(directory, "wireguard.exe")


def run_wg_set(cnf, args):
    """Runs `wg set` command.

    Arguments:
        cnf (Config): Config object.
        args: Command arguments.
    """
    if not cnf.wiresock:
        run([cnf.wg, "set", *args], check=False)  # noqa: S603


def run_wg_show(cnf):
    """Runs `wg show` command.

    Arguments:
        cnf (Config): Config object.

    Returns:
        str: Output of `wg show` command.
    """
    if cnf.wiresock:
        return ""
    result = run([cnf.wg, "show", "all", "dump"], stdout=PIPE, check=False)  # noqa: S603
    return result.stdout.decode("utf-8")


def parse_wg_show(s):
    """Parses `wg show` command output into a dict.

    Raises:
        ValueError: Output can't be parsed.

    Arguments:
        s (str): Output of `wg show` command.

    Returns:
        dict: Output of `wg show` command as a dict.
    """
    result = {}

    for line in s.splitlines():
        fields = line.split()
        len_fields = len(fields)

        if len_fields == 0:
            pass
        elif len_fields == 5:
            _add_interface(result, fields)
        elif len_fields == 9:
            _add_peer(result, fields)
        else:
            raise ValueError("can't parse line from wg show", line)

    return result


def annotate_wg_show(dst, src):
    """Copies properties from source interfaces to destination interfaces.

    Arguments:
        dst (str): Output of `wg show` command as dict.
        src (str): Output of `wg show` command as dict.

    Returns:
        dict: Dst dict updated with interface properties.
    """
    _default_all_endpoints_unavailable(dst)
    for name, src_iface in src.items():
        dst_iface = dst.get(name)
        if dst_iface:
            _annotate_wg_show_interface(dst_iface, src_iface)
    return dst


def _default_all_endpoints_unavailable(interfaces):
    """Defaults interfaces to down and peers unavailable.

    Arguments:
        interfaces (str): Output of `wg show` command as dict.

    Returns:
        dict: Dict updated with interface properties.
    """
    for iface in interfaces.values():
        iface["up"] = False
        peers = iface.get("peers")
        if peers:
            for peer in peers.values():
                peer["available"] = False


def _annotate_wg_show_interface(dst, src):
    """Copies properties from source interface to destination interface.

    Arguments:
        dst (str): One interface from output of `wg show` command as dict.
        src (str): One interface from output of `wg show` command as dict.

    Returns:
        dict: Dst dict updated with interface properties.
    """
    dst_peers = dst.get("peers")
    for name, src_value in src.items():
        if name == "peers" and dst_peers:
            _annotate_wg_show_peers(dst_peers, src_value)
        else:
            dst[name] = src_value
    return dst


def _annotate_wg_show_peers(dst, src):
    """Copies properties from source peer to destination peer.

    Arguments:
        dst (str): One peer from output of `wg show` command as dict.
        src (str): One peer from output of `wg show` command as dict.

    Returns:
        dict: Dst dict updated with peer properties.
    """
    for pubkey, src_peer in src.items():
        dst_peer = dst.get(pubkey)
        if dst_peer:
            dst_peer.update(src_peer)
        else:
            dst[pubkey] = src_peer


def update_socket_mark(data, cnf):
    """Updates the active socket mark with a new mark from the parsed interfaces.

    Arguments:
        data (dict): Dict parsed from `wg show` command.
        cnf (Config): Config object.

    Returns:
        dict: Same dict.
    """
    # don't override explicitly configured mark
    if cnf.fw_mark:
        return data
    fwmark = _get_fwmark_for_default_peer(data)
    # reset mark consumers if changed
    if cnf.socket_mark != fwmark:
        cnf.socket_mark = fwmark
        cnf.resolver = None
        cnf.transport = None
    return data


def filter_wg_show(data, cnf):
    """Removes configured elements from parsed output of `wg show`.

    Arguments:
        data (dict): Dict parsed from `wg show` command.
        cnf (Config): Config object.

    Returns:
        dict: Same dict with some items removed.
    """
    for interface in cnf.unmanaged_interfaces:
        data.pop(interface, None)
    if cnf.redact_secrets:
        data = remove_secrets_from_wg_show(data)
    elif cnf.redact_psk:
        data = remove_secrets_from_wg_show(data, psk_only=True)
    return data


def remove_secrets_from_wg_show(data, *, psk_only=False):
    """Removes secrets from parsed output of `wg show`.

    Arguments:
        data (dict): Dict parsed from `wg show` command.
        psk_only (bool): True to remove only preshared keys from output (default false).

    Returns:
        dict: Same dict with secret items removed.
    """
    for interface in data.values():
        if not psk_only:
            interface.pop("private_key", None)
        for peer in interface["peers"].values():
            peer.pop("preshared_key", None)
    return data


def _add_interface(result, fields):
    """Adds the the specified interface fields to the result.

    Arguments:
        result (dict): Result dict.
        fields (list): List of field values.
    """
    interface, private, public, port, fwmark = fields
    result[interface] = {
        "up": True,
        "private_key": private if private != "(none)" else "",
        "public_key": public if public != "(none)" else "",
        "listen_port": int(port),
        "fwmark": int(fwmark, 0) if fwmark != "off" else 0,
        "peers": {},
    }


def _add_peer(result, fields):
    """Adds the the specified peer fields to the result.

    Arguments:
        result (dict): Result dict.
        fields (list): List of field values.
    """
    interface, public, preshared, endpoint, ips, handshake, rx, tx, keepalive = fields
    result[interface]["peers"][public] = {
        "available": True,
        "preshared_key": preshared if preshared != "(none)" else "",
        "preshared_key_hash": hash_preshared_key(preshared),
        "endpoint": endpoint if endpoint != "(none)" else "",
        "allowed_ips": ips.split(",") if ips != "(none)" else [],
        "latest_handshake": int(handshake),
        "transfer_rx": int(rx),
        "transfer_tx": int(tx),
        "persistent_keepalive": int(keepalive) if keepalive != "off" else 0,
    }


def derive_public_key(key):
    """Derives the public key from the specified private key.

    Arguments:
        key (str): Private key as a base64 string.

    Returns:
        str: Public key as a base64 string.
    """
    if not key or key == "(none)":
        return ""
    public_key = PrivateKey(key, Base64Encoder).public_key
    return public_key.encode(Base64Encoder).decode("utf-8")


def hash_preshared_key(key):
    """Hashes the specified key.

    Arguments:
        key (str): Base64-encoded key to hash.

    Returns:
        str: Hash of raw key bytes as base64 string.
    """
    if not key or key == "(none)":
        return ""
    return b64encode(sha256(b64decode(key.encode())).digest()).decode()


def separate_dns_and_search(items):
    """Separates the specified list into DNS servers and search domains.

    Arguments:
        items (list): Mixed list of DNS servers and search domains.

    Returns:
        tuple: List of DNS servers, list of search domains.
    """
    dns = []
    search = []
    if items:
        for item in items:
            if re.search("[A-Za-z]", item) and ":" not in item:
                search.append(item)
            else:
                dns.append(item)
    return dns, search


def _get_fwmark_for_default_peer(data):
    """Returns the fwmark for the first interface with peer with a default route.

    Arguments:
        data (dict): Dict parsed from `wg show` command.

    Returns:
        str: Socket mark or blank.
    """
    for name in sorted(data):
        interface = data[name]
        fwmark = interface.get("fwmark")
        if fwmark:
            for peer in interface["peers"].values():
                for ip in peer.get("allowed_ips", []):
                    if ip.endswith("/0"):
                        return fwmark
    return ""
