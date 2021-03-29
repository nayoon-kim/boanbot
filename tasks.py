from celery.decorators import task
from utils import basicCard_keywords
import json
from _redis import redis
from crawler import Crawler

crawler = Crawler()

@task(name="crawling_process")
def crawling_process():
    from hub import Hub
    hub = Hub()
    
    if len(redis.keys()) > 0:
        for keyword in redis.keys():
            result = hub.diverge(keyword)
            redis.set(keyword, result)

    else:
        for keyword in basicCard_keywords:
            result = hub.diverge(keyword)
            # redis에는 key=keyword, value=list를 str로 바꿈(str이 아니면 에러가 남)
            redis.set(keyword, result)
