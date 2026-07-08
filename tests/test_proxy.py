from asyncio import run
from os import remove
from pathlib import Path

from appdirs import user_cache_dir

from swiftshadow.classes import ProxyInterface
from swiftshadow.models import Proxy
from swiftshadow.providers import Providers


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


def test_async_update():
    cacheFilePath = Path(user_cache_dir(appname="swiftshadow")).joinpath(
        "swiftshadow.pickle"
    )
    try:
        remove(cacheFilePath)
    except FileNotFoundError:
        pass
    swift = ProxyInterface(autoUpdate=False, debug=True)
    run(swift.async_update())
    assert isinstance(swift.get(), Proxy)


def test_async_update_autorotate():
    cacheFilePath = Path(user_cache_dir(appname="swiftshadow")).joinpath(
        "swiftshadow.pickle"
    )
    remove(cacheFilePath)
    swift = ProxyInterface(autoUpdate=False, autoRotate=True, debug=True)
    run(swift.async_update())
    assert isinstance(swift.get(), Proxy)
    assert isinstance(swift.get(), Proxy)


def test_provider_selection():
    selectedProvider = list(Providers.keys())[0]
    swift = ProxyInterface(selectedProviders=[selectedProvider], debug=True)
    proxy = swift.get()
    assert isinstance(proxy, Proxy)
    assert swift.providers[0] == Providers[selectedProvider]
