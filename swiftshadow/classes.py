from requests import get


class ScrapingAnt:
    def __init__(self):
        self.update()

    def update(self):
        raw = get("https://scrapingant.com/proxies").text
        rows = [i.split("<td>") for i in raw.split("<tr>")]
        data = []

        def clean(text):
            return text[: text.find("<")].strip()

        for row in rows[2:]:
            cleaned = [clean(row[1]) + ":" + clean(row[2]), clean(row[3]).lower()]
            data.append(cleaned)
        print(data)


a = ScrapingAnt()
