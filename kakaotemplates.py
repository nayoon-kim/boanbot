import crawling
import categorize

def keywords(keyword):
    if keyword in crawling.basicCard_keywords:
        return basicCard(keyword, carousel=False)
    return basicCard(keyword, carousel=True)

def basicCard(keyword, carousel=True):
    _googleprojectzero = crawling.googleprojectzero()
    data = categorize.diverge(keyword)

    if data == []:
        return False

    if carousel:
        items = list()
        count = 0
        for d in data:
            if count == 10:
                break
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
                            "description": _googleprojectzero["headline1"]["title"] + "\n" + _googleprojectzero["headline1"]["date"],
                            "thumbnail": {
                                "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                            },
                            "buttons": [
                                {
                                    "action": "webLink",
                                    "label": "자세히 보기",
                                    "webLinkUrl": _googleprojectzero["headline1"]["link"]
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
def simpleText(name):
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": name
                    }
                }
            ]
        }
    }

# 바로가기 응답 템플릿
def quickReplies():
    data = []
    for d in crawling.carousel_keywords + crawling.basicCard_keywords:
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