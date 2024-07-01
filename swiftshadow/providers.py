from requests import get
from swiftshadow.helpers import checkProxy

def Monosans(max, countries=[],protocol="http"):
    raw = get('https://raw.githubusercontent.com/monosans/proxy-list/main/proxies.json').json()
    results = []
    count = 0
    for proxy in raw:
        if count == max:
            return results
        if proxy['protocol'] == protocol:
            if len(countries) != 0 and proxy['geolocation']['country']['iso_code'] not in countries:
                return
            proxy = [f'{proxy['host']}:{proxy['port']}',proxy['protocol'],proxy['geolocation']['country']['iso_code']]
            if checkProxy(proxy):
                results.append(proxy)
                count += 1
            
Providers = [Monosans]