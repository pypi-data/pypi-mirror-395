"""Utilities for updating endpoints with resolved hostnames."""

from base64 import urlsafe_b64encode
from contextlib import suppress
from logging import getLogger
from re import fullmatch, search
from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, getaddrinfo
from socket import socket as make_socket
from threading import Event, Thread
from time import time
from urllib.parse import urlsplit, urlunsplit

from dns.exception import DNSException
from dns.message import from_wire as message_from_wire
from dns.message import make_query
from dns.name import from_text as make_qname
from dns.query import BadResponse
from dns.query import _connect as connect_tcp
from dns.query import tcp as query_tcp
from dns.query import udp as query_udp
from dns.rcode import NOERROR, NXDOMAIN
from dns.rcode import to_text as format_rcode
from dns.rdataclass import IN
from dns.rdatatype import AAAA, A
from dns.resolver import Answer, Cache, NoAnswer
from requests import Request, Session
from requests.adapters import HTTPAdapter

from procustodibus_agent.cnf import DEFAULT_DNS_SERVERS
from procustodibus_agent.wg import run_wg_set

QUAD_SERVERS = {"1.1.1.1", "8.8.8.8", "9.9.9.9"}
PREFER_IPV6_SERVERS = DEFAULT_DNS_SERVERS[2:4] + DEFAULT_DNS_SERVERS[0:2]
# linux/include/uapi/asm-generic/socket.h
SO_MARK = 36


def is_likely_ip(hostname):
    """Checks if a hostname is likely an IP address.

    Arguments:
        hostname (str): Hostname to check (eg 'foo.example.com').

    Returns:
        True if likely an IP address.
    """
    return bool(
        hostname
        and (
            search(r"[0-9](\.[0-9]{1,3}){3}\]?$", hostname)
            or (
                fullmatch(r"\[?[0-9A-Fa-f:]+\]?", hostname)
                and search(":[^:]*:", hostname)
            )
        )
    )


def lookup_ip(cnf, hostname, family=None, *, raises=True):
    """Looks up the top IP address for the specified hostname.

    Arguments:
        cnf (Config): Config object.
        hostname (str): Hostname to lookup (eg 'foo.example.com').
        family (int): Preferred family (eg AF_INET6).
        raises (bool): True to raise if cannot resolve hostname (default True).

    Returns:
        str: Top IP address (eg '10.1.2.3').

    Propagates:
        DNSException: Cannot resolve hostname.
    """
    ips = lookup_ips(cnf, hostname, family, raises=raises)
    return ips[0] if ips else ""


def lookup_ips(cnf, hostname, family=None, *, raises=True):
    """Looks up the IP addresses for the specified hostname.

    Arguments:
        cnf (Config): Config object.
        hostname (str): Hostname to lookup (eg 'foo.example.com').
        family (int): Preferred family (eg AF_INET6).
        raises (bool): True to raise if cannot resolve hostname (default True).

    Returns:
        list: IP addresss (eg ['10.1.2.3', '10.4.5.6']).

    Raises:
        Exception: Cannot resolve hostname.
    """
    try:
        return get_resolver(cnf).lookup_ips(hostname, family)
    except Exception as e:
        if raises:
            raise
        message = f"dns error resolving {hostname}: {e}"
        getLogger(__name__).debug(message)
        return []


def get_resolver(cnf):
    """Finds or creates resolver for the specified configuration object.

    Arguments:
        cnf (Config): Config object.

    Returns:
        Resolver: Resolver object.
    """
    resolver = cnf.resolver
    if not resolver:
        resolver = DnsResolver(cnf)
        cnf.resolver = resolver
    return resolver


class Resolver(dict):
    """Base hostname resolver."""

    def lookup_ips(self, _hostname, _family=None):
        """Looks up the IP addresses for the specified hostname.

        Arguments:
            hostname (str): Hostname to lookup (eg 'foo.example.com').
            family (int): Preferred family (eg AF_INET6).

        Raises:
            DNSException: Cannot resolve hostname.
        """
        raise DNSException("cannot resolve hostnames")


class DictionaryResolver(Resolver):
    """Resolves hostnames through static dictionary."""

    def __init__(self, dictionary=None):
        """Creates new resolver object.

        Arguments:
            dictionary (dict): Map of hostnames to ip addresses.
        """
        self.dictionary = {} if dictionary is None else dictionary

    def __str__(self):  # noqa: D105
        return str(self.dictionary)

    def lookup_ips(self, hostname, _family=None):
        """Looks up the IP addresses for the specified hostname.

        Arguments:
            hostname (str): Hostname to lookup (eg 'foo.example.com').
            family (int): Preferred family (eg AF_INET6).

        Returns:
            list: IP addresss (eg ['10.1.2.3', '10.4.5.6']).

        Raises:
            DNSException: Cannot resolve hostname.
        """
        answer = self.dictionary.get(hostname)
        if answer is None:
            raise DNSException(f"hostname not found: {hostname}")
        return answer

    def __bool__(self):  # noqa: D105
        return bool(self.dictionary)


class DnsResolver(Resolver):
    """Resolves hostnames through DNS queries, caching results."""

    class _MinimumCnf(dict):
        """Configuration object with defaults for resolver."""

        def __init__(self, resolve_hostnames=""):
            """Creates minimal configuration object.

            Arguments:
                resolve_hostnames (str): Family preference (eg "ipv4" or "ipv6").
            """
            self.dns = []
            self.dns_protocol = ""
            self.dns_timeout = 5.0
            self.dns_timeout_primary = 0.5
            self.doh = ""
            self.resolve_hostnames = resolve_hostnames
            self.socket_mark = ""
            self.transport = None

    def __init__(self, cnf=None, resolve_hostnames=""):
        """Creates new resolver object.

        Arguments:
            cnf (Config): Config object.
            resolve_hostnames (str): Family preference (eg "ipv4" or "ipv6").
        """
        self.cnf = cnf or self._MinimumCnf(resolve_hostnames)
        self.cache = Cache()
        self.prefer_ipv6, self.has_ipv6 = self._calculate_prefer_ipv6()
        self.dns_servers = self._calculate_dns_servers()
        self.doh_url, self.doh_hostname = self._calculate_doh_url()

    def __str__(self):  # noqa: D105
        return f"{self.doh_hostname}#{self.cnf.dns}"

    def flip_ipv6_preference(self):
        """Reverses preference for ipv6 vs ipv4."""
        old = 6 if self.prefer_ipv6 else 4
        new = 4 if old == 6 else 6
        getLogger(__name__).info("adjusting preference from ipv%s to ipv%s", old, new)
        self.prefer_ipv6 = not self.prefer_ipv6
        ipv4_servers = [x for x in self.dns_servers if ":" not in x]
        ipv6_servers = [x for x in self.dns_servers if ":" in x]
        self.dns_servers = (
            ipv6_servers + ipv4_servers
            if self.prefer_ipv6
            else ipv4_servers + ipv6_servers
        )

    def lookup_ips(self, hostname, family=None):
        """Looks up the IP addresses for the specified hostname.

        Arguments:
            hostname (str): Hostname to lookup (eg 'foo.example.com').
            family (int): Preferred family (eg AF_INET6).

        Returns:
            list: IP addresss (eg ['10.1.2.3', '10.4.5.6']).

        Propagates:
            DNSException: Cannot resolve hostname.
        """
        return self.lookup_ips_from_cache(
            hostname, family
        ) or self.lookup_ips_from_servers(hostname, family)

    def lookup_ips_from_cache(self, hostname, family=None):
        """Looks up the IP addresses for the specified hostname in the cache.

        Arguments:
            hostname (str): Hostname to lookup (eg 'foo.example.com').
            family (int): Preferred family (eg AF_INET6).

        Returns:
            list: IP addresses, or empty if not in cache.

        Raises:
            NoAnswer: Cached response was that the hostname has no IP addresses.
        """
        if not self.dns_servers:
            return []

        qname = make_qname(hostname)
        rdtype = AAAA if family == AF_INET6 or (not family and self.prefer_ipv6) else A
        answer = self.cache.get((qname, rdtype, IN))
        # check non-preferred type only if preferred type is NXDOMAIN
        if not family and not answer and answer is not None:
            answer2 = self.cache.get((qname, AAAA if rdtype == A else A, IN))
            if answer2:
                answer = answer2

        # NB: the Answer object is falsy if it has no rrset sections
        # (ie the server answered with an empty list of addresses, aka NXDOMAIN)
        if answer is None:
            return []
        if not answer:
            raise NoAnswer(response=answer.response)

        return [x.address for x in answer]

    def lookup_ips_from_servers(self, hostname, family=None):
        """Looks up the IP addresses for the specified hostname from DNS.

        Arguments:
            hostname (str): Hostname to lookup (eg 'foo.example.com').
            family (int): Preferred family (eg AF_INET6).

        Returns:
            list: IP addresss (eg ['10.1.2.3', '10.4.5.6']).

        Propagates:
            DNSException: Cannot resolve hostname.
        """
        if not self.dns_servers:
            return self.lookup_ips_from_gai(hostname, family)
        return QueryRunner(hostname, family).run(self)

    def lookup_ips_from_gai(self, hostname, family=None):
        """Looks up the IP addresses for the specified hostname from OS.

        Arguments:
            hostname (str): Hostname to lookup (eg 'foo.example.com').
            family (int): Preferred family (eg AF_INET6).

        Returns:
            list: IP addresss (eg ['10.1.2.3', '10.4.5.6']).

        Raises:
            DNSException: Cannot resolve hostname.
        """
        preferred = family or (AF_INET6 if self.prefer_ipv6 else AF_INET)
        try:
            return [x[4][0] for x in getaddrinfo(hostname, 0, preferred)]
        except Exception as e:
            if not family:
                other = AF_INET if self.prefer_ipv6 else AF_INET6
                return self.lookup_ips_from_gai(hostname, other)
            raise DNSException(f"dns error resolving {hostname}: {e}") from e

    def query_server(self, query, server):
        """Sends the specified query to the specified server.

        Arguments:
            query (Message): Message object.
            server (str): DNS server to query (eg '9.9.9.9').

        Returns:
            tuple: Response object, server port used.
        """
        protocol = self.cnf.dns_protocol
        if protocol == "doh" and self.doh_hostname:
            return (self.query_with_doh(query, server), 443)
        if protocol == "tcp":
            return (self.query_with_tcp(query, server), 53)
        return (self.query_with_udp(query, server), 53)

    def query_with_udp(self, query, server):
        """Sends the specified query to the specified server with UDP.

        Arguments:
            query (Message): Message object.
            server (str): DNS server to query (eg '9.9.9.9').

        Returns:
            Response object.
        """
        timeout = self.cnf.dns_timeout
        socket = self._make_socket(server, SOCK_DGRAM)
        try:
            return query_udp(query, server, timeout, sock=socket)
        finally:
            socket.close()

    def query_with_tcp(self, query, server):
        """Sends the specified query to the specified server with TCP.

        Arguments:
            query (Message): Message object.
            server (str): DNS server to query (eg '9.9.9.9').

        Returns:
            Response object.
        """
        timeout = self.cnf.dns_timeout
        socket = self._make_socket(server, SOCK_STREAM)
        try:
            connect_tcp(socket, (server, 53), time() + timeout)
            return query_tcp(query, server, timeout, sock=socket)
        finally:
            socket.close()

    def query_with_doh(self, query, server):
        """Sends the specified query to the specified server with DoH.

        Arguments:
            query (Message): Message object.
            server (str): DNS server to query (eg '9.9.9.9').

        Returns:
            Response object.
        """
        timeout = self.cnf.dns_timeout
        session = self._make_session(server)
        return query_doh(query, self.doh_url, timeout, session)

    def __bool__(self):  # noqa: D105
        return True

    def _make_socket(self, ip, socket_type):
        """Creates a new socket of the specified type.

        Arguments:
            ip (str): Server IP address.
            socket_type (int): SOCK_STREAM or SOCK_DGRAM.

        Raises:
            Exception: Socket set-up failed.

        Returns:
            Socket object.
        """
        socket = make_socket(AF_INET6 if ":" in ip else AF_INET, socket_type)
        try:
            socket.setblocking(False)  # noqa: FBT003
            mark = coerce_socket_mark(self.cnf.socket_mark)
            if mark:
                socket.setsockopt(SOL_SOCKET, SO_MARK, mark)
        except Exception:
            socket.close()
            raise
        else:
            return socket

    def _make_session(self, ip):
        """Creates a new requests session for the specified server IP.

        Arguments:
            ip (str): Server IP address.

        Returns:
            Session object.
        """
        resolver = DictionaryResolver(dictionary={self.doh_hostname: [ip]})
        adapter = ResolverHTTPAdapter(
            resolver=resolver,
            socket_mark=self.cnf.socket_mark,
        )
        session = Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _calculate_prefer_ipv6(self):
        """Checks if IPv6 is preferred and available.

        Returns:
            tuple: True if IPv6 preferred, True if IPv6 available
        """
        if self.cnf.resolve_hostnames == "ipv6":
            return (True, True)
        if self.cnf.resolve_hostnames == "ipv4":
            return (False, False)
        # if no explicit preference, use ipv6 if preferred address for localhost is ipv6
        try:
            families = [x[0] for x in getaddrinfo("localhost", 0)]
            return (families[0] == AF_INET6, AF_INET6 in families)
        except Exception:  # noqa: BLE001
            return (False, False)

    def _calculate_dns_servers(self):
        """Returns list of DNS servers in preferred order.

        Returns:
            list: List of DNS servers.
        """
        servers = self.cnf.dns
        servers_6 = [x for x in servers if ":" in x]
        servers_4 = [x for x in servers if ":" not in x]

        # if ipv6 not available, use just ipv4 servers
        if not self.has_ipv6 and servers_4:
            return servers_4
        # when ipv6 is preferred, reorder default ipv6 servers first
        if self.prefer_ipv6 and len(servers) > 1 and servers[0] in QUAD_SERVERS:
            return servers_6 + servers_4
        return servers

    def _calculate_doh_url(self):
        """Returns URL and hostname to use for DoH.

        Returns:
            Tuple of DoH URL, DoH hostname
            (eg ('https://example.org/dns-query', 'example.org')).
        """
        doh = self.cnf.doh
        protocol = self.cnf.dns_protocol
        if protocol == "https" or doh:
            self.cnf.dns_protocol = "doh"
        if doh.startswith(("https:", "http:")):
            return (doh, urlsplit(doh).hostname)
        if not doh:
            servers = self.cnf.dns
            if "9.9.9.9" in servers:
                doh = "dns.quad9.net"
            elif "1.1.1.1" in servers:
                doh = "cloudflare-dns.com"
            elif "8.8.8.8" in servers:
                doh = "dns.google"
        return (f"https://{doh}/dns-query", doh)


class ErrorAnswer(NoAnswer):
    """The DNS response was an error."""

    supp_kwargs = {"response"}

    def __init__(self, *args, **kwargs):  # noqa: D107
        super().__init__(*args, **kwargs)

    def __str__(self):  # noqa: D105
        return f"The DNS response was {self.rcode()} to the question: {self.query()}"

    def query(self):
        """Formats DNS query.

        Returns:
            str: DNS query.
        """
        q = self.kwargs["response"].question
        return str(q[0]) if q else ""

    def rcode(self):
        """Formats DNS response code.

        Returns:
            str: DNS response code.
        """
        return format_rcode(self.kwargs["response"].rcode())


class ResolverHTTPAdapter(HTTPAdapter):
    """Custom requests library HTTP adapter."""

    def __init__(self, *args, **kwargs):
        """Creates new adapter.

        Arguments:
            *args (list): List of arguments to pass to super.
            **kwargs (dict): Dictionary of arguments to pass to super.
        """
        self.resolver = kwargs.pop("resolver", None)
        self.socket_mark = kwargs.pop("socket_mark", None)
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        """Initializes the adapter's connection pool manager.

        Arguments:
            *args (list): List of arguments to pass to super.
            **kwargs (dict): Dictionary of arguments to pass to super.
        """
        mark = coerce_socket_mark(self.socket_mark)
        if mark:
            kwargs["socket_options"] = [(SOL_SOCKET, SO_MARK, mark)]
        super().init_poolmanager(*args, **kwargs)

    def send(self, request, **kwargs):
        """Sends the specified request.

        Arguments:
            request: Request object.
            **kwargs (dict): Dictionary of arguments to pass to super.

        Returns:
            Response object.
        """
        url = urlsplit(request.url)
        proxies = kwargs.get("proxies")
        if not self._is_proxied(proxies, url) and not is_likely_ip(url.hostname):
            self._replace_hostname_with_ip(request, url)

        return super().send(request, **kwargs)

    def _is_proxied(self, proxies, _url):
        """Checks if the specified URL should be proxied.

        Arguments:
            proxies: Dict of proxies.
            url: Parsed URL object.

        Returns:
            bool: True if is proxied.
        """
        # TODO: this should probably check whether or not any of the proxies
        # actually apply to the specific URL, and also ignore SOCKS proxies
        return bool(proxies)

    def _replace_hostname_with_ip(self, request, url):
        """Replaces hostname in request URL with resolved IP address.

        Arguments:
            request: Request object.
            url: Parsed URL object.
        """
        https = url.scheme == "https"
        hostname = url.hostname
        ip = self.resolver.lookup_ips(hostname)[0] if self.resolver else hostname
        x = format_endpoint_address(ip, url.port or (443 if https else 80))

        request.url = urlunsplit((url.scheme, x, url.path, url.query, url.fragment))
        request.headers["host"] = hostname

        pool_kw = self.poolmanager.connection_pool_kw
        if https:
            pool_kw["assert_hostname"] = hostname
        pool_kw["server_hostname"] = hostname


class QueryRunner:
    """Runs the configured DNS query against multiple DNS servers in parallel."""

    def __init__(self, hostname, family=None):
        """Initializes this runner.

        Arguments:
            hostname (str): Hostname to lookup (eg 'foo.example.com').
            family (int): Preferred family (eg AF_INET6).
        """
        self.hostname = hostname
        self.family = family
        self.qname = make_qname(hostname)
        self.event = Event()
        self.slots = []

    def run(self, resolver):
        """Runs the configured DNS query using the specified resolver.

        Runs a set of queries staggered by time across the primary and backup
        DNS servers of the specified resolver. Returns the list of resolved
        addresses from the first non-empty response. If no DNS servers respond
        with a non-empty answer within the configured timeout, raises the error
        from the most-preferred DNS server that responded (or if no servers
        respond, raises a generic 'timeout' error).

        Arguments:
            resolver (Resolver): Resolver to run query with.

        Returns:
            list: IP addresss (eg ['10.1.2.3', '10.4.5.6']).

        Raises:
            DNSException: Cannot resolve hostname.
        """
        deadline = time() + resolver.cnf.dns_timeout
        self.make_slots(resolver)

        for slot in self.slots:
            self.start_slot(slot, resolver)
            self.event.wait(resolver.cnf.dns_timeout_primary)
            self.event.clear()
            addresses = self.check_answers(resolver)
            if addresses:
                return addresses

        remaining = deadline - time()
        while remaining > 0:
            self.event.wait(remaining)
            self.event.clear()
            addresses = self.check_answers(resolver)
            if addresses:
                return addresses
            remaining = deadline - time()

        raise self.make_error()

    def make_slots(self, resolver):
        """Sets up this runner's answer slots for the specified resolver.

        Arguments:
            resolver (Resolver): Resolver to run query with.
        """
        if self.family:
            types = [AAAA] if self.family == AF_INET6 else [A]
        else:
            types = [AAAA, A] if resolver.prefer_ipv6 else [A, AAAA]

        self.slots.clear()
        for server in resolver.dns_servers:
            for rdtype in types:
                self.slots.append(AnswerSlot(server, rdtype))

    def start_slot(self, slot, resolver):
        """Starts the specified slot in a new thread with the specified resolver.

        Arguments:
            slot (AnswerSlot): Slot to run.
            resolver (Resolver): Resolver to run query with.
        """
        Thread(target=self.run_slot, args=(slot, resolver)).start()

    def run_slot(self, slot, resolver):
        """Runs the specified slot in this thread with the specified resolver.

        Arguments:
            slot (AnswerSlot): Slot to run.
            resolver (Resolver): Resolver to run query with.
        """
        server, rdtype, qname = (slot.server, slot.rdtype, self.qname)

        def debug(s, *args):
            getLogger(__name__).debug(s, server, rdtype.name, self.hostname, *args)

        try:
            debug("%s querying %s %s")
            query = make_query(qname, rdtype)
            (response, port) = resolver.query_server(query, server)

            code = response.rcode()
            if code in (NOERROR, NXDOMAIN):
                answer = Answer(qname, rdtype, IN, response, server, port)
            else:
                answer = None

            slot.code = code
            slot.response = response
            slot.answer = answer
            debug("%s resolved %s %s with %s", code.name)

        except Exception as e:  # noqa: BLE001
            slot.error = e
            debug("%s resolved %s %s with error: %s", e)

        self.event.set()

    def check_answers(self, resolver):
        """Checks the answered slots, caching results with specified resolver.

        Returns the list of addresses from the first slot with a positive answer.
        If all the slots have answered without a positive answer, raises an error.

        Arguments:
            resolver (Resolver): Resolver to run query with.

        Returns:
            list: IP addresss (eg ['10.1.2.3', '10.4.5.6']).

        Raises:
            DNSException: Cannot resolve hostname.
        """
        for slot in self.slots:
            if not slot.checked:
                response, answer = (slot.response, slot.answer)
                slot.checked = bool(response or slot.error)
                if response:
                    if slot.code in (NOERROR, NXDOMAIN):
                        if answer is not None:
                            resolver.cache.put((self.qname, slot.rdtype, IN), answer)
                        if answer:
                            return [x.address for x in answer]
                        slot.error = NoAnswer(response=response)
                    else:
                        slot.error = ErrorAnswer(response=response)
        if all(slot.checked for slot in self.slots):
            raise self.make_error()
        return []

    def make_error(self):
        """Makes an error that can be raised from the individual slot errors.

        Returns:
            DNSException: Error from slots, or generic 'timeout' error.
        """
        error = next((slot.error for slot in self.slots if slot.error), "timeout")
        if isinstance(error, DNSException):
            return error
        return DNSException(f"dns error resolving {self.hostname}: {error}")


class AnswerSlot:
    """Holds the answer for an individual query-runner slot."""

    def __init__(self, server, rdtype):
        """Initializes this slot.

        Arguments:
            server (str): DNS server to query (eg '9.9.9.9').
            rdtype (RdataType): Record type to query (eg AAAA).
        """
        self.server = server
        self.rdtype = rdtype
        self.checked = False
        self.code = None
        self.response = None
        self.answer = None
        self.error = None


def query_doh(query, url, timeout, session):
    """Queries the specified DoH URL with the specified DNS query.

    Arguments:
        query: DNS query object.
        url (str): Base DoH URL (eg 'https://example.org/dns-query').
        timeout (float): Request timeout in seconds (eg 0.5).
        session: Requests session object.

    Returns:
        DNS response object.

    Raises:
        BadResponse: Bad response from DoH URL.

    Propagates:
        RequestException: Error connecting to DoH URL.
    """
    http = _send_doh_query(query, url, timeout, session)
    response = message_from_wire(http.content)
    if not query.is_response(response):
        raise BadResponse
    return response


def _send_doh_query(query, url, timeout, session):
    """Sends the specified DNS query to the specified DoH URL.

    Arguments:
        query: DNS query object.
        url (str): Base DoH URL (eg 'https://example.org/dns-query').
        timeout (float): Request timeout in seconds (eg 0.5).
        session: Requests session object.

    Returns:
        Requests response object.

    Propagates:
        RequestException: Error connecting to DoH URL.
    """
    params = {"dns": urlsafe_b64encode(query.to_wire()).decode("utf-8").rstrip("=")}
    headers = {"accept": "application/dns-message"}
    request = Request("GET", url, params=params, headers=headers)
    request = request.prepare()
    response = session.send(request, timeout=timeout)
    response.raise_for_status()
    return response


def coerce_socket_mark(mark):
    """Converts the socket mark to an int.

    Arguments:
        mark: Mark value (eg '' or 'off' or 123 or '0x7b').

    Returns:
        int: Mark value (eg 0 or 123).
    """
    if not mark or mark == "off":
        return 0
    if isinstance(mark, int):
        return mark
    return int(str(mark), 0)


def resolve_endpoint_hostname(cnf, endpoint):
    """Resolves the specified endpoint to an IP address.

    Arguments:
        cnf (Cnf): Config object.
        endpoint (str): Endpoint with a hostname (eg 'vpn.example.com:51820').

    Returns:
        tuple: Resolved endpoint, hostname, port
        (eg ('[fd01::1]:51820', 'vpn.example.com', 51820)).
    """
    hostname, port, family = split_endpoint_address(endpoint)
    if not hostname or family:
        return endpoint, "", 0

    ip = lookup_ip(cnf, hostname, raises=False)
    if ip:
        endpoint = format_endpoint_address(ip, port)
    return endpoint, hostname, port


def apply_endpoint_hostnames(cnf, interfaces):
    """Updates the endpoints of the specified peers if configured with a hostname.

    Arguments:
        cnf (Cnf): Config object.
        interfaces (dict): Interfaces data.
    """
    if cnf.resolve_hostnames == "once":
        return

    for name, interface in interfaces.items():
        for pubkey, peer in interface.get("peers", {}).items():
            hostname = peer.get("hostname")
            endpoint = peer.get("endpoint")
            apply_endpoint_hostname(cnf, name, pubkey, hostname, endpoint)


def apply_endpoint_hostname(cnf, name, pubkey, hostname, endpoint):
    """Updates the specified peer's endpoint using the specified hostname.

    Arguments:
        cnf (Cnf): Config object.
        name (str): Interface name (eg 'wg0').
        pubkey (str): Peer public key.
        hostname (str): Hostname to use (eg 'foo.example.com').
        endpoint (str): Existing endpoint (eg '10.10.10.10:51820').
    """
    if not name or not pubkey or not hostname or not endpoint:
        return

    ip, port, family = split_endpoint_address(endpoint)
    ips = lookup_ips(cnf, hostname, family, raises=False)
    if ips and ip not in ips:
        set_endpoint_address(cnf, name, pubkey, ips[0], port)


def set_endpoint_address(cnf, name, pubkey, address, port):
    """Runs the `wg set` command to set the endpoint of the specified peer.

    Arguments:
        cnf (Cnf): Config object.
        name (str): Interface name (eg 'wg0').
        pubkey (str): Peer public key.
        address (str): Endpoint IP address (eg '10.10.10.10').
        port (int): Endpoint port (eg 51820).
    """
    endpoint = format_endpoint_address(address, port)
    run_wg_set(cnf, [name, "peer", pubkey, "endpoint", endpoint])


def format_endpoint_address(address, port):
    """Formats the specified endpoint IP address and port.

    Arguments:
        address (str): Endpoint IP address (eg 'fd01::1').
        port (int): Endpoint port (eg 51820).

    Returns:
        str: Formatted endpoint address (eg '[fd01::1]:51820').
    """
    port = port or 51820
    return f"[{address}]:{port}" if address.find(":") >= 0 else f"{address}:{port}"


def split_endpoint_address(endpoint):
    """Splits the specified endpoint into IP address, port, and address family.

    Arguments:
        endpoint (str): IP address and port (eg '[fc00:0:0:1::]:51820').

    Returns:
        tuple: String IP address, integer port number, integer family.
    """
    if not endpoint:
        return "", 0, 0

    ipv6 = fullmatch(r"\[([^\]]+)\](?::(\d+))?", endpoint)
    if ipv6:
        return ipv6[1], int(ipv6[2] or 0), AF_INET6

    family = 0 if search("[A-Za-z]", endpoint) else AF_INET
    ipv4 = endpoint.split(":")
    if len(ipv4) == 2:
        with suppress(ValueError):
            return ipv4[0], int(ipv4[1]), family

    return ipv4[0], 0, family


def split_endpoint_hostname_and_port(endpoint):
    """Splits the specified endpoint into hostname and port.

    If the endpoint has an IP address instead of a hostname, returns ('', 0).

    Arguments:
        endpoint (str): Hostname and port (eg 'vpn.example.com:51820').

    Returns:
        Tuple of string hostname and integer port number.
    """
    address, port, family = split_endpoint_address(endpoint)
    if family:
        return "", 0
    return address, port
