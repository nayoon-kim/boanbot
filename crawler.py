from bs4 import BeautifulSoup
from utils import dateFormat
import requests

class Crawler:
    boannews_url = "https://www.boannews.com/"
    dailysecu_url = "https://www.dailysecu.com/news/articleList.html"
    wired_url = "https://www.wired.com/"
    def boannews_(self, url, full_path=False):
        return "https://www.boannews.com/" + url if not full_path else url
    def dailysecu_(self, url, full_path=False):
        return "https://www.dailysecu.com/news/articleList.html" + url if not full_path else url
    def wired_(self, url, full_path=False):
        return "https://www.wired.com/" + url if not full_path else url
    def googlezeroprojects_(self, url, full_path=False):
        return "https://googleprojectzero.blogspot.com/" + url if not full_path else url

    def boannews(self, url):
        webpage = requests.get(self.boannews_(url))
        soup = BeautifulSoup(webpage.text, "html.parser")

        news = soup.select('div.news_list')
        print(self.boannews_(url))
        result = list()
        for n in news:
            result.append({
                "title": n.select("span.news_txt")[0].text,
                "link": self.boannews_url + n.find("a")['href'],
                "img": self.boannews_url + n.find("img")["src"] if n.find("img") is not None else "",
                "author": n.select("span.news_writer")[0].text.split(' | ')[0],
                "date": n.select("span.news_writer")[0].text.split(' | ')[1]
            })

        return result

    def dailysecu(self, url):
        webpage = requests.get(self.dailysecu_(url))
        soup = BeautifulSoup(webpage.text, "html.parser")

        news = soup.select('div.list-block')

        result = list()
        for n in news:
            result.append({
                "title": n.select_one("div.list-titles").text,
                "link": self.dailysecu_url + n.select_one("div.list-titles a")["href"],
                "img": self.dailysecu_url + '.'.join(n.select_one("div.list-image")["style"].split('.')[1:3]) if n.select_one("div.list-image") is not None else "",
                "author": n.select_one("div.list-dated").text.split(' | ')[1],
                "date": dateFormat(n.select_one("div.list-dated").text.split(' | ')[2])
            })

        return result

    def wired(self, url):
        webpage = requests.get(self.wired_(url))
        soup = BeautifulSoup(webpage.text, "html.parser")

        news = soup.select("div.primary-grid-component div.card-component")

        result = list()
        for n in news:
            description = n.select_one('li.card-component__description')
            result.append({
                "title": description.select_one('a h2').text,
                "link": self.wired_url + description.select_one('a')['href'],
                "img": n.select_one('li.card-component__image').select_one('div.image-group-component img')['src'],
                "author": description.select_one('a.byline-component__link').text,
                "date": self.wired_date(self.wired_url + description.select_one('a')['href']),
            })

        return result

    def wired_date(self, url):
        _soup = BeautifulSoup(requests.get(url).text, "html.parser")
        date = _soup.select_one("div.content-header__row.content-header__title-block time").text

        # 시간 포맷
        # wired date format: 02.18.2021 05:01 PM
        date = date.split()
        m, d, y = date[0].split('.')
        h, _m = date[1].split(':')
        h = str(int(h) + 12 if date[2] == 'PM' else 0)

        return "%s년 %s월 %s일 %s:%s" % (y, m, d, h, _m)

    # News and updates from the Project Zero team at Google
    def googlezeroprojects(self, url):
        webpage = requests.get(self.googlezeroprojects_(url))
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

    def query_(self, where, url, category):
        path = ""
        # boannews
        if where == "boannews":
            path = url + "?search=title&find=" + category.encode('euc-kr')
        # dailysecu
        elif where == "dailysecu":
            path = url + "?sc_area=A&view_type=sm&sc_word=" + category

        return path