"""Windows configuration utilities."""

from contextlib import contextmanager
from io import BytesIO, StringIO
from logging import DEBUG, getLogger
from pathlib import Path

# pywin32 only needs to be installed on windows
try:
    from win32crypt import CryptProtectData, CryptUnprotectData
    from win32security import (
        DACL_SECURITY_INFORMATION,
        GetFileSecurity,
        LookupAccountSid,
        SetFileSecurity,
    )
except ImportError:
    CryptProtectData = None
    CryptUnprotectData = None
    DACL_SECURITY_INFORMATION = None
    GetFileSecurity = None
    LookupAccountSid = None
    SetFileSecurity = None


FILE_WRITE_DATA = 1 << 1
GENERIC_ALL = 1 << 28


@contextmanager
def open_dpapi(path, method="r"):
    """Opens and decrypts or encrypts the specified file.

    Arguments:
        path (str): Path to file.
        method (str): "r" or "w" to read or write file (default "r").

    Yields:
        Stream object to read or write.
    """
    method = "wb" if method == "w" else "rb"
    description = _calculate_dpapi_file_description(path)
    if "WireSock" in str(path):
        description = ""
    buffer = StringIO()

    with open(path, method) as file:
        try:
            if method == "rb":
                decrypt(file, buffer, description)
                buffer.seek(0)
            yield buffer

        finally:
            if method == "wb":
                buffer.seek(0)
                encrypt(buffer, file, description)
            file.close()


def _calculate_dpapi_file_description(path):
    """Calculates the description value for the specified .dpapi file.

    Arguments:
        path (str): Path to file.

    Returns:
        str: Description value
    """
    path = Path(path)
    if path.suffix == ".dpapi":
        return _calculate_dpapi_file_description(path.stem)
    return path.stem


def decrypt(cipher_stream, plain_stream=None, description=""):
    """Decrypts the first stream to the second.

    Arguments:
        cipher_stream: Input stream with encrypted bytes.
        plain_stream: Output stream for decrypted text.
        description (str): Expected description included in encrypted bytes.

    Returns:
        Output stream.

    Raises:
        ValueError: Expected description does not match actual description.
    """
    if not plain_stream:
        plain_stream = StringIO()

    cipher_bytes = cipher_stream.read()
    actual_description, plain_bytes = CryptUnprotectData(cipher_bytes)
    if description and description != actual_description:
        msg = f"expected description '{description}'; actual '{actual_description}'"
        raise ValueError(msg)
    plain_stream.write(plain_bytes.decode("utf-8"))

    return plain_stream


def encrypt(plain_stream, cipher_stream=None, description=""):
    """Encrypts the first stream to the second.

    Arguments:
        plain_stream: Input stream with decrypted text.
        cipher_stream: Output stream for encrypted bytes.
        description (str): Description to include in encrypted bytes.

    Returns:
        Output stream.
    """
    if not cipher_stream:
        cipher_stream = BytesIO()

    plain_text = plain_stream.read()
    cipher_bytes = CryptProtectData(plain_text.encode("utf-8"), description)
    cipher_stream.write(cipher_bytes)

    return cipher_stream


def restrict_access_to_cnf_dir(cnf):
    """Restricts permissions of the specified config file directory.

    Arguments:
        cnf: Config object.
    """
    cnf_file = Path(cnf.cnf_file)
    if not cnf_file.is_file():
        getLogger(__name__).error("cnf file not found: %s", cnf_file)
        return

    cnf_dir = cnf_file.parent
    restrict_access_to_file(cnf_dir)
    for file in sorted(cnf_dir.iterdir()):
        restrict_access_to_file(file)


def restrict_access_to_file(file):
    """Restricts permissions of the specified file.

    Arguments:
        file (str): Path to file.
    """
    file = str(file)
    getLogger(__name__).debug("restricting access to %s", file)

    descriptor = GetFileSecurity(file, DACL_SECURITY_INFORMATION)
    dacl = descriptor.GetSecurityDescriptorDacl()

    keep = set()
    for i in range(dacl.GetAceCount()):
        (ace_type, flags), mask, sid = dacl.GetAce(i)
        if ace_type == 0 and ((mask & FILE_WRITE_DATA) or (mask & GENERIC_ALL)):
            _debug_keep_ace(sid, mask)
            keep.add(str(sid))

    for i in reversed(range(dacl.GetAceCount())):
        (ace_type, flags), mask, sid = dacl.GetAce(i)
        if ace_type == 0 and str(sid) not in keep:
            _debug_remove_ace(sid, mask)
            dacl.DeleteAce(i)

    descriptor.SetSecurityDescriptorDacl(1, dacl, 0)
    SetFileSecurity(file, DACL_SECURITY_INFORMATION, descriptor)


def _debug_keep_ace(sid, mask):
    """Logs info about ACE being kept.

    Arguments:
        sid: SID object.
        mask: Rights.
    """
    logger = getLogger(__name__)
    if logger.isEnabledFor(DEBUG):
        formatted_sid = _format_ace_sid(sid)
        formatted_mask = _format_ace_mask(mask)
        logger.debug("keep access for %s (%s)", formatted_sid, formatted_mask)


def _debug_remove_ace(sid, mask):
    """Logs info about ACE being removed.

    Arguments:
        sid: SID object.
        mask: Rights.
    """
    logger = getLogger(__name__)
    if logger.isEnabledFor(DEBUG):
        formatted_sid = _format_ace_sid(sid)
        formatted_mask = _format_ace_mask(mask)
        logger.debug("remove access for %s (%s)", formatted_sid, formatted_mask)


def _format_ace_sid(sid):
    r"""Formats the specified SID.

    Arguments:
        sid: SID object.

    Returns:
        str: Formatted SID (eg 'BUILTIN\Users').
    """
    name, domain, account_type = LookupAccountSid("", sid)
    return f"{domain}\\{name}" if domain else name


def _format_ace_mask(mask):
    """Formats the specified bit mask.

    Arguments:
        mask (int): Bit mask.

    Returns:
        str: Formatted bit mask (eg '0x1a').
    """
    if mask < 0:
        mask = 0x100000000 + mask
    return f"0x{mask:x}"
