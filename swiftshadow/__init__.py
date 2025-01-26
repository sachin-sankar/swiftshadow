from typing import Literal
from swiftshadow.providers import Providers
from swiftshadow.models import Proxy
from asyncio import run


def QuickProxy(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
) -> Proxy | None:
    """
    This function is a faster alternative to `Proxy` class.
    No caching is done.

    Args:
        countries: ISO 3166-2 Two letter country codes to filter proxies.
        protocol: HTTP/HTTPS protocol to filter proxies.

    Returns:
        proxyObject (dict): A working proxy object if found or else None.
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
