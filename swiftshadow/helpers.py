from datetime import datetime
from typing import Literal

from requests import get

from swiftshadow.models import Proxy
from swiftshadow.validator import validate_proxies


def checkProxy(proxy):
    proxyDict = {proxy[1]: proxy[0]}
    try:
        resp = get(
            f"{proxy[1]}://checkip.amazonaws.com", proxies=proxyDict, timeout=2
        ).text
        if resp.count(".") == 3:
            return True
        return False
    except Exception:
        return False


def log(level, message):
    level = level.upper()
    print(
        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - [swiftshadow] - {level} : {message}"
    )


def plaintextToProxies(text: str, protocol: Literal["http", "https"]) -> list[Proxy]:
    proxies: list[Proxy] = []
    for line in text.splitlines():
        try:
            ip, port = line.split(":")
        except ValueError:
            continue
        proxy = Proxy(ip=ip, port=int(port), protocol=protocol)
        proxies.append(proxy)
    return proxies


async def GenericPlainTextProxyProvider(
    url: str, protocol: Literal["http", "https"] = "http"
) -> list[Proxy]:
    raw: str = get(url).text
    proxies: list[Proxy] = plaintextToProxies(raw, protocol=protocol)
    results = await validate_proxies(proxies)
    return results


def deduplicateProxies(proxies: list[Proxy]) -> list[Proxy]:
    return list({p.as_string(): p for p in proxies}.values())
