from hub import Hub
from templates import KakaoTemplates
from utils import quickReplies_keywords, basicCard_keywords

class Messages:
    hub = Hub()
    templates = KakaoTemplates()

    def reply(self, client_utterance):
        return self.analyze(client_utterance)

    # client_utterance에 따른 templates 해석
    def analyze(self, client_utterance):
        # quickReplies_keywords = ['보안', '안내', '키워드']
        if client_utterance in quickReplies_keywords:
            templates = self.templates.quickReplies()
        # basicCard_keywords = ['보안뉴스', '데일리시큐', '와이어드', '주의 이슈', '다크웹', '사건사고', '취약점 경고 및 버그리포트', '주간 핫 뉴스', '올해 보안 전망', '의료 보안', '구글제로프로젝트', '해외 보안 뉴스', ]
        elif client_utterance in basicCard_keywords:
            data = self.hub.distribute(client_utterance)
            templates = self.templates.basicCard(data)
        # 위의 키워드에 포함되지 않는 경우 검색
        else:
            valid_check = self.hub.distribute(client_utterance)
            templates = self.templates.basicCard(valid_check) if valid_check != [] else self.templates.quickReplies()

        return templates