import json
import redis

class Redis:
    def __init__(self):
        self.redis = redis.Redis(host="redis", port=6379, db=2, decode_responses=True)
        print("-------------------REDIS START-------------------\nREDIS PING:\n PONG(", self.redis.ping(), ")")

    def get(self, key):
        if self.redis.get(key) is None:
            return []
        return json.loads(self.redis.get(key))

    def set(self, key, value):
        if str(type(value)) == "<class 'list'>":
            self.redis.set(key, json.dumps(value, ensure_ascii=False))
        else:
            self.redis.set(key, value)

    def keys(self, pattern='*'):
        return self.redis.keys(pattern=pattern)

redis = Redis()
