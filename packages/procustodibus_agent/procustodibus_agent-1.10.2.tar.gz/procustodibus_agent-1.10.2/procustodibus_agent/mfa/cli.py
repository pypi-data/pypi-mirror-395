"""Pro Custodibus multifactor authentication tool.

Checks WireGuard multifactor authentication state,
and enables the interactive portion of multifactor authentication.

Usage:
  procustodibus-mfa [--config=CONFIG] [-v | -vv | --verbosity=LEVEL]
  procustodibus-mfa --auth=USER --endpoint=ENDPOINT [--password-fd=NUMBER]
          [--secondary-code=CODE | --secondary-fd=NUMBER | --secondary-prompt]
          [--config=CONFIG] [-v | -vv | --verbosity=LEVEL]
  procustodibus-mfa --check --endpoint=ENDPOINT [--config=CONFIG]
  procustodibus-mfa --help
  procustodibus-mfa --version

Options:
  -h --help               Show this help
  --version               Show agent version
  -a --auth=USER          ID of user to authenticate as
  --password-fd=NUMBER    File descriptor to use instead of password prompt
  --secondary-code=CODE   Secondary verification code
  --secondary-fd=NUMBER   File descriptor to use for secondary code
  --secondary-prompt      Prompt for secondary code
  --check                 Check a single endpoint
  -e --endpoint=ENDPOINT  ID of endpoint to check/authenticate
  -c --config=CONFIG      Config file
  --verbosity=LEVEL       Log level (ERROR, WARNING, INFO, DEBUG)
  -v                      INFO verbosity
  -vv                     DEBUG verbosity

Examples:
  $ procustodibus-mfa
  Interface    Endpoint       ID           State
  -----------  -------------  -----------  ------------------------------
  wg-prod      Prod Server 1  ZSp2TSWJ6Ge  EXPIRED
  wg-prod      Prod Server 2  63Wa7kQ68oH  OK until 01/01/20 01:00:00 PST
  wg-dev       Test Server    USBiuu8PBZw  -
  $ procustodibus-mfa --check --endpoint=ZSp2TSWJ6Ge
  EXPIRED
  $ procustodibus-mfa --auth=Ahg1opVcGX --endpoint=ZSp2TSWJ6Ge
  Password: ********
  OK until 01/01/20 08:00:00 PST
"""

from docopt import docopt

from procustodibus_agent import __version__ as version
from procustodibus_agent.cnf import Cnf
from procustodibus_agent.mfa import check_mfa, do_mfa, list_mfa, read_password


def main():
    """Tool entry point."""
    args = docopt(__doc__)
    if args["--version"]:
        # print version to stdout
        print("procustodibus-mfa " + version)  # noqa: T201
    elif args["--auth"]:
        authenticate(
            args["--endpoint"],
            args["--auth"],
            args["--password-fd"],
            args["--secondary-code"],
            args["--secondary-fd"],
            args["--secondary-prompt"],
            args["--config"],
            args["--verbosity"] or args["-v"],
        )
    elif args["--check"]:
        check(args["--endpoint"], args["--config"])
    else:
        run(args["--config"], args["--verbosity"] or args["-v"])


def authenticate(
    endpoint,
    user,
    password_input=None,
    secondary_code=None,
    secondary_input=None,
    secondary_prompt=False,  # noqa: FBT002
    cnf_file="",
    verbosity=None,
):
    """Authenticates the specified user for the specified endpoint.

    Arguments:
        endpoint (str): Endpoint ID.
        user (str): User ID.
        password_input (str): Optional file descriptor from which to read password.
        secondary_code (str): Optional secondary verification code.
        secondary_input (str): Optional file descriptor from which to read code.
        secondary_prompt (bool): True to prompt for code.
        cnf_file (str): Optional path to config file.
        verbosity: Root log level.
    """
    if secondary_prompt:
        secondary_prompt = "Secondary code: "
    cnf = Cnf(cnf_file, verbosity)
    password = read_password(None, password_input, prompt=True)
    secondary_code = read_password(secondary_code, secondary_input, secondary_prompt)
    do_mfa(cnf, endpoint, user, password, secondary_code)


def check(endpoint, cnf_file=""):
    """Checks the MFA state of the specified endpoint.

    Arguments:
        endpoint (str): Endpoint ID.
        cnf_file (str): Path to config file (optional).
    """
    cnf = Cnf(cnf_file)
    check_mfa(cnf, endpoint)


def run(*args):
    """Lists MFA state for all endpoints of the configured host.

    Arguments:
        *args (list): List of arguments to pass to Cnf constructor.
    """
    cnf = Cnf(*args)
    list_mfa(cnf)


if __name__ == "__main__":
    main()
