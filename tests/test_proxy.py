from swiftshadow.classes import Proxy


def test_basic_proxy():
    swift = Proxy()
    assert isinstance(swift.proxy(), list)


def test_proxy_country_filter():
    swift = Proxy(countries=["US"])
    assert isinstance(swift.proxy(), list)
