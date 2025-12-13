"""Agent logic."""

from io import StringIO
from logging import getLogger
from signal import SIGINT, SIGTERM, signal
from threading import Event
from time import sleep

from procustodibus_agent import __version__ as version
from procustodibus_agent.api import ping_api
from procustodibus_agent.cnf import reload_cnf_if_modified
from procustodibus_agent.connectivity import check_connectivity
from procustodibus_agent.executor import execute_desired
from procustodibus_agent.ip_route import (
    annotate_wg_show_with_ip_address_show,
    annotate_wg_show_with_tx,
    annotate_wg_show_with_up,
)
from procustodibus_agent.resolve_hostname import apply_endpoint_hostnames
from procustodibus_agent.wg import (
    annotate_wg_show,
    filter_wg_show,
    parse_wg_show,
    run_wg_show,
    update_socket_mark,
)
from procustodibus_agent.wg_cnf import (
    annotate_wg_show_with_wg_cnf,
    load_all_from_wg_cnf,
)

try:
    from signal import SIGHUP
except ImportError:
    SIGHUP = 0


def is_connection_good(cnf, message="Checking connectivity", *, expect_error=False):
    """Runs connectivity check and logs result.

    Arguments:
        cnf (Config): Config object.
        message (str): Message to log (defaults to 'Checking connectivity').
        expect_error (bool): True if error expected (defaults to False).

    Returns:
        bool: True if connection is good.
    """
    buffer = StringIO()
    print(message, file=buffer)

    error = check_connectivity(cnf, buffer)
    if error:
        if not expect_error:
            getLogger(__name__).error(buffer.getvalue())
        return False

    getLogger(__name__).info(buffer.getvalue())
    return True


def capture_shutdown_signal(cnf, event_loop=None):
    """Sets up signal handlers to terminate the ping loop.

    Arguments:
        cnf (Config): Config object.
        event_loop (Event): Event on which loop should wait.

    Returns:
        Event on which loop should wait.
    """
    event = event_loop or Event()

    def shutdown(_signum, _frame):
        cnf.loop = 0
        event.set()

    for s in (SIGHUP, SIGINT, SIGTERM):
        if s:
            signal(s, shutdown)

    return event


def ping_loop(cnf, cli_args=None, event_loop=None):
    """Pings continuously as specified by looping configuration.

    Arguments:
        cnf (Config): Config object.
        event_loop (Event): Event on which loop should wait.
        cli_args (list): List of arguments to pass to Cnf constructor when reloading.
    """
    event = capture_shutdown_signal(cnf, event_loop)
    good = is_connection_good(cnf, message=f"Starting agent {version}")
    hide_error = True

    while cnf.loop and not event.is_set():
        if good:
            try:
                ping(cnf)
            except Exception:
                getLogger(__name__).exception("ping failed")
                good = False
                hide_error = False
        else:
            good = is_connection_good(cnf, expect_error=hide_error)
            hide_error = True
            if good:
                continue

        event.wait(cnf.loop)

        cnf, modified = reload_cnf_if_modified(cnf, cli_args)
        if modified:
            good = is_connection_good(cnf, message="Reloading configuration")
            hide_error = True


def ping(cnf):
    """Gathers wg info and pings api, executing desired changes from response.

    Arguments:
        cnf (Config): Config object.
    """
    interfaces = interrogate(cnf)
    response = ping_api(cnf, interfaces)
    executed = execute_desired(cnf, interfaces, response.get("data"))

    if executed:
        # allow time for changes to propagate
        sleep(2)
        # notify api of changes
        interfaces = interrogate(cnf)
        ping_api(cnf, interfaces, executed)
    else:
        # check for endpoint dns updates
        apply_endpoint_hostnames(cnf, interfaces)


def interrogate(cnf):
    """Extracts interface dict from wg show and wg config.

    Arguments:
        cnf (Config): Config object.

    Returns:
        dict: Interface info parsed from wg etc.
    """
    if cnf.wiresock:
        interfaces = filter_wg_show(load_all_from_wg_cnf(cnf), cnf)
        interfaces = annotate_wg_show_with_up(interfaces)
        interfaces = annotate_wg_show_with_tx(interfaces)
    elif cnf.read_only:
        interfaces = parse_wg_show(run_wg_show(cnf))
        update_socket_mark(interfaces, cnf)
        interfaces = filter_wg_show(interfaces, cnf)
        interfaces = annotate_wg_show_with_wg_cnf(cnf, interfaces)
        interfaces = annotate_wg_show_with_ip_address_show(interfaces)
    else:
        interfaces = load_all_from_wg_cnf(cnf)
        interfaces = annotate_wg_show(interfaces, parse_wg_show(run_wg_show(cnf)))
        update_socket_mark(interfaces, cnf)
        interfaces = filter_wg_show(interfaces, cnf)
    return interfaces
