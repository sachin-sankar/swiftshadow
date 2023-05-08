from requests import get
from swiftshadow.helpers import getCountryCode, checkProxy, log


def Scrapingant(max, countries=[], protocol="http"):
    result = []
    count = 0
    raw = get("https://scrapingant.com/proxies").text
    rows = [i.split("<td>") for i in raw.split("<tr>")]

    def clean(text):
        return text[: text.find("<")].strip()

    for row in rows[2:]:
        if count == max:
            return result
        zprotocol = clean(row[3]).lower()
        if zprotocol != protocol:
            continue
        cleaned = [
            clean(row[1]) + ":" + clean(row[2]),
            protocol,
            getCountryCode(clean(row[4].split(" ", 1)[1])),
        ]
        if checkProxy(cleaned, countries):
            result.append({cleaned[1]: cleaned[0]})
            count += 1
    return result


def Proxyscrape(max, countries=[], protocol="http"):
    result = []
    count = 0
    query = "https://api.proxyscrape.com/v2/?timeout=5000&request=displayproxies&protocol=http"
    if countries == []:
        query += "&country=all"
    else:
        query += "&country=" + ",".join(countries)
    if protocol == "https":
        query += "&ssl=yes"
    ips = get(query).text
    for ip in ips.split("\n"):
        if count == max:
            return result
        proxy = [ip.strip(), protocol, "all"]
        if checkProxy(proxy, []):
            result.append({proxy[1]: proxy[0]})
            count += 1
    return result


Providers = [Proxyscrape, Scrapingant]
