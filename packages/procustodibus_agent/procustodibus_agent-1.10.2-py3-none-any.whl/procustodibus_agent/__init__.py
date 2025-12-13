"""Pro Custodibus Agent."""

from importlib_metadata import version

__version__ = version(__package__)

DISPLAY_NAME = "Pro Custodibus Agent"
DESCRIPTION = "Synchronizes your WireGuard settings with Pro Custodibus."
SERVICE_NAME = "ProCustodibusAgent"

DEFAULT_API_URL = "https://api.custodib.us"
DEFAULT_APP_URL = "https://pro.custodib.us"
DOCS_URL = "https://docs.procustodibus.com"
