from requests import get
from random import choice
from datetime import datetime, timezone, timedelta
from pickle import dump, load


class Proxy:
    def __init__(self, country=None, protocol="http", maxProxies=10, autoRotate=False):
        self.country = country
        self.protocol = protocol
        self.maxProxies = maxProxies
        self.autoRotate = autoRotate
        self.update()

    def checkIp(self, ip, cc, protocol):
        if (ip[1] == cc or cc == None) and ip[2] == protocol:
            proxy = {ip[2]: ip[0]}
            try:
                oip = get(f"{protocol}://ipinfo.io/ip", proxies=proxy, timeout=5).text
            except:
                return False
            if oip.count(".") == 3 and oip != self.mip:
                return True
            else:
                return False
        else:
            return False

    def checkCache(self, latestTimeString, cache=datetime.now(timezone.utc)):
        latest = datetime.strptime(latestTimeString + " UTC", "%Y-%m-%d %H:%M:%S %Z")
        latest = latest.replace(tzinfo=timezone.utc)
        expiry = latest + timedelta(minutes=10)
        live = cache - latest
        dead = expiry - cache
        if live.seconds / 60 < 10.0 and dead.seconds / 60 < 10.0:
            cacheValid = True
        else:
            cacheValid = False
        return cacheValid

    def update(self):
        raw = get("https://free-proxy-list.net/").text
        try:
            with open(".swiftshadow.dat", "rb") as file:
                data = load(file)
                cacheState = self.checkCache(
                    raw.split("UTC")[0].split("Updated at")[-1].strip(), data[0]
                )
            if cacheState:
                print("[ swiftshadow ] Loaded proxies from cache")
                self.proxies = data[1]
                self.current = self.proxies[0]
                return
            else:
                print("[ swiftshadow ] Cache expired. Updating cache...")
        except FileNotFoundError:
            print("[ swiftshadow ] No cache found. Creating cache... ")
        self.mip = get("https://ipinfo.io/ip").text
        raw = [
            i.split("<td>")
            for i in raw.split("<tbody>")[1].split("</tbody>")[0].split("</tr><tr>")
        ]
        raw = [
            [
                i[1].rstrip("</td>"),
                i[2].rstrip("</td>"),
                i[3].split("<", 1)[0],
                i[-1].split("hx", 1)[1][2],
            ]
            for i in raw
        ]
        final = [
            [i[0] + ":" + i[1], i[2], "https" if i[3] == "y" else "http"] for i in raw
        ]
        self.proxies = []
        for i in final:
            if self.checkIp(i, self.country, self.protocol):
                if len(self.proxies) == self.maxProxies:
                    break
                self.proxies.append({i[2]: i[0]})
        if len(self.proxies) == 0:
            print(
                "[ swiftshadow ] No proxies found for current settings. To prevent runtime error updating the proxy list again."
            )
            self.update()
        with open(".swiftshadow.dat", "wb") as file:
            dump([datetime.now(timezone.utc), self.proxies], file)

        self.current = self.proxies[0]

    def rotate(self):
        self.current = choice(self.proxies)

    def proxy(self):
        if self.autoRotate == True:
            return choice(self.proxies)
        else:
            return self.current


# a = Proxy(country='IN')
# print(a.proxies)
