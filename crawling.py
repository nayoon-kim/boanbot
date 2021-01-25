import requests
import json
from datetime import time
from bs4 import BeautifulSoup

urls = {"fireeye": "https://www.fireeye.com/blog.html", "googleprojectzero": "https://googleprojectzero.blogspot.com", "보안뉴스": "http://boannews.com", "지디넷": "https://www.zdnet.com", "wired": "https://www.wired.com", "포브스": "https://www.forbes.com", "데일리시큐": "https://www.dailysecu.com"}
carousel_keywords = ["최신 보안 뉴스", "해외 보안 뉴스(한글)", "해외 보안 뉴스(영어)", "사건사고", "주의 이슈", "다크웹", "올해 보안 전망", "의료 보안", "주간 핫 뉴스", "취약점 경고 및 버그리포트", "컨퍼런스"]
basicCard_keywords = ["구글제로프로젝트"]
basic_image_url = ""

# threat research -> 취약점 분석
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
        result[headline]["link"] = urls["fireeye"] + c['href']

    result_json = json.dumps(result, ensure_ascii=False)
    print(result_json)

# News and updates from the Project Zero team at Google
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

    return result


# 한국 지디넷코리아가 아님
def zdnet_security():
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
        result[headline]["link"] = urls['지디넷'] + hn['href']
    for i, hnd in enumerate(headline_news_details):
        headline = "headline" + str(i+1)
        result[headline]["author"] = hnd.find("a").text
        result[headline]["date"] = hnd.find("span")['data-date']

    result_json = json.dumps(result, ensure_ascii=False)
    print(result_json)

def forbes():
    url = "https://www.forbes.com"

def boannews(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    news = soup.select('div.news_list')

    result = list()
    for n in news:
        result.append({
            "title": n.select("span.news_txt")[0].text,
            "link": urls["보안뉴스"] + n.find("a")['href'],
            "img": urls["보안뉴스"] + n.find("img")["src"] if n.find("img") is not None else basic_image_url,
            "author": n.select("span.news_writer")[0].text.split(' | ')[0],
            "date": n.select("span.news_writer")[0].text.split(' | ')[1]
        })

    return result

def dailysecu_news(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    news = soup.select('div.list-block')

    result = list()

    for n in news:
        author_and_date = n.select("div.list-dated")[0].text.split(' | ')[1:3]

        result.append({
            "title": n.select_one("div.list-titles").text,
            "link": urls['데일리시큐'] + n.select_one("div.list-titles a")["href"],
            "img": image(urls['데일리시큐'] + n.select_one("div.list-titles a")["href"], "div.IMGFLOATING"),
            "author": author_and_date[0],
            "date": author_and_date[1]
        })

    return result

def dailysecu_conference(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    news = soup.select('div.index-columns.grid-2.width-321')

    print(news)


def image(url, option):
    _soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return urls['데일리시큐'] + _soup.select_one(option + " img")["src"] if _soup.select_one(
        option) is not None else basic_image_url


# def wired(url):
#     webpage = requests.get(url)
#     soup = BeautifulSoup(webpage.text, "html.parser")
#
#     news = soup.select("div.cards-component div.card-component li")
#
#     result = list()
#     print(len(news))
#     for n in news:
#         print(n)
#         print('\n')
#         # result.append({
#         #     "title" : n.select_one('a h2').text,
#         #     "link" : urls['wired'] + n.select_one('a').text,
#         #     "img" : n.select_one('div.image-group-component img')['src'],
#         #     "author" : n.select_one('a.byline-component__link').text,
#         #     "date" : date(urls['wired'] + n.select_one('a').text),
#         # })
#
#     return result

def date(url):
    _soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return _soup.select_one("div.content-header__row.content-header__title-block time").text


# print(wired("https://www.wired.com/category/security"))
#side-scroll-in > div:nth-child(1) > div > div > div:nth-child(4) > a > img

dailysecu_conference("https://www.dailysecu.com/")