# Swiftshadow

![Swiftshadow Logo](assets/logo.png)

**Swiftshadow** is a Python package designed to manage and rotate free IP proxies. It provides a simple and efficient way to fetch, cache, and validate proxies from multiple sources. The package supports filtering by country and protocol, automatic proxy rotation, and caching to improve performance.

---

## Features

- **Proxy Fetching**: Fetch proxies from multiple providers.
- **Filtering**: Filter proxies by country and protocol (HTTP/HTTPS).
- **Caching**: Cache proxies to reduce frequent fetching.
- **Validation**: Validate proxies to ensure they are working.
- **Automatic Rotation**: Automatically rotate proxies for load balancing.
- **Logging**: Built-in logging for debugging and monitoring.

---

## Quick Start

### Installation

Install `swiftshadow` using pip:

```bash
pip install swiftshadow
```

### Basic Usage

Here’s a quick example to get started:

```python
from swiftshadow import QuickProxy
from swiftshadow.classes import ProxyInterface

# Get a proxy quickly
proxy = QuickProxy(countries=["US"], protocol="http")
print(proxy.as_string())

# Use ProxyInterface for more control
proxy_manager = ProxyInterface(countries=["US"], protocol="http", autoRotate=True)
print(proxy_manager.get().as_string())
```

---

## Documentation

Explore the full documentation to learn more about `swiftshadow`:

- [API Reference](proxyInterface.md): Detailed documentation for all classes and functions.
- [Examples](examples.md): Practical examples to help you get started.

---

## Why Swiftshadow?

- **Lightweight**: Minimal dependencies and easy to integrate.
- **Extensible**: Add custom providers and extend functionality.
- **Reliable**: Built-in validation ensures only working proxies are used.
- **Open Source**: Free to use and modify under the MIT License.
