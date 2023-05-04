from swiftshadow.constants import CountryCodes
from requests import get
from datetime import datetime


def getCountryCode(countryName):
    try:
        return CountryCodes[countryName]
    except KeyError:
        for name in list(CountryCodes.keys()):
            if countryName in name:
                return CountryCodes[name]


def checkProxy(proxy, countries):
    if countries != []:
        if proxy[-1].upper() not in countries:
            return False
    proxyDict = {proxy[1]: proxy[0]}
    try:
        resp = get(f"{proxy[1]}://ipinfo.io/ip", proxies=proxyDict, timeout=2).text
        if resp.count(".") == 3:
            return True
        return False
    except Exception as e:
        # log('error',str(e))
        return False


def log(level, message):
    level = level.upper()
    print(
        f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - [swiftshadow] - {level} : {message}'
    )
