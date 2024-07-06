from swiftshadow.providers import Providers


def QuickProxy(countries: list = [], protocol: str = "http"):
    """
    This function is a faster alternative to `Proxy` class.
    No caching is done.

    Args:
     countries: ISO 3166-2 Two letter country codes to filter proxies.
     protocol: HTTP/HTTPS protocol to filter proxies.

    Returns:
                    proxyObject (dict): A working proxy object.
    """
    for providerDict in Providers:
        if protocol not in providerDict["protocols"]:
            continue
        if (len(countries) != 0) and (not providerDict["countryFilter"]):
            continue
        try:
            return providerDict["provider"](1, countries, protocol)[0]
        except:
            continue
    return None
