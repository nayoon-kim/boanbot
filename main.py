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
        if client_utterance in quickReplies_keywords:
            templates = self.templates.quickReplies()
        elif client_utterance in basicCard_keywords:
            data = self.hub.distribute(client_utterance)
            templates = self.templates.basicCard(data)
        else:
            valid_check = self.hub.distribute(client_utterance)
            templates = self.templates.basicCard(valid_check) if valid_check is not None else self.templates.quickReplies()

        return templates