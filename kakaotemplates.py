import crawling
import categorize

def keywords(keyword):
    if keyword in list(crawling.basicCard_keywords.values()):
        return basicCard(keyword, carousel=False)
    return basicCard(keyword, carousel=True)

def basicCard(keyword, carousel=True):
    _googleprojectzero = crawling.googleprojectzero()

    if carousel:
        data = categorize.diverge(keyword)
        if data == []:
            return False

        items = list()
        count = 0
        for d in data:
            # 뉴스 기사가 10개 이상일 경우 break
            if count == 10: break
            count += 1

            items.append({
                "title": d["title"],
                "description": d["author"] + " | " + d["date"],
                "thumbnail": {
                    "imageUrl": d["img"]
                },
                "buttons": [
                    {
                        "action": "webLink",
                        "label": "자세히 보기",
                        "webLinkUrl": d["link"]
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

    else:
        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": "구글 프로젝트 제로에 대한 최신 이슈",
                            "description": _googleprojectzero["title"] + "\n" + _googleprojectzero["date"],
                            "thumbnail": {
                                "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                            },
                            "buttons": [
                                {
                                    "action": "webLink",
                                    "label": "자세히 보기",
                                    "webLinkUrl": _googleprojectzero["link"]
                                }
                            ]
                        }
                    }
                ]
            }
        }


# 리스트 메시지 템플릿
def listcard(news_title):
    data = []

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": news_title
                        },
                        "items": data
                    }
                }
            ]
        }
    }

# SimpleText 템플릿
def simpleText():
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "최신 보안 이슈를 알려주는 보안봇입니다!\n\n보안뉴스, 데일리시큐, wired 등 원하는 뉴스를 볼 수 있습니다.\n\n'보안', '안내', '키워드' 를 입력하면 확인 가능한 뉴스 리스트를 볼 수 있습니다.\n\n원하는 키워드가 들어간 최신 뉴스 기사를 볼 수 있습니다.\n\n채팅창에 '솔라윈즈', '제로데이' 와 같은 핫한 보안 키워드를 입력해보세요."
                    }
                }
            ]
        }
    }

# 바로가기 응답 템플릿
def quickReplies():
    data = []
    for d in list(crawling.carousel_keywords.keys()) + list(crawling.basicCard_keywords.keys()):

        data.append({
            "messageText": d,
            "action": "message",
            "label": d
        })

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "보안 서비스"
                    }
                }
            ],
            "quickReplies": data
        }
    }
