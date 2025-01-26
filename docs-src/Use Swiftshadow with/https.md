# HTTPX Library

`swiftshadow` works seamlessly with the modern and asynchronous [`httpx`](https://www.python-httpx.org/) library, making it easy to route your HTTP/HTTPS requests through a proxy. Whether you're building synchronous or asynchronous applications, `swiftshadow` has you covered.

## Example Usage

Here’s how you can use a proxy fetched by [`QuickProxy`](quickProxy.md) with the `httpx` library:

### Synchronous Example
```python
from swiftshadow import QuickProxy
import httpx

# Fetch a proxy
proxy = QuickProxy()

# Use the proxy with httpx
with httpx.Client(proxies={"http://": proxy.as_string(), "https://": proxy.as_string()}) as client:
    resp = client.get('https://checkip.amazonaws.com')
    print(resp.text)
```

### Asynchronous Example
```python
from swiftshadow import QuickProxy
import httpx
import asyncio

async def fetch_with_proxy():
    # Fetch a proxy
    proxy = QuickProxy()

    # Use the proxy with httpx
    async with httpx.AsyncClient(proxies={"http://": proxy.as_string(), "https://": proxy.as_string()}) as client:
        resp = await client.get('https://checkip.amazonaws.com')
        print(resp.text)

# Run the async function
asyncio.run(fetch_with_proxy())
```

### Explanation
- [`QuickProxy`](quickProxy.md) fetches a proxy object.
- The `as_string()` method converts the proxy into a format compatible with `httpx`.
- For synchronous requests, use `httpx.Client`.
- For asynchronous requests, use `httpx.AsyncClient`.
- The `proxies` parameter is used to route requests through the proxy.

!!! note
    If the proxy is working correctly, the output should be an `IPv4` address that is not your own.

---

For more advanced use cases, such as caching and automatic rotation, consider using the [`ProxyInterface`](proxyInterface.md) class. For additional details, visit the [References](proxyInterface.md) page.
