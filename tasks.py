from celery.decorators import task
import crawling
import categorize
import redis
import json

REDIS = redis.Redis(host="redis", port=6379, db=1, decode_responses=True)

print("-------------------REDIS START-------------------\nREDIS PING:\n PONG(", REDIS.ping(), ")")

@task(name="say_hello")
def say_hello():
    print("Hello, celery")

@task(name="crawling_process")
def crawling_process():
    for keyword in crawling.carousel_keywords:
        result = categorize.diverge(crawling.carousel_keywords[keyword])
        # redis에는 key keyword에 list result가 들어감
        REDIS.set(name=keyword, value=json.dumps(result))
