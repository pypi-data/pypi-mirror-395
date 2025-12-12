from socket import timeout
import functools
import logging
from fedkit.validators import validate_url

logger = logging.getLogger(__name__)


def Fetch(url: str) -> dict:
    """
    Fetch a remote object, wrapped in a cache
    """
    logger.error(f"Fetching {url}")
    import django.core.exceptions
    from django.conf import settings
    from django.core.cache import cache

    if not settings.CACHES.get("default"):
        raise django.core.exceptions.ImproperlyConfigured(
            "ActivityPub Fetch requires configured cache."
        )

    if not validate_url(url):
        raise ValueError("Host/URL validation failed.")

    return cache.get_or_set(url, BaseFetch(url, safe=True), 3600)


@functools.lru_cache(maxsize=512)
def BaseFetch(url: str, safe: bool = False) -> dict:
    """
    Fetch a remote object
    """
    logger.error(f"Fetching {url}")

    if not validate_url(url):
        raise ValueError("Host/URL validation failed.") from e

    import requests

    headers = {
        "Content-type": "application/activity+json",
        "Accept": "application/activity+json",
    }

    return requests.get(url, headers=headers, timeout=60).json()
