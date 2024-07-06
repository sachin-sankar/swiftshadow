## Basic Usage

To get a random `HTTP` proxy from any country
``` py
from swiftshadow.classes import Proxy
swift = Proxy()

print(swift.proxy())
```
!!! note
    When the `swift.Proxy` class instance is created for the first time the `Proxy.update()` function is called. This method updates the proxy list from Providers so it will take around 10 seconds to do so. This will also repeat after the `cachePeriod`

`Proxy.proxy()` method returns a proxy in dict form. See about it in reference.
This is the most basic usage of swiftshadow but wait it got more stuff.

!!! note
    From now on all example will exclude the import statement for the sake of simplicity.

## Filtering Proxies
You can filter and get proxies based on country of origin or SSL enabled (HTTPS) proxies.
### Country Filter
To filter proxies based on countries pass a list of countries as a **two letter code** when initialising the `swiftshadow.Proxy` class.

- For the list of countries and their two letter code visit [this wikipedia page.](https://en.m.wikipedia.org/wiki/ISO_3166-2)

```py title="country filtered"
swift = Proxy(countries=['US','IN'])
```

### Protocol Filter
By default all proxies are `HTTP` for **SSL** enabled `HTTPS` proxies set the parameter `protocol` to `https`
``` py title="HTTPS filter"
swift = Proxy(protocol='https')
```

!!! warning
    There is no validation done by swiftshadow on country codes or protocol as of now. This means if you pass in invalid country codes or protocol then there will be no proxies available to choose from.
    

## Proxy Rotation
### Manual Rotation 
You can manually rotate proxies using the `rotate()` method. This will choose a random proxy from available proxies.
``` py
from swiftshadow.classes import Proxy
swift = Proxy()

print(swift.proxy())
swift.rotate()
print(swift.proxy())
```
### Auto Rotation
Proxies can be rotated automatically by setting the parameter `autoRotate` to `True` when initialising the `Proxy` object. When auto rotate is set to true proxy is rotated everytime `proxy()` method is called.
``` py
from swiftshadow.classes import Proxy
swift = Proxy(autoRotate=True)

print(swift.proxy())
print(swift.proxy())
```

Visit [Refrences](../references.md) for more information on methods.