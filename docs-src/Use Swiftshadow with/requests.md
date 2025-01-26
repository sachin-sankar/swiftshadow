# Requests Library

`swiftshadow` integrates seamlessly with the popular [`requests`](https://docs.python-requests.org/) library, allowing you to easily route your HTTP/HTTPS requests through a proxy.

## Example Usage

Here’s how you can use a proxy fetched by [`QuickProxy`](quickProxy.md) with the `requests` library:

```python
from swiftshadow import QuickProxy
from requests import get

# Fetch a proxy
proxy = QuickProxy()

# Use the proxy with requests
resp = get('https://checkip.amazonaws.com', proxies=proxy.as_requests_dict())
print(resp.text)
```

### Explanation
- [`QuickProxy`](quickProxy.md) fetches a proxy object.
- The `as_requests_dict()` method converts the proxy into a format compatible with the `requests` library.
- The `proxies` parameter in `requests.get()` is used to route the request through the proxy.

!!! note
    If the proxy is working correctly, the output should be an `IPv4` address that is not your own.

---

For more advanced use cases, such as caching and automatic rotation, consider using the [`ProxyInterface`](proxyInterface.md) class. For additional details, visit the [References](proxyInterface.md) page.
