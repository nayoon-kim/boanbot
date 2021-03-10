import json
from django_redis import cache


class Redis:
    def __init__(self):
        cache.flushdb()
        print("-------------------REDIS START-------------------\nREDIS PING:\n PONG(", cache.ping(), ")")

    def get(self, key):
        return json.loads(cache.get(key))

    def set(self, key, value):
        if str(type(value)) == "<class 'list'>":
            cache.set(key, json.dumps(value, ensure_ascii=False))
        else:
            cache.set(key, value)

    def keys(self, pattern='*'):
        return cache.keys(pattern=pattern)

redis = Redis()
