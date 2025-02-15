from datetime import datetime, timedelta, timezone


def getExpiry(timeToLive: int) -> datetime:
    """
    Fetch a datetime object representing the cache expiry based on TTL.

    Args:
        timeToLive(int): Time in minutes the cache should expire.

    Returns:
        expiry(datetime): Datetime object representing the expiry time.
    """
    now = datetime.now(timezone.utc)
    expiry = now + timedelta(minutes=timeToLive)
    return expiry


def checkExpiry(expiryDate: datetime) -> bool:
    """
    Check if a expiry date object has expired.

    Args:
        expiryDate(datetime): Expiry date object.

    Returns:
        expiry(bool): Expire Status.
    """
    now = datetime.now(timezone.utc)
    if (now - expiryDate).days < 0:
        return False
    else:
        return True
