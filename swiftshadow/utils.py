from asyncio import as_completed, gather

from aiohttp import ClientResponse, ClientSession, ClientTimeout

from swiftshadow.models import Proxy


async def validate_for_target(
    session: ClientSession,
    url: str,
    proxy: Proxy,
    headers: dict[str, str] = {},
    timeout: int = 2,
) -> tuple[Proxy, ClientResponse]:
    """Validates a single proxy by attempting to connect to a target URL.

    Performs an HTTP GET request to the specified URL through the provided proxy
    and returns both the proxy object and the response for further evaluation.
    This is a low-level helper function used by higher-level filtering operations.

    Args:
        session: An active aiohttp ClientSession to use for the HTTP request.
            Reusing sessions improves performance when validating multiple proxies.
        url: The target URL to test proxy connectivity against. Must be a
            fully qualified URL including protocol (e.g., 'https://api.example.com').
        proxy: The Proxy object to validate against the target URL.
        headers: HTTP headers to include in the request. Useful for endpoints
            requiring authentication, User-Agent, or custom headers. Defaults to {}.
        timeout: Maximum time in seconds to wait for a response before considering
            the proxy as failed. Defaults to 2 seconds.

    Returns:
        A tuple containing the tested Proxy object and the ClientResponse received.
        The response can be used to check status codes, headers, or body content
        for validation.

    Raises:
        asyncio.TimeoutError: If the request exceeds the specified timeout.
        aiohttp.ClientError: For various HTTP client errors including connection
            failures, DNS resolution errors, or invalid proxy configurations.

    Example:
        ```py
        async with ClientSession() as session:
            proxy = Proxy('127.0.0.1:8080')
            proxy_obj, response = await validate_for_target(
                session,
                'https://httpbin.org/ip',
                proxy,
                headers={'User-Agent': 'ProxyValidator/1.0'},
                timeout=5
            )
            print(f"Status: {response.status}")
        ```
    """
    result = await session.get(
        url, headers=headers, proxy=proxy.as_string(), timeout=ClientTimeout(timeout)
    )
    return proxy, result


async def filter_on_target(
    url: str,
    proxies: list[Proxy],
    headers: dict[str, str] = {},
    timeout: int = 2,
) -> list[Proxy]:
    """Filters a list of proxies, returning only those that successfully connect to a target URL.

    Tests all provided proxies concurrently against the specified URL and returns
    a filtered list containing only proxies that respond with HTTP 200 status.
    This is useful for bulk proxy validation and filtering out dead or blocked proxies.

    Args:
        url: The target URL to test proxy connectivity against. Should be a
            reliable endpoint that returns 200 OK for valid requests
            (e.g., 'https://httpbin.org/ip' or 'https://api.ipify.org').
        proxies: A list of Proxy objects to be tested and filtered.
            All proxies are tested concurrently for maximum efficiency.
        headers: HTTP headers to include in validation requests. Useful for endpoints
            requiring specific headers like User-Agent, Authorization, or Accept
            headers. Defaults to {}.
        timeout: Maximum time in seconds to wait for each proxy response. Proxies
            exceeding this timeout are excluded from results. Defaults to 2 seconds.

    Returns:
        A filtered list containing only Proxy objects that successfully connected
        to the target URL and received HTTP 200 status. Proxies that fail, timeout,
        or return non-200 status codes are excluded. The relative order of working
        proxies is preserved from the input list.

    Example:
        ```py
        proxies = [
            Proxy('127.0.0.1:8080'),
            Proxy('192.168.1.1:3128'),
            Proxy('10.0.0.1:8888')
        ]
        working = await filter_on_target(
            'https://httpbin.org/get',
            proxies,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=5
        )
        print(f"{len(working)} out of {len(proxies)} proxies are working")
        # Output: 2 out of 3 proxies are working
        ```
    """
    working: list[Proxy] = []
    async with ClientSession() as session:
        results: list[tuple[Proxy, ClientResponse] | BaseException] = await gather(
            *(
                validate_for_target(
                    session, url, headers=headers, proxy=p, timeout=timeout
                )
                for p in proxies
            ),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, BaseException):
                continue
            else:
                if result[1].status == 200:
                    working.append(result[0])
    return working


async def get_for_target(
    url: str, proxies: list[Proxy], headers: dict[str, str] = {}, timeout: int = 2
) -> Proxy | None:
    """Returns the first working proxy from a list that successfully connects to a target URL.

    Tests proxies concurrently and returns immediately upon finding the first proxy
    that responds with HTTP 200 status. This is optimized for scenarios where you
    need any working proxy quickly, rather than validating the entire list.

    Args:
        url: The target URL to test proxy connectivity against. Should be a
            reliable endpoint that returns 200 OK for valid requests.
        proxies: A list of Proxy objects to test. Testing begins concurrently for
            all proxies, but returns as soon as the first working proxy is found.
        headers: HTTP headers to include in validation requests. Useful for endpoints
            requiring authentication or specific headers. Defaults to {}.
        timeout: Maximum time in seconds to wait for each proxy response.
            Defaults to 2 seconds.

    Returns:
        The first Proxy object that successfully responds with HTTP 200, or None
        if all proxies fail, timeout, or return non-200 status codes. The "first"
        proxy is determined by which completes successfully first, not by input
        list order.

    Example:
        ```py
        proxies = [
            Proxy('slow-proxy.com:8080'),
            Proxy('fast-proxy.com:3128'),
            Proxy('dead-proxy.com:8888')
        ]
        proxy = await get_for_target(
            'https://httpbin.org/ip',
            proxies,
            headers={'User-Agent': 'ProxyFinder/1.0'},
            timeout=3
        )
        if proxy:
            print(f"Found working proxy: {proxy.as_string()}")
        else:
            print("No working proxies found")
        # Output: Found working proxy: http://fast-proxy.com:3128
        ```
    """
    async with ClientSession() as session:
        for task in as_completed(
            validate_for_target(session, url, headers=headers, proxy=p, timeout=timeout)
            for p in proxies
        ):
            result: tuple[Proxy, ClientResponse] = await task
            if isinstance(result, BaseException):
                continue
            else:
                if result[1].status == 200:
                    return result[0]
    return None
