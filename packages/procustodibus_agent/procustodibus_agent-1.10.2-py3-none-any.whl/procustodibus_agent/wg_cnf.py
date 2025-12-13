"""Utilities for manipulating wq conf ini."""

from contextlib import suppress
from logging import DEBUG, getLogger
from pathlib import Path
from platform import system

from inflection import underscore

from procustodibus_agent import __version__ as version
from procustodibus_agent.api import format_datetime
from procustodibus_agent.cnf import (
    WIREGUARD_SPLITTABLE,
    find_ini_section_with_line,
    join_ini_splittable_lines,
    load_ini,
    load_ini_lines,
    rename_ini,
    replace_ini_line_value,
    save_ini_lines,
)
from procustodibus_agent.extras import (
    annotate_extras_from_peers,
    annotate_extras_from_scripts,
    apply_extras_to_peers,
    apply_extras_to_scripts,
    rewrite_extra_scripts_to_ini_section,
    rewrite_ini_section_to_extra_scripts,
)
from procustodibus_agent.resolve_hostname import (
    resolve_endpoint_hostname,
    split_endpoint_hostname_and_port,
)
from procustodibus_agent.wg import derive_public_key, hash_preshared_key


def load_all_from_wg_cnf(cnf):
    """Loads equivalent of `wg show` from wg all configs.

    Arguments:
        cnf (Config): Config object.

    Returns:
        dict: Interfaces.
    """
    directory = Path(cnf.wg_cnf_dir)
    if not cnf.wg_cnf_dir or not directory.is_dir():
        return {}

    suffix = ".conf.dpapi" if system() == "Windows" else ".conf"
    interfaces = {}
    for f in directory.glob(f"*{suffix}"):
        name = f.name[: -len(suffix)]
        interface = load_interface_from_wg_cnf(cnf, name)
        if interface:
            interfaces[name] = interface
    return interfaces


def load_interface_from_wg_cnf(cnf, name):
    """Loads equivalent of `wg show` from specified wg config.

    Arguments:
        cnf (Config): Config object.
        name (str): Interface name (eg 'wg0').

    Returns:
        dict: Interface properties
    """
    properties = {}
    path = find_wg_cnf_path(cnf, name)
    try:
        if not path.exists():
            return properties
    except PermissionError:
        return properties

    ini = load_ini(path, WIREGUARD_SPLITTABLE)
    interface = ini.get("interface")
    if not interface:
        return properties

    _core_interface_properties(properties, interface[0])
    _derive_public_key(properties)
    _annotate_interface_properties(properties, interface[0])
    annotate_extras_from_scripts(cnf, properties)
    _core_interface_peers(cnf, properties, ini)
    annotate_extras_from_peers(cnf, properties)
    return properties


def _core_interface_properties(properties, ini):
    """Loads core interface properties from specified wg config.

    Arguments:
        properties (dict): Dict of interface properties.
        ini (dict): Dict of interface config from wg ini.

    Returns:
        dict: Same dict with additional properties.
    """
    # string properties
    for key in ["private_key"]:
        values = ini.get(key)
        if values:
            properties[key] = values[0]

    # integer properties
    for key, ini_key in {"fwmark": "fw_mark", "listen_port": "listen_port"}.items():
        values = ini.get(ini_key)
        if values:
            v = values[0]
            with suppress(ValueError):
                properties[key] = int(v, 16) if v.startswith("0x") else int(v)

    return properties


def _core_interface_peers(cnf, interface, ini):
    """Loads core interface peers from specified wg config.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Dict of interface properties.
        ini (dict): Dict of full config from wg ini.

    Returns:
        dict: Same dict with additional properties.
    """
    peers = {}
    for peer in ini.get("peer", []):
        properties = _core_peer_properties(peer)
        public_key = properties.pop("public_key", None)
        if public_key:
            peers[public_key] = properties
            _wiresock_peer_properties(cnf, peer, properties)
            _hash_preshared_key(properties)
            _resolve_endpoint(cnf, properties)
    interface["peers"] = peers
    return interface


def _core_peer_properties(ini):
    """Loads core peer properties from specified wg config.

    Arguments:
        ini (dict): Dict of peer config from wg ini.

    Returns:
        dict: Peer properties
    """
    properties = {}

    # string properties
    for key in ["endpoint", "preshared_key", "public_key"]:
        values = ini.get(key)
        if values:
            properties[key] = values[0]

    # integer properties
    for key in ["persistent_keepalive"]:
        values = ini.get(key)
        if values:
            with suppress(ValueError):
                properties[key] = int(values[0])

    # list properties
    for key in ["allowed_ips"]:
        values = ini.get(key)
        if values:
            properties[key] = values

    return properties


def _wiresock_peer_properties(cnf, ini, properties):
    """Loads core peer properties from specified wg config.

    Arguments:
        cnf (Config): Config object.
        ini (dict): Dict of peer config from wg ini.
        properties (dict): Dict of peer properties.

    Returns:
        dict: Peer properties
    """
    if not cnf.wiresock:
        return properties

    # string properties
    for key in ["socks5_proxy", "socks5_proxy_username", "socks5_proxy_password"]:
        values = ini.get(key)
        if values:
            properties[key] = values[0]

    # boolean properties
    for key in ["socks5_proxy_all_traffic"]:
        values = ini.get(key)
        if values:
            properties[key] = values[0] == "true"

    # list properties
    for key in ["allowed_apps", "disallowed_apps", "disallowed_ips"]:
        values = ini.get(key)
        if values:
            properties[key] = values

    return properties


def _derive_public_key(properties):
    """Adjusts interface properties to derive public key.

    Arguments:
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    private_key = properties.get("private_key")
    if private_key:
        properties["public_key"] = derive_public_key(private_key)
    return properties


def _hash_preshared_key(properties):
    """Adjusts peer properties to hash preshared key.

    Arguments:
        properties (dict): Dict of peer properties.

    Returns:
        dict: Same dict with additional properties.
    """
    preshared_key = properties.get("preshared_key")
    if preshared_key:
        properties["preshared_key_hash"] = hash_preshared_key(preshared_key)
    return properties


def _resolve_endpoint(cnf, properties):
    """Adjusts peer properties to include numeric endpoint and separate hostname.

    Arguments:
        cnf (Config): Config object.
        properties (dict): Dict of peer properties.

    Returns:
        dict: Same dict with additional properties.
    """
    endpoint, hostname, _ = resolve_endpoint_hostname(cnf, properties.get("endpoint"))
    if hostname:
        properties["hostname"] = hostname
        properties["endpoint"] = endpoint
    return properties


def annotate_wg_show_with_wg_cnf(cnf, interfaces):
    """Annotates parsed output of `wg show` with wg config.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Dict parsed from `wg show` command.

    Returns:
        dict: Same dict with additional properties.
    """
    for name, properties in interfaces.items():
        _annotate_interface(cnf, name, properties)
    return interfaces


def find_wg_cnf_path(cnf, name):
    """Returns path to ini file for specified wg interface.

    Arguments:
        cnf (Config): Config object.
        name (str): Interface name (eg 'wg0').

    Returns:
        Path: Path to ini file (eg '/etc/wireguard/wg0.conf').
    """
    directory = cnf.wg_cnf_dir or "/etc/wireguard"
    file_name = f"{name}.conf.dpapi" if system() == "Windows" else f"{name}.conf"
    return Path(directory, file_name)


def _annotate_interface(cnf, name, properties):
    """Annotates specified dict with wg config for specified interface.

    Arguments:
        cnf (Config): Config object.
        name (str): Interface name (eg 'wg0').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    path = find_wg_cnf_path(cnf, name)
    try:
        if not path.exists():
            return properties
    except PermissionError:
        return properties

    ini = load_ini(path, WIREGUARD_SPLITTABLE)
    interface = ini.get("interface")
    if not interface:
        return properties

    _annotate_interface_properties(properties, interface[0])
    annotate_extras_from_scripts(cnf, properties)
    _annotate_interface_peers(properties, ini)
    annotate_extras_from_peers(cnf, properties)
    return properties


def _annotate_interface_properties(properties, ini):
    """Annotates specified interface properties from specified wg config.

    Arguments:
        properties (dict): Dict of interface properties.
        ini (dict): Dict of interface config from wg ini.

    Returns:
        dict: Same dict with additional properties.
    """
    # string properties
    for key in ["table"]:
        values = ini.get(key)
        if values:
            properties[key] = values[0]

    # integer properties
    for key in ["mtu"]:
        values = ini.get(key)
        if values:
            with suppress(ValueError):
                properties[key] = int(values[0])

    # boolean properties
    for key in ["save_config"]:
        values = ini.get(key)
        if values:
            properties[key] = values[0] == "true"

    # list properties
    for key in ["address", "dns", "pre_up", "post_up", "pre_down", "post_down"]:
        values = ini.get(key)
        if values:
            properties[key] = values

    return properties


def _annotate_interface_peers(interface, ini):
    """Annotates specified interface peers from specified wg config.

    Arguments:
        interface (dict): Dict of interface properties.
        ini (dict): Dict of full config from wg ini.

    Returns:
        dict: Same dict with additional properties.
    """
    peers = {p["public_key"][0]: p for p in ini.get("peer", []) if p.get("public_key")}
    for name, properties in interface.get("peers", {}).items():
        peer = peers.get(name)
        if peer:
            _annotate_peer_properties(properties, peer)
    return interface


def _annotate_peer_properties(properties, ini):
    """Annotates specified peer properties from specified wg config.

    Arguments:
        properties (dict): Dict of peer properties.
        ini (dict): Dict of peer config from wg ini.

    Returns:
        dict: Same dict with additional properties.
    """
    endpoint = ini.get("endpoint")
    if endpoint:
        hostname, _ = split_endpoint_hostname_and_port(endpoint[0])
        if hostname:
            properties["hostname"] = hostname

    return properties


def delete_wg_cnf(cnf, name):
    """Deletes the cnf file for the specified interface with the specified name.

    Arguments:
        cnf (Config): Config object.
        name (str): Interface name (eg 'wg0').
    """
    path = find_wg_cnf_path(cnf, name)
    if path.exists():
        path.unlink()


def rename_wg_cnf(cnf, old_name, new_name):
    """Renames the cnf file for the specified interface to the specified new name.

    Arguments:
        cnf (Config): Config object.
        old_name (str): Existing name (eg 'wg0').
        new_name (str): New name (eg 'wg100').
    """
    if old_name and new_name and old_name != new_name:
        path = find_wg_cnf_path(cnf, old_name)
        if path.exists():
            rename_ini(path, find_wg_cnf_path(cnf, new_name))


def update_wg_cnf(cnf, name, interface, peers=None):
    """Updates the cnf file for the specified interface with the specified properties.

    Arguments:
        cnf (Config): Config object.
        name (str): Name of interface to update (eg 'wg0').
        interface (dict): Properties of interface to update.
        peers (list): List of dicts with peer properties to update.

    Raises:
        ValueError: Cnf file for the interface cannot be written.
    """
    if not interface and not peers:
        return

    chmod = None
    path = find_wg_cnf_path(cnf, name)
    if path.exists():
        sections = load_ini_lines(path)
    elif interface.get("private_key"):
        sections = [_stub_wg_cnf_interface_section(cnf, interface)]
        chmod = 0o640
    else:
        raise ValueError(f"{path} does not exist and private key not available")

    interface = apply_extras_to_scripts(cnf, interface)
    peers = apply_extras_to_peers(cnf, peers)

    section = _find_wg_cnf_interface_section(cnf, interface, path, sections)
    rewrite_ini_section_to_extra_scripts(cnf, section, name)
    _update_wg_cnf_interface_section(section, interface)
    _update_wg_cnf_routing_section(section, interface)
    _update_wg_cnf_peer_sections(cnf, sections, peers)
    rewrite_extra_scripts_to_ini_section(cnf, section, name)

    if cnf.one_line_fields:
        join_ini_splittable_lines(sections, WIREGUARD_SPLITTABLE)
    _debug_wg_cnf_sections(sections)
    save_ini_lines(path, sections, chmod)


def _find_wg_cnf_interface_section(cnf, interface, path, sections):
    """Finds the interface section within the list of sections.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Properties of interface to update.
        path (str): Path to cnf file.
        sections (list): List of list of lines.

    Returns:
        list: List of lines in interface section.

    Raises:
        ValueError: Interface section cannot be found or stubbed.
    """
    section = find_ini_section_with_line(sections, "[Interface]")
    if section:
        return section

    if interface.get("private_key"):
        section = _stub_wg_cnf_interface_section(cnf, interface)
        sections.append(section)
        return section
    raise ValueError(
        f"{path} does not contain an existing interface definition "
        "and private key not available"
    )


def _stub_wg_cnf_interface_section(cnf, interface):
    """Generates lines for the interface section of a new cnf file.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Properties of interface.

    Returns:
        list: List of lines for new cnf file.
    """
    identifier = interface.get("id")
    description = interface.get("description")
    url = f"{cnf.app}/interfaces/{identifier}" if identifier else ""

    if description and url:
        description = f"{description} ({url})"
    else:
        description = description or url

    return [
        f"# generated {format_datetime()} by procustodibus-agent {version}",
        f"# {description}",
        "[Interface]",
        f"PrivateKey = {interface['private_key']}",
    ]


def _update_wg_cnf_interface_section(lines, interface):
    """Updates the lines of the interface section of a cnf file.

    Arguments:
        lines (list): List of lines in interface section.
        interface (dict): Core properties of interface to update.
    """
    pk = interface.get("private_key")
    if pk:
        replace_ini_line_value(lines, "PrivateKey", pk)

    _update_wg_cnf_number_line(lines, interface, "ListenPort", ["listen_port", "port"])
    _update_wg_cnf_number_line(lines, interface, "FwMark", ["fw_mark", "fwmark"])


def _update_wg_cnf_routing_section(lines, interface):
    """Updates the lines of the interface section of a cnf file with routing info.

    Arguments:
        lines (list): List of lines in interface section.
        interface (dict): Routing properties of interface to update.
    """
    _update_wg_cnf_list_line(lines, interface, "Address")

    dns = interface.get("dns")
    search = interface.get("search")
    if dns is not None and search is not None:
        dns = dns + search
    elif search is not None:
        dns = search
    if dns == []:
        replace_ini_line_value(lines, "DNS", None)
    elif dns:
        replace_ini_line_value(lines, "DNS", dns)

    _update_wg_cnf_number_line(lines, interface, "MTU")
    _update_wg_cnf_text_auto_line(lines, interface, "Table")

    for key in ["Extras", "PreUp", "PostUp", "PreDown", "PostDown"]:
        _update_wg_cnf_list_line(lines, interface, key)

    _update_wg_cnf_boolean_line(lines, interface, "SaveConfig")


def _update_wg_cnf_peer_sections(cnf, sections, peers):
    """Updates the lines of the peer sections of a cnf file.

    Arguments:
        cnf (Config): Config object.
        sections (list): List of list of lines.
        peers (list): List of dicts with peer properties to update.
    """
    for peer in peers or []:
        pk = peer["public_key"]
        section = find_ini_section_with_line(sections, f"PublicKey = {pk}")
        if peer.get("delete"):
            if section:
                sections.remove(section)
        else:
            if not section:
                section = _stub_wg_cnf_peer_section(cnf, peer)
                sections.append(section)
            _update_wg_cnf_peer_section(cnf, section, peer)


def _stub_wg_cnf_peer_section(cnf, peer):
    """Generates lines for a new peer section of a cnf file.

    Arguments:
        cnf (Config): Config object.
        peer (dict): Properties of the peer.

    Returns:
        list: List of lines for new peer.
    """
    identifier = peer.get("id")
    name = peer.get("name")
    url = f"{cnf.app}/endpoints/{identifier}" if identifier else ""
    description = f"{name} ({url})" if name and url else name or url
    return [
        "",
        f"# {description}",
        "[Peer]",
        f"PublicKey = {peer['public_key']}",
    ]


def _update_wg_cnf_peer_section(cnf, lines, peer):
    """Updates the lines of a peer section in a cnf file.

    Arguments:
        cnf (Config): Config object.
        lines (list): Existing list of lines in the peer section.
        peer (dict): Properties of the peer to update.
    """
    _update_wg_cnf_text_off_line(lines, peer, "PresharedKey")
    _update_wg_cnf_list_line(lines, peer, "AllowedIPs", ["allowed_ips"])
    _update_wg_cnf_text_line(lines, peer, "Endpoint")
    _update_wg_cnf_number_line(
        lines, peer, "PersistentKeepalive", ["persistent_keepalive", "keepalive"]
    )

    if cnf.wiresock:
        _update_wg_cnf_list_line(lines, peer, "AllowedApps")
        _update_wg_cnf_list_line(lines, peer, "DisallowedApps")
        _update_wg_cnf_list_line(lines, peer, "DisallowedIPs", ["disallowed_ips"])
        _update_wg_cnf_text_line(lines, peer, "Socks5Proxy")
        _update_wg_cnf_text_line(lines, peer, "Socks5ProxyUsername")
        _update_wg_cnf_text_line(lines, peer, "Socks5ProxyPassword")
        _update_wg_cnf_boolean_line(lines, peer, "Socks5ProxyAllTraffic")


def _update_wg_cnf_list_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, [[]], ini_key, src_keys)


def _update_wg_cnf_text_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, [""], ini_key, src_keys)


def _update_wg_cnf_text_auto_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, ["", "auto"], ini_key, src_keys)


def _update_wg_cnf_text_off_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, ["", "off"], ini_key, src_keys)


def _update_wg_cnf_number_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, [0, "0", "off"], ini_key, src_keys)


def _update_wg_cnf_boolean_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, [False, "", "false"], ini_key, src_keys)


def _update_wg_cnf_line(lines, src, empty_values, ini_key, src_keys=None):
    """Updates a line with the specified key from the specified src dict.

    Arguments:
        lines (list): Existing list of lines.
        src (dict): Source dict from which to update the value.
        empty_values (list): Values that should result in removing the line
            instead of updating it.
        ini_key (str): Key in lines to update (eg 'ListenPort').
        src_keys (list): Src keys to check (eg ['listen_port', 'port']).
    """
    if not src_keys:
        src_keys = [underscore(ini_key)]

    value = None
    for x in src_keys:
        value = src.get(x)
        if value is not None:
            break

    if value in empty_values:
        replace_ini_line_value(lines, ini_key, None)
    elif value is True:
        replace_ini_line_value(lines, ini_key, "true")
    elif value:
        replace_ini_line_value(lines, ini_key, value)


def _debug_wg_cnf_sections(sections):
    """Logs content of wg cnf ini.

    Arguments:
        sections (list): List of list of lines.
    """
    log = getLogger(__name__)
    if log.level <= DEBUG:
        log.debug("\n".join(_debug_wg_cnf_sections_content(sections)))


def _debug_wg_cnf_sections_content(sections):
    """Generates content lines from wg cnf ini to log.

    Arguments:
        sections (list): List of list of lines.

    Returns:
        list: List of of lines to log.
    """
    content = [""]
    for lines in sections:
        for line in lines:
            if line.startswith("PrivateKey"):
                line = _hide_private_key_line(line)  # noqa: PLW2901
            elif line.startswith("PresharedKey"):
                line = _hide_preshared_key_line(line)  # noqa: PLW2901
            content.append(line)
    return content


def _hide_private_key_line(line):
    """Hides the private key on the specified line.

    Arguments:
        line (str): WG conf line (eg 'PrivateKey = XYZ=').

    Returns:
        str: Line with hidden key ('PrivateKey = (hidden; public key: ABC=)').
    """
    parts = line.split("=", maxsplit=1)
    if len(parts) < 2:
        return line

    name = parts[0].strip()
    value = derive_public_key(parts[1].strip())
    return f"{name} = (hidden; public key: {value})"


def _hide_preshared_key_line(line):
    """Hides the preshared key on the specified line.

    Arguments:
        line (str): WG conf line (eg 'PresharedKey = XYZ=').

    Returns:
        str: Line with hidden key ('PresharedKey = (hidden; sha256 hash: ABC=)').
    """
    parts = line.split("=", maxsplit=1)
    if len(parts) < 2:
        return line

    name = parts[0].strip()
    value = hash_preshared_key(parts[1].strip())
    return f"{name} = (hidden; sha256 hash: {value})"
