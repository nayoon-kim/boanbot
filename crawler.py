from bs4 import BeautifulSoup
from utils import dateFormat
import requests

class Crawler:
    def boannews_path(self, params=""):
        return "https://www.boannews.com" + params
    def dailysecu_path(self, params=""):
        return "https://www.dailysecu.com" + params
    def wired_path(self, params=""):
        return "https://www.wired.com" + params
    def googlezeroprojects_path(self, params=""):
        return "https://googleprojectzero.blogspot.com" + params
    def query_path(self, where, path, find):
        q_path = ""
        # boannews
        if where == "보안뉴스":
            params = {"search": "title", "find": find.encode('euc-kr')}
            q_path = path + "?" + (requests.get(self.boannews_path(path), params).url).split('?')[1]
        # dailysecu
        elif where == "데일리시큐":
            params = {"sc_area": "A", "view_type": "sm", "sc_word": find}
            q_path = path + "?" + (requests.get(self.dailysecu_path(path), params).url).split('?')[1]

        return q_path

    def boannews(self, params):
        webpage = requests.get(self.boannews_path(params))
        soup = BeautifulSoup(webpage.text, "html.parser")

        news = soup.select('div.news_list')
        print(self.boannews_path(params))
        result = list()
        for n in news:
            result.append({
                "title": n.select("span.news_txt")[0].text,
                "link": self.boannews_path(n.find("a")['href']),
                "img": self.boannews_path(n.find("img")["src"] if n.find("img") is not None else ""),
                "author": n.select("span.news_writer")[0].text.split(' | ')[0],
                "date": n.select("span.news_writer")[0].text.split(' | ')[1]
            })

        return result

    def dailysecu(self, params):
        webpage = requests.get(self.dailysecu_path(params))
        soup = BeautifulSoup(webpage.text, "html.parser")

        news = soup.select('div.list-block')

        result = list()
        for n in news:
            result.append({
                "title": n.select_one("div.list-titles").text,
                "link": self.dailysecu_path(n.select_one("div.list-titles a")["href"]),
                "img": self.dailysecu_path("/news" + ('.'.join(n.select_one("div.list-image")["style"].split('.')[1:2]) if n.select_one("div.list-image") is not None else "") + ".jpg"),
                "author": n.select_one("div.list-dated").text.split(' | ')[1],
                "date": dateFormat(n.select_one("div.list-dated").text.split(' | ')[2])
            })

        return result

    def wired(self, params):
        webpage = requests.get(self.wired_path(params))
        soup = BeautifulSoup(webpage.text, "html.parser")

        news = soup.select("div.primary-grid-component div.card-component")

        result = list()
        for n in news:
            description = n.select_one('li.card-component__description')
            result.append({
                "title": description.select_one('a h2').text,
                "link": self.wired_path(description.select_one('a')['href']),
                "img": n.select_one('li.card-component__image').select_one('div.image-group-component img')['src'],
                "author": description.select_one('a.byline-component__link').text,
                "date": self.wired_date(self.wired_path(description.select_one('a')['href'])),
            })

        return result

    def wired_date(self, path):
        _soup = BeautifulSoup(requests.get(path).text, "html.parser")
        date = _soup.select_one("div.content-header__row.content-header__title-block time").text

        # 시간 포맷
        # wired date format: 02.18.2021 05:01 PM
        date = date.split()
        m, d, y = date[0].split('.')
        h, _m = date[1].split(':')
        h = str(int(h) + 12 if date[2] == 'PM' else 0)

        return "%s년 %s월 %s일 %s:%s" % (y, m, d, h, _m)

    # News and updates from the Project Zero team at Google
    def googlezeroprojects(self, params):
        webpage = requests.get(self.googlezeroprojects_path(params))
        soup = BeautifulSoup(webpage.text, "html.parser")

        result = list()
        result.append({
            "title": soup.select_one('h3.post-title.entry-title a').text,
            "link": soup.select_one('h3.post-title.entry-title a')['href'],
            "img": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
            "author": "google zero projects",
            "date": soup.select_one('h2.date-header span').text,
        })
        return result
