from celery.decorators import task
import crawling
import categorize
import redis
import json

REDIS = redis.Redis(host="redis", port=6379, db=1, decode_responses=True)
REDIS.flushdb()

print("-------------------REDIS START-------------------\nREDIS PING:\n PONG(", REDIS.ping(), ")")

@task(name="say_hello")
def say_hello():
    print("Hello, celery")

@task(name="crawling_process")
def crawling_process():
    for keyword in crawling.carousel_keywords:
        result = categorize.diverge(keyword)
        print(crawling.carousel_keywords[keyword], json.dumps(result, ensure_ascii=False))
        # redis에는 key=keyword, value=list를 str로 바꿈(str이 아니면 에러가 남)
        REDIS.set(crawling.carousel_keywords[keyword], json.dumps(result, ensure_ascii=False))
