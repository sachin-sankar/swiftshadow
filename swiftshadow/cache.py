from datetime import datetime, timezone, timedelta
from time import sleep


def getExpiry(expiryIn):
    now = datetime.now(timezone.utc)
    expiry = now + timedelta(minutes=expiryIn)
    return expiry


def checkExpiry(expiryDateObject):
    now = datetime.now(timezone.utc)
    if (now - expiryDateObject).days < 0:
        return False
    else:
        return True
