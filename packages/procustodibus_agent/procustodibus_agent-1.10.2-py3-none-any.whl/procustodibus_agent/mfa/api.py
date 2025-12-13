"""MFA API utilities."""

from procustodibus_agent.api import (
    encode_base64_web,
    request_from_api,
    request_with_session,
)
from procustodibus_agent.cnf import Cnf


def check_mfa_api(cnf, endpoint):
    """Checks if MFA for specified endpoint has expired.

    Arguments:
        cnf (Config): Config object.
        endpoint (str): Endpoint ID.

    Returns:
        str: OK, EXPIRED, UPDATING, or UNKNOWN.
    """
    if cnf is None:
        cnf = Cnf()
    return request_from_api(cnf, "GET", f"endpoints/{endpoint}/psk-rotation").text


def list_mfa_api(cnf):
    """Lists MFA state for all endpoints of the configured host.

    Arguments:
        cnf (Config): Config object.

    Returns:
        Response: Response json.
    """
    params = {"included": "connection", "max": 1000}
    return request_with_session(cnf, "GET", "endpoints", params=params).json()


def do_mfa_api(cnf, endpoint, user, token):
    """Synchorizes the MFA key of the specified endpoint.

    Arguments:
        cnf (Config): Config object.
        endpoint (str): Endpoint ID.
        user (str): User ID.
        token (str): Session token.

    Returns:
        Response: Response json.
    """
    url = f"endpoints/{endpoint}/psk-synchronize"
    authn = f"X-Custos user=^{user}, session=^{token}"
    return request_from_api(cnf, "POST", url, headers={"authorization": authn}).json()


def login_api_with_password(cnf, user, password, secondary_code=None):
    """Authenticates with specified username and password.

    Arguments:
        cnf (Config): Config object.
        user (str): User ID.
        password (str): Password.
        secondary_code (str): Optional secondary verification code.

    Returns:
        str: Session token.
    """
    url = "sessions"
    password = encode_base64_web(password.encode("utf-8"))
    if secondary_code:
        code = encode_base64_web(secondary_code.encode("utf-8"))
        authn = f"X-Custos user=^{user}, password={password}, secondary_code={code}"
    else:
        authn = f"X-Custos user=^{user}, password={password}"

    response = request_from_api(cnf, "POST", url, headers={"authorization": authn})
    return response.json()["data"][0]["attributes"]["token"]
