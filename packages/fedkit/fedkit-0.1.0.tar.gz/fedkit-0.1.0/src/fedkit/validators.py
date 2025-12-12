"""
validators.py

This module contains custom validators for the application.

def validate_iri(url):
    This function validates the IRI of a URL.
"""
import logging
import urllib.parse
import functools
import socket

from django.core.exceptions import ValidationError
# from rfc3987 import parse

logger = logging.getLogger(__name__)


def validate_uri(x) -> []:
    try:
        result = urllib.parse.urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def validate_iri(uri: str) -> bool:
    """
    This function validates the IRI of a URL.
    # https://chromium.googlesource.com/external/googleappengine/python/+/3b4e135a03ddf2132df0c0c8d3f7cdc9eaa8c34b/httplib2/iri2uri.py
    """

    try:
        if isinstance(uri ,str):
            (scheme, authority, path, query, fragment) = urlparse.urlsplit(uri)
            authority = authority.encode('idna')
            # For each character in 'ucschar' or 'iprivate'
            #  1. encode as utf-8
            #  2. then %-encode each octet of that utf-8
            uri = urlparse.urlunsplit((scheme, authority, path, query, fragment))
            uri = "".join([encode(c) for c in uri])
        return uri
    except ValueError:
        raise ValidationError("Invalid IRI")


@functools.lru_cache(maxsize=512)
def validate_url(url: str) -> bool:
    """
    Implements basic SSRF protection.
    Check if a remote object is valid
    Check if the URL is blocked

    :param url: str: The URL to check
    :return: bool: True if the URL is valid
    :raises ValueError: If the URL is invalid
    """
    import urllib.parse

    from django.conf import settings

    parsed = urllib.parse.urlparse(url)

    if parsed.scheme not in ["https"]:
        """
        Don't support HTTP
        """
        raise ValueError(f"Unsupported scheme {parsed.scheme}")

    for blocked_hostname in settings.BLOCKED_SERVERS:
        if parsed.hostname == blocked_hostname or parsed.hostname.endswith(
            f".{blocked_hostname}"
        ):
            raise ValueError(f"Blocked hostname {parsed.hostname}")

    if not parsed.hostname or parsed.hostname.lower() in ["localhost"]:
        raise ValueError(f"Invalid hostname {parsed.hostname}")

    if parsed.hostname.endswith(".onion"):
        logger.warning(f"{url} is an onion service")
        raise ValueError(f"Unsupported onion service {parsed.hostname}")

    try:
        ip_address = socket.getaddrinfo(
            parsed.hostname,
            parsed.port or (80 if parsed.scheme == "http" else 443),
        )[0][4][0]
        logger.debug(f"{ip_address=}")
    except socket.gaierror:  # [Errno -2] Name or service not known
        logger.info(f"rejecting not found invalid URL {url}")
        raise ValueError(f"rejecting not found invalid URL {url}")

    try:
        ip = ipaddress.ip_address(ip_address)
    except socket.gaierror:  # [Errno -2] Name or service not known
        logger.info(f"rejecting invalid IP {ip_address}")
        raise ValueError(f"rejecting invalid IP {ip_address}")

    if ip.is_private:
        logger.info(f"rejecting private URL {url} -> {ip_address}")
        raise ValueError(f"rejecting private URL {url} -> {ip_address}")

    return True
