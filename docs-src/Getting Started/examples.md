# Examples

This page provides practical examples to help you get started with `swiftshadow`. It covers all major features, including filtering, caching, rotation, and integration with popular libraries.

---

## Basic Usage

### Fetching a Proxy
To fetch a random proxy:
```python
from swiftshadow import QuickProxy

proxy = QuickProxy()
print(proxy.as_string())  # Output: http://<ip>:<port>
```

---

## Filtering Proxies

### Country Filter
Filter proxies by country using two-letter ISO codes:
```python
from swiftshadow.classes import ProxyInterface

# Fetch proxies from the US and India
swift = ProxyInterface(countries=["US", "IN"])
print(swift.get().as_string())
```

### Protocol Filter
Filter proxies by protocol (`http` or `https`):
```python
from swiftshadow.classes import ProxyInterface

# Fetch HTTPS proxies
swift = ProxyInterface(protocol="https")
print(swift.get().as_string())
```

---

## Proxy Rotation

### Manual Rotation
Manually rotate proxies using the `rotate()` method:
```python
from swiftshadow.classes import ProxyInterface

swift = ProxyInterface()

# Get the first proxy
print(swift.get().as_string())

# Rotate to a new proxy
swift.rotate()
print(swift.get().as_string())
```

### Automatic Rotation
Enable automatic rotation by setting `autoRotate=True`:
```python
from swiftshadow.classes import ProxyInterface

swift = ProxyInterface(autoRotate=True)

# Each call to get() will return a new proxy
print(swift.get().as_string())
print(swift.get().as_string())
```

---

## Caching

### Custom Cache Folder
Specify a custom cache folder (useful for AWS Lambda):
```python
from swiftshadow.classes import ProxyInterface

# Use the /tmp directory for caching
swift = ProxyInterface(cacheFolderPath="/tmp")
print(swift.get().as_string())
```

### Disabling Caching
For one-off use cases, use [`QuickProxy`](quickProxy.md):
```python
from swiftshadow import QuickProxy

proxy = QuickProxy()
print(proxy.as_string())
```

---

## Integration with Libraries

### Using with `requests`
Route requests through a proxy using the `requests` library:
```python
from swiftshadow import QuickProxy
from requests import get

proxy = QuickProxy()
resp = get('https://checkip.amazonaws.com', proxies=proxy.as_requests_dict())
print(resp.text)  # Output: Proxy's IP address
```

### Using with `httpx`
Route requests through a proxy using the `httpx` library:
```python
from swiftshadow import QuickProxy
import httpx

proxy = QuickProxy()
with httpx.Client(proxies={"http://": proxy.as_string(), "https://": proxy.as_string()}) as client:
    resp = client.get('https://checkip.amazonaws.com')
    print(resp.text)  # Output: Proxy's IP address
```

---

## Advanced Usage

### Combining Filters
Combine country and protocol filters for precise proxy selection:
```python
from swiftshadow.classes import ProxyInterface

# Fetch HTTPS proxies from the US and India
swift = ProxyInterface(countries=["US", "IN"], protocol="https")
print(swift.get().as_string())
```

### Force Cache Update
Force an update of the proxy cache:
```python
from swiftshadow.classes import ProxyInterface

swift = ProxyInterface()
swift.update()  # Force update the proxy list
print(swift.get().as_string())
```

---

For more details on classes and methods, visit the [References](proxyInterface.md) page.
