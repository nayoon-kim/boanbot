import requests
import json
from datetime import time
from bs4 import BeautifulSoup

urls = ["https://www.fireeye.com/blog.html", "https://googleprojectzero.blogspot.com/", "http://boannews.com/", "https://www.zdnet.com/topic/security/", "https://www.wired.com/category/security/", "https://www.forbes.com", "https://www.dailysecu.com/news/articleList.html?sc_section_code=S1N2&view_type=sm"]

# 최신 보안 뉴스
def boannews():
    url = "https://www.boannews.com/media/t_list.asp"
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    headline_news = soup.select('div.news_list')
    # print(headline_news)
    result = dict()
    for i, hn in enumerate(headline_news):
        headline = str(i + 1)
        result[headline] = dict()
        result[headline]["title"] = hn.select("span.news_txt")[0].text
        result[headline]["link"] = hn.select("a")[0]['href']
        result[headline]["author"] = hn.select("span.news_writer")[0].text.split(' | ')[0]
        result[headline]["date"] = hn.select("span.news_writer")[0].text.split(' | ')[1]

    return result

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
        result[headline]["link"] = c['href']

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

    result_json = json.dumps(result, ensure_ascii=False)
    print(result_json)


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
        result[headline]["link"] = hn['href']
    for i, hnd in enumerate(headline_news_details):
        headline = "headline" + str(i+1)
        result[headline]["author"] = hnd.find("a").text
        result[headline]["date"] = hnd.find("span")['data-date']

    result_json = json.dumps(result, ensure_ascii=False)
    print(result_json)

# 최신 보안 뉴스
def wired_security():
    url = "https://www.wired.com"
    security_feature = "/category/security"
    webpage = requests.get(url + security_feature)
    soup = BeautifulSoup(webpage.text, "html.parser")

    headline_news = soup.select("div.cards-component__row li.card-component__description")
    result = dict()
    for i, hn in enumerate(headline_news):
        headline = str(i + 1)
        result[headline] = dict()
        result[headline]["title"] = hn.select('a h2')[0].text
        result[headline]["link"] = hn.select('a')[0]['href']
        result[headline]["author"] = hn.select('a.byline-component__link')[0].text

        _soup = BeautifulSoup(requests.get(url+result[headline]["link"]).text, "html.parser")
        result[headline]["date"] = _soup.select_one("div.content-header__row.content-header__title-block time").text

    # result_json = json.dumps(result, ensure_ascii=False)
    # print(result_json)
    return result


def forbes():
    url = "https://www.forbes.com"

# 최신 보안 뉴스
def dailysecu():
    url = "https://www.dailysecu.com/news/articleList.html?sc_section_code=S1N2&view_type=sm"
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    headline_news = soup.select('div.list-block')

    result = dict()
    for i, hn in enumerate(headline_news):
        author_and_date = hn.select("div.list-dated")[0].text.split(' | ')[1:3]

        headline = str(i + 1)
        result[headline] = dict()
        result[headline]["title"] = hn.select("div.list-titles")[0].text
        result[headline]["link"] = hn.select("div.list-titles")[0].find("a")["href"]

        result[headline]["author"] = author_and_date[0]
        result[headline]["date"] = author_and_date[1]

    return result


def newest_news():
    # 추가되었으면 하는 기능
    # 두 개의 기사를 비교해서 비슷한 내용일 경우 하나의 헤드라인을 삭제하는 식.
    # 각각 총 5개의 기사를 가져온다고 했을 때, 최악의 비교 횟수 5 * 5 * 5

    _boannews = boannews()
    _wired_security = wired_security()
    _dailysecu = dailysecu()

    result = dict()
    for i in range(1, 6):

        number = str(i)

        b_number = str(i)
        w_number = str(i+5)
        d_number = str(i+10)

        result[b_number] = dict()
        result[b_number]["title"] = _boannews[number]["title"]
        result[b_number]["link"] = _boannews[number]["link"]
        result[b_number]["author"] = _boannews[number]["author"]
        result[b_number]["date"] = _boannews[number]["date"]

        result[w_number] = dict()
        result[w_number]["title"] = _wired_security[number]["title"]
        result[w_number]["link"] = _wired_security[number]["link"]
        result[w_number]["author"] = _wired_security[number]["author"]
        result[w_number]["date"] = _wired_security[number]["date"]

        result[d_number] = dict()
        result[d_number]["title"] = _dailysecu[number]["title"]
        result[d_number]["link"] = _dailysecu[number]["link"]
        result[d_number]["author"] = _dailysecu[number]["author"]
        result[d_number]["date"] = _dailysecu[number]["date"]

    return result
    # result_json = json.dumps(result, ensure_ascii=False)
    # return result_json

def news_to_redis(self):

    # 서버에서 1시간에 한번씩 이슈를 가지고 와서 레디스의 이슈를 최신 이슈로 변경한다.
    # newest_news -> redis / 가장 최근 이슈와의 date를 비교 후 삽입시도

    # 일단 15개 밖에 없기 때문에, redis를 모두 지우고 redis에 다시 삽입.



    return self


# fireeye()
# googleprojectzero()
# zdnet_security()
# forbes()