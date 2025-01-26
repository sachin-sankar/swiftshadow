# Swiftshadow

![PyPI - Downloads](https://img.shields.io/pypi/dm/swiftshadow)  
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/sachin-sankar/swiftshadow?include_prereleases&style=flat)

> [!WARNING]  
> **Heads up!** If you're using **versions 1.2.1 or below**, please note that **version 2.0.0 and above** includes breaking changes. Before upgrading, read the [documentation](https://sachin-sankar.github.io/swiftshadow/) to understand the changes and ensure compatibility with your code. If you encounter issues, please review the docs before opening a GitHub issue.

## About

**Swiftshadow** is a lightweight and efficient Python library designed to simplify IP proxy rotation for web scraping, data mining, and other automated tasks. It helps you bypass common challenges like IP bans, rate limits, and detection mechanisms, ensuring smooth and uninterrupted data collection.

### Key Features
- **Speed**: Optimized for fast proxy retrieval and rotation.
- **Reliability**: Automatically switches to working proxies if one fails.
- **Customization**: Configure proxy filters, rotation frequency, and caching behavior.
- **Low Dependencies**: Only one third-party dependency (`requests`), making it easy to use and maintain.
- **Caching**: Built-in caching mechanism to reduce load times and improve performance.

Whether you're a seasoned developer or a beginner, **Swiftshadow** makes proxy management effortless.

---

## Installation

Install the library using pip:

```bash
pip install swiftshadow
```

---

## Quick Start

### Get a Proxy in 2 Lines
Fetch a random proxy with just two lines of code:

```python
from swiftshadow import QuickProxy

print(QuickProxy())  # Output: http://<ip>:<port>
```

### Advanced Usage
For more control, use the `ProxyInterface` class:

```python
from swiftshadow.classes import ProxyInterface

# Fetch HTTPS proxies from the US
swift = ProxyInterface(countries=["US"], protocol="https")
print(swift.get().as_string())  # Output: https://<ip>:<port>
```

---

## Documentation

Explore the full documentation to learn more about **Swiftshadow**'s features and advanced usage:

📚 [Documentation](https://sachin-sankar.github.io/swiftshadow/)

---

## Why Swiftshadow?

- **Lightweight**: Minimal dependencies and easy to integrate.
- **Flexible**: Supports filtering by country and protocol.
- **Scalable**: Ideal for both small scripts and large-scale scraping projects.
- **Open Source**: Free to use, modify, and contribute to under the MIT License.

---

## Contributing

Contributions are welcome! If you'd like to improve **Swiftshadow**, feel free to open an issue or submit a pull request on [GitHub](https://github.com/sachin-sankar/swiftshadow).

---

## License

**Swiftshadow** is licensed under the MIT License. See the [LICENSE](https://github.com/sachin-sankar/swiftshadow/blob/main/LICENSE) file for details.
