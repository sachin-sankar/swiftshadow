Swiftshadow integrates very well with `requests` library and can be used with it seamlessly.

```py
from swiftshadow.swiftshadow import Proxy
from requests import get

swift = Proxy()
resp = get('https://ip.me',proxies=swift.proxy())
print(resp.text)

```
Hopefully you should a `ipv6` address that is not yours.