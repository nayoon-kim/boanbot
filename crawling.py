import requests
import json
import datetime
from bs4 import BeautifulSoup

urls = ["https://www.fireeye.com/blog.html", "https://googleprojectzero.blogspot.com/", "http://boannews.com/", "https://www.zdnet.com/topic/security/", "https://www.wired.com/category/security/", "https://www.forbes.com"]

def boannews():
    url = "https://www.boannews.com/Default.asp"
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    headline_news = soup.select('#headline0 li')

    result = dict()
    for i, mn in enumerate(headline_news):
        headline = "headline" + str(i + 1)
        result[headline] = dict()
        result[headline]["title"] = mn.text
        result[headline]["link"] = mn['onclick']
        result[headline]["author"] = mn.text
        result[headline]["date"] = str(datetime.datetime.now())

    result_json = json.dumps(result, ensure_ascii=False)
    print(result_json)

def fireeye():
    url = "https://www.fireeye.com/blog/threat-research.html"
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")
    c11v9_links = soup.select('div.c11v9 a')

    result = dict()
    for i, c in enumerate(c11v9_links):
        headline = "headline" + str(i + 1)
        result[headline] = {}
        result[headline]["date"] = c.find("p").text
        result[headline]["title"] = c.find("h4").text
        result[headline]["link"] = c['href']

    result_json = json.dumps(result, ensure_ascii=False)
    print(result_json)


def googleprojectzero():
    url = "https://googleprojectzero.blogspot.com/"
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    headline_news = soup.select('h2.date-header span')
    headline_title = soup.select('h3.post-title.entry-title a')

    result = dict()
    result["headline1"] = dict()
    result["headline1"]["date"] = headline_news[0].text
    result["headline1"]["title"] = headline_title[0].text
    result["headline1"]["link"] = headline_title[0]['href']

    result_json = json.dumps(result, ensure_ascii=False)
    print(result_json)



def zdnet():
    url = "https://www.zdnet.com/topic/security/"
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    headline_news = soup.select('#topic-river-latest div.content h3 a')
    headline_news_details = soup.select('#topic-river-latest div.content p.meta')

    result = dict()
    for i, hn in enumerate(headline_news):
        headline = "headline" + str(i+1)
        result[headline] = dict()
        result[headline]["title"] = hn.text
        result[headline]["link"] = hn['href']
    for i, hnd in enumerate(headline_news_details):
        headline = "headline" + str(i+1)
        result[headline]["author"] = hnd.find("a").text
        result[headline]["date"] = hnd.find("span")['data-date']

    result_json = json.dumps(result, ensure_ascii=False)
    print(result_json)


def wired_security():
    url = "https://www.wired.com/category/security/"
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    headline_news_link = soup.select('li.card-component__description a')
    headline_news_title = soup.select('li.card-component__description a h2')
    headline_news_author = soup.select('li.card-component__description a.byline-component__link')

    result = dict()
    for i, hn in enumerate(headline_news_title):
        headline = "headline" + str(i+1)
        result[headline] = dict()
        result[headline]["title"] = hn.text
        result[headline]["link"] = headline_news_link[1 + 3*i]['href']
        # print(hn)

    for i, hn in enumerate(headline_news_author):
        headline = "headline" + str(i+1)
        result[headline]["author"] = hn.text

    result_json = json.dumps(result, ensure_ascii=False)
    print(result_json)


def forbes():
    url = "https://www.forbes.com"



# boannews()
# fireeye()
# googleprojectzero()
# zdnet()
wired_security()
# forbes()