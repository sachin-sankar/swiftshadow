from asyncio import create_task, gather
from collections.abc import Callable, Coroutine
from typing import Any, Literal

import aiohttp
from lxml import etree
from requests import get

from swiftshadow.helpers import GenericPlainTextProxyProvider
from swiftshadow.models import Provider, Proxy
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
    results = await GenericPlainTextProxyProvider(
        url="https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        protocol="http",
    )
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


async def GoodProxy(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
):
    baseUrl = "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/refs/heads/main/GoodProxy.txt"
    proxies: list[Proxy] = []
    raw = get(baseUrl).text

    for line in raw.splitlines():
        if line == "":
            continue
        line = line.split("|")[0].split(":")
        proxy = Proxy(ip=line[0], port=int(line[1]), protocol="http")
        proxies.append(proxy)
    results = await validate_proxies(proxies)
    return results


async def OpenProxyList(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
):
    results = await GenericPlainTextProxyProvider(
        "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/HTTPS_RAW.txt",
        "http",
    )
    return results


async def MuRongPIG(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
):
    results = await GenericPlainTextProxyProvider(
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/refs/heads/main/http_checked.txt",
        "http",
    )
    return results


async def Mmpx12(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
):
    url = f"https://github.com/mmpx12/proxy-list/raw/refs/heads/master/{protocol}.txt"
    results = await GenericPlainTextProxyProvider(url, protocol)
    return results


async def Anonym0usWork1221(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
):
    url = f"https://github.com/Anonym0usWork1221/Free-Proxies/raw/refs/heads/main/proxy_files/{protocol}_proxies.txt"
    results = await GenericPlainTextProxyProvider(url, protocol)
    return results


async def ProxyDB(
    countries: list[str] = [], protocol: Literal["http", "https"] = "http"
):
    base_url = f"https://www.proxydb.net/?protocol={protocol}&sort_column_id=uptime&sort_order_desc=true"
    proxies: list[Proxy] = []
    raw = get(base_url).text
    total = int(
        raw.split("Showing")[-1].split("total proxies")[0].split("of")[-1].strip()
    )

    async def parsePage(session: aiohttp.ClientSession, url: str):
        proxies = []
        async with session.get(url) as resp:
            raw = await resp.text()
            exml = etree.HTML(raw)
            table = exml.find("body/div/div/table/tbody")
            rows = iter(table)
            for row in rows:
                if len(proxies) > 500:
                    break
                data = []
                for td in row[:4]:
                    text = td.text.strip()
                    if text == "":
                        text = list(td)[-1].text
                        data.append(text)
                if countries != [] and data[-1] not in countries:
                    continue
                proxy = Proxy(data[0], protocol, data[1])
                proxies.append(proxy)
        return proxies

    tasks = []
    async with aiohttp.ClientSession() as session:
        for offset in range(0, total, 30):
            url = base_url + f"&offset={offset}"
            task = create_task(coro=parsePage(session, url))
            tasks.append(task)
        results = await gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, BaseException):
            continue
        proxies.extend(result)
    return proxies


Providers: dict[
    Callable[[list[str], Literal["http", "https"]], Coroutine[Any, Any, list[Proxy]]],
    Provider,
] = {
    ProxyScrape: Provider(
        providerFunction=ProxyScrape, countryFilter=True, protocols=["http"]
    ),
    Monosans: Provider(
        providerFunction=Monosans, countryFilter=True, protocols=["http"]
    ),
    MuRongPIG: Provider(
        providerFunction=MuRongPIG, countryFilter=False, protocols=["http"]
    ),
    Thespeedx: Provider(
        providerFunction=Thespeedx, countryFilter=False, protocols=["http"]
    ),
    Anonym0usWork1221: Provider(
        providerFunction=Anonym0usWork1221,
        countryFilter=False,
        protocols=["http", "https"],
    ),
    Mmpx12: Provider(
        providerFunction=Mmpx12, countryFilter=False, protocols=["http", "https"]
    ),
    GoodProxy: Provider(
        providerFunction=GoodProxy, countryFilter=False, protocols=["http"]
    ),
    OpenProxyList: Provider(
        providerFunction=OpenProxyList, countryFilter=False, protocols=["http"]
    ),
    ProxyDB: Provider(
        providerFunction=ProxyDB, countryFilter=True, protocols=["http", "https"]
    ),
}
