from logging import getLogger
from typing import Literal

from requests import get

from swiftshadow.models import Proxy
from swiftshadow.validator import validate_proxies


logger = getLogger("swiftshadow")


def log(level, message):
    logger.log(getattr(logger, level.upper(), 20), message)


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
