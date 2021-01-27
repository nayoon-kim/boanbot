import crawling

def diverge(keyword):
    data = ""
    if keyword == "주간 핫 뉴스":
        data = weekly_hot_news()
    elif keyword == "컨퍼런스":
        data = conference()
    elif keyword == "취약점 경고 및 버그리포트":
        data = warning_and_bugreport()
    elif keyword == "사건사고":
        data = incidents()
    elif keyword == "주의 이슈":
        data = issues()
    elif keyword == "다크웹":
        data = darkweb()
    elif keyword == "올해 보안 전망":
        data = this_year_security_prospect()
    elif keyword == "최신 보안 뉴스":
        data = newest_news()
    elif keyword == "해외 보안 뉴스(한글)":
        data = foreign_news_korean()
    elif keyword == "해외 보안 뉴스(영어)":
        data = foreign_news_english()
    elif keyword == "의료 보안":
        data = medical_security()

    return data

# 컨퍼런스
def conference():
    url = "https://www.dailysecu.com/"
    result = crawling.dailysecu_conference(url)

    return result

# 주간 핫 뉴스
# 보안뉴스 '가장 많이 본 기사[주간]'
def weekly_hot_news():
    url = "https://www.boannews.com/media/o_list.asp"
    result = crawling.boannews(url)
    return result

# 취약점 경고 및 버그리포트
def warning_and_bugreport():
    url = "https://www.boannews.com/media/s_list.asp?skind=5"
    result = crawling.boannews(url)

    return result

# 사건사고
def incidents():
    url = "https://www.boannews.com/search/news_total.asp?search=key_word&find=%BB%E7%B0%C7%BB%E7%B0%ED"
    result = crawling.boannews(url)

    return result

# 주의 이슈
def issues():
    url = "https://www.dailysecu.com/news/articleList.html?sc_serial_code=SRN2&view_type=sm"
    result = crawling.dailysecu_news(url)

    return result

# 다크웹
def darkweb():
    url = "https://www.boannews.com/search/news_total.asp?search=title&find=%B4%D9%C5%A9%C0%A5"
    result = crawling.boannews(url)

    return result

# 올해 보안 전망
def this_year_security_prospect():
    url = "https://www.boannews.com/search/news_total.asp?search=title&find=2021%B3%E2%BA%B8%BE%C8%C0%FC%B8%C1"
    result = crawling.boannews(url)

    return result

# 최신 보안 뉴스
def newest_news():
    url = "https://www.boannews.com/media/t_list.asp"
    result = crawling.boannews(url)

    return result

# 해외 보안 뉴스(한글)
def foreign_news_korean():
    url = "https://www.dailysecu.com/news/articleList.html?sc_serial_code=SRN4&view_type=sm"
    result = crawling.dailysecu_news(url)

    return result

# 해외 보안 뉴스(영어)
def foreign_news_english():
    url = "https://www.wired.com/category/security/"
    result = crawling.wired(url)

    return result

# 의료 보안
def medical_security():
    url = "https://www.dailysecu.com/news/articleList.html?sc_serial_code=SRN5&view_type=sm"
    result = crawling.dailysecu_news(url)

    return result
