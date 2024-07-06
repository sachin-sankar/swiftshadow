Swiftshadow integrates very well with `requests` library and can be used with it seamlessly.

```py
from swiftshadow import QuickProxy
from requests import get
proxy = QuickProxy()
resp = get('https://checkip.amazonaws.com',proxies={proxy[1]:proxy[0]})
print(resp.text)

```
Hopefully you should get a `ipv4` address that is not yours.