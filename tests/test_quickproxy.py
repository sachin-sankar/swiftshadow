from swiftshadow import QuickProxy
from swiftshadow.models import Proxy


def test_quickProxy():
    proxy = QuickProxy()
    assert isinstance(proxy, Proxy)
