# AWS Lambda

Using `swiftshadow` with AWS Lambda normally raises an error because the cache mechanism won't work properly due to the read-only file permissions in the Lambda environment. To fix this, you can pass the `cacheFolderPath` parameter and set it to `"/tmp"` when creating a [`ProxyInterface`](proxyInterface.md) instance.

```python
from swiftshadow.classes import ProxyInterface

swift = ProxyInterface(cacheFolderPath="/tmp")
```

The `/tmp` directory in AWS Lambda is writable, allowing the cache to function correctly.

---

## Disabling Caching

If you don’t want the caching behavior at all, consider using the [`QuickProxy`](quickProxy.md) function instead. It does not cache proxies, making it ideal for serverless environments like AWS Lambda.

```python
from swiftshadow import QuickProxy

proxy = QuickProxy()
print(proxy.as_string())
```

---

For more details on the [`ProxyInterface`](proxyInterface.md) class or the [`QuickProxy`](quickProxy.md) function, visit the [References](proxyInterface.md) page.
