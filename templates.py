from utils import basicCard_keywords

class KakaoTemplates:
    # 바로가기 응답 템플릿
    def quickReplies(self):
        data = []
        # 바로가기 항목 추가 부분
        for keyword in basicCard_keywords:
            data.append({
                "messageText": keyword,
                "action": "message",
                "label": keyword
            })

        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "최신 보안 이슈를 알려주는 보안봇입니다!\n\n보안뉴스, 데일리시큐, 와이어드 등 원하는 뉴스를 볼 수 있습니다.\n\n 뉴스 카테고리는 아래와 같습니다. 원하는 카테고리를 클릭하세요!\n\n원하는 키워드가 들어간 최신 뉴스 기사를 볼 수 있습니다.\n\n채팅창에 '솔라윈즈', '제로데이' 와 같은 핫한 보안 키워드를 입력해보세요."
                        }
                    }
                ],
                "quickReplies": data
            }
        }

    def basicCard(self, data):
        items = list()
        count = 0
        for _data in data:
            # 뉴스 기사가 15개 이상일 경우 break
            if count == 15: break
            count += 1

            items.append({
                "title": _data["title"],
                "description": _data["author"] + " | " + _data["date"],
                "thumbnail": {
                    "imageUrl": _data["img"]
                },
                "buttons": [
                    {
                        "action": "webLink",
                        "label": "자세히 보기",
                        "webLinkUrl": _data["link"]
                    }
                ]
            })

        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": items
                        }
                    }
                ]
            }
        }
