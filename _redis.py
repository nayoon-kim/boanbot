import _redis
import json

class Redis:
    def __init__(self):
        self.REDIS = _redis.Redis(host="redis", port=6379, db=1, decode_responses=True)
        self.REDIS.flushdb()
        print("-------------------REDIS START-------------------\nREDIS PING:\n PONG(", REDIS.ping(), ")")

    def get(self, key):
        return self.REDIS.get(key)

    def set(self, key, value):
        if str(type(value)) == "<class 'list'>":
            self.REDIS.set(key, json.dumps(value, ensure_ascii=False))
        else:
            self.REDIS.set(key, value)
