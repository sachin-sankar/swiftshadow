from pathlib import Path
from swiftshadow.classes import ProxyInterface
from swiftshadow.models import Proxy
from appdirs import user_cache_dir


def test_basic_proxy():
    swift = ProxyInterface(debug=True)
    assert isinstance(swift.get(), Proxy)


def test_proxy_country_filter():
    swift = ProxyInterface(countries=["US"], debug=True)
    assert isinstance(swift.get(), Proxy)


def test_proxy_rotation():
    swift = ProxyInterface(debug=True)
    first = swift.get()
    swift.rotate()
    second = swift.get()
    assert first != second


def test_proxy_auto_rotation():
    swift = ProxyInterface(debug=True, autoRotate=True)
    first = swift.get()
    second = swift.get()
    assert first != second


def test_log_file():
    _ = ProxyInterface(debug=True, logToFile=True)
    logPath = Path(user_cache_dir(appname="swiftshadow")).joinpath("swiftshadow.log")

    with open(logPath, "rt") as file:
        text = file.read()
        assert text != "", True
