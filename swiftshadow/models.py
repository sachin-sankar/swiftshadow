from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Coroutine, Literal


@dataclass
class Proxy:
    """
    Class representing a Proxy object.

    Attributes:
        ip: IP Address of the proxy.
        port: Port associated with the proxy.
        protocol: Protocol type of the proxy.

    """

    ip: str
    protocol: Literal["http", "https"]
    port: int

    def as_requests_dict(self) -> dict[Literal["http", "https"], str]:
        """
        Return proxy in requests commpatible dict format.

        Returns:
            dict: Dict representation of Proxy class.
        """
        return {self.protocol: f"{self.ip}:{self.port}"}

    def as_string(self) -> str:
        """
        Return proxy in a string of format
        <protocol>://<ip>:<port>

        Returns:
            string: Proxy in string format.
        """
        return f"{self.protocol}://{self.ip}:{self.port}"


@dataclass
class CacheData:
    """
    Class repersenting data structure if the cache in cache file.

    Attributes:
        expiryIn: Expiry date object.
        configString: Configuration String for the ProxyInterface this cache was created.
        proxies: Proxies to head.
    """

    expiryIn: datetime
    configString: str
    proxies: list[Proxy]


@dataclass
class Provider:
    """
    Class repersenting a Provider.

    Attributes:
        providerFunction: Callable function for this provider.
        countryFilter: Whether the provider supports country based filters.
        protocols: Protocols supported by the provider.
    """

    providerFunction: Callable[
        [list[str], Literal["http", "https"]], Coroutine[Any, Any, list[Proxy]]
    ]
    countryFilter: bool
    protocols: list[Literal["http", "https"]]
