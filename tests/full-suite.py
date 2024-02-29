from swiftshadow import QuickProxy
from swiftshadow.classes import Proxy

#print(QuickProxy())
#print(QuickProxy(countries=['us']))
#print(QuickProxy(protocol="https"))

swift = Proxy(logToFile=True)
print(swift.current)