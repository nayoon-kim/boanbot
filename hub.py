from _redis import Redis
import json
from crawler import Crawler

class Hub:
    category_in_boannews = {"최신 보안 뉴스" : "media/t_list.asp", "올해 보안 전망": "search/news_total.asp?search=title&find=2021%B3%E2%BA%B8%BE%C8%C0%FC%B8%C1", "다크웹": "search/news_total.asp?search=title&find=%B4%D9%C5%A9%C0%A5", "사건사고":"search/news_total.asp?search=key_word&find=%BB%E7%B0%C7%BB%E7%B0%ED", "취약점 경고 및 버그리포트":"media/s_list.asp?skind=5", "주간 핫 뉴스":"media/o_list.asp", "query": "search/news_total.asp"}
    category_in_dailysecu = {"의료 보안": "?sc_serial_code=SRN5&view_type=sm", "해외 보안 뉴스(한글)":"?sc_serial_code=SRN4&view_type=s", "주의 이슈": "?sc_serial_code=SRN2&view_type=sm"}
    category_in_wired = {"해외 보안 뉴스(영어)": "category/security/"}
    category_in_googlezeroprojects = {"구글제로프로젝트": ""}

    crawler = Crawler()
    redis = Redis()

    def distribute(self, category):
        result = self.diverge(category) if not self.redis.get(category) else self.redis.get(category)

        if not self.redis.get(category): self.redis.set(category, result)

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
            result = self.crawler.boannews(self.crawler.query("boannews", self.category_in_boannews["query"], category))
        return result