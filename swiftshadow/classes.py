from requests import get
from random import choice
from datetime import datetime, timezone, timedelta
from json import dump, load
from swiftshadow.helpers import log
from swiftshadow.providers import Proxyscrape, Scrapingant, Providers
import swiftshadow.cache as cache
import os


class Proxy:
    def __init__(
        self,
        countries: list = [],
        protocol: str = "http",
        maxProxies: int = 10,
        autoRotate: bool = False,
        cachePeriod: int = 10,
        cacheFolder: str = "",
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
        if cacheFolder != "":
            self.cacheFilePath = ".swiftshadow.json"
        else:
            self.cacheFilePath = f"{cacheFolder}/.swiftshadow.json"

        self.update()

    def checkIp(self, ip, cc, protocol):
        if (ip[1] == cc or cc == None) and ip[2] == protocol:
            proxy = {ip[2]: ip[0]}
            try:
                oip = get(f"{protocol}://ipinfo.io/ip", proxies=proxy).text
            except:
                return False
            if oip.count(".") == 3 and oip != self.mip:
                return True
            else:
                return False
        else:
            return False

    def update(self):
        try:
            with open(self.cacheFilePath, "r") as file:
                data = load(file)
                self.expiry = data[0]
                expired = cache.checkExpiry(self.expiry)
            if not expired:
                log(
                    "info",
                    f"Loaded proxies from cache",
                )
                self.proxies = data[1]
                self.expiry = data[0]
                self.current = self.proxies[0]
                return
            else:
                log(
                    "info",
                    f"Cache expired. Updating cache...",
                )
        except FileNotFoundError:
            log("error", "No cache found. Cache will be created after update")

        self.proxies = []
        self.proxies.extend(Proxyscrape(self.maxProxies, self.countries, self.protocol))
        if len(self.proxies) != self.maxProxies:
            self.proxies.extend(
                Scrapingant(self.maxProxies, self.countries, self.protocol)
            )
        if len(self.proxies) == 0:
            log(
                "warning",
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


class ProxyChains:
    def __init__(
        self, countries: list = [], protocol: str = "http", maxProxies: int = 10
    ):
        self.countries = [i.upper() for i in countries]
        self.protocol = protocol
        self.maxProxies = maxProxies
        self.update()

    def update(self):
        proxies = []
        for provider in Providers:
            print(len(proxies))
            if len(proxies) == self.maxProxies:
                break
            log("INFO", f"{provider}")
            for proxyDict in provider(self.maxProxies, self.countries, self.protocol):
                proxyRaw = list(proxyDict.items())[0]
                proxy = f'{proxyRaw[0]} {proxyRaw[1].replace(":"," ")}'
                proxies.append(proxy)
        proxies = "\n".join(proxies)
        configFileName = "swiftshadow-proxychains.conf"
        config = f"random_chain\nchain_len=1\nproxy_dns\n[ProxyList]\n{proxies}"
        with open(configFileName, "w") as file:
            file.write(config)
        cmd = f"proxychains -f {os.path.abspath(configFileName)}"
        os.system(cmd)
