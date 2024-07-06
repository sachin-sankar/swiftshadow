from requests import get
from datetime import datetime


def checkProxy(proxy):
    proxyDict = {proxy[1]: proxy[0]}
    try:
        resp = get(
            f"{proxy[1]}://checkip.amazonaws.com", proxies=proxyDict, timeout=2
        ).text
        if resp.count(".") == 3:
            return True
        return False
    except Exception as e:
        return False


def log(level, message):
    level = level.upper()
    print(
        f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - [swiftshadow] - {level} : {message}'
    )
