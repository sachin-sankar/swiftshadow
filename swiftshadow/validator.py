import asyncio

import aiohttp

from swiftshadow.models import Proxy


async def check_proxy(async_session: aiohttp.ClientSession, proxy: Proxy) -> str:
    """
    Check one proxy abject.

    Args:
        async_session: aiohttp client session object
        proxy: Proxy Object

    Returns:
        text: API response text
    """
    async with async_session.get(
        url=f"{proxy.protocol}://checkip.amazonaws.com",
        proxy=proxy.as_string(),
        timeout=4,
    ) as response:
        text = await response.text()
        return text


async def validate_proxies(proxies: list[Proxy]) -> list[Proxy]:
    """
    Validate all proxies asynchronously.

    Args:
        proxies: List of Proxy objects

    Returns:
        working_proxies: List of working Proxies
    """
    working_proxies: list[Proxy] = []
    async with aiohttp.ClientSession() as async_session:
        tasks = []
        for proxy in proxies:
            task = asyncio.create_task(coro=check_proxy(async_session, proxy))
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for proxy, result in zip(proxies, results):
            if type(result) is not str:
                continue
            if result.count(".") == 3:
                working_proxies.append(proxy)
    return working_proxies
