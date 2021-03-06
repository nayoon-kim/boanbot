from _redis import redis
import tasks
from crawler import Crawler

class Hub:
    category_in_boannews = {"보안뉴스" : "/media/t_list.asp", "올해 보안 전망": "/search/news_total.asp?search=title&find=2021%B3%E2%BA%B8%BE%C8%C0%FC%B8%C1", "다크웹": "/search/news_total.asp?search=title&find=%B4%D9%C5%A9%C0%A5", "사건사고":"/search/news_total.asp?search=key_word&find=%BB%E7%B0%C7%BB%E7%B0%ED", "취약점 경고 및 버그리포트":"/media/s_list.asp?skind=5", "주간 핫 뉴스":"/media/o_list.asp", "query": "/search/news_total.asp"}
    category_in_dailysecu = {"데일리시큐" : "/news/articleList.html?sc_section_code=S1N2&view_type=sm", "의료 보안": "/news/articleList.html?sc_serial_code=SRN5&view_type=sm", "해외 보안 뉴스":"/news/articleList.html?sc_serial_code=SRN4&view_type=sm", "주의 이슈": "/news/articleList.html?sc_serial_code=SRN2&view_type=sm", "query": "/news/articleList.html"}
    category_in_wired = {"와이어드": "/category/security/"}
    category_in_googlezeroprojects = {"구글제로프로젝트": ""}
    query_site = "보안뉴스"

    crawler = Crawler()

    def distribute(self, category):
        if not redis.get(category):
            result = self.diverge(category)
            if result != []:
                redis.set(category, result)
        else:
            result = redis.get(category)

        return result

    def diverge(self, category):
        result = ""
        if category in self.category_in_boannews:
            result = self.crawler.boannews(self.category_in_boannews[category])
        elif category in self.category_in_dailysecu:
            result = self.crawler.dailysecu(self.category_in_dailysecu[category])
        elif category in self.category_in_wired:
            result = self.crawler.wired(self.category_in_wired[category])
        elif category in self.category_in_googlezeroprojects:
            result = self.crawler.googlezeroprojects(self.category_in_googlezeroprojects[category])
        else:
            if self.query_site == "보안뉴스":
                result = self.crawler.boannews(self.crawler.query_path("보안뉴스", self.category_in_boannews["query"], category))
            elif self.query_site == "데일리시큐":
                result = self.crawler.dailysecu(self.crawler.query_path("데일리시큐", self.category_in_dailysecu["query"], category))
        return result
