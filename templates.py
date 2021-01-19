import crawling
import json

def templates():
    return {
        "version": "2.0",
        "template": {
            "outputs": [

            ]
        }
    }
def list_item(news_title):
    data = []

    _boannews = crawling.newest_news(news_title)
    count = 1
    for bn in _boannews:
        if count == 6 : break
        _temp = dict()
        _temp["title"] = _boannews[bn]["title"]
        _temp["description"] = _boannews[bn]["date"] + " | " + _boannews[bn]["author"]
        _temp["link"] = {"web" : _boannews[bn]["link"]}
        data.append(_temp)
        count += 1

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

def boan_news():
    _boannews = crawling.boannews()
    _templates = templates()

    _templates["template"]["outputs"] = list()
    _templates["template"]["outputs"].append(_boannews)

    return json.dumps(_templates, ensure_ascii=False)

print(list_item("보안뉴스"))