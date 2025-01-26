# QuickProxy

For faster use cases where caching is not required, the [`swiftshadow.QuickProxy`](quickProxy.md) function is the best choice. Unlike the [`ProxyInterface`](proxyInterface.md) class, `QuickProxy` does not cache proxies, making it lightweight and ideal for one-off or quick operations.

::: swiftshadow.QuickProxy

You can use filters just like in the [`ProxyInterface`](proxyInterface.md) class. This includes filtering by **country** and **protocol**.

## Parameters
- `countries` (list[str]): A list of two-letter country codes to filter proxies by country. Defaults to an empty list (no filtering).
- `protocol` (Literal["http", "https"]): The protocol to filter proxies by. Defaults to `"http"`.

## Returns
- [`Proxy`](proxy.md) | `None`: A `Proxy` object if a valid proxy is found, otherwise `None`.

## Example
```python
from swiftshadow import QuickProxy

# Get a random HTTP proxy
proxy = QuickProxy()
print(proxy.as_string())

# Get an HTTPS proxy from the US or India
proxy = QuickProxy(countries=["US", "IN"], protocol="https")
print(proxy.as_string())
```

!!! note
    Since `QuickProxy` does not cache proxies, it may take slightly longer to fetch a proxy compared to [`ProxyInterface`](proxyInterface.md) when used repeatedly. However, it is faster for single-use scenarios.

!!! warning
    If no proxies match the provided filters, `QuickProxy` will return `None`. Always check the return value before using it.

---

For more advanced use cases, such as caching and automatic rotation, consider using the [`ProxyInterface`](proxyInterface.md) class. 
