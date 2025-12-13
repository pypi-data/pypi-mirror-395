"""API utilities."""

import time
from base64 import urlsafe_b64encode
from datetime import datetime, timezone
from json import dumps
from pathlib import Path
from random import randint
from socket import AI_CANONNAME, gaierror, getaddrinfo, gethostname

import requests
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey
from requests import Request, Session

from procustodibus_agent import DOCS_URL
from procustodibus_agent import __version__ as version
from procustodibus_agent.cnf import load_cnf
from procustodibus_agent.resolve_hostname import ResolverHTTPAdapter, get_resolver

API_TIMEOUT = 16  # seconds
UTC = timezone.utc


def get_session_transport(cnf):
    """Finds or creates session object cached for the specified config.

    Arguments:
        cnf (Config): Config object.

    Returns:
        Session: Requests session object.
    """
    session = cnf.transport
    if not session:
        adapter = ResolverHTTPAdapter(
            resolver=get_resolver(cnf),
            socket_mark=cnf.socket_mark,
        )
        session = Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        cnf.transport = session
    return session


def send_to_api(cnf, request, *, raises=True):
    """Sends request to the API.

    Arguments:
        cnf (Config): Config object.
        request (Request): Request object to send.
        raises (bool): True to raise on error response (default True).

    Returns:
        Response: Response object.
    """
    session = get_session_transport(cnf)

    if not hasattr(request, "body"):
        request = request.prepare()
    response = session.send(request, timeout=API_TIMEOUT)

    if raises:
        response.raise_for_status()
    return response


def request_from_api(cnf, method, url, **kwargs):
    """Sends request to the API.

    Arguments:
        cnf (Config): Config object.
        method (str): Request method (eg "GET").
        url (str): Relative request URL (eg "hosts/123").
        **kwargs (dict): Dict of arguments to pass to Request constructor.

    Returns:
        Response: Response object.
    """
    if not cnf.api:
        _raise_setup_issue("Missing conf for API endpoint")
    raises = kwargs.pop("raises", True)
    request = Request(method, f"{cnf.api}/{url}", **kwargs)
    return send_to_api(cnf, request, raises=raises)


def setup_api(cnf):
    """Generates and saves new credential for configured agent.

    Arguments:
        cnf (Config): Config object.
    """
    raise_unless_has_cnf(cnf)
    setup = load_setup(cnf)
    code = setup["code"]

    signing_key = SigningKey.generate()
    public_key = signing_key.verify_key.encode(Base64Encoder).decode("utf-8")

    url = f"users/{cnf.agent}/credentials/signature"
    headers = {
        "authorization": f"X-Custos user=^{cnf.agent}, agent_setup=^{code}",
        "content-type": "application/json",
    }
    data = dumps(
        {
            "secret": public_key,
            "description": f"on {getfqdn()}",
            "keep_others": setup.get("keep_others") or False,
        },
        separators=(",", ":"),
    )

    request_from_api(cnf, "POST", url, data=data, headers=headers)
    save_signing_key(cnf, signing_key)


def login_api(cnf):
    """Logs into the api and saves session token on cnf obj.

    Arguments:
        cnf (Config): Config object.
    """
    raise_unless_has_cnf(cnf)

    challenge = get_signing_challenge(cnf)["data"][0]
    challenge_id = challenge["id"]
    signature = sign_data(cnf, challenge["attributes"]["value"].encode("utf-8"))

    headers = {
        "authorization": f"X-Custos user=^{cnf.agent}"
        f", challenge=^{challenge_id}"
        f", signature={signature}",
    }
    response = request_from_api(cnf, "POST", "sessions", headers=headers)

    # add 1-10 minutes of jitter before real session timeout
    # to prevent repeating stampeding herd on every login
    jitter = randint(60, 600)  # noqa: S311

    session = response.json()["data"][0]
    cnf.session = {
        "token": session["attributes"]["token"],
        "expiration": time.time() + session["meta"]["expiration_timeout"] - jitter,
    }


def ping_api(cnf, interfaces, executed=None):
    """Sends ping request to API.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from `wg show`.
        executed (list): List of executed desired changes.

    Returns:
        Response: Response json.
    """
    raise_unless_has_cnf(cnf)

    data = {"interfaces": interfaces}
    if executed:
        data["executed"] = executed

    agent = build_agent_info(cnf)
    if agent:
        data["agent"] = agent

    response = request_with_session(
        cnf,
        "POST",
        f"hosts/{cnf.host}/ping/{version}",
        data=dumps(data, separators=(",", ":")),
        headers={"content-type": "application/json"},
    )
    return response.json()


def get_health_info(cnf):
    """Gets the api's health info.

    Arguments:
        cnf (Config): Config object.

    Returns:
        Response: Response json.
    """
    return request_from_api(cnf, "GET", "health").json()


def get_host_info(cnf):
    """Gets the configured host's info from the API.

    Arguments:
        cnf (Config): Config object.

    Returns:
        Response: Response json.
    """
    return request_with_session(cnf, "GET", f"hosts/{cnf.host}").json()


def send_with_session(cnf, request):
    """Sends request with session authn header.

    Arguments:
        cnf (Config): Config object.
        request (Request): Request object to send.

    Returns:
        Response: Response object.
    """
    create_session_if_expired(cnf)
    prepped = request.prepare()
    prepped.headers["authorization"] = build_authn_header(cnf)

    response = send_to_api(cnf, prepped, raises=False)

    if response.status_code == requests.codes.unauthorized:
        login_api(cnf)
        prepped = request.prepare()
        prepped.headers["authorization"] = build_authn_header(cnf)
        response = send_to_api(cnf, prepped, raises=False)

    response.raise_for_status()
    return response


def request_with_session(cnf, method, url, **kwargs):
    """Sends request with session authn header.

    Arguments:
        cnf (Config): Config object.
        method (str): Request method (eg "GET").
        url (str): Relative request URL (eg "hosts/123").
        **kwargs (dict): Dict of arguments to pass to Request constructor.

    Returns:
        Response: Response object.
    """
    request = Request(method, f"{cnf.api}/{url}", **kwargs)
    return send_with_session(cnf, request)


def create_session_if_expired(cnf):
    """Creates a new session if session is missing or has timed-out.

    Arguments:
        cnf (Config): Config object.
    """
    raise_unless_has_cnf(cnf)
    session = cnf.__dict__.get("session")
    if not session or session["expiration"] < time.time():
        login_api(cnf)


def build_authn_header(cnf):
    """Constructs authn header with session token.

    Arguments:
        cnf (Config): Config object.

    Returns:
        str: Authn header
    """
    return f"X-Custos user=^{cnf.agent}, session=^{cnf.session['token']}"


def get_signing_challenge(cnf):
    """Gets the api's current authn challenge data.

    Arguments:
        cnf (Config): Config object.

    Returns:
        Response: Response json.
    """
    return request_from_api(cnf, "GET", "sessions/challenge").json()


def sign_data(cnf, data):
    """Signs the specified message.

    Arguments:
        cnf (Config): Config object.
        data (bytes): Message to sign.

    Returns:
        str: Base64-web-encoded signature.
    """
    signing_key = load_signing_key(cnf)
    signed_message = signing_key.sign(data)
    return encode_base64_web(signed_message.signature)


def load_signing_key(cnf):
    """Loads the agent's signing key.

    Arguments:
        cnf (Config): Config object.

    Returns:
        SingingKey: Agent's signing key.

    Propagates:
        ValueError: If the signing credentials are missing or invalid.
    """
    try:
        credentials = _load_credentials_dict(cnf.credentials, "credentials")
        private_key = credentials["private_key"]
    except KeyError:
        _raise_setup_issue("Missing private key in credentials file")

    try:
        return SigningKey(private_key, Base64Encoder)
    except Exception:  # noqa: BLE001
        _raise_setup_issue("Invalid private key in credentials file")


def encode_base64_web(message):
    """Base64-web-encodes the specified message.

    Arguments:
        message (str): Message to encode.

    Returns:
        str: Base64-web-encoded message.
    """
    return urlsafe_b64encode(message).decode("utf-8").rstrip("=")


def format_datetime(now=None):
    """Formats datetime as an RFC 3339 string.

    Arguments:
        now (datetime): Datetime to format (defaults to now).

    Returns:
        str: Formatted datetime.
    """
    if not now:
        now = time.time()
    return datetime.fromtimestamp(now, tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_agent_info(cnf):
    """Builds dict of agent info to send to API.

    Arguments:
        cnf (Config): Config object.

    Returns:
        dict: Agent info dict.
    """
    keys = ["read_only", "redact_secrets", "unmanaged_interfaces"]
    if cnf.resolve_hostnames != "auto":
        keys.append("resolve_hostnames")

    return {key: getattr(cnf, key) for key in keys if getattr(cnf, key)}


def load_setup(cnf):
    """Loads the setup configuration dict, or raises an error.

    Arguments:
        cnf (Config): Config object.

    Returns:
        dict: Setup configuration dict.

    Propagates:
        ValueError: If the setup config is missing the "code" property, or
                    the "expires" property indicates it has expired, or
                    if generated credentials cannot be saved because there is
                    no configured path to the credentials file.
    """
    if type(cnf.credentials) is dict:
        _raise_setup_issue("Missing path to credentials file")

    try:
        setup = _load_credentials_dict(cnf.setup, "setup")
        setup["code"]
    except KeyError:
        _raise_setup_issue("Missing code in setup file")

    expires = setup.get("expires")
    if expires:
        expires = datetime.strptime(expires, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        now = datetime.now(tz=UTC)
        if expires < now:
            _raise_setup_issue("Setup code has expired")

    return setup


def save_signing_key(cnf, signing_key):
    """Saves the specified signing key to the configured credentials location.

    Also deletes the configured setup file (to indicate setup is complete).

    Arguments:
        cnf (Config): Config object.
        signing_key (SigningKey): Signing key to save.
    """
    private_key = signing_key.encode(Base64Encoder).decode("utf-8")
    public_key = signing_key.verify_key.encode(Base64Encoder).decode("utf-8")

    credentials = f"""
        # procustodibus-credentials.conf generated {format_datetime()}
        # for agent {cnf.agent} on {getfqdn()}
        [Procustodibus.Credentials]
        PublicKey = {public_key}
        PrivateKey = {private_key}
    """.strip()

    with open(cnf.credentials, "w") as f:
        for line in credentials.splitlines():
            print(line.strip(), file=f)

    Path(cnf.credentials).chmod(0o640)

    if type(cnf.setup) is not dict:
        Path(cnf.setup).unlink()


def getfqdn():
    """Looks up fully-qualified domain name of localhost.

    Returns:
        str: Fully-qualified domain name (eg 'foo.example.com').
    """
    hostname = gethostname()
    try:
        return getaddrinfo(hostname, 0, flags=AI_CANONNAME)[0][3]
    except gaierror:
        return hostname


def raise_unless_has_cnf(cnf):
    """Raises an error unless the specified cnf has all required settings.

    Arguments:
        cnf (Config): Config object.

    Propagates:
        ValueError: If the specified cnf is missing some required settings.
    """
    missing = []

    if not cnf.api:
        missing.append("API endpoint")

    if not cnf.agent:
        missing.append("Agent ID")

    if not cnf.host:
        missing.append("Host ID")

    if missing:
        _raise_setup_issue(f"Missing conf for {' and '.join(missing)}")


def _raise_setup_issue(problem):
    raise ValueError(f"{problem}; see {DOCS_URL}/guide/agents/troubleshoot/ to fix")


def _load_credentials_dict(path, key):
    """Loads the credentials in the specified ini file if not already a dict.

    Arguments:
        path: Path to credentials file or dict of credentials.
        key: Key to load in ini (eg 'credentials').

    Returns:
        dict: Dict containing credentials.

    Propagates:
        ValueError: If the specified file cannot be read.
    """
    if type(path) is dict:
        return path

    try:
        loaded = load_cnf(path)
    except OSError:
        _raise_setup_issue(f"Could not read {key} file {path}")

    return loaded["procustodibus"][key]
