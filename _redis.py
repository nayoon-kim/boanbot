import redis
import json

class Redis:
    def __init__(self):
        self.REDIS = redis.Redis(host="redis", port=6379, db=1, decode_responses=True)
        self.REDIS.flushdb()
        print("-------------------REDIS START-------------------\nREDIS PING:\n PONG(", self.REDIS.ping(), ")")

    def get(self, key):
        return self.REDIS.get(key)

    def set(self, key, value):
        if str(type(value)) == "<class 'list'>":
            self.REDIS.set(key, json.dumps(value, ensure_ascii=False))
        else:
            self.REDIS.set(key, value)

    def isEmpty(self):
        if self.REDIS.dbsize() > 0:
            return False
        return True

    def keys(self, pattern='*'):
        return self.REDIS.keys(pattern=pattern)
