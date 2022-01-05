"""A deduplication log using redis to log tasks"""
from json import dumps, loads
from math import ceil
from redis import from_url
from time import time

from .. import DeduplicationLog

class RedisDeduplicationLog(DeduplicationLog):
    """This deduplication log registers tasks in a redis backend to dedup.

    Task JSON is registered as key with the associated
    {'task_id': task_id, 'timestamp': timestamp} JSON dictionnary as value.
    Key and value are serialized using JSON into the redis database.

    Task are stored in the redis backend with an expire parameter of
    ceil(self.dedup_slot_s) to prevent to saturate the redis database with
    expired entries.
    """

    def __init__(self, dedup_slot_ms=0, redis_dedup_backend=None):
        """Create a new deduplication log using a redis backend

        redis_dedup_backend parameter must be an url of a redis database.
        """
        super(RedisDeduplicationLog, self).__init__(dedup_slot_ms)
        self.dedup_backend_connection = from_url(redis_dedup_backend)

    def register_task(self, task, task_id):
        """Store the task in the redis deduplication backend"""
        key = dumps(task)
        value = dumps({'task_id': task_id, 'timestamp': time()})
        self.dedup_backend_connection.set(key, value)
        self.dedup_backend_connection.expire(key, ceil(self.dedup_slot_s))

    def get_task(self, task):
        """Return existing task_id from dedup_backend or None"""
        value = self.dedup_backend_connection.get(dumps(task))
        if value:
            decoded_value = loads(value)
            if decoded_value['timestamp'] > time() - self.dedup_slot_s:
                return decoded_value['task_id']

        return None
