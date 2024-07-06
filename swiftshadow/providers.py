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
                continue
            proxy = [f'{proxy['host']}:{proxy['port']}',proxy['protocol']]
            if checkProxy(proxy):
                results.append(proxy)
                count += 1
    return results

def Thespeedx(max,countries=[],protocol='http'):
    results = []
    count =0
    raw = get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt').text
    for line in raw.splitlines():
        if count == max:
            break
        proxy = [line,'http']
        if checkProxy(proxy):
            results.append(proxy)
            print(proxy,True)
            count +=1
        else:
            continue
    return results
        
def ProxyScrape(max,countries=[],protocol='http'):
    baseUrl = 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=ipport&format=json'
    results = []
    count = 0
    if len(countries) == 0:
        apiUrl = baseUrl + '&country=all'
    else:
        apiUrl = baseUrl + '&country=' + ','.join([i.upper() for i in countries])
    raw = get(apiUrl).json()
    for ipRaw in raw['proxies']:
        if count == max:
            break
        proxy = [ipRaw['proxy'],'http']  
        if checkProxy(proxy):
            results.append(proxy)
            count += 1
        else:
            print(proxy,False)
            continue
    return results          

Providers = [{'provider':Monosans,'countryFilter':True,'protocols':['http']},{'provider':Thespeedx,'countryFilter':False,'protocols':['http']},{'provider':ProxyScrape,'countryFilter':True,'protocols':['http']}]
