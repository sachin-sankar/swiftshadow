Swiftshadow integrates very well with `requests` library and can be used with it seamlessly.

```py
from swiftshadow import QuickProxy
from requests import get

resp = get('https://ip.me',proxies=QuickProxy())
print(resp.text)

```
Hopefully you should get a `ipv6` address that is not yours.