from typing import Literal

from requests import get

from swiftshadow.models import Proxy, Provider
from swiftshadow.types import MonosansProxyDict
from swiftshadow.validator import validate_proxies


async def Monosans(
    countries: list[str] = [],
    protocol: Literal["http", "https"] = "http",
) -> list[Proxy]:
    response = get(
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies.json"
    )
    proxy_dicts: list[MonosansProxyDict] = response.json()
    proxies_to_validate: list[Proxy] = []
    for proxy_dict in proxy_dicts:
        if proxy_dict["protocol"] != protocol:
            continue
        if (
            len(countries) != 0
            and proxy_dict["geolocation"]["country"]["iso_code"] not in countries
        ):
            continue
        proxy = Proxy(
            ip=proxy_dict["host"],
            port=proxy_dict["port"],
            protocol=proxy_dict["protocol"],
        )
        proxies_to_validate.append(proxy)
    result = await validate_proxies(proxies_to_validate)
    return result


async def Thespeedx(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
):
    raw: str = get(
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    ).text
    proxies: list[Proxy] = []
    for line in raw.splitlines():
        line = line.split(":")
        proxy = Proxy(ip=line[0], protocol="http", port=int(line[-1]))
        proxies.append(proxy)
    results = await validate_proxies(proxies)
    return results


async def ProxyScrape(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
):
    baseUrl = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=ipport&format=json"
    proxies: list[Proxy] = []
    if len(countries) == 0:
        apiUrl = baseUrl + "&country=all"
    else:
        apiUrl = baseUrl + "&country=" + ",".join([i.upper() for i in countries])
    raw = get(apiUrl).json()
    for ipRaw in raw["proxies"]:
        proxy = Proxy(protocol="http", ip=ipRaw["ip"], port=ipRaw["port"])
        proxies.append(proxy)
    results = await validate_proxies(proxies)
    return results


Providers: list[Provider] = [
    Provider(providerFunction=Monosans, countryFilter=True, protocols=["http"]),
    Provider(providerFunction=Thespeedx, countryFilter=False, protocols=["http"]),
    Provider(providerFunction=ProxyScrape, countryFilter=True, protocols=["http"]),
]
