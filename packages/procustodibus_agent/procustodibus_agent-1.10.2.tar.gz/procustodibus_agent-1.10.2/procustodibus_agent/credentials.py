"""Pro Custodibus credentials tool.

Generates Pro Custodibus credentials from the configured agent-setup code.

Usage:
  procustodibus-credentials [--config=CONFIG] [-v | -vv | --verbosity=LEVEL]
  procustodibus-credentials --help
  procustodibus-credentials --version

Options:
  -h --help             Show this help
  --version             Show agent version
  -c --config=CONFIG    Config file
  --verbosity=LEVEL     Log level (ERROR, WARNING, INFO, DEBUG)
  -v                    INFO verbosity
  -vv                   DEBUG verbosity
"""

from docopt import docopt

from procustodibus_agent import __version__ as version
from procustodibus_agent.api import setup_api
from procustodibus_agent.cnf import Cnf


def main():
    """Tool entry point."""
    args = docopt(__doc__)
    if args["--version"]:
        # print version to stdout
        print("procustodibus-credentials " + version)  # noqa: T201
    else:
        run(
            args["--config"],
            args["--verbosity"] or args["-v"],
        )


def run(*args):
    """Runs tool.

    Arguments:
        *args (list): List of arguments to pass to Cnf constructor.
    """
    cnf = Cnf(*args)

    if not cnf.agent and type(cnf.setup) is dict:
        cnf.agent = cnf.setup.get("agent")

    if not cnf.host:
        cnf.host = "ignored"

    setup_api(cnf)


if __name__ == "__main__":
    main()
