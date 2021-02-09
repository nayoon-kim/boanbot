import requests
import urllib.request
import json
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

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
            "date": dateFormat(author_and_date[1])
        })

    return result

# beautifulsoup는 오로지 html을 파싱하고 데이터를 크롤링하는 데에 쓰인다.
# selenium은 웹 애플리케이션을 위한 테스팅 프레임워크이다.
# 직접적으로 웹 사이트에 접근할 수 있게 해준다.
def dailysecu_conference(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(r"\home\ubuntu\chrome\chromedriver", chrome_options=chrome_options)
    driver.set_window_size(1010, 700)
    driver.implicitly_wait(time_to_wait=5)
    driver.get(url=url)

    req = driver.page_source
    soup = BeautifulSoup(req, "html.parser")
    news = soup.select('div.clearfix.auto-pad-20.box-skin.line div.banner_box a')

    result = list()
    for i, n in enumerate(news):
        driver.get(n['href'])
        sleep(0.1)
        driver.save_screenshot("media/" + str(i+1) + ".png")

        result.append({
            "title": "컨퍼런스",
            "author": "nayoon",
            "date": "2021.01.27",
            "link": n['href'],
            "img": "",
        })

    driver.close()
    print(result)
    return result

def image(url, option):
    _soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return urls['데일리시큐'] + _soup.select_one(option + " img")["src"] if _soup.select_one(
        option) is not None else basic_image_url

def wired(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")

    news = soup.select("div.primary-grid-component div.card-component")

    result = list()
    for n in news:
        description = n.select_one('li.card-component__description')
        image = n.select_one('li.card-component__image')
        result.append({
            "title" : description.select_one('a h2').text,
            "link" : urls['wired'] + description.select_one('a')['href'],
            "img" : image.select_one('div.image-group-component img')['src'],
            "author" : description.select_one('a.byline-component__link').text,
            "date" : date(urls['wired'] + description.select_one('a')['href']),
        })

    return result

def date(url):
    _soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return _soup.select_one("div.content-header__row.content-header__title-block time").text

def dateFormat(date):
    date_str, time = date.split()
    year, mon, day = date_str.split('-')

    return year + "년 "+ mon + "월 " + day + "일 " + time

# POST 방식
def dailysecu_query_news(parameter):
    url = "https://www.dailysecu.com/news/articleList.html"
    data = "sc_area=A&view_type=sm&sc_word=" + parameter
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))

    soup = BeautifulSoup(response.read().decode('utf-8'), "html.parser")
    news = soup.select('div.list-block')
    result = list()

    if news != None:
        for n in news:
            author_and_date = n.select("div.list-dated")[0].text.split(' | ')[1:3]

            result.append({
                "title": n.select_one("div.list-titles").text,
                "link": urls['데일리시큐'] + n.select_one("div.list-titles a")["href"],
                "img": image(urls['데일리시큐'] + n.select_one("div.list-titles a")["href"], "div.IMGFLOATING"),
                "author": author_and_date[0],
                "date": dateFormat(author_and_date[1])
            })

    return result

# GET 방식
def boannews_query_news(parameter):
    url = "https://www.boannews.com/search/news_total.asp"
    params = {"search": "title", "find": parameter.encode('euc-kr')}
    query_url = requests.get(url, params).url

    return boannews(query_url)

def query(parameter):
    result = list()
    result.extend(dailysecu_query_news(parameter))
    result.extend(boannews_query_news(parameter))

    return result
