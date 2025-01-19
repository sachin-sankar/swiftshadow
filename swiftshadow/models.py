from dataclasses import dataclass
from typing import Literal


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
