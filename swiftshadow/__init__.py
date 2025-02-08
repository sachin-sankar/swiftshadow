from asyncio import run
from typing import Literal

from swiftshadow.models import Proxy
from swiftshadow.providers import Providers


def QuickProxy(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
) -> Proxy | None:
    """
    This function is a faster alternative to `ProxyInterface` class.
    No caching is done.

    Args:
        countries: ISO 3166-2 Two letter country codes to filter proxies.
        protocol: HTTP/HTTPS protocol to filter proxies.

    Returns:
        proxyObject (Proxy): A working proxy object if found or else None.
    """
    for provider in Providers:
        if protocol not in provider.protocols:
            continue
        if (len(countries) != 0) and (not provider.countryFilter):
            continue
        try:
            return run(provider.providerFunction(countries, protocol))[0]
        except Exception:
            continue
    return None
