"""Connectivity test."""

import os
import sys
from re import search
from socket import AF_INET, AF_INET6

from dns.exception import DNSException
from requests import RequestException

from procustodibus_agent import DOCS_URL
from procustodibus_agent.api import (
    get_health_info,
    get_host_info,
    raise_unless_has_cnf,
    setup_api,
)
from procustodibus_agent.resolve_hostname import get_resolver, is_likely_ip
from procustodibus_agent.wg import parse_wg_show, run_wg_show, update_socket_mark
from procustodibus_agent.wg_cnf import load_all_from_wg_cnf


def check_connectivity(cnf, output=None):
    """Runs all connectivity checks and outputs issues.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to (defaults to stdout).

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    if not output:
        output = sys.stdout

    try:
        raise_unless_has_cnf(cnf)
    except ValueError as e:
        print(str(e), file=output)
        return 1

    exit_code = (
        check_wg(cnf, output)
        + check_dns(cnf, output)
        + check_health(cnf, output)
        + check_host(cnf, output)
    )

    if exit_code:
        print(
            f"Issues encountered; see {DOCS_URL}/guide/agents/troubleshoot/ to fix",
            file=output,
        )
    else:
        print("All systems go :)", file=output)

    return exit_code


def check_wg(cnf, output):
    """Checks that wireguard is available and configured with at least one interface.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    if cnf.wiresock:
        try:
            interfaces = load_all_from_wg_cnf(cnf)
        except Exception as e:  # noqa: BLE001
            _bad(f"cannot open interface conf files ({e})", output)
            return 2
    else:
        try:
            interfaces = parse_wg_show(run_wg_show(cnf))
            update_socket_mark(interfaces, cnf)
        except OSError as e:
            _bad(f"no wg executable found ({e})", output)
            return 2

    if interfaces:
        _good(f"{len(interfaces)} wireguard interfaces found", output)
        return 0
    _bad("no wireguard interfaces found", output)
    return 0


def check_dns(cnf, output):
    """Checks that the local DNS resolver can resolve api.procustodib.us.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    hostname = _get_hostname(cnf.api)
    if is_likely_ip(hostname):
        version = 6 if ":" in hostname else 4
        _good(f"{hostname} is pro custodibus api ipv{version} address", output)
        return 0

    resolver = get_resolver(cnf)
    families = [AF_INET6, AF_INET] if resolver.prefer_ipv6 else [AF_INET, AF_INET6]

    result = _check_dns_family(resolver, hostname, families[0], output)
    if (
        result == 0
        or not resolver.has_ipv6
        or cnf.resolve_hostnames in ("ipv4", "ipv6")
    ):
        return result

    result = _check_dns_family(resolver, hostname, families[1], output)
    if result == 0:
        resolver.flip_ipv6_preference()
    return result


def _check_dns_family(resolver, hostname, family, output):
    """Checks that the local DNS resolver can resolve api.procustodib.us.

    Arguments:
        resolver (Resolver): Resolver object.
        hostname (str): Hostname to lookup (eg 'foo.example.com').
        family (int): Preferred family (eg AF_INET6).
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    version = 6 if family == AF_INET6 else 4
    try:
        addresses = resolver.lookup_ips(hostname, family)
        if addresses:
            _good(f"{addresses[0]} is pro custodibus api ipv{version} address", output)
            return 0
    except DNSException as e:
        _bad(f"cannot resolve pro custodibus api ipv{version} address: {e}", output)
        return 4
    else:
        _bad(f"no pro custodibus api ipv{version} address", output)
        return 4


def check_health(cnf, output):
    """Checks connectivity to and the health of the Pro Custodibus API.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    try:
        errors = [x["error"] for x in get_health_info(cnf) if not x["healthy"]]
    except RequestException as e:
        errors = _check_health_of_other_family(cnf, output, e)
    except DNSException as e:
        errors = [_build_server_unvailable_message(e)]

    if errors:
        for error in errors:
            _bad(f"unhealthy pro custodibus api: {error}", output)
        return 8
    _good("healthy pro custodibus api", output)
    return 0


def _check_health_of_other_family(cnf, output, error):
    """Checks connectivity to the API using the other IP version (4 or 6).

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.
        error: Error that triggered this check.

    Returns:
        list: List of errors messages (or empty if no errors).
    """
    resolver = get_resolver(cnf)
    hostname = _get_hostname(cnf.api)
    if (
        not resolver.has_ipv6
        or cnf.resolve_hostnames in ("ipv4", "ipv6")
        or is_likely_ip(hostname)
    ):
        return [_build_server_unvailable_message(error)]

    _bad(_build_server_unvailable_message(error, resolver), output)
    resolver.flip_ipv6_preference()
    family = AF_INET6 if resolver.prefer_ipv6 else AF_INET
    if _check_dns_family(resolver, hostname, family, output):
        return [_build_server_unvailable_message()]

    try:
        return [x["error"] for x in get_health_info(cnf) if not x["healthy"]]
    except (RequestException, DNSException) as e:
        return [_build_server_unvailable_message(e, resolver)]


def _build_server_unvailable_message(error=None, resolver=None):
    """Builds the 'server unavailable' error message.

    Arguments:
        error: Error that triggered this check (or none).
        resolver: DNS resolver (or none), to display IP version (4 or 6).

    Returns:
        str: Error message (eg 'server unavailable').
    """
    if not error:
        return "server unavailable"
    if not resolver:
        return f"server unavailable ({error})"
    version = 6 if resolver.prefer_ipv6 else 4
    return f"server unavailable at ipv{version} address ({error})"


def check_host(cnf, output):
    """Checks that the agent can access the configured host through the API.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    try:
        _setup_if_available(cnf)
    except (DNSException, RequestException, ValueError) as e:
        _bad(f"cannot set up access to api ({e})", output)
        return 16

    try:
        host = get_host_info(cnf)
        name = host["data"][0]["attributes"]["name"]
        _good(f"can access host record on api for {name}", output)
    except (DNSException, RequestException, ValueError) as e:
        _bad(f"cannot access host record on api ({e})", output)
        return 16
    else:
        return 0


def _setup_if_available(cnf):
    """Sets up new agent credentials if setup code is available.

    Arguments:
        cnf (Config): Config object.
    """
    if type(cnf.setup) is dict or os.path.exists(cnf.setup):
        setup_api(cnf)


def _good(message, output):
    """Prints the specified "good" message to the specified output stream.

    Arguments:
        message (str): Message to print.
        output (IOBase): Output stream to write to.
    """
    print(f"... {message} ...", file=output)


def _bad(message, output):
    """Prints the specified "bad" message to the specified output stream.

    Arguments:
        message (str): Message to print.
        output (IOBase): Output stream to write to.
    """
    print(f"!!! {message} !!!", file=output)


def _get_hostname(url):
    """Extracts the hostname from the specified URL.

    Arguments:
        url (str): URL (eg 'http://test.example.com:8080').

    Returns:
        str: Hostname (eg 'test.example.com').
    """
    match = search(r"(?<=://)[^:/]+", url)
    return match.group(0) if match else None
