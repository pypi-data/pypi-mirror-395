"""Utilities for applying and annotating extras."""

from logging import getLogger
from pathlib import Path
from platform import system
from re import compile as compile_re
from re import match, search, sub

from inflection import underscore

PEER_EXTRAS = [
    "allowed_apps",
    "disallowed_apps",
    "socks5_proxy",
    "socks5_proxy_username",
    "socks5_proxy_password",
    "socks5_proxy_all_traffic",
]


def apply_extras_to_scripts(_cnf, interface):
    """Applies the extras from the specified interface properties to scripts.

    For example, given the following interface properties:
    ```
    {'extras': {'masquerade': 'outbound'}, 'post_up': ['echo up']}
    ```

    This would apply them like so:
    ```
    {
        'pre_up': ['scripts/masquerade pre_up "%i" "outbound"'],
        'post_up': ['echo up', 'scripts/masquerade post_up "%i" "outbound"'],
        'pre_down': ['scripts/masquerade pre_down "%i" "outbound"'],
        'post_down': ['scripts/masquerade post_down "%i" "outbound"'],
    }
    ```

    Arguments:
        cnf (Config): Config object.
        interface (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    extras = []
    for name, value in interface.get("extras", {}).items():
        converted = _convert_extra_script_value_to_string(name, value)
        extras.append(f"{name} {converted}")

    if extras:
        interface["extras"] = extras
    return interface


def _convert_extra_script_value_to_string(name, value):
    """Converts the specified extra script value to a string.

    Arguments:
        name (str): Extra script name.
        value: Extra script value.

    Returns:
        str: Extra script value as a string.

    Raises:
        ValueError: If the extra value contains problematic characters.
    """
    if value is True:
        return "true"
    if not value and type(value) not in (int, float):
        return ""

    value = str(value)
    bad_character = search(r"[\x00-\x1f\"\\]", value)
    if bad_character:
        encoded = hex(bad_character.group(0).encode("utf-8")[0])
        raise ValueError(f"bad character in extras value: {name} ({encoded})")
    return value


def rewrite_ini_section_to_extra_scripts(cnf, lines, _dev):
    """Rewrites the specified ini lines from real scripts to fake extra properties.

    For example, given the following lines:
    ```
    [
        '[Interface]',
        'PrivateKey = 123...',
        'PreUp = scripts/masquerade pre_up "%i" "outbound"',
        'PostUp = scripts/masquerade post_up "%i" "outbound"',
        'PreDown = scripts/masquerade pre_down "%i" "outbound"',
        'PostDown = scripts/masquerade post_down "%i" "outbound"',
        'PostUp = echo up',
    ]
    ```

    This would rewrite them like so:
    ```
    [
        '[Interface]',
        'PrivateKey = 123...',
        'Extras = masquerade outbound',
        'PostUp = echo up',
    ]
    ```

    Arguments:
        cnf (Config): Config object.
        lines (dict): List of lines in '[Interface]` section.
        dev (str): Name of interface to update (eg 'wg0').

    Returns:
        list: Same lines list with, but with updated lines.
    """
    re = _get_script_re(cnf.scripts)
    re = compile_re(rf"((?:Pre|Post)(?:Up|Down))\s*=\s*{re.pattern}")
    i = 0
    while i < len(lines):
        parts = re.match(lines[i])
        if parts:
            key, name, value = parts.groups()
            if key == "PreUp":
                lines[i] = f"Extras = {name} {value}"
            else:
                del lines[i]
        else:
            i += 1
    return lines


def rewrite_extra_scripts_to_ini_section(cnf, lines, dev):
    """Rewrites the specified ini lines from fake extra properties to real scripts.

    For example, given the following lines:
    ```
    [
        '[Interface]',
        'PrivateKey = 123...',
        'Extras = masquerade outbound',
        'Extras = foo bar',
        'PostUp = echo up',
    ]
    ```

    This would rewrite them like so:
    ```
    [
        '[Interface]',
        'PrivateKey = 123...',
        'PreUp = scripts/masquerade pre_up "%i" "outbound"',
        'PostUp = scripts/masquerade post_up "%i" "outbound"',
        'PreDown = scripts/masquerade pre_down "%i" "outbound"',
        'PostDown = scripts/masquerade post_down "%i" "outbound"',
        'PostUp = echo up',
    ]
    ```

    Arguments:
        cnf (Config): Config object.
        lines (dict): List of lines in '[Interface]` section.
        dev (str): Name of interface to update (eg 'wg0').

    Returns:
        list: Same lines list with, but with updated lines.
    """
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith("Extras ="):
            i += 1
            continue

        parts = match(r"Extras = (\w+) (.+)", line)
        if not parts:
            del lines[i]
            continue

        name, value = parts.groups()
        path = _get_script_path(cnf.scripts, name)
        if path:
            scripts = list(_expand_scripts(dev, path, name, value))
            lines[i : i + 1] = scripts
            i += len(scripts)
        else:
            getLogger(__name__).warning("no extras script: %s", name)
            del lines[i]
    return lines


def _get_script_path(directory, name):
    """Returns the path to the script if it exists, or "".

    Arguments:
        directory (str): Path to scripts directory (eg '/scripts').
        name (str): Name of script (eg 'forward').

    Returns:
        str: Path to script (eg '/scripts/forward').
    """
    if not directory:
        return ""

    windows = system() == "Windows"
    if windows:
        name = f"{name}.ps1"

    path = Path(directory, name)
    if path.is_file():
        return f'powershell -F "{path}"' if windows else str(path)
    return ""


def _expand_scripts(dev, path, _name, value):
    """Creates the lines for an extra script.

    Arguments:
        dev (str): Name of interface to update (eg 'wg0').
        path (str): Full path to script (eg '/scripts/forward').
        name (str): Extra name (eg 'forward').
        value (str): Extra value (eg 'outbound').

    Yields:
        str: Expanded script line.
    """
    if system() != "Windows":
        dev = "%i"
    for phase in ["PreUp", "PostUp", "PreDown", "PostDown"]:
        yield f'{phase} = {path} {underscore(phase)} "{dev}" "{value}"'


def annotate_extras_from_scripts(cnf, interface):
    """Annotates the specified interface properties with extras from its scripts.

    For example, given the following interface properties:
    ```
    {
        'pre_up': ['scripts/masquerade pre_up "%i" "outbound"'],
        'post_up': ['echo up', 'scripts/masquerade post_up "%i" "outbound"'],
        'pre_down': ['scripts/masquerade pre_down "%i" "outbound"'],
        'post_down': ['scripts/masquerade post_down "%i" "outbound"'],
    }
    ```

    This would annotate it like so:
    ```
    {'extras': {'masquerade': 'outbound'}, 'post_up': ['echo up']}
    ```


    Arguments:
        cnf (Config): Config object.
        interface (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    directory = cnf.scripts
    if not directory:
        return interface

    extras = dict(_extract_extras_from_scripts(directory, interface))
    if not extras:
        return interface

    interface["extras"] = extras
    return _strip_extras_from_scripts(directory, interface)


def _extract_extras_from_scripts(directory, properties):
    """Extracts extra script names and values from the specified interface properties.

    Arguments:
        directory (str): Path to scripts directory (eg '/scripts').
        properties (dict): Dict of interface properties.

    Yields:
        tuple: Extra name and value (eg ('forward', 'outbound')).
    """
    re = _get_script_re(directory)
    for script in properties.get("pre_up", []):
        match = re.fullmatch(script)
        if match:
            yield match.groups()


def _strip_extras_from_scripts(directory, properties):
    """Strips extra scripts from the specified interface properties.

    Arguments:
        directory (str): Path to scripts directory (eg '/scripts').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict stripped of some values.
    """
    for phase in ["pre_up", "post_up", "pre_down", "post_down"]:
        _strip_extras_from_script(directory, properties, phase)
    return properties


def _strip_extras_from_script(directory, properties, phase):
    """Strips extra scripts from the specified script phase.

    Arguments:
        directory (str): Path to scripts directory (eg '/scripts').
        properties (dict): Dict of interface properties.
        phase (str): Pre/post/up/down phase (eg 'pre_up').

    Returns:
        dict: Same dict stripped of some values.
    """
    old_values = properties.get(phase)
    if not old_values:
        return properties

    re = _get_script_re(directory)
    new_values = [x for x in old_values if not re.fullmatch(x)]
    if not new_values:
        del properties[phase]
    elif len(old_values) != len(new_values):
        properties[phase] = new_values
    return properties


def _get_script_re(directory):
    """Generates regex to match name and value of extra scripts.

    Arguments:
        directory (str): Path to scripts directory (eg '/scripts').

    Returns:
        re: Regex that matches extra scripts.
    """
    if system() != "Windows":
        return compile_re(rf'{directory}\W(\w+) \S+ \S+ "([^"]*)"')
    directory = sub(r"[/\\]", r"\\W", directory)
    return compile_re(rf'powershell -F "{directory}\W(\w+).ps1" \S+ \S+ "([^"]*)"')


def apply_extras_to_peers(_cnf, peers):
    """Applies the extras from the specified peer properties.

    For example, given the following peer properties:
    ```
    {'extras': {'allowed_apps': ['firefox', 'chrome']}}
    ```

    This would apply them like so:
    ```
    {'allowed_apps': ['firefox', 'chrome']}
    ```

    Arguments:
        cnf (Config): Config object.
        peers (list): List of peer dicts.

    Returns:
        list: Same peer dicts with additional properties.
    """
    if peers:
        for peer in peers:
            extras = peer.get("extras", {})
            if extras:
                peer.update({k: (extras.pop(k)) for k in PEER_EXTRAS if k in extras})
                if not extras:
                    del peer["extras"]
    return peers


def annotate_extras_from_peers(_cnf, interface):
    """Annotates the specified interface properties with extras from its peers.

    For example, given the following interface properties:
    ```
    {
        peers: {
            'ABC=': {'allowed_apps': ['firefox', 'chrome']},
        },
    }
    ```

    This would annotate it like so:
    ```
    {
        peers: [
            'ABC=': {'extras': {'allowed_apps': ['firefox', 'chrome']}},
        ],
    }
    ```

    Arguments:
        cnf (Config): Config object.
        interface (dict): Dict of interface properties.

    Returns:
        dict: Same dict with changes to peers.
    """
    peers = interface["peers"]
    if peers:
        for peer in peers.values():
            extras = {k: (peer.pop(k)) for k in PEER_EXTRAS if k in peer}
            if extras:
                peer["extras"] = extras
    return interface
