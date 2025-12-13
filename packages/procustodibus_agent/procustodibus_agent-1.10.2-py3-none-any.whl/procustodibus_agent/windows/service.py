"""cx_Freeze Win32Service for the agent."""

import sys
from pathlib import Path
from threading import Event

# cx_Logging only needs to be installed in the build_exe environment
try:
    import cx_Logging
except ImportError:
    cx_Logging = None  # noqa: N816

from procustodibus_agent.agent import ping_loop
from procustodibus_agent.cnf import Cnf
from procustodibus_agent.executor.execution import set_sys_cmd
from procustodibus_agent.executor.sys_cmd import WireSockSysCmd
from procustodibus_agent.windows.cnf import restrict_access_to_cnf_dir

LOG_LEVEL = "INFO"
LOOP_SECONDS = 120


class Service:
    """cx_Freeze Win32Service for the agent."""

    def initialize(self, cnf_file):
        """Called when the service is starting.

        Arguments:
            cnf_file (str): Path to configuration file.
        """
        try:
            init_log()
            cnf_file = normalize_cnf_file(cnf_file)
            self.cnf = Cnf(cnf_file, LOG_LEVEL, LOOP_SECONDS)
            self.event_loop = Event()
            init_wiresock(self.cnf)
        except Exception:  # noqa: BLE001
            cx_Logging.LogException()

    def run(self):
        """Called when the service is running."""
        init_args = [self.cnf.cnf_file, LOG_LEVEL, LOOP_SECONDS]
        try:
            restrict_access_to_cnf_dir(self.cnf)
            ping_loop(self.cnf, init_args, event_loop=self.event_loop)
        except Exception:  # noqa: BLE001
            cx_Logging.LogException()

    def stop(self):
        """Called when the service is stopping."""
        self.event_loop.set()


def init_log():
    """Initializes service logging."""
    log_dir = get_log_dir()
    cx_Logging.StartLogging(str(log_dir / "init.log"), cx_Logging.DEBUG)
    sys.stdout = open(log_dir / "stdout.log", "a")  # noqa: SIM115


def get_log_dir():
    """Gets service logging directory.

    Returns:
        str: Path to logging directory.
    """
    executable_dir = Path(sys.executable).parent
    log_dir = executable_dir / "log"
    Path.mkdir(log_dir, parents=True, exist_ok=True)
    return log_dir


def normalize_cnf_file(cnf_file):
    """Checks that specified configuration file has the correct file extension.

    Arguments:
        cnf_file (str): Path to configuration file.

    Returns:
        str: Path to configuration file or blank.
    """
    file = cnf_file if cnf_file and cnf_file.endswith(".conf") else ""
    cx_Logging.Debug("service config is %r", file)
    return file


def init_wiresock(cnf):
    """Initializes WireSock if necessary.

    Arguments:
        cnf (Config): Config object.
    """
    if cnf.wiresock:
        set_sys_cmd(WireSockSysCmd())
