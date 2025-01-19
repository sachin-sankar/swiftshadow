from swiftshadow.models import Proxy


def test_proxy():
    proxy = Proxy(ip="0.0.0.0", protocol="http", port=8000)
    assert proxy.as_requests_dict() == {"http": "0.0.0.0:8000"}
