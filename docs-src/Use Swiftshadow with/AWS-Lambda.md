Using swiftshadow with AWS Lambda normally would raise an error as the cache mechanism wont work properly due to the read only file permission. To fix this you can pass `cacheFolder="tmp"` when creating a `Proxy` class.

```py
from swiftshadow.classes import Proxy

swift = Proxy(cacheFolder="tmp")
```

If you don't want the caching behaviour try using the [`QuickProxy`](/Getting%20Started/Using-QuickProxy/) function.