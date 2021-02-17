from celery.decorators import task
import crawling
import categorize
# import redis

# REDIS = redis.Redis(host="127.0.0.1", port=6379, db=1)

@task(name="say_hello")
def say_hello():
    print("Hello, celery")

@task(name="crawling_process")
def crawling_process():
    for keyword in crawling.carousel_keywords:
        result = categorize.diverge(keyword)
        # redis에는 key keyword에 list result가 들어감
        # REDIS.set(keyword, result)
        return result
