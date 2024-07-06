from requests import get
from random import choice
from json import dump, load
from swiftshadow.helpers import log
from swiftshadow.providers import Providers
import swiftshadow.cache as cache
import logging
import sys

logger = logging.getLogger("swiftshadow")
logger.setLevel(logging.INFO)
logFormat = logging.Formatter("%(asctime)s - %(name)s [%(levelname)s]:%(message)s")
streamhandler = logging.StreamHandler(stream=sys.stdout)
streamhandler.setFormatter(logFormat)
logger.addHandler(streamhandler)


class Proxy:
    def __init__(
        self,
        countries: list = [],
        protocol: str = "http",
        maxProxies: int = 10,
        autoRotate: bool = False,
        cachePeriod: int = 10,
        cacheFolder: str = "",
        debug: bool = False,
        logToFile: bool = False,
    ):
        """
        The one class for everything.

        Proxy class contains all necessary methods required to use swiftshadow.

        Args:
                countries: ISO 3166-2 Two letter country codes to filter proxies.
                protocol: HTTP/HTTPS protocol to filter proxies.
                maxProxies: Maximum number of proxies to store and rotate from.
                autoRotate: Rotates proxy when `Proxy.proxy()` function is called.
                cachePeriod: Time to cache proxies in minutes.
                cacheFolder: Folder to store cache file.
                debug: Sets Log Level to Debug.
                logToFile: Whether to pipe log to a log file. If cacheFolder is set log file is saved there.

        Returns:
                proxyClass (swiftshadow.Proxy): `swiftshadow.Proxy` class instance

        Examples:
                Simplest way to get a proxy
                >>> from swiftshadow.swiftshadow import Proxy
                >>> swift = Proxy()
                >>> print(swift.proxy())
                {'http':'192.0.0.1:8080'}
        Note:
                Proxies are sourced from **Proxyscrape** and **Scrapingant** websites which are freely available and validated locally.
        """
        self.countries = [i.upper() for i in countries]
        self.protocol = protocol
        self.maxProxies = maxProxies
        self.autoRotate = autoRotate
        self.cachePeriod = cachePeriod
        if cacheFolder == "":
            self.cacheFilePath = ".swiftshadow.json"
        else:
            self.cacheFilePath = f"{cacheFolder}/.swiftshadow.json"
        if debug:
            logger.setLevel(logging.DEBUG)
        if logToFile:
            if cacheFolder == "":
                logFilePath = "swiftshadow.log"
            else:
                logFilePath = f"{cacheFolder}/swiftshadow.log"
            fileHandler = logging.FileHandler(logFilePath)
            fileHandler.setFormatter(logFormat)
            logger.addHandler(fileHandler)
        self.update()

    def update(self):
        try:
            with open(self.cacheFilePath, "r") as file:
                data = load(file)
                self.expiry = data[0]
                expired = cache.checkExpiry(self.expiry)
            if not expired:
                logger.info(
                    "Loaded proxies from cache",
                )
                self.proxies = data[1]
                self.expiry = data[0]
                self.current = self.proxies[0]
                return
            else:
                logger.info(
                    "Cache expired. Updating cache.",
                )
        except FileNotFoundError:
            logger.info("No cache found. Cache will be created after update")

        self.proxies = []
        for providerDict in Providers:
            if self.protocol not in providerDict["protocols"]:
                continue
            if (len(self.countries) != 0) and (not providerDict["countryFilter"]):
                continue
            self.proxies.extend(
                providerDict["provider"](self.maxProxies, self.countries, self.protocol)
            )
            if len(self.proxies) >= self.maxProxies:
                break
        if len(self.proxies) == 0:
            logger.warning(
                "No proxies found for current settings. To prevent runtime error updating the proxy list again.",
            )
            self.update()
        with open(self.cacheFilePath, "w") as file:
            self.expiry = cache.getExpiry(self.cachePeriod).isoformat()
            dump([self.expiry, self.proxies], file)
        self.current = self.proxies[0]

    def rotate(self):
        """
        Rotate the current proxy.

        Sets the current proxy to a random one from available proxies and also validates cache.

        Note:
                Function only for manual rotation. If `autoRotate` is set to `True` then no need to call this function.
        """
        if cache.checkExpiry(self.expiry):
            self.update()
        self.current = choice(self.proxies)

    def proxy(self):
        """
        Returns a proxy dict.

        Returns:
                proxyDict (dict):A proxy dict of format `{protocol:address}`
        """
        if cache.checkExpiry(self.expiry):
            self.update()
        if self.autoRotate == True:
            return choice(self.proxies)
        else:
            return self.current
