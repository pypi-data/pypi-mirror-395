"""Executor system commands."""

from logging import DEBUG, INFO, getLogger, root
from pathlib import Path
from platform import system
from re import match, search, sub
from subprocess import PIPE, STDOUT, CompletedProcess, run
from time import sleep

from procustodibus_agent.wg_cnf import (
    delete_wg_cnf,
    find_wg_cnf_path,
    rename_wg_cnf,
    update_wg_cnf,
)


def calculate_ip_family(address):
    """Determines whether the specified IP address is IPv4 or IPv6.

    Arguments:
        address (str): IP address (eg 'fc00:0:0:1::').

    Returns:
        int: 4 or 6.
    """
    return 6 if search(r":.*:", address) else 4


def resolvconf_interface_prefix(file="/etc/resolvconf/interface-order"):
    """Returns the prefix to append to an interface name for resolvconf commands.

    Arguments:
        file (str): Resolvconf interface-order file path to check.

    Returns:
        str: Prefix (eg 'tun') or blank ('').
    """
    path = Path(file)
    if path.exists():
        with open(path) as f:
            for line in f:
                interface_match = match(r"([A-Za-z0-9-]+)\*", line)
                if interface_match:
                    return interface_match[1]
    return ""


def get_sys_cmd():
    """Returns the command object appropriate for the current operating system.

    Returns:
        SysCmd: Command object.
    """
    s = system()
    if s == "Linux":
        return LinuxSysCmd()
    if s == "Windows":
        return WindowsSysCmd()
    return SysCmd()


class SysCmd:
    """Runs commands for a generic operating system."""

    def start_service(self, cnf, dev, results):
        """Starts the specified WireGuard interface.

        Arguments:
            cnf (Config): Config object.
            dev (str): Interface name (eg 'wg0').
            results (list): List to append the results of the command to.
        """
        self._do_start_service(cnf, dev, results)

    def stop_service(self, cnf, dev, results):
        """Stops the specified WireGuard interface.

        Arguments:
            cnf (Config): Config object.
            dev (str): Interface name (eg 'wg0').
            results (list): List to append the results of the command to.
        """
        self._do_stop_service(cnf, dev, results)

    def update_address(self, action, address, dev, results):
        """Adds or remove the specified interface address.

        Arguments:
            action (str): "add" or "del".
            address (str): IP address or CIDR (eg '10.0.0.0/24').
            dev (str): Interface name (eg 'wg0').
            results (list): List of completed proccess objects (to add to).
        """
        self._do_update_address(action, address, dev, results)

    def update_mtu(self, mtu, dev, results):
        """Sets the specified interface MTU.

        Arguments:
            mtu (int): New MTU value (eg 1420).
            dev (str): Interface name (eg 'wg0').
            results (list): List of completed proccess objects (to add to).
        """
        self._do_update_mtu(mtu, dev, results)

    def update_dns(self, dns, search, dev, results):
        """Sets the specified interface DNS resolvers and search suffixes.

        Arguments:
            dns (list): List of DNS resolver IP addresses (eg ['9.9.9.9']).
            search (list): List of DNS search suffixes (eg ['wg.corp']).
            dev (str): Interface name (eg 'wg0').
            results (list): List of completed proccess objects (to add to).
        """
        self._do_update_dns(dns, search, dev, results)

    def check_route(self, to, dev, table, results):
        """Checks if the specified route exists.

        Arguments:
            to (str): IP address or CIDR (eg '10.0.0.0/24').
            dev (str): Interface name (eg 'wg0').
            table (str): Route table name (eg 'auto').
            results (list): List of completed proccess objects (to add to).

        Returns:
            str: None if error; 'found' if found; 'missing' if missing.
        """
        return self._do_check_route(to, dev, table, results)

    def update_route(self, action, to, dev, table, results):
        """Adds or removes the specified route.

        Arguments:
            action (str): "add" or "del".
            to (str): IP address or CIDR (eg '10.0.0.0/24').
            dev (str): Interface name (eg 'wg0').
            table (str): Route table name (eg 'auto').
            results (list): List of completed proccess objects (to add to).
        """
        check = self.check_route(to, dev, table, results)
        if (action == "add" and check == "missing") or (
            action == "del" and check == "found"
        ):
            self._do_update_route(action, to, dev, table, results)

    def set_interface(self, cnf, dev, setting, value, results):
        """Sets the specified wg setting for the specified interface.

        Arguments:
            cnf (Config): Config object.
            dev (str): Interface name (eg 'wg0').
            setting (str): Setting name (eg 'allowed-ips').
            value (str): Setting value (eg '10.0.0.1/24,fc00:0:0:1::/64').
            results (list): List to append the results of the command to.
        """
        results.append(_cmd(cnf.wg, "set", dev, setting, value))

    def set_peer(self, cnf, dev, pk, setting, value, results):
        """Sets the specified wg setting for the specified peer.

        Arguments:
            cnf (Config): Config object.
            dev (str): Interface name (eg 'wg0').
            pk (str): Peer public key.
            setting (str): Setting name (eg 'allowed-ips').
            value (str): Setting value (eg '10.0.0.1/24,fc00:0:0:1::/64').
            results (list): List to append the results of the command to.
        """
        if setting == "remove":
            results.append(_cmd(cnf.wg, "set", dev, "peer", pk, setting))
        else:
            results.append(_cmd(cnf.wg, "set", dev, "peer", pk, setting, value))

    def check_wg_cnf(self, cnf, dev, _results):
        """Checks if the specified interface config file exists.

        Arguments:
            cnf (Config): Config object.
            dev (str): Name of interface to update (eg 'wg0').
            results (list): List of completed proccess objects (to add to).

        Returns:
            str: None if error; 'found' if found; 'missing' if missing.
        """
        return "found" if find_wg_cnf_path(cnf, dev).exists() else "missing"

    def create_wg_cnf(self, cnf, dev, interface, peers, results):
        """Creates the interface cnf file with the specified properties.

        Arguments:
            cnf (Config): Config object.
            dev (str): Name of interface to update (eg 'wg0').
            interface (dict): Properties of interface to update.
            peers (list): List of dicts with peer properties to update.
            results (list): List of completed proccess objects (to add to).
        """
        self.update_wg_cnf(cnf, dev, interface, peers, results)

    def update_wg_cnf(self, cnf, dev, interface, peers, results):
        """Updates the interface cnf file with the specified properties.

        Arguments:
            cnf (Config): Config object.
            dev (str): Name of interface to update (eg 'wg0').
            interface (dict): Properties of interface to update.
            peers (list): List of dicts with peer properties to update.
            results (list): List of completed proccess objects (to add to).
        """
        description = f"procustodibus_agent setconf {dev} {find_wg_cnf_path(cnf, dev)}"
        results.append(
            _as_cmd(description, lambda: update_wg_cnf(cnf, dev, interface, peers))
        )

    def rename_wg_cnf(self, cnf, old_dev, new_dev, results):
        """Renames the specified interface config file.

        Arguments:
            cnf (Config): Config object.
            old_dev (str): Old interface name (eg 'wg0').
            new_dev (str): New interface name (eg 'wg0').
            results (list): List of completed proccess objects (to add to).
        """
        description = (
            f"mv {find_wg_cnf_path(cnf, old_dev)} {find_wg_cnf_path(cnf, new_dev)}"
        )
        results.append(
            _as_cmd(description, lambda: rename_wg_cnf(cnf, old_dev, new_dev))
        )

    def delete_wg_cnf(self, cnf, dev, results):
        """Deletes the specified interface config file.

        Arguments:
            cnf (Config): Config object.
            dev (str): Interface name (eg 'wg0').
            results (list): List of completed proccess objects (to add to).
        """
        description = f"rm {find_wg_cnf_path(cnf, dev)}"
        results.append(_as_cmd(description, lambda: delete_wg_cnf(cnf, dev)))

    def _do_start_service(self, cnf, dev, results):
        raise NotImplementedError

    def _do_stop_service(self, cnf, dev, results):
        raise NotImplementedError

    def _do_update_address(self, address, dev, results):
        raise NotImplementedError

    def _do_update_mtu(self, mtu, dev, results):
        raise NotImplementedError

    def _do_update_dns(self, dns, search, dev, results):
        raise NotImplementedError

    def _do_check_route(self, to, dev, table, results):
        raise NotImplementedError

    def _do_update_route(self, action, to, dev, table, results):
        raise NotImplementedError


class LinuxSysCmd(SysCmd):
    """Runs commands for Linux."""

    def _do_start_service(self, cnf, dev, results):
        cnf_name = _find_wg_quick_cnf_name(cnf, dev)
        if cnf.manager == "systemd" and not cnf_name.startswith("/"):
            # stop first, and ignore shutdown output/errors
            _cmd("systemctl", "stop", f"wg-quick@{dev}.service")
            results.append(_cmd("systemctl", "start", f"wg-quick@{dev}.service"))
            results.append(_cmd("systemctl", "enable", f"wg-quick@{dev}.service"))
            _append_journalctl_to_results_if_suggested(results)
        else:
            # stop first, and ignore shutdown output/errors
            _cmd(cnf.wg_quick, "down", cnf_name)
            results.append(_cmd(cnf.wg_quick, "up", cnf_name))

    def _do_stop_service(self, cnf, dev, results):
        cnf_name = _find_wg_quick_cnf_name(cnf, dev)
        if cnf.manager == "systemd" and not cnf_name.startswith("/"):
            results.append(_cmd("systemctl", "stop", f"wg-quick@{dev}.service"))
            results.append(_cmd("systemctl", "disable", f"wg-quick@{dev}.service"))
            _append_journalctl_to_results_if_suggested(results)
        else:
            results.append(_cmd(cnf.wg_quick, "down", cnf_name))

    def _do_update_address(self, action, address, dev, results):
        results.append(_cmd(*_ip_route_args("address", action, address, dev)))

    def _do_update_mtu(self, mtu, dev, results):
        results.append(_cmd("ip", "link", "set", "mtu", str(mtu), "up", "dev", dev))

    def _do_update_dns(self, dns, search, dev, results):
        resolvconf_name = f"{resolvconf_interface_prefix()}{dev}"
        results.append(_cmd("resolvconf", "-d", resolvconf_name, "-f"))
        resolvconf_input = []

        if dns:
            resolvconf_input.append(f"nameserver {','.join(dns)}\n")
        if search:
            resolvconf_input.append(f"search {','.join(search)}\n")
        if resolvconf_input:
            results.append(
                _cmd(
                    "resolvconf",
                    "-a",
                    resolvconf_name,
                    "-m",
                    "0",
                    "-x",
                    stdin="".join(resolvconf_input),
                )
            )

    def _do_update_route(self, action, to, dev, table, results):
        results.append(_cmd(*_ip_route_args("route", action, to, dev, table)))

    def _do_check_route(self, to, dev, table, results):
        completed = _cmd(*_ip_route_args("route", "show", to, dev, table), quiet=True)

        if completed.returncode:
            results.append(completed)
            return None

        return "found" if completed.stdout.strip() else "missing"


class WindowsSysCmd(SysCmd):
    """Runs commands for Windows."""

    def _do_start_service(self, cnf, dev, results):
        if _sc_query_state(cnf, dev) == "RUNNING":
            results.append(_cmd("sc", "stop", _sc_service_name(cnf, dev)))
            _sc_query_state_wait_until("STOPPED", cnf, dev, results)

        cnf_path = find_wg_cnf_path(cnf, dev)
        results.append(_cmd("wireguard", "/installtunnelservice", str(cnf_path)))
        _sc_query_state_wait_until("RUNNING", cnf, dev, results)

    def _do_stop_service(self, cnf, dev, results):
        results.append(_cmd("wireguard", "/uninstalltunnelservice", dev))
        _sc_query_state_wait_until(None, cnf, dev, results)

    def _do_update_address(self, action, address, dev, results):
        args = [
            *_netsh_interface_args(address),
            action,
            "address",
            f"interface={dev}",
            f"address={address}",
            "store=active",
        ]
        if args[2] == "ipv4":
            args[5] = f"name={dev}"
            if action == "del":
                address = sub(r"/.*", "", address)
                args[6] = f"address={address}"
        results.append(_cmd(*args))

    def _do_update_mtu(self, mtu, dev, results):
        args = [
            *_netsh_interface_args(4),
            "set",
            "interface",
            f"interface={dev}",
            f"mtu={mtu}",
            "store=active",
        ]
        results.append(_cmd(*args))
        args[2] = "ipv6"
        results.append(_cmd(*args))

    def _do_update_dns(self, dns, _search, dev, results):
        # TODO: search/suffix list not exposed via netsh?
        existing_4 = _netsh_show_dns_servers(4, dev, results)
        existing_6 = _netsh_show_dns_servers(6, dev, results)
        for address in existing_4 + existing_6:
            args = [
                *_netsh_interface_args(address),
                "del",
                "dnsservers",
                f"name={dev}",
                f"address={address}",
            ]
            results.append(_cmd(*args))
        for address in dns:
            args = [
                *_netsh_interface_args(address),
                "add",
                "dnsservers",
                f"name={dev}",
                f"address={address}",
            ]
            results.append(_cmd(*args))

    def _do_update_route(self, action, to, dev, _table, results):
        args = [
            *_netsh_interface_args(to),
            action,
            "route",
            f"prefix={to}",
            f"interface={dev}",
            "store=active",
        ]
        results.append(_cmd(*args))

    def _do_check_route(self, to, dev, _table, results):
        args = [*_netsh_interface_args(to), "show", "route"]
        completed = _cmd(*args, quiet=True)

        if completed.returncode:
            results.append(completed)
            return None

        for line in completed.stdout.split("\n"):
            parts = line.split()
            if len(parts) >= 6 and parts[3] == to and parts[5] == dev:
                return "found"

        return "missing"


class WireSockSysCmd(SysCmd):
    """Runs commands for WireSock."""

    def set_interface(self, cnf, dev, setting, value, results):  # noqa: D102
        pass

    def set_peer(self, cnf, dev, pk, setting, value, results):  # noqa: D102
        pass

    def _do_start_service(self, cnf, dev, results):
        state = _sc_query_state(cnf, dev)
        if not state:
            results.append(
                _cmd(
                    cnf.wg,
                    "install",
                    "-start-type",
                    "2",
                    "-config",
                    str(find_wg_cnf_path(cnf, dev)),
                    "-log-level",
                    _sc_service_log_level(cnf),
                    "-lac",
                )
            )
            state = "STOPPED"

        name = _sc_service_name(cnf, dev)
        if state == "RUNNING":
            results.append(_cmd("sc", "stop", name))
            _sc_query_state_wait_until("STOPPED", cnf, dev, results)

        results.append(_cmd("sc", "start", name))
        _sc_query_state_wait_until("RUNNING", cnf, dev, results)

    def _do_stop_service(self, cnf, dev, results):
        results.append(_cmd(cnf.wg, "uninstall"))
        _sc_query_state_wait_until(None, cnf, dev, results)

    def _do_update_address(self, action, address, dev, results):
        pass

    def _do_update_mtu(self, mtu, dev, results):
        pass

    def _do_update_dns(self, dns, search, dev, results):
        pass

    def _do_update_route(self, action, to, dev, table, results):
        pass

    def _do_check_route(self, _to, _dev, _table, _results):
        return "missing"


def _cmd(*args, stdin=None, quiet=False):
    """Executes a command with the specified arguments.

    Arguments:
        *args (list): Command arguments.
        stdin (str): Optional command input.
        quiet (bool): True to skip logging if ok (default False).

    Returns:
        Completed process object.
    """
    try:
        if stdin:
            completed = run(  # noqa: S603
                args,
                input=stdin,
                stdout=PIPE,
                stderr=STDOUT,
                timeout=30,
                text=True,
                check=False,
            )
        else:
            completed = run(  # noqa: S603
                args, stdout=PIPE, stderr=STDOUT, timeout=30, text=True, check=False
            )
    except Exception as e:  # noqa: BLE001
        completed = CompletedProcess([], 1, stdout=str(e))

    output = " ".join(args)
    stdout = completed.stdout.strip() if completed.stdout else ""
    if stdout:
        output = f"{output}\n{stdout}"

    if completed.returncode and quiet != "silent":
        getLogger(__name__).warning("err # %s", output)
    elif not quiet:
        getLogger(__name__).info("ok  # %s", output)

    return completed


def _as_cmd(description, function):
    """Runs the specified function and returns a CompletedProcess object as the result.

    Arguments:
        description (str): Command description (eg 'update config file').
        function (lambda): Zero-argument function to run.

    Returns:
        Completed process object.
    """
    try:
        function()
        getLogger(__name__).info("ok  # %s", description)
        return CompletedProcess([], 0)
    except Exception as e:  # noqa: BLE001
        getLogger(__name__).warning("err # %s", description, exc_info=True)
        return CompletedProcess([], 1, stdout=str(e))


def _find_wg_quick_cnf_name(cnf, dev):
    """Finds name or path to use for wg-quick for the specified interface.

    Arguments:
        cnf (Config): Config object.
        dev (str): Name of interface (eg 'wg0').

    Returns:
        str: Name or path (eg 'wg0' or '/usr/local/etc/wireguard/wg.conf').
    """
    full_name = str(find_wg_cnf_path(cnf, dev))
    return dev if full_name == f"/etc/wireguard/{dev}.conf" else full_name


def _append_journalctl_to_results_if_suggested(results):
    """Appends output of journalctl to results if suggested.

    Arguments:
        results (list): List of command results.
    """
    for line in results:
        m = search(r"journalctl -xeu ((?:.*?).service)", str(line))
        if m:
            results.append(_cmd("journalctl", "-S", "-9", "-u", m.group(1)))


def _ip_route_args(cmd, action, to, dev, table="auto"):
    """Builds arg list for ip address/route add/del/show command.

    Arguments:
        cmd (str): "address" or "route".
        action (str): "add", "del", or "show".
        to (str): IP address or CIDR (eg '10.0.0.0/24').
        dev (str): Interface name (eg 'wg0').
        table (str): Route table name (eg 'auto').

    Returns:
        list: Arg list.
    """
    family = calculate_ip_family(to)

    args = ["ip", f"-{family}", cmd, action, to, "dev", dev]
    if table != "auto":
        args += ["table", table]

    return args


def _netsh_interface_args(to):
    """Builds arg list for netsh route add/del/show command.

    Arguments:
        to (str): IP address or CIDR (eg '10.0.0.0/24').

    Returns:
        list: Arg list.
    """
    family = to if to in (4, 6) else calculate_ip_family(to)
    return ["netsh", "interface", f"ipv{family}"]


def _netsh_show_dns_servers(family, dev, results):
    """Runs netsh command to show DNS servers.

    Arguments:
        family (int): 4 or 6.
        dev (str): Interface name (eg 'wg0').
        results (list): List of completed proccess objects (to add to).

    Returns:
        list: List of DNS servers.
    """
    args = [*_netsh_interface_args(family), "show", "dnsservers", dev]
    completed = _cmd(*args, quiet=True)
    results.append(completed)
    servers = []

    for line in completed.stdout.split("\n"):
        m = search(r"(\d+\.\d+\.\d+\.\d+|[\da-f]+:[\da-f.:%]+)", line)
        if m:
            servers.append(m.group(0))

    return servers


def _sc_query_state_wait_until(state, cnf, dev, results=None):
    """Runs sc command to query service status until it matches specified state.

    Arguments:
        state (str): Desired state (eg 'STOPPED').
        cnf (Config): Config object.
        dev (str): Interface name (eg 'wg0').
        results (list): List of completed proccess objects (to add to).

    Returns:
        bool: True if reached specified state.
    """
    for x in range(5):
        sleep(x / 4)
        if _sc_query_state(cnf, dev) == state:
            return True

    sleep(2)
    return _sc_query_state(cnf, dev, results) == state


def _sc_query_state(cnf, dev, results=None):
    """Runs sc command to query service status.

    Arguments:
        cnf (Config): Config object.
        dev (str): Interface name (eg 'wg0').
        results (list): List of completed proccess objects (to add to).

    Returns:
        str: Service state (eg 'RUNNING'), or None if service unknown.
    """
    completed = _cmd("sc", "query", _sc_service_name(cnf, dev), quiet="silent")
    if results is not None:
        results.append(completed)

    for line in completed.stdout.split("\n"):
        parts = line.split()
        if len(parts) >= 4 and parts[0] == "STATE":
            return parts[3]
    return None


def _sc_service_name(cnf, dev):
    """Returns service name.

    Arguments:
        cnf (Config): Config object.
        dev (str): Interface name (eg 'wg0').

    Returns:
        str: Service name (eg 'wiresock-client-service').
    """
    if cnf.wiresock:
        return "wiresock-client-service"
    return f"WireGuardTunnel${dev}"


def _sc_service_log_level(_cnf):
    """Returns service log level.

    Arguments:
        cnf (Config): Config object.

    Returns:
        str: Service log level (eg 'debug').
    """
    level = root.level
    if level < DEBUG:
        return "all"
    if level == DEBUG:
        return "debug"
    if level <= INFO:
        return "info"
    return "none"
