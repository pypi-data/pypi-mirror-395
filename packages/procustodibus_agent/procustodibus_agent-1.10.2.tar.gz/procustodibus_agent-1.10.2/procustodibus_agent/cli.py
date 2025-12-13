"""Pro Custodibus Agent.

Synchronizes your WireGuard settings with Pro Custodibus.

Usage:
  procustodibus-agent [--config=CONFIG] [--loop=SECONDS]
                      [-v | -vv | --verbosity=LEVEL]
  procustodibus-agent --help
  procustodibus-agent --test [--config=CONFIG] [-v | -vv | --verbosity=LEVEL]
  procustodibus-agent --version

Options:
  -h --help             Show this help
  --test                Run connectivity check
  --version             Show agent version
  -c --config=CONFIG    Config file
  -l --loop=SECONDS     Loop indefinitely, sending ping every SECONDS
  --verbosity=LEVEL     Log level (ERROR, WARNING, INFO, DEBUG)
  -v                    INFO verbosity
  -vv                   DEBUG verbosity
"""

import sys

from docopt import docopt

from procustodibus_agent import __version__ as version
from procustodibus_agent.agent import ping, ping_loop
from procustodibus_agent.cnf import Cnf
from procustodibus_agent.connectivity import check_connectivity


def main():
    """CLI Entry point."""
    args = docopt(__doc__)
    if args["--version"]:
        # print version to stdout
        print("procustodibus-agent " + version)  # noqa: T201
    elif args["--test"]:
        check(args["--config"], args["--verbosity"] or args["-v"])
    else:
        run(
            args["--config"],
            args["--verbosity"] or args["-v"],
            args["--loop"],
        )


def check(*args):
    """Runs connectivity check.

    Arguments:
        *args (list): List of arguments to pass to Cnf constructor.
    """
    cnf = Cnf(*args)
    sys.exit(check_connectivity(cnf))


def run(*args):
    """Runs CLI.

    Arguments:
        *args (list): List of arguments to pass to Cnf constructor.
    """
    cnf = Cnf(*args)

    if cnf.loop:
        ping_loop(cnf, args)
    else:
        ping(cnf)


if __name__ == "__main__":
    main()
