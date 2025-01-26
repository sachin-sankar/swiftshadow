# Basic Usage

To get a random `HTTP` proxy from any country:
```python
from swiftshadow.classes import ProxyInterface
swift = ProxyInterface()

print(swift.get().as_string())
```

!!! note
    When the `ProxyInterface` class instance is created for the first time, the `update()` method is called. This method fetches proxies from providers and caches them. This process may take around 10 seconds. The cache will refresh after the `cachePeriod` expires.

The `get()` method returns a `Proxy` object. You can convert it to a string using `as_string()` or to a dictionary using `as_requests_dict()`. See the [References](proxyInterface.md) for more details.

This is the most basic usage of `swiftshadow`, but there’s more to explore.

!!! note
    From now on, all examples will exclude the import statement for simplicity.

---

# Filtering Proxies

You can filter proxies based on their country of origin or protocol (HTTP/HTTPS).

## Country Filter
To filter proxies by country, pass a list of **two-letter country codes** when initializing the `ProxyInterface` class.

- For a list of countries and their two-letter codes, visit [this Wikipedia page](https://en.m.wikipedia.org/wiki/ISO_3166-2).

```python title="Country Filtered"
swift = ProxyInterface(countries=['US', 'IN'])
```

## Protocol Filter
By default, all proxies are `HTTP`. For **SSL-enabled** `HTTPS` proxies, set the `protocol` parameter to `"https"`.

```python title="HTTPS Filter"
swift = ProxyInterface(protocol='https')
```

!!! warning
    `swiftshadow` does not validate country codes or protocols. If you provide invalid country codes or protocols, no proxies will be available.

---

# Proxy Rotation

## Manual Rotation
You can manually rotate proxies using the `rotate()` method. This selects a random proxy from the available list.

```python
from swiftshadow.classes import ProxyInterface
swift = ProxyInterface()

print(swift.get().as_string())
swift.rotate()
print(swift.get().as_string())
```

## Auto Rotation
To enable automatic proxy rotation, set the `autoRotate` parameter to `True` when initializing the `ProxyInterface` object. When enabled, the proxy will rotate every time the `get()` method is called.

```python
from swiftshadow.classes import ProxyInterface
swift = ProxyInterface(autoRotate=True)

print(swift.get().as_string())
print(swift.get().as_string())
```

---

# Caching

Proxies are cached to improve performance. The cache expires after the `cachePeriod` (default: 10 minutes). You can force a cache update by calling the `update()` method.

```python
swift = ProxyInterface()
swift.update()  # Force update the proxy list
```

---

Visit [References](proxyInterface.md) for more information on methods and classes.
